#!/usr/bin/env python3
"""Classify active tickets by AI/planning ownership.

Farplane does not need a ``created_by`` frontmatter field for Pulse refill.
Planned AI tickets identify themselves with frontmatter ``rewards.kpi`` or
``reward.kpi``. The human-readable ``## Reward`` block still carries expected
reward and guard details. The spawned-thread ledger is worker state, not the
source of truth for ticket origin.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import yaml


ACTIVE_STATUSES = {
    "spawned",
    "active",
    "handoff_recorded",
    "completed_pending_reward",
    "blocked",
    "waiting_human_review",
    "waiting_final_action",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        default=".",
        help="Farplane project root. Defaults to the current directory.",
    )
    parser.add_argument(
        "ticket_paths",
        nargs="*",
        help=(
            "Optional active ticket.md paths to classify. When omitted, all "
            "tickets/TASK-*/ticket.md files under --project-root are used."
        ),
    )
    return parser.parse_args()


def load_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}
    data = yaml.safe_load(parts[1]) or {}
    if not isinstance(data, dict):
        return {}
    return data


def split_ticket(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}, text
    try:
        data = yaml.safe_load(parts[1]) or {}
        if not isinstance(data, dict):
            data = {}
    except yaml.YAMLError:
        data = parse_frontmatter_fallback(parts[1])
    return data, parts[2]


def parse_frontmatter_fallback(raw: str) -> dict[str, Any]:
    data: dict[str, Any] = {}
    lines = raw.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip() or line.startswith(" "):
            index += 1
            continue
        if ":" not in line:
            index += 1
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        if not re.match(r"^[A-Za-z0-9_.-]+$", key):
            index += 1
            continue
        if value:
            data[key] = value.strip('"').strip("'")
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


def parse_reward_block(body: str) -> dict[str, Any] | None:
    lines = body.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != "## Reward":
            continue
        fence_start = None
        for cursor in range(index + 1, len(lines)):
            stripped = lines[cursor].strip()
            if stripped.startswith("```"):
                fence_start = cursor
                break
            if stripped.startswith("## "):
                return None
        if fence_start is None:
            return None
        fence_end = None
        for cursor in range(fence_start + 1, len(lines)):
            if lines[cursor].strip().startswith("```"):
                fence_end = cursor
                break
        if fence_end is None:
            return None
        raw = "\n".join(lines[fence_start + 1 : fence_end])
        try:
            loaded = yaml.safe_load(raw) or {}
        except yaml.YAMLError:
            return None
        if not isinstance(loaded, dict):
            return None
        rewards = loaded.get("kpi_rewards")
        if not isinstance(rewards, list) or not rewards:
            return None
        return loaded


def frontmatter_reward_kpis(frontmatter: dict[str, Any]) -> list[str]:
    for key in ("rewards.kpi", "reward.kpi"):
        value = frontmatter.get(key)
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        if isinstance(value, str) and value.strip():
            return [value.strip()]
    for key in ("rewards", "reward"):
        value = frontmatter.get(key)
        if isinstance(value, dict):
            kpi = value.get("kpi")
            if isinstance(kpi, list):
                return [str(item).strip() for item in kpi if str(item).strip()]
            if isinstance(kpi, str) and kpi.strip():
                return [kpi.strip()]
    return []


def reward_summary(frontmatter: dict[str, Any], reward: dict[str, Any] | None) -> dict[str, Any]:
    frontmatter_kpi_ids = frontmatter_reward_kpis(frontmatter)
    if not reward:
        return {
            "has_ai_planning_marker": bool(frontmatter_kpi_ids),
            "frontmatter_kpi_ids": frontmatter_kpi_ids,
            "body_kpi_ids": [],
            "guard": None,
        }
    kpi_ids = []
    for item in reward.get("kpi_rewards") or []:
        if isinstance(item, dict) and item.get("kpi_id"):
            kpi_ids.append(str(item["kpi_id"]))
    return {
        "has_ai_planning_marker": bool(frontmatter_kpi_ids),
        "frontmatter_kpi_ids": frontmatter_kpi_ids,
        "body_kpi_ids": kpi_ids,
        "guard": reward.get("guard"),
    }


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"{path}:{line_number}: invalid JSONL row: {exc}") from exc
        if isinstance(row, dict):
            rows.append(row)
    return rows


def latest_rows_by_ticket(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    latest: dict[str, dict[str, Any]] = {}
    for row in rows:
        ticket_id = str(row.get("ticket_id", "")).strip()
        if ticket_id:
            latest[ticket_id] = row
    return latest


def active_ticket_paths(root: Path, ticket_paths: list[str]) -> list[Path]:
    if ticket_paths:
        paths = []
        for raw in ticket_paths:
            path = Path(raw)
            if not path.is_absolute():
                path = root / path
            paths.append(path.resolve())
        return sorted(paths)
    return sorted((root / "tickets").glob("TASK-*/ticket.md"))


def active_ticket_rows(root: Path, ticket_paths: list[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for ticket_path in active_ticket_paths(root, ticket_paths):
        frontmatter, body = split_ticket(ticket_path)
        reward = parse_reward_block(body)
        reward_info = reward_summary(frontmatter, reward)
        ticket_id = str(frontmatter.get("ticket_id") or ticket_path.parent.name)
        phase = str(frontmatter.get("phase", "")).strip()
        status = str(frontmatter.get("status", "")).strip()
        try:
            relative_path = str(ticket_path.relative_to(root))
        except ValueError:
            relative_path = str(ticket_path)
        rows.append(
            {
                "ticket_id": ticket_id,
                "path": relative_path,
                "title": str(frontmatter.get("title", "")).strip(),
                "phase": phase,
                "status": status,
                "ready": bool(frontmatter.get("ready", False)),
                "approval_required": bool(frontmatter.get("approval_required", False)),
                "claimed_by": frontmatter.get("claimed_by"),
                "blocked_by": frontmatter.get("blocked_by") or [],
                "next_action": str(frontmatter.get("next_action", "")).strip(),
                "reward": reward_info,
            }
        )
    return rows


def main() -> int:
    args = parse_args()
    root = Path(args.project_root).resolve()
    ledger_path = root / ".farplane" / "automation" / "spawned-threads.jsonl"
    spawned_latest = latest_rows_by_ticket(load_jsonl(ledger_path))

    active_rows = active_ticket_rows(root, args.ticket_paths)
    active_ticket_ids = {row["ticket_id"] for row in active_rows}
    ai_generated: list[dict[str, Any]] = []
    manual_active: list[dict[str, Any]] = []
    archive_needed: list[dict[str, Any]] = []

    for row in active_rows:
        latest = spawned_latest.get(row["ticket_id"])
        enriched = dict(row)
        if latest:
            enriched["pulse_ledger_status"] = latest.get("status")
            enriched["thread_id"] = latest.get("thread_id")
            enriched["latest_pulse_report"] = latest.get("report")
        if row["phase"] == "complete" or row["status"] == "done":
            archive_needed.append(enriched)
        if row["reward"]["has_ai_planning_marker"]:
            ai_generated.append(enriched)
        else:
            manual_active.append(enriched)

    open_pulse_workers = [
        row
        for row in spawned_latest.values()
        if str(row.get("status", "")).strip() in ACTIVE_STATUSES
        and str(row.get("ticket_id", "")).strip() in active_ticket_ids
    ]
    stale_open_worker_rows = [
        row
        for row in spawned_latest.values()
        if str(row.get("status", "")).strip() in ACTIVE_STATUSES
        and str(row.get("ticket_id", "")).strip() not in active_ticket_ids
    ]

    result = {
        "schema": "farplane.pulse_board.v1",
        "project_root": str(root),
        "ledger": str(ledger_path.relative_to(root)),
        "active_ticket_count": len(active_rows),
        "ai_generated_active_tickets": ai_generated,
        "pulse_managed_active_tickets": ai_generated,
        "manual_active_tickets": manual_active,
        "archive_needed_active_tickets": archive_needed,
        "open_pulse_workers": open_pulse_workers,
        "stale_open_worker_rows": stale_open_worker_rows,
        "manual_tickets_block_refill": False,
        "refill_allowed_if_no_ai_work": not ai_generated and not open_pulse_workers,
        "refill_allowed_if_no_pulse_work": not ai_generated and not open_pulse_workers,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
