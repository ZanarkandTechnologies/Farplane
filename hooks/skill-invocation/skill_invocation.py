#!/usr/bin/env python3
"""PostToolUse hook: record each real skill invocation as a `skill_invoked` row.

- Claude: every `Skill` tool call (source `skill_tool`); a plugin prefix is kept apart from the name.
- Codex: a shell read of an installed `<root>/<name>/SKILL.md` (source `skill_read`), at most one per
  turn and none when the prompt already named a `$skill`. Reads of a source tree (`skills/<name>/`) are
  maintenance, and later reads in a turn are sub-reads (composition, intelligest's skill level-up).
Observation only: it never prints to the agent and never blocks.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for directory in (ROOT / "hooks" / "shared", ROOT / "bin" / "core"):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from runtime_config import farplane_home, hydrate_process_env  # noqa: E402
from skill_events import plugin_and_name, post_skill_event, prompt_names_skill, skill_event_row  # noqa: E402

# A path ending in <name>/SKILL.md, inside a runtime's installed skill roots (~/.codex, ~/.agents, ~/.claude).
SKILL_PATH = re.compile(r"""(?P<path>[^\s'"`;|&<>()]*/(?P<name>[A-Za-z0-9][A-Za-z0-9_.-]*)/SKILL\.md)\b""")
INSTALLED_ROOT = re.compile(r"(^|/)\.(codex|agents|claude)/")
READ_COMMAND = re.compile(r"""(^|[;&|("'\s])(cat|sed|head|tail|nl|less|more|bat|awk)\s""")
WRITE_COMMAND = re.compile(r">\s*\S*SKILL\.md|\bsed\s+(-[a-zA-Z]*\s+)*-i\b|\btee\b")


def text(value: object) -> str:
    return value.strip() if isinstance(value, str) else ""


def installed_skill_reads(command: str) -> list[tuple[str, str]]:
    """(name, path) of installed SKILL.md files a read-only shell command opens, in order."""
    if not READ_COMMAND.search(command) or WRITE_COMMAND.search(command):
        return []
    reads: list[tuple[str, str]] = []
    for match in SKILL_PATH.finditer(command):
        if INSTALLED_ROOT.search(match["path"]) and (match["name"], match["path"]) not in reads:
            reads.append((match["name"], match["path"]))
    return reads


def claude_event(payload: dict[str, object]) -> dict[str, object] | None:
    tool_input = payload.get("tool_input") if isinstance(payload.get("tool_input"), dict) else {}
    plugin, name = plugin_and_name(text(tool_input.get("skill")))
    if not name:
        return None
    installed = Path.home() / ".claude" / "skills" / name / "SKILL.md"
    return skill_event_row(
        kind="skill_invoked",
        skill=name,
        plugin=plugin,
        session_id=text(payload.get("session_id")),
        anchor=text(payload.get("tool_use_id")) or text(payload.get("turn_id")),
        turn_id=text(payload.get("turn_id")),
        cwd=text(payload.get("cwd")),
        source="skill_tool",
        runtime="claude",
        tool_name="Skill",
        skill_path=str(installed) if not plugin and installed.is_file() else f"skill:{text(tool_input.get('skill'))}",
    )


def turn_prompt(payload: dict[str, object], turn_id: str) -> str:
    """The prompt that opened this turn, from the user-turn hook's message window (empty if unknown)."""
    from user_turn import conversation_window_path, load_json_dict, project_root_from_payload

    project = project_root_from_payload(payload)
    session_id = text(payload.get("session_id"))
    if project is None or not session_id:
        return ""
    pending = load_json_dict(conversation_window_path(project, session_id)).get("pending_user_turn")
    if not isinstance(pending, dict) or text(pending.get("user_turn_id")) != turn_id:
        return ""
    return text(pending.get("user_text"))


def first_read_this_turn(session_id: str, turn_id: str) -> bool:
    """True once per (session, turn): the turn's first installed-skill read claims it."""
    state = farplane_home() / "state" / "skill-invocations" / f"{re.sub(r'[^A-Za-z0-9._-]+', '_', session_id)}.json"
    try:
        if json.loads(state.read_text(encoding="utf-8")).get("turn_id") == turn_id:
            return False
    except (OSError, ValueError, AttributeError):
        pass
    try:
        state.parent.mkdir(parents=True, exist_ok=True)
        state.write_text(json.dumps({"turn_id": turn_id}) + "\n", encoding="utf-8")
    except OSError:
        pass
    return True


def codex_event(payload: dict[str, object]) -> dict[str, object] | None:
    tool_input = payload.get("tool_input") if isinstance(payload.get("tool_input"), dict) else {}
    reads = installed_skill_reads(text(tool_input.get("command")))
    session_id, turn_id = text(payload.get("session_id")), text(payload.get("turn_id"))
    if not reads or not session_id or not turn_id or not first_read_this_turn(session_id, turn_id):
        return None
    if prompt_names_skill(turn_prompt(payload, turn_id)):
        return None
    name, path = reads[0]
    return skill_event_row(
        kind="skill_invoked",
        skill=name,
        session_id=session_id,
        anchor=turn_id,
        turn_id=turn_id,
        cwd=text(payload.get("cwd")),
        source="skill_read",
        runtime="codex",
        tool_name="Bash",
        skill_path=path,
    )


def skill_event(payload: dict[str, object], runtime: str) -> dict[str, object] | None:
    if payload.get("hook_event_name") != "PostToolUse":
        return None
    tool = payload.get("tool_name")
    if tool == "Skill":
        return claude_event(payload)
    if tool == "Bash" and runtime == "codex":
        return codex_event(payload)
    return None


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError:
        return 0
    if not isinstance(payload, dict):
        return 0
    hydrate_process_env()
    row = skill_event(payload, os.getenv("FARPLANE_AGENT_RUNTIME", "codex").strip() or "codex")
    if row:
        post_skill_event(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
