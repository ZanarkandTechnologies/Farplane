from __future__ import annotations

import copy
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
                "board": {"held_review_chases": [{"review": {"unanswered_pulse_turns": 22}}]},
                "history_query": {"ref": ".farplane/tmp/history-1000.json", "limit": 20},
                "metric_movement": {"reach": {"current": 10, "previous": 9}},
                "semantic_time_state": self.semantic_time_state(),
            }
            second_input = {
                "as_of": "2026-07-14T10:30:00Z",
                "board": {"held_review_chases": [{"review": {"unanswered_pulse_turns": 23}}]},
                "history_query": {"ref": ".farplane/tmp/history-1030.json", "limit": 20},
                "metric_movement": {"reach": {"current": 10, "previous": 9}},
                "semantic_time_state": self.semantic_time_state(),
            }

            first = guard.begin_wave(root, first_input, 1)
            guard.finish_wave(root, first["claim_id"], "no_op", [], {})
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

    def test_legacy_unanswered_pulse_turns_remains_semantic_without_derived_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = {"board": {"held_review_chases": [{"review": {"unanswered_pulse_turns": 22}}]}}
            later = {"board": {"held_review_chases": [{"review": {"unanswered_pulse_turns": 23}}]}}

            self.assertNotEqual(
                guard.semantic_planning_fingerprint(root, first),
                guard.semantic_planning_fingerprint(root, later),
            )

    def test_board_source_coordinates_and_released_diagnostics_do_not_reopen(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            baseline_board = {
                "active_workers": [],
                "idle_worker_slots": 4,
                "executable_tickets": [],
                "awaiting_review_tickets": [{"ticket_id": "TASK-1"}],
                "human_active_tickets": [{"ticket_id": "TASK-HUMAN"}],
                "due_review_action_count": 1,
                "review_wip": 1,
                "queued_review_pools": [{"pool": "awaiting_review", "count": 1}],
                "held_review_chases": [{"review": {"action": "held_outside_active_hours"}}],
                "ledger": ".farplane/automation/spawned-threads.jsonl",
            }
            with_diagnostics = copy.deepcopy(baseline_board)
            with_diagnostics.pop("ledger")
            with_diagnostics["worker_index"] = ".farplane/state/ticket-thread-associations.jsonl"
            with_diagnostics["released_worker_rows"] = [
                {
                    "ticket_id": "TASK-OLD",
                    "thread_id": "thread-old",
                    "status": "active",
                    "release_reason": "ticket_not_active",
                    "source_event_key": ".farplane/automation/spawned-threads.jsonl:old",
                }
            ]
            first_input = {
                "board": baseline_board,
                "semantic_time_state": self.semantic_time_state(),
            }
            second_input = {
                "board": with_diagnostics,
                "semantic_time_state": self.semantic_time_state(),
            }

            first = guard.begin_wave(root, first_input, 1)
            guard.finish_wave(root, first["claim_id"], "no_op", [], {})
            retry = guard.begin_wave(root, second_input, 1)

            self.assertEqual(retry["status"], "no_op_unchanged_input")
            self.assertEqual(
                first["planning_fingerprint"], retry["planning_fingerprint"]
            )

    def test_board_work_changing_boundaries_remain_semantic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            baseline = {
                "board": {
                    "active_workers": [{"ticket_id": "TASK-1", "thread_id": "thread-1"}],
                    "idle_worker_slots": 3,
                    "executable_tickets": [{"ticket_id": "TASK-2"}],
                    "awaiting_review_tickets": [{"ticket_id": "TASK-3"}],
                    "human_active_tickets": [{"ticket_id": "TASK-HUMAN"}],
                    "due_review_action_count": 1,
                    "review_wip": 1,
                    "queued_review_pools": [{"pool": "awaiting_review", "count": 1}],
                    "held_review_chases": [{"review": {"action": "held_outside_active_hours"}}],
                    "ledger": ".farplane/automation/spawned-threads.jsonl",
                    "worker_index": ".farplane/state/ticket-thread-associations.jsonl",
                    "released_worker_rows": [{"ticket_id": "TASK-OLD"}],
                },
                "semantic_time_state": self.semantic_time_state(
                    matured_reward_ids=["reward-due"]
                ),
            }
            baseline_fingerprint = guard.semantic_planning_fingerprint(root, baseline)
            board_variants = {
                "active_worker": {"active_workers": [{"ticket_id": "TASK-9", "thread_id": "thread-9"}]},
                "idle_capacity": {"idle_worker_slots": 2},
                "executable_ticket": {"executable_tickets": [{"ticket_id": "TASK-4"}]},
                "review_pool": {"queued_review_pools": [{"pool": "awaiting_review", "count": 2}]},
                "review_action": {"held_review_chases": [{"review": {"action": "dispatch_phone_chaser"}}]},
                "human_active": {"human_active_tickets": [{"ticket_id": "TASK-OTHER-HUMAN"}]},
            }
            for name, patch in board_variants.items():
                with self.subTest(name=name):
                    changed = copy.deepcopy(baseline)
                    changed["board"].update(patch)
                    self.assertNotEqual(
                        baseline_fingerprint,
                        guard.semantic_planning_fingerprint(root, changed),
                    )

            reward_changed = copy.deepcopy(baseline)
            reward_changed["semantic_time_state"] = self.semantic_time_state(
                matured_reward_ids=["reward-due", "new-reward-due"]
            )
            self.assertNotEqual(
                baseline_fingerprint,
                guard.semantic_planning_fingerprint(root, reward_changed),
            )

    def test_explicit_semantic_time_state_requires_all_boundary_classes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, "matured_reward_ids"):
                guard.semantic_planning_fingerprint(
                    Path(tmp),
                    {
                        "semantic_time_state": {
                            "metric_freshness": {},
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
                "metric_movement": {"reach": {"current": 10, "previous": 9}},
                "board": {
                    "idle_worker_slots": 4,
                    "review_wip": 2,
                    "held_review_chases": [{"review": {"action": "held_outside_active_hours"}}],
                },
                "evidence_ref": "reports/proof-a.md",
                "history_query": {"ref": ".farplane/tmp/history.json"},
                "semantic_time_state": self.semantic_time_state(),
                "scout_brief": [{"path": ".farplane/feed-scout/scout-brief.md", "evidence": "baseline"}],
            }
            baseline_fingerprint = guard.semantic_planning_fingerprint(root, baseline)
            variants = [
                {**baseline, "metrics": {"reach": 11}},
                {**baseline, "metric_movement": {"reach": {"current": 11, "previous": 10}}},
                {**baseline, "board": {"idle_worker_slots": 3, "review_wip": 2}},
                {
                    **baseline,
                    "board": {
                        "idle_worker_slots": 4,
                        "review_wip": 3,
                        "held_review_chases": [{"review": {"action": "held_outside_active_hours"}}],
                    },
                },
                {
                    **baseline,
                    "board": {
                        "idle_worker_slots": 4,
                        "review_wip": 2,
                        "held_review_chases": [{"review": {"action": "dispatch_phone_chaser"}}],
                    },
                },
                {**baseline, "evidence_ref": "reports/proof-b.md"},
                {
                    **baseline,
                    "semantic_time_state": self.semantic_time_state(
                        metric_freshness={"reach": "stale"}
                    ),
                },
                {
                    **baseline,
                    "semantic_time_state": self.semantic_time_state(
                        matured_reward_ids=["reach-checkin-7d"]
                    ),
                },
                {
                    **baseline,
                    "semantic_time_state": self.semantic_time_state(
                        operator_availability={"state": "available", "validity": "current"}
                    ),
                },
                {**baseline, "scout_brief": [{"path": ".farplane/feed-scout/scout-brief.md", "evidence": "changed"}]},
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
            result = guard.finish_wave(
                root,
                first["claim_id"],
                "completed",
                ["TASK-0001"],
                {"TASK-0001": "farplane-content-creation"},
                {"TASK-0001": "marketing"},
            )
            self.assertEqual(
                result["admitted_skill_calls"],
                [
                    {
                        "ticket_id": "TASK-0001",
                        "skill_ref": "farplane-content-creation",
                        "area_id": "marketing",
                    }
                ],
            )
            self.assertNotIn("admitted_specs", result)
            changed = guard.begin_wave(root, {"tickets": [], "metric": 1}, 2)
            self.assertEqual(changed["status"], "acquired")

    def test_identical_completed_input_is_no_op(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            planning_input = {"tickets": ["TASK-0001"], "metric": 2}
            first = guard.begin_wave(root, planning_input, 1)
            guard.finish_wave(
                root,
                first["claim_id"],
                "completed",
                ["TASK-0002"],
                {"TASK-0002": "farplane-market-learning"},
            )
            retry = guard.begin_wave(root, planning_input, 1)
            self.assertEqual(retry["status"], "no_op_unchanged_input")
            self.assertEqual(retry["no_op_category"], "unchanged_planning_fingerprint")

    def test_finish_enforces_wave_cap_and_unique_ticket_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = guard.begin_wave(root, {"metric": 0}, 1)
            with self.assertRaisesRegex(ValueError, "exceeds wave_size"):
                guard.finish_wave(
                    root,
                    first["claim_id"],
                    "completed",
                    ["TASK-1", "TASK-2"],
                    {"TASK-1": "skill-a", "TASK-2": "skill-b"},
                )
            with self.assertRaisesRegex(ValueError, "duplicate admitted"):
                guard.finish_wave(
                    root,
                    first["claim_id"],
                    "completed",
                    ["TASK-1", "TASK-1"],
                    {"TASK-1": "skill-a"},
                )
            with self.assertRaisesRegex(ValueError, "selected skill_ref"):
                guard.finish_wave(root, first["claim_id"], "completed", ["TASK-1"])
            with self.assertRaisesRegex(ValueError, "non-admitted tickets"):
                guard.finish_wave(
                    root,
                    first["claim_id"],
                    "completed",
                    ["TASK-1"],
                    {"TASK-1": "skill-a"},
                    {"TASK-2": "area-b"},
                )
            result = guard.finish_wave(
                root,
                first["claim_id"],
                "completed",
                ["TASK-1"],
                {"TASK-1": "skill-a"},
            )
            self.assertEqual(
                result["admitted_skill_calls"],
                [{"ticket_id": "TASK-1", "skill_ref": "skill-a"}],
            )
            second = guard.begin_wave(root, {"metric": 1}, 1)
            with self.assertRaisesRegex(ValueError, "already admitted"):
                guard.finish_wave(
                    root,
                    second["claim_id"],
                    "completed",
                    ["TASK-1"],
                    {"TASK-1": "skill-a"},
                )


if __name__ == "__main__":
    unittest.main()
