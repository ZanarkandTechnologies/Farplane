from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from user_turn import (
    append_conversation_assistant_response,
    append_conversation_user_turn,
    build_runtime_claim,
    capture_user_turn,
    conversation_window_path,
    current_run_state_path,
    has_explicit_impl_invocation,
    is_internal_user_prompt,
    load_current_run,
    load_runtime_claim,
    normalize_user_turn,
    recent_conversation_windows,
    session_state_path,
    should_review_skill_opportunities,
    skill_opportunity_application_dir,
)


class RuntimeClaimTests(unittest.TestCase):
    def test_has_explicit_impl_invocation_requires_exact_impl_token(self) -> None:
        self.assertTrue(has_explicit_impl_invocation("$impl TASK-0061"))
        self.assertTrue(has_explicit_impl_invocation("please $impl TASK-0061"))
        self.assertTrue(has_explicit_impl_invocation("please $impl, continue TASK-0061"))
        self.assertFalse(has_explicit_impl_invocation("$impl-plan TASK-0061"))
        self.assertFalse(has_explicit_impl_invocation("$impl-plan-extra TASK-0061"))
        self.assertFalse(has_explicit_impl_invocation("impl TASK-0061"))

    def test_normalize_user_turn_detects_qa_and_demo_execution_phases(self) -> None:
        qa = normalize_user_turn(
            "$qa TASK-0061",
            turn_id="turn-qa",
            source="test",
            captured_at="2026-04-24T00:00:00Z",
        )
        demo = normalize_user_turn(
            "$demo TASK-0061",
            turn_id="turn-demo",
            source="test",
            captured_at="2026-04-24T00:00:00Z",
        )

        self.assertEqual(qa["control_surface"], "qa")
        self.assertEqual(qa["requested_execution_phase"], "qa")
        self.assertEqual(qa["requested_outcome"], "qa_pass")
        self.assertEqual(demo["control_surface"], "demo")
        self.assertEqual(demo["requested_execution_phase"], "demo")
        self.assertEqual(demo["requested_outcome"], "demo_pass")

    def test_normalize_user_turn_keeps_impl_plan_out_of_impl_loop(self) -> None:
        normalized = normalize_user_turn(
            "$impl-plan TASK-0061",
            turn_id="turn-plan",
            source="test",
            captured_at="2026-04-13T00:00:00Z",
        )

        self.assertEqual(normalized["control_surface"], "impl-plan")
        self.assertFalse(normalized["explicit_impl_requested"])
        self.assertEqual(normalized["intent_mode"], "planning")
        self.assertEqual(normalized["requested_outcome"], "ticket_plan")

    def test_normalize_user_turn_rejects_hyphen_suffixed_skill_lookalikes(self) -> None:
        normalized = normalize_user_turn(
            "$impl-plan-extra TASK-0061",
            turn_id="turn-invalid",
            source="test",
            captured_at="2026-04-13T00:00:00Z",
        )

        self.assertEqual(normalized["control_surface"], "")
        self.assertFalse(normalized["explicit_impl_requested"])
        self.assertEqual(normalized["intent_mode"], "unknown")

    def test_normalize_user_turn_uses_close_ticket_as_canonical_closeout_name(self) -> None:
        normalized = normalize_user_turn(
            "$close-ticket TASK-0061",
            turn_id="turn-close",
            source="test",
            captured_at="2026-04-13T00:00:00Z",
        )

        self.assertEqual(normalized["control_surface"], "close-ticket")
        self.assertEqual(normalized["intent_mode"], "documenting")
        self.assertEqual(normalized["requested_outcome"], "docs_update")

    def test_normalize_user_turn_maps_docs_closeout_alias_to_close_ticket(self) -> None:
        normalized = normalize_user_turn(
            "$docs-closeout TASK-0061",
            turn_id="turn-close-alias",
            source="test",
            captured_at="2026-04-13T00:00:00Z",
        )

        self.assertEqual(normalized["control_surface"], "close-ticket")
        self.assertEqual(normalized["intent_mode"], "documenting")
        self.assertEqual(normalized["requested_outcome"], "docs_update")

    def test_normalize_user_turn_detects_ralph_control_surface_without_impl_loop(self) -> None:
        normalized = normalize_user_turn(
            "$ralph max_loops=5",
            turn_id="turn-ralph",
            source="test",
            captured_at="2026-05-04T00:00:00Z",
        )

        self.assertEqual(normalized["control_surface"], "ralph")
        self.assertEqual(normalized["intent_mode"], "building")
        self.assertEqual(normalized["requested_outcome"], "code_change")
        self.assertEqual(normalized["requested_execution_phase"], "")
        self.assertFalse(normalized["explicit_impl_requested"])

    def test_normalize_user_turn_detects_work_control_surface_without_impl_loop(self) -> None:
        normalized = normalize_user_turn(
            "$work TASK-0178",
            turn_id="turn-work",
            source="test",
            captured_at="2026-05-25T00:00:00Z",
        )

        self.assertEqual(normalized["control_surface"], "work")
        self.assertEqual(normalized["intent_mode"], "building")
        self.assertEqual(normalized["requested_outcome"], "code_change")
        self.assertEqual(normalized["requested_execution_phase"], "")
        self.assertFalse(normalized["explicit_impl_requested"])

    def test_build_runtime_claim_groups_active_ownership(self) -> None:
        claim = build_runtime_claim(
            {
                "ticket_id": "TASK-0035",
                "ticket_path": "/tmp/TASK-0035.md",
                "run_id": "run-task-0035-building-01",
                "phase": "building",
                "status": "running",
                "skill_name": "impl",
                "worker_name": "builder",
                "main_artifact_path": "/tmp/TASK-0035.md",
                "grounding_summary": "reviewing TASK-0035 acceptance criteria",
                "worker_started_at": "2026-04-08T14:59:00Z",
                "last_checkpoint_at": "2026-04-08T15:00:00Z",
                "checkpoint_summary": "worker launched",
                "session_id": "sess-123",
                "tmux_session": "main",
                "tmux_window": "@5",
                "tmux_pane": "%9",
                "updated_at": "2026-04-08T15:00:00Z",
            }
        )

        self.assertEqual(
            claim,
            {
                "ticket_id": "TASK-0035",
                "ticket_path": "/tmp/TASK-0035.md",
                "run_id": "run-task-0035-building-01",
                "claimed_at": "2026-04-08T15:00:00Z",
                "phase": "building",
                "status": "running",
                "skill_name": "impl",
                "worker_name": "builder",
                "main_artifact_path": "/tmp/TASK-0035.md",
                "grounding_summary": "reviewing TASK-0035 acceptance criteria",
                "worker_started_at": "2026-04-08T14:59:00Z",
                "last_checkpoint_at": "2026-04-08T15:00:00Z",
                "checkpoint_summary": "worker launched",
                "session_id": "sess-123",
                "tmux_session": "main",
                "tmux_window": "@5",
                "tmux_pane": "%9",
            },
        )

    def test_build_runtime_claim_preserves_existing_claimed_at(self) -> None:
        claim = build_runtime_claim(
            {
                "ticket_id": "TASK-0035",
                "run_id": "run-task-0035-building-01",
                "phase": "building",
                "status": "waiting_for_judge",
                "updated_at": "2026-04-08T16:00:00Z",
                "claim": {
                    "ticket_id": "TASK-0035",
                    "run_id": "run-task-0035-building-01",
                    "claimed_at": "2026-04-08T15:00:00Z",
                    "phase": "building",
                    "status": "running",
                },
            }
        )

        self.assertIsNotNone(claim)
        self.assertEqual(claim["claimed_at"], "2026-04-08T15:00:00Z")
        self.assertEqual(claim["status"], "waiting_for_judge")

    def test_load_runtime_claim_prefers_nested_run_state_claim(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            state_dir = project_root / ".harness" / "state"
            state_dir.mkdir(parents=True, exist_ok=True)
            run_state = project_root / ".harness" / "runs" / "task-0035-building.json"
            run_state.parent.mkdir(parents=True, exist_ok=True)
            run_state.write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-0035",
                        "run_id": "run-task-0035-building-01",
                        "phase": "building",
                        "status": "running",
                        "claim": {
                            "ticket_id": "TASK-0035",
                            "run_id": "run-task-0035-building-01",
                            "claimed_at": "2026-04-08T15:00:00Z",
                            "phase": "building",
                            "status": "running",
                            "session_id": "sess-123",
                        },
                    }
                ),
                encoding="utf-8",
            )
            (state_dir / "current-run.json").write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-0035",
                        "run_id": "run-task-0035-building-01",
                        "phase": "building",
                        "status": "running",
                        "run_state": str(run_state.relative_to(project_root)),
                    }
                ),
                encoding="utf-8",
            )

            claim = load_runtime_claim(project_root)

        self.assertIsNotNone(claim)
        self.assertEqual(claim["session_id"], "sess-123")
        self.assertEqual(claim["claimed_at"], "2026-04-08T15:00:00Z")

    def test_load_current_run_prefers_session_state_over_global_pointer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            state_dir = project_root / ".harness" / "state"
            state_dir.mkdir(parents=True, exist_ok=True)
            session_path = session_state_path(project_root, "sess-123")
            session_path.parent.mkdir(parents=True, exist_ok=True)
            session_path.write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-1234",
                        "run_id": "run-task-1234-building-01",
                        "phase": "building",
                        "status": "running",
                        "session_id": "sess-123",
                        "last_user_turn": {"turn_id": "turn-a", "raw_text": "build task 1234"},
                    }
                ),
                encoding="utf-8",
            )
            (state_dir / "current-run.json").write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-9999",
                        "run_id": "run-task-9999-building-01",
                        "phase": "building",
                        "status": "running",
                        "session_id": "sess-other",
                    }
                ),
                encoding="utf-8",
            )

            current = load_current_run(project_root, session_id="sess-123")

        self.assertIsNotNone(current)
        assert current is not None
        self.assertEqual(current["ticket_id"], "TASK-1234")
        self.assertEqual(current["session_id"], "sess-123")

    def test_load_current_run_falls_through_session_stub_to_same_session_global_run_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            state_dir = project_root / ".harness" / "state"
            state_dir.mkdir(parents=True, exist_ok=True)
            run_state = project_root / ".harness" / "runs" / "task-0016-building.json"
            run_state.parent.mkdir(parents=True, exist_ok=True)
            run_state.write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-0016",
                        "ticket_path": str(project_root / "tickets" / "TASK-0016" / "ticket.md"),
                        "run_id": "run-task-0016-building-01",
                        "phase": "building",
                        "status": "running",
                        "skill_name": "impl",
                        "session_id": "sess-123",
                        "impl_loop_active": True,
                    }
                ),
                encoding="utf-8",
            )
            session_path = session_state_path(project_root, "sess-123")
            session_path.parent.mkdir(parents=True, exist_ok=True)
            session_path.write_text(
                json.dumps(
                    {
                        "session_id": "sess-123",
                        "session_origin": "control",
                        "last_user_turn": {
                            "turn_id": "turn-a",
                            "raw_text": "please $impl this",
                            "control_surface": "impl",
                            "explicit_impl_requested": True,
                        },
                        "impl_loop_active": True,
                    }
                ),
                encoding="utf-8",
            )
            (state_dir / "current-run.json").write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-0016",
                        "ticket_path": str(project_root / "tickets" / "TASK-0016" / "ticket.md"),
                        "run_id": "run-task-0016-building-01",
                        "phase": "building",
                        "status": "running",
                        "skill_name": "impl",
                        "session_id": "sess-123",
                        "run_state": str(run_state.relative_to(project_root)),
                        "impl_loop_active": True,
                    }
                ),
                encoding="utf-8",
            )

            current = load_current_run(project_root, session_id="sess-123")

        self.assertIsNotNone(current)
        assert current is not None
        self.assertEqual(current["ticket_id"], "TASK-0016")
        self.assertEqual(current["run_state"], str(run_state.relative_to(project_root)))
        self.assertEqual(current["skill_name"], "impl")

    def test_load_current_run_explicit_run_state_outranks_session_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            run_state = project_root / ".harness" / "runs" / "task-0042-building.json"
            run_state.parent.mkdir(parents=True, exist_ok=True)
            run_state.write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-0042",
                        "run_id": "run-task-0042-building-01",
                        "phase": "building",
                        "status": "running",
                    }
                ),
                encoding="utf-8",
            )
            session_path = session_state_path(project_root, "sess-123")
            session_path.parent.mkdir(parents=True, exist_ok=True)
            session_path.write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-9999",
                        "run_id": "run-task-9999-building-01",
                        "phase": "building",
                        "status": "running",
                        "session_id": "sess-123",
                    }
                ),
                encoding="utf-8",
            )

            current = load_current_run(
                project_root,
                session_id="sess-123",
                explicit_run_state=str(run_state.relative_to(project_root)),
            )

        self.assertIsNotNone(current)
        assert current is not None
        self.assertEqual(current["ticket_id"], "TASK-0042")
        self.assertEqual(current["run_state"], str(run_state.relative_to(project_root)))

    def test_load_current_run_ignores_retired_runtime_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            state_dir = project_root / ".retired-runtime" / "state"
            state_dir.mkdir(parents=True, exist_ok=True)
            (state_dir / "current-run.json").write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-7777",
                        "run_id": "run-task-7777-building-01",
                        "phase": "building",
                        "status": "running",
                    }
                ),
                encoding="utf-8",
            )

            current = load_current_run(project_root)

        self.assertIsNone(current)

    def test_capture_user_turn_initializes_control_session_and_current_run_without_existing_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            (project_root / ".harness" / "state").mkdir(parents=True, exist_ok=True)

            captured = capture_user_turn(
                project_root=project_root,
                raw_text="okay please $impl",
                turn_id="turn-init",
                source="test",
                session_id="sess-init",
            )

            session_payload = json.loads(session_state_path(project_root, "sess-init").read_text(encoding="utf-8"))
            current_run = json.loads(current_run_state_path(project_root).read_text(encoding="utf-8"))

        self.assertIsNotNone(captured)
        assert captured is not None
        self.assertEqual(session_payload["session_id"], "sess-init")
        self.assertEqual(session_payload["session_name"], "agent-01")
        self.assertEqual(session_payload["last_user_turn"]["turn_id"], "turn-init")
        self.assertEqual(session_payload["session_origin"], "control")
        self.assertEqual(current_run["session_id"], "sess-init")
        self.assertEqual(current_run["session_origin"], "control")

    def test_conversation_window_pairs_user_and_assistant_turns(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            user_turn = normalize_user_turn(
                "$impl-plan TASK-0104",
                turn_id="turn-1",
                source="test",
                captured_at="2026-05-08T00:00:00Z",
            )

            append_conversation_user_turn(project_root, "sess-window", user_turn)
            window = append_conversation_assistant_response(
                project_root,
                "sess-window",
                "plan complete",
                captured_at="2026-05-08T00:00:01Z",
                source="test-stop",
            )
            self.assertTrue(skill_opportunity_application_dir(project_root).is_dir())

        self.assertEqual(window["turn_count"], 1)
        self.assertEqual(window["pending_user_turn"], {})
        self.assertEqual(len(window["rolling_exchanges"]), 1)
        exchange = window["rolling_exchanges"][0]
        self.assertEqual(exchange["user_turn_id"], "turn-1")
        self.assertEqual(exchange["assistant_text"], "plan complete")
        self.assertEqual(exchange["assistant_source"], "test-stop")

    def test_conversation_window_trims_to_last_ten_exchanges_and_tracks_cadence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            (project_root / ".harness" / "state").mkdir(parents=True, exist_ok=True)
            for index in range(12):
                user_turn = normalize_user_turn(
                    f"$impl-plan TASK-{index:04d}",
                    turn_id=f"turn-{index}",
                    source="test",
                    captured_at=f"2026-05-08T00:00:{index:02d}Z",
                )
                append_conversation_user_turn(project_root, "sess-window", user_turn)
                window = append_conversation_assistant_response(
                    project_root,
                    "sess-window",
                    f"response {index}",
                    captured_at=f"2026-05-08T00:01:{index:02d}Z",
                    source="test-stop",
                )

            saved = json.loads(conversation_window_path(project_root, "sess-window").read_text(encoding="utf-8"))

        self.assertEqual(window["turn_count"], 12)
        self.assertEqual(len(window["rolling_exchanges"]), 10)
        self.assertEqual(window["rolling_exchanges"][0]["user_turn_id"], "turn-2")
        self.assertEqual(saved["rolling_exchanges"][-1]["assistant_text"], "response 11")
        trigger = should_review_skill_opportunities(window, cadence=10)
        self.assertTrue(trigger["due"])
        self.assertEqual(trigger["turn_count"], 12)

    def test_recent_conversation_windows_prefers_current_then_recent_sessions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            for index, session_id in enumerate(("sess-a", "sess-current", "sess-c")):
                user_turn = normalize_user_turn(
                    f"$impl-plan TASK-{index:04d}",
                    turn_id=f"turn-{index}",
                    source="test",
                    captured_at=f"2026-05-08T00:00:0{index}Z",
                )
                append_conversation_user_turn(project_root, session_id, user_turn)
                append_conversation_assistant_response(
                    project_root,
                    session_id,
                    f"response {index}",
                    captured_at=f"2026-05-08T00:01:0{index}Z",
                    source="test-stop",
                )

            windows = recent_conversation_windows(project_root, current_session_id="sess-current", limit=2)

        self.assertEqual([window["session_id"] for window in windows], ["sess-current", "sess-c"])

    def test_capture_user_turn_impl_plan_stays_control_but_does_not_activate_impl_loop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            (project_root / ".harness" / "state").mkdir(parents=True, exist_ok=True)

            captured = capture_user_turn(
                project_root=project_root,
                raw_text="please $impl-plan TASK-0061",
                turn_id="turn-plan",
                source="test",
                session_id="sess-plan",
            )

            session_payload = json.loads(session_state_path(project_root, "sess-plan").read_text(encoding="utf-8"))
            current_run = json.loads(current_run_state_path(project_root).read_text(encoding="utf-8"))

        self.assertIsNotNone(captured)
        assert captured is not None
        self.assertEqual(captured["control_surface"], "impl-plan")
        self.assertFalse(captured["explicit_impl_requested"])
        self.assertEqual(captured["intent_mode"], "planning")
        self.assertFalse(session_payload["impl_loop_active"])
        self.assertFalse(current_run["impl_loop_active"])

    def test_capture_user_turn_explicit_impl_seeds_unambiguous_active_ticket_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            state_dir = project_root / ".harness" / "state"
            state_dir.mkdir(parents=True, exist_ok=True)
            ticket_path = project_root / "tickets" / "TASK-0016" / "ticket.md"
            ticket_path.parent.mkdir(parents=True, exist_ok=True)
            ticket_path.write_text(
                """---
ticket_id: TASK-0016
title: example
phase: building
status: building
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-10T00:00:00Z
updated_at: 2026-04-10T00:00:00Z
next_action: continue implementation
last_verification: none
linked_docs: []
---

# TASK-0016: example
""",
                encoding="utf-8",
            )

            captured = capture_user_turn(
                project_root=project_root,
                raw_text="please $impl this",
                turn_id="turn-impl-seed",
                source="test",
                session_id="sess-seed",
            )

            session_payload = json.loads(session_state_path(project_root, "sess-seed").read_text(encoding="utf-8"))
            current_run = json.loads(current_run_state_path(project_root).read_text(encoding="utf-8"))

        self.assertIsNotNone(captured)
        assert captured is not None
        self.assertTrue(captured["explicit_impl_requested"])
        self.assertEqual(session_payload["ticket_id"], "TASK-0016")
        self.assertEqual(session_payload["current_ticket_id"], "TASK-0016")
        self.assertEqual(session_payload["phase"], "building")
        self.assertEqual(session_payload["status"], "running")
        self.assertEqual(session_payload["skill_name"], "impl")
        self.assertEqual(session_payload["execution_phase"], "impl")
        self.assertTrue(session_payload["requires_qa"])
        self.assertFalse(session_payload["requires_demo"])
        self.assertIn("qa", session_payload["phase_requirements"])
        self.assertTrue(session_payload["impl_loop_active"])
        self.assertEqual(current_run["ticket_id"], "TASK-0016")
        self.assertEqual(current_run["claim"]["ticket_id"], "TASK-0016")
        self.assertEqual(current_run["claim"]["session_id"], "sess-seed")

    def test_capture_user_turn_ralph_stays_control_without_activating_impl_loop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            (project_root / ".harness" / "state").mkdir(parents=True, exist_ok=True)

            captured = capture_user_turn(
                project_root=project_root,
                raw_text="$ralph max_loops=3",
                turn_id="turn-ralph-seed",
                source="test",
                session_id="sess-ralph",
            )

            session_payload = json.loads(session_state_path(project_root, "sess-ralph").read_text(encoding="utf-8"))
            current_run = json.loads(current_run_state_path(project_root).read_text(encoding="utf-8"))

        self.assertIsNotNone(captured)
        assert captured is not None
        self.assertEqual(captured["control_surface"], "ralph")
        self.assertEqual(session_payload["session_origin"], "control")
        self.assertFalse(session_payload["impl_loop_active"])
        self.assertFalse(current_run["impl_loop_active"])
        self.assertNotIn("claim", current_run)

    def test_capture_user_turn_work_stays_control_without_activating_impl_loop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            (project_root / ".harness" / "state").mkdir(parents=True, exist_ok=True)

            captured = capture_user_turn(
                project_root=project_root,
                raw_text="$work TASK-0178",
                turn_id="turn-work-seed",
                source="test",
                session_id="sess-work",
            )

            session_payload = json.loads(session_state_path(project_root, "sess-work").read_text(encoding="utf-8"))
            current_run = json.loads(current_run_state_path(project_root).read_text(encoding="utf-8"))

        self.assertIsNotNone(captured)
        assert captured is not None
        self.assertEqual(captured["control_surface"], "work")
        self.assertEqual(session_payload["session_origin"], "control")
        self.assertFalse(session_payload["impl_loop_active"])
        self.assertFalse(current_run["impl_loop_active"])
        self.assertNotIn("claim", current_run)

    def test_capture_user_turn_ignores_non_control_session_without_existing_origin(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            (project_root / ".harness" / "state").mkdir(parents=True, exist_ok=True)

            captured = capture_user_turn(
                project_root=project_root,
                raw_text="what is active in this repo?",
                turn_id="turn-plain",
                source="test",
                session_id="sess-plain",
            )

        self.assertIsNone(captured)
        self.assertFalse(session_state_path(project_root, "sess-plain").exists())
        self.assertFalse(current_run_state_path(project_root).exists())

    def test_capture_user_turn_requires_dollar_prefixed_control_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            (project_root / ".harness" / "state").mkdir(parents=True, exist_ok=True)

            captured = capture_user_turn(
                project_root=project_root,
                raw_text="impl TASK-0061",
                turn_id="turn-no-dollar",
                source="test",
                session_id="sess-no-dollar",
            )

        self.assertIsNone(captured)
        self.assertFalse(session_state_path(project_root, "sess-no-dollar").exists())
        self.assertFalse(current_run_state_path(project_root).exists())

    def test_capture_user_turn_rejects_hyphen_suffixed_skill_lookalike(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            (project_root / ".harness" / "state").mkdir(parents=True, exist_ok=True)

            captured = capture_user_turn(
                project_root=project_root,
                raw_text="$impl-plan-extra TASK-0061",
                turn_id="turn-invalid-skill",
                source="test",
                session_id="sess-invalid-skill",
            )

        self.assertIsNone(captured)
        self.assertFalse(session_state_path(project_root, "sess-invalid-skill").exists())
        self.assertFalse(current_run_state_path(project_root).exists())

    def test_capture_user_turn_writes_claimed_by_to_ticket(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            state_dir = project_root / ".harness" / "state"
            state_dir.mkdir(parents=True, exist_ok=True)
            ticket_path = project_root / "tickets" / "TASK-1234" / "ticket.md"
            ticket_path.parent.mkdir(parents=True, exist_ok=True)
            ticket_path.write_text(
                """---
ticket_id: TASK-1234
title: example
phase: building
status: building
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-10T00:00:00Z
updated_at: 2026-04-10T00:00:00Z
next_action: continue implementation
last_verification: none
linked_docs: []
---

# TASK-1234: example
""",
                encoding="utf-8",
            )
            session_path = session_state_path(project_root, "sess-123")
            session_path.parent.mkdir(parents=True, exist_ok=True)
            session_path.write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-1234",
                        "ticket_path": str(ticket_path),
                        "run_id": "run-task-1234-building-01",
                        "phase": "building",
                        "status": "running",
                        "session_id": "sess-123",
                        "session_origin": "control",
                    }
                ),
                encoding="utf-8",
            )
            (state_dir / "current-run.json").write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-1234",
                        "ticket_path": str(ticket_path),
                        "run_id": "run-task-1234-building-01",
                        "phase": "building",
                        "status": "running",
                        "session_id": "sess-123",
                        "session_origin": "control",
                    }
                ),
                encoding="utf-8",
            )

            capture_user_turn(
                project_root=project_root,
                raw_text="continue TASK-1234",
                turn_id="turn-claim",
                source="test",
                session_id="sess-123",
            )

            ticket_text = ticket_path.read_text(encoding="utf-8")
            session_payload = json.loads(session_path.read_text(encoding="utf-8"))

        self.assertIn("claimed_by: agent-01", ticket_text)
        self.assertEqual(session_payload["session_name"], "agent-01")
        self.assertEqual(session_payload["current_ticket_id"], "TASK-1234")

    def test_capture_user_turn_updates_only_resolved_session_lane(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            state_dir = project_root / ".harness" / "state"
            state_dir.mkdir(parents=True, exist_ok=True)

            run_state_a = project_root / ".harness" / "runs" / "task-0042-building.json"
            run_state_b = project_root / ".harness" / "runs" / "task-0041-planning.json"
            run_state_a.parent.mkdir(parents=True, exist_ok=True)
            run_state_a.write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-0042",
                        "run_id": "run-task-0042-building-01",
                        "phase": "building",
                        "status": "running",
                        "session_id": "sess-a",
                        "last_user_turn": {
                            "turn_id": "turn-a0",
                            "raw_text": "$impl TASK-0042",
                            "control_surface": "impl",
                            "explicit_impl_requested": True,
                        },
                    }
                ),
                encoding="utf-8",
            )
            run_state_b.write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-0041",
                        "run_id": "run-task-0041-planning-01",
                        "phase": "planning",
                        "status": "running",
                        "session_id": "sess-b",
                        "last_user_turn": {"turn_id": "turn-b", "raw_text": "plan task 41"},
                    }
                ),
                encoding="utf-8",
            )
            session_state_a = session_state_path(project_root, "sess-a")
            session_state_b = session_state_path(project_root, "sess-b")
            session_state_a.parent.mkdir(parents=True, exist_ok=True)
            session_state_a.write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-0042",
                        "run_id": "run-task-0042-building-01",
                        "phase": "building",
                        "status": "running",
                        "session_id": "sess-a",
                        "run_state": str(run_state_a.relative_to(project_root)),
                        "last_user_turn": {
                            "turn_id": "turn-a0",
                            "raw_text": "$impl TASK-0042",
                            "control_surface": "impl",
                            "explicit_impl_requested": True,
                        },
                    }
                ),
                encoding="utf-8",
            )
            session_state_b.write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-0041",
                        "run_id": "run-task-0041-planning-01",
                        "phase": "planning",
                        "status": "running",
                        "session_id": "sess-b",
                        "run_state": str(run_state_b.relative_to(project_root)),
                        "last_user_turn": {"turn_id": "turn-b", "raw_text": "plan task 41"},
                    }
                ),
                encoding="utf-8",
            )
            (state_dir / "current-run.json").write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-0041",
                        "run_id": "run-task-0041-planning-01",
                        "phase": "planning",
                        "status": "running",
                        "session_id": "sess-b",
                        "run_state": str(run_state_b.relative_to(project_root)),
                    }
                ),
                encoding="utf-8",
            )

            captured = capture_user_turn(
                project_root=project_root,
                raw_text="Implement TASK-0042 in this session only.",
                turn_id="turn-a",
                source="test",
                session_id="sess-a",
            )

            session_a = json.loads(session_state_a.read_text(encoding="utf-8"))
            session_b = json.loads(session_state_b.read_text(encoding="utf-8"))
            persisted_run_state_a = json.loads(run_state_a.read_text(encoding="utf-8"))

        self.assertIsNotNone(captured)
        assert captured is not None
        self.assertEqual(captured["turn_id"], "turn-a")
        self.assertEqual(session_a["last_user_turn"]["turn_id"], "turn-a")
        self.assertEqual(session_a["last_user_turn"]["raw_text"], "Implement TASK-0042 in this session only.")
        self.assertEqual(session_a["session_origin"], "control")
        self.assertFalse(session_a["impl_loop_active"])
        self.assertEqual(session_a["session_name"], "agent-01")
        self.assertEqual(session_b["last_user_turn"]["turn_id"], "turn-b")
        self.assertNotIn("impl_loop_active", session_b)
        self.assertFalse(persisted_run_state_a["impl_loop_active"])
        self.assertEqual(persisted_run_state_a["last_user_turn"]["turn_id"], "turn-a")

    def test_capture_user_turn_explicit_impl_activates_only_resolved_session_lane(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            state_dir = project_root / ".harness" / "state"
            state_dir.mkdir(parents=True, exist_ok=True)

            run_state_a = project_root / ".harness" / "runs" / "task-0042-building.json"
            run_state_b = project_root / ".harness" / "runs" / "task-0041-planning.json"
            run_state_a.parent.mkdir(parents=True, exist_ok=True)
            run_state_a.write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-0042",
                        "run_id": "run-task-0042-building-01",
                        "phase": "building",
                        "status": "running",
                        "session_id": "sess-a",
                        "skill_name": "impl",
                    }
                ),
                encoding="utf-8",
            )
            run_state_b.write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-0041",
                        "run_id": "run-task-0041-planning-01",
                        "phase": "planning",
                        "status": "running",
                        "session_id": "sess-b",
                        "last_user_turn": {"turn_id": "turn-b", "raw_text": "plan task 41"},
                    }
                ),
                encoding="utf-8",
            )
            session_state_a = session_state_path(project_root, "sess-a")
            session_state_b = session_state_path(project_root, "sess-b")
            session_state_a.parent.mkdir(parents=True, exist_ok=True)
            session_state_a.write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-0042",
                        "run_id": "run-task-0042-building-01",
                        "phase": "building",
                        "status": "running",
                        "skill_name": "impl",
                        "session_id": "sess-a",
                        "run_state": str(run_state_a.relative_to(project_root)),
                    }
                ),
                encoding="utf-8",
            )
            session_state_b.write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-0041",
                        "run_id": "run-task-0041-planning-01",
                        "phase": "planning",
                        "status": "running",
                        "session_id": "sess-b",
                        "run_state": str(run_state_b.relative_to(project_root)),
                        "last_user_turn": {"turn_id": "turn-b", "raw_text": "plan task 41"},
                    }
                ),
                encoding="utf-8",
            )
            (state_dir / "current-run.json").write_text(
                json.dumps(
                    {
                        "ticket_id": "TASK-0041",
                        "run_id": "run-task-0041-planning-01",
                        "phase": "planning",
                        "status": "running",
                        "session_id": "sess-b",
                        "run_state": str(run_state_b.relative_to(project_root)),
                    }
                ),
                encoding="utf-8",
            )

            captured = capture_user_turn(
                project_root=project_root,
                raw_text="$impl TASK-0042 in this session only.",
                turn_id="turn-impl",
                source="test",
                session_id="sess-a",
            )

            session_a = json.loads(session_state_a.read_text(encoding="utf-8"))
            session_b = json.loads(session_state_b.read_text(encoding="utf-8"))
            persisted_run_state_a = json.loads(run_state_a.read_text(encoding="utf-8"))

        self.assertIsNotNone(captured)
        assert captured is not None
        self.assertTrue(captured["explicit_impl_requested"])
        self.assertTrue(session_a["impl_loop_active"])
        self.assertEqual(session_a["last_user_turn"]["turn_id"], "turn-impl")
        self.assertEqual(session_a["session_origin"], "control")
        self.assertNotIn("impl_loop_active", session_b)
        self.assertTrue(persisted_run_state_a["impl_loop_active"])

    def test_capture_user_turn_explicit_qa_seeds_execution_phase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            state_dir = project_root / ".harness" / "state"
            state_dir.mkdir(parents=True, exist_ok=True)
            ticket_path = project_root / "tickets" / "TASK-0042" / "ticket.md"
            ticket_path.parent.mkdir(parents=True, exist_ok=True)
            ticket_path.write_text(
                """---
ticket_id: TASK-0042
title: example
phase: building
status: building
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
requires_qa: true
requires_demo: false
created_at: 2026-04-10T00:00:00Z
updated_at: 2026-04-10T00:00:00Z
next_action: run qa
last_verification: none
linked_docs: []
---

# TASK-0042: example
""",
                encoding="utf-8",
            )

            captured = capture_user_turn(
                project_root=project_root,
                raw_text="$qa TASK-0042",
                turn_id="turn-qa",
                source="test",
                session_id="sess-qa",
            )

            session_payload = json.loads(session_state_path(project_root, "sess-qa").read_text(encoding="utf-8"))

        self.assertIsNotNone(captured)
        assert captured is not None
        self.assertEqual(session_payload["skill_name"], "qa")
        self.assertEqual(session_payload["execution_phase"], "qa")
        self.assertTrue(session_payload["requires_qa"])
        self.assertFalse(session_payload["requires_demo"])

    def test_capture_user_turn_explicit_demo_forces_demo_requirement(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            state_dir = project_root / ".harness" / "state"
            state_dir.mkdir(parents=True, exist_ok=True)
            ticket_path = project_root / "tickets" / "TASK-0043" / "ticket.md"
            ticket_path.parent.mkdir(parents=True, exist_ok=True)
            ticket_path.write_text(
                """---
ticket_id: TASK-0043
title: example
phase: building
status: building
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
requires_qa: true
requires_demo: false
created_at: 2026-04-10T00:00:00Z
updated_at: 2026-04-10T00:00:00Z
next_action: run demo
last_verification: none
linked_docs: []
---

# TASK-0043: example
""",
                encoding="utf-8",
            )

            captured = capture_user_turn(
                project_root=project_root,
                raw_text="$demo TASK-0043",
                turn_id="turn-demo",
                source="test",
                session_id="sess-demo",
            )

            session_payload = json.loads(session_state_path(project_root, "sess-demo").read_text(encoding="utf-8"))

        self.assertIsNotNone(captured)
        assert captured is not None
        self.assertEqual(session_payload["skill_name"], "demo")
        self.assertEqual(session_payload["execution_phase"], "demo")
        self.assertTrue(session_payload["requires_qa"])
        self.assertTrue(session_payload["requires_demo"])

    def test_is_internal_user_prompt_rejects_approval_reviewer_requests(self) -> None:
        prompt = (
            "The following is the Codex agent history whose request action you are assessing.\n"
            ">>> APPROVAL REQUEST START\n"
            "Assess the exact planned action below.\n"
        )

        self.assertTrue(is_internal_user_prompt(prompt))

    def test_is_internal_user_prompt_rejects_delegated_read_only_lanes(self) -> None:
        prompt = (
            "TASK-0007 reviewer lane. Inspect the upcoming batch-first enrichment contract changes. "
            "Do not edit files. Return: worker_name, main_artifact_path, grounding_summary, and findings."
        )

        self.assertTrue(is_internal_user_prompt(prompt))

    def test_is_internal_user_prompt_keeps_real_operator_requests(self) -> None:
        prompt = (
            "please investigate why the hook is creating extra runs in "
            "/Users/kenjipcx/60x/ai-brain/.harness and fix the harness bug"
        )

        self.assertFalse(is_internal_user_prompt(prompt))


if __name__ == "__main__":
    unittest.main()
