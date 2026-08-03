#!/usr/bin/env python3
"""Block commits when the committing session's ticket is still active.

Multiple Codex workers can share one worktree, so unrelated active tickets are
allowed. This gate blocks only when the current process exposes a session id
and the ticket/thread association log ties that session to a ticket still on
the active board.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
TICKET_ID_PREFIX = "TASK-"
ARCHIVE_DIR = "archive"
SESSION_ENV_KEYS = (
    "FARPLANE_SESSION_ID",
    "CODEX_SESSION_ID",
    "CODEX_THREAD_ID",
    "CODEX_CONVERSATION_ID",
)


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}
    result: dict[str, str] = {}
    for line in parts[0][4:].splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def active_ticket_dirs(root: Path) -> list[Path]:
    tickets_dir = root / "tickets"
    if not tickets_dir.is_dir():
        return []
    return sorted(
        path
        for path in tickets_dir.iterdir()
        if path.is_dir() and path.name.startswith(TICKET_ID_PREFIX)
    )


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            rows.append(
                {
                    "_parse_error": f"{path}:{line_number}: invalid JSONL row: {exc}",
                }
            )
            continue
        if isinstance(value, dict):
            rows.append(value)
    return rows


def associations_by_ticket(root: Path) -> dict[str, list[dict[str, Any]]]:
    path = root / ".farplane" / "state" / "ticket-thread-associations.jsonl"
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in read_jsonl(path):
        ticket_id = str(row.get("ticket_id") or "").strip()
        if ticket_id.startswith(TICKET_ID_PREFIX):
            grouped.setdefault(ticket_id, []).append(row)
    return grouped


def associated_tickets_for_sessions(root: Path, session_ids: list[str]) -> dict[str, list[dict[str, Any]]]:
    if not session_ids:
        return {}
    wanted = set(session_ids)
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in read_jsonl(root / ".farplane" / "state" / "ticket-thread-associations.jsonl"):
        row_session_ids = {
            str(row.get("session_id") or "").strip(),
            str(row.get("thread_id") or "").strip(),
        }
        if not wanted.intersection(row_session_ids):
            continue
        ticket_id = str(row.get("ticket_id") or "").strip()
        if ticket_id.startswith(TICKET_ID_PREFIX):
            grouped.setdefault(ticket_id, []).append(row)
    return grouped


def session_ids_from_env(environ: dict[str, str] | None = None) -> list[str]:
    source = environ if environ is not None else os.environ
    seen: set[str] = set()
    session_ids: list[str] = []
    for key in SESSION_ENV_KEYS:
        value = str(source.get(key) or "").strip()
        if value and value not in seen:
            seen.add(value)
            session_ids.append(value)
    return session_ids


def ticket_state(ticket_dir: Path) -> str:
    ticket_path = ticket_dir / "ticket.md"
    if not ticket_path.is_file():
        return "missing ticket.md"
    frontmatter = parse_frontmatter(ticket_path)
    status = frontmatter.get("status", "?")
    title = frontmatter.get("title", "").strip()
    suffix = f" - {title}" if title else ""
    return f"status={status}{suffix}"


def active_completed_ticket_errors(root: Path) -> list[str]:
    errors: list[str] = []
    for ticket_dir in active_ticket_dirs(root):
        ticket_path = ticket_dir / "ticket.md"
        if not ticket_path.is_file():
            continue
        frontmatter = parse_frontmatter(ticket_path)
        status = frontmatter.get("status", "")
        if status in {"done", "failed", "rejected"}:
            errors.append(
                f"active ticket is terminal and should be archived: "
                f"{ticket_path.relative_to(root)} ({ticket_state(ticket_dir)})"
            )
    return errors


def archive_ticket_exists(root: Path, ticket_id: str) -> bool:
    return (root / "tickets" / ARCHIVE_DIR / ticket_id / "ticket.md").is_file()


def validate_ticket_closure(
    root: Path,
    *,
    environ: dict[str, str] | None = None,
) -> list[str]:
    errors: list[str] = []
    active_dirs = active_ticket_dirs(root)
    associations = associations_by_ticket(root)
    session_ids = session_ids_from_env(environ)
    current_session_tickets = associated_tickets_for_sessions(root, session_ids)
    missing_archives = sorted(
        ticket_id
        for ticket_id in associations
        if not (root / "tickets" / ticket_id / "ticket.md").is_file()
        and not archive_ticket_exists(root, ticket_id)
    )
    if missing_archives:
        errors.append("association rows point at tickets that are neither active nor archived:")
        for ticket_id in missing_archives:
            errors.append(f"  - {ticket_id}")

    for current_ticket_id, rows in sorted(current_session_tickets.items()):
        active_ticket = root / "tickets" / current_ticket_id / "ticket.md"
        archived_ticket = root / "tickets" / ARCHIVE_DIR / current_ticket_id / "ticket.md"
        if active_ticket.is_file():
            active_dir = active_ticket.parent
            errors.append(
                f"current session is still tied to active {current_ticket_id}: "
                f"{active_ticket.relative_to(root)} ({ticket_state(active_dir)})"
            )
            for row in rows[-3:]:
                thread_id = row.get("thread_id") or row.get("session_id") or "unknown-thread"
                confidence = row.get("confidence") or "unknown-confidence"
                observed_at = row.get("observed_at") or "unknown-time"
                errors.append(
                    f"  associated thread: {thread_id} ({confidence}, observed_at={observed_at})"
                )
        elif not archived_ticket.is_file():
            errors.append(
                f"current session points at {current_ticket_id}, but that ticket is neither active nor archived"
            )

    parse_errors = [
        str(row["_parse_error"])
        for row in read_jsonl(root / ".farplane" / "state" / "ticket-thread-associations.jsonl")
        if "_parse_error" in row
    ]
    errors.extend(parse_errors)
    return errors


def validate_terminal_ticket_hygiene(root: Path) -> list[str]:
    """Report terminal packets still awaiting canonical remote closeout."""
    return active_completed_ticket_errors(root)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="Repository root to validate.",
    )
    parser.add_argument(
        "--terminal-hygiene",
        action="store_true",
        help="Report terminal active-board packets without session closure checks.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    session_ids = session_ids_from_env()
    errors = (
        validate_terminal_ticket_hygiene(root)
        if args.terminal_hygiene
        else validate_ticket_closure(root)
    )
    if errors:
        label = "ticket terminal hygiene" if args.terminal_hygiene else "ticket closure gate"
        print(f"{label} failed")
        if not args.terminal_hygiene:
            print("Close or archive the ticket for this committing session before committing.")
        for error in errors:
            print(error)
        return 1

    association_count = len(associations_by_ticket(root))
    active_count = len(active_ticket_dirs(root))
    if session_ids:
        session_note = f"session_ids={','.join(session_ids)}"
    else:
        session_note = "no session env"
    print(
        f"ticket closure gate OK ({active_count} active tickets allowed, "
        f"{association_count} associated ticket ids, {session_note})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
