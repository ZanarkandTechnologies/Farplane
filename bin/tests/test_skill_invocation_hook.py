from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
HOOK_PATH = ROOT / "hooks/skill-invocation/skill_invocation.py"
SPEC = importlib.util.spec_from_file_location("skill_invocation", HOOK_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

INSTALLED = "/Users/op/.codex/skills/research/SKILL.md"


def post(tool: str, **fields: object) -> dict[str, object]:
    return {"hook_event_name": "PostToolUse", "tool_name": tool, "session_id": "s1", "cwd": "/tmp", **fields}


class SkillInvocationHookTests(unittest.TestCase):
    def setUp(self) -> None:
        state = tempfile.TemporaryDirectory()
        self.addCleanup(state.cleanup)
        patcher = mock.patch.dict(os.environ, {"FARPLANE_STATE_DIR": state.name})
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_claude_skill_call_is_an_invocation_with_plugin_kept_apart(self) -> None:
        row = MODULE.skill_event(post("Skill", tool_use_id="tu1", tool_input={"skill": "farplane:commit"}), "claude")

        self.assertEqual(row["hookName"], "skill-invocation-listener")
        self.assertEqual(row["hookType"], "PostToolUse")
        self.assertEqual(row["payload"]["eventType"], "skill_invoked")
        self.assertEqual(row["payload"]["skillId"], "commit")
        self.assertEqual(row["payload"]["plugin"], "farplane")
        self.assertEqual(row["payload"]["source"], "skill_tool")
        self.assertEqual(row["eventKey"], "skill-invocation-listener:skill_invoked:s1:tu1:farplane:commit")

    def test_claude_bash_reads_are_never_invocations(self) -> None:
        payload = post("Bash", turn_id="t1", tool_input={"command": f"cat {INSTALLED}"})
        self.assertIsNone(MODULE.skill_event(payload, "claude"))

    def test_codex_counts_first_installed_read_per_turn_only(self) -> None:
        first = post("Bash", turn_id="t1", tool_input={"command": f"sed -n '1,220p' {INSTALLED}"})
        level_up = post("Bash", turn_id="t1", tool_input={"command": "cat /Users/op/.codex/skills/advise/SKILL.md"})
        next_turn = post("Bash", turn_id="t2", tool_input={"command": "cat ~/.agents/skills/advise/SKILL.md"})

        row = MODULE.skill_event(first, "codex")
        self.assertEqual((row["payload"]["skillId"], row["payload"]["source"]), ("research", "skill_read"))
        self.assertIsNone(MODULE.skill_event(level_up, "codex"))
        self.assertEqual(MODULE.skill_event(next_turn, "codex")["payload"]["skillId"], "advise")

    def test_codex_source_tree_reads_and_writes_are_maintenance(self) -> None:
        commands = [
            "sed -n '1,80p' skills/research/SKILL.md",
            "cat /Users/op/projects/Farplane/skills/research/SKILL.md",
            f"sed -i '' 's/a/b/' {INSTALLED}",
            f"rg -n heat {INSTALLED}",
        ]
        for index, command in enumerate(commands):
            payload = post("Bash", turn_id=f"t{index}", tool_input={"command": command})
            self.assertIsNone(MODULE.skill_event(payload, "codex"), command)

    def test_codex_turn_that_named_a_skill_counts_no_read(self) -> None:
        payload = post("Bash", turn_id="t1", tool_input={"command": f"cat {INSTALLED}"})
        with mock.patch.object(MODULE, "turn_prompt", return_value="$intelligest https://example.com/v"):
            self.assertIsNone(MODULE.skill_event(payload, "codex"))

    def test_installed_skill_reads_parses_wrapped_commands(self) -> None:
        reads = MODULE.installed_skill_reads(f'bash -lc "cat {INSTALLED} && cat ~/.claude/skills/pdf/SKILL.md"')
        self.assertEqual([name for name, _ in reads], ["research", "pdf"])


if __name__ == "__main__":
    unittest.main()
