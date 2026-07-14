from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("plan_wave_guard.py")
SPEC = importlib.util.spec_from_file_location("plan_wave_guard", MODULE_PATH)
assert SPEC and SPEC.loader
guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guard)


class PlanWaveGuardTests(unittest.TestCase):
    @staticmethod
    def semantic_time_state(**overrides: object) -> dict[str, object]:
        state: dict[str, object] = {
            "metric_freshness": {"reach": "fresh"},
            "goal_urgency": {"reach-goal": "on_track"},
            "matured_reward_ids": [],
            "operator_availability": {"state": "unavailable", "validity": "current"},
        }
        state.update(overrides)
        return state

    def test_semantic_fingerprint_ignores_as_of_and_temp_receipt_path_churn(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            receipt_a = root / ".farplane" / "tmp" / "history-1000.json"
            receipt_b = root / ".farplane" / "tmp" / "history-1030.json"
            receipt_a.parent.mkdir(parents=True)
            history = {"rows": [{"ticket_id": "TASK-1", "decision": "accept"}]}
            receipt_a.write_text(json.dumps(history), encoding="utf-8")
            receipt_b.write_text(json.dumps(history, indent=2), encoding="utf-8")
            first_input = {
                "as_of": "2026-07-14T10:00:00Z",
                "history_query": {"ref": ".farplane/tmp/history-1000.json", "limit": 20},
                "goals": [{"metric_id": "reach", "target_value": 100}],
                "semantic_time_state": self.semantic_time_state(),
            }
            second_input = {
                "as_of": "2026-07-14T10:30:00Z",
                "history_query": {"ref": ".farplane/tmp/history-1030.json", "limit": 20},
                "goals": [{"metric_id": "reach", "target_value": 100}],
                "semantic_time_state": self.semantic_time_state(),
            }

            first = guard.begin_wave(root, first_input, 1)
            guard.finish_wave(root, first["claim_id"], "no_op", [], {}, admitted_lanes={})
            retry = guard.begin_wave(root, second_input, 1)

            self.assertEqual(retry["status"], "no_op_unchanged_input")
            self.assertEqual(
                first["planning_fingerprint"], retry["planning_fingerprint"]
            )

    def test_semantic_time_boundaries_each_invalidate_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            baseline = {
                "as_of": "2026-07-14T10:00:00Z",
                "semantic_time_state": self.semantic_time_state(),
            }
            baseline_fingerprint = guard.semantic_planning_fingerprint(root, baseline)
            states = {
                "metric_becomes_stale": self.semantic_time_state(
                    metric_freshness={"reach": "stale"}
                ),
                "goal_enters_deadline_bucket": self.semantic_time_state(
                    goal_urgency={"reach-goal": "due_within_24h"}
                ),
                "delayed_checkin_matures": self.semantic_time_state(
                    matured_reward_ids=["reach-checkin-7d"]
                ),
                "operator_availability_expires": self.semantic_time_state(
                    operator_availability={"state": "unavailable", "validity": "expired"}
                ),
            }
            for name, state in states.items():
                with self.subTest(name=name):
                    changed = {**baseline, "as_of": "2026-07-14T10:30:00Z", "semantic_time_state": state}
                    self.assertNotEqual(
                        baseline_fingerprint,
                        guard.semantic_planning_fingerprint(root, changed),
                    )

    def test_legacy_as_of_remains_semantic_when_derived_state_is_absent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = {"as_of": "2026-07-14T10:00:00Z", "metrics": {"reach": 10}}
            later = {"as_of": "2026-07-14T10:30:00Z", "metrics": {"reach": 10}}

            self.assertNotEqual(
                guard.semantic_planning_fingerprint(root, first),
                guard.semantic_planning_fingerprint(root, later),
            )

    def test_explicit_semantic_time_state_requires_all_boundary_classes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "matured_reward_ids"):
                guard.semantic_planning_fingerprint(
                    Path(tmp),
                    {
                        "semantic_time_state": {
                            "metric_freshness": {},
                            "goal_urgency": {},
                            "operator_availability": {},
                        }
                    },
                )

    def test_semantic_fingerprint_changes_for_each_planning_signal_class(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            receipt = root / ".farplane" / "tmp" / "history.json"
            receipt.parent.mkdir(parents=True)
            receipt.write_text(
                json.dumps({"rows": [{"ticket_id": "TASK-1", "decision": "accept"}]}),
                encoding="utf-8",
            )
            baseline = {
                "metrics": {"reach": 10},
                "goals": [{"metric_id": "reach", "target_value": 100}],
                "board": {"idle_worker_slots": 4, "review_wip": 2},
                "evidence_ref": "reports/proof-a.md",
                "history_query": {"ref": ".farplane/tmp/history.json"},
            }
            baseline_fingerprint = guard.semantic_planning_fingerprint(root, baseline)
            variants = [
                {**baseline, "metrics": {"reach": 11}},
                {**baseline, "goals": [{"metric_id": "reach", "target_value": 200}]},
                {**baseline, "board": {"idle_worker_slots": 3, "review_wip": 2}},
                {**baseline, "evidence_ref": "reports/proof-b.md"},
            ]
            for variant in variants:
                with self.subTest(variant=variant):
                    self.assertNotEqual(
                        baseline_fingerprint,
                        guard.semantic_planning_fingerprint(root, variant),
                    )

            receipt.write_text(
                json.dumps({"rows": [{"ticket_id": "TASK-1", "decision": "kill"}]}),
                encoding="utf-8",
            )
            self.assertNotEqual(
                baseline_fingerprint,
                guard.semantic_planning_fingerprint(root, baseline),
            )

    def test_overlap_is_blocked_and_changed_input_can_follow_completion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = guard.begin_wave(root, {"tickets": [], "metric": 0}, 2)
            overlap = guard.begin_wave(root, {"tickets": [], "metric": 1}, 2)
            self.assertEqual(first["status"], "acquired")
            self.assertEqual(overlap["status"], "blocked_overlap")
            result = guard.finish_wave(root, first["claim_id"], "completed", ["TASK-0001"], {"TASK-0001": "delivery"}, admitted_lanes={"TASK-0001": "experiment"})
            self.assertEqual(result["admitted_specs"][0]["ranking"]["lane"], "experiment")
            changed = guard.begin_wave(root, {"tickets": [], "metric": 1}, 2)
            self.assertEqual(changed["status"], "acquired")

    def test_identical_completed_input_is_no_op(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            planning_input = {"tickets": ["TASK-0001"], "metric": 2}
            first = guard.begin_wave(root, planning_input, 1)
            guard.finish_wave(root, first["claim_id"], "completed", ["TASK-0002"], {"TASK-0002": "delivery"}, admitted_lanes={"TASK-0002": "delivery"})
            retry = guard.begin_wave(root, planning_input, 1)
            self.assertEqual(retry["status"], "no_op_unchanged_input")
            self.assertEqual(retry["no_op_category"], "unchanged_planning_fingerprint")

    def test_finish_enforces_wave_cap_and_unique_ticket_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = guard.begin_wave(root, {"metric": 0}, 1)
            with self.assertRaisesRegex(ValueError, "exceeds wave_size"):
                guard.finish_wave(root, first["claim_id"], "completed", ["TASK-1", "TASK-2"], {"TASK-1": "a", "TASK-2": "b"}, admitted_lanes={"TASK-1": "delivery", "TASK-2": "experiment"})
            with self.assertRaisesRegex(ValueError, "duplicate admitted"):
                guard.finish_wave(root, first["claim_id"], "completed", ["TASK-1", "TASK-1"], {"TASK-1": "a"}, admitted_lanes={"TASK-1": "delivery"})
            with self.assertRaisesRegex(ValueError, "selected lane"):
                guard.finish_wave(root, first["claim_id"], "completed", ["TASK-1"], {"TASK-1": "a"})
            guard.finish_wave(root, first["claim_id"], "completed", ["TASK-1"], {"TASK-1": "a"}, admitted_lanes={"TASK-1": "delivery"})
            second = guard.begin_wave(root, {"metric": 1}, 1)
            with self.assertRaisesRegex(ValueError, "already admitted"):
                guard.finish_wave(root, second["claim_id"], "completed", ["TASK-1"], {"TASK-1": "a"}, admitted_lanes={"TASK-1": "delivery"})


if __name__ == "__main__":
    unittest.main()
