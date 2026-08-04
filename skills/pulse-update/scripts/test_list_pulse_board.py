#!/usr/bin/env python3
"""Focused tests for the Work Pulse board classifier."""

from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable


MODULE_PATH = Path(__file__).with_name("list_pulse_board.py")
SPEC = importlib.util.spec_from_file_location("list_pulse_board", MODULE_PATH)
assert SPEC and SPEC.loader
BOARD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BOARD)
MATERIALIZER_PATH = Path(__file__).with_name("materialize_skill_call.py")
MATERIALIZER_SPEC = importlib.util.spec_from_file_location("materialize_skill_call", MATERIALIZER_PATH)
assert MATERIALIZER_SPEC and MATERIALIZER_SPEC.loader
MATERIALIZER = importlib.util.module_from_spec(MATERIALIZER_SPEC)
MATERIALIZER_SPEC.loader.exec_module(MATERIALIZER)


def planned_call(ticket_id: str, call_id: str | None = None) -> dict[str, object]:
    return {
        "ticket_id": ticket_id,
        "call_id": call_id or ticket_id.lower(),
        "title": f"Run {ticket_id}",
        "skill_ref": "self-improve",
        "arguments": {
            "target": "skills/plan-next-wave",
            "metric": "planner_idea_keep_rate",
            "feedback_class": "immediate",
            "failure_evidence": "tickets/TASK-0385/artifacts/review/completion-review.md",
        },
        "expected_artifact": "a measured preventive change",
        "objective_contribution": {
            "ultimate_kpi_id": "evidence_distribution_reach",
            "contribution_type": "enabler",
            "kpi_or_guard_id": "planner_idea_keep_rate",
            "causal_mechanism": "prevent repeated low-value planner output",
            "expected_change": "one measured configured-skill improvement",
            "forecast_basis": {
                "kind": "configured_threshold",
                "ref": "tickets/TASK-0385/ticket.md",
            },
            "metric_provider": "planner eval",
            "signal_horizon": "immediate",
            "check_in_at": "unscheduled",
        },
    }


def write_ticket(
    root: Path,
    ticket_id: str,
    *,
    status: str = "todo",
    claimed_by: str = "",
    depends_on: list[str] | None = None,
    priority: str = "medium",
    due_at: str = "",
    reward_rows: list[dict[str, object]] | None = None,
    review_state: dict[str, object] | None = None,
    area_id: str = "",
) -> Path:
    path = root / "tickets" / ticket_id / "ticket.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
                "---",
                f"ticket_id: {ticket_id}",
                f"title: {ticket_id}",
                f"status: {status}",
                f"priority: {priority}",
                *( [f"due_at: {due_at}"] if due_at else [] ),
                f"claimed_by: {claimed_by}",
                f"depends_on: {json.dumps(depends_on or [])}",
                "created_at: 2026-07-01T00:00:00Z",
                "updated_at: 2026-07-01T00:00:00Z",
                "---",
                "",
                f"# {ticket_id}",
                "",
    ]
    if area_id:
        lines.extend(["## State", "", f"- `area:` {area_id}", ""])
    if reward_rows is not None:
        lines.extend(
            [
                "## Reward",
                "",
                "```yaml",
                "kpi_rewards:",
            ]
        )
        for row in reward_rows:
            lines.extend(
                [
                    f"  - reward_id: {row.get('reward_id', '')}",
                    f"    kpi_id: {row.get('kpi_id', 'metric')}",
                    f"    expected_reward: {json.dumps(row.get('expected_reward', 'improve metric'))}",
                    f"    check_in_at: {json.dumps(row.get('check_in_at', ''))}",
                    f"    actual_result: {json.dumps(row.get('actual_result')) if row.get('actual_result') is not None else ''}",
                    f"    decision: {row.get('decision', '')}",
                    f"    evaluated_at: {json.dumps(row.get('evaluated_at')) if row.get('evaluated_at') is not None else ''}",
                    f"    evaluation_key: {row.get('evaluation_key', '')}",
                    f"    supersedes_evaluation_key: {row.get('supersedes_evaluation_key', '')}",
                    f"    evidence_refs: {json.dumps(row.get('evidence_refs', []))}",
                ]
            )
        lines.extend(["guard: preserve attribution", "```", ""])
    path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )
    if review_state is not None:
        progress = path.parent / "progress.md"
        progress.write_text(
            "## Review\n\n```yaml\n" + "\n".join(
                f"{key}: {json.dumps(value) if not isinstance(value, bool) else str(value).lower()}"
                for key, value in review_state.items()
            ) + "\n```\n",
            encoding="utf-8",
        )
    return path


def write_associations(root: Path, rows: list[dict[str, object]]) -> None:
    path = root / ".farplane" / "state" / "ticket-thread-associations.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def run_minimal_pulse_fixture(
    root: Path,
    planner: Callable[[dict[str, str], list[dict[str, object]], int], list[dict[str, str]]],
    *,
    wave_size: int,
    worker_limit: int,
    ready_low_watermark: int = 1,
) -> dict[str, object]:
    """Exercise the prompt-owned Pulse boundary without inventing a runtime.

    The real board classifier owns admission. This fixture injects the pure
    planner result, materializes admitted skill calls as ticket files, reruns
    admission, and applies worker capacity so the composed contract is
    executable in tests.
    """

    board = BOARD.build_board(root, worker_limit=worker_limit)
    planner_calls = 0
    materialized: list[str] = []
    initial_dispatch_limit = min(board["idle_worker_slots"], len(board["executable_tickets"]))
    dispatched = [
        row["ticket_id"] for row in board["executable_tickets"][:initial_dispatch_limit]
    ]
    remaining_slots = board["idle_worker_slots"] - len(dispatched)
    ready_after_dispatch = max(0, board["ready_ticket_count"] - len(dispatched))
    mode = "dispatch_ready"
    if ready_after_dispatch < max(0, ready_low_watermark):
        mode = "dispatch_then_plan" if dispatched else "plan_next_wave"
        project_context = {
            name: (root / "farplane" / name).read_text(encoding="utf-8")
            for name in ("harness.yaml", "metrics.yaml")
        }
        ticket_history = [*board["executable_tickets"], *board["excluded_tickets"]]
        specs = planner(project_context, ticket_history, wave_size)
        planner_calls += 1
        for spec in specs[:wave_size]:
            ticket_id = spec["ticket_id"]
            call = {key: value for key, value in spec.items() if key != "ticket_id"}
            MATERIALIZER.materialize_skill_call(
                root,
                ticket_id,
                call,
                created_at="2026-07-17T00:00:00Z",
            )
            materialized.append(ticket_id)
        board = BOARD.build_board(root, worker_limit=worker_limit)
        newly_ready = [
            row["ticket_id"] for row in board["executable_tickets"]
            if row["ticket_id"] not in dispatched
        ]
        dispatched.extend(newly_ready[:remaining_slots])
    return {
        "mode": mode,
        "planner_calls": planner_calls,
        "materialized": materialized,
        "dispatched": dispatched,
        "board": board,
    }


