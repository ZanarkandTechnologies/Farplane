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


def write_ticket(
    root: Path,
    ticket_id: str,
    *,
    status: str = "todo",
    claimed_by: str = "",
    depends_on: list[str] | None = None,
    priority: str = "medium",
    reward_rows: list[dict[str, object]] | None = None,
    review_state: dict[str, object] | None = None,
) -> Path:
    path = root / "tickets" / ticket_id / "ticket.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
                "---",
                f"ticket_id: {ticket_id}",
                f"title: {ticket_id}",
                f"status: {status}",
                f"priority: {priority}",
                f"claimed_by: {claimed_by}",
                f"depends_on: {json.dumps(depends_on or [])}",
                "created_at: 2026-07-01T00:00:00Z",
                "updated_at: 2026-07-01T00:00:00Z",
                "---",
                "",
                f"# {ticket_id}",
                "",
    ]
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
                    f"  - kpi_id: {row.get('kpi_id', 'metric')}",
                    f"    expected_reward: {json.dumps(row.get('expected_reward', 'improve metric'))}",
                    f"    check_in_at: {json.dumps(row.get('check_in_at', ''))}",
                    f"    actual_result: {json.dumps(row.get('actual_result')) if row.get('actual_result') is not None else ''}",
                    f"    reward_score: {json.dumps(row.get('reward_score')) if row.get('reward_score') is not None else ''}",
                    f"    reward_score_reason: {json.dumps(row.get('reward_score_reason')) if row.get('reward_score_reason') is not None else ''}",
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


def run_minimal_pulse_fixture(
    root: Path,
    planner: Callable[[dict[str, str], list[dict[str, object]], int], list[dict[str, str]]],
    *,
    wave_size: int,
    worker_limit: int,
) -> dict[str, object]:
    """Exercise the prompt-owned Pulse boundary without inventing a runtime.

    The real board classifier owns admission. This fixture injects the pure
    planner result, materializes accepted specs as ticket files, reruns
    admission, and applies worker capacity so the composed contract is
    executable in tests.
    """

    board = BOARD.build_board(root, worker_limit=worker_limit)
    planner_calls = 0
    materialized: list[str] = []
    mode = "dispatch_ready"
    if board["empty_executable_board"]:
        mode = "plan_next_wave"
        project_context = {
            name: (root / "farplane" / name).read_text(encoding="utf-8")
            for name in ("harness.md", "goals.yaml", "metrics.yaml")
        }
        ticket_history = [*board["executable_tickets"], *board["excluded_tickets"]]
        specs = planner(project_context, ticket_history, wave_size)
        planner_calls += 1
        for spec in specs[:wave_size]:
            ticket_id = spec["ticket_id"]
            write_ticket(root, ticket_id)
            materialized.append(ticket_id)
        board = BOARD.build_board(root, worker_limit=worker_limit)

    dispatch_limit = min(board["idle_worker_slots"], len(board["executable_tickets"]))
    dispatched = [
        row["ticket_id"] for row in board["executable_tickets"][:dispatch_limit]
    ]
    return {
        "mode": mode,
        "planner_calls": planner_calls,
        "materialized": materialized,
        "dispatched": dispatched,
        "board": board,
    }


