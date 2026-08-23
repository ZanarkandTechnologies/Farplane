#!/usr/bin/env python3
from __future__ import annotations

import json
import sys

from runtime_telemetry import emit_hook_telemetry
from user_turn import (
    append_conversation_user_turn,
    capture_user_turn,
    extract_control_surfaces,
    extract_skill_mentions,
    explicit_run_state_selector,
    is_internal_user_prompt,
    load_skill_registry,
    normalize_user_turn,
    project_root_from_payload,
    runtime_metadata_from_payload,
)


def read_payload() -> dict[str, object]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def main() -> int:
    payload = read_payload()
    if payload.get("hook_event_name") != "UserPromptSubmit":
        return 0

    prompt = payload.get("prompt")
    if not isinstance(prompt, str) or not prompt.strip():
        return 0
    if is_internal_user_prompt(prompt):
        return 0

    project_root = project_root_from_payload(payload)
    if project_root is None:
        return 0
    runtime = runtime_metadata_from_payload(payload, prompt)

    captured = capture_user_turn(
        project_root=project_root,
        raw_text=prompt,
        turn_id=str(payload.get("turn_id") or "").strip() or None,
        source="user_prompt_submit_hook",
        session_id=str(payload.get("session_id") or "").strip() or None,
        explicit_run_state=explicit_run_state_selector(payload) or None,
        runtime=runtime,
    )
    session_id = str(payload.get("session_id") or "").strip()
    if captured is not None and session_id:
        append_conversation_user_turn(
            project_root=project_root,
            session_id=session_id,
            last_user_turn=captured,
        )
    elif session_id:
        append_conversation_user_turn(
            project_root=project_root,
            session_id=session_id,
            last_user_turn=normalize_user_turn(
                prompt,
                turn_id=str(payload.get("turn_id") or "").strip() or None,
                source="user_prompt_submit_hook",
                runtime=runtime,
            ),
        )
    control_surfaces = extract_control_surfaces(prompt)
    skill_registry = load_skill_registry(project_root)
    skill_mentions = extract_skill_mentions(prompt, registry=skill_registry)
    registry_error_count = int(skill_registry.status != "loaded")
    emit_hook_telemetry(
        event_type="turn_start",
        hook_event_name="UserPromptSubmit",
        payload=payload,
        project_root=project_root,
        extra={
            "prompt_length": len(prompt),
            "source": "capture_user_turn.py",
            "producer": "capture_user_turn.py",
            "summary": "user turn captured",
            "registry_source": "docs/skills/registry.jsonl",
            "registry_path": str(skill_registry.path),
            "registry_status": skill_registry.status,
            "registry_error": skill_registry.error,
            "counts": {
                "prompt_length": len(prompt),
                "control_surface_count": len(control_surfaces),
                "skill_mention_count": len(skill_mentions),
                "registry_skill_count": len(skill_registry.records),
                "registry_error_count": registry_error_count,
            },
        },
    )
    for surface in control_surfaces:
        emit_hook_telemetry(
            event_type="control_surface_detected",
            hook_event_name="UserPromptSubmit",
            payload=payload,
            project_root=project_root,
            extra={
                "source": "capture_user_turn.py",
                "summary": f"detected ${surface}",
                "skill_name": surface,
                "control_surface": surface,
            },
        )
    for skill in skill_mentions:
        registry_record = skill_registry.records[skill.lower()]
        emit_hook_telemetry(
            event_type="skill_requested",
            hook_event_name="UserPromptSubmit",
            payload=payload,
            project_root=project_root,
            extra={
                "source": "user_explicit_request",
                "producer": "capture_user_turn.py",
                "status": "requested",
                "summary": f"requested ${skill}",
                "skill_name": skill,
                "registry_source": "docs/skills/registry.jsonl",
                "registry_path": str(skill_registry.path),
                "registry_skill_source": registry_record.get("source", ""),
                "registry_skill_path": registry_record.get("path", ""),
            },
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
