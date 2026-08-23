from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "check_skill_ensembles",
    ROOT / "bin" / "validators" / "check_skill_ensembles.py",
)
assert SPEC and SPEC.loader
check_skill_ensembles = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(check_skill_ensembles)


def write_ensemble(root: Path, content: str) -> None:
    path = root / "skills" / "advisor" / "ensemble.yaml"
    path.parent.mkdir(parents=True)
    path.write_text(content, encoding="utf-8")


class SkillEnsembleLintTests(unittest.TestCase):
    def test_loads_complete_personas(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ensemble(
                root,
                """version: 1
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
""",
            )

            rows = check_skill_ensembles.load_skill_ensembles(root)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1]["personas"][0]["id"], "operator")

    def test_rejects_duplicate_persona_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ensemble(
                root,
                """version: 1
personas:
  - id: operator
    name: Operator
    prompt: Optimize for the operator.
    focus: [value]
  - id: operator
    name: Duplicate operator
    prompt: Duplicate prompt.
    focus: [risk]
  - id: skeptic
    name: Skeptic
    prompt: Look for unsupported claims.
    focus: [evidence]
""",
            )

            with self.assertRaisesRegex(ValueError, "persona ids must not contain duplicates"):
                check_skill_ensembles.load_skill_ensembles(root)

    def test_rejects_incomplete_persona(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ensemble(
                root,
                """version: 1
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
""",
            )

            with self.assertRaisesRegex(ValueError, "focus: Field required"):
                check_skill_ensembles.load_skill_ensembles(root)


if __name__ == "__main__":
    unittest.main()
