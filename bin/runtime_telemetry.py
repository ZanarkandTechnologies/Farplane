from __future__ import annotations

import json
import os
import socket
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping
from urllib import error, request


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _safe_str(value: object) -> str:
    if isinstance(value, str):
        return value.strip()
    return ""


def _mapping_value(mapping: Mapping[str, object] | None, key: str) -> str:
    if not isinstance(mapping, Mapping):
        return ""
    return _safe_str(mapping.get(key))


def telemetry_config() -> tuple[str, str, float]:
    url = os.environ.get("CODEXTER_TELEMETRY_API_URL", "").strip()
    token = os.environ.get("CODEXTER_TELEMETRY_API_TOKEN", "").strip()
    raw_timeout = os.environ.get("CODEXTER_TELEMETRY_TIMEOUT_SECS", "").strip()
    try:
        timeout = float(raw_timeout) if raw_timeout else 2.0
    except ValueError:
        timeout = 2.0
    return url, token, max(timeout, 0.2)


def emit_hook_telemetry(
    *,
    event_type: str,
    hook_event_name: str,
    payload: Mapping[str, object] | None,
    project_root: Path | None,
    current_run: Mapping[str, object] | None = None,
    runtime_claim: Mapping[str, object] | None = None,
    extra: Mapping[str, object] | None = None,
) -> bool:
    url, token, timeout = telemetry_config()
    if not url:
        return False

    body: dict[str, object] = {
        "timestamp": now_iso(),
        "event_type": event_type,
        "hook_event_name": hook_event_name,
        "project_root": str(project_root) if project_root is not None else "",
        "hostname": socket.gethostname(),
        "pid": os.getpid(),
        "session_id": _mapping_value(payload, "session_id")
        or _mapping_value(runtime_claim, "session_id")
        or _mapping_value(current_run, "session_id"),
        "turn_id": _mapping_value(payload, "turn_id"),
        "cwd": _mapping_value(payload, "cwd")
        or _mapping_value(payload, "workdir")
        or _mapping_value(payload, "current_working_directory"),
        "ticket_id": _mapping_value(runtime_claim, "ticket_id")
        or _mapping_value(current_run, "ticket_id"),
        "run_id": _mapping_value(runtime_claim, "run_id")
        or _mapping_value(current_run, "run_id"),
        "session_name": _mapping_value(runtime_claim, "session_name")
        or _mapping_value(current_run, "session_name"),
        "worker_name": _mapping_value(runtime_claim, "worker_name")
        or _mapping_value(current_run, "worker_name"),
        "skill_name": _mapping_value(runtime_claim, "skill_name")
        or _mapping_value(current_run, "skill_name"),
        "phase": _mapping_value(current_run, "phase") or _mapping_value(runtime_claim, "phase"),
        "status": _mapping_value(current_run, "status") or _mapping_value(runtime_claim, "status"),
    }
    if isinstance(extra, Mapping):
        body.update(extra)

    data = json.dumps(body).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = request.Request(url, data=data, headers=headers, method="POST")
    try:
        with request.urlopen(req, timeout=timeout) as response:
            response.read(1)
            return 200 <= response.status < 300
    except (error.URLError, TimeoutError, OSError):
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        raise SystemExit("runtime_telemetry.py is a helper module, not a CLI entrypoint.")
