#!/usr/bin/env python3
"""Core-owned typed file-event capture with durable local delivery state.

Inputs are Codex PostToolUse payloads and project files. Outputs are sanitized
event records, a durable outbox entry, and the next parser snapshot. The event
record is always durable before the snapshot advances.
"""

from __future__ import annotations

import fnmatch
import hashlib
import json
import os
import re
import shlex
import tempfile
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import yaml


SCHEMA_VERSION = 1
WRITE_TOOL_RE = re.compile(r"(?:bash|apply_patch|edit|write|multiedit|filesystem.*(?:write|edit))", re.I)
PATCH_PATH_RE = re.compile(r"^\*\*\* (?:Add|Update|Delete) File: (.+)$", re.M)
TICKET_PATH_RE = re.compile(r"^tickets/(TASK-[A-Za-z0-9_-]+)/ticket\.md$", re.I)
TICKET_PROGRAM_RE = re.compile(r"^tickets/(TASK-[A-Za-z0-9_-]+)/(program|progress)\.md$", re.I)
TERMINAL_VALUES = {"done", "complete", "completed", "closed"}
SENSITIVE_FIELD_RE = re.compile(r"(?:api[_-]?key|token|secret|password|credential|private[_-]?key)", re.I)
SAFE_PREVIEW_FIELDS = {"status", "phase", "next_action", "priority", "human_gate"}
DEFAULT_PATTERNS = (
    "tickets/TASK-*/ticket.md",
    "tickets/TASK-*/program.md",
    "tickets/TASK-*/progress.md",
    "farplane/*.yaml",
    "farplane/*.yml",
    "farplane/*.json",
    "docs/MEMORY.md",
    "docs/LESSONS.md",
    "docs/TROUBLES.md",
    "docs/HISTORY.md",
)
DEFAULT_EVENTS = (
    "farplane.ticket.completed",
    "farplane.ticket.changed",
    "farplane.ticket.program.changed",
    "farplane.ticket.progress.changed",
    "farplane.config.changed",
    "farplane.memory.changed",
    "farplane.learning.changed",
    "farplane.history.changed",
)


class FileEventError(RuntimeError):
    """Raised when a file-event contract cannot be safely processed."""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_json(value: Any) -> str:
    def encode_yaml_scalar(item: Any) -> str:
        if isinstance(item, (datetime, date)):
            return item.isoformat()
        raise TypeError(f"Object of type {item.__class__.__name__} is not JSON serializable")

    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=encode_yaml_scalar,
    )


def sha256_value(value: Any) -> str:
    text = value if isinstance(value, str) else canonical_json(value)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def atomic_write_json(path: Path, payload: Any) -> None:
    """Atomically replace one JSON file and fsync the containing directory."""

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, raw_tmp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    tmp = Path(raw_tmp)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if tmp.exists():
            tmp.unlink()


def create_json_exclusive(path: Path, payload: Any) -> bool:
    """Create one immutable JSON record, returning False when it already exists."""

    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, raw_tmp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    tmp = Path(raw_tmp)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(tmp, path)
        except FileExistsError:
            return False
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
        return True
    finally:
        tmp.unlink(missing_ok=True)


def read_json(path: Path, fallback: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return fallback


def find_project_root(start: str | Path) -> Path:
    current = Path(start).expanduser().resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / "farplane").is_dir() or (candidate / ".git").exists():
            return candidate
    return current


