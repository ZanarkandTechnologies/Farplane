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

        self.assertEqual(len(files), 6)
        self.assertTrue(all(record["schema"] == "farplane_project_automation" for record in records))
        self.assertEqual(sum(record["kind"] == "heartbeat" for record in records), 1)
        self.assertEqual(len({record["id"] for record in records}), len(records))


if __name__ == "__main__":
    unittest.main()
