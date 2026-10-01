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

CORE_DIR = Path(__file__).resolve().parents[1] / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))
from farplane_convex import RUNTIME_AGENT, TELEMETRY_TEAM, telemetry_project_id  # noqa: E402


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


def _config_value(name: str) -> str:
    """A setting from the environment, else Farplane's runtime config (as the hooks read it)."""
    value = os.environ.get(name, "").strip()
    if value:
        return value
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "core"))
        from runtime_config import read_config_value  # type: ignore

        return str(read_config_value(name) or "").strip()
    except Exception:
        return ""


def telemetry_config() -> tuple[str, str, float]:
    # Every event goes to Convex only: an explicit endpoint, else the Convex site's /ingest, the same
    # deployment the hook telemetry posts to. Nothing is logged locally; the metric engine reads Convex.
    url = _config_value("FARPLANE_TELEMETRY_API_URL")
    if not url:
        site = _config_value("FARPLANE_CONVEX_SITE_URL")
        url = f"{site.rstrip('/')}/ingest" if site else ""
    token = _config_value("FARPLANE_TELEMETRY_TOKEN")
    raw_timeout = os.environ.get("FARPLANE_TELEMETRY_TIMEOUT_SECS", "").strip()
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


def convex_runtime_row(project_root: Path, event: Mapping[str, object]) -> dict[str, object]:
    """The event as a runtime row of Convex's `events` table (the `/ingest` payload).

    The original event type rides in `activityType`; turn, ticket and counts ride in `detail` as JSON.
    """
    event_type = _safe_str(event.get("event_type")) or "runtime_event"
    timestamp = _safe_str(event.get("timestamp")) or now_iso()
    try:
        occurred_at = int(datetime.fromisoformat(timestamp.replace("Z", "+00:00")).timestamp() * 1000)
    except ValueError:
        occurred_at = int(datetime.now(timezone.utc).timestamp() * 1000)
    detail = {
        "eventId": event.get("event_id", ""),
        "turnId": event.get("turn_id", ""),
        "hookName": event.get("hook_name", ""),
        "phase": event.get("phase", ""),
        "status": event.get("status", ""),
        "outcome": event.get("outcome", ""),
        "counts": event.get("counts", {}),
        "metadata": event.get("metadata", {}),
    }
    row: dict[str, object] = {
        "teamId": TELEMETRY_TEAM,
        "projectId": telemetry_project_id(project_root),
        "agentId": RUNTIME_AGENT,
        "eventType": "activity_log",
        "activityType": event_type,
        "label": (_safe_str(event.get("summary")) or event_type)[:200],
        "detail": json.dumps(detail, sort_keys=True),
        "source": _safe_str(event.get("source")) or "runtime_telemetry",
        "stepKey": _safe_str(event.get("event_id")),
        "sessionKey": _safe_str(event.get("session_id")),
        "skillId": _safe_str(event.get("skill_name")),
        "taskId": _safe_str(event.get("ticket_id")),
        "occurredAt": occurred_at,
    }
    return {key: value for key, value in row.items() if value != ""}


def emit_farplane_event(project_root: Path, event: Mapping[str, object]) -> bool:
    """Send one event to Convex; False when it isn't configured or didn't take it (never raises)."""
    url, token, timeout = telemetry_config()
    if not url:
        return False

    data = json.dumps(convex_runtime_row(project_root, event)).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = request.Request(url, data=data, headers=headers, method="POST")
    try:
        with request.urlopen(req, timeout=timeout) as response:
            response.read(1)
            return 200 <= response.status < 300
    except (error.URLError, TimeoutError, OSError) as exc:
        reason = getattr(exc, "code", None) or getattr(exc, "reason", None) or type(exc).__name__
        print(f"farplane: runtime telemetry not delivered to Convex ({reason})", file=sys.stderr)
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
    return emit_farplane_event(project_root, event)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        raise SystemExit("runtime_telemetry.py is a helper module, not a CLI entrypoint.")