def project_id(project_root: Path) -> str:
    bindings = project_root / "farplane" / "bindings.yaml"
    try:
        payload = yaml.safe_load(bindings.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        payload = {}
    project = payload.get("project") if isinstance(payload, dict) else None
    value = project.get("id") if isinstance(project, dict) else None
    if isinstance(value, str) and value.strip():
        return value.strip()
    return "local-" + re.sub(r"[^a-z0-9]+", "-", project_root.name.lower()).strip("-")


def hook_policy(project_root: Path) -> dict[str, Any]:
    path = project_root / "farplane" / "hooks.json"
    payload = read_json(path, {})
    file_events = payload.get("file_events") if isinstance(payload, dict) else None
    config = file_events if isinstance(file_events, dict) else {}
    patterns = config.get("patterns")
    events = config.get("events")
    return {
        "enabled": config.get("enabled", True) is not False,
        "patterns": tuple(str(row) for row in patterns if str(row).strip())
        if isinstance(patterns, list)
        else DEFAULT_PATTERNS,
        "events": tuple(str(row) for row in events if str(row).strip())
        if isinstance(events, list)
        else DEFAULT_EVENTS,
    }


def _payload_record(payload: dict[str, Any], *keys: str) -> dict[str, Any]:
    for key in keys:
        value = payload.get(key)
        if isinstance(value, dict):
            return value
    return {}


def _payload_text(payload: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _candidate_strings(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, child in value.items():
            if key.lower() in {
                "path",
                "file",
                "file_path",
                "filepath",
                "target",
                "target_file",
                "command",
                "cmd",
                "patch",
            }:
                yield from _candidate_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from _candidate_strings(child)


def _paths_from_command(command: str) -> Iterable[str]:
    try:
        tokens = shlex.split(command)
    except ValueError:
        tokens = command.split()
    for token in tokens:
        cleaned = token.strip("'\";,()")
        if cleaned.startswith(("tickets/", "farplane/", "docs/")):
            yield cleaned


def candidate_paths(payload: dict[str, Any], project_root: Path) -> list[str]:
    project_root = project_root.resolve()
    tool_input = _payload_record(payload, "tool_input", "toolInput", "input")
    candidates: set[str] = set()
    for value in _candidate_strings(tool_input):
        candidates.update(match.strip() for match in PATCH_PATH_RE.findall(value))
        if "\n" not in value:
            candidates.add(value)
        if any(marker in value for marker in ("tickets/", "farplane/", "docs/")):
            candidates.update(_paths_from_command(value))

    normalized: set[str] = set()
    for raw in candidates:
        raw = raw.strip().replace("\\", "/").removeprefix("./")
        if not raw or raw.startswith("-"):
            continue
        path = Path(raw).expanduser()
        absolute = path.resolve() if path.is_absolute() else (project_root / path).resolve()
        try:
            relative = absolute.relative_to(project_root).as_posix()
        except ValueError:
            continue
        normalized.add(relative)
    return sorted(normalized)


def _frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---"):
        return {}
    match = re.match(r"^---\s*\n(.*?)\n---(?:\s*\n|$)", text, flags=re.S)
    if not match:
        return {}
    try:
        payload = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _terminal(frontmatter: dict[str, Any]) -> bool:
    values = {
        str(frontmatter.get("status") or "").strip().lower(),
        str(frontmatter.get("phase") or "").strip().lower(),
    }
    return bool(values & TERMINAL_VALUES) or str(frontmatter.get("next_action") or "").strip().lower() == "done"


def _file_contract(relative_path: str, text: str) -> dict[str, Any] | None:
    ticket = TICKET_PATH_RE.match(relative_path)
    if ticket:
        frontmatter = _frontmatter(text)
        return {
            "kind": "ticket",
            "entity_ref": {"kind": "ticket", "id": ticket.group(1).upper(), "path": relative_path},
            "frontmatter": frontmatter,
            "terminal": _terminal(frontmatter),
            "changed_event": "farplane.ticket.changed",
        }
    packet = TICKET_PROGRAM_RE.match(relative_path)
    if packet:
        part = packet.group(2).lower()
        return {
            "kind": f"ticket_{part}",
            "entity_ref": {"kind": "ticket", "id": packet.group(1).upper(), "path": relative_path},
            "frontmatter": _frontmatter(text),
            "terminal": None,
            "changed_event": f"farplane.ticket.{part}.changed",
        }
    if relative_path.startswith("farplane/"):
        return {
            "kind": "config",
            "entity_ref": {"kind": "config", "id": relative_path, "path": relative_path},
            "frontmatter": {},
            "terminal": None,
            "changed_event": "farplane.config.changed",
        }
    doc_events = {
        "docs/MEMORY.md": "farplane.memory.changed",
        "docs/LESSONS.md": "farplane.learning.changed",
        "docs/TROUBLES.md": "farplane.learning.changed",
        "docs/HISTORY.md": "farplane.history.changed",
    }
    if relative_path in doc_events:
        return {
            "kind": "doc",
            "entity_ref": {"kind": "doc", "id": relative_path, "path": relative_path},
            "frontmatter": {},
            "terminal": None,
            "changed_event": doc_events[relative_path],
        }
    return None


def _field_preview(key: str, value: Any) -> dict[str, str]:
    raw = canonical_json(value)
    preview = (
        re.sub(r"\s+", " ", str(value)).strip()[:120]
        if key in SAFE_PREVIEW_FIELDS and not SENSITIVE_FIELD_RE.search(key)
        else "[redacted]"
    )
    return {"hash": sha256_value(raw), "preview": preview}


def _field_state(key: str, value: Any) -> dict[str, str]:
    if (
        isinstance(value, dict)
        and isinstance(value.get("hash"), str)
        and isinstance(value.get("preview"), str)
        and set(value) == {"hash", "preview"}
    ):
        return {"hash": value["hash"], "preview": value["preview"]}
    return _field_preview(key, value)


def _frontmatter_state(frontmatter: dict[str, Any]) -> dict[str, dict[str, str]]:
    return {str(key): _field_preview(str(key), value) for key, value in sorted(frontmatter.items())}


def _privacy_safe_delta(previous: dict[str, Any], current: dict[str, Any]) -> dict[str, Any]:
    before = previous.get("frontmatter") if isinstance(previous.get("frontmatter"), dict) else {}
    after = current.get("frontmatter") if isinstance(current.get("frontmatter"), dict) else {}
    changed = []
    for key in sorted(set(before) | set(after)):
        before_state = _field_state(key, before[key]) if key in before else None
        after_state = _field_state(key, after[key]) if key in after else None
        if before_state and after_state and before_state["hash"] == after_state["hash"]:
            continue
        changed.append(
            {
                "path": key,
                "before": before_state,
                "after": after_state,
            }
        )
    return {"changed_fields": changed[:12]}


def snapshot_path(project_root: Path, relative_path: str) -> Path:
    key = sha256_value(relative_path)[:24]
    return project_root / ".farplane" / "file-events" / "state" / f"{key}.json"


def event_record_path(project_root: Path, event_id: str) -> Path:
    return project_root / ".farplane" / "events" / "records" / f"{event_id}.json"


def outbox_path(project_root: Path, event_id: str) -> Path:
    return project_root / ".farplane" / "events" / "outbox" / f"{event_id}.json"


def hook_error_path(project_root: Path, error_id: str) -> Path:
    return project_root / ".farplane" / "hooks" / "errors" / f"{error_id}.json"


def record_hook_error(
    project_root: Path,
    *,
    hook_name: str,
    error: object,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Write a bounded local hook error receipt without failing the hook."""

    root = project_root.resolve()
    occurred_at = now_iso()
    payload_keys = sorted(str(key) for key in payload.keys())[:40] if isinstance(payload, dict) else []
    receipt = {
        "schema_version": SCHEMA_VERSION,
        "hook_name": str(hook_name or "unknown")[:120],
        "error": str(error)[:500],
        "payload_keys": payload_keys,
        "occurred_at": occurred_at,
    }
    error_id = sha256_value(receipt)
    receipt["error_id"] = error_id
    path = hook_error_path(root, error_id)
    create_json_exclusive(path, receipt)
    receipt["path"] = str(path)
    return receipt


def capture_file(project_root: Path, relative_path: str, *, payload: dict[str, Any], event_at: str | None = None) -> dict[str, Any] | None:
    """Capture one tracked file, durably enqueueing its event before snapshot advancement."""

    project_root = project_root.resolve()
    policy = hook_policy(project_root)
    if not policy["enabled"] or not any(fnmatch.fnmatch(relative_path, pattern) for pattern in policy["patterns"]):
        return None
    absolute = (project_root / relative_path).resolve()
    try:
        absolute.relative_to(project_root)
    except ValueError as exc:
        raise FileEventError(f"unsafe_file_path:{relative_path}") from exc
    if not absolute.is_file():
        return None
    text = absolute.read_text(encoding="utf-8", errors="replace")
    contract = _file_contract(relative_path, text)
    if not contract:
        return None

    current_hash = sha256_value(text)
    state_path = snapshot_path(project_root, relative_path)
    previous = read_json(state_path, {})
    if not isinstance(previous, dict):
        previous = {}
    if previous.get("content_hash") == current_hash:
        return None

    previous_terminal = previous.get("terminal") if isinstance(previous.get("terminal"), bool) else None
    current_terminal = contract["terminal"]
    completed = contract["kind"] == "ticket" and current_terminal is True and previous_terminal is not True
    event_name = "farplane.ticket.completed" if completed else contract["changed_event"]
    if event_name not in policy["events"]:
        snapshot = {
            "schema_version": SCHEMA_VERSION,
            "path": relative_path,
            "kind": contract["kind"],
            "content_hash": current_hash,
            "frontmatter": _frontmatter_state(contract["frontmatter"]),
            "terminal": current_terminal,
            "updated_at": event_at or now_iso(),
        }
        atomic_write_json(state_path, snapshot)
        return None

    entity_ref = contract["entity_ref"]
    identity = {
        "project_id": project_id(project_root),
        "event_name": event_name,
        "entity_ref": entity_ref,
        "previous_hash": previous.get("content_hash"),
        "content_hash": current_hash,
    }
    event_id = sha256_value(identity)
    session_id = _payload_text(payload, "session_id", "sessionId")
    thread_id = _payload_text(payload, "thread_id", "threadId") or session_id
    event = {
        "schema_version": SCHEMA_VERSION,
        "event_id": event_id,
        "event_key": f"farplane-file-event:{event_id}",
        "event_name": event_name,
        "project_id": identity["project_id"],
        "entity_ref": entity_ref,
        "previous_hash": previous.get("content_hash"),
        "content_hash": current_hash,
        "terminal": current_terminal,
        "event_at": event_at or now_iso(),
        "privacy_safe_delta": _privacy_safe_delta(previous, contract),
        "provenance": {"source": "codex_post_tool_use", "session_id": session_id, "thread_id": thread_id},
    }
    record = event_record_path(project_root, event_id)
    created = create_json_exclusive(record, event)
    if not created:
        existing = read_json(record, {})
        semantic_fields = (
            "schema_version",
            "event_id",
            "event_key",
            "event_name",
            "project_id",
            "entity_ref",
            "previous_hash",
            "content_hash",
            "terminal",
            "privacy_safe_delta",
        )
        if not isinstance(existing, dict) or any(existing.get(key) != event.get(key) for key in semantic_fields):
            raise FileEventError(f"event_identity_collision:{event_id}")
        # Identity deliberately excludes retry-time provenance. Once one
        # immutable record exists, retries redeliver that canonical record.
        event = existing
    create_json_exclusive(outbox_path(project_root, event_id), event)

    snapshot = {
        "schema_version": SCHEMA_VERSION,
        "path": relative_path,
        "kind": contract["kind"],
        "content_hash": current_hash,
        "frontmatter": _frontmatter_state(contract["frontmatter"]),
        "terminal": current_terminal,
        "updated_at": event["event_at"],
        "last_event_id": event_id,
    }
    atomic_write_json(state_path, snapshot)
    return event


def capture_payload(payload: dict[str, Any], *, project_root: Path | None = None) -> list[dict[str, Any]]:
    """Capture all tracked paths named by one Codex PostToolUse payload."""

    event_name = _payload_text(payload, "hook_event_name", "hookType", "event") or ""
    tool_name = _payload_text(payload, "tool_name", "toolName", "tool") or ""
    if event_name and not re.search(r"post.*tool.*use", event_name, re.I):
        return []
    if tool_name and not WRITE_TOOL_RE.search(tool_name):
        return []
    root = (project_root or find_project_root(_payload_text(payload, "cwd", "project_path", "projectPath") or os.getcwd())).resolve()
    occurred_at = _payload_text(payload, "event_at", "eventAt", "occurred_at", "occurredAt")
    events = []
    for relative_path in candidate_paths(payload, root):
        event = capture_file(root, relative_path, payload=payload, event_at=occurred_at)
        if event:
            events.append(event)
    return events


def pending_events(project_root: Path) -> list[dict[str, Any]]:
    root = project_root / ".farplane" / "events" / "outbox"
    if not root.exists():
        return []
    events = []
    for path in sorted(root.glob("*.json")):
        payload = read_json(path, None)
        if isinstance(payload, dict) and payload.get("event_id"):
            events.append(payload)
    return events


def acknowledge_event(project_root: Path, event_id: str) -> None:
    outbox_path(project_root, event_id).unlink(missing_ok=True)
