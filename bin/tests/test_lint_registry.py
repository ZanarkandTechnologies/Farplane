from __future__ import annotations

import unittest
from pathlib import Path

from bin.core.lint.models import LintContext, LintSpec
from bin.core.lint.registry import LintRegistry, build_registry
from bin.core.lint.runner import lint


ROOT = Path(__file__).resolve().parents[2]


class LintRegistryTests(unittest.TestCase):
    def test_changed_paths_select_only_their_contracts_plus_source_syntax(self) -> None:
        checks = build_registry().select(
            scope="all",
            changed_paths=("docs/features/FEAT-0039.md",),
        )
        ids = {check.check_id for check in checks}

        self.assertIn("feature_and_system_records", ids)
        self.assertIn("source_yaml_json_syntax", ids)
        self.assertNotIn("skill_contract", ids)
        self.assertNotIn("project_contract", ids)

    def test_runner_refuses_write_arguments_even_if_a_bad_spec_is_registered(self) -> None:
        registry = LintRegistry(
            (
                LintSpec(
                    "bad_writer",
                    frozenset({"project"}),
                    ("example.yaml",),
                    command=lambda _context: ("bad-tool", "--write"),
                ),
            )
        )

        results = lint(
            registry,
            LintContext(ROOT, changed=True, paths=("example.yaml",)),
            "project",
        )

        self.assertEqual(len(results), 1)
        self.assertFalse(results[0].ok)
        self.assertIn("rejected write arguments", results[0].output)


if __name__ == "__main__":
    unittest.main()
