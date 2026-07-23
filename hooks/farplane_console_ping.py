#!/usr/bin/env python3
"""Send Codex lifecycle hook pings to the Farplane UI Convex telemetry ingress."""

from __future__ import annotations

import hashlib
import json
import os
import re
import socket
import sys
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin

CORE_DIR = Path(__file__).resolve().parents[1] / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from runtime_config import codex_home, hydrate_process_env, read_config_value


TITLE_LIMIT = 120
SESSION_INDEX_READ_LIMIT = 8 * 1024 * 1024
TICKET_ID_PATTERN = re.compile(r"\bTASK-\d{4}\b")


def clean_text(value: object, limit: int) -> str | None:
    if not isinstance(value, str):
        return None
    trimmed = value.strip()
    if not trimmed:
        return None
    return trimmed[:limit]


def clean_title(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    normalized = " ".join(re.sub(r"[\x00-\x1f\x7f]+", " ", value).split())
    return normalized[:TITLE_LIMIT] or None


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


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


def find_project_root(start: object) -> Path | None:
    start_path = resolve_directory(start)
    if start_path is None:
        return None
    for candidate in (start_path, *start_path.parents):
        if (candidate / "tickets").is_dir() or (candidate / ".farplane").is_dir():
            return candidate
    return find_git_root(start)


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
    if hook == "SubagentStart":
        return "subagent_start"
    if hook == "SubagentStop":
        return "subagent_stop"
    return "heartbeat"


def source_for_hook(hook: str) -> str:
    if hook == "UserPromptSubmit":
        return "codex-user-prompt"
    if hook == "Stop":
        return "codex-stop"
    if hook == "SubagentStart":
        return "codex-subagent-start"
    if hook == "SubagentStop":
        return "codex-subagent-stop"
    return "codex-hook"


def event_key_for_hook(
    hook: str,
    session_id: str | None,
    turn_id: str | None,
    agent_id: str | None = None,
) -> str | None:
    if not session_id or not turn_id:
        return None
    identity = agent_id or session_id
    return f"codex-lifecycle:{session_id}:{identity}:{turn_id}:{hook}"


def event_text(event: dict[str, object], *keys: str, limit: int) -> str | None:
    for key in keys:
        value = clean_text(event.get(key), limit)
        if value:
            return value
    return None


def resolve_thread_name(thread_id: str | None) -> str | None:
    if not thread_id:
        return None
    index_path = codex_home() / "session_index.jsonl"
    try:
        with index_path.open("rb") as handle:
            handle.seek(0, os.SEEK_END)
            size = handle.tell()
            start = max(0, size - SESSION_INDEX_READ_LIMIT)
            handle.seek(start)
            raw = handle.read(SESSION_INDEX_READ_LIMIT)
    except OSError:
        return None

    if start:
        newline = raw.find(b"\n")
        raw = raw[newline + 1 :] if newline >= 0 else b""

    latest: str | None = None
    for line in raw.decode("utf-8", errors="replace").splitlines():
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(row, dict) or row.get("id") != thread_id:
            continue
        title = clean_title(row.get("thread_name"))
        if title:
            latest = title
    return latest


def safe_thread_id(thread_id: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", thread_id).strip(".-")
    digest = hashlib.sha256(thread_id.encode("utf-8")).hexdigest()[:12]
    return f"{(safe or 'thread')[:140]}-{digest}"


def title_binding_path(project_root: Path, thread_id: str) -> Path:
    return project_root / ".farplane" / "state" / "thread-title-bindings" / f"{safe_thread_id(thread_id)}.json"


def read_title_binding(project_root: Path, thread_id: str) -> dict[str, str] | None:
    path = title_binding_path(project_root, thread_id)
    try:
        row = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(row, dict) or row.get("threadId") != thread_id:
        return None
    ticket_id = clean_text(row.get("ticketId"), 16)
    ticket_title = clean_title(row.get("ticketTitle"))
    ticket_display_title = clean_title(row.get("ticketDisplayTitle"))
    if not ticket_id or not TICKET_ID_PATTERN.fullmatch(ticket_id) or not ticket_title or not ticket_display_title:
        return None
    return {
        "ticketId": ticket_id,
        "ticketTitle": ticket_title,
        "ticketDisplayTitle": ticket_display_title,
    }


def write_title_binding(project_root: Path, thread_id: str, binding: dict[str, str]) -> bool:
    path = title_binding_path(project_root, thread_id)
    row = {
        "version": 1,
        "threadId": thread_id,
        "ticketId": binding["ticketId"],
        "ticketPath": binding["ticketPath"],
        "ticketTitle": binding["ticketTitle"],
        "ticketDisplayTitle": binding["ticketDisplayTitle"],
        "observedAt": now_iso(),
        "source": "codex-user-prompt",
    }
    temporary_path: Path | None = None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            json.dump(row, handle, indent=2, sort_keys=True)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
            temporary_path = Path(handle.name)
        os.replace(temporary_path, path)
        return True
    except OSError:
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass
        return False


def ticket_title(ticket_path: Path, ticket_id: str) -> str | None:
    try:
        text = ticket_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if text.startswith("---\n"):
        parts = text.split("\n---\n", 1)
        if len(parts) == 2:
            for line in parts[0][4:].splitlines():
                if line.startswith("title:"):
                    raw = line.split(":", 1)[1].strip()
                    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in {'"', "'"}:
                        raw = raw[1:-1]
                    title = clean_title(raw)
                    if title:
                        return title
    heading = re.search(rf"^#\s+{re.escape(ticket_id)}\s*:\s*(.+)$", text, re.MULTILINE)
    return clean_title(heading.group(1)) if heading else None


def resolve_ticket_title_binding(
    event: dict[str, object],
    project_root: Path | None,
    thread_id: str | None,
) -> dict[str, str] | None:
    if project_root is None or not thread_id:
        return None
    current_hook = hook_type(event)
    if current_hook != "UserPromptSubmit":
        return read_title_binding(project_root, thread_id)

    prompt = event.get("prompt")
    if not isinstance(prompt, str):
        return read_title_binding(project_root, thread_id)
    ticket_ids = list(dict.fromkeys(TICKET_ID_PATTERN.findall(prompt)))
    if not ticket_ids:
        return read_title_binding(project_root, thread_id)
    if len(ticket_ids) != 1:
        return None

    ticket_id = ticket_ids[0]
    active = project_root / "tickets" / ticket_id / "ticket.md"
    archived = project_root / "tickets" / "archive" / ticket_id / "ticket.md"
    candidates = [path for path in (active, archived) if path.is_file()]
    if len(candidates) != 1:
        return None
    ticket_path = candidates[0]
    resolved_root = project_root.resolve()
    resolved_ticket_root = (resolved_root / "tickets").resolve()
    try:
        resolved_ticket = ticket_path.resolve(strict=True)
        resolved_ticket.relative_to(resolved_ticket_root)
        relative_path = resolved_ticket.relative_to(resolved_root)
    except (OSError, ValueError):
        return None
    resolved_title = ticket_title(ticket_path, ticket_id)
    if not resolved_title:
        return None
    display_title = clean_title(f"[{ticket_id}] {resolved_title}")
    if not display_title:
        return None
    binding = {
        "ticketId": ticket_id,
        "ticketPath": relative_path.as_posix(),
        "ticketTitle": resolved_title,
        "ticketDisplayTitle": display_title,
    }
    if not write_title_binding(project_root, thread_id, binding):
        return None
    return {key: binding[key] for key in ("ticketId", "ticketTitle", "ticketDisplayTitle")}


def runtime_classification() -> tuple[str | None, str | None]:
    return (
        clean_text(os.getenv("FARPLANE_CODEX_RUNTIME_KIND"), 80),
        clean_text(os.getenv("FARPLANE_CODEX_RUNTIME_PURPOSE"), 80),
    )


def should_skip_telemetry() -> bool:
    runtime_kind, runtime_purpose = runtime_classification()
    return (runtime_purpose or "").lower() == "eval" or (
        (runtime_kind or "").lower() == "ephemeral"
        and (runtime_purpose or "").lower() in {"eval", "judge", "baseline"}
    )


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

    machine_id = clean_text(socket.gethostname(), 120)
    machine_name = clean_text(os.getenv("AIKAGE_MACHINE_NAME"), 120) or machine_id
    project_name, project_directory = get_project_metadata(event)

    current_hook_type = hook_type(event)
    event_type = event_type_for_hook(current_hook_type)
    session_id = clean_text(event.get("session_id"), 120)
    turn_id = clean_text(event.get("turn_id"), 120)
    agent_id = event_text(event, "agent_id", "agentId", limit=160)
    agent_type = event_text(event, "agent_type", "agentType", limit=120)
    thread_title = clean_title(event_text(
        event,
        "thread_title",
        "threadTitle",
        "display_title",
        "displayTitle",
        "title",
        limit=TITLE_LIMIT,
    ))
    runtime_kind, runtime_purpose = runtime_classification()
    project_id = project_id_from_directory(project_directory)
    is_subagent = current_hook_type in {"SubagentStart", "SubagentStop"}
    thread_id = agent_id if is_subagent and agent_id else session_id
    event_cwd = event.get("cwd") or event.get("current_working_directory") or project_directory
    project_root = None if is_subagent else find_project_root(event_cwd)
    native_thread_title = None if is_subagent else resolve_thread_name(session_id)
    ticket_binding = None if is_subagent else resolve_ticket_title_binding(event, project_root, session_id)
    title_source = (
        "native"
        if native_thread_title
        else "ticket"
        if ticket_binding
        else "hook"
        if thread_title
        else None
    )

    return {
        "hookName": "farplane-console-ping",
        "hookType": current_hook_type,
        "projectId": project_id,
        "sessionId": session_id,
        "eventKey": event_key_for_hook(current_hook_type, session_id, turn_id, agent_id),
        "payload": {
            "eventType": event_type,
            "source": source_for_hook(current_hook_type),
            "activeAgentCount": max(active_agents, 1),
            "agentName": clean_text(os.getenv("AIKAGE_AGENT_NAME", "codex"), 80),
            "agentId": agent_id,
            "agentType": agent_type,
            "threadId": thread_id,
            "parentThreadId": session_id if is_subagent else None,
            "threadTitle": thread_title,
            "nativeThreadTitle": native_thread_title,
            "ticketId": ticket_binding.get("ticketId") if ticket_binding else None,
            "ticketTitle": ticket_binding.get("ticketTitle") if ticket_binding else None,
            "ticketDisplayTitle": ticket_binding.get("ticketDisplayTitle") if ticket_binding else None,
            "titleSource": title_source,
            "runtimeKind": runtime_kind,
            "runtimePurpose": runtime_purpose,
            "isEphemeral": True if is_subagent else (runtime_kind or "").lower() == "ephemeral",
            "workflowName": clean_text(os.getenv("AIKAGE_WORKFLOW_NAME"), 120),
            "machineId": machine_id,
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
    if should_skip_telemetry():
        return 0

    body = build_ping(event)
    endpoint = telemetry_endpoint()
    if endpoint is None:
        return 0

    headers = {"content-type": "application/json"}
    token = clean_text(read_config_value("FARPLANE_TELEMETRY_TOKEN"), 500)
    if token:
        headers["x-farplane-telemetry-token"] = token

    request = urllib.request.Request(
        endpoint,
        data=json.dumps(body).encode("utf-8"),
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
