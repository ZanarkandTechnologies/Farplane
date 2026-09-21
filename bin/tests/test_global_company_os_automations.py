from __future__ import annotations

import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


class GlobalCompanyOSAutomationTests(unittest.TestCase):
    def test_root_owns_exactly_two_global_company_os_automations(self) -> None:
        automation_dir = ROOT / "automations"
        files = sorted(automation_dir.glob("*.md"))
        self.assertEqual(
            [path.name for path in files],
            ["daily-operating-update.md", "weekly-operating-review.md"],
        )

        expected = {
            "daily-operating-update": ("farplane-daily-interval", (
                "## 1. Fetch all context",
                "## 2. Save one context list per Project",
                "## 3. Run PM Daily",
                "## 4. Render memory and apply JSON actions",
                "farplane/harness.yaml",
                "read back the issue and returned revision",
            )),
            "weekly-operating-review": ("farplane-weekly-interval", (
                "## 1. Freeze the weekly input",
                "## 2. Run PM Weekly",
                "## 3. Verify the JSON handoff",
                "## 4. Render and propagate authorized artifacts",
                "represented Project set to equal the eligible frozen inventory",
                "Never create, assign, close, start, dispatch, or execute Work",
            )),
        }
        for path in files:
            front_matter, body = path.read_text(encoding="utf-8").split("\n---\n", 1)
            record = yaml.safe_load(front_matter[4:])
            self.assertEqual(record["schema"], "farplane_project_automation")
            self.assertEqual(record["kind"], "cron")
            expected_id, clauses = expected[path.stem]
            self.assertEqual(record["id"], expected_id)
            self.assertTrue(all(clause in body for clause in clauses))

    def test_project_local_automations_do_not_duplicate_global_reviews(self) -> None:
        names = {path.name for path in (ROOT / "farplane" / "automations").glob("*.md")}
        self.assertNotIn("daily-operating-update.md", names)
        self.assertNotIn("weekly-operating-review.md", names)

    def test_installed_advisor_resolves_prompts_from_explicit_office_root(self) -> None:
        template = (ROOT / "skills/automation-advisor/templates/company-os-automation.md").read_text()
        self.assertIn("<office-root>/automations/daily-operating-update.md", template)
        self.assertIn("<office-root>/automations/weekly-operating-review.md", template)
        self.assertNotIn("../../../automations/", template)


if __name__ == "__main__":
    unittest.main()
