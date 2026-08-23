from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("quick_validate.py")
SPEC = importlib.util.spec_from_file_location("quick_validate", SCRIPT)
assert SPEC and SPEC.loader
quick_validate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(quick_validate)


class QuickValidateCapabilityTests(unittest.TestCase):
    def write_skill(self, root: Path, frontmatter: str) -> Path:
        skill_dir = root / "x-thread"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            f"---\n{frontmatter}\n---\n\n# X Thread\n",
            encoding="utf-8",
        )
        return skill_dir

    def test_accepts_the_shared_artifact_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = self.write_skill(
                Path(tmp),
                """name: x-thread
description: Create a review-ready X thread draft.
tier: 3
source: local
group: marketing
capability:
  kind: artifact
  consumes: [content-brief]
  produces: [x-thread-draft]""",
            )

            valid, message = quick_validate.validate_skill(skill_dir)

            self.assertTrue(valid, message)

    def test_rejects_retired_portfolio_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = self.write_skill(
                Path(tmp),
                """name: x-thread
description: Create a review-ready X thread draft.
tier: 3
source: local
group: marketing
portfolio: domain
capability:
  kind: artifact
  produces: [x-thread-draft]""",
            )

            valid, message = quick_validate.validate_skill(skill_dir)

            self.assertFalse(valid)
            self.assertIn("portfolio", message)


if __name__ == "__main__":
    unittest.main()