class WorkPulseBoardTests(unittest.TestCase):
    def test_review_tickets_project_to_area_pools_without_consuming_workers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "TASK-REVIEW-A", status="awaiting_review")
            write_ticket(root, "TASK-REVIEW-B", status="awaiting_review")
            write_ticket(root, "TASK-REVIEW-C", status="awaiting_review", area_id="delivery")
            decisions = root / ".farplane" / "automation" / "decisions.jsonl"
            decisions.parent.mkdir(parents=True, exist_ok=True)
            decisions.write_text(
                json.dumps(
                    {
                        "action": "plan_next_wave",
                        "status": "completed",
                        "admitted_skill_calls": [
                            {
                                "ticket_id": "TASK-REVIEW-A",
                                "skill_ref": "self-improve",
                                "area_id": "self_improvement",
                            },
                            {
                                "ticket_id": "TASK-REVIEW-B",
                                "skill_ref": "self-improve",
                                "area_id": "self_improvement",
                            },
                        ],
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            result = BOARD.build_board(root, worker_limit=4)

            self.assertEqual(result["review_item_count"], 3)
            self.assertEqual(result["review_pool_count"], 2)
            self.assertEqual(result["review_wip"], 2)
            self.assertEqual(
                [pool["pool_id"] for pool in result["review_pools"]],
                ["delivery", "self_improvement"],
            )
            self.assertEqual(
                result["review_pools"][1]["ticket_ids"],
                ["TASK-REVIEW-A", "TASK-REVIEW-B"],
            )
            self.assertEqual(result["review_pool_limit"], 3)
            self.assertEqual(result["total_review_pool_count"], 2)
            self.assertFalse(result["review_pool_saturated"])
            self.assertEqual(result["queued_review_pools"], [])
            self.assertEqual(result["idle_worker_slots"], 4)

    def test_historical_admitted_specs_remain_read_only_area_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            decisions = root / ".farplane" / "automation" / "decisions.jsonl"
            decisions.parent.mkdir(parents=True, exist_ok=True)
            decisions.write_text(
                json.dumps(
                    {
                        "action": "materialize_reserved_wave",
                        "pulse_receipt": {
                            "admitted_specs": [
                                {"ticket_id": "TASK-OLD", "area_id": "legacy-area"}
                            ]
                        },
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            self.assertEqual(
                BOARD.planner_area_by_ticket(root), {"TASK-OLD": "legacy-area"}
            )

    def test_review_pool_limit_caps_active_digests_and_queues_every_other_area(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for suffix, area in zip("ABCD", ("area-a", "area-b", "area-c", "area-d")):
                write_ticket(
                    root,
                    f"TASK-REVIEW-{suffix}",
                    status="awaiting_review",
                    area_id=area,
                    review_state={
                        "artifact_refs": [f"tickets/TASK-REVIEW-{suffix}/artifacts/output.md"],
                        "thread_ref": f"thread-{suffix.lower()}",
                        "requested_at": "2026-07-14T10:00:00Z",
                        "decision": "",
                        "reminder_count": 0,
                        "telegram_reminder_message_ids": [],
                        "phone_chaser_count": 0,
                        "phone_chaser_dispatch_ids": [],
                    },
                )

            result = BOARD.build_board(root, worker_limit=4, review_wip=2)
            rerun = BOARD.build_board(root, worker_limit=4, review_wip=2)

            self.assertEqual(result["review_pool_limit"], 2)
            self.assertEqual(result["total_review_pool_count"], 4)
            self.assertEqual(result["review_pool_count"], 2)
            self.assertEqual(result["review_wip"], 2)
            self.assertTrue(result["review_pool_saturated"])
            self.assertEqual(
                [pool["pool_id"] for pool in result["review_pools"]],
                ["area-a", "area-b"],
            )
            self.assertEqual(
                [pool["pool_id"] for pool in result["queued_review_pools"]],
                ["area-c", "area-d"],
            )
            digest = result["review_pools"][0]["operator_digest"]
            self.assertEqual(digest["area_id"], "area-a")
            self.assertEqual(
                digest["tickets"][0],
                {
                    "ticket_id": "TASK-REVIEW-A",
                    "ticket_path": "tickets/TASK-REVIEW-A/ticket.md",
                    "progress_ref": "tickets/TASK-REVIEW-A/progress.md",
                    "artifact_refs": ["tickets/TASK-REVIEW-A/artifacts/output.md"],
                    "thread_ref": "thread-a",
                    "requested_at": "2026-07-14T10:00:00Z",
                    "decision": "",
                    "next_action": "send_initial_telegram",
                },
            )
            self.assertEqual(
                digest["digest_id"],
                rerun["review_pools"][0]["operator_digest"]["digest_id"],
            )
            self.assertEqual(result["review_item_count"], 4)
            self.assertEqual(result["idle_worker_slots"], 4)

    def test_missing_review_area_provenance_never_collapses_unrelated_tickets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "TASK-UNKNOWN-A", status="awaiting_review")
            write_ticket(root, "TASK-UNKNOWN-B", status="awaiting_review")

            result = BOARD.build_board(root, worker_limit=1)

            self.assertEqual(result["review_item_count"], 2)
            self.assertEqual(result["review_pool_count"], 2)
            self.assertEqual(
                [pool["pool_id"] for pool in result["review_pools"]],
                ["unassigned:TASK-UNKNOWN-A", "unassigned:TASK-UNKNOWN-B"],
            )

    def test_composed_ready_ticket_dispatch_skips_planner(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "TASK-READY-A")
            write_ticket(root, "TASK-READY-B")

            def planner(*_args: object) -> list[dict[str, str]]:
                self.fail("planner must not run while executable work exists")

            result = run_minimal_pulse_fixture(
                root,
                planner,
                wave_size=3,
                worker_limit=1,
            )

            self.assertEqual(result["mode"], "dispatch_ready")
            self.assertEqual(result["planner_calls"], 0)
            self.assertEqual(result["materialized"], [])
            self.assertEqual(result["dispatched"], ["TASK-READY-A"])

    def test_composed_empty_board_plans_materializes_readmits_and_limits_dispatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            (farplane / "harness.yaml").write_text("kind: project-harness\n", encoding="utf-8")
            (farplane / "metrics.yaml").write_text("metrics: {}\n", encoding="utf-8")
            observed: dict[str, object] = {}

            def planner(
                project_context: dict[str, str],
                ticket_history: list[dict[str, object]],
                wave_size: int,
            ) -> list[dict[str, str]]:
                observed.update(
                    context_files=sorted(project_context),
                    ticket_history=ticket_history,
                    wave_size=wave_size,
                )
                return [
                    planned_call("TASK-PLAN-1"),
                    planned_call("TASK-PLAN-2"),
                    planned_call("TASK-PLAN-3"),
                    planned_call("TASK-PLAN-OVERFLOW"),
                ]

            result = run_minimal_pulse_fixture(
                root,
                planner,
                wave_size=3,
                worker_limit=1,
            )

            self.assertEqual(result["mode"], "plan_next_wave")
            self.assertEqual(result["planner_calls"], 1)
            self.assertEqual(
                observed["context_files"],
                ["harness.yaml", "metrics.yaml"],
            )
            self.assertEqual(observed["ticket_history"], [])
            self.assertEqual(observed["wave_size"], 3)
            self.assertEqual(
                result["materialized"],
                ["TASK-PLAN-1", "TASK-PLAN-2", "TASK-PLAN-3"],
            )
            self.assertEqual(result["dispatched"], ["TASK-PLAN-1"])
            self.assertEqual(
                [row["ticket_id"] for row in result["board"]["executable_tickets"]],
                ["TASK-PLAN-1", "TASK-PLAN-2", "TASK-PLAN-3"],
            )
            self.assertFalse((root / "tickets" / "TASK-PLAN-OVERFLOW").exists())
            ticket_text = (root / "tickets" / "TASK-PLAN-1" / "ticket.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("skill_ref: self-improve", ticket_text)
            self.assertIn("failure_evidence:", ticket_text)
            self.assertNotIn("workflow_steps", ticket_text)
            self.assertNotIn("Todo List", ticket_text)

    def test_composed_dispatch_then_refills_below_ready_low_watermark(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            (farplane / "harness.yaml").write_text("kind: project-harness\n", encoding="utf-8")
            (farplane / "metrics.yaml").write_text("metrics: {}\n", encoding="utf-8")
            write_ticket(root, "TASK-READY")

            def planner(*_args: object) -> list[dict[str, str]]:
                return [planned_call("TASK-REFILL")]

            result = run_minimal_pulse_fixture(
                root,
                planner,
                wave_size=1,
                worker_limit=2,
                ready_low_watermark=2,
            )

            self.assertEqual(result["mode"], "dispatch_then_plan")
            self.assertEqual(result["planner_calls"], 1)
            self.assertEqual(result["materialized"], ["TASK-REFILL"])
            self.assertEqual(result["dispatched"], ["TASK-READY", "TASK-REFILL"])

    def test_empty_board_exposes_refill_condition_without_product_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            result = BOARD.build_board(root, worker_limit=2)

            self.assertEqual(result["executable_tickets"], [])
            self.assertEqual(result["ready_ticket_count"], 0)
            self.assertEqual(result["idle_worker_slots"], 2)
            self.assertNotIn("products", result)

    def test_classifies_generic_ticket_state_without_product_or_reward(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "TASK-READY")
            write_ticket(root, "TASK-BLOCKED", status="blocked")
            write_ticket(root, "TASK-APPROVAL", status="awaiting_review")
            write_ticket(root, "TASK-CLAIMED", status="active", claimed_by="codex-other")
            write_ticket(root, "TASK-DEPENDENCY", depends_on=["TASK-MISSING"])
            write_ticket(root, "TASK-DONE", status="done")
            write_ticket(root, "TASK-REVIEW", status="awaiting_review")

            result = BOARD.build_board(root, worker_limit=2)

            self.assertEqual(
                [row["ticket_id"] for row in result["executable_tickets"]],
                ["TASK-READY"],
            )
            exclusions = {
                row["ticket_id"]: row["exclusion_reasons"]
                for row in result["excluded_tickets"]
            }
            self.assertIn("status_not_executable", exclusions["TASK-BLOCKED"])
            self.assertIn("awaiting_review", exclusions["TASK-APPROVAL"])
            self.assertIn("claimed_by", exclusions["TASK-CLAIMED"])
            self.assertIn("unsatisfied_dependencies", exclusions["TASK-DEPENDENCY"])
            self.assertIn("terminal", exclusions["TASK-DONE"])
            self.assertIn("awaiting_review", exclusions["TASK-REVIEW"])
            self.assertEqual(result["review_wip"], 2)
            self.assertEqual(result["idle_worker_slots"], 2)
            self.assertEqual(
                [row["ticket_id"] for row in result["human_active_tickets"]],
                ["TASK-CLAIMED"],
            )
            self.assertEqual(result["ready_ticket_count"], 1)

    def test_human_active_ticket_does_not_block_empty_board_refill_or_capacity(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "TASK-HUMAN", status="active", claimed_by="codex-human")

            result = BOARD.build_board(root, worker_limit=1)

            self.assertEqual(result["ready_ticket_count"], 0)
            self.assertEqual(result["idle_worker_slots"], 1)
            self.assertEqual(result["active_workers"], [])
            self.assertEqual(
                [row["ticket_id"] for row in result["human_active_tickets"]],
                ["TASK-HUMAN"],
            )

    def test_worker_limit_excludes_released_review_and_blocked_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "TASK-READY")
            write_ticket(root, "TASK-ACTIVE", status="active", claimed_by="codex-active")
            write_associations(
                root,
                [
                    {"ticket_id": "TASK-ACTIVE", "thread_id": "thread-active"},
                    {"ticket_id": "TASK-REVIEW", "thread_id": "thread-review"},
                    {"ticket_id": "TASK-BLOCKED", "thread_id": "thread-blocked"},
                ],
            )

            result = BOARD.build_board(root, worker_limit=1)

            self.assertEqual(result["idle_worker_slots"], 0)
            self.assertEqual(len(result["active_workers"]), 1)
            self.assertEqual(len(result["released_worker_rows"]), 2)

    def test_due_reward_rows_resume_original_ticket_and_future_rows_stay_dormant(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(
                root,
                "TASK-EXPERIMENT",
                status="waiting_signal",
                reward_rows=[
                    {
                        "reward_id": "conversion-7d",
                        "kpi_id": "conversion",
                        "check_in_at": "2026-07-10T00:00:00Z",
                    },
                    {
                        "reward_id": "retention-monitor",
                        "kpi_id": "retention",
                        "check_in_at": "2026-07-11T00:00:00Z",
                        "actual_result": "observed",
                        "decision": "monitor",
                        "evaluation_key": "eval-retention-1",
                    },
                    {
                        "reward_id": "quality-14d",
                        "kpi_id": "quality",
                        "check_in_at": "2026-07-12T00:00:00Z",
                    },
                    {
                        "reward_id": "accepted-now",
                        "kpi_id": "quality",
                        "check_in_at": "2026-07-10T00:00:00Z",
                        "decision": "accept",
                    },
                ],
            )

            result = BOARD.build_board(
                root,
                now=datetime(2026, 7, 11, tzinfo=timezone.utc),
            )

            self.assertEqual(
                [row["ticket_id"] for row in result["executable_tickets"]],
                ["TASK-EXPERIMENT"],
            )
            ticket = result["executable_tickets"][0]
            self.assertEqual(ticket["execution_reason"], "due_reward_checkin")
            self.assertEqual(
                [row["reward_id"] for row in ticket["due_reward_checkins"]],
                ["conversion-7d", "retention-monitor"],
            )
            self.assertEqual(
                [row["reward_id"] for row in ticket["future_reward_checkins"]],
                ["quality-14d"],
            )
            self.assertEqual(
                ticket["terminal_reward_outcomes"][0]["state"], "terminal_accept"
            )
            self.assertEqual(result["due_checkin_tickets"][0]["path"], "tickets/TASK-EXPERIMENT/ticket.md")
            self.assertEqual(result["ready_ticket_count"], 1)

    def test_unscheduled_rewards_are_valid_inert_and_malformed_rows_stay_actionable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(
                root,
                "TASK-SCHEDULE-SHAPES",
                status="waiting_signal",
                reward_rows=[
                    {
                        "reward_id": "explicitly-unscheduled",
                        "check_in_at": "unscheduled",
                    },
                    {
                        "reward_id": "blank-pending",
                        "check_in_at": None,
                    },
                    {
                        "reward_id": "bad-delayed-time",
                        "check_in_at": "after review",
                    },
                    {
                        "reward_id": "timezone-naive",
                        "check_in_at": "2026-07-15T18:00:00",
                    },
                ],
            )

            result = BOARD.build_board(
                root,
                now=datetime(2026, 7, 11, tzinfo=timezone.utc),
            )

            ticket = result["excluded_tickets"][0]
            self.assertEqual(
                [row["reward_id"] for row in ticket["unscheduled_reward_checkins"]],
                ["explicitly-unscheduled"],
            )
            self.assertEqual(
                [row["state"] for row in ticket["unscheduled_reward_checkins"]],
                ["unscheduled"],
            )
            self.assertEqual(
                [row["reward_id"] for row in ticket["reward_checkin_gaps"]],
                ["blank-pending", "bad-delayed-time", "timezone-naive"],
            )
            self.assertEqual(
                [row["gap"] for row in ticket["reward_checkin_gaps"]],
                ["missing_reward_schedule", "invalid_check_in_at", "invalid_check_in_at"],
            )
            self.assertEqual(result["due_checkin_tickets"], [])
            self.assertEqual(result["executable_tickets"], [])

    def test_due_projection_uses_decision_state_and_keeps_safety_gates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            now = datetime(2026, 7, 11, tzinfo=timezone.utc)
            write_ticket(
                root,
                "TASK-PARTIAL",
                status="waiting_signal",
                reward_rows=[
                    {
                        "reward_id": "partial",
                        "check_in_at": "2026-07-10T00:00:00Z",
                        "actual_result": "observed",
                    }
                ],
            )
            write_ticket(
                root,
                "TASK-SCORED",
                status="waiting_signal",
                reward_rows=[
                    {
                        "reward_id": "accepted",
                        "check_in_at": "2026-07-10T00:00:00Z",
                        "actual_result": "observed",
                        "decision": "accept",
                    }
                ],
            )
            write_ticket(
                root,
                "TASK-BLOCKED-CHECKIN",
                status="blocked",
                reward_rows=[
                    {"reward_id": "blocked", "check_in_at": "2026-07-10T00:00:00Z"}
                ],
            )

            result = BOARD.build_board(root, now=now)

            self.assertEqual(
                [row["ticket_id"] for row in result["executable_tickets"]],
                ["TASK-PARTIAL"],
            )
            exclusions = {
                row["ticket_id"]: row["exclusion_reasons"]
                for row in result["excluded_tickets"]
            }
            self.assertIn("status_not_executable", exclusions["TASK-SCORED"])
            self.assertIn("status_not_executable", exclusions["TASK-BLOCKED-CHECKIN"])

    def test_reward_identity_survives_row_reordering_and_missing_ids_are_invalid(self) -> None:
        rows = [
            {
                "reward_id": "second-horizon",
                "kpi_id": "retention",
                "check_in_at": "2026-07-10T00:00:00Z",
            },
            {
                "reward_id": "first-horizon",
                "kpi_id": "activation",
                "check_in_at": "2026-07-09T00:00:00Z",
            },
        ]
        now = datetime(2026, 7, 11, tzinfo=timezone.utc)
        first = BOARD.classify_reward_checkins(
            "## Reward\n\n```yaml\n" + "kpi_rewards:\n" + "\n".join(
                f"  - reward_id: {row['reward_id']}\n    kpi_id: {row['kpi_id']}\n    check_in_at: {row['check_in_at']}"
                for row in rows
            ) + "\n```\n",
            now,
        )
        second = BOARD.classify_reward_checkins(
            "## Reward\n\n```yaml\n" + "kpi_rewards:\n" + "\n".join(
                f"  - reward_id: {row['reward_id']}\n    kpi_id: {row['kpi_id']}\n    check_in_at: {row['check_in_at']}"
                for row in reversed(rows)
            )
            + "\n  - kpi_id: missing\n    check_in_at: 2026-07-10T00:00:00Z"
            + "\n  - reward_id: first-horizon\n    kpi_id: duplicate\n    check_in_at: 2026-07-10T00:00:00Z\n```\n",
            now,
        )

        self.assertEqual(
            {row["reward_id"] for row in first["due"]},
            {row["reward_id"] for row in second["due"]},
        )
        self.assertEqual(
            [row["gap"] for row in second["invalid"]],
            ["missing_reward_id", "duplicate_reward_id"],
        )

    def test_priority_orders_executable_tickets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "TASK-LOW", priority="low")
            write_ticket(root, "TASK-HIGH", priority="high")

            result = BOARD.build_board(root)

            self.assertEqual(
                [row["ticket_id"] for row in result["executable_tickets"]],
                ["TASK-HIGH", "TASK-LOW"],
            )

    def test_due_at_orders_within_priority_and_missing_is_last(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "TASK-MISSING")
            write_ticket(root, "TASK-LATE", due_at="2026-07-20T00:00:00Z")
            write_ticket(root, "TASK-EARLY", due_at="2026-07-10T09:00:00+08:00")
            write_ticket(root, "TASK-OVERDUE", due_at="2026-06-30T00:00:00Z")

            result = BOARD.build_board(
                root, now=datetime(2026, 7, 1, tzinfo=timezone.utc)
            )

            self.assertEqual(
                [row["ticket_id"] for row in result["executable_tickets"]],
                ["TASK-OVERDUE", "TASK-EARLY", "TASK-LATE", "TASK-MISSING"],
            )

    def test_priority_precedes_due_at_and_ticket_id_breaks_due_ties(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "TASK-URGENT", priority="urgent")
            write_ticket(
                root,
                "TASK-B",
                priority="high",
                due_at="2026-07-01T00:00:00Z",
            )
            write_ticket(
                root,
                "TASK-A",
                priority="high",
                due_at="2026-07-01T08:00:00+08:00",
            )

            result = BOARD.build_board(root)

            self.assertEqual(
                [row["ticket_id"] for row in result["executable_tickets"]],
                ["TASK-URGENT", "TASK-A", "TASK-B"],
            )

    def test_only_done_dependencies_are_satisfied(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rejected = write_ticket(root, "TASK-REJECTED", status="rejected")
            done = write_ticket(root, "TASK-DONE", status="done")
            archive = root / "tickets" / "archive"
            archive.mkdir(parents=True)
            rejected.parent.rename(archive / rejected.parent.name)
            done.parent.rename(archive / done.parent.name)
            write_ticket(root, "TASK-WAITS-REJECTED", depends_on=["TASK-REJECTED"])
            write_ticket(root, "TASK-WAITS-DONE", depends_on=["TASK-DONE"])

            result = BOARD.build_board(root)

            self.assertEqual(
                [row["ticket_id"] for row in result["executable_tickets"]],
                ["TASK-WAITS-DONE"],
            )
            rejected_row = next(
                row for row in result["excluded_tickets"]
                if row["ticket_id"] == "TASK-WAITS-REJECTED"
            )
            self.assertIn("unsatisfied_dependencies", rejected_row["exclusion_reasons"])

    def test_indexed_github_issue_satisfies_dependency_without_network(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "TASK-WAITS-REMOTE", depends_on=["TASK-REMOTE"])
            index = root / "tickets" / "archive-index.jsonl"
            index.parent.mkdir(parents=True, exist_ok=True)
            index.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "storage": "github_issue",
                        "ticket_id": "TASK-REMOTE",
                        "title": "Remote dependency",
                        "status": "done",
                        "closed_at": "2026-07-12T00:00:00Z",
                        "github_issue_url": "https://github.com/acme/archive/issues/12",
                        "github_issue_number": 12,
                        "media_comment_urls": [],
                        "event_id": "event-12",
                        "runs": [],
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            result = BOARD.build_board(root)

        self.assertEqual(
            [row["ticket_id"] for row in result["executable_tickets"]],
            ["TASK-WAITS-REMOTE"],
        )

    def test_due_review_action_is_worker_free_and_decision_closes_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(
                root,
                "TASK-REVIEW",
                status="awaiting_review",
                review_state={
                    "artifact_refs": ["tickets/TASK-REVIEW/artifacts/example.md"],
                    "thread_ref": "thread-1",
                    "requested_at": "2026-07-09T00:00:00Z",
                    "reminder_count": 0,
                    "phone_chaser_count": 0,
                    "telegram_status": "sent",
                    "telegram_message_id": "telegram-1",
                    "decision": None,
                },
            )
            write_ticket(
                root,
                "TASK-DECIDED",
                status="awaiting_review",
                review_state={
                    "thread_ref": "thread-2",
                    "requested_at": "2026-07-09T00:00:00Z",
                    "artifact_refs": ["tickets/TASK-DECIDED/artifacts/example.md"],
                    "decision": "approved",
                },
            )

            result = BOARD.build_board(
                root,
                worker_limit=1,
                now=datetime(2026, 7, 11, tzinfo=timezone.utc),
            )

            self.assertEqual(result["next_due_review_action"]["ticket_id"], "TASK-REVIEW")
            self.assertEqual(
                result["next_due_review_action"]["review"]["action"],
                "send_telegram_reminder",
            )
            self.assertEqual(result["due_review_action_count"], 1)
            self.assertEqual(result["idle_worker_slots"], 1)
            self.assertEqual(result["active_workers"], [])

    def test_review_thread_mismatch_blocks_chase_and_resume(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(
                root,
                "TASK-REVIEW",
                status="awaiting_review",
                review_state={
                    "artifact_refs": ["tickets/TASK-REVIEW/artifacts/example.md"],
                    "thread_ref": "pulse-manager-thread",
                    "requested_at": "2026-07-09T00:00:00Z",
                    "reminder_count": 0,
                    "phone_chaser_count": 0,
                    "telegram_status": "sent",
                    "telegram_message_id": "telegram-1",
                    "decision": None,
                },
            )
            write_associations(root, [{
                "ticket_id": "TASK-REVIEW",
                "thread_id": "ticket-worker-thread",
                "observed_at": "2026-07-09T00:00:00Z",
            }])

            result = BOARD.build_board(root, now=datetime(2026, 7, 11, tzinfo=timezone.utc))

            action = result["next_due_review_action"]
            self.assertEqual(action["review"]["action"], "repair_thread_identity")
            self.assertEqual(action["review"]["associated_thread_ref"], "ticket-worker-thread")
            self.assertEqual(len(result["thread_identity_mismatches"]), 1)

    def test_missing_review_ledger_is_repair_action_not_silent_wait(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "TASK-REVIEW", status="awaiting_review")

            result = BOARD.build_board(root, now=datetime(2026, 7, 11, tzinfo=timezone.utc))

            action = result["next_due_review_action"]
            self.assertEqual(action["ticket_id"], "TASK-REVIEW")
            self.assertEqual(action["review"]["action"], "repair_review_state")
            self.assertEqual(action["review"]["reason"], "missing_progress_md")

    def test_blocked_initial_telegram_is_retried_by_automation_authority(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(
                root,
                "TASK-REVIEW",
                status="awaiting_review",
                review_state={
                    "artifact_refs": ["tickets/TASK-REVIEW/artifacts/example.md"],
                    "thread_ref": "thread-1",
                    "requested_at": "2026-07-11T00:00:00Z",
                    "telegram_status": "blocked",
                    "telegram_message_id": None,
                    "reminder_count": 0,
                    "phone_chaser_count": 0,
                    "decision": None,
                },
            )

            result = BOARD.build_board(root, now=datetime(2026, 7, 11, 1, tzinfo=timezone.utc))

            self.assertEqual(
                result["next_due_review_action"]["review"]["action"],
                "send_initial_telegram",
            )

    def test_documented_plain_yaml_review_block_is_parsed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_ticket(root, "TASK-REVIEW", status="awaiting_review")
            (ticket.parent / "progress.md").write_text(
                """## Review

artifact_refs:
  - tickets/TASK-REVIEW/artifacts/example.md
thread_ref: thread-1
requested_at: 2026-07-11T00:00:00Z
telegram_status: blocked
telegram_message_id:
reminder_count: 0
phone_chaser_count: 0
decision:
""",
                encoding="utf-8",
            )

            result = BOARD.build_board(root, now=datetime(2026, 7, 11, 1, tzinfo=timezone.utc))

            self.assertEqual(
                result["next_due_review_action"]["review"]["action"],
                "send_initial_telegram",
            )

    def test_versioned_current_review_wins_over_stale_exact_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_ticket(root, "TASK-REVIEW", status="awaiting_review")
            (ticket.parent / "progress.md").write_text(
                """## V5 Post-ready Review

```yaml
artifact_refs: [tickets/TASK-REVIEW/artifacts/v5.mp4]
thread_ref: thread-v5
requested_at: 2026-07-11T00:00:00Z
telegram_status: sent
telegram_message_id: telegram-v5
reminder_count: 0
phone_chaser_count: 0
decision:
```

## Review

```yaml
artifact_refs: [tickets/TASK-REVIEW/artifacts/v4.mp4]
thread_ref: thread-v4
requested_at: 2026-07-10T00:00:00Z
decision: reject
```

## Superseded V3 Review

```yaml
artifact_refs: [tickets/TASK-REVIEW/artifacts/v3.mp4]
thread_ref: thread-v3
requested_at: 2026-07-09T00:00:00Z
decision: reject
```
""",
                encoding="utf-8",
            )

            result = BOARD.build_board(root, now=datetime(2026, 7, 11, 1, tzinfo=timezone.utc))

            review = result["awaiting_review_tickets"][0]
            self.assertEqual(review["review_artifact_refs"], ["tickets/TASK-REVIEW/artifacts/v5.mp4"])
            self.assertEqual(review["review_thread_ref"], "thread-v5")
            self.assertEqual(review["review_decision"], "")

    def test_phone_chaser_follows_two_unanswered_telegram_reminders(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bindings = root / "farplane" / "bindings.yaml"
            bindings.parent.mkdir(parents=True)
            bindings.write_text(
                """operator:
  review_chase_policy:
    timezone: UTC
    active_hours: {start: '00:00', end: '23:59'}
    pulse_interval_minutes: 30
    telegram_reminder_after_unanswered_turns: [2, 4]
    phone_chaser_after_unanswered_turns: [6, 12]
    telegram_reminder_limit: 2
    phone_chaser_limit: 2
""",
                encoding="utf-8",
            )
            write_ticket(
                root,
                "TASK-REVIEW",
                status="awaiting_review",
                review_state={
                    "artifact_refs": ["tickets/TASK-REVIEW/artifacts/example.md"],
                    "thread_ref": "thread-1",
                    "requested_at": "2026-07-11T00:00:00Z",
                    "telegram_status": "sent",
                    "telegram_message_id": "telegram-1",
                    "reminder_count": 2,
                    "telegram_reminder_message_ids": ["telegram-2", "telegram-3"],
                    "phone_chaser_count": 0,
                    "decision": None,
                },
            )

            result = BOARD.build_board(root, now=datetime(2026, 7, 11, 3, tzinfo=timezone.utc))

            action = result["next_due_review_action"]["review"]
            self.assertEqual(action["action"], "dispatch_phone_chaser")
            self.assertEqual(action["unanswered_pulse_turns"], 6)

    def test_phone_chaser_requires_receipts_for_prior_telegram_reminders(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(
                root,
                "TASK-REVIEW",
                status="awaiting_review",
                review_state={
                    "artifact_refs": ["tickets/TASK-REVIEW/artifacts/example.md"],
                    "thread_ref": "thread-1",
                    "requested_at": "2026-07-11T00:00:00Z",
                    "telegram_status": "sent",
                    "telegram_message_id": "telegram-1",
                    "reminder_count": 2,
                    "telegram_reminder_message_ids": ["telegram-2"],
                    "phone_chaser_count": 0,
                    "decision": None,
                },
            )

            result = BOARD.build_board(root, now=datetime(2026, 7, 11, 3, tzinfo=timezone.utc))

            action = result["next_due_review_action"]["review"]
            self.assertEqual(action["action"], "repair_review_state")
            self.assertEqual(action["reason"], "telegram_reminder_receipt_count_mismatch")

    def test_delayed_first_phone_call_preserves_repeat_interval(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bindings = root / "farplane" / "bindings.yaml"
            bindings.parent.mkdir(parents=True)
            bindings.write_text(
                """operator:
  review_chase_policy:
    timezone: UTC
    active_hours: {start: '00:00', end: '23:59'}
    pulse_interval_minutes: 30
    telegram_reminder_after_unanswered_turns: [2, 4]
    phone_chaser_after_unanswered_turns: [6, 12]
    phone_chaser_repeat_after_turns: 6
    telegram_reminder_limit: 2
    phone_chaser_limit: 2
""",
                encoding="utf-8",
            )
            write_ticket(
                root,
                "TASK-REVIEW",
                status="awaiting_review",
                review_state={
                    "artifact_refs": ["tickets/TASK-REVIEW/artifacts/example.md"],
                    "thread_ref": "thread-1",
                    "requested_at": "2026-07-11T00:00:00Z",
                    "telegram_status": "sent",
                    "telegram_message_id": "telegram-1",
                    "reminder_count": 2,
                    "telegram_reminder_message_ids": ["telegram-2", "telegram-3"],
                    "phone_chaser_count": 1,
                    "phone_chaser_dispatch_ids": ["call-1"],
                    "last_phone_chaser_at": "2026-07-11T06:00:00Z",
                    "decision": None,
                },
            )

            result = BOARD.build_board(root, now=datetime(2026, 7, 11, 6, 30, tzinfo=timezone.utc))

            self.assertIsNone(result["next_due_review_action"])

    def test_malformed_review_counter_becomes_repair_action(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(
                root,
                "TASK-REVIEW",
                status="awaiting_review",
                review_state={
                    "artifact_refs": ["tickets/TASK-REVIEW/artifacts/example.md"],
                    "thread_ref": "thread-1",
                    "requested_at": "2026-07-11T00:00:00Z",
                    "telegram_status": "sent",
                    "telegram_message_id": "telegram-1",
                    "reminder_count": "nope",
                    "phone_chaser_count": 0,
                    "decision": None,
                },
            )

            result = BOARD.build_board(root, now=datetime(2026, 7, 11, 1, tzinfo=timezone.utc))

            action = result["next_due_review_action"]["review"]
            self.assertEqual(action["action"], "repair_review_state")
            self.assertEqual(action["reason"], "invalid_review_counter")

    def test_malformed_numeric_policy_uses_safe_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bindings = root / "farplane" / "bindings.yaml"
            bindings.parent.mkdir(parents=True)
            bindings.write_text(
                """operator:
  review_chase_policy:
    timezone: UTC
    active_hours: {start: '00:00', end: '23:59'}
    pulse_interval_minutes: nope
    telegram_reminder_after_unanswered_turns: [2, 4]
    phone_chaser_after_unanswered_turns: [6, 12]
    phone_chaser_repeat_after_turns: nope
    telegram_reminder_limit: nope
    phone_chaser_limit: nope
""",
                encoding="utf-8",
            )
            write_ticket(
                root,
                "TASK-REVIEW",
                status="awaiting_review",
                review_state={
                    "artifact_refs": ["tickets/TASK-REVIEW/artifacts/example.md"],
                    "thread_ref": "thread-1",
                    "requested_at": "2026-07-11T00:00:00Z",
                    "telegram_status": "sent",
                    "telegram_message_id": "telegram-1",
                    "reminder_count": 0,
                    "phone_chaser_count": 0,
                    "decision": None,
                },
            )

            result = BOARD.build_board(root, now=datetime(2026, 7, 11, 1, tzinfo=timezone.utc))

            self.assertEqual(
                result["next_due_review_action"]["review"]["action"],
                "send_telegram_reminder",
            )

    def test_phone_receipt_count_and_timestamp_are_required(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ticket = write_ticket(
                root,
                "TASK-REVIEW",
                status="awaiting_review",
                review_state={
                    "artifact_refs": ["tickets/TASK-REVIEW/artifacts/example.md"],
                    "thread_ref": "thread-1",
                    "requested_at": "2026-07-11T00:00:00Z",
                    "telegram_status": "sent",
                    "telegram_message_id": "telegram-1",
                    "reminder_count": 2,
                    "telegram_reminder_message_ids": ["telegram-2", "telegram-3"],
                    "phone_chaser_count": 1,
                    "phone_chaser_dispatch_ids": [],
                    "decision": None,
                },
            )
            result = BOARD.build_board(root, now=datetime(2026, 7, 11, 6, tzinfo=timezone.utc))
            self.assertEqual(
                result["next_due_review_action"]["review"]["reason"],
                "phone_chaser_receipt_count_mismatch",
            )

            progress = ticket.parent / "progress.md"
            progress.write_text(
                progress.read_text(encoding="utf-8").replace(
                    "phone_chaser_dispatch_ids: []",
                    'phone_chaser_dispatch_ids: ["call-1"]',
                ),
                encoding="utf-8",
            )
            result = BOARD.build_board(root, now=datetime(2026, 7, 11, 6, tzinfo=timezone.utc))
            self.assertEqual(
                result["next_due_review_action"]["review"]["reason"],
                "missing_last_phone_chaser_at",
            )

    def test_phone_chaser_is_held_outside_active_hours_and_stops_at_cap(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bindings = root / "farplane" / "bindings.yaml"
            bindings.parent.mkdir(parents=True)
            bindings.write_text(
                """operator:
  review_chase_policy:
    timezone: Asia/Kuala_Lumpur
    active_hours: {start: '10:00', end: '01:00'}
    pulse_interval_minutes: 30
    telegram_reminder_after_unanswered_turns: [2, 4]
    phone_chaser_after_unanswered_turns: [6, 12]
    phone_chaser_repeat_after_turns: 6
    telegram_reminder_limit: 2
    phone_chaser_limit: 2
""",
                encoding="utf-8",
            )
            ticket = write_ticket(
                root,
                "TASK-REVIEW",
                status="awaiting_review",
                review_state={
                    "artifact_refs": ["tickets/TASK-REVIEW/artifacts/example.md"],
                    "thread_ref": "thread-1",
                    "requested_at": "2026-07-10T16:00:00Z",
                    "telegram_status": "sent",
                    "telegram_message_id": "telegram-1",
                    "reminder_count": 2,
                    "telegram_reminder_message_ids": ["telegram-2", "telegram-3"],
                    "phone_chaser_count": 0,
                    "phone_chaser_dispatch_ids": [],
                    "decision": None,
                },
            )

            result = BOARD.build_board(root, now=datetime(2026, 7, 10, 19, tzinfo=timezone.utc))
            self.assertIsNone(result["next_due_review_action"])
            self.assertEqual(
                result["held_review_chases"][0]["review"]["held_action"],
                "dispatch_phone_chaser",
            )

            progress = ticket.parent / "progress.md"
            progress.write_text(
                progress.read_text(encoding="utf-8")
                .replace("phone_chaser_count: 0", "phone_chaser_count: 2")
                .replace(
                    "phone_chaser_dispatch_ids: []",
                    'phone_chaser_dispatch_ids: ["call-1", "call-2"]',
                )
                .replace("decision: null", "last_phone_chaser_at: 2026-07-10T18:00:00Z\ndecision: null"),
                encoding="utf-8",
            )
            result = BOARD.build_board(root, now=datetime(2026, 7, 11, 4, tzinfo=timezone.utc))
            self.assertIsNone(result["next_due_review_action"])
            self.assertEqual(result["held_review_chases"], [])

    def test_awaiting_review_releases_stale_active_association_row(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "TASK-REVIEW", status="awaiting_review")
            write_associations(root, [{"ticket_id": "TASK-REVIEW", "thread_id": "thread-review"}])

            result = BOARD.build_board(root, worker_limit=1)

            self.assertEqual(result["active_workers"], [])
            self.assertEqual(result["idle_worker_slots"], 1)
            self.assertEqual(result["released_worker_rows"][0]["release_reason"], "ticket_status:awaiting_review")

    def test_missing_active_ticket_releases_stale_active_association_row(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_associations(root, [{"ticket_id": "TASK-ARCHIVED", "thread_id": "thread-archived"}])

            result = BOARD.build_board(root, worker_limit=1)

            self.assertEqual(result["active_workers"], [])
            self.assertEqual(result["idle_worker_slots"], 1)
            self.assertEqual(result["released_worker_rows"][0]["release_reason"], "ticket_not_active")


if __name__ == "__main__":
    unittest.main()
