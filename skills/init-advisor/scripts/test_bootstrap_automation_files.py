from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


class BootstrapAutomationFilesTests(unittest.TestCase):
    def test_bootstrap_starts_with_no_jobs(self) -> None:
        skill_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                ["bash", str(skill_root / "scripts" / "bootstrap.sh"), tmp],
                check=True,
                capture_output=True,
                text=True,
            )
            folder = Path(tmp) / "farplane" / "automations"
            self.assertTrue(folder.is_dir())
            self.assertEqual(list(folder.glob("*.md")), [])


if __name__ == "__main__":
    unittest.main()
