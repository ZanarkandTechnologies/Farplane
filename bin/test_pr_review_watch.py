#!/usr/bin/env python3
"""Tests for bin/pr_review_watch.py."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from pr_review_watch import (
    PipelineConfigError,
    classify,
    load_fixture,
    load_project_pipeline,
    parse_project_pipeline,
)


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "skills" / "pr-review-watch" / "fixtures"
HELPER = ROOT / "bin" / "pr_review_watch.py"


class PrReviewWatchTests(unittest.TestCase):
    def config(self):
        return parse_project_pipeline(
            (FIXTURES / "pipeline-config.md").read_text(encoding="utf-8"),
            str(FIXTURES / "pipeline-config.md"),
        )

    def classify_fixture(self, name: str) -> str:
        verdict = classify(load_fixture(FIXTURES / name), self.config())
        return verdict.state

    def test_clean_pass_fixture(self) -> None:
        self.assertEqual(self.classify_fixture("clean-pass.json"), "pass")

    def test_failed_checks_are_actionable(self) -> None:
        self.assertEqual(self.classify_fixture("failed-checks.json"), "actionable")

    def test_gh_bucket_fail_checks_are_actionable(self) -> None:
        self.assertEqual(self.classify_fixture("gh-bucket-fail.json"), "actionable")

    def test_unresolved_comments_are_actionable(self) -> None:
        self.assertEqual(self.classify_fixture("unresolved-comments.json"), "actionable")

    def test_pending_checks_wait(self) -> None:
        self.assertEqual(self.classify_fixture("pending-checks.json"), "wait")

    def test_missing_auth_blocks(self) -> None:
        self.assertEqual(self.classify_fixture("missing-auth.json"), "blocked")

    def test_no_active_pr_blocks(self) -> None:
        self.assertEqual(self.classify_fixture("no-active-pr.json"), "blocked")

    def test_missing_config_blocks_in_cli(self) -> None:
        result = subprocess.run(
            [
                "python3",
                str(HELPER),
                "classify",
                "--fixture",
                str(FIXTURES / "clean-pass.json"),
                "--repo",
                str(FIXTURES),
                "--json",
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["verdict"]["state"], "blocked")
        self.assertIsNone(payload["config"])

    def test_cli_classify_fixture_outputs_verdict_json(self) -> None:
        result = subprocess.run(
            [
                "python3",
                str(HELPER),
                "classify",
                "--fixture",
                str(FIXTURES / "clean-pass.json"),
                "--config",
                str(FIXTURES / "pipeline-config.md"),
                "--json",
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["verdict"]["state"], "pass")
        self.assertEqual(payload["config"]["poll_interval_minutes"], 10)

    def test_load_project_pipeline_prefers_docs_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            (repo / "docs").mkdir()
            (repo / "PROJECT_RULES.md").write_text("no config here", encoding="utf-8")
            (repo / "docs" / "pr-review-pipeline.md").write_text(
                (FIXTURES / "pipeline-config.md").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            config = load_project_pipeline(repo)
        self.assertTrue(config.source_path.endswith("docs/pr-review-pipeline.md"))

    def test_invalid_poll_interval_rejected(self) -> None:
        with self.assertRaises(PipelineConfigError):
            parse_project_pipeline(
                """
```json
{"pr_review_pipeline": {"providers": ["github"], "poll_interval_minutes": 1}}
```
""",
                "inline",
            )

    def test_non_integer_poll_interval_rejected(self) -> None:
        with self.assertRaises(PipelineConfigError):
            parse_project_pipeline(
                """
```json
{"pr_review_pipeline": {"providers": ["github"], "poll_interval_minutes": "soon"}}
```
""",
                "inline",
            )

    def test_string_boolean_pass_condition_rejected(self) -> None:
        with self.assertRaises(PipelineConfigError):
            parse_project_pipeline(
                """
```json
{
  "pr_review_pipeline": {
    "providers": ["github"],
    "pass_conditions": {"require_checks_pass": "false"}
  }
}
```
""",
                "inline",
            )


if __name__ == "__main__":
    unittest.main()
