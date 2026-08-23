from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch


BIN_DIR = Path(__file__).resolve().parents[1]
if str(BIN_DIR) not in sys.path:
    sys.path.insert(0, str(BIN_DIR))

import farplane
from lint import build_registry
from lint.models import LintContext


class FarplaneLintTests(unittest.TestCase):
    def selected_check_ids(self, scope: str) -> set[str]:
        return {spec.check_id for spec in build_registry().select(scope=scope, changed_paths=None)}

    def test_parser_defaults_lint_to_all(self) -> None:
        args = farplane.build_parser().parse_args(["lint"])

        self.assertEqual(args.scope, "all")

    def test_skill_scope_uses_the_unified_skill_contract_validator(self) -> None:
        self.assertIn("skill_contract", self.selected_check_ids("skills"))

    def test_skill_scope_checks_registry_drift_without_writing_projections(self) -> None:
        registry = build_registry()
        checks = registry.select(scope="skills", changed_paths=None)

        self.assertIn("skill_registry", {check.check_id for check in checks})
        commands = [check.command(LintContext(BIN_DIR.parent)) for check in checks if check.command]
        self.assertFalse(any("--write" in command for command in commands))

    def test_document_scope_routes_each_document_metadata_owner(self) -> None:
        self.assertTrue(
            {
                "document_frontmatter",
                "feature_and_system_records",
                "template_registry",
                "template_metadata",
                "source_registry",
            }.issubset(self.selected_check_ids("docs"))
        )

    def test_changed_feature_selects_its_semantic_document_contract(self) -> None:
        checks = build_registry().select(
            scope="all",
            changed_paths=("docs/features/FEAT-0039.md",),
        )

        self.assertIn("feature_and_system_records", {check.check_id for check in checks})

    def test_validate_has_no_static_frontmatter_alias(self) -> None:
        with self.assertRaises(SystemExit):
            farplane.build_parser().parse_args(["validate", "frontmatter"])

    def test_validate_skills_is_the_projection_write_boundary(self) -> None:
        args = farplane.build_parser().parse_args(["validate", "skills"])

        self.assertEqual(args.func.__name__, "run_validate_skills")
        self.assertFalse(args.check)

    def test_validate_skills_refreshes_projections_before_final_lint(self) -> None:
        args = farplane.build_parser().parse_args(["validate", "skills"])

        class Completed:
            returncode = 0
            stdout = "ok"
            stderr = ""

        with patch("farplane_skill_validation.subprocess.run", return_value=Completed()) as run:
            self.assertEqual(args.func(args), 0)

        commands = [call.args[0] for call in run.call_args_list]
        self.assertEqual(len(commands), 4)
        self.assertEqual(commands[0][-1], "--write")
        self.assertIn("skill-registry", commands[1])
        self.assertIn("harness-reference", commands[2])
        self.assertEqual(commands[3][-2:], ("lint", "skills"))

    def test_validate_skills_check_mode_never_writes_projections(self) -> None:
        args = farplane.build_parser().parse_args(["validate", "skills", "--check"])

        class Completed:
            returncode = 0
            stdout = "ok"
            stderr = ""

        with patch("farplane_skill_validation.subprocess.run", return_value=Completed()) as run:
            self.assertEqual(args.func(args), 0)

        commands = [call.args[0] for call in run.call_args_list]
        self.assertTrue(all("--write" not in command for command in commands))
        self.assertEqual(commands[0][-2:], ("lint", "skills"))
        self.assertEqual(commands[1][-1], "--check")
        self.assertEqual(commands[2][-1], "--check")
        self.assertEqual(commands[3][-1], "--check")


if __name__ == "__main__":
    unittest.main()
