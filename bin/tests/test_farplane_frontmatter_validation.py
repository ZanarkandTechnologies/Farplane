from __future__ import annotations

import sys
import unittest
from pathlib import Path


BIN_DIR = Path(__file__).resolve().parents[1]
if str(BIN_DIR) not in sys.path:
    sys.path.insert(0, str(BIN_DIR))

import farplane
from farplane_cli_base import CORE_ROOT
from farplane_cli_commands import frontmatter_validation_commands


class FarplaneFrontmatterValidationTests(unittest.TestCase):
    def test_parser_defaults_frontmatter_validation_to_all(self) -> None:
        args = farplane.build_parser().parse_args(["validate", "frontmatter"])

        self.assertEqual(args.scope, "all")

    def test_skill_scope_uses_only_the_skill_contract_validator(self) -> None:
        checks = frontmatter_validation_commands(CORE_ROOT, "skills")

        self.assertEqual(
            [check_id for check_id, _command in checks],
            ["skill_contract", "skill_ensembles"],
        )

    def test_document_scope_routes_each_document_metadata_owner(self) -> None:
        checks = frontmatter_validation_commands(CORE_ROOT, "docs")

        self.assertEqual(
            [check_id for check_id, _command in checks],
            [
                "document_frontmatter_syntax",
                "feature_and_system_records",
                "template_registry",
                "template_metadata",
                "source_registry",
            ],
        )


if __name__ == "__main__":
    unittest.main()
