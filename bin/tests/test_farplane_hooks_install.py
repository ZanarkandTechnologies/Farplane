from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
BIN_DIR = ROOT / "bin"
ADDED_BIN_PATH = str(BIN_DIR) not in sys.path
if ADDED_BIN_PATH:
    sys.path.insert(0, str(BIN_DIR))

import farplane

if ADDED_BIN_PATH:
    sys.path.remove(str(BIN_DIR))


class FarplaneHooksInstallTests(unittest.TestCase):
    def test_linked_worktree_install_is_blocked(self) -> None:
        git_dir = tempfile.gettempdir() + "/worktrees/task"
        common_dir = tempfile.gettempdir() + "/repo/.git"
        results = [
            farplane.subprocess.CompletedProcess([], 0, git_dir + "\n", ""),
            farplane.subprocess.CompletedProcess([], 0, common_dir + "\n", ""),
        ]
        with patch.object(farplane.subprocess, "run", side_effect=results):
            with self.assertRaisesRegex(
                farplane.CliError, "global Codex installation must come from the primary"
            ):
                farplane.require_primary_checkout_install("hooks_install")

    def test_primary_checkout_install_is_allowed(self) -> None:
        git_dir = tempfile.gettempdir() + "/repo/.git"
        results = [
            farplane.subprocess.CompletedProcess([], 0, git_dir + "\n", ""),
            farplane.subprocess.CompletedProcess([], 0, git_dir + "\n", ""),
        ]
        with patch.object(farplane.subprocess, "run", side_effect=results):
            farplane.require_primary_checkout_install("hooks_install")

    def test_wrapped_hook_inventory_resolves_owner_and_requires_cli(self) -> None:
        with tempfile.TemporaryDirectory(prefix="hook inventory ") as tmp:
            codex_home = Path(tmp).resolve()
            farplane.install_hooks(codex_home)
            source = codex_home / "wrapper-hooks.json"
            source.write_text(json.dumps({"hooks": {"Stop": [{"hooks": [{
                "type": "command",
                "command": '\"$HOME/.codex/bin/farplane\" run -- python3 \"$HOME/.codex/hooks/continuation_gate.py\"'
            }]}]}}))
            commands = farplane.hook_command_inventory(codex_home, source)
            issues, _ = farplane.hook_inventory_issues(commands)
            row = next(row for row in commands
                       if row["target"] == str(codex_home / "hooks" / "continuation_gate.py"))
            self.assertEqual(row["expected"], str(ROOT / "hooks" / "continuation_gate.py"))
            self.assertEqual(row["interpreter"], str(codex_home / "bin" / "farplane"))
            self.assertTrue(row["targetLinked"])
            self.assertTrue(any("interpreter_missing:" + row["interpreter"] in issue
                                for issue in issues))
            (codex_home / "bin" / "farplane").symlink_to(ROOT / "bin" / "farplane")
            self.assertTrue(farplane.hooks_doctor(codex_home)["ok"])

    def test_wrapped_hook_reports_missing_inner_interpreter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = Path(tmp).resolve()
            farplane.install_hooks(codex_home)
            (codex_home / "bin" / "farplane").symlink_to(ROOT / "bin" / "farplane")
            source = codex_home / "custom-hooks.json"
            source.write_text(json.dumps({"hooks": {"Stop": [{"hooks": [{
                "type": "command",
                "command": '\"$HOME/.codex/bin/farplane\" run -- missing-python-for-test \"$HOME/.codex/hooks/continuation_gate.py\"'
            }]}]}}))
            rows = farplane.hook_command_inventory(codex_home, source)
            issues, _ = farplane.hook_inventory_issues(rows)
            self.assertTrue(any("interpreter_missing:missing-python-for-test" in issue for issue in issues))
            self.assertEqual(rows[0]["target"], str(codex_home / "hooks" / "continuation_gate.py"))

    def test_install_retires_obsolete_post_tool_hook_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = Path(tmp).resolve()
            hooks = codex_home / "hooks"
            hooks.mkdir(parents=True)
            for name in farplane.RETIRED_HOOK_FILES:
                (hooks / name).symlink_to(ROOT / "hooks" / name)

            (codex_home / "bin").mkdir()
            (codex_home / "bin" / "farplane").symlink_to(ROOT / "bin" / "farplane")
            payload = farplane.install_hooks(codex_home)

            self.assertTrue(payload["ok"])
            for name in farplane.RETIRED_HOOK_FILES:
                self.assertFalse((hooks / name).is_symlink())
            retired = [row for row in payload["operations"] if row.get("retired")]
            self.assertEqual(len(retired), len(farplane.RETIRED_HOOK_FILES))
            self.assertTrue(all(Path(row["backup"]).is_symlink() for row in retired))


if __name__ == "__main__":
    unittest.main()
