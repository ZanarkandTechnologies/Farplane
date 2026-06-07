#!/usr/bin/env python3
"""Plan incremental reads for pinned Notion task pages."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any


DEFAULT_STATE_PATH = Path(".farplane/state/notion-context/pinned-tasks-read-state.json")


class ReadCheckError(ValueError):
    """Raised when pinned task read-check input is invalid."""


@dataclass(frozen=True)
class PinnedTask:
    url: str
    name: str
    last_edited_time: str | None
    act_time: str | None


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def iso_week(value: date | None = None) -> str:
    current = value or date.today()
    year, week, _ = current.isocalendar()
    return f"{year}-W{week:02d}"


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as exc:
        raise ReadCheckError(f"{path}: invalid JSON: {exc}") from exc


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def string_value(raw: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        value = raw.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def bool_value(raw: dict[str, Any], *keys: str) -> bool:
    for key in keys:
        value = raw.get(key)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized in {"__yes__", "true", "yes", "1"}:
                return True
            if normalized in {"__no__", "false", "no", "0", ""}:
                return False
    return False


def parse_date_prefix(value: str | None) -> date | None:
    if not value or len(value) < 10:
        return None
    try:
        return date.fromisoformat(value[:10])
    except ValueError:
        return None


def in_recent_window(task_date: date | None, *, today: date, days: int) -> bool:
    if task_date is None:
        return True
    return today - timedelta(days=days) <= task_date <= today


def parse_tasks(raw: Any) -> list[PinnedTask]:
    rows = raw.get("rows") or raw.get("results") or raw.get("tasks") if isinstance(raw, dict) else raw
    if not isinstance(rows, list):
        raise ReadCheckError("input must be a JSON array or an object with rows/results/tasks")
    tasks: list[PinnedTask] = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            raise ReadCheckError(f"row {index}: expected object")
        if not bool_value(row, "Pinned", "pinned"):
            continue
        url = string_value(row, "url", "URL")
        if not url:
            raise ReadCheckError(f"row {index}: pinned task is missing url")
        tasks.append(
            PinnedTask(
                url=url,
                name=string_value(row, "Name", "name", "title") or url,
                last_edited_time=string_value(
                    row,
                    "last_edited_time",
                    "lastEditedTime",
                    "lastEdited",
                    "last_edit_time",
                ),
                act_time=string_value(
                    row,
                    "Act Time",
                    "act_time",
                    "actTime",
                    "date:Act Time:start",
                    "date:Act Time",
                ),
            )
        )
    return tasks


def recent_tasks(tasks: list[PinnedTask], *, today: date, days: int) -> list[PinnedTask]:
    return [
        task
        for task in tasks
        if in_recent_window(parse_date_prefix(task.act_time), today=today, days=days)
    ]


def normalized_state(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        return {"tasks": {}}
    if not isinstance(raw.get("tasks"), dict):
        raw["tasks"] = {}
    return raw


def due_tasks(
    tasks: list[PinnedTask],
    state: dict[str, Any],
    *,
    current_week: str,
    weekly_full_read: bool,
) -> tuple[list[dict[str, Any]], bool]:
    state_tasks = state.get("tasks", {})
    if not isinstance(state_tasks, dict):
        state_tasks = {}
    week_changed = weekly_full_read and state.get("last_full_read_week") != current_week
    due: list[dict[str, Any]] = []
    for task in tasks:
        prior = state_tasks.get(task.url)
        prior_marker = prior.get("last_edited_time") if isinstance(prior, dict) else None
        reasons: list[str] = []
        if week_changed:
            reasons.append("weekly_full_read")
        if not isinstance(prior, dict):
            reasons.append("new_pinned_task")
        elif task.last_edited_time is None:
            reasons.append("missing_update_marker")
        elif prior_marker != task.last_edited_time:
            reasons.append("last_edited_changed")
        if reasons:
            due.append(
                {
                    "url": task.url,
                    "name": task.name,
                    "last_edited_time": task.last_edited_time,
                    "reasons": reasons,
                }
            )
    return due, week_changed


def record_reads(
    state: dict[str, Any],
    tasks: list[PinnedTask],
    read_urls: set[str],
    *,
    current_week: str,
    read_at: str,
) -> dict[str, Any]:
    next_tasks = dict(state.get("tasks", {}) if isinstance(state.get("tasks"), dict) else {})
    by_url = {task.url: task for task in tasks}
    for url in sorted(read_urls):
        task = by_url.get(url)
        next_tasks[url] = {
            "name": task.name if task else url,
            "last_edited_time": task.last_edited_time if task else None,
            "last_read_at": read_at,
        }
    return {
        **state,
        "last_checked_at": read_at,
        "last_full_read_week": current_week,
        "tasks": next_tasks,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("plan", "record"))
    parser.add_argument("--rows", required=True, help="JSON file containing pinned task rows from MCP")
    parser.add_argument("--state", default=str(DEFAULT_STATE_PATH), help="runtime state file")
    parser.add_argument("--today", type=date.fromisoformat, help="override current date for tests")
    parser.add_argument(
        "--recent-days",
        type=int,
        default=14,
        help="only plan pinned rows whose Act Time is within this many days; rows missing Act Time are kept",
    )
    parser.add_argument("--no-weekly-full-read", action="store_true")
    parser.add_argument("--read-url", action="append", default=[], help="record a page URL as read")
    parser.add_argument("--json", action="store_true", help="print JSON output")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    state_path = Path(args.state)
    try:
        all_tasks = parse_tasks(read_json(Path(args.rows)))
        today = args.today or date.today()
        tasks = recent_tasks(all_tasks, today=today, days=args.recent_days)
        state = normalized_state(read_json(state_path))
        current_week = iso_week(today)
        if args.command == "plan":
            due, week_changed = due_tasks(
                tasks,
                state,
                current_week=current_week,
                weekly_full_read=not args.no_weekly_full_read,
            )
            output = {
                "state_path": str(state_path),
                "current_week": current_week,
                "recent_days": args.recent_days,
                "input_pinned_count": len(all_tasks),
                "pinned_count": len(tasks),
                "due_count": len(due),
                "weekly_full_read_due": week_changed,
                "read_required": due,
            }
        else:
            read_urls = set(args.read_url) or {task.url for task in tasks}
            output = record_reads(
                state,
                tasks,
                read_urls,
                current_week=current_week,
                read_at=utc_now_iso(),
            )
            write_json(state_path, output)
        if args.json:
            print(json.dumps(output, indent=2, sort_keys=True))
        elif args.command == "plan":
            for item in output["read_required"]:
                print(f"{item['url']} {item['name']} ({', '.join(item['reasons'])})")
        else:
            print(f"recorded {len(read_urls)} read pinned task(s) in {state_path}")
    except ReadCheckError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
