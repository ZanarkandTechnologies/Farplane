"""One task per thread: scope the user sets with <task>...</task>.

The prompt hook saves the text between the tags to
`.farplane/tasks/<session_id>.md`; a new tag replaces it and an empty tag clears
it. The Stop hook reads it by the same session id. A thread with no file (a
fork, or one another session started) falls back to the latest tag in a real
user message of its transcript. Only user text sets a task, never the agent's.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
from typing import Callable, Mapping

ROOT = Path(__file__).resolve().parents[2]
TASKS_DIR = ROOT / ".farplane" / "tasks"
MAX_TASK = 4000
REQUIRED_PATHS_ENV = "FARPLANE_TASK_REQUIRED_PATHS"
TAG = re.compile(r"<task>(.*?)</task>", re.S | re.I)
SECTIONS = {
    "In scope": re.compile(r"(?im)^\W*in[ -]scope\b"),
    "Out of scope": re.compile(r"(?im)^\W*(?:out of|not in)[ -]scope\b"),
    "Done when": re.compile(r"(?im)^\W*done[ -]when\b"),
    "Design link": re.compile(r"(?i)\b(?:figma\.com/(?:design|file|proto|board)/|design:\s*https?://)"),
}


def task_path(session_id: str, tasks_dir: Path | None = None) -> Path | None:
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", session_id.strip()).strip("._")
    return (tasks_dir or TASKS_DIR) / f"{name}.md" if name else None


def tag_in(text: str) -> str | None:
    """The latest <task> body in text, stripped; None when there is no tag."""
    found = TAG.findall(text)
    return found[-1].strip() if found else None


def save(session_id: str, body: str, tasks_dir: Path | None = None) -> Path | None:
    """Write (or, for an empty body, clear) this thread's task."""
    path = task_path(session_id, tasks_dir)
    if path is None:
        return None
    if not body:
        path.unlink(missing_ok=True)
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body[:MAX_TASK] + "\n", encoding="utf-8")
    return path


def missing(body: str) -> list[str]:
    return [name for name, pattern in SECTIONS.items() if not pattern.search(body)]


def title(body: str) -> str:
    first = next((line.strip(" #-*") for line in body.splitlines() if line.strip()), "")
    return first[:80]


def transcript_tag(transcript_path: str | None,
                   is_user_row: Callable[[Mapping[str, object]], str | None]) -> str | None:
    """The latest <task> a real user wrote in the transcript, if any."""
    if not transcript_path or not os.path.isfile(transcript_path):
        return None
    latest = None
    with open(transcript_path, encoding="utf-8") as handle:
        for line in handle:
            if "<task>" not in line.lower():
                continue
            row = json.loads(line)
            text = is_user_row(row) if isinstance(row, dict) else None
            body = tag_in(text) if text else None
            if body is not None:
                latest = body
    return latest


def current(session_id: str, transcript_path: str | None,
            is_user_row: Callable[[Mapping[str, object]], str | None],
            tasks_dir: Path | None = None) -> str | None:
    """This thread's task: its saved file, else the transcript's latest tag."""
    path = task_path(session_id, tasks_dir) if session_id else None
    if path is not None and path.is_file():
        return path.read_text(encoding="utf-8").strip()[:MAX_TASK] or None
    body = transcript_tag(transcript_path, is_user_row)
    if body and path is not None:
        save(session_id, body, tasks_dir)
    return body or None


def requires_task(cwd: str, environ: Mapping[str, str]) -> bool:
    """True when cwd sits under a path listed in FARPLANE_TASK_REQUIRED_PATHS."""
    raw = environ.get(REQUIRED_PATHS_ENV, "")
    try:
        here = Path(cwd).expanduser().resolve()
    except (OSError, RuntimeError):
        return False
    for entry in filter(None, (part.strip() for part in raw.split(os.pathsep))):
        root = Path(entry).expanduser().resolve()
        if here == root or root in here.parents:
            return True
    return False


def scope_rule() -> str:
    return ("Work only inside the task's In scope until its Done when checks pass. "
            "List ideas outside it in your answer as v2 candidates; do not build them.")


def prompt_context(session_id: str, prompt: str, cwd: str, transcript_path: str | None,
                   environ: Mapping[str, str],
                   is_user_row: Callable[[Mapping[str, object]], str | None],
                   tasks_dir: Path | None = None) -> str:
    """Context for the agent on a user prompt: a set or cleared task, or the pre-work ask."""
    path = task_path(session_id, tasks_dir) if session_id else None
    if path is None:
        return ""
    body = tag_in(prompt)
    if body is not None:
        save(session_id, body, tasks_dir)
        if not body:
            return "Farplane thread task cleared."
        gaps = missing(body)
        line = f"Farplane thread task set: {title(body)} (saved to {path})."
        if gaps:
            line += (f" Missing: {', '.join(gaps)}. Before building, ask the user once "
                     "for the missing pieces.")
        if "Design link" not in gaps:
            line += " Open its Design link before building; if it will not open, ask the user once."
        return f"{line} {scope_rule()}"
    if path.is_file() or not requires_task(cwd, environ):
        return ""
    if current(session_id, transcript_path, is_user_row, tasks_dir):
        return ""
    asked = path.with_suffix(".asked")
    if asked.exists():
        return ""
    asked.parent.mkdir(parents=True, exist_ok=True)
    asked.touch()
    return ("Farplane: this project needs a thread task before building. If the user "
            "linked one (a tracker task, an issue), fill it from that source and write "
            f"it to {path} with In scope, Out of scope, Done when and Design link "
            "(a design link that opens). If anything is missing, ask the user once "
            "for it, or for a <task>...</task> message, before building. "
            "Questions, reviews and proposals need no task.")
