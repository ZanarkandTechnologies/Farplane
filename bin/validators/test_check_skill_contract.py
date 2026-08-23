from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "check_skill_frontmatter",
    ROOT / "bin" / "validators" / "check_skill_frontmatter.py",
)
assert SPEC and SPEC.loader
check_skill_frontmatter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_skill_frontmatter)


def write_skill(root: Path) -> Path:
    path = root / "skills" / "advisor" / "SKILL.md"
    path.parent.mkdir(parents=True)
    path.write_text(
        """---
name: advisor
description: A test skill.
tier: 1
source: local
---

# Advisor
""",
        encoding="utf-8",
    )
    return path


VALID_ENSEMBLE = """version: 1
personas:
    - id: operator
      name: Operator
      prompt: Optimize for the operator.
      focus: [value]
    - id: engineer
      name: Engineer
      prompt: Optimize for safe implementation.
      focus: [risk]
    - id: skeptic
      name: Skeptic
      prompt: Look for unsupported claims.
      focus: [evidence]
"""


class SkillContractLintTests(unittest.TestCase):
    def test_lints_complete_frontmatter_and_optional_ensemble_through_one_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_skill(root)
            (root / "skills" / "advisor" / "ensemble.yaml").write_text(
                VALID_ENSEMBLE,
                encoding="utf-8",
            )

            frontmatter_rows = check_skill_frontmatter.load_skill_contracts(root)
            ensemble_rows = check_skill_frontmatter.load_skill_ensembles(root)
            report = check_skill_frontmatter.ensemble_contract_report(ensemble_rows)

        self.assertEqual(len(frontmatter_rows), 1)
        self.assertEqual(ensemble_rows[0][1]["personas"][0]["id"], "operator")
        self.assertEqual(report, {"ensemble_packages": 1, "ensemble_personas": 3})

    def test_rejects_duplicate_persona_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_skill(root)
            (root / "skills" / "advisor" / "ensemble.yaml").write_text(
                VALID_ENSEMBLE.replace("- id: engineer", "- id: operator"),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "persona ids must not contain duplicates"):
                check_skill_frontmatter.load_skill_ensembles(root)

    def test_rejects_incomplete_persona(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_skill(root)
            (root / "skills" / "advisor" / "ensemble.yaml").write_text(
                VALID_ENSEMBLE.replace("      focus: [evidence]\n", ""),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "focus: Field required"):
                check_skill_frontmatter.load_skill_ensembles(root)

    def test_frontmatter_stays_minimal_when_an_optional_ensemble_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_skill(root)
            ensemble_path = root / "skills" / "advisor" / "ensemble.yaml"
            ensemble_path.write_text(VALID_ENSEMBLE, encoding="utf-8")

            metadata = check_skill_frontmatter.load_skill_contracts(root)[0][1]
            ensembles = check_skill_frontmatter.load_skill_ensembles(root)

        self.assertNotIn("ensemble", metadata)
        self.assertEqual(len(ensembles), 1)


if __name__ == "__main__":
    unittest.main()
