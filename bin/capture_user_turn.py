#!/usr/bin/env python3
from __future__ import annotations

import json
import sys

from user_turn import capture_user_turn, project_root_from_payload


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

    project_root = project_root_from_payload(payload)
    if project_root is None:
        return 0

    capture_user_turn(
        project_root=project_root,
        raw_text=prompt,
        turn_id=str(payload.get("turn_id") or "").strip() or None,
        source="user_prompt_submit_hook",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
