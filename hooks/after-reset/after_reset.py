#!/usr/bin/env python3
"""SessionStart hook, source compact: hands a thread its goals back after a reset.

A context reset replaces the conversation with a summary, and a summary can drop
what the user asked for. This reads the thread's notes and the user's own words
from the transcript, so nothing here depends on that summary. No model runs here.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "hooks" / "shared") not in sys.path:
    sys.path.insert(0, str(ROOT / "hooks" / "shared"))

import thread_notes

MAX_CONTEXT = 9500  # Claude Code moves hook context over 10,000 characters to a file.
MAX_MESSAGE = 240
MIN_WORDS = 4
INJECTED = re.compile(r"<(system-reminder|task-notification|pasted_content)\b.*?</\1>", re.S)
NOT_THE_USER = ("Stop hook feedback", "Base directory for this skill", "[Request interrupted",
                "Another Claude session sent a message", "<")
RULE = ("Your context was just reset, and the summary may have dropped what the user asked for. "
        "Before your next step, compare the summary with the notes and messages below. Add every "
        "ask that is neither finished nor closed by the user to the `## Open goals` section at "
        "the top of {path}, in the user's words, and tell the user about any you had dropped.")


def own_words(entry: dict[str, object]) -> str:
    """The user's text in one transcript row, or nothing for tool and harness rows."""
    if entry.get("type") != "user" or entry.get("isSidechain") or entry.get("isCompactSummary"):
        return ""
    message = entry.get("message")
    content = message.get("content") if isinstance(message, dict) else None
    if isinstance(content, list):
        content = "\n".join(str(block.get("text", "")) for block in content
                            if isinstance(block, dict) and block.get("type") == "text")
    text = INJECTED.sub("", content).strip() if isinstance(content, str) else ""
    return "" if text.startswith(NOT_THE_USER) else text


def user_messages(transcript: str) -> list[str]:
    """The user's messages, oldest first, each cut to one line."""
    found: list[str] = []
    try:
        with open(transcript, encoding="utf-8", errors="replace") as lines:
            for line in lines:
                if '"user"' not in line:
                    continue
                try:
                    text = own_words(json.loads(line))
                except json.JSONDecodeError:
                    continue
                if len(text.split()) >= MIN_WORDS:
                    found.append(" ".join(text.split())[:MAX_MESSAGE])
    except (OSError, TypeError):
        return []
    return list(dict.fromkeys(found))


def context(session_id: str, transcript: str) -> str:
    path = thread_notes.notes_path(session_id)
    if path is None:
        return ""
    notes = thread_notes.read(session_id, thread_notes.MAX_OWN)
    head = [RULE.format(path=path),
            f"Thread notes:\n{notes}" if notes else "This thread has no notes yet."]
    room = MAX_CONTEXT - sum(len(part) + 2 for part in head) - 40
    kept: list[str] = []
    for message in reversed(user_messages(transcript)):
        if room < len(message) + 3:
            break
        kept.insert(0, f"- {message}")
        room -= len(message) + 3
    if kept:
        head.append("The user's messages, oldest first:\n" + "\n".join(kept))
    return "\n\n".join(head)


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return 0
    if not isinstance(payload, dict) or payload.get("source") != "compact":
        return 0
    text = context(str(payload.get("session_id") or ""), str(payload.get("transcript_path") or ""))
    if text:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart",
                                                 "additionalContext": text}}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
