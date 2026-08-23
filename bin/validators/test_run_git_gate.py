"""Regression coverage for central static-lint Git-gate routing."""

from __future__ import annotations

import unittest

from bin.core.lint.registry import build_registry
from bin.validators.run_git_gate import DEFAULT_CONFIG, load_config, select_checks, stage_config


class LintGitGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = load_config(DEFAULT_CONFIG)

    def test_every_git_stage_delegates_static_contract_selection_to_lint(self) -> None:
        expected = {"pre_commit": "lint_changed", "pre_push": "lint_branch"}
        for stage_name, check_id in expected.items():
            with self.subTest(stage=stage_name):
                checks = select_checks(stage_config(self.config, stage_name), ["docs/features/FEAT-0039.md"])
                self.assertIn(check_id, checks)

    def test_registry_selects_feature_project_skill_eval_and_ticket_contracts(self) -> None:
        registry = build_registry()
        cases = {
            "docs/features/FEAT-0039.md": "feature_and_system_records",
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


if __name__ == "__main__":
    unittest.main()
