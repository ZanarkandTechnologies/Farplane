"""Regression coverage for capability-contract Git-gate routing."""

from __future__ import annotations

import unittest

from bin.validators.run_git_gate import DEFAULT_CONFIG, load_config, select_checks, stage_config


class SkillContractGitGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = load_config(DEFAULT_CONFIG)

    def test_capability_contract_sources_select_the_contract_check(self) -> None:
        contract_sources = [
            "bin/core/skill_contract.py",
            "bin/core/farplane_cli_commands.py",
            "bin/core/farplane_cli_parser.py",
            "bin/farplane.py",
            "bin/validators/check_doc_frontmatter.py",
            "bin/validators/test_check_doc_frontmatter.py",
            "bin/validators/check_skill_frontmatter.py",
            "bin/validators/test_check_skill_frontmatter.py",
            "bin/validators/check_skill_ensembles.py",
            "bin/validators/test_check_skill_ensembles.py",
        ]
        for stage_name in ("pre_commit", "pre_push"):
            for path in contract_sources:
                with self.subTest(stage=stage_name, path=path):
                    checks = select_checks(
                        stage_config(self.config, stage_name),
                        [path],
                    )
                    self.assertIn("skill_contract", checks)

    def test_skill_contract_docs_select_the_contract_check(self) -> None:
        checks = select_checks(
            stage_config(self.config, "pre_commit"),
            ["docs/skills/system.md"],
        )
        self.assertIn("skill_check", checks)
        self.assertIn("skill_contract", checks)

    def test_skill_package_changes_keep_the_fast_registry_contract_check(self) -> None:
        for stage_name in ("pre_commit", "pre_push"):
            with self.subTest(stage=stage_name):
                checks = select_checks(
                    stage_config(self.config, stage_name),
                    ["skills/x-thread/SKILL.md"],
                )
                self.assertIn("skill_check", checks)
                self.assertNotIn("skill_contract", checks)

    def test_capability_projection_sources_select_projection_check(self) -> None:
        projection_sources = [
            "skills/skill-maintenance/scripts/generate_skill_graph.py",
            "skills/skill-maintenance/scripts/test_generate_skill_graph.py",
            "skills/skill-maintenance/scripts/sync_skill_plugins.py",
            "skills/skill-maintenance/scripts/test_sync_skill_plugins.py",
        ]
        for stage_name in ("pre_commit", "pre_push"):
            for path in projection_sources:
                with self.subTest(stage=stage_name, path=path):
                    checks = select_checks(
                        stage_config(self.config, stage_name),
                        [path],
                    )
                    self.assertIn("skill_projection", checks)

    def test_unrelated_path_does_not_select_the_contract_check(self) -> None:
        checks = select_checks(
            stage_config(self.config, "pre_commit"),
            ["README.md"],
        )
        self.assertNotIn("skill_contract", checks)


if __name__ == "__main__":
    unittest.main()
