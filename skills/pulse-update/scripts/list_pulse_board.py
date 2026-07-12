#!/usr/bin/env python3
"""Classify the one project ticket board for Work Pulse."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


ACTIVE_WORKER_STATUSES = {"spawned", "active", "handoff_recorded"}
EXECUTABLE_STATUSES = {"todo"}
REVIEW_STATUSES = {"awaiting_review"}
SIGNAL_WAIT_STATUSES = {"waiting_signal"}
TERMINAL_STATUSES = {"done", "failed", "rejected"}
PRIORITY_ORDER = {"urgent": 0, "high": 1, "medium": 2, "low": 3}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--worker-limit", type=int, default=1)
    parser.add_argument(
        "--now",
        default="",
        help="ISO-8601 check-in time. Defaults to the current UTC time.",
    )
    parser.add_argument(
        "ticket_paths",
        nargs="*",
        help="Optional ticket.md paths. Defaults to tickets/TASK-*/ticket.md.",
    )
    return parser.parse_args()


def read_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}
    try:
        data = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        data = parse_frontmatter_fallback(parts[1])
    return data if isinstance(data, dict) else {}


def parse_iso_datetime(value: Any) -> datetime | None:
    if value is None:
        return None
    raw = str(value).strip()
    if not raw:
        return None
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def markdown_heading_section(markdown: str, heading: str) -> str:
    lines = markdown.splitlines()
    target = f"## {heading}"
    for start, line in enumerate(lines):
        if line.strip() != target:
            continue
        end = len(lines)
        for index in range(start + 1, len(lines)):
            if lines[index].startswith("## "):
                end = index
                break
        return "\n".join(lines[start + 1 : end]).strip()
    return ""


def parse_fenced_yaml(section: str) -> dict[str, Any]:
    fence_start = section.find("```yaml")
    if fence_start == -1:
        return {}
    yaml_start = section.find("\n", fence_start)
    if yaml_start == -1:
        return {}
    fence_end = section.find("```", yaml_start + 1)
    if fence_end == -1:
        return {}
    try:
        loaded = yaml.safe_load(section[yaml_start + 1 : fence_end]) or {}
    except yaml.YAMLError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def classify_reward_checkins(markdown: str, now: datetime) -> dict[str, list[dict[str, Any]]]:
    """Project canonical Reward rows into due, future, terminal, and invalid state.

    ``reward_id`` is the durable identity handed to a check-in worker. Array
    position is intentionally diagnostic-only so reordering rows cannot change
    which reward is evaluated.
    """

    reward = parse_fenced_yaml(markdown_heading_section(markdown, "Reward"))
    raw_rewards = reward.get("kpi_rewards")
    if not isinstance(raw_rewards, list):
        return {"due": [], "future": [], "terminal": [], "invalid": []}

    result: dict[str, list[dict[str, Any]]] = {
        "due": [],
        "future": [],
        "terminal": [],
        "invalid": [],
    }
    seen_reward_ids: set[str] = set()
    for index, raw_item in enumerate(raw_rewards):
        if not isinstance(raw_item, dict):
            result["invalid"].append({"index": index, "gap": "invalid_reward_item"})
            continue
        reward_id = str(raw_item.get("reward_id") or "").strip()
        if not reward_id:
            result["invalid"].append({"index": index, "gap": "missing_reward_id"})
            continue
        if reward_id in seen_reward_ids:
            result["invalid"].append(
                {"index": index, "reward_id": reward_id, "gap": "duplicate_reward_id"}
            )
            continue
        seen_reward_ids.add(reward_id)
        decision = str(raw_item.get("decision") or "").strip().lower()
        if decision not in {"", "accept", "kill", "monitor"}:
            result["invalid"].append(
                {
                    "index": index,
                    "reward_id": reward_id,
                    "gap": "invalid_decision",
                    "decision": decision,
                }
            )
            continue
        check_in_at = parse_iso_datetime(raw_item.get("check_in_at"))
        item = {
            "reward_id": reward_id,
            "kpi_id": str(raw_item.get("kpi_id") or ""),
            "expected_reward": str(raw_item.get("expected_reward") or ""),
            "check_in_at": str(raw_item.get("check_in_at") or ""),
            "decision": decision,
            "evaluation_key": str(raw_item.get("evaluation_key") or ""),
        }
        if decision in {"accept", "kill"}:
            result["terminal"].append(
                {**item, "state": f"terminal_{decision}"}
            )
            continue
        if check_in_at is None:
            result["invalid"].append(
                {**item, "index": index, "gap": "invalid_check_in_at"}
            )
            continue
        if check_in_at <= now:
            state = "monitor_due" if decision == "monitor" else "due"
            result["due"].append({**item, "state": state})
        else:
            state = "monitor_pending" if decision == "monitor" else "pending"
            result["future"].append({**item, "state": state})
    return result


def parse_frontmatter_fallback(raw: str) -> dict[str, Any]:
    """Read the top-level board fields from legacy imperfect YAML."""

    data: dict[str, Any] = {}
    lines = raw.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line or line[0].isspace() or ":" not in line:
            index += 1
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        if not key:
            index += 1
            continue
        if value:
            try:
                parsed = yaml.safe_load(value)
            except yaml.YAMLError:
                parsed = value.strip('"').strip("'").strip("`")
            data[key] = parsed
            index += 1
            continue
        items: list[str] = []
        cursor = index + 1
        while cursor < len(lines) and lines[cursor].startswith("  - "):
            items.append(lines[cursor][4:].strip().strip('"').strip("'"))
            cursor += 1
        data[key] = items
        index = cursor
    return data


def as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def is_terminal(frontmatter: dict[str, Any]) -> bool:
    status = str(frontmatter.get("status", "")).strip().lower()
    return status in TERMINAL_STATUSES


def review_state(progress_path: Path) -> dict[str, Any]:
    if not progress_path.is_file():
        return {}
    markdown = progress_path.read_text(encoding="utf-8", errors="replace")
    return parse_fenced_yaml(markdown_heading_section(markdown, "Review"))


def due_review_reminder(progress_path: Path, now: datetime) -> dict[str, Any] | None:
    state = review_state(progress_path)
    if not state or str(state.get("decision") or "").strip():
        return None
    next_reminder_at = parse_iso_datetime(state.get("next_reminder_at"))
    if next_reminder_at is None or next_reminder_at > now:
        return None
    return {
        "progress_path": str(progress_path),
        "artifact_refs": as_list(state.get("artifact_refs")),
        "thread_ref": str(state.get("thread_ref") or "").strip(),
        "requested_at": str(state.get("requested_at") or "").strip(),
        "next_reminder_at": str(state.get("next_reminder_at") or "").strip(),
        "reminder_count": int(state.get("reminder_count") or 0),
        "escalation_used": state.get("escalation_used") is True,
    }


def ticket_paths(root: Path, explicit: list[str] | None = None) -> list[Path]:
    if explicit:
        resolved: list[Path] = []
        for raw in explicit:
            path = Path(raw)
            if not path.is_absolute():
                path = root / path
            resolved.append(path.resolve())
        return sorted(resolved)
    return sorted((root / "tickets").glob("TASK-*/ticket.md"))


def completed_archived_ticket_ids(root: Path) -> set[str]:
    ids: set[str] = set()
    for path in (root / "tickets" / "archive").glob("TASK-*/ticket.md"):
        data = read_frontmatter(path)
        if str(data.get("status") or "").strip().lower() == "done":
            ids.add(str(data.get("ticket_id") or path.parent.name).strip())
    return ids


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{line_number}: invalid JSONL: {exc}") from exc
        if isinstance(value, dict):
            rows.append(value)
    return rows


def latest_worker_rows(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for row in rows:
        ticket_id = str(row.get("ticket_id", "")).strip()
        if ticket_id:
            latest[ticket_id] = row
    return latest


def classify_ticket(
    row: dict[str, Any],
    satisfied_dependencies: set[str],
) -> list[str]:
    reasons: list[str] = []
    if row["terminal"]:
        reasons.append("terminal")
    status = row["status"].lower()
    if status in REVIEW_STATUSES:
        reasons.append("awaiting_review")
    # A matured delayed-reward row is executable check-in work on the original
    # ticket. It does not need a hand-maintained readiness mutation or a new
    # check-in ticket. All other lifecycle and safety gates still apply.
    is_due_checkin = status in SIGNAL_WAIT_STATUSES and bool(row["due_reward_checkins"])
    if status not in EXECUTABLE_STATUSES and not is_due_checkin and not row["terminal"]:
        reasons.append("status_not_executable")
    if row["claimed_by"]:
        reasons.append("claimed_by")
    unsatisfied = [
        dependency
        for dependency in row["depends_on"]
        if dependency not in satisfied_dependencies
    ]
    if unsatisfied:
        reasons.append("unsatisfied_dependencies")
        row["unsatisfied_dependencies"] = unsatisfied
    return reasons


def build_board(
    root: Path,
    worker_limit: int = 1,
    explicit_ticket_paths: list[str] | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    paths = ticket_paths(root, explicit_ticket_paths)
    rows: list[dict[str, Any]] = []
    active_completed_ids: set[str] = set()

    for path in paths:
        markdown = path.read_text(encoding="utf-8", errors="replace")
        data = read_frontmatter(path)
        ticket_id = str(data.get("ticket_id") or path.parent.name).strip()
        terminal = is_terminal(data)
        if str(data.get("status") or "").strip().lower() == "done":
            active_completed_ids.add(ticket_id)
        try:
            relative = str(path.relative_to(root))
        except ValueError:
            relative = str(path)
        reward_checkins = classify_reward_checkins(markdown, now)
        rows.append(
            {
                "ticket_id": ticket_id,
                "path": relative,
                "title": str(data.get("title", "")).strip(),
                "status": str(data.get("status", "")).strip(),
                "priority": str(data.get("priority") or "medium").strip().lower(),
                "claimed_by": str(data.get("claimed_by") or "").strip(),
                "depends_on": as_list(data.get("depends_on")),
                "human_gate": data.get("human_gate", "none"),
                "terminal": terminal,
                "due_reward_checkins": reward_checkins["due"],
                "future_reward_checkins": reward_checkins["future"],
                "terminal_reward_outcomes": reward_checkins["terminal"],
                "reward_checkin_gaps": reward_checkins["invalid"],
            }
        )

    satisfied_dependencies = completed_archived_ticket_ids(root) | active_completed_ids
    executable: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    archive_needed: list[dict[str, Any]] = []
    awaiting_review: list[dict[str, Any]] = []
    due_checkins: list[dict[str, Any]] = []
    future_checkins: list[dict[str, Any]] = []
    due_review_reminders: list[dict[str, Any]] = []

    for row in rows:
        reasons = classify_ticket(row, satisfied_dependencies)
        row["exclusion_reasons"] = reasons
        if row["terminal"]:
            archive_needed.append(row)
        if row["status"].lower() in REVIEW_STATUSES:
            awaiting_review.append(row)
            reminder = due_review_reminder(root / Path(row["path"]).parent / "progress.md", now)
            if reminder:
                due_review_reminders.append({**row, "review": reminder})
        if row["status"].lower() in SIGNAL_WAIT_STATUSES and row["due_reward_checkins"]:
            due_checkins.append(row)
        if row["status"].lower() in SIGNAL_WAIT_STATUSES and row["future_reward_checkins"]:
            future_checkins.append(row)
        if reasons:
            excluded.append(row)
        else:
            row["execution_reason"] = (
                "due_reward_checkin" if row["due_reward_checkins"] else "ready_ticket"
            )
            executable.append(row)

    executable.sort(
        key=lambda row: (
            PRIORITY_ORDER.get(row["priority"], PRIORITY_ORDER["medium"]),
            row["ticket_id"],
        )
    )
    due_review_reminders.sort(
        key=lambda row: (row["review"]["next_reminder_at"], row["ticket_id"])
    )

    ledger_path = root / ".farplane" / "automation" / "spawned-threads.jsonl"
    workers_by_ticket = latest_worker_rows(load_jsonl(ledger_path))
    ticket_status_by_id = {
        row["ticket_id"]: row["status"].lower() for row in rows
    }
    worker_release_ticket_statuses = REVIEW_STATUSES | SIGNAL_WAIT_STATUSES | TERMINAL_STATUSES | {"blocked"}
    active_workers: list[dict[str, Any]] = []
    released_worker_rows: list[dict[str, Any]] = []
    for worker_row in workers_by_ticket.values():
        worker_status = str(worker_row.get("status", "")).strip().lower()
        ticket_id = str(worker_row.get("ticket_id") or "").strip()
        ticket_status = ticket_status_by_id.get(ticket_id, "")
        if worker_status in ACTIVE_WORKER_STATUSES:
            if not ticket_status:
                released_worker_rows.append(
                    {**worker_row, "release_reason": "ticket_not_active"}
                )
            elif ticket_status in worker_release_ticket_statuses:
                released_worker_rows.append(
                    {**worker_row, "release_reason": f"ticket_status:{ticket_status}"}
                )
            else:
                active_workers.append(worker_row)
        elif worker_status in {"blocked", "waiting_human_review", "waiting_final_action"}:
            released_worker_rows.append(worker_row)
    active_worker_ticket_ids = {
        str(row.get("ticket_id") or "").strip() for row in active_workers
    }
    # A claimed active ticket is unavailable for dispatch, but a ticket claim
    # alone does not prove that Pulse owns a live worker. Human-started and
    # directly-created Codex tasks commonly claim tickets without a row in the
    # Pulse spawned-thread ledger. Only live ledger rows consume the configured
    # Pulse worker pool.
    human_active_tickets = [
        row
        for row in rows
        if row["status"].lower() == "active"
        and row["claimed_by"]
        and row["ticket_id"] not in active_worker_ticket_ids
    ]
    worker_limit = max(0, worker_limit)
    return {
        "schema": "farplane.work_pulse_board.v2",
        "project_root": str(root),
        "ledger": str(ledger_path.relative_to(root)),
        "active_ticket_count": len(rows),
        "as_of": now.isoformat(),
        "executable_tickets": executable,
        "excluded_tickets": excluded,
        "archive_needed_tickets": archive_needed,
        "awaiting_review_tickets": awaiting_review,
        # Reconciliation exposes one action even when several waits are due.
        # It does not reserve or assign an execution worker.
        "next_due_review_reminder": due_review_reminders[0] if due_review_reminders else None,
        "due_review_reminder_count": len(due_review_reminders),
        "due_checkin_tickets": due_checkins,
        "future_checkin_tickets": future_checkins,
        "review_wip": len(awaiting_review),
        "active_workers": active_workers,
        "human_active_tickets": human_active_tickets,
        "released_worker_rows": released_worker_rows,
        "worker_limit": worker_limit,
        "idle_worker_slots": max(0, worker_limit - len(active_workers)),
        # Pulse combines this fact with review_wip and current context before
        # choosing plan_next_wave; the classifier does not make that decision.
        "empty_executable_board": not executable,
    }


def main() -> int:
    args = parse_args()
    now = parse_iso_datetime(args.now) if args.now else datetime.now(timezone.utc)
    if now is None:
        raise SystemExit("--now must be an ISO-8601 datetime")
    result = build_board(
        Path(args.project_root),
        worker_limit=args.worker_limit,
        explicit_ticket_paths=args.ticket_paths,
        now=now,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
