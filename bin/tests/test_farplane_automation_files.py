from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = ROOT / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from farplane_project_snapshot import load_automations


class AutomationFileTests(unittest.TestCase):
    def test_loads_one_record_per_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "farplane" / "automations"
            folder.mkdir(parents=True)
            (folder / "work-pulse.md").write_text(
                '---\nid: pulse\nname: Work Pulse\nkind: heartbeat\nstatus: active\n---\nUse $pulse-update.\n',
                encoding="utf-8",
            )
            (folder / "daily.md").write_text(
                '---\nid: daily\nname: Daily\nkind: cron\nstatus: paused\n---\nUse $progress-update.\n',
                encoding="utf-8",
            )

            records, gaps = load_automations(root)

        self.assertEqual(gaps, [])
        self.assertEqual([record["id"] for record in records], ["daily", "pulse"])
        self.assertEqual(records[1]["source_ref"]["path"], "farplane/automations/work-pulse.md")

    def test_configured_automations_name_github_task_record(self) -> None:
        folder = ROOT / "farplane" / "automations"
        for name in ("feed-scout", "work-pulse", "weekly-self-improvement",
                     "monthly-registry-consolidation", "weekly-thread-friction-audit"):
            text = (folder / f"{name}.md").read_text(encoding="utf-8")
            self.assertIn("Task record: GitHub Issues of each project's repo", text)
            self.assertNotIn("Multica CLI", text)

    def test_reports_invalid_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "farplane" / "automations"
            folder.mkdir(parents=True)
            (folder / "broken.md").write_text("missing front matter\n", encoding="utf-8")

            records, gaps = load_automations(root)

        self.assertEqual(records, [])
        self.assertEqual(gaps, ["invalid_automation_markdown:broken.md"])

    def test_recipe_is_not_exposed_as_configured_automation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / "farplane/automations"
            folder.mkdir(parents=True)
            (folder / "recipe.md").write_text(
                "---\nschema: farplane_automation_recipe\nid: example\n---\nUse $progress-update.\n")
            records, gaps = load_automations(Path(tmp))
        self.assertEqual(records, [])
        self.assertEqual(gaps, ["unconfigured_automation_recipe:recipe.md"])


if __name__ == "__main__":
    unittest.main()
