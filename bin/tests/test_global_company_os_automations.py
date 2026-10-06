from __future__ import annotations

import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


class GlobalCompanyOSAutomationTests(unittest.TestCase):
    def test_configured_office_reviews_preserve_identity_and_contract(self) -> None:
        automation_dir = ROOT / "farplane" / "automations"
        files = [automation_dir / "steps/daily-operating-update.md", automation_dir / "report-gen.md"]

        expected = {
            "daily-operating-update": ("farplane-daily-interval", (
                "## 1. Load today's collected context",
                "## 2. Confirm coverage per Project",
                "## 3. Run Progress Update",
                "## 4. Render memory and apply JSON actions",
                "farplane/harness.yaml",
                "read back the issue and returned revision",
                "gh issue comment <n> -R <owner/repo>",
                "github_writes: <n comments | none>",
                "Check-ins",
            )),
            "report-gen": ("farplane-weekly-interval", (
                "## 1. Freeze the weekly input",
                "## 2. Run Report Gen",
                "## 3. Verify the JSON handoff",
                "## 4. Render and propagate authorized artifacts",
                "represented Project set to equal the eligible frozen inventory",
                "Never create, assign, close, start, dispatch, or execute Work",
                "engineering facts only",
                "github_writes: <n comments | none>",
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

    def test_daily_collect_owns_fetching_and_writes_run_marker(self) -> None:
        body = (ROOT / "farplane/automations/steps/daily-collect.md").read_text(encoding="utf-8")
        for clause in ("## 1. Fetch shared sources once", "Agent sessions", "Operator plan",
                       "_run.json", "Read providers only", "~/.farplane/company.json",
                       "gh issue list", "issues/comments?since=", "`check-in`",
                       "Multica is archived read-only; don't read or write it."):
            self.assertIn(clause, body)
        daily = (ROOT / "farplane/automations/steps/daily-operating-update.md").read_text(encoding="utf-8")
        self.assertIn("Never fall back to fetching in this automation.", daily)

    def test_all_configured_automations_are_discoverable_once(self) -> None:
        from bin.core.farplane_project_snapshot import load_automations
        records, gaps = load_automations(ROOT)
        self.assertEqual(gaps, [])
        ids = [row["id"] for row in records]
        self.assertEqual(ids.count("farplane-morning"), 1)
        self.assertEqual(ids.count("farplane-weekly-interval"), 1)
        self.assertNotIn("farplane-daily-collect", ids)  # steps are called by jobs, never listed as jobs
        self.assertEqual(len(ids), len(set(ids)))

    def test_installed_advisor_resolves_prompts_from_explicit_office_root(self) -> None:
        template = (ROOT / "skills/automation-advisor/templates/company-os-automation.md").read_text()
        self.assertIn("<office-root>/farplane/automations/steps/daily-operating-update.md", template)
        self.assertIn("<office-root>/farplane/automations/report-gen.md", template)


if __name__ == "__main__":
    unittest.main()
