import json
import subprocess
import tempfile
import unittest
from pathlib import Path

GUARD = Path(__file__).resolve().parents[2] / "hooks" / "worktree-guard" / "worktree_guard.sh"


def decide(tool, tool_input, cwd=None):
    payload = json.dumps({"tool_name": tool, "cwd": cwd or "/nonexistent", "tool_input": tool_input})
    out = subprocess.run(["sh", str(GUARD)], input=payload, capture_output=True, text=True).stdout
    return json.loads(out)["hookSpecificOutput"]["permissionDecision"] if out.strip() else "allow"


class WorktreeGuardTest(unittest.TestCase):
    def test_new_worktree_is_denied(self):
        self.assertEqual(decide("Bash", {"command": "git fetch && git worktree add .claude/worktrees/x -b fix/x origin/dev"}), "deny")
        self.assertEqual(decide("Bash", {"command": "git -C ~/repo worktree add ../y"}), "deny")

    def test_override_and_other_worktree_commands_pass(self):
        self.assertEqual(decide("Bash", {"command": "FARPLANE_WORKTREE_OK=1 git worktree add ../chairhorse-12"}), "allow")
        self.assertEqual(decide("Bash", {"command": "git worktree list"}), "allow")
        self.assertEqual(decide("Bash", {"command": "git worktree remove ../old"}), "allow")
        self.assertEqual(decide("Bash", {"command": "ls"}), "allow")

    def test_session_with_its_own_worktree_is_denied(self):
        tool = "mcp__ccd_session__start_session"
        self.assertEqual(decide(tool, {"title": "x", "use_worktree": True}), "deny")
        self.assertEqual(decide(tool, {"title": "x", "use_worktree": False}), "allow")
        self.assertEqual(decide(tool, {"title": "worktree notes"}), "allow")

    def test_repo_that_opted_in_may_add_worktrees(self):
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(["git", "init", "-q", d], check=True)
            add = {"command": "git worktree add .claude/worktrees/x -b fix/x origin/dev"}
            self.assertEqual(decide("Bash", add, d), "deny")
            subprocess.run(["git", "-C", d, "config", "farplane.worktreePerChange", "true"], check=True)
            self.assertEqual(decide("Bash", add, d), "allow")
            self.assertEqual(decide("mcp__ccd_session__start_session", {"title": "x", "use_worktree": True}, d), "allow")


if __name__ == "__main__":
    unittest.main()
