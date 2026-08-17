from __future__ import annotations

import importlib.util
import io
import json
import sys
import tempfile
import tomllib
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
HOOK_PATH = ROOT / "hooks/skill_file_line_gate.py"
SPEC = importlib.util.spec_from_file_location("skill_file_line_gate", HOOK_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class SkillFileLineGateTests(unittest.TestCase):
    def make_root(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        return Path(temporary.name)

    def write_lines(self, root: Path, relative: str, count: int) -> Path:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("line\n" * count, encoding="utf-8")
        return path

    def payload(self, root: Path, relative: str) -> dict[str, object]:
        return {
            "hook_event_name": "PostToolUse",
            "tool_name": "apply_patch",
            "cwd": str(root),
            "tool_input": {
                "command": (
                    "*** Begin Patch\n"
                    f"*** Update File: {relative}\n"
                    "@@\n-old\n+new\n"
                    "*** End Patch\n"
                )
            },
        }

    def test_touched_skill_at_limit_passes(self) -> None:
        root = self.make_root()
        relative = "skills/demo/SKILL.md"
        self.write_lines(root, relative, 200)

        self.assertIsNone(MODULE.gate_skill_files(self.payload(root, relative), repo_root=root))

    def test_touched_skill_over_limit_blocks_with_repair_context(self) -> None:
        root = self.make_root()
        relative = "skills/demo/SKILL.md"
        self.write_lines(root, relative, 201)

        result = MODULE.gate_skill_files(self.payload(root, relative), repo_root=root)

        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual("block", result["decision"])
        self.assertIn("skills/demo/SKILL.md: 201 lines", result["reason"])
        self.assertIn("edit remains applied", result["reason"])

    def test_untouched_oversized_skill_is_not_scanned(self) -> None:
        root = self.make_root()
        self.write_lines(root, "skills/legacy/SKILL.md", 201)
        self.write_lines(root, "docs/note.md", 2)

        result = MODULE.gate_skill_files(
            self.payload(root, "docs/note.md"),
            repo_root=root,
        )

        self.assertIsNone(result)

    def test_non_skill_and_outside_repo_paths_are_ignored(self) -> None:
        root = self.make_root()
        self.write_lines(root, "skills/demo/reference.md", 201)
        outside = root.parent / "SKILL.md"
        outside.write_text("line\n" * 201, encoding="utf-8")
        self.addCleanup(outside.unlink)

        self.assertIsNone(
            MODULE.gate_skill_files(
                self.payload(root, "skills/demo/reference.md"),
                repo_root=root,
            )
        )
        self.assertIsNone(
            MODULE.gate_skill_files(self.payload(root, "../SKILL.md"), repo_root=root)
        )

    def test_other_events_and_tools_are_ignored(self) -> None:
        root = self.make_root()
        relative = "skills/demo/SKILL.md"
        self.write_lines(root, relative, 201)
        payload = self.payload(root, relative)
        payload["hook_event_name"] = "Stop"
        self.assertIsNone(MODULE.gate_skill_files(payload, repo_root=root))
        payload["hook_event_name"] = "PostToolUse"
        payload["tool_name"] = "exec_command"
        self.assertIsNone(MODULE.gate_skill_files(payload, repo_root=root))

    def test_main_emits_valid_block_json(self) -> None:
        root = self.make_root()
        relative = "skills/demo/SKILL.md"
        self.write_lines(root, relative, 201)
        stdin = io.StringIO(json.dumps(self.payload(root, relative)))
        stdout = io.StringIO()

        with mock.patch.object(sys, "stdin", stdin), redirect_stdout(stdout):
            self.assertEqual(0, MODULE.main())

        self.assertEqual("block", json.loads(stdout.getvalue())["decision"])

    def test_hook_config_routes_apply_patch_aliases_to_gate(self) -> None:
        config = json.loads((ROOT / "hooks.json").read_text(encoding="utf-8"))
        groups = config["hooks"]["PostToolUse"]
        commands = [hook["command"] for group in groups for hook in group["hooks"]]
        self.assertTrue(any("skill_file_line_gate.py" in command for command in commands))
        self.assertTrue(any("apply_patch" in group.get("matcher", "") for group in groups))

    def test_pre_commit_backstop_is_strict_and_skill_scoped(self) -> None:
        with (ROOT / "rules/git-review-gates.toml").open("rb") as handle:
            config = tomllib.load(handle)
        argv = config["checks"]["skill_file_line_count"]["argv"]
        self.assertIn("--strict", argv)
        self.assertEqual("200", argv[argv.index("--max-lines") + 1])
        self.assertEqual("skills/**/SKILL.md", argv[argv.index("--glob") + 1])


if __name__ == "__main__":
    unittest.main()
