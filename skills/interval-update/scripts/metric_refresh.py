#!/usr/bin/env python3
"""Small interval-owned metric refresh helpers.

These helpers return daily metric readings for `.farplane/metrics/daily`.
They intentionally do not write dashboard projections or fetch external APIs.
"""

from __future__ import annotations

import argparse
import json
from datetime import date as date_type
from datetime import timedelta
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


def parse_iso_datetime(value: Any) -> datetime | None:
    if not value:
        return None
    raw = str(value).strip()
    if not raw:
        return None
    try:
        if raw.endswith("Z"):
            raw = raw[:-1] + "+00:00"
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        try:
            parsed_date = date_type.fromisoformat(raw[:10])
        except ValueError:
            return None
        return datetime.combine(parsed_date, datetime.min.time(), tzinfo=timezone.utc)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def row_date(row: dict[str, Any]) -> str:
    raw = row.get("ts") or row.get("timestamp") or row.get("created_at") or row.get("date") or ""
    parsed = parse_iso_datetime(raw)
    return parsed.date().isoformat() if parsed else str(raw)[:10]


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            raw = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(raw, dict):
            rows.append(raw)
    return rows


def read_jsonl_glob(root: Path, pattern: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(root.glob(pattern)):
        rows.extend(read_jsonl(path))
    return rows


def content_row_date(row: dict[str, Any]) -> str | None:
    parsed = parse_iso_datetime(row.get("published_at"))
    return parsed.date().isoformat() if parsed else None


def select_content_metric_targets(
    content_ledger: Path,
    platform: str,
    kpi_key: str,
    date: str,
    window_days: int = 7,
) -> dict[str, Any]:
    """select_content_metric_targets(content_ledger, platform, kpi_key, date, window_days) -> fetch target packet."""
    if not content_ledger.exists():
        return {"status": "source_gap", "external_ids": [], "items": [], "payload": {"gaps": [f"missing:{content_ledger}"]}}
    until = date_type.fromisoformat(date) + timedelta(days=1)
    since = until - timedelta(days=window_days)
    rows = []
    for row in read_jsonl(content_ledger):
        if row.get("platform") != platform:
            continue
        if row.get("status") != "posted":
            continue
        if kpi_key not in (row.get("kpis") if isinstance(row.get("kpis"), list) else []):
            continue
        published_date = content_row_date(row)
        if published_date is None:
            continue
        parsed_date = date_type.fromisoformat(published_date)
        if since <= parsed_date < until:
            rows.append(row)
    external_ids = [
        str(row["external_id"])
        for row in rows
        if isinstance(row.get("external_id"), str) and row.get("external_id")
    ]
    if platform == "instagram":
        fetch_command = "python3 skills/instagram-account/scripts/fetch_metrics.py " + " ".join(
            f"--media-id {content_id}" for content_id in external_ids
        )
    elif platform == "x":
        fetch_command = "python3 skills/x-account/scripts/fetch_metrics.py " + " ".join(
            f"--tweet-id {content_id}" for content_id in external_ids
        )
    else:
        fetch_command = ""
    return {
        "status": "available" if external_ids else "source_gap",
        "external_ids": external_ids,
        "items": rows,
        "payload": {
            "platform": platform,
            "kpi_key": kpi_key,
            "window_days": window_days,
            "since_date": since.isoformat(),
            "until_date": until.isoformat(),
            "fetch_command": fetch_command,
            "gaps": [] if external_ids else ["no_posted_content_targets_for_window"],
        },
    }


def markdown_heading_section(markdown: str, heading: str) -> str:
    target = f"## {heading}"
    lines = markdown.splitlines()
    start: int | None = None
    for index, line in enumerate(lines):
        if line.strip() == target:
            start = index + 1
            break
    if start is None:
        return ""
    end = len(lines)
    for index in range(start, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return "\n".join(lines[start:end]).strip()


def parse_fenced_yaml_from_section(section: str) -> dict[str, Any]:
    fence_start = section.find("```yaml")
    if fence_start == -1:
        return {}
    yaml_start = section.find("\n", fence_start)
    fence_end = section.find("```", yaml_start + 1)
    if yaml_start == -1 or fence_end == -1:
        return {}
    loaded = yaml.safe_load(section[yaml_start + 1 : fence_end]) or {}
    return loaded if isinstance(loaded, dict) else {}


def parse_ticket_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text:
        return {}
    raw = text.split("\n---\n", 1)[0][4:]
    try:
        loaded = yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        loaded = {}
        for line in raw.splitlines():
            if ":" not in line or line.startswith(("  ", "- ")):
                continue
            key, value = line.split(":", 1)
            loaded[key.strip()] = value.strip().strip('"')
    if not isinstance(loaded, dict):
        return {}
    return {str(key): "" if value is None else str(value) for key, value in loaded.items()}


def iter_ticket_files(ticket_dir: Path) -> list[Path]:
    roots = [ticket_dir, ticket_dir / "archive"]
    tickets: list[Path] = []
    for root in roots:
        if root.exists():
            tickets.extend(root.glob("TASK-*/ticket.md"))
    return sorted(set(tickets))


def ticket_completion_date(fm: dict[str, str], fallback_date: str) -> str:
    for key in ("completed_at", "closed_at", "updated_at"):
        parsed = parse_iso_datetime(fm.get(key, ""))
        if parsed:
            return parsed.date().isoformat()
    return fallback_date


def ticket_is_complete(fm: dict[str, str]) -> bool:
    return fm.get("phase") == "complete" or fm.get("status") == "done"


def ticket_has_completion_proof(markdown: str) -> bool:
    done = markdown_heading_section(markdown, "Done / Proof") or markdown_heading_section(markdown, "Done")
    lowered = done.lower()
    return any(
        token in lowered
        for token in ("passed", "proof", "evidence", "artifact", "artifacts/", "review", "receipt", "verification")
    )


def parse_ticket_kpi_rewards(markdown: str) -> tuple[list[dict[str, str]], list[str]]:
    reward = markdown_heading_section(markdown, "Reward")
    if not reward:
        return [], ["missing_reward_section"]
    payload = parse_fenced_yaml_from_section(reward)
    raw_rewards = payload.get("kpi_rewards")
    if not isinstance(raw_rewards, list):
        return [], ["missing_kpi_rewards"]
    rewards: list[dict[str, str]] = []
    gaps: list[str] = []
    for index, raw_reward in enumerate(raw_rewards):
        if not isinstance(raw_reward, dict):
            gaps.append(f"invalid_kpi_reward:{index}")
            continue
        kpi_id = str(raw_reward.get("kpi_id") or "").strip()
        expected_reward = str(raw_reward.get("expected_reward") or "").strip()
        if not kpi_id:
            gaps.append(f"missing_kpi_id:{index}")
            continue
        rewards.append({"kpi_id": kpi_id, "expected_reward": expected_reward})
    return rewards, gaps


def count_ticket_kpi_rewards(ticket_dir: Path, date: str, kpi_key: str) -> dict[str, Any]:
    """count_ticket_kpi_rewards(ticket_dir, date, kpi_key) -> MetricReading."""
    count = 0
    tickets: list[dict[str, str]] = []
    gaps: list[str] = []
    root = ticket_dir.resolve()
    for ticket in iter_ticket_files(root):
        markdown = ticket.read_text(encoding="utf-8")
        fm = parse_ticket_frontmatter(ticket)
        if not fm or not ticket_is_complete(fm):
            continue
        if ticket_completion_date(fm, date) != date:
            continue
        relative_ticket = str(ticket.relative_to(root.parent if root.name == "tickets" else root))
        rewards, reward_gaps = parse_ticket_kpi_rewards(markdown)
        gaps.extend(f"{relative_ticket}:{gap}" for gap in reward_gaps)
        if not rewards:
            continue
        if not ticket_has_completion_proof(markdown):
            gaps.append(f"{relative_ticket}:missing_completion_proof")
            continue
        for reward in rewards:
            if reward["kpi_id"] != kpi_key:
                continue
            count += 1
            tickets.append(
                {
                    "ticket_id": fm.get("ticket_id") or ticket.parent.name,
                    "ticket": relative_ticket,
                    "expected_reward": reward.get("expected_reward", ""),
                }
            )
    return {
        "value": count,
        "status": "available",
        "payload": {"tickets": tickets, "gaps": gaps},
    }


def estimate_human_attention_minutes(times: list[datetime]) -> float:
    if not times:
        return 0.0
    ordered = sorted(times)
    total = 5.0
    for previous, current in zip(ordered, ordered[1:], strict=False):
        gap = max((current - previous).total_seconds() / 60.0, 1.0)
        total += min(gap, 30.0)
    return round(total, 2)


def accepted_reward_count(rows: list[dict[str, Any]], date: str) -> int:
    return len(
        [
            row
            for row in rows
            if row_date(row) == date and row.get("outcome") in {"positive", "partial_positive"} and row.get("evidence")
        ]
    )


def calculate_autonomy_time_ratio(runtime_dir: Path, date: str) -> dict[str, Any]:
    """calculate_autonomy_time_ratio(runtime_dir, date) -> MetricReading."""
    root = runtime_dir.resolve()
    event_rows = read_jsonl_glob(root, "events/*.jsonl")
    spawned_rows = read_jsonl(root / "automation" / "spawned-threads.jsonl")
    reward_rows = read_jsonl(root / "automation" / "rewards.jsonl")
    gaps = []
    if not (root / "events").exists():
        gaps.append("missing:events")
    if not (root / "automation" / "spawned-threads.jsonl").exists():
        gaps.append("missing:automation/spawned-threads.jsonl")
    if not (root / "automation" / "rewards.jsonl").exists():
        gaps.append("missing:automation/rewards.jsonl")
    if len(gaps) == 3:
        return {"value": None, "status": "source_gap", "payload": {"gaps": gaps}}

    spawned_thread_ids = {
        str(row.get("thread_id") or row.get("session_id"))
        for row in spawned_rows
        if row.get("thread_id") or row.get("session_id")
    }
    human_times_by_session: dict[str, list[datetime]] = {}
    for row in event_rows:
        if row_date(row) != date:
            continue
        if str(row.get("event_type") or row.get("type") or "") not in {"turn_start", "user_prompt", "prompt"}:
            continue
        session_id = str(row.get("session_id") or row.get("thread_id") or "unknown")
        if session_id in spawned_thread_ids:
            continue
        parsed = parse_iso_datetime(row.get("ts") or row.get("timestamp") or row.get("created_at") or row.get("date"))
        if parsed is not None:
            human_times_by_session.setdefault(session_id, []).append(parsed)

    spawned_today: dict[str, datetime] = {}
    latest_by_thread: dict[str, datetime] = {}
    rewarded_threads: set[str] = set()
    for row in spawned_rows:
        thread_id = str(row.get("thread_id") or row.get("session_id") or "")
        parsed = parse_iso_datetime(row.get("ts") or row.get("timestamp") or row.get("created_at") or row.get("date"))
        if not thread_id or parsed is None:
            continue
        if row_date(row) == date and str(row.get("status") or row.get("event") or "spawned") in {"spawned", "created", "started"}:
            spawned_today.setdefault(thread_id, parsed)
        if parsed.date().isoformat() <= date:
            latest_by_thread[thread_id] = max(parsed, latest_by_thread.get(thread_id, parsed))
        if row_date(row) == date and str(row.get("status") or row.get("event") or "").startswith("rewarded"):
            rewarded_threads.add(thread_id)

    autonomous_minutes = 0.0
    for thread_id, start in spawned_today.items():
        end = latest_by_thread.get(thread_id, start)
        elapsed = max((end - start).total_seconds() / 60.0, 0.0)
        autonomous_minutes += elapsed if elapsed > 0 else 30.0
    human_prompt_count = sum(len(times) for times in human_times_by_session.values())
    human_active_threads = len(human_times_by_session)
    human_minutes = sum(estimate_human_attention_minutes(times) for times in human_times_by_session.values())
    accepted_today = accepted_reward_count(reward_rows, date)
    ratio = autonomous_minutes / human_minutes if human_minutes else (autonomous_minutes if autonomous_minutes else 0.0)
    return {
        "value": round(float(ratio), 4),
        "status": "available",
        "payload": {
            "human_prompt_count": human_prompt_count,
            "human_active_thread_count": human_active_threads,
            "human_attention_minutes_estimated": round(float(human_minutes), 2),
            "autonomous_thread_count": len(spawned_today),
            "autonomous_worker_elapsed_minutes": round(float(autonomous_minutes), 2),
            "rewarded_autonomous_thread_count": len(rewarded_threads),
            "output_per_human_prompt": round(float(accepted_today / human_prompt_count), 4) if human_prompt_count else 0.0,
            "gaps": gaps,
        },
    }


def is_human_turn(row: dict[str, Any]) -> bool:
    actor = str(row.get("actor") or row.get("role") or row.get("source") or "").lower()
    if actor in {"assistant", "system", "automation", "tool"}:
        return False
    event_type = str(row.get("event_type") or row.get("type") or row.get("event") or "").lower()
    if event_type not in {"turn_start", "user_prompt", "prompt", "message"}:
        return False
    if str(row.get("is_initial_request") or "").lower() == "true":
        return False
    return actor in {"", "user", "human", "operator"} or "user" in actor or "human" in actor


def calculate_ticket_intervention_metrics(ticket_dir: Path, runtime_dir: Path, date: str) -> dict[str, Any]:
    """calculate_ticket_intervention_metrics(ticket_dir, runtime_dir, date) -> daily metrics map."""
    completed: dict[str, tuple[Path, str, datetime]] = {}
    gaps: list[str] = []
    ticket_root = ticket_dir.resolve()
    for ticket in iter_ticket_files(ticket_root):
        fm = parse_ticket_frontmatter(ticket)
        if not fm or not ticket_is_complete(fm):
            continue
        completed_at = parse_iso_datetime(fm.get("completed_at") or fm.get("closed_at") or fm.get("updated_at"))
        if completed_at is None or completed_at.date().isoformat() != date:
            continue
        markdown = ticket.read_text(encoding="utf-8")
        if not ticket_has_completion_proof(markdown):
            gaps.append(f"{ticket.parent.name}:missing_completion_proof")
            continue
        ticket_id = fm.get("ticket_id") or ticket.parent.name
        relative_ticket = str(ticket.relative_to(ticket_root.parent if ticket_root.name == "tickets" else ticket_root))
        completed[ticket_id] = (ticket, relative_ticket, completed_at)

    runtime_root = runtime_dir.resolve()
    association_rows = read_jsonl(runtime_root / "state" / "ticket-thread-associations.jsonl")
    if not association_rows:
        gaps.append("missing_ticket_thread_association_source")
    event_rows = read_jsonl_glob(runtime_root, "events/*.jsonl")
    if not (runtime_root / "events").exists():
        gaps.append("missing:events")

    associations_by_ticket: dict[str, list[dict[str, Any]]] = {}
    for row in association_rows:
        ticket_id = str(row.get("ticket_id") or "")
        if ticket_id:
            associations_by_ticket.setdefault(ticket_id, []).append(row)

    counted_tickets = 0
    intervention_free = 0
    total_interventions = 0
    items: list[dict[str, Any]] = []
    for ticket_id, (_ticket_path, relative_ticket, completed_at) in completed.items():
        associations = associations_by_ticket.get(ticket_id, [])
        if not associations:
            gaps.append(f"{relative_ticket}:missing_ticket_thread_association")
            continue
        thread_ids = {str(row.get("thread_id") or row.get("session_id")) for row in associations if row.get("thread_id") or row.get("session_id")}
        if len(thread_ids) != 1:
            gaps.append(f"{relative_ticket}:ambiguous_ticket_thread_association")
            continue
        association = associations[0]
        started_at = parse_iso_datetime(
            association.get("execution_started_at")
            or association.get("started_at")
            or association.get("created_at")
            or association.get("timestamp")
            or association.get("ts")
        )
        if started_at is None:
            gaps.append(f"{relative_ticket}:missing_execution_start")
            continue
        thread_id = next(iter(thread_ids))
        turn_count = 0
        for row in event_rows:
            if str(row.get("thread_id") or row.get("session_id") or "") != thread_id:
                continue
            if not is_human_turn(row):
                continue
            event_time = parse_iso_datetime(row.get("ts") or row.get("timestamp") or row.get("created_at") or row.get("date"))
            if event_time is not None and started_at < event_time <= completed_at:
                turn_count += 1
        counted_tickets += 1
        total_interventions += turn_count
        if turn_count == 0:
            intervention_free += 1
        items.append({"ticket_id": ticket_id, "ticket": relative_ticket, "intervention_turns": turn_count})

    if counted_tickets == 0:
        return {
            "auto_completion_rate": {"value": None, "status": "source_gap", "payload": {"gaps": gaps}},
            "intervention_free_ticket_count": {"value": None, "status": "source_gap", "payload": {"gaps": gaps}},
            "ticket_intervention_turn_count": {"value": None, "status": "source_gap", "payload": {"gaps": gaps}},
        }
    payload = {"tickets": items, "gaps": gaps}
    return {
        "auto_completion_rate": {"value": round(float(intervention_free / counted_tickets), 4), "status": "available", "payload": payload},
        "intervention_free_ticket_count": {"value": intervention_free, "status": "available", "payload": payload},
        "ticket_intervention_turn_count": {"value": total_interventions, "status": "available", "payload": payload},
    }


def print_json(payload: dict[str, Any]) -> int:
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect one interval metric reading.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    rewards = subparsers.add_parser("ticket-reward-count")
    rewards.add_argument("--ticket-dir", required=True)
    rewards.add_argument("--date", required=True)
    rewards.add_argument("--kpi-key", required=True)

    autonomy = subparsers.add_parser("autonomy-time-ratio")
    autonomy.add_argument("--runtime-dir", required=True)
    autonomy.add_argument("--date", required=True)

    interventions = subparsers.add_parser("ticket-intervention-metrics")
    interventions.add_argument("--ticket-dir", required=True)
    interventions.add_argument("--runtime-dir", required=True)
    interventions.add_argument("--date", required=True)

    content_targets = subparsers.add_parser("content-targets")
    content_targets.add_argument("--content-ledger", required=True)
    content_targets.add_argument("--platform", required=True)
    content_targets.add_argument("--kpi-key", required=True)
    content_targets.add_argument("--date", required=True)
    content_targets.add_argument("--window-days", type=int, default=7)

    args = parser.parse_args()
    if args.command == "ticket-reward-count":
        return print_json(count_ticket_kpi_rewards(Path(args.ticket_dir), args.date, args.kpi_key))
    if args.command == "autonomy-time-ratio":
        return print_json(calculate_autonomy_time_ratio(Path(args.runtime_dir), args.date))
    if args.command == "ticket-intervention-metrics":
        return print_json(calculate_ticket_intervention_metrics(Path(args.ticket_dir), Path(args.runtime_dir), args.date))
    if args.command == "content-targets":
        return print_json(
            select_content_metric_targets(
                Path(args.content_ledger),
                args.platform,
                args.kpi_key,
                args.date,
                args.window_days,
            )
        )
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
