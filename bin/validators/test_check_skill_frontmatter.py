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


def write_skill(root: Path, name: str, capability: str = "") -> None:
    skill_dir = root / "skills" / name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "\n".join(
            [
                "---",
                f"name: {name}",
                "description: Test skill.",
                "tier: 3",
                "group: marketing",
                "source: local",
                capability,
                "---",
                "",
                f"# {name}",
            ]
        ),
        encoding="utf-8",
    )


class SkillFrontmatterLintTests(unittest.TestCase):
    def test_reports_a_declared_artifact_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_skill(
                root,
                "thread-writer",
                """capability:
  kind: artifact
  produces: [x-thread-draft]""",
            )
            skill_dir = root / "skills" / "x-account"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text(
                """---
name: x-account
description: Operate X publishing.
tier: 3
group: marketing
source: local
capability:
  kind: integration
  consumes: [x-thread-draft]
---
""",
                encoding="utf-8",
            )

            report = check_skill_frontmatter.artifact_contract_report(
                check_skill_frontmatter.load_skill_contracts(root)
            )

        self.assertEqual(report["artifact_dependencies"], 1)
        self.assertEqual(report["unresolved_inputs"], {})
        self.assertEqual(report["capability_kinds"], {"artifact": 1, "integration": 1})

    def test_rejects_unknown_frontmatter_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_skill(root, "writer", "invented_field: no")

            with self.assertRaisesRegex(check_skill_frontmatter.FrontmatterLintError, "Extra inputs"):
                check_skill_frontmatter.load_skill_contracts(root)

    def test_rejects_retired_eval_and_qa_frontmatter_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_skill(root, "writer", "eval: evals/evals.json\nqa_checklist: qa_checklist.md")

            with self.assertRaisesRegex(
                check_skill_frontmatter.FrontmatterLintError,
                "retired frontmatter field\\(s\\): eval is derived.*qa_checklist was retired",
            ):
                check_skill_frontmatter.load_skill_contracts(root)

    def test_rejects_retired_qa_sidecar(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_skill(root, "writer")
            (root / "skills" / "writer" / "qa_checklist.md").write_text("- [ ] obsolete\n")

            with self.assertRaisesRegex(check_skill_frontmatter.FrontmatterLintError, "was retired"):
                check_skill_frontmatter.validate_retired_skill_surfaces(root)

    def test_rejects_two_skills_that_claim_the_same_output_family(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            capability = """capability:
  kind: artifact
  produces: [x-thread-draft]"""
            write_skill(root, "writer-one", capability)
            write_skill(root, "writer-two", capability)

            rows = check_skill_frontmatter.load_skill_contracts(root)
            with self.assertRaisesRegex(check_skill_frontmatter.FrontmatterLintError, "one producing skill"):
                check_skill_frontmatter.artifact_contract_report(rows)


if __name__ == "__main__":
    unittest.main()
