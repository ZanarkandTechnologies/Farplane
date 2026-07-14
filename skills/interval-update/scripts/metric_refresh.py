#!/usr/bin/env python3
"""Small interval-owned metric refresh helpers.

These helpers return daily metric readings for `.farplane/metrics/daily`.
They intentionally do not write dashboard projections or fetch external APIs.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date as date_type
from datetime import timedelta
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from bin.core.farplane_metric_schema import observation_from_reading, write_metric_batch
except ImportError:  # pragma: no cover
    observation_from_reading = None
    write_metric_batch = None


def resolve_refresh_plan(
    metrics_file: Path,
    requested_metric_ids: list[str],
    date: str,
    fresh_metric_ids: set[str] | None = None,
) -> dict[str, Any]:
    """Resolve prompt jobs; the Interval agent executes them and writes results."""
    fresh = fresh_metric_ids or set()
    try:
        config = yaml.safe_load(metrics_file.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        return {"date": date, "refresh_groups": [], "skipped_metric_ids": [], "source_gaps": [f"invalid_metrics_config:{exc}"]}
    metrics = config.get("metrics") if isinstance(config, dict) else {}
    refreshers = config.get("refreshers") if isinstance(config, dict) else {}
    metrics = metrics if isinstance(metrics, dict) else {}
    refreshers = refreshers if isinstance(refreshers, dict) else {}
    jobs: dict[str, dict[str, Any]] = {}
    skipped: list[str] = []
    gaps: list[str] = []
    for metric_id in requested_metric_ids:
        if metric_id in fresh:
            skipped.append(metric_id)
            continue
        definition = metrics.get(metric_id)
        if not isinstance(definition, dict):
            gaps.append(f"unknown_metric:{metric_id}")
            continue
        refresh_ref = str(definition.get("refresh_ref") or "").strip()
        inline = str(definition.get("refresh") or "").strip()
        if bool(refresh_ref) == bool(inline):
            gaps.append(f"invalid_refresh_owner:{metric_id}")
            continue
        if inline:
            jobs[f"metric:{metric_id}"] = {"refresh_id": f"metric:{metric_id}", "refresh": inline.replace("<YYYY-MM-DD>", date), "provides": [metric_id], "requested_metric_ids": [metric_id]}
            continue
        refresher = refreshers.get(refresh_ref)
        if not isinstance(refresher, dict) or not str(refresher.get("refresh") or "").strip():
            gaps.append(f"missing_refresher:{metric_id}:{refresh_ref}")
            continue
        job = jobs.setdefault(refresh_ref, {"refresh_id": refresh_ref, "refresh": str(refresher["refresh"]).replace("<YYYY-MM-DD>", date), "provides": list(refresher.get("provides") or []), "requested_metric_ids": []})
        job["requested_metric_ids"].append(metric_id)
    return {"date": date, "refresh_groups": list(jobs.values()), "skipped_metric_ids": skipped, "source_gaps": gaps}


def resolve_interval_refresh_plan(interval_id: str, enabled: bool, *args: Any, **kwargs: Any) -> dict[str, Any]:
    if interval_id != "daily" or not enabled:
        return {"date": kwargs.get("date") or (args[2] if len(args) > 2 else None), "refresh_groups": [], "skipped_metric_ids": [], "source_gaps": [], "reason": "weekly_read_only" if interval_id == "weekly" else "refresh_disabled"}
    return resolve_refresh_plan(*args, **kwargs)


def record_refresh_result(project_root: Path, date: str, job: dict[str, Any], readings: dict[str, Any]) -> dict[str, Any]:
    """Normalize one agent-executed group result into flat metric observations."""
    if observation_from_reading is None or write_metric_batch is None:
        raise RuntimeError("Farplane metric schema is unavailable")
    observations = []
    gaps: list[str] = []
    for metric_id in job.get("requested_metric_ids", []):
        reading = readings.get(metric_id)
        if not isinstance(reading, dict):
            gaps.append(f"missing_refresh_output:{metric_id}")
            continue
        observations.append(observation_from_reading(metric_id, date, reading, {"refresh_id": job.get("refresh_id")}))
    path = write_metric_batch(project_root, str(job.get("refresh_id") or "metric_refresh"), date, observations, gaps=gaps, payload={"requested_metric_ids": job.get("requested_metric_ids", [])})
    return {"path": str(path), "observation_metric_ids": [row.metric_id for row in observations], "source_gaps": gaps}


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
        fetch_command = f"python3 skills/instagram-account/scripts/fetch_metrics.py --date {date} " + " ".join(
            f"--media-id {content_id}" for content_id in external_ids
        )
    elif platform == "x":
        fetch_command = f"python3 skills/x-account/scripts/fetch_metrics.py --date {date} " + " ".join(
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
    status = str(fm.get("status") or "").strip().lower()
    phase = str(fm.get("phase") or "").strip().lower()
    return status == "done" and phase in {"", "complete"}


def ticket_has_completion_proof(markdown: str) -> bool:
    done = markdown_heading_section(markdown, "Done / Proof") or markdown_heading_section(markdown, "Done")
    lowered = done.lower()
    return any(
        token in lowered
        for token in ("passed", "proof", "evidence", "artifact", "artifacts/", "review", "receipt", "verification")
    )


def ticket_has_acceptance_evidence(ticket: Path, markdown: str) -> bool:
    review_root = ticket.parent / "artifacts" / "review"
    for path in sorted(review_root.rglob("*")) if review_root.exists() else []:
        if not path.is_file() or path.suffix.lower() not in {".md", ".json"}:
            continue
        lowered = path.read_text(encoding="utf-8", errors="ignore").lower()
        if ("verdict: pass" in lowered or '"verdict": "pass"' in lowered) and (
            "tas-a" in lowered or '"overall_tas": "tas-a"' in lowered
        ):
            return True
    done = (markdown_heading_section(markdown, "Done / Proof") or "").lower()
    return "tas-a" in done and "verdict" in done and "pass" in done and "pending" not in done


def nonempty(value: Any) -> bool:
    return value is not None and str(value).strip() != ""


def string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def parse_ticket_kpi_rewards(markdown: str) -> tuple[list[dict[str, Any]], list[str]]:
    reward = markdown_heading_section(markdown, "Reward")
    if not reward:
        return [], ["missing_reward_section"]
    payload = parse_fenced_yaml_from_section(reward)
    raw_rewards = payload.get("kpi_rewards")
    if not isinstance(raw_rewards, list):
        return [], ["missing_kpi_rewards"]
    rewards: list[dict[str, Any]] = []
    gaps: list[str] = []
    seen_reward_ids: set[str] = set()
    for index, raw_reward in enumerate(raw_rewards):
        if not isinstance(raw_reward, dict):
            gaps.append(f"invalid_kpi_reward:{index}")
            continue
        kpi_id = str(raw_reward.get("kpi_id") or "").strip()
        reward_id = str(raw_reward.get("reward_id") or "").strip()
        expected_reward = str(raw_reward.get("expected_reward") or "").strip()
        if not reward_id:
            gaps.append(f"missing_reward_id:{index}")
            continue
        if reward_id in seen_reward_ids:
            gaps.append(f"duplicate_reward_id:{index}:{reward_id}")
            continue
        seen_reward_ids.add(reward_id)
        if not kpi_id:
            gaps.append(f"missing_kpi_id:{index}")
            continue
        rewards.append(
            {
                "reward_id": reward_id,
                "kpi_id": kpi_id,
                "expected_reward": expected_reward,
                "actual_result": raw_reward.get("actual_result"),
                "decision": str(raw_reward.get("decision") or "").strip().lower(),
                "evaluated_at": str(raw_reward.get("evaluated_at") or "").strip(),
                "evaluation_key": str(raw_reward.get("evaluation_key") or "").strip(),
                "supersedes_evaluation_key": str(
                    raw_reward.get("supersedes_evaluation_key") or ""
                ).strip(),
                "evidence_refs": string_list(raw_reward.get("evidence_refs")),
            }
        )
    return rewards, gaps


def accepted_reward(reward: dict[str, Any], *, has_acceptance_evidence: bool) -> bool:
    """Return whether one canonical Reward row is realized accepted value."""

    return (
        reward.get("decision") == "accept"
        and nonempty(reward.get("actual_result"))
        and parse_iso_datetime(reward.get("evaluated_at")) is not None
        and bool(reward.get("evidence_refs"))
        and has_acceptance_evidence
    )


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
        has_acceptance_evidence = ticket_has_acceptance_evidence(ticket, markdown)
        for reward in rewards:
            if reward["kpi_id"] != kpi_key:
                continue
            decision = reward.get("decision")
            if decision == "kill":
                continue
            if not accepted_reward(
                reward,
                has_acceptance_evidence=has_acceptance_evidence,
            ):
                if decision in {"", "monitor"}:
                    gaps.append(
                        f"{relative_ticket}:unresolved_reward:{reward['reward_id']}"
                    )
                elif decision == "accept" and not has_acceptance_evidence:
                    gaps.append(
                        f"{relative_ticket}:missing_acceptance_evidence:{reward['reward_id']}"
                    )
                else:
                    gaps.append(
                        f"{relative_ticket}:invalid_accept_evidence:{reward['reward_id']}"
                    )
                continue
            count += 1
            tickets.append(
                {
                    "ticket_id": fm.get("ticket_id") or ticket.parent.name,
                    "ticket": relative_ticket,
                    "reward_id": reward["reward_id"],
                    "expected_reward": reward.get("expected_reward", ""),
                    "actual_result": str(reward.get("actual_result") or ""),
                    "evaluated_at": reward.get("evaluated_at", ""),
                    "evidence_refs": reward.get("evidence_refs", []),
                }
            )
            # This primitive is a completed-ticket count by KPI. Multiple
            # accepted horizons for the same ticket/KPI remain evidence on the
            # ticket and do not inflate the daily ticket count.
            break
    return {
        "value": count,
        "status": "available" if count or not gaps else "source_gap",
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
    intervals: list[tuple[datetime, datetime]] = []
    accepted_minutes = 0.0
    for thread_id, start in spawned_today.items():
        end = latest_by_thread.get(thread_id, start)
        elapsed = max((end - start).total_seconds() / 60.0, 0.0)
        effective_elapsed = elapsed if elapsed > 0 else 30.0
        effective_end = end if elapsed > 0 else start + timedelta(minutes=30)
        autonomous_minutes += effective_elapsed
        intervals.append((start, effective_end))
        if thread_id in rewarded_threads:
            accepted_minutes += effective_elapsed
    union_minutes = 0.0
    for start, end in sorted(intervals):
        if not intervals:
            break
        if union_minutes == 0.0:
            current_start, current_end = start, end
            union_minutes = max((current_end - current_start).total_seconds() / 60.0, 0.0)
            continue
        if start > current_end:
            current_start, current_end = start, end
            union_minutes += max((end - start).total_seconds() / 60.0, 0.0)
        elif end > current_end:
            union_minutes += max((end - current_end).total_seconds() / 60.0, 0.0)
            current_end = end
    human_prompt_count = sum(len(times) for times in human_times_by_session.values())
    human_active_threads = len(human_times_by_session)
    human_minutes = sum(estimate_human_attention_minutes(times) for times in human_times_by_session.values())
    accepted_today = accepted_reward_count(reward_rows, date)
    ratio = autonomous_minutes / human_minutes if human_minutes else (autonomous_minutes if autonomous_minutes else 0.0)
    potential_saved_minutes = max(accepted_minutes - human_minutes, 0.0)
    if spawned_today and not rewarded_threads:
        gaps.append("missing:accepted_thread_runtime_attribution")
    gaps.extend(["source_gap:waiting_for_human_hours", "source_gap:unproductive_agent_hours"])
    return {
        "value": round(float(ratio), 4),
        "status": "available",
        "payload": {
            "human_prompt_count": human_prompt_count,
            "human_active_thread_count": human_active_threads,
            "human_attention_minutes_estimated": round(float(human_minutes), 2),
            "autonomous_thread_count": len(spawned_today),
            "autonomous_worker_elapsed_minutes": round(float(autonomous_minutes), 2),
            "clone_hours": round(float(autonomous_minutes / 60.0), 4),
            "concurrent_agent_wall_hours": round(float(union_minutes / 60.0), 4),
            "accepted_clone_hours": round(float(accepted_minutes / 60.0), 4) if rewarded_threads else None,
            "nonaccepted_clone_hours": None,
            "potential_human_time_saved_hours_estimated": round(float(potential_saved_minutes / 60.0), 4) if rewarded_threads else None,
            "formula": "max(accepted_clone_hours - human_attention_hours_estimated, 0)",
            "concurrency_policy": "clone_hours sum parallel intervals; concurrent_agent_wall_hours uses their union",
            "confidence": "estimated",
            "rewarded_autonomous_thread_count": len(rewarded_threads),
            "output_per_human_prompt": round(float(accepted_today / human_prompt_count), 4) if human_prompt_count else 0.0,
            "gaps": gaps,
        },
    }


def calculate_autonomy_savings(ticket_dir: Path, runtime_dir: Path, date: str, baseline_reasonable_hours: float | None = None, baseline_max_hours: float | None = None) -> dict[str, Any]:
    """Project accepted/nonaccepted clone hours through ticket proof and TAS-A."""
    attention = calculate_autonomy_time_ratio(runtime_dir, date)
    human_minutes = float(attention.get("payload", {}).get("human_attention_minutes_estimated") or 0.0)
    by_ticket: dict[str, list[dict[str, Any]]] = {}
    for row in read_jsonl(runtime_dir / "state" / "ticket-thread-associations.jsonl"):
        if row.get("ticket_id"):
            by_ticket.setdefault(str(row["ticket_id"]), []).append(row)
    accepted_minutes = nonaccepted_minutes = 0.0
    intervals: list[tuple[datetime, datetime]] = []
    terminal_count = attributed_count = 0
    items: list[dict[str, Any]] = []
    gaps: list[str] = []
    for ticket in iter_ticket_files(ticket_dir.resolve()):
        fm = parse_ticket_frontmatter(ticket)
        status = str(fm.get("status") or "").lower()
        completed = parse_iso_datetime(fm.get("completed_at") or fm.get("closed_at") or fm.get("updated_at"))
        if status not in {"done", "failed", "rejected"} or completed is None or completed.date().isoformat() != date:
            continue
        terminal_count += 1
        ticket_id = str(fm.get("ticket_id") or ticket.parent.name)
        rows = by_ticket.get(ticket_id, [])
        thread_ids = {str(row.get("thread_id") or row.get("session_id")) for row in rows if row.get("thread_id") or row.get("session_id")}
        starts = [parse_iso_datetime(row.get("execution_started_at") or row.get("started_at") or row.get("created_at") or row.get("timestamp") or row.get("ts")) for row in rows]
        starts = [value for value in starts if value is not None]
        if len(thread_ids) != 1 or not starts or completed <= min(starts):
            gaps.append(f"{ticket_id}:missing_or_ambiguous_runtime_attribution")
            continue
        start = min(starts)
        minutes = (completed - start).total_seconds() / 60.0
        markdown = ticket.read_text(encoding="utf-8")
        accepted = status == "done" and ticket_has_completion_proof(markdown) and ticket_has_acceptance_evidence(ticket, markdown)
        accepted_minutes += minutes if accepted else 0.0
        nonaccepted_minutes += 0.0 if accepted else minutes
        attributed_count += 1
        intervals.append((start, completed))
        items.append({"ticket_id": ticket_id, "thread_id": next(iter(thread_ids)), "minutes": round(minutes, 2), "accepted": accepted})
    union_minutes = 0.0
    current_end: datetime | None = None
    for start, end in sorted(intervals):
        if current_end is None or start > current_end:
            union_minutes += (end - start).total_seconds() / 60.0
            current_end = end
        elif end > current_end:
            union_minutes += (end - current_end).total_seconds() / 60.0
            current_end = end
    if terminal_count and not attributed_count:
        gaps.append("missing:accepted_runtime_attribution")
    coverage = attributed_count / terminal_count if terminal_count else None
    saved_minutes = max(accepted_minutes - human_minutes, 0.0) if attributed_count else None
    return {"value": round(saved_minutes / 60.0, 4) if saved_minutes is not None else None, "status": "available" if saved_minutes is not None else "source_gap", "payload": {"clone_hours": round((accepted_minutes + nonaccepted_minutes) / 60.0, 4), "concurrent_agent_wall_hours": round(union_minutes / 60.0, 4), "accepted_clone_hours": round(accepted_minutes / 60.0, 4), "nonaccepted_clone_hours": round(nonaccepted_minutes / 60.0, 4), "human_attention_hours_estimated": round(human_minutes / 60.0, 4), "potential_human_time_saved_hours_estimated": round(saved_minutes / 60.0, 4) if saved_minutes is not None else None, "attribution_coverage": round(coverage, 4) if coverage is not None else None, "baseline_provenance": {"reasonable_hours_per_day": baseline_reasonable_hours, "max_hours_per_day": baseline_max_hours, "source": "operator_provided" if baseline_reasonable_hours is not None or baseline_max_hours is not None else "not_provided"}, "formula": "max(accepted_clone_hours - human_attention_hours_estimated, 0)", "items": items, "gaps": gaps}}


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
        empty_payload = {"tickets": [], "gaps": gaps, "empty_window": True}
        return {
            "auto_completion_rate": {"value": None, "status": "not_applicable", "payload": empty_payload},
            "intervention_free_ticket_count": {"value": 0, "status": "available", "payload": empty_payload},
            "ticket_intervention_turn_count": {"value": 0, "status": "available", "payload": empty_payload},
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

    savings = subparsers.add_parser("autonomy-savings")
    savings.add_argument("--ticket-dir", required=True)
    savings.add_argument("--runtime-dir", required=True)
    savings.add_argument("--date", required=True)
    savings.add_argument("--baseline-reasonable-hours", type=float)
    savings.add_argument("--baseline-max-hours", type=float)

    content_targets = subparsers.add_parser("content-targets")
    content_targets.add_argument("--content-ledger", required=True)
    content_targets.add_argument("--platform", required=True)
    content_targets.add_argument("--kpi-key", required=True)
    content_targets.add_argument("--date", required=True)
    content_targets.add_argument("--window-days", type=int, default=7)

    refresh_plan = subparsers.add_parser("refresh-plan")
    refresh_plan.add_argument("--metrics-file", required=True)
    refresh_plan.add_argument("--date", required=True)
    refresh_plan.add_argument("--metric-id", action="append", default=[])
    refresh_plan.add_argument("--fresh-metric-id", action="append", default=[])

    args = parser.parse_args()
    if args.command == "ticket-reward-count":
        return print_json(count_ticket_kpi_rewards(Path(args.ticket_dir), args.date, args.kpi_key))
    if args.command == "autonomy-time-ratio":
        return print_json(calculate_autonomy_time_ratio(Path(args.runtime_dir), args.date))
    if args.command == "ticket-intervention-metrics":
        return print_json(calculate_ticket_intervention_metrics(Path(args.ticket_dir), Path(args.runtime_dir), args.date))
    if args.command == "autonomy-savings":
        return print_json(calculate_autonomy_savings(Path(args.ticket_dir), Path(args.runtime_dir), args.date, args.baseline_reasonable_hours, args.baseline_max_hours))
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
    if args.command == "refresh-plan":
        return print_json(resolve_refresh_plan(Path(args.metrics_file), args.metric_id, args.date, set(args.fresh_metric_id)))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
