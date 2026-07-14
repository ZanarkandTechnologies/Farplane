#!/usr/bin/env python3
"""Persist a bounded circuit for shared worker create/lookup failures."""

from __future__ import annotations

import argparse
import json
import os
import time
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path


THRESHOLD = 2
PROBE_COOLDOWN = timedelta(minutes=30)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_iso(value: object) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def state_path(project_root: Path) -> Path:
    return project_root / ".farplane" / "state" / "dispatch-circuit.json"


@contextmanager
def state_lock(project_root: Path, timeout_seconds: float = 5.0):
    lock = state_path(project_root).with_suffix(".lock")
    lock.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + timeout_seconds
    fd: int | None = None
    while fd is None:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except FileExistsError:
            if time.monotonic() >= deadline:
                raise TimeoutError("dispatch circuit lock is busy")
            time.sleep(0.01)
    try:
        yield
    finally:
        os.close(fd)
        lock.unlink(missing_ok=True)


def load_state(project_root: Path) -> dict[str, object]:
    path = state_path(project_root)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        payload = {}
    return {
        "status": payload.get("status", "closed"),
        "consecutive_failures": int(payload.get("consecutive_failures") or 0),
        "last_failure_at": payload.get("last_failure_at"),
        "last_reason": payload.get("last_reason"),
        "next_probe_at": payload.get("next_probe_at"),
        "health_check_required": payload.get("health_check_required", "one verified create-or-lookup success"),
    }


def save_state(project_root: Path, state: dict[str, object]) -> dict[str, object]:
    path = state_path(project_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return state


def record_failure(project_root: Path, reason: str, *, now: datetime | None = None) -> dict[str, object]:
    with state_lock(project_root):
        state = load_state(project_root)
        failures = int(state["consecutive_failures"]) + 1
        observed = now or datetime.now(timezone.utc)
        state.update(status="open" if failures >= THRESHOLD else "closed", consecutive_failures=failures,
                     last_failure_at=observed.isoformat().replace("+00:00", "Z"), last_reason=reason,
                     next_probe_at=(observed + PROBE_COOLDOWN).isoformat().replace("+00:00", "Z") if failures >= THRESHOLD else None)
        return save_state(project_root, state)


def record_success(project_root: Path) -> dict[str, object]:
    with state_lock(project_root):
        state = load_state(project_root)
        state.update(status="closed", consecutive_failures=0, last_reason=None, next_probe_at=None)
        return save_state(project_root, state)


def request_probe(project_root: Path, *, now: datetime | None = None) -> dict[str, object]:
    with state_lock(project_root):
        state = load_state(project_root)
        observed = now or datetime.now(timezone.utc)
        due = parse_iso(state.get("next_probe_at"))
        if state["status"] == "closed":
            return {**state, "probe_allowed": True, "probe_reason": "circuit_closed"}
        if state["status"] == "open" and due is not None and observed >= due:
            state.update(status="half_open")
            save_state(project_root, state)
            return {**state, "probe_allowed": True, "probe_reason": "cooldown_elapsed_single_probe"}
        return {**state, "probe_allowed": False, "probe_reason": "cooldown_pending_or_probe_in_flight"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("status", "probe", "failure", "success"))
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--reason", default="worker create or lookup did not return")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    state = (record_failure(root, args.reason) if args.command == "failure"
             else record_success(root) if args.command == "success"
             else request_probe(root) if args.command == "probe" else load_state(root))
    print(json.dumps(state, indent=2, sort_keys=True))
    if args.command == "probe":
        return 0 if state.get("probe_allowed") else 2
    return 2 if args.command == "status" and state["status"] != "closed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
