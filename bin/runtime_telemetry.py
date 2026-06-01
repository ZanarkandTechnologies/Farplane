from __future__ import annotations

import json
import os
import socket
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping
from uuid import uuid4
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


def _safe_metadata_value(value: object) -> str | int | float | bool | None:
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        return value.strip()[:500]
    return str(value)[:500]


def event_log_path(project_root: Path, timestamp: str) -> Path:
    day = timestamp[:10] if len(timestamp) >= 10 else now_iso()[:10]
    return project_root / ".harness" / "events" / f"{day}.jsonl"


def telemetry_config() -> tuple[str, str, float]:
    url = os.environ.get("CODEXTER_TELEMETRY_API_URL", "").strip()
    token = os.environ.get("CODEXTER_TELEMETRY_API_TOKEN", "").strip()
    raw_timeout = os.environ.get("CODEXTER_TELEMETRY_TIMEOUT_SECS", "").strip()
    try:
        timeout = float(raw_timeout) if raw_timeout else 2.0
    except ValueError:
        timeout = 2.0
    return url, token, max(timeout, 0.2)


def build_event(
    *,
    event_type: str,
    source: str,
    project_root: Path,
    payload: Mapping[str, object] | None = None,
    current_run: Mapping[str, object] | None = None,
    runtime_claim: Mapping[str, object] | None = None,
    hook_name: str = "",
    status: str = "",
    outcome: str = "",
    summary: str = "",
    counts: Mapping[str, object] | None = None,
    metadata: Mapping[str, object] | None = None,
) -> dict[str, object]:
    timestamp = now_iso()
    safe_metadata = {
        str(key): _safe_metadata_value(value)
        for key, value in (metadata or {}).items()
        if str(key) not in {"prompt", "raw_text", "last_assistant_message", "transcript_path"}
    }
    safe_counts = {
        str(key): value
        for key, value in (counts or {}).items()
        if isinstance(value, (int, float))
    }
    return {
        "schema_version": 1,
        "event_id": f"evt_{timestamp}_{uuid4().hex[:12]}",
        "event_type": event_type,
        "timestamp": timestamp,
        "source": source,
        "project_root": str(project_root),
        "project_name": project_root.name,
        "session_id": _mapping_value(payload, "session_id")
        or _mapping_value(runtime_claim, "session_id")
        or _mapping_value(current_run, "session_id"),
        "turn_id": _mapping_value(payload, "turn_id"),
        "ticket_id": _mapping_value(runtime_claim, "ticket_id")
        or _mapping_value(current_run, "ticket_id"),
        "skill_name": _mapping_value(runtime_claim, "skill_name")
        or _mapping_value(current_run, "skill_name")
        or _mapping_value(metadata, "skill_name"),
        "hook_name": hook_name,
        "phase": _mapping_value(current_run, "phase") or _mapping_value(runtime_claim, "phase"),
        "status": status or _mapping_value(current_run, "status") or _mapping_value(runtime_claim, "status"),
        "outcome": outcome,
        "summary": summary[:500],
        "counts": safe_counts,
        "metadata": safe_metadata,
        "privacy": {
            "prompt_included": False,
            "raw_transcript_included": False,
            "redaction_version": 1,
        },
    }


def write_local_event(project_root: Path, event: Mapping[str, object]) -> Path:
    timestamp = _safe_str(event.get("timestamp")) or now_iso()
    path = event_log_path(project_root, timestamp)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(dict(event), sort_keys=True) + "\n")
    return path


def emit_codexter_event(project_root: Path, event: Mapping[str, object]) -> bool:
    write_local_event(project_root, event)
    url, token, timeout = telemetry_config()
    if not url:
        return False

    data = json.dumps(dict(event)).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = request.Request(url, data=data, headers=headers, method="POST")
    try:
        with request.urlopen(req, timeout=timeout) as response:
            response.read(1)
            return 200 <= response.status < 300
    except (error.URLError, TimeoutError, OSError):
        failed = project_root / ".harness" / "events" / "failed-sync.jsonl"
        failed.parent.mkdir(parents=True, exist_ok=True)
        with failed.open("a", encoding="utf-8") as handle:
            handle.write(
                json.dumps(
                    {
                        "timestamp": now_iso(),
                        "event_id": event.get("event_id", ""),
                        "event_type": event.get("event_type", ""),
                        "reason": "network_error",
                    },
                    sort_keys=True,
                )
                + "\n"
            )
        return False


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
    if project_root is None:
        return False

    metadata: dict[str, object] = {
        "hostname": socket.gethostname(),
        "pid": os.getpid(),
        "cwd": _mapping_value(payload, "cwd")
        or _mapping_value(payload, "workdir")
        or _mapping_value(payload, "current_working_directory"),
        "run_id": _mapping_value(runtime_claim, "run_id")
        or _mapping_value(current_run, "run_id"),
        "session_name": _mapping_value(runtime_claim, "session_name")
        or _mapping_value(current_run, "session_name"),
        "worker_name": _mapping_value(runtime_claim, "worker_name")
        or _mapping_value(current_run, "worker_name"),
    }
    summary = ""
    status = ""
    outcome = ""
    counts: Mapping[str, object] | None = None
    if isinstance(extra, Mapping):
        summary = _safe_str(extra.get("summary"))
        status = _safe_str(extra.get("status"))
        outcome = _safe_str(extra.get("outcome"))
        raw_counts = extra.get("counts")
        counts = raw_counts if isinstance(raw_counts, Mapping) else None
        metadata.update({str(key): value for key, value in extra.items() if key not in {"summary", "status", "outcome", "counts"}})

    event = build_event(
        event_type=event_type,
        source=_mapping_value(extra, "source") or "runtime_telemetry",
        project_root=project_root,
        payload=payload,
        current_run=current_run,
        runtime_claim=runtime_claim,
        hook_name=hook_event_name,
        status=status,
        outcome=outcome,
        summary=summary,
        counts=counts,
        metadata=metadata,
    )
    return emit_codexter_event(project_root, event)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        raise SystemExit("runtime_telemetry.py is a helper module, not a CLI entrypoint.")
