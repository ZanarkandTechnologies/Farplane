#!/usr/bin/env python3
"""Classify the one project ticket board for Work Pulse."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import yaml


ACTIVE_WORKER_STATUSES = {"spawned", "active", "handoff_recorded"}
EXECUTABLE_STATUSES = {"todo"}
REVIEW_STATUSES = {"awaiting_review"}
SIGNAL_WAIT_STATUSES = {"waiting_signal"}
TERMINAL_STATUSES = {"done", "failed", "rejected"}
PRIORITY_ORDER = {"urgent": 0, "high": 1, "medium": 2, "low": 3}
REVIEW_ACTION_PRIORITY = {
    "send_initial_telegram": 0,
    "send_telegram_reminder": 1,
    "dispatch_phone_chaser": 2,
    "repair_review_state": 3,
}
DEFAULT_REVIEW_CHASE_POLICY = {
    "timezone": "UTC",
    "active_hours": {"start": "00:00", "end": "23:59"},
    "pulse_interval_minutes": 30,
    "telegram_reminder_after_unanswered_turns": [2, 4],
    "phone_chaser_after_unanswered_turns": [6, 12],
    "phone_chaser_repeat_after_turns": 6,
    "telegram_reminder_limit": 2,
    "phone_chaser_limit": 2,
    "actions_per_beat": 1,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--worker-limit", type=int, default=1)
    parser.add_argument(
        "--review-wip",
        type=int,
        default=3,
        help="Maximum operator-facing review-area pools. Does not limit workers.",
    )
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


def parse_yaml_section(section: str) -> dict[str, Any]:
    """Parse the documented plain Review block or an explicitly fenced one."""

    fenced = parse_fenced_yaml(section)
    if fenced:
        return fenced
    try:
        loaded = yaml.safe_load(section) or {}
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
    return parse_yaml_section(markdown_heading_section(markdown, "Review"))


def review_chase_policy(root: Path) -> dict[str, Any]:
    policy = dict(DEFAULT_REVIEW_CHASE_POLICY)
    bindings_path = root / "farplane" / "bindings.yaml"
    if not bindings_path.is_file():
        return policy
    try:
        bindings = yaml.safe_load(bindings_path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return policy
    configured = (bindings.get("operator") or {}).get("review_chase_policy")
    if isinstance(configured, dict):
        policy.update(configured)
    return policy


def parse_clock(value: Any) -> tuple[int, int] | None:
    try:
        hour, minute = str(value).split(":", 1)
        parsed = (int(hour), int(minute))
    except (TypeError, ValueError):
        return None
    return parsed if 0 <= parsed[0] <= 23 and 0 <= parsed[1] <= 59 else None


def within_active_hours(now: datetime, policy: dict[str, Any]) -> bool:
    try:
        local_now = now.astimezone(ZoneInfo(str(policy.get("timezone") or "UTC")))
    except ZoneInfoNotFoundError:
        local_now = now.astimezone(timezone.utc)
    hours = policy.get("active_hours") or {}
    start = parse_clock(hours.get("start"))
    end = parse_clock(hours.get("end"))
    if not start or not end:
        return False
    current = (local_now.hour, local_now.minute)
    if start <= end:
        return start <= current < end
    return current >= start or current < end


def integer_list(value: Any, limit: int) -> list[int]:
    if not isinstance(value, list):
        return []
    result: list[int] = []
    for item in value[: max(0, limit)]:
        try:
            parsed = int(item)
        except (TypeError, ValueError):
            continue
        if parsed >= 0:
            result.append(parsed)
    return result


def parse_nonnegative_int(value: Any) -> int | None:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed >= 0 else None


def policy_nonnegative_int(policy: dict[str, Any], key: str) -> int:
    configured = parse_nonnegative_int(policy.get(key))
    if configured is not None:
        return configured
    fallback = parse_nonnegative_int(DEFAULT_REVIEW_CHASE_POLICY.get(key))
    return fallback or 0


def review_action(
    progress_path: Path,
    now: datetime,
    policy: dict[str, Any],
) -> dict[str, Any]:
    state = review_state(progress_path)
    if not progress_path.is_file():
        return {"action": "repair_review_state", "reason": "missing_progress_md"}
    if not state:
        return {"action": "repair_review_state", "reason": "missing_or_invalid_review_block"}
    if str(state.get("decision") or "").strip():
        return {"action": "none", "reason": "review_decided"}

    required = ["artifact_refs", "thread_ref", "requested_at"]
    missing = [name for name in required if not state.get(name)]
    requested_at = parse_iso_datetime(state.get("requested_at"))
    if requested_at is None:
        missing.append("requested_at_valid_iso8601")
    if missing:
        return {
            "action": "repair_review_state",
            "reason": "missing_required_review_fields",
            "missing_fields": sorted(set(missing)),
        }

    reminder_count = parse_nonnegative_int(state.get("reminder_count") or 0)
    phone_chaser_count = parse_nonnegative_int(state.get("phone_chaser_count") or 0)
    if reminder_count is None or phone_chaser_count is None:
        return {
            "action": "repair_review_state",
            "reason": "invalid_review_counter",
            "reminder_count": state.get("reminder_count"),
            "phone_chaser_count": state.get("phone_chaser_count"),
        }
    reminder_message_ids = as_list(state.get("telegram_reminder_message_ids"))
    if reminder_count != len(reminder_message_ids):
        return {
            "action": "repair_review_state",
            "reason": "telegram_reminder_receipt_count_mismatch",
            "reminder_count": reminder_count,
            "telegram_reminder_message_id_count": len(reminder_message_ids),
        }

    phone_chaser_dispatch_ids = as_list(state.get("phone_chaser_dispatch_ids"))
    if phone_chaser_count != len(phone_chaser_dispatch_ids):
        return {
            "action": "repair_review_state",
            "reason": "phone_chaser_receipt_count_mismatch",
            "phone_chaser_count": phone_chaser_count,
            "phone_chaser_dispatch_id_count": len(phone_chaser_dispatch_ids),
        }
    last_phone_chaser_at = parse_iso_datetime(state.get("last_phone_chaser_at"))
    if phone_chaser_count and last_phone_chaser_at is None:
        return {
            "action": "repair_review_state",
            "reason": "missing_last_phone_chaser_at",
            "phone_chaser_count": phone_chaser_count,
        }

    base = {
        "progress_path": str(progress_path),
        "artifact_refs": as_list(state.get("artifact_refs")),
        "thread_ref": str(state.get("thread_ref") or "").strip(),
        "requested_at": str(state.get("requested_at") or "").strip(),
        "reminder_count": reminder_count,
        "telegram_reminder_message_ids": reminder_message_ids,
        "phone_chaser_count": phone_chaser_count,
        "phone_chaser_dispatch_ids": phone_chaser_dispatch_ids,
        "last_phone_chaser_at": (
            last_phone_chaser_at.isoformat() if last_phone_chaser_at else ""
        ),
    }

    telegram_sent = (
        str(state.get("telegram_status") or "").strip().lower() == "sent"
        and bool(str(state.get("telegram_message_id") or "").strip())
    )
    if not telegram_sent:
        return {
            **base,
            "action": "send_initial_telegram",
            "reason": "initial_review_notification_missing_or_blocked",
            "due_at": requested_at.isoformat(),
        }

    interval_minutes = max(1, policy_nonnegative_int(policy, "pulse_interval_minutes"))
    elapsed_turns = max(
        0,
        int((now - requested_at).total_seconds() // (interval_minutes * 60)),
    )
    active_now = within_active_hours(now, policy)
    telegram_limit = policy_nonnegative_int(policy, "telegram_reminder_limit")
    reminder_turns = integer_list(
        policy.get("telegram_reminder_after_unanswered_turns"), telegram_limit
    )
    reminder_count = base["reminder_count"]
    if reminder_count < len(reminder_turns):
        threshold = reminder_turns[reminder_count]
        due_at = requested_at + timedelta(minutes=interval_minutes * threshold)
        if elapsed_turns >= threshold:
            action = "send_telegram_reminder" if active_now else "held_outside_active_hours"
            return {
                **base,
                "action": action,
                "held_action": None if active_now else "send_telegram_reminder",
                "reason": "telegram_chase_due" if active_now else "telegram_chase_outside_active_hours",
                "due_at": due_at.isoformat(),
                "unanswered_pulse_turns": elapsed_turns,
            }
        return {**base, "action": "none", "reason": "telegram_chase_not_due"}

    phone_limit = policy_nonnegative_int(policy, "phone_chaser_limit")
    phone_turns = integer_list(policy.get("phone_chaser_after_unanswered_turns"), phone_limit)
    phone_count = base["phone_chaser_count"]
    if phone_count < len(phone_turns):
        threshold = phone_turns[phone_count]
        due_at = requested_at + timedelta(minutes=interval_minutes * threshold)
        repeat_turns = policy_nonnegative_int(policy, "phone_chaser_repeat_after_turns")
        if last_phone_chaser_at is not None:
            due_at = max(
                due_at,
                last_phone_chaser_at
                + timedelta(minutes=interval_minutes * repeat_turns),
            )
        if now >= due_at:
            action = "dispatch_phone_chaser" if active_now else "held_outside_active_hours"
            return {
                **base,
                "action": action,
                "held_action": None if active_now else "dispatch_phone_chaser",
                "reason": "phone_chaser_due" if active_now else "phone_chaser_outside_active_hours",
                "due_at": due_at.isoformat(),
                "unanswered_pulse_turns": elapsed_turns,
            }
    return {**base, "action": "none", "reason": "review_chase_not_due_or_capped"}


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


def planner_area_by_ticket(root: Path) -> dict[str, str]:
    """Resolve immutable planner-selected area provenance from admission rows."""

    resolved: dict[str, str] = {}
    decision_rows = load_jsonl(
        root / ".farplane" / "automation" / "decisions.jsonl"
    )
    for decision in decision_rows:
        specs = decision.get("admitted_specs")
        if not isinstance(specs, list):
            continue
        for spec in specs:
            if not isinstance(spec, dict):
                continue
            ticket_id = str(spec.get("ticket_id") or "").strip()
            area_id = str(spec.get("area_id") or "").strip()
            if ticket_id and area_id:
                resolved[ticket_id] = area_id
    return resolved


def ticket_state_area(markdown: str) -> str:
    """Read the compact ticket-body ``State`` area when no receipt exists."""

    section = markdown_heading_section(markdown, "State")
    match = re.search(
        r"^\s*(?:[-*]\s*)?(?:`?area`?)\s*:\s*`?([^`\n]+?)`?\s*$",
        section,
        flags=re.MULTILINE,
    )
    return match.group(1).strip() if match else ""


def project_review_pools(
    awaiting_review: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Keep review tickets distinct while grouping their human decision surface."""

    grouped: dict[str, list[dict[str, Any]]] = {}
    for ticket in awaiting_review:
        area_id = str(ticket.get("area_id") or "").strip()
        # Missing provenance must not make unrelated tickets look like one
        # decision surface. A ticket-scoped pool is the honest fallback.
        pool_id = area_id or f"unassigned:{ticket['ticket_id']}"
        grouped.setdefault(pool_id, []).append(ticket)

    pools: list[dict[str, Any]] = []
    for pool_id, tickets in sorted(grouped.items()):
        tickets.sort(key=lambda row: row["ticket_id"])
        digest_tickets = [
            {
                "ticket_id": row["ticket_id"],
                "ticket_path": row["path"],
                "progress_ref": row.get("review_ref", ""),
                "artifact_refs": row.get("review_artifact_refs", []),
                "thread_ref": row.get("review_thread_ref", ""),
                "requested_at": row.get("review_requested_at", ""),
                "decision": row.get("review_decision", ""),
                "next_action": row.get("review_next_action", ""),
            }
            for row in tickets
        ]
        digest = {
            "area_id": pool_id if not pool_id.startswith("unassigned:") else "",
            "tickets": digest_tickets,
        }
        digest_id = hashlib.sha256(
            json.dumps(
                digest, sort_keys=True, separators=(",", ":"), ensure_ascii=True
            ).encode("utf-8")
        ).hexdigest()
        pools.append(
            {
                "pool_id": pool_id,
                "area_id": pool_id if not pool_id.startswith("unassigned:") else "",
                "ticket_count": len(tickets),
                "ticket_ids": [row["ticket_id"] for row in tickets],
                "ticket_paths": [row["path"] for row in tickets],
                "operator_digest": {**digest, "digest_id": digest_id},
            }
        )
    return pools


