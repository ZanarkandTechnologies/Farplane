from __future__ import annotations

import subprocess
import os
import shutil
import tempfile
import unittest
from pathlib import Path

import yaml


class BootstrapAutomationFilesTests(unittest.TestCase):
    def test_bootstrap_copies_one_complete_file_per_automation(self) -> None:
        skill_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                ["bash", str(skill_root / "scripts" / "bootstrap.sh"), tmp],
                check=True,
                capture_output=True,
                text=True,
            )
            files = sorted((Path(tmp) / "farplane" / "automations").glob("*.md"))
            records = [yaml.safe_load(path.read_text(encoding="utf-8").split("\n---\n", 1)[0][4:]) for path in files]
            names = {path.name for path in files}

        self.assertEqual(len(files), 4)
        self.assertTrue(all(record["schema"] == "farplane_project_automation" for record in records))
        self.assertEqual(sum(record["kind"] == "heartbeat" for record in records), 1)
        self.assertEqual(len({record["id"] for record in records}), len(records))
        self.assertEqual(
            names,
            {
                "feed-scout.md",
                "monthly-registry-consolidation.md",
                "weekly-self-improvement.md",
                "work-pulse.md",
            },
        )
        self.assertNotIn("daily-collect.md", names)
        self.assertNotIn("daily-operating-update.md", names)
        self.assertNotIn("weekly-operating-review.md", names)

    def test_office_bootstrap_adds_reviews_and_preserves_customized_record(self) -> None:
        skill_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            command = ["bash", str(skill_root / "scripts/bootstrap.sh"), "--office", tmp]
            subprocess.run(command, check=True, capture_output=True)
            folder = Path(tmp) / "farplane/automations"
            self.assertEqual(len(list(folder.glob("*.md"))), 7)
            daily = folder / "daily-operating-update.md"
            self.assertIn("source_template: automations/daily-operating-update.md", daily.read_text())
            daily.write_text(daily.read_text() + "\nOperator customization.\n")
            expected = daily.read_bytes()
            subprocess.run(command, check=True, capture_output=True)
            self.assertEqual(daily.read_bytes(), expected)

    def test_installed_copy_resolves_recipes_from_installed_cli(self) -> None:
        skill_root = Path(__file__).resolve().parents[1]
        repo = skill_root.parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            installed = root / "codex/skills/init-advisor"
            (installed / "scripts").mkdir(parents=True)
            shutil.copy2(skill_root / "scripts/bootstrap.sh", installed / "scripts/bootstrap.sh")
            (installed / "references").symlink_to(skill_root / "references", target_is_directory=True)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            (bin_dir / "farplane").symlink_to(repo / "bin/farplane")
            target = root / "project"
            target.mkdir()
            env = {**os.environ, "PATH": str(bin_dir) + os.pathsep + os.environ["PATH"]}
            subprocess.run(["bash", str(installed / "scripts/bootstrap.sh"), str(target)],
                           check=True, capture_output=True, env=env)
            self.assertTrue((target / "farplane/automations/work-pulse.md").is_file())


if __name__ == "__main__":
    unittest.main()
