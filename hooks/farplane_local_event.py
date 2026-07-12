#!/usr/bin/env python3
"""Installed PostToolUse boundary for small Core-local hook telemetry."""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any


CORE_DIR = Path(__file__).resolve().parents[1] / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from farplane_file_events import (
    create_json_exclusive,
    find_project_root,
    record_hook_error,
    sha256_value,
)


SKILL_PATH_RE = re.compile(r"(^|[\s'\"`])((?:\.?/)?skills/([A-Za-z0-9_-]+)/SKILL\.md)($|[\s'\"`])")
THREAD_KEY_RE = re.compile(r"(?:^|_)(?:thread|session)(?:_|$)", re.I)


def _safe_text(value: object, limit: int = 240) -> str:
    if not isinstance(value, str):
        return ""
    return re.sub(r"\s+", " ", value).strip()[:limit]


def _payload_record(payload: dict[str, Any], *keys: str) -> dict[str, Any]:
    for key in keys:
        value = payload.get(key)
        if isinstance(value, dict):
            return value
    return {}


def _walk_strings(value: object) -> list[str]:
    strings: list[str] = []
    if isinstance(value, str):
        strings.append(value)
    elif isinstance(value, dict):
        for child in value.values():
            strings.extend(_walk_strings(child))
    elif isinstance(value, list):
        for child in value:
            strings.extend(_walk_strings(child))
    return strings[:80]


def _skill_events(payload: dict[str, Any], project_root: Path) -> list[dict[str, Any]]:
    tool_input = _payload_record(payload, "tool_input", "toolInput", "input")
    haystack = "\n".join(_walk_strings(tool_input))
    events = []
    for match in SKILL_PATH_RE.finditer(haystack):
        relative_path = match.group(2).removeprefix("./")
        skill_id = match.group(3)
        identity = {
            "event_name": "farplane.skill.invoked",
            "project_root": str(project_root),
            "skill_id": skill_id,
            "path": relative_path,
            "session_id": _safe_text(payload.get("session_id") or payload.get("sessionId"), 160),
            "tool_name": _safe_text(payload.get("tool_name") or payload.get("toolName") or payload.get("tool"), 120),
        }
        event_id = sha256_value(identity)
        events.append(
            {
                "schema_version": 1,
                "event_id": event_id,
                "event_key": f"farplane-skill-invoked:{event_id}",
                "event_name": "farplane.skill.invoked",
                "entity_ref": {"kind": "skill", "id": skill_id, "path": relative_path},
                "privacy_safe_delta": {},
                "provenance": {
                    "source": "codex_post_tool_use",
                    "session_id": identity["session_id"],
                    "tool_name": identity["tool_name"],
                },
            }
        )
    return events


def _thread_events(payload: dict[str, Any]) -> list[dict[str, Any]]:
    tool_name = _safe_text(payload.get("tool_name") or payload.get("toolName") or payload.get("tool"), 160)
    if not re.search(r"(?:create_thread|fork_thread|thread)", tool_name, re.I):
        return []
    tool_input = _payload_record(payload, "tool_input", "toolInput", "input")
    thread_refs = {}
    for key, value in tool_input.items():
        if THREAD_KEY_RE.search(str(key)):
            safe = _safe_text(value, 160)
            if safe:
                thread_refs[str(key)[:80]] = safe
    identity = {
        "event_name": "farplane.thread.lineage.observed",
        "tool_name": tool_name,
        "session_id": _safe_text(payload.get("session_id") or payload.get("sessionId"), 160),
        "thread_refs": thread_refs,
    }
    event_id = sha256_value(identity)
    return [
        {
            "schema_version": 1,
            "event_id": event_id,
            "event_key": f"farplane-thread-lineage:{event_id}",
            "event_name": "farplane.thread.lineage.observed",
            "entity_ref": {"kind": "codex_thread", "id": thread_refs.get("thread_id") or thread_refs.get("threadId") or event_id[:16]},
            "privacy_safe_delta": {"thread_refs": sorted(thread_refs)},
            "provenance": {"source": "codex_post_tool_use", "session_id": identity["session_id"], "tool_name": tool_name},
        }
    ]


def _append_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")


def capture_local_events(payload: dict[str, Any], project_root: Path | None = None) -> dict[str, Any]:
    root = project_root or find_project_root(str(payload.get("cwd") or payload.get("project_path") or payload.get("projectPath") or os.getcwd()))
    root = root.resolve()
    events = [*_skill_events(payload, root), *_thread_events(payload)]
    created = []
    for event in events:
        path = root / ".farplane" / "events" / "records" / f"{event['event_id']}.json"
        if create_json_exclusive(path, event):
            created.append({**event, "record_path": str(path)})
    _append_jsonl(root / ".farplane" / "events" / "hook-telemetry.jsonl", created)
    return {"ok": True, "project_root": str(root), "captured_event_ids": [row["event_id"] for row in created]}


def main() -> int:
    payload: dict[str, Any] = {}
    try:
        payload = json.load(sys.stdin)
        if not isinstance(payload, dict):
            return 0
        result = capture_local_events(payload)
        if os.getenv("FARPLANE_HOOK_EVENT_DEBUG") == "1":
            print(json.dumps(result, indent=2, sort_keys=True), file=sys.stderr)
    except Exception as exc:
        root = find_project_root(str(payload.get("cwd") or os.getcwd())) if isinstance(payload, dict) else Path.cwd()
        receipt = record_hook_error(root, hook_name="farplane_local_event.py", error=exc, payload=payload)
        print(f"farplane local event: {receipt['path']}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
