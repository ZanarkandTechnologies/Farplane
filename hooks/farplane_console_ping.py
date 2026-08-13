#!/usr/bin/env python3
"""Send Codex lifecycle hook pings to the Farplane UI Convex telemetry ingress."""

from __future__ import annotations

import json
import os
import re
import socket
import sys
import tempfile
import time
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
THREAD_ID_LIMIT = 160
TICKET_THREAD_LOCK_WAIT_SECONDS = 4.0
TICKET_THREAD_LOCK_STALE_SECONDS = 60.0
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


def decode_frontmatter_scalar(value: str) -> str:
    raw = value.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] == '"':
        try:
            decoded = json.loads(raw)
        except json.JSONDecodeError:
            return ""
        return decoded if isinstance(decoded, str) else ""
    if len(raw) >= 2 and raw[0] == raw[-1] == "'":
        return raw[1:-1]
    return raw


def ticket_frontmatter_lines(text: str) -> tuple[list[str], str] | None:
    if not text.startswith("---\n"):
        return None
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return None
    return parts[0][4:].splitlines(), parts[1]


def ticket_scalar(lines: list[str], key: str) -> str:
    prefix = f"{key}:"
    for line in lines:
        if line.startswith(prefix):
            return decode_frontmatter_scalar(line[len(prefix) :])
    return ""


def ticket_thread_id(ticket_path: Path) -> str:
    try:
        parsed = ticket_frontmatter_lines(ticket_path.read_text(encoding="utf-8", errors="replace"))
    except OSError:
        return ""
    if parsed is None:
        return ""
    thread_id = ticket_scalar(parsed[0], "thread_id").strip()
    if not thread_id or len(thread_id) > THREAD_ID_LIMIT or any(ord(char) < 32 for char in thread_id):
        return ""
    return thread_id


def ticket_paths(project_root: Path) -> list[Path]:
    active = project_root / "tickets"
    archived = active / "archive"
    return sorted({*active.glob("TASK-*/ticket.md"), *archived.glob("TASK-*/ticket.md")})


def ticket_paths_for_id(project_root: Path, ticket_id: str) -> list[Path]:
    active = project_root / "tickets" / ticket_id / "ticket.md"
    archived = project_root / "tickets" / "archive" / ticket_id / "ticket.md"
    return [path for path in (active, archived) if path.is_file()]


def ticket_binding(ticket_path: Path, ticket_id: str) -> dict[str, str] | None:
    title = ticket_title(ticket_path, ticket_id)
    display_title = clean_title(f"[{ticket_id}] {title}") if title else None
    if not title or not display_title:
        return None
    return {
        "ticketId": ticket_id,
        "ticketTitle": title,
        "ticketDisplayTitle": display_title,
    }


def ticket_thread_lock_path(project_root: Path, ticket_path: Path) -> Path:
    return (
        project_root
        / ".farplane"
        / "state"
        / "ticket-thread-locks"
        / f"{ticket_path.parent.name}.lock"
    )


def acquire_ticket_thread_lock(lock_path: Path) -> bool:
    """Acquire the lock directory shared by Python hooks and Node ticket writers."""
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + TICKET_THREAD_LOCK_WAIT_SECONDS
    while True:
        try:
            lock_path.mkdir()
            return True
        except FileExistsError:
            try:
                age_seconds = time.time() - lock_path.stat().st_mtime
            except OSError:
                continue
            if age_seconds > TICKET_THREAD_LOCK_STALE_SECONDS:
                try:
                    lock_path.rmdir()
                except OSError:
                    pass
                continue
            if time.monotonic() >= deadline:
                return False
            time.sleep(0.025)
        except OSError:
            return False


def release_ticket_thread_lock(lock_path: Path) -> None:
    try:
        lock_path.rmdir()
    except OSError:
        pass


def write_ticket_thread_id(project_root: Path, ticket_path: Path, thread_id: str) -> str:
    """Bind an unclaimed ticket to one root Codex thread without overwriting it."""
    if not thread_id or len(thread_id) > THREAD_ID_LIMIT or any(ord(char) < 32 for char in thread_id):
        return "invalid"
    temporary_path: Path | None = None
    lock_path = ticket_thread_lock_path(project_root, ticket_path)
    lock_acquired = False
    try:
        lock_acquired = acquire_ticket_thread_lock(lock_path)
        if not lock_acquired:
            return "error"
        text = ticket_path.read_text(encoding="utf-8")
        parsed = ticket_frontmatter_lines(text)
        if parsed is None:
            return "invalid"
        lines, body = parsed
        current = ticket_scalar(lines, "thread_id").strip()
        if current:
            return "same" if current == thread_id else "conflict"
        insert_at = next(
            (index + 1 for index, line in enumerate(lines) if line.startswith("ticket_id:")),
            len(lines),
        )
        lines.insert(insert_at, f"thread_id: {json.dumps(thread_id)}")
        frontmatter = "\n".join(lines)
        updated = f"---\n{frontmatter}\n---\n{body}"
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=ticket_path.parent,
            prefix=f".{ticket_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            handle.write(updated)
            handle.flush()
            os.fsync(handle.fileno())
            temporary_path = Path(handle.name)
        os.replace(temporary_path, ticket_path)
        return "bound"
    except OSError:
        return "error"
    finally:
        if lock_acquired:
            release_ticket_thread_lock(lock_path)
        if temporary_path is not None and temporary_path.exists():
            try:
                temporary_path.unlink()
            except OSError:
                pass


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


def resolve_ticket_thread_binding(
    event: dict[str, object],
    project_root: Path | None,
    thread_id: str | None,
) -> dict[str, str] | None:
    if project_root is None or not thread_id:
        return None

    matching_paths = [path for path in ticket_paths(project_root) if ticket_thread_id(path) == thread_id]
    if len(matching_paths) == 1:
        ticket_id = matching_paths[0].parent.name
        return ticket_binding(matching_paths[0], ticket_id)
    if len(matching_paths) > 1:
        print(
            f"farplane: thread {thread_id} is bound to multiple tickets; lifecycle ticket context omitted",
            file=sys.stderr,
        )
        return None

    current_hook = hook_type(event)
    if current_hook != "UserPromptSubmit":
        return None

    prompt = event.get("prompt")
    if not isinstance(prompt, str):
        return None
    ticket_ids = list(dict.fromkeys(TICKET_ID_PATTERN.findall(prompt)))
    if not ticket_ids:
        return None
    if len(ticket_ids) != 1:
        return None

    ticket_id = ticket_ids[0]
    candidates = ticket_paths_for_id(project_root, ticket_id)
    if len(candidates) != 1:
        return None
    ticket_path = candidates[0]
    if ticket_path.parent.parent.name == "archive":
        return None
    result = write_ticket_thread_id(project_root, ticket_path, thread_id)
    if result == "conflict":
        print(
            f"farplane: {ticket_id} already owns a different task thread; lifecycle ticket context omitted",
            file=sys.stderr,
        )
        return None
    if result not in {"bound", "same"}:
        return None
    return ticket_binding(ticket_path, ticket_id)


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
    ticket_binding = None if is_subagent else resolve_ticket_thread_binding(event, project_root, session_id)
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
