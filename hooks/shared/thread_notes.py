"""Thread notes: each thread's own scope file, read by the Stop hook.

A thread keeps `~/.farplane/memory/notes/<session-id>.md` itself (the global
contract tells it how; Claude Code exposes the id as $CLAUDE_CODE_SESSION_ID).
A `parent: <session-id>` line links a sub-thread to the thread that started it;
the parent may also be named by its desktop app id (`local_...`), which the
prompt hook maps to the session id under `notes/.desktop/`.
The Stop hook only reads: the thread's notes and its parent's, bounded. The
prompt hook names the path once, on a thread's first prompt, and the after-reset
hook hands the notes back after a context reset. Nothing is fetched and no model
runs here.
"""
from __future__ import annotations

from pathlib import Path
import re

NOTES_DIR = Path.home() / ".farplane" / "memory" / "notes"
MAX_OWN = 4000
MAX_PARENT = 2000
SESSION_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{7,}")
PARENT = re.compile(r"(?im)^\W*parent\W*:?\s*`?([A-Za-z0-9][A-Za-z0-9._-]{7,})")
FORK_SOURCE = re.compile(r'"sessionId":\s*"([A-Za-z0-9][A-Za-z0-9._-]{7,})"')
OPEN_GOALS = re.compile(r"(?ims)^##\s*open goals\b.*?(?=^##\s|\Z)")
REMINDER = (
    "Farplane thread notes for this thread: {path}. If this message gives you a ticket "
    "or task scope, write it there first as a Task section (In scope, Out of scope, "
    "Done when, Design). If In scope, Done when or a design link is missing, ask the "
    "user once and wait instead of building. A link shared only for reference goes under "
    "References. Keep an Open goals section at the top, in the user's words, and "
    "Decisions, Progress and V2 candidates there as you work."
)
SCOPE_RULE = ("Work only inside your notes' Open goals and Task (and your parent's) until "
              "the Done when checks pass. List ideas outside it in your answer and notes as v2 "
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
    """A parent named by its desktop id, or a short prefix of either id, becomes the
    session id whose notes exist; unknown names come back unchanged."""
    parent = parent.strip().strip("`")
    aliases = NOTES_DIR / ".desktop"
    if parent.startswith("local_"):
        if (aliases / parent).is_file():
            return (aliases / parent).read_text(encoding="utf-8").strip()
        found = sorted(aliases.glob(f"{parent}*")) if aliases.is_dir() else []
        if len(found) == 1:
            return found[0].read_text(encoding="utf-8").strip()
        parent = parent.removeprefix("local_")
    if not SESSION_ID.fullmatch(parent) or (NOTES_DIR / f"{parent}.md").is_file():
        return parent
    found = sorted(NOTES_DIR.glob(f"{parent}*.md"))
    return found[0].stem if len(found) == 1 else parent


def transcript_of(session_id: str) -> Path | None:
    found = sorted(Path.home().glob(f".claude/projects/*/{session_id}.jsonl"))
    return found[0] if found else None


def parent_context(parent: str | None, own_id: str, limit: int = MAX_PARENT) -> str:
    """The parent's notes and transcript path, so a sub-thread checks its parent's words."""
    parent = resolve(parent) if parent else ""
    if not parent or parent == own_id.strip():
        return ""
    notes = read(parent, limit)
    transcript = transcript_of(parent) if SESSION_ID.fullmatch(parent) else None
    if not notes and transcript is None:
        return ""
    parts = [f"Parent thread {parent}."]
    if notes:
        parts.append(f"Its notes (its decisions bind you too):\n{notes}")
    if transcript is not None:
        parts.append(f"Its transcript: {transcript}. When the user says it was already decided or "
                     "shown, search the user's words there and in your own transcript before any doc.")
    return "\n".join(parts)


def inherit(session_id: str, transcript: str) -> None:
    """A forked thread keeps its original's notes: the fork gets a new session id, but its
    transcript still starts with the original's rows. Copies them once; quiet on any error."""
    path = notes_path(session_id)
    if path is None or path.exists() or not transcript:
        return
    try:
        with open(transcript, encoding="utf-8", errors="replace") as handle:
            for _, line in zip(range(400), handle):
                found = FORK_SOURCE.search(line)
                if not found or found.group(1) == session_id.strip():
                    continue
                source = notes_path(found.group(1))
                if source is not None and source.is_file():
                    text = source.read_text(encoding="utf-8", errors="replace").rstrip()
                    path.write_text(f"{text}\n\nForked from {found.group(1)}; notes copied from there.\n",
                                    encoding="utf-8")
                return
    except OSError:
        return


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
    return with_goals_first(text, limit) or None


def with_goals_first(text: str, limit: int) -> str:
    """Bounded notes that always keep the Open goals section."""
    if len(text) <= limit:
        return text
    found = OPEN_GOALS.search(text)
    if found is None or found.end() <= limit:
        return text[:limit]
    goals = found.group(0).strip()[:limit]
    return f"{goals}\n\n{text[:found.start()]}{text[found.end():]}"[:limit]


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
