#!/usr/bin/env python3
"""Regression tests for the staged-only commit helper."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "commit_staged.py"


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=repo, text=True, capture_output=True, check=check
    )


class CommitStagedTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        git(self.repo, "init")
        git(self.repo, "config", "user.email", "tests@example.invalid")
        git(self.repo, "config", "user.name", "Farplane Tests")
        (self.repo / "seed.txt").write_text("seed\n")
        git(self.repo, "add", "seed.txt")
        git(self.repo, "commit", "-m", "chore: seed")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_helper(self, message: str = "feat(test): add boundary") -> tuple[int, dict[str, str]]:
        result = subprocess.run(
            ["python3", str(SCRIPT), "--repo-root", str(self.repo), "--message", message],
            text=True,
            capture_output=True,
        )
        return result.returncode, json.loads(result.stdout)

    def test_no_staged_changes_leaves_head_unchanged(self) -> None:
        before = git(self.repo, "rev-parse", "HEAD").stdout.strip()
        code, receipt = self.run_helper()
        self.assertEqual(code, 0)
        self.assertEqual(receipt, {"status": "no_staged_changes"})
        self.assertEqual(git(self.repo, "rev-parse", "HEAD").stdout.strip(), before)

    def test_commits_only_staged_changes_and_preserves_unstaged_work(self) -> None:
        (self.repo / "staged.txt").write_text("staged\n")
        git(self.repo, "add", "staged.txt")
        (self.repo / "seed.txt").write_text("unstaged change\n")
        before = git(self.repo, "rev-parse", "HEAD").stdout.strip()

        code, receipt = self.run_helper()

        self.assertEqual(code, 0)
        self.assertEqual(receipt["status"], "committed")
        self.assertNotEqual(receipt["commit"], before)
        self.assertEqual(git(self.repo, "show", "--format=", "--name-only", "HEAD").stdout.strip(), "staged.txt")
        self.assertIn("seed.txt", git(self.repo, "diff", "--name-only").stdout)
        self.assertEqual(git(self.repo, "diff", "--cached", "--name-only").stdout, "")

    def test_helper_has_no_stage_or_push_command(self) -> None:
        source = SCRIPT.read_text()
        self.assertNotIn('"add"', source)
        self.assertNotIn('"push"', source)


if __name__ == "__main__":
    unittest.main()
