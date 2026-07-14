#!/usr/bin/env python3
"""Allocate collision-free ticket IDs from active and archived durable state."""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from contextlib import contextmanager
from pathlib import Path


TICKET_ID_RE = re.compile(r"TASK-(\d{4,})")
FRONTMATTER_ID_RE = re.compile(r"^ticket_id:\s*(TASK-\d{4,})\s*$", re.MULTILINE)


def durable_ticket_ids(project_root: Path) -> set[str]:
    tickets_root = project_root / "tickets"
    ids: set[str] = set()
    if not tickets_root.exists():
        return ids
    paths = list(tickets_root.glob("TASK-*/ticket.md"))
    archive_root = tickets_root / "archive"
    if archive_root.exists():
        paths.extend(archive_root.rglob("ticket.md"))
    for path in paths:
        for part in path.parts:
            match = TICKET_ID_RE.fullmatch(part)
            if match:
                ids.add(match.group(0))
        try:
            match = FRONTMATTER_ID_RE.search(path.read_text(encoding="utf-8"))
        except OSError:
            match = None
        if match:
            ids.add(match.group(1))
    return ids


def next_ticket_ids(project_root: Path, count: int = 1) -> list[str]:
    if count < 1:
        raise ValueError("count must be positive")
    used = durable_ticket_ids(project_root)
    highest = max((int(ticket_id.split("-", 1)[1]) for ticket_id in used), default=0)
    return [f"TASK-{number:04d}" for number in range(highest + 1, highest + count + 1)]


def next_ticket_id(project_root: Path) -> str:
    return next_ticket_ids(project_root, 1)[0]


def reservations_path(project_root: Path) -> Path:
    return project_root / ".farplane" / "state" / "ticket-id-reservations.json"


@contextmanager
def reservation_lock(project_root: Path, timeout_seconds: float = 5.0):
    lock = reservations_path(project_root).with_suffix(".lock")
    lock.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + timeout_seconds
    fd: int | None = None
    while fd is None:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            if time.monotonic() >= deadline:
                raise TimeoutError("ticket ID reservation lock is busy")
            time.sleep(0.01)
    try:
        yield
    finally:
        os.close(fd)
        lock.unlink(missing_ok=True)


def reserve_ticket_ids(project_root: Path, count: int = 1) -> list[str]:
    with reservation_lock(project_root):
        path = reservations_path(project_root)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            payload = {"reserved": []}
        reserved = {str(value) for value in payload.get("reserved", [])}
        used = durable_ticket_ids(project_root) | reserved
        highest = max((int(ticket_id.split("-", 1)[1]) for ticket_id in used), default=0)
        values = [f"TASK-{number:04d}" for number in range(highest + 1, highest + count + 1)]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"reserved": sorted(reserved | set(values))}, indent=2) + "\n", encoding="utf-8")
        return values


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--reserve", action="store_true")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    values = reserve_ticket_ids(root, args.count) if args.reserve else next_ticket_ids(root, args.count)
    print(json.dumps({"ticket_ids": values}) if args.json else "\n".join(values))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