class WorkPulseBoardTests(unittest.TestCase):
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
            (farplane / "harness.md").write_text("# Harness\n", encoding="utf-8")
            (farplane / "goals.yaml").write_text("goals: {}\n", encoding="utf-8")
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
                    {"ticket_id": "TASK-PLAN-1"},
                    {"ticket_id": "TASK-PLAN-2"},
                    {"ticket_id": "TASK-PLAN-3"},
                    {"ticket_id": "TASK-PLAN-OVERFLOW"},
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
                ["goals.yaml", "harness.md", "metrics.yaml"],
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

    def test_empty_board_exposes_refill_condition_without_product_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            result = BOARD.build_board(root, worker_limit=2)

            self.assertEqual(result["executable_tickets"], [])
            self.assertTrue(result["empty_executable_board"])
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
            self.assertEqual(result["idle_worker_slots"], 1)
            self.assertFalse(result["empty_executable_board"])

    def test_worker_limit_excludes_released_review_and_blocked_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "TASK-READY")
            write_ticket(root, "TASK-ACTIVE", status="active", claimed_by="codex-active")
            ledger = root / ".farplane" / "automation" / "spawned-threads.jsonl"
            ledger.parent.mkdir(parents=True, exist_ok=True)
            ledger.write_text(
                "\n".join(
                    [
                        json.dumps({"ticket_id": "TASK-ACTIVE", "status": "active"}),
                        json.dumps(
                            {
                                "ticket_id": "TASK-REVIEW",
                                "status": "waiting_human_review",
                            }
                        ),
                        json.dumps({"ticket_id": "TASK-BLOCKED", "status": "blocked"}),
                    ]
                )
                + "\n",
                encoding="utf-8",
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
                        "kpi_id": "conversion",
                        "check_in_at": "2026-07-10T00:00:00Z",
                    },
                    {
                        "kpi_id": "retention",
                        "check_in_at": "2026-07-11T00:00:00Z",
                        "actual_result": "observed",
                    },
                    {
                        "kpi_id": "quality",
                        "check_in_at": "2026-07-12T00:00:00Z",
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
                [row["index"] for row in ticket["due_reward_checkins"]], [0, 1]
            )
            self.assertEqual(
                [row["index"] for row in ticket["future_reward_checkins"]], [2]
            )
            self.assertEqual(result["due_checkin_tickets"][0]["path"], "tickets/TASK-EXPERIMENT/ticket.md")
            self.assertFalse(result["empty_executable_board"])

    def test_due_projection_requires_actual_and_score_and_keeps_safety_gates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            now = datetime(2026, 7, 11, tzinfo=timezone.utc)
            write_ticket(
                root,
                "TASK-PARTIAL",
                status="waiting_signal",
                reward_rows=[
                    {
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
                        "check_in_at": "2026-07-10T00:00:00Z",
                        "actual_result": "observed",
                        "reward_score": 0.8,
                    }
                ],
            )
            write_ticket(
                root,
                "TASK-BLOCKED-CHECKIN",
                status="blocked",
                reward_rows=[{"check_in_at": "2026-07-10T00:00:00Z"}],
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

    def test_due_review_reminder_is_worker_free_and_decision_closes_it(self) -> None:
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
                    "next_reminder_at": "2026-07-10T00:00:00Z",
                    "reminder_count": 0,
                    "escalation_used": False,
                    "decision": None,
                },
            )
            write_ticket(
                root,
                "TASK-DECIDED",
                status="awaiting_review",
                review_state={
                    "thread_ref": "thread-2",
                    "next_reminder_at": "2026-07-10T00:00:00Z",
                    "decision": "approved",
                },
            )

            result = BOARD.build_board(
                root,
                worker_limit=1,
                now=datetime(2026, 7, 11, tzinfo=timezone.utc),
            )

            self.assertEqual(result["next_due_review_reminder"]["ticket_id"], "TASK-REVIEW")
            self.assertEqual(result["due_review_reminder_count"], 1)
            self.assertEqual(result["idle_worker_slots"], 1)
            self.assertEqual(result["active_workers"], [])

    def test_awaiting_review_releases_stale_active_ledger_row(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_ticket(root, "TASK-REVIEW", status="awaiting_review")
            ledger = root / ".farplane" / "automation" / "spawned-threads.jsonl"
            ledger.parent.mkdir(parents=True)
            ledger.write_text(
                json.dumps({"ticket_id": "TASK-REVIEW", "status": "handoff_recorded"}) + "\n",
                encoding="utf-8",
            )

            result = BOARD.build_board(root, worker_limit=1)

            self.assertEqual(result["active_workers"], [])
            self.assertEqual(result["idle_worker_slots"], 1)
            self.assertEqual(result["released_worker_rows"][0]["release_reason"], "ticket_status:awaiting_review")

    def test_missing_active_ticket_releases_stale_active_ledger_row(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            ledger = root / ".farplane" / "automation" / "spawned-threads.jsonl"
            ledger.parent.mkdir(parents=True)
            ledger.write_text(
                json.dumps({"ticket_id": "TASK-ARCHIVED", "status": "active"}) + "\n",
                encoding="utf-8",
            )

            result = BOARD.build_board(root, worker_limit=1)

            self.assertEqual(result["active_workers"], [])
            self.assertEqual(result["idle_worker_slots"], 1)
            self.assertEqual(result["released_worker_rows"][0]["release_reason"], "ticket_not_active")


if __name__ == "__main__":
    unittest.main()
