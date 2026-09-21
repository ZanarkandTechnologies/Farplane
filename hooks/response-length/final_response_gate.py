#!/usr/bin/env python3
"""Codex Stop-hook gate for bounded user-facing responses.

The gate never edits or truncates text. It asks Codex to continue the turn and
rewrite an over-limit final response so semantic ownership stays with the model
and, for material work, the reviewer lane.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import sys
from typing import Any

CORE_DIR = Path(__file__).resolve().parents[2] / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from farplane_response import (  # noqa: E402
    DEFAULT_MAX_PROSE_LINES,
    DEFAULT_MAX_PROSE_WORDS,
    measure_response,
)
from runtime_config import load_runtime_env  # noqa: E402


ENV_MAX_PROSE_WORDS = "FARPLANE_FINAL_RESPONSE_MAX_PROSE_WORDS"
ENV_MAX_PROSE_LINES = "FARPLANE_FINAL_RESPONSE_MAX_PROSE_LINES"
FORMAT_MARKER = "<!-- farplane-response-length:v2 -->"


def configured_max_prose_words(env: dict[str, str] | None = None) -> int:
    source = load_runtime_env(os.environ) if env is None else env
    raw = source.get(ENV_MAX_PROSE_WORDS, str(DEFAULT_MAX_PROSE_WORDS))
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return DEFAULT_MAX_PROSE_WORDS
    return value if value > 0 else DEFAULT_MAX_PROSE_WORDS


def configured_max_prose_lines(env: dict[str, str] | None = None) -> int:
    source = load_runtime_env(os.environ) if env is None else env
    raw = source.get(ENV_MAX_PROSE_LINES, str(DEFAULT_MAX_PROSE_LINES))
    try:
        value = int(raw)
    except (TypeError, ValueError):
        return DEFAULT_MAX_PROSE_LINES
    return value if value > 0 else DEFAULT_MAX_PROSE_LINES


def legacy_gate_response(
    payload: dict[str, Any], max_prose_words: int, max_prose_lines: int
) -> dict[str, Any] | None:
    """Render the pre-heading feedback only for in-flight transcript migration."""
    message = payload.get("last_assistant_message")
    if payload.get("hook_event_name") != "Stop" or not isinstance(message, str):
        return None
    measure = measure_response(message)
    if (measure.prose_words <= max_prose_words
            and measure.prose_nonblank_lines <= max_prose_lines):
        return None
    retry_note = (
        "The previous compression attempt is still over the ceiling.\n\n"
        if payload.get("stop_hook_active")
        else ""
    )
    reason = (
        f"{retry_note}Rewrite the user-facing final answer to at most "
        f"{max_prose_words} prose words (current: {measure.prose_words}) and "
        f"at most {max_prose_lines} nonblank prose lines "
        f"(current: {measure.prose_nonblank_lines}).\n\n"
        "- Preserve only the outcome, decisive evidence, required action or blocker, "
        "verification pointers, and any safety-critical qualification.\n"
        "- Remove process narration, repeated context, generic advice, "
        "and unasked follow-up offers.\n"
        "- Prefer links to durable artifacts over copied detail.\n"
        "- Closed Mermaid and `wireframe` blocks, exact image/video embed lines, "
        "marker-only Markdown blockquote spacer lines, and a final link-only "
        "References/Citations section are outside the prose budget, but must not "
        "introduce new topic breadth.\n"
        "- Return the revised final answer only and do not mention this gate."
    )
    return {"decision": "block", "reason": reason}


def gate_response(
    payload: dict[str, Any], max_prose_words: int, max_prose_lines: int
) -> dict[str, Any] | None:
    if payload.get("hook_event_name") != "Stop":
        return None

    message = payload.get("last_assistant_message")
    if not isinstance(message, str) or not message.strip():
        return None

    measure = measure_response(message)
    words_over = measure.prose_words > max_prose_words
    lines_over = measure.prose_nonblank_lines > max_prose_lines
    if not words_over and not lines_over:
        return None

    retry_line = (
        "- **Retry:** The previous compression attempt is still over the ceiling.\n"
        if payload.get("stop_hook_active")
        else ""
    )
    reason = (
        f"#### Response length\n\n{FORMAT_MARKER}\n\n"
        f"{retry_line}"
        f"- **Limit:** Rewrite the user-facing final answer to at most "
        f"{max_prose_words} prose words (current: {measure.prose_words}) and "
        f"at most {max_prose_lines} nonblank prose lines "
        f"(current: {measure.prose_nonblank_lines}).\n"
        "- **Keep:** Preserve only the outcome, decisive evidence, required action "
        "or blocker, verification pointers, and safety-critical qualifications.\n"
        "- **Remove:** Process narration, repeated context, generic advice, and "
        "unasked follow-up offers.\n"
        "- **Prefer:** Links to durable artifacts over copied detail.\n"
        "- **Budget exclusions:** Closed Mermaid and `wireframe` blocks, exact "
        "image/video embed lines, marker-only Markdown blockquote spacer lines, "
        "and a final link-only References/Citations section are outside the prose "
        "budget, but must not introduce new topic breadth.\n"
        "- **Return:** The revised final answer only; do not mention this gate."
    )
    return {"decision": "block", "reason": reason}


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, TypeError):
        return 0
    if not isinstance(payload, dict):
        return 0

    result = gate_response(
        payload, configured_max_prose_words(), configured_max_prose_lines()
    )
    if result is not None:
        json.dump(result, sys.stdout, separators=(",", ":"))
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
