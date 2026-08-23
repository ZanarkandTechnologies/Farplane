from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_DIR = ROOT / "bin" / "runtime"
if str(RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(RUNTIME_DIR))

from user_turn import (
    append_conversation_user_turn,
    build_runtime_claim,
    capture_user_turn,
    conversation_window_path,
    has_explicit_goal_execution_invocation,
    is_internal_user_prompt,
    normalize_user_turn,
    recent_conversation_windows,
)


class RuntimeClaimTests(unittest.TestCase):
    def test_has_explicit_goal_execution_invocation_requires_exact_goal_advisor_token(self) -> None:
        self.assertTrue(has_explicit_goal_execution_invocation("$goal-advisor TASK-0061"))
        self.assertTrue(has_explicit_goal_execution_invocation("please $goal-advisor TASK-0061"))
        self.assertTrue(has_explicit_goal_execution_invocation("please $goal-advisor, continue TASK-0061"))
        self.assertFalse(has_explicit_goal_execution_invocation("$impl-plan TASK-0061"))
        self.assertFalse(has_explicit_goal_execution_invocation("$impl-plan-extra TASK-0061"))
        self.assertFalse(has_explicit_goal_execution_invocation("impl TASK-0061"))

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

    def test_normalize_user_turn_keeps_impl_plan_out_of_goal_execution_loop(self) -> None:
        normalized = normalize_user_turn(
            "$impl-plan TASK-0061",
            turn_id="turn-plan",
            source="test",
            captured_at="2026-04-13T00:00:00Z",
        )

        self.assertEqual(normalized["control_surface"], "impl-plan")
        self.assertFalse(normalized["explicit_goal_execution_requested"])
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
        self.assertFalse(normalized["explicit_goal_execution_requested"])
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

    def test_normalize_user_turn_does_not_accept_docs_closeout_alias(self) -> None:
        normalized = normalize_user_turn(
            "$docs-closeout TASK-0061",
            turn_id="turn-close-legacy",
            source="test",
            captured_at="2026-04-13T00:00:00Z",
        )

        self.assertEqual(normalized["control_surface"], "")
        self.assertEqual(normalized["intent_mode"], "unknown")
        self.assertEqual(normalized["requested_outcome"], "unknown")

    def test_build_runtime_claim_groups_active_ownership(self) -> None:
        claim = build_runtime_claim(
            {
                "ticket_id": "TASK-0035",
                "ticket_path": "/tmp/TASK-0035.md",
                "run_id": "run-task-0035-building-01",
                "phase": "building",
                "status": "running",
                "skill_name": "goal-advisor",
                "worker_name": "builder",
                "main_artifact_path": "/tmp/TASK-0035.md",
                "grounding_summary": "reviewing TASK-0035 acceptance criteria",
                "worker_started_at": "2026-04-08T14:59:00Z",
                "last_checkpoint_at": "2026-04-08T15:00:00Z",
                "checkpoint_summary": "worker launched",
                "session_id": "sess-123",
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
                "skill_name": "goal-advisor",
                "worker_name": "builder",
                "main_artifact_path": "/tmp/TASK-0035.md",
                "grounding_summary": "reviewing TASK-0035 acceptance criteria",
                "worker_started_at": "2026-04-08T14:59:00Z",
                "last_checkpoint_at": "2026-04-08T15:00:00Z",
                "checkpoint_summary": "worker launched",
                "session_id": "sess-123",
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

    def test_capture_user_turn_does_not_write_runtime_state_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            (project_root / ".farplane" / "state").mkdir(parents=True, exist_ok=True)

            captured = capture_user_turn(
                project_root=project_root,
                raw_text="okay please $goal-advisor",
                turn_id="turn-init",
                source="test",
                session_id="sess-init",
            )

        self.assertIsNotNone(captured)
        assert captured is not None
        self.assertEqual(captured["turn_id"], "turn-init")
        self.assertEqual(captured["control_surface"], "goal-advisor")
        self.assertFalse((project_root / ".farplane" / "state" / "sessions" / "sess-init.json").exists())
        self.assertFalse((project_root / ".farplane" / "state" / "current-run.json").exists())

    def test_conversation_window_promotes_previous_operator_turn(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            user_turn = normalize_user_turn(
                "$impl-plan TASK-0104",
                turn_id="turn-1",
                source="test",
                captured_at="2026-05-08T00:00:00Z",
            )

            append_conversation_user_turn(project_root, "sess-window", user_turn)
            window = append_conversation_user_turn(
                project_root,
                "sess-window",
                normalize_user_turn(
                    "follow-up correction",
                    turn_id="turn-2",
                    source="test",
                    captured_at="2026-05-08T00:00:01Z",
                ),
            )
            self.assertTrue(conversation_window_path(project_root, "sess-window").is_file())

        self.assertEqual(window["turn_count"], 2)
        self.assertEqual(window["pending_user_turn"]["user_turn_id"], "turn-2")
        self.assertEqual(len(window["rolling_exchanges"]), 1)
        exchange = window["rolling_exchanges"][0]
        self.assertEqual(exchange["user_turn_id"], "turn-1")
        self.assertNotIn("assistant_text", exchange)

    def test_conversation_window_preserves_runtime_marker(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            user_turn = normalize_user_turn(
                "Run the eval and report the pass/fail result.",
                turn_id="turn-1",
                source="test",
                captured_at="2026-05-08T00:00:00Z",
                runtime={"kind": "ephemeral", "purpose": "eval", "source": "env"},
            )

            append_conversation_user_turn(project_root, "sess-window", user_turn)
            window = append_conversation_user_turn(
                project_root,
                "sess-window",
                normalize_user_turn(
                    "next operator turn",
                    turn_id="turn-2",
                    source="test",
                    captured_at="2026-05-08T00:00:01Z",
                ),
            )

        self.assertEqual(window["runtime"], {"kind": "ephemeral", "purpose": "eval", "source": "env"})
        exchange = window["rolling_exchanges"][0]
        self.assertEqual(exchange["runtime"], {"kind": "ephemeral", "purpose": "eval", "source": "env"})

    def test_conversation_window_trims_to_last_ten_exchanges(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            (project_root / ".farplane" / "state").mkdir(parents=True, exist_ok=True)
            for index in range(12):
                user_turn = normalize_user_turn(
                    f"$impl-plan TASK-{index:04d}",
                    turn_id=f"turn-{index}",
                    source="test",
                    captured_at=f"2026-05-08T00:00:{index:02d}Z",
                )
                window = append_conversation_user_turn(project_root, "sess-window", user_turn)

            saved = json.loads(conversation_window_path(project_root, "sess-window").read_text(encoding="utf-8"))

        self.assertEqual(window["turn_count"], 12)
        self.assertEqual(len(window["rolling_exchanges"]), 10)
        self.assertEqual(window["rolling_exchanges"][0]["user_turn_id"], "turn-1")
        self.assertEqual(saved["rolling_exchanges"][-1]["user_turn_id"], "turn-10")
        self.assertEqual(saved["pending_user_turn"]["user_turn_id"], "turn-11")

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

            windows = recent_conversation_windows(project_root, current_session_id="sess-current", limit=2)

        self.assertEqual([window["session_id"] for window in windows], ["sess-current", "sess-c"])

    def test_capture_user_turn_impl_plan_stays_control_but_does_not_activate_goal_execution_loop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            (project_root / ".farplane" / "state").mkdir(parents=True, exist_ok=True)

            captured = capture_user_turn(
                project_root=project_root,
                raw_text="please $impl-plan TASK-0061",
                turn_id="turn-plan",
                source="test",
                session_id="sess-plan",
            )

        self.assertIsNotNone(captured)
        assert captured is not None
        self.assertEqual(captured["control_surface"], "impl-plan")
        self.assertFalse(captured["explicit_goal_execution_requested"])
        self.assertEqual(captured["intent_mode"], "planning")
        self.assertFalse((project_root / ".farplane" / "state" / "sessions" / "sess-plan.json").exists())
        self.assertFalse((project_root / ".farplane" / "state" / "current-run.json").exists())

    def test_capture_user_turn_explicit_goal_advisor_seeds_unambiguous_active_ticket_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            state_dir = project_root / ".farplane" / "state"
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
                raw_text="please $goal-advisor this",
                turn_id="turn-execution-seed",
                source="test",
                session_id="sess-seed",
            )

        self.assertIsNotNone(captured)
        assert captured is not None
        self.assertTrue(captured["explicit_goal_execution_requested"])
        self.assertEqual(captured["explicit_ticket_id"], "")
        self.assertFalse((project_root / ".farplane" / "state" / "sessions" / "sess-seed.json").exists())
        self.assertFalse((project_root / ".farplane" / "state" / "current-run.json").exists())

    def test_capture_user_turn_ignores_non_control_session_without_existing_origin(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            (project_root / ".farplane" / "state").mkdir(parents=True, exist_ok=True)

            captured = capture_user_turn(
                project_root=project_root,
                raw_text="what is active in this repo?",
                turn_id="turn-plain",
                source="test",
                session_id="sess-plain",
            )

        self.assertIsNone(captured)
        self.assertFalse((project_root / ".farplane" / "state" / "sessions" / "sess-plain.json").exists())
        self.assertFalse((project_root / ".farplane" / "state" / "current-run.json").exists())

    def test_capture_user_turn_requires_dollar_prefixed_control_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            (project_root / ".farplane" / "state").mkdir(parents=True, exist_ok=True)

            captured = capture_user_turn(
                project_root=project_root,
                raw_text="impl TASK-0061",
                turn_id="turn-no-dollar",
                source="test",
                session_id="sess-no-dollar",
            )

        self.assertIsNone(captured)
        self.assertFalse((project_root / ".farplane" / "state" / "sessions" / "sess-no-dollar.json").exists())
        self.assertFalse((project_root / ".farplane" / "state" / "current-run.json").exists())

    def test_capture_user_turn_rejects_hyphen_suffixed_skill_lookalike(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            (project_root / ".farplane" / "state").mkdir(parents=True, exist_ok=True)

            captured = capture_user_turn(
                project_root=project_root,
                raw_text="$impl-plan-extra TASK-0061",
                turn_id="turn-invalid-skill",
                source="test",
                session_id="sess-invalid-skill",
            )

        self.assertIsNone(captured)
        self.assertFalse((project_root / ".farplane" / "state" / "sessions" / "sess-invalid-skill.json").exists())
        self.assertFalse((project_root / ".farplane" / "state" / "current-run.json").exists())

    def test_capture_user_turn_explicit_qa_seeds_execution_phase(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            state_dir = project_root / ".farplane" / "state"
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

        self.assertIsNotNone(captured)
        assert captured is not None
        self.assertEqual(captured["control_surface"], "qa")
        self.assertEqual(captured["requested_execution_phase"], "qa")
        self.assertFalse((project_root / ".farplane" / "state" / "sessions" / "sess-qa.json").exists())

    def test_capture_user_turn_explicit_demo_forces_demo_requirement(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            state_dir = project_root / ".farplane" / "state"
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

        self.assertIsNotNone(captured)
        assert captured is not None
        self.assertEqual(captured["control_surface"], "demo")
        self.assertEqual(captured["requested_execution_phase"], "demo")
        self.assertFalse((project_root / ".farplane" / "state" / "sessions" / "sess-demo.json").exists())

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
            "/Users/kenjipcx/60x/ai-brain/.farplane and fix the harness bug"
        )

        self.assertFalse(is_internal_user_prompt(prompt))


if __name__ == "__main__":
    unittest.main()
