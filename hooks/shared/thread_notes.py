"""Thread notes: each thread's own scope file, read by the Stop hook.

A thread keeps `~/.farplane/memory/notes/<session-id>.md` itself (the global
contract tells it how; Claude Code exposes the id as $CLAUDE_CODE_SESSION_ID).
A `parent: <session-id>` line links a sub-thread to the thread that started it.
The Stop hook only reads: the thread's notes and its parent's, bounded. The
prompt hook names the path once, on a thread's first prompt. Nothing is fetched
and no model runs here.
"""
from __future__ import annotations

from pathlib import Path
import re

NOTES_DIR = Path.home() / ".farplane" / "memory" / "notes"
MAX_OWN = 4000
MAX_PARENT = 2000
SESSION_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{7,}")
PARENT = re.compile(r"(?im)^\W*parent\W*:?\s*`?([A-Za-z0-9][A-Za-z0-9._-]{7,})")
REMINDER = (
    "Farplane thread notes for this thread: {path}. If this message gives you a ticket "
    "or task scope, write it there first as a Task section (In scope, Out of scope, "
    "Done when, Design). If In scope, Done when or a design link is missing, ask the "
    "user once and wait instead of building. A link shared only for reference goes under "
    "References. Keep Decisions, Progress and V2 candidates there as you work."
)
SCOPE_RULE = ("Work only inside your notes' Task (and your parent's) until its Done when "
              "checks pass. List ideas outside it in your answer and notes as v2 "
              "candidates; do not build them.")


def first_prompt_reminder(session_id: str) -> str:
    """The notes path and rule, once per thread, before the thread has notes."""
    path = notes_path(session_id)
    if path is None or path.exists():
        return ""
    marker = NOTES_DIR / ".reminded" / path.stem
    if marker.exists():
        return ""
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.touch()
    return REMINDER.format(path=path)


def notes_path(session_id: str) -> Path | None:
    session_id = session_id.strip()
    return NOTES_DIR / f"{session_id}.md" if SESSION_ID.fullmatch(session_id) else None


def read(session_id: str, limit: int) -> str | None:
    path = notes_path(session_id)
    if path is None or not path.is_file():
        return None
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    return text[:limit] or None


def parent_id(notes: str) -> str | None:
    found = PARENT.search(notes)
    return found.group(1) if found else None


def load(session_id: str) -> tuple[str | None, str | None]:
    """This thread's notes and its parent's (one level), either possibly None."""
    own = read(session_id, MAX_OWN)
    parent = parent_id(own) if own else None
    if not parent or parent == session_id.strip():
        return own, None
    return own, read(parent, MAX_PARENT)
