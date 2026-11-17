"""What the Stop gate runs when nothing is configured (17 Nov 2026)."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("stop_gate_defaults", ROOT / "hooks/stop-gate/stop_gate.py")
stop_gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stop_gate)


class DefaultChecksTests(unittest.TestCase):
    def test_by_default_no_check_polices_the_wording(self):
        # Kenji, 17 Nov 2026: "cover the topline in the agents.md and dont cature
        # bottom line with the hooks" (1,112 length and format send-backs that week).
        self.assertEqual(stop_gate.configured_checks({}), frozenset({"spec", "notes", "continuation"}))
        payload = {"hook_event_name": "Stop", "last_assistant_message": "word " * 600}
        with patch.object(stop_gate, "load_runtime_env", return_value={}), \
                patch.object(stop_gate, "operator_asleep", return_value=False), \
                patch.object(stop_gate, "jev_gate") as jev:
            self.assertIsNone(stop_gate.run_gate(payload))
        jev.assert_not_called()

    def test_keep_working_push_runs_only_while_the_operator_is_asleep(self):
        payload = {"hook_event_name": "Stop", "last_assistant_message": "word " * 600}
        with patch.object(stop_gate, "load_runtime_env", return_value={}), \
                patch.object(stop_gate, "operator_asleep", return_value=True), \
                patch.object(stop_gate, "jev_gate", return_value=None) as jev:
            stop_gate.run_gate(payload)
        sent, checks = jev.call_args.args[0], jev.call_args.args[1]
        self.assertEqual(checks, frozenset({"continuation"}))
        # No length check will block, so the push must not wait for one.
        self.assertTrue(sent[stop_gate.LENGTH_CAPPED_KEY])

    def test_asleep_is_read_from_the_evidence_switch(self):
        with tempfile.TemporaryDirectory() as folder, \
                patch.object(stop_gate.evidence, "STATE", Path(folder)):
            for mode, asleep in (("asleep", True), ("awake", False)):
                (Path(folder) / "mode").write_text(mode + "\n")
                self.assertEqual(stop_gate.operator_asleep(), asleep)
        with patch.object(stop_gate.evidence, "resolve", side_effect=OSError):
            self.assertFalse(stop_gate.operator_asleep())


if __name__ == "__main__":
    unittest.main()
