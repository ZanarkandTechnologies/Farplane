"""Thread notes: each thread's own scope file, read by the Stop hook.

A thread keeps `~/.farplane/memory/notes/<session-id>.md` itself (the global
contract tells it how; Claude Code exposes the id as $CLAUDE_CODE_SESSION_ID).
A `parent: <session-id>` line links a sub-thread to the thread that started it;
the parent may also be named by its desktop app id (`local_...`), which the
prompt hook maps to the session id under `notes/.desktop/`.
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


def remember_desktop_id(session_id: str, desktop_id: str) -> None:
    """Map the desktop app's id for this thread to its session id, for parent links."""
    if notes_path(session_id) is None or not SESSION_ID.fullmatch(desktop_id or ""):
        return
    alias = NOTES_DIR / ".desktop" / desktop_id
    if alias.is_file() and alias.read_text(encoding="utf-8").strip() == session_id.strip():
        return
    alias.parent.mkdir(parents=True, exist_ok=True)
    alias.write_text(session_id.strip() + "\n", encoding="utf-8")


def resolve(parent: str) -> str:
    """A parent named by its desktop id becomes its session id when known."""
    alias = NOTES_DIR / ".desktop" / parent
    if parent.startswith("local_") and alias.is_file():
        return alias.read_text(encoding="utf-8").strip()
    return parent


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
    parent = resolve(parent_id(own)) if own and parent_id(own) else None
    if not parent or parent == session_id.strip():
        return own, None
    return own, read(parent, MAX_PARENT)
