#!/usr/bin/env python3
"""Send Codex lifecycle hook pings to the Farplane UI Convex telemetry ingress."""

from __future__ import annotations

import json
import os
import re
import socket
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urljoin

CORE_DIR = Path(__file__).resolve().parents[1] / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from runtime_config import hydrate_process_env, read_config_value


def clean_text(value: object, limit: int) -> str | None:
    if not isinstance(value, str):
        return None
    trimmed = value.strip()
    if not trimmed:
        return None
    return trimmed[:limit]


def resolve_directory(start: object) -> Path | None:
    if not isinstance(start, str) or not start.strip():
        return None

    try:
        current = Path(start).expanduser().resolve()
    except Exception:
        return None

    if current.is_file():
        current = current.parent

    return current


def find_git_root(start: object) -> Path | None:
    start_path = resolve_directory(start)
    if start_path is None:
        return None

    for candidate in (start_path, *start_path.parents):
        if (candidate / ".git").exists():
            return candidate

    return None


def get_project_metadata(event: dict[str, object]) -> tuple[str | None, str | None]:
    explicit_name = clean_text(os.getenv("AIKAGE_PROJECT_NAME"), 120)
    explicit_directory = clean_text(os.getenv("AIKAGE_PROJECT_DIRECTORY"), 240)
    if explicit_name or explicit_directory:
        return explicit_name, explicit_directory

    cwd = (
        event.get("cwd")
        or event.get("current_working_directory")
        or os.getenv("PWD")
        or os.getcwd()
    )
    project_root = find_git_root(cwd) or resolve_directory(cwd)
    if project_root is None or not project_root.name:
        return None, None

    return clean_text(project_root.name, 120), clean_text(str(project_root), 240)


def telemetry_endpoint() -> str | None:
    explicit = clean_text(read_config_value("FARPLANE_TELEMETRY_HOOKS_URL"), 500)
    if explicit:
        return explicit

    site_url = clean_text(read_config_value("FARPLANE_CONVEX_SITE_URL"), 500)
    if not site_url:
        return None
    return urljoin(site_url.rstrip("/") + "/", "telemetry/hooks")


def safe_id_part(value: str) -> str:
    slug = re.sub(r"[^a-z0-9_.:-]+", "-", value.lower())
    slug = re.sub(r"-+", "-", slug).strip("-")
    return (slug or "unknown")[:120]


def project_id_from_directory(value: str | None) -> str | None:
    if not value:
        return None
    return f"codex-proj-{safe_id_part(value)}"


def hook_type(event: dict[str, object]) -> str:
    return (
        clean_text(event.get("hook_event_name"), 160)
        or clean_text(event.get("hookType"), 160)
        or clean_text(event.get("event"), 160)
        or "Heartbeat"
    )


def event_type_for_hook(hook: str) -> str:
    if hook in {"UserPromptSubmit", "TurnStart"}:
        return "turn_start"
    if hook in {"Stop", "TurnEnd"}:
        return "turn_end"
    return "heartbeat"


def source_for_hook(hook: str) -> str:
    if hook == "UserPromptSubmit":
        return "codex-user-prompt"
    if hook == "Stop":
        return "codex-stop"
    return "codex-hook"


def event_key_for_hook(hook: str, session_id: str | None, turn_id: str | None) -> str | None:
    if not session_id or not turn_id:
        return None
    return f"codex-lifecycle:{session_id}:{turn_id}:{hook}"


def read_payload() -> dict[str, object]:
    try:
        event = json.load(sys.stdin)
    except Exception as error:
        print(f"farplane: failed to parse hook payload: {error}", file=sys.stderr)
        return {}
    return event if isinstance(event, dict) else {}


def build_ping(event: dict[str, object]) -> dict[str, object]:
    try:
        active_agents = int(os.getenv("AIKAGE_ACTIVE_AGENTS", "1"))
    except ValueError:
        active_agents = 1

    machine_name = clean_text(os.getenv("AIKAGE_MACHINE_NAME"), 120)
    if machine_name is None:
        machine_name = clean_text(socket.gethostname(), 120)
    project_name, project_directory = get_project_metadata(event)

    current_hook_type = hook_type(event)
    event_type = event_type_for_hook(current_hook_type)
    prompt = clean_text(event.get("prompt"), 100) if event_type == "turn_start" else None
    session_id = clean_text(event.get("session_id"), 120)
    turn_id = clean_text(event.get("turn_id"), 120)
    project_id = project_id_from_directory(project_directory)

    return {
        "hookName": "farplane-console-ping",
        "hookType": current_hook_type,
        "projectId": project_id,
        "sessionId": session_id,
        "eventKey": event_key_for_hook(current_hook_type, session_id, turn_id),
        "payload": {
            "eventType": event_type,
            "source": source_for_hook(current_hook_type),
            "activeAgentCount": max(active_agents, 1),
            "prompt": prompt,
            "agentName": clean_text(os.getenv("AIKAGE_AGENT_NAME", "codex"), 80),
            "workflowName": clean_text(os.getenv("AIKAGE_WORKFLOW_NAME"), 120),
            "machineName": machine_name,
            "projectName": project_name,
            "projectDirectory": project_directory,
            "cwd": project_directory,
            "projectId": project_id,
            "sessionId": session_id,
            "turnId": turn_id,
        },
    }


def main() -> int:
    hydrate_process_env()
    event = read_payload()
    if not event:
        return 0

    endpoint = telemetry_endpoint()
    if endpoint is None:
        return 0

    headers = {"content-type": "application/json"}
    token = clean_text(read_config_value("FARPLANE_TELEMETRY_TOKEN"), 500)
    if token:
        headers["x-farplane-telemetry-token"] = token

    request = urllib.request.Request(
        endpoint,
        data=json.dumps(build_ping(event)).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=2) as response:
            response.read()
    except urllib.error.URLError as error:
        print(f"farplane: telemetry ping failed: {error}", file=sys.stderr)
    except Exception as error:
        print(f"farplane: unexpected telemetry ping error: {error}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
