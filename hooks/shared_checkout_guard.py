#!/usr/bin/env python3
"""Keep concurrent Codex tasks out of one primary Git checkout."""

from __future__ import annotations

import fcntl
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Mapping


LEASE_NAME = "farplane-shared-writer.json"
MUTEX_NAME = "farplane-shared-writer.lock"
DEFAULT_LEASE_SECONDS = 24 * 60 * 60


def read_payload() -> dict[str, object]:
    try:
        payload = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def payload_cwd(payload: Mapping[str, object]) -> Path | None:
    raw = payload.get("cwd") or payload.get("current_working_directory")
    if not isinstance(raw, str) or not raw.strip():
        return None
    try:
        return Path(raw).expanduser().resolve()
    except OSError:
        return None


def git_path(cwd: Path, argument: str) -> Path | None:
    result = subprocess.run(
        ["git", "rev-parse", argument],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode != 0 or not result.stdout.strip():
        return None
    path = Path(result.stdout.strip())
    return (cwd / path).resolve() if not path.is_absolute() else path.resolve()


def primary_checkout_git_dir(cwd: Path) -> Path | None:
    git_dir = git_path(cwd, "--git-dir")
    common_dir = git_path(cwd, "--git-common-dir")
    if git_dir is None or common_dir is None or git_dir != common_dir:
        return None
    return common_dir


def configured_lease_seconds() -> int:
    raw = os.environ.get("FARPLANE_SHARED_CHECKOUT_LEASE_SECONDS", "")
    try:
        value = int(raw)
    except ValueError:
        return DEFAULT_LEASE_SECONDS
    return value if value >= 60 else DEFAULT_LEASE_SECONDS


def load_lease(path: Path) -> dict[str, object]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return payload if isinstance(payload, dict) else {}


def write_lease(path: Path, payload: Mapping[str, object]) -> None:
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(dict(payload), sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def lease_is_live(lease: Mapping[str, object], now: float) -> bool:
    try:
        updated_at = float(lease.get("updated_at", 0))
    except (TypeError, ValueError):
        return False
    return bool(str(lease.get("session_id") or "").strip()) and now - updated_at < configured_lease_seconds()


def acquire_or_block(payload: Mapping[str, object], common_dir: Path, now: float) -> str | None:
    session_id = str(payload.get("session_id") or "").strip()
    if not session_id:
        return None
    lease_path = common_dir / LEASE_NAME
    mutex_path = common_dir / MUTEX_NAME
    with mutex_path.open("a+", encoding="utf-8") as mutex:
        fcntl.flock(mutex.fileno(), fcntl.LOCK_EX)
        lease = load_lease(lease_path)
        owner = str(lease.get("session_id") or "").strip()
        if owner and owner != session_id and lease_is_live(lease, now):
            return (
                "Shared Git checkout already has an active Codex writer "
                f"({owner}). Do not edit here. Move or hand off this task to a "
                "branch-backed worktree, or wait for the owning turn to stop."
            )
        write_lease(
            lease_path,
            {
                "session_id": session_id,
                "turn_id": str(payload.get("turn_id") or "").strip(),
                "cwd": str(payload_cwd(payload) or ""),
                "updated_at": now,
            },
        )
    return None


def release(payload: Mapping[str, object], common_dir: Path) -> None:
    session_id = str(payload.get("session_id") or "").strip()
    if not session_id:
        return
    lease_path = common_dir / LEASE_NAME
    mutex_path = common_dir / MUTEX_NAME
    with mutex_path.open("a+", encoding="utf-8") as mutex:
        fcntl.flock(mutex.fileno(), fcntl.LOCK_EX)
        lease = load_lease(lease_path)
        if str(lease.get("session_id") or "").strip() == session_id:
            lease_path.unlink(missing_ok=True)


def evaluate(payload: Mapping[str, object], *, now: float | None = None) -> str | None:
    if os.environ.get("FARPLANE_SHARED_CHECKOUT_GUARD", "1").strip().lower() in {"0", "false", "off"}:
        return None
    cwd = payload_cwd(payload)
    if cwd is None:
        return None
    common_dir = primary_checkout_git_dir(cwd)
    if common_dir is None:
        return None
    event = str(payload.get("hook_event_name") or "").strip()
    if event == "Stop":
        release(payload, common_dir)
        return None
    if event == "UserPromptSubmit":
        return acquire_or_block(payload, common_dir, now if now is not None else time.time())
    return None


def main() -> int:
    payload = read_payload()
    try:
        reason = evaluate(payload)
    except (OSError, subprocess.SubprocessError):
        return 0
    if reason:
        print(json.dumps({"decision": "block", "reason": reason}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
