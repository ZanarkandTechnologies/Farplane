from __future__ import annotations

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

    def test_install_retires_obsolete_post_tool_hook_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = Path(tmp)
            hooks = codex_home / "hooks"
            hooks.mkdir(parents=True)
            for name in farplane.RETIRED_HOOK_FILES:
                (hooks / name).symlink_to(ROOT / "hooks" / name)

            payload = farplane.install_hooks(codex_home)

            self.assertTrue(payload["ok"])
            for name in farplane.RETIRED_HOOK_FILES:
                self.assertFalse((hooks / name).is_symlink())
            retired = [row for row in payload["operations"] if row.get("retired")]
            self.assertEqual(len(retired), len(farplane.RETIRED_HOOK_FILES))
            self.assertTrue(all(Path(row["backup"]).is_symlink() for row in retired))


if __name__ == "__main__":
    unittest.main()
