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
            (folder / "work-pulse.toml").write_text(
                'id = "pulse"\nname = "Work Pulse"\nkind = "heartbeat"\nstatus = "active"\n',
                encoding="utf-8",
            )
            (folder / "daily.toml").write_text(
                'id = "daily"\nname = "Daily"\nkind = "cron"\nstatus = "paused"\n',
                encoding="utf-8",
            )

            records, gaps = load_automations(root)

        self.assertEqual(gaps, [])
        self.assertEqual([record["id"] for record in records], ["daily", "pulse"])
        self.assertEqual(records[1]["source_ref"]["path"], "farplane/automations/work-pulse.toml")


if __name__ == "__main__":
    unittest.main()
