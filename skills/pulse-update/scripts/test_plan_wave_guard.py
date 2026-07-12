from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("plan_wave_guard.py")
SPEC = importlib.util.spec_from_file_location("plan_wave_guard", MODULE_PATH)
assert SPEC and SPEC.loader
guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guard)


class PlanWaveGuardTests(unittest.TestCase):
    def test_overlap_is_blocked_and_changed_input_can_follow_completion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = guard.begin_wave(root, {"tickets": [], "metric": 0}, 2)
            overlap = guard.begin_wave(root, {"tickets": [], "metric": 1}, 2)
            self.assertEqual(first["status"], "acquired")
            self.assertEqual(overlap["status"], "blocked_overlap")
            guard.finish_wave(root, first["claim_id"], "completed", ["TASK-0001"], {"TASK-0001": "delivery"})
            changed = guard.begin_wave(root, {"tickets": [], "metric": 1}, 2)
            self.assertEqual(changed["status"], "acquired")

    def test_identical_completed_input_is_no_op(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            planning_input = {"tickets": ["TASK-0001"], "metric": 2}
            first = guard.begin_wave(root, planning_input, 1)
            guard.finish_wave(root, first["claim_id"], "completed", ["TASK-0002"], {"TASK-0002": "delivery"})
            retry = guard.begin_wave(root, planning_input, 1)
            self.assertEqual(retry["status"], "no_op_unchanged_input")
            self.assertEqual(retry["no_op_category"], "unchanged_planning_fingerprint")

    def test_finish_enforces_wave_cap_and_unique_ticket_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = guard.begin_wave(root, {"metric": 0}, 1)
            with self.assertRaisesRegex(ValueError, "exceeds wave_size"):
                guard.finish_wave(root, first["claim_id"], "completed", ["TASK-1", "TASK-2"], {"TASK-1": "a", "TASK-2": "b"})
            with self.assertRaisesRegex(ValueError, "duplicate admitted"):
                guard.finish_wave(root, first["claim_id"], "completed", ["TASK-1", "TASK-1"], {"TASK-1": "a"})
            guard.finish_wave(root, first["claim_id"], "completed", ["TASK-1"], {"TASK-1": "a"})
            second = guard.begin_wave(root, {"metric": 1}, 1)
            with self.assertRaisesRegex(ValueError, "already admitted"):
                guard.finish_wave(root, second["claim_id"], "completed", ["TASK-1"], {"TASK-1": "a"})


if __name__ == "__main__":
    unittest.main()
