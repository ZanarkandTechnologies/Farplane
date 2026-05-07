#!/usr/bin/env python3
from __future__ import annotations

import json
import sys

from runtime_telemetry import emit_hook_telemetry
from user_turn import (
    append_conversation_user_turn,
    capture_user_turn,
    explicit_run_state_selector,
    is_internal_user_prompt,
    project_root_from_payload,
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

    captured = capture_user_turn(
        project_root=project_root,
        raw_text=prompt,
        turn_id=str(payload.get("turn_id") or "").strip() or None,
        source="user_prompt_submit_hook",
        session_id=str(payload.get("session_id") or "").strip() or None,
        explicit_run_state=explicit_run_state_selector(payload) or None,
    )
    session_id = str(payload.get("session_id") or "").strip()
    if captured is not None and session_id:
        append_conversation_user_turn(
            project_root=project_root,
            session_id=session_id,
            last_user_turn=captured,
        )
    emit_hook_telemetry(
        event_type="user_prompt_submit",
        hook_event_name="UserPromptSubmit",
        payload=payload,
        project_root=project_root,
        extra={
            "prompt_length": len(prompt),
            "source": "capture_user_turn.py",
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
