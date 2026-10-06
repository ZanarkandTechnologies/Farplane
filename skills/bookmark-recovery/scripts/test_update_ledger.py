from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("update_ledger.py")
SPEC = importlib.util.spec_from_file_location("update_ledger", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class UpdateLedgerTests(unittest.TestCase):
    def test_two_runs_preserve_first_seen_and_retry_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            inbox = root / "inbox.json"
            ledger = root / "ledger.jsonl"
            base = {
                "run_id": "run-1", "generated_at": "2026-09-20T00:00:00Z",
                "candidates": [{"canonical_key": "x:1", "source": "x"}],
                "duplicates": [], "excluded": [],
            }
            inbox.write_text(json.dumps(base), encoding="utf-8")
            self.assertEqual(MODULE.append_observations(inbox, ledger)["appended"], 1)
            self.assertEqual(MODULE.append_observations(inbox, ledger)["appended"], 0)
            base.update({
                "run_id": "run-2", "generated_at": "2026-09-21T00:00:00Z",
                "candidates": [],
                "duplicates": [{"canonical_key": "x:1", "source": "x", "reason": "seen"}],
            })
            inbox.write_text(json.dumps(base), encoding="utf-8")
            self.assertEqual(MODULE.append_observations(inbox, ledger)["appended"], 1)
            rows = MODULE.read_rows(ledger)
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[1]["first_seen"], "2026-09-20T00:00:00Z")
            self.assertEqual(rows[1]["last_seen"], "2026-09-21T00:00:00Z")


if __name__ == "__main__":
    unittest.main()