def association_worker_rows(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for row in rows:
        ticket_id = str(row.get("ticket_id", "")).strip()
        thread_id = str(row.get("thread_id") or row.get("session_id") or "").strip()
        if not ticket_id or not thread_id:
            continue
        observed_at = str(
            row.get("observed_at")
            or row.get("execution_started_at")
            or row.get("started_at")
            or row.get("created_at")
            or ""
        ).strip()
        candidate = {
            **row,
            "ticket_id": ticket_id,
            "thread_id": thread_id,
            "status": "active",
            "observed_at": observed_at,
        }
        previous = latest.get(ticket_id)
        previous_at = parse_iso_datetime(previous.get("observed_at")) if previous else None
        candidate_at = parse_iso_datetime(observed_at)
        if previous is None or (
            candidate_at is not None
            and (previous_at is None or candidate_at >= previous_at)
        ):
            latest[ticket_id] = candidate
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
    review_wip: int = 3,
    explicit_ticket_paths: list[str] | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    paths = ticket_paths(root, explicit_ticket_paths)
    receipt_areas = planner_area_by_ticket(root)
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
                "area_id": receipt_areas.get(ticket_id) or ticket_state_area(markdown),
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
    review_actions: list[dict[str, Any]] = []
    held_review_chases: list[dict[str, Any]] = []
    chase_policy = review_chase_policy(root)

    for row in rows:
        reasons = classify_ticket(row, satisfied_dependencies)
        row["exclusion_reasons"] = reasons
        if row["terminal"]:
            archive_needed.append(row)
        if row["status"].lower() in REVIEW_STATUSES:
            awaiting_review.append(row)
            progress_path = root / Path(row["path"]).parent / "progress.md"
            state = review_state(progress_path)
            action = review_action(
                progress_path, now, chase_policy
            )
            try:
                progress_ref = str(progress_path.relative_to(root))
            except ValueError:
                progress_ref = str(progress_path)
            row.update(
                review_ref=progress_ref,
                review_artifact_refs=as_list(state.get("artifact_refs")),
                review_thread_ref=str(state.get("thread_ref") or "").strip(),
                review_requested_at=str(state.get("requested_at") or "").strip(),
                review_decision=str(state.get("decision") or "").strip(),
                review_next_action=str(action.get("action") or "").strip(),
            )
            action_row = {**row, "review": action}
            if action["action"] in {
                "repair_review_state",
                "send_initial_telegram",
                "send_telegram_reminder",
                "dispatch_phone_chaser",
            }:
                review_actions.append(action_row)
            elif action["action"] == "held_outside_active_hours":
                held_review_chases.append(action_row)
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
    review_actions.sort(
        key=lambda row: (
            REVIEW_ACTION_PRIORITY.get(row["review"]["action"], 99),
            row["review"].get("due_at", ""),
            row["ticket_id"],
        )
    )

    worker_index_path = root / ".farplane" / "state" / "ticket-thread-associations.jsonl"
    workers_by_ticket = association_worker_rows(load_jsonl(worker_index_path))
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
    # directly-created Codex tasks commonly claim tickets without a canonical
    # ticket-thread association. Only live association rows consume the
    # configured Pulse worker pool.
    human_active_tickets = [
        row
        for row in rows
        if row["status"].lower() == "active"
        and row["claimed_by"]
        and row["ticket_id"] not in active_worker_ticket_ids
    ]
    worker_limit = max(0, worker_limit)
    review_pool_limit = max(0, review_wip)
    all_review_pools = project_review_pools(awaiting_review)
    review_pools = all_review_pools[:review_pool_limit]
    queued_review_pools = all_review_pools[review_pool_limit:]
    review_pool_saturated = bool(all_review_pools) and (
        len(review_pools) >= review_pool_limit
    )
    return {
        "schema": "farplane.work_pulse_board.v2",
        "project_root": str(root),
        "worker_index": str(worker_index_path.relative_to(root)),
        "active_ticket_count": len(rows),
        "as_of": now.isoformat(),
        "executable_tickets": executable,
        "excluded_tickets": excluded,
        "archive_needed_tickets": archive_needed,
        "awaiting_review_tickets": awaiting_review,
        "review_pools": review_pools,
        "queued_review_pools": queued_review_pools,
        "review_pool_count": len(review_pools),
        "review_pool_limit": review_pool_limit,
        "total_review_pool_count": len(all_review_pools),
        "review_pool_saturated": review_pool_saturated,
        "review_item_count": len(awaiting_review),
        # Reconciliation exposes one policy-derived action even when several
        # waits need service. Review actions never reserve an execution worker.
        "review_chase_policy": chase_policy,
        "next_due_review_action": review_actions[0] if review_actions else None,
        "due_review_action_count": len(review_actions),
        "held_review_chases": held_review_chases,
        "due_checkin_tickets": due_checkins,
        "future_checkin_tickets": future_checkins,
        # Review WIP is a bounded human-decision surface, not execution-worker
        # occupancy. Distinct underlying tickets and their chase ledgers remain
        # visible in ``awaiting_review_tickets``.
        "review_wip": len(review_pools),
        "active_workers": active_workers,
        "human_active_tickets": human_active_tickets,
        "released_worker_rows": released_worker_rows,
        "worker_limit": worker_limit,
        "idle_worker_slots": max(0, worker_limit - len(active_workers)),
        # Pulse subtracts tickets dispatched in the current phase before
        # comparing remaining ready supply with ready_low_watermark.
        "ready_ticket_count": len(executable),
    }


def main() -> int:
    args = parse_args()
    now = parse_iso_datetime(args.now) if args.now else datetime.now(timezone.utc)
    if now is None:
        raise SystemExit("--now must be an ISO-8601 datetime")
    result = build_board(
        Path(args.project_root),
        worker_limit=args.worker_limit,
        review_wip=args.review_wip,
        explicit_ticket_paths=args.ticket_paths,
        now=now,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
