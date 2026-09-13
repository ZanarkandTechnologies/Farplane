#!/usr/bin/env python3
"""Integration tests for isolated request-owned commits."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SCRIPT = ROOT / "commit_staged.py"


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=repo, text=True, capture_output=True, check=check)


class IsolatedCommitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        git(self.repo, "init")
        git(self.repo, "config", "user.email", "tests@example.invalid")
        git(self.repo, "config", "user.name", "Farplane Tests")
        (self.repo / "owned.txt").write_text("owned old\n")
        (self.repo / "other.txt").write_text("other old\n")
        (self.repo / "mixed.txt").write_text("first old\nkeep\nlast old\n")
        git(self.repo, "add", "owned.txt", "other.txt", "mixed.txt")
        git(self.repo, "commit", "-m", "chore: seed")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_helper(self, *extra: str) -> tuple[int, dict]:
        result = subprocess.run(
            ["python3", str(SCRIPT), "--repo-root", str(self.repo),
             "--message", "feat(test): commit owned change", *extra],
            text=True, capture_output=True,
        )
        return result.returncode, json.loads(result.stdout)

    def test_commits_requested_file_and_preserves_other_unstaged(self) -> None:
        (self.repo / "owned.txt").write_text("owned new\n")
        (self.repo / "other.txt").write_text("other unstaged\n")
        code, receipt = self.run_helper("--path", "owned.txt")
        self.assertEqual(code, 0)
        self.assertEqual(receipt["status"], "committed")
        self.assertEqual(receipt["paths"], ["owned.txt"])
        self.assertEqual(git(self.repo, "show", "--format=", "--name-only", "HEAD").stdout.strip(), "owned.txt")
        self.assertIn("other.txt", git(self.repo, "diff", "--name-only").stdout)

    def test_preserves_unrelated_prestaged_file(self) -> None:
        (self.repo / "other.txt").write_text("other staged\n")
        git(self.repo, "add", "other.txt")
        staged_before = git(self.repo, "diff", "--cached", "--binary", "--", "other.txt").stdout
        (self.repo / "owned.txt").write_text("owned new\n")
        code, receipt = self.run_helper("--path", "owned.txt")
        self.assertEqual(code, 0)
        self.assertEqual(receipt["status"], "committed")
        self.assertEqual(git(self.repo, "diff", "--cached", "--binary", "--", "other.txt").stdout, staged_before)
        self.assertNotIn("other.txt", git(self.repo, "show", "--format=", "--name-only", "HEAD").stdout)

    def test_cached_patch_commits_only_selected_hunk(self) -> None:
        (self.repo / "mixed.txt").write_text("first new\nkeep\nlast new\n")
        patch = self.repo / "first.patch"
        patch.write_text(
            "diff --git a/mixed.txt b/mixed.txt\n--- a/mixed.txt\n+++ b/mixed.txt\n"
            "@@ -1,3 +1,3 @@\n-first old\n+first new\n keep\n last old\n"
        )
        code, receipt = self.run_helper("--cached-patch", str(patch))
        self.assertEqual(code, 0)
        self.assertEqual(receipt["status"], "committed")
        self.assertIn("+first new", git(self.repo, "show", "--format=", "--", "mixed.txt").stdout)
        remaining = git(self.repo, "diff", "--", "mixed.txt").stdout
        self.assertIn("+last new", remaining)
        self.assertNotIn("+first new", remaining)

    def test_cached_patch_preserves_prestaged_hunk_in_same_file(self) -> None:
        (self.repo / "mixed.txt").write_text("first old\nkeep\nlast staged\n")
        git(self.repo, "add", "mixed.txt")
        (self.repo / "mixed.txt").write_text("first new\nkeep\nlast staged\n")
        patch = self.repo / "first.patch"
        patch.write_text(
            "diff --git a/mixed.txt b/mixed.txt\n--- a/mixed.txt\n+++ b/mixed.txt\n"
            "@@ -1,3 +1,3 @@\n-first old\n+first new\n keep\n last old\n"
        )
        code, receipt = self.run_helper("--cached-patch", str(patch))
        self.assertEqual(code, 0)
        self.assertEqual(receipt["status"], "committed")
        staged = git(self.repo, "diff", "--cached", "--", "mixed.txt").stdout
        self.assertIn("+last staged", staged)
        self.assertNotIn("+first new", staged)
        committed = git(self.repo, "show", "--format=", "--", "mixed.txt").stdout
        self.assertIn("+first new", committed)
        self.assertNotIn("+last staged", committed)

    def test_rejects_broad_or_missing_boundary_without_mutation(self) -> None:
        before = git(self.repo, "rev-parse", "HEAD").stdout.strip()
        directory = self.repo / "group"
        directory.mkdir()
        (directory / "owned.txt").write_text("owned\n")
        (directory / "unrelated.txt").write_text("unrelated\n")
        for unsafe in (".", ":(glob)**", "*", "group"):
            with self.subTest(unsafe=unsafe):
                code, receipt = self.run_helper("--path", unsafe)
                self.assertEqual(code, 2)
                self.assertEqual(receipt["status"], "error")
                self.assertEqual(git(self.repo, "rev-parse", "HEAD").stdout.strip(), before)


if __name__ == "__main__":
    unittest.main()
