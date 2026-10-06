from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class BookmarkRecoveryAutomationTests(unittest.TestCase):
    def test_record_calls_one_skill_and_preserves_boundaries(self) -> None:
        prompt = (ROOT / "farplane/automations/steps/bookmark-recovery.md").read_text(encoding="utf-8").split("---\n", 2)[2]
        self.assertEqual(prompt.count("$bookmark-recovery"), 2)
        self.assertNotIn("$progress-update", prompt)
        self.assertIn("provider_mutations: 0", prompt)
        self.assertIn("resource_bank_writes: 0", prompt)
        self.assertIn("project_memory_writes: 0", prompt)
        self.assertIn("github_writes: none", prompt)
        self.assertIn("Read X only through the operator's logged-in browser", prompt)
        self.assertIn("never operate the provider UI as fallback", prompt)
        self.assertIn("Never use post creation time as bookmark-save time", prompt)
        self.assertIn("update_ledger.py", prompt)
        self.assertIn("append-only observation history", prompt)
        self.assertIn("project-memory.sources.json", prompt)
        self.assertIn("schema-v2 output", prompt)
        self.assertIn("project_matches[]", prompt)
        self.assertIn("addresses_constraint", prompt)


if __name__ == "__main__":
    unittest.main()
