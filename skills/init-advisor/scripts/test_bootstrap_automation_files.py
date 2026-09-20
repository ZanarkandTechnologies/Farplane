from __future__ import annotations

import subprocess
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
            prompts = {
                path.stem: path.read_text(encoding="utf-8").split("\n---\n", 1)[1]
                for path in files
            }

        self.assertEqual(len(files), 6)
        self.assertTrue(all(record["schema"] == "farplane_project_automation" for record in records))
        self.assertEqual(sum(record["kind"] == "heartbeat" for record in records), 1)
        self.assertEqual(len({record["id"] for record in records}), len(records))

        self.assertTrue(
            all(
                clause in prompts["daily-operating-update"]
                for clause in (
                    "## 1. Fetch all context",
                    "## 2. Save one context list per Project",
                    "## 3. Run PM Daily",
                    "## 4. Render memory and apply JSON actions",
                    "farplane/harness.yaml",
                    "expected revision",
                    "read back the issue and returned revision",
                    "`applied`, `duplicate`, `blocked`, or `failed`",
                )
            )
        )
        self.assertTrue(
            all(
                clause in prompts["weekly-operating-review"]
                for clause in (
                    "## 1. Freeze the weekly input",
                    "## 2. Run PM Weekly",
                    "## 3. Verify the JSON handoff",
                    "## 4. Render and propagate authorized artifacts",
                    "represented Project set to equal the eligible frozen inventory",
                    "Compare every existing output with its frozen original",
                    "Never create, assign, close, start, dispatch, or execute Work",
                    "every changed field plus the returned revision",
                )
            )
        )


if __name__ == "__main__":
    unittest.main()
