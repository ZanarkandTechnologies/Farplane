"""Regression coverage for central static-lint Git-gate routing."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from bin.core.lint.registry import build_registry
from bin.validators.run_git_gate import (
    DEFAULT_CONFIG, build_snapshot, configured_argv, load_config, select_checks, stage_config,
)


class LintGitGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = load_config(DEFAULT_CONFIG)

    def test_every_git_stage_delegates_static_contract_selection_to_lint(self) -> None:
        expected = {"pre_commit": "lint_changed", "pre_push": "lint_branch"}
        for stage_name, check_id in expected.items():
            with self.subTest(stage=stage_name):
                checks = select_checks(stage_config(self.config, stage_name), ["docs/guides/work-loop.md"])
                self.assertIn(check_id, checks)

    def test_python_checks_run_under_the_gate_interpreter(self) -> None:
        argv = configured_argv(self.config, "lint_changed", base="main")
        self.assertEqual(argv[0], sys.executable)

    def test_registry_selects_document_project_skill_eval_and_ticket_contracts(self) -> None:
        registry = build_registry()
        cases = {
            "docs/guides/work-loop.md": "document_frontmatter",
            "farplane/harness.yaml": "project_contract",
            "skills/eval/evals/evals.json": "eval_contract",
            "skills/eval/SKILL.md": "skill_contract",
            "tickets/TASK-9031/ticket.md": "ticket_metadata",
        }
        for path, check_id in cases.items():
            with self.subTest(path=path):
                checks = registry.select(scope="all", changed_paths=(path,))
                self.assertIn(check_id, {spec.check_id for spec in checks})

    def test_git_only_diff_guards_remain_outside_lint_registry(self) -> None:
        ids = {spec.check_id for spec in build_registry().specs()}
        self.assertNotIn("source_line_growth_staged", ids)
        self.assertNotIn("ticket_closure_gate", ids)

    def test_skill_line_gate_ratcheted_legacy_files(self) -> None:
        argv = self.config["checks"]["skill_file_line_count"]["argv"]
        self.assertNotIn("--strict", argv)
        self.assertIn("--max-lines", argv)
        self.assertIn("200", argv)



def git(repo: Path, *args: str) -> str:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(["git", *args], cwd=repo, env=env, text=True, capture_output=True,
                          check=True).stdout.strip()


class SnapshotTests(unittest.TestCase):
    """The gate judges only what is committed or pushed, never other threads' files."""

    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name) / "repo"
        self.repo.mkdir()
        git(self.repo, "init", "-q", "-b", "main")
        (self.repo / ".gitignore").write_text("local/\n")
        (self.repo / "a.md").write_text("committed\n")
        git(self.repo, "add", ".")
        git(self.repo, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "base")
        (self.repo / "local").mkdir()
        (self.repo / "local" / "state.txt").write_text("ignored local state\n")
        (self.repo / "a.md").write_text("staged\n")
        git(self.repo, "add", "a.md")
        (self.repo / "a.md").write_text("unstaged other-thread edit\n")
        (self.repo / "wip.md").write_text("---\nbroken: [\n")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def snapshot(self, stage: str) -> Path:
        dest = Path(self.temp.name) / stage
        dest.mkdir()
        with patch.dict(os.environ, {}, clear=False):
            for key in [k for k in os.environ if k.startswith("GIT_")]:
                os.environ.pop(key)
            return build_snapshot(stage, dest, base="main", root=self.repo)

    def test_pre_commit_judges_the_staged_index_only(self) -> None:
        snap = self.snapshot("pre_commit")
        self.assertEqual((snap / "a.md").read_text(), "staged\n")
        self.assertFalse((snap / "wip.md").exists())
        self.assertEqual(git(snap, "diff", "--cached", "--name-only"), "a.md")
        self.assertEqual(git(snap, "status", "--porcelain", "--untracked-files=all"), "M  a.md")

    def test_pre_push_judges_head_and_links_ignored_state(self) -> None:
        snap = self.snapshot("pre_push")
        self.assertEqual((snap / "a.md").read_text(), "committed\n")
        self.assertFalse((snap / "wip.md").exists())
        self.assertTrue((snap / "local").is_symlink())
        self.assertEqual((snap / "local" / "state.txt").read_text(), "ignored local state\n")
        self.assertEqual(git(snap, "status", "--porcelain", "--untracked-files=all"), "")
        self.assertEqual(git(snap, "rev-parse", "HEAD"), git(self.repo, "rev-parse", "HEAD"))

    def test_hook_index_override_selects_the_commit_tree(self) -> None:
        alt = Path(self.temp.name) / "alt.index"
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        subprocess.run(["git", "read-tree", "HEAD"], cwd=self.repo, check=True,
                       env={**env, "GIT_INDEX_FILE": str(alt)})
        dest = Path(self.temp.name) / "hook"
        dest.mkdir()
        with patch.dict(os.environ, {"GIT_INDEX_FILE": str(alt)}):
            snap = build_snapshot("pre_commit", dest, base="main", root=self.repo)
        self.assertEqual((snap / "a.md").read_text(), "committed\n")
        self.assertEqual(git(snap, "diff", "--cached", "--name-only"), "")


if __name__ == "__main__":
    unittest.main()
