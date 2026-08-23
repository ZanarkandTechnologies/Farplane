from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VALIDATORS_DIR = ROOT / "bin" / "validators"
if str(VALIDATORS_DIR) not in sys.path:
    sys.path.insert(0, str(VALIDATORS_DIR))

import sync_skill_registry as registry


class MethodContractRegistryTests(unittest.TestCase):
    def test_parses_and_normalizes_structured_method_contracts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "SKILL.md"
            path.write_text(
                """---
name: alpha
methods:
  - id: alpha:report
    class: artifact
    output: research-report
  - id: alpha:publish
    class: integration
    output: publish-receipt
---
""",
                encoding="utf-8",
            )
            metadata = registry.parse_skill_frontmatter(path)

        self.assertEqual(
            registry.normalize_method_contracts(metadata["methods"], "alpha", path),
            [
                {"id": "alpha:report", "class": "artifact", "output": "research-report"},
                {"id": "alpha:publish", "class": "integration", "output": "publish-receipt"},
            ],
        )

    def test_rejects_legacy_method_strings_and_cross_owner_ids(self) -> None:
        path = Path("skills/alpha/SKILL.md")
        with self.assertRaisesRegex(registry.RegistryError, "list of mappings"):
            registry.normalize_method_contracts(["alpha:report"], "alpha", path)
        with self.assertRaisesRegex(registry.RegistryError, "must start with alpha:"):
            registry.normalize_method_contracts(
                [{"id": "beta:report", "class": "artifact", "output": "report"}],
                "alpha",
                path,
            )


if __name__ == "__main__":
    unittest.main()
