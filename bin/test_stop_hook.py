#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parent.parent
STOP_HOOK_PATH = ROOT / "bin" / "stop_hook.py"


def load_stop_hook_module():
    bin_dir = str(STOP_HOOK_PATH.parent)
    if bin_dir not in sys.path:
        sys.path.insert(0, bin_dir)
    spec = importlib.util.spec_from_file_location("codexter_stop_hook_test", STOP_HOOK_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load stop hook module from {STOP_HOOK_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class StopHookRoleConfigTests(unittest.TestCase):
    def setUp(self) -> None:
        self.stop_hook = load_stop_hook_module()

    def test_load_role_config_reads_toml_fields(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stop-hook-role-") as td:
            base = Path(td)
            agents = base / "agents"
            agents.mkdir(parents=True)
            (agents / "reviewer.toml").write_text(
                '\n'.join(
                    [
                        'model = "gpt-5.4"',
                        'model_reasoning_effort = "high"',
                        'developer_instructions = """',
                        'You are the reviewer.',
                        '"""',
                        "",
                    ]
                ),
                encoding="utf-8",
            )

            parsed = self.stop_hook.load_role_config(base, "reviewer")

            self.assertEqual(
                parsed,
                {
                    "developer_instructions": "You are the reviewer.",
                    "model": "gpt-5.4",
                    "model_reasoning_effort": "high",
                },
            )

    def test_load_role_config_rejects_missing_instructions(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stop-hook-role-") as td:
            base = Path(td)
            agents = base / "agents"
            agents.mkdir(parents=True)
            (agents / "reviewer.toml").write_text('model = "gpt-5.4"\n', encoding="utf-8")

            parsed = self.stop_hook.load_role_config(base, "reviewer")

            self.assertIsNone(parsed)

    def test_role_command_injects_model_and_instructions(self) -> None:
        cmd = self.stop_hook.role_command(
            Path("/tmp/codexter"),
            Path("/tmp/out.json"),
            {
                "developer_instructions": "Line one\nLine two",
                "model": "gpt-5.4",
                "model_reasoning_effort": "high",
            },
        )

        self.assertIn("-m", cmd)
        self.assertIn("gpt-5.4", cmd)
        self.assertIn('model_reasoning_effort="high"', cmd)
        injected = next(part for part in cmd if part.startswith("developer_instructions="))
        self.assertIn("\\n", injected)
        self.assertIn("Line one", injected)

    def test_parse_role_output_preserves_user_intent_gate_fields(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stop-hook-output-") as td:
            output_path = Path(td) / "review.json"
            output_path.write_text(
                """{
  "action": "continue_same_ticket",
  "reason": "user intent impression failed",
  "continuation_message": "continue the same ticket and address the mismatch",
  "speak": "continuing same ticket",
  "next_ticket_id": "",
  "next_phase": "",
  "overall_score": 4.2,
  "evidence_quality": "pass",
  "integration_readiness": "pass",
  "traceability": "pass",
  "freshness": "pass",
  "user_intent_impression": "fail",
  "user_intent_mismatch_reason": "result undershoots the saved user ask",
  "obvious_next_step_exists": true,
  "next_step_safe": true,
  "obvious_next_step": "update the active ticket with the missing proof and rerun review",
  "user_would_expect_more": true,
  "rerun_required": false,
  "blocking_findings": []
}""",
                encoding="utf-8",
            )

            parsed = self.stop_hook.parse_role_output(output_path)

        assert parsed is not None
        self.assertEqual(parsed["user_intent_impression"], "fail")
        self.assertEqual(parsed["user_intent_mismatch_reason"], "result undershoots the saved user ask")
        self.assertTrue(parsed["obvious_next_step_exists"])
        self.assertEqual(parsed["obvious_next_step"], "update the active ticket with the missing proof and rerun review")
        self.assertTrue(parsed["user_would_expect_more"])


class StopHookReviewerPromptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.stop_hook = load_stop_hook_module()
        self.ticket = {
            "ticket_id": "TASK-0038",
            "title": "normalize stop-hook role configs",
            "phase": "building",
            "status": "building",
            "next_action": "test",
            "acceptance_gaps": [],
            "evidence_gaps": [],
            "blockers": [],
            "review_packet": {"overall_verdict": "pass"},
            "review_packet_missing": [],
            "review_packet_errors": [],
        }
        self.current_run = {
            "claim": {"status": "build_complete"},
            "last_user_turn": {"summary": "ship the change"},
            "last_intent_alignment": "aligned",
            "last_intent_alignment_reason": "matches current turn",
            "last_intent_turn_id": "turn-123",
        }

    def test_reviewer_prompt_completion_gate_includes_review_packet(self) -> None:
        prompt = self.stop_hook.reviewer_prompt(
            "latest response",
            self.ticket,
            self.current_run,
            {"decision": "complete_ticket"},
            mode="completion_gate",
        )

        self.assertIn('"mode": "completion_gate"', prompt)
        self.assertIn('"completion_claim_is_candidate_only": true', prompt)
        self.assertIn('"review_packet"', prompt)
        self.assertIn('"claim"', prompt)
        self.assertIn('"last_intent_alignment"', prompt)

    def test_reviewer_prompt_missing_result_review_excludes_review_packet(self) -> None:
        prompt = self.stop_hook.reviewer_prompt(
            "latest response",
            self.ticket,
            self.current_run,
            None,
            mode="missing_result_review",
        )

        self.assertIn('"mode": "missing_result_review"', prompt)
        self.assertNotIn('"review_packet"', prompt)

    def test_validate_reviewer_gate_requires_completion_fields(self) -> None:
        ok, reason, failures = self.stop_hook.validate_reviewer_gate({"action": "continue_same_ticket"})

        self.assertFalse(ok)
        self.assertIn("completion-gate fields", reason)
        self.assertIn("missing gate field: overall_score", failures)

    def test_validate_reviewer_gate_passes_with_clean_gate(self) -> None:
        ok, reason, failures = self.stop_hook.validate_reviewer_gate(
            {
                "overall_score": 4.6,
                "evidence_quality": "pass",
                "integration_readiness": "pass",
                "traceability": "pass",
                "freshness": "pass",
                "user_intent_impression": "pass",
                "user_intent_mismatch_reason": "",
                "obvious_next_step_exists": False,
                "next_step_safe": False,
                "obvious_next_step": "",
                "user_would_expect_more": False,
                "rerun_required": False,
                "blocking_findings": [],
            }
        )

        self.assertTrue(ok)
        self.assertEqual(reason, "")
        self.assertEqual(failures, [])

    def test_validate_reviewer_gate_fails_when_user_intent_impression_fails(self) -> None:
        ok, reason, failures = self.stop_hook.validate_reviewer_gate(
            {
                "overall_score": 4.6,
                "evidence_quality": "pass",
                "integration_readiness": "pass",
                "traceability": "pass",
                "freshness": "pass",
                "user_intent_impression": "fail",
                "user_intent_mismatch_reason": "result is technically valid but undershoots the saved user ask",
                "obvious_next_step_exists": False,
                "next_step_safe": False,
                "obvious_next_step": "",
                "user_would_expect_more": False,
                "rerun_required": False,
                "blocking_findings": [],
            }
        )

        self.assertFalse(ok)
        self.assertEqual(reason, "reviewer completion gates are not passing")
        self.assertIn("user_intent_impression=fail", failures)
        self.assertIn(
            "user_intent_mismatch_reason=result is technically valid but undershoots the saved user ask",
            failures,
        )

    def test_validate_reviewer_gate_fails_when_obvious_next_step_exists(self) -> None:
        ok, reason, failures = self.stop_hook.validate_reviewer_gate(
            {
                "overall_score": 4.6,
                "evidence_quality": "pass",
                "integration_readiness": "pass",
                "traceability": "pass",
                "freshness": "pass",
                "user_intent_impression": "pass",
                "user_intent_mismatch_reason": "",
                "obvious_next_step_exists": True,
                "next_step_safe": True,
                "obvious_next_step": "run one more same-ticket pass to attach the missing proof",
                "user_would_expect_more": True,
                "rerun_required": False,
                "blocking_findings": [],
            }
        )

        self.assertFalse(ok)
        self.assertEqual(reason, "reviewer completion gates are not passing")
        self.assertIn("obvious_next_step=run one more same-ticket pass to attach the missing proof", failures)
        self.assertIn("user_would_expect_more=true", failures)


class StopHookTmuxFollowupTests(unittest.TestCase):
    def setUp(self) -> None:
        self.stop_hook = load_stop_hook_module()

    def test_spawn_tmux_followup_requests_json_output(self) -> None:
        ticket = {"path": "tickets/TASK-0033-tighten-agent-facing-cli-surfaces.md"}
        current_run = {
            "tmux_session": "main",
            "auto_continue": True,
            "run_state": ".harness/runs/task-0033-building.json",
        }
        captured: dict[str, object] = {}

        def fake_run(cmd, text, capture_output, check, cwd):
            captured["cmd"] = cmd
            captured["cwd"] = cwd
            return self.stop_hook.subprocess.CompletedProcess(
                cmd,
                0,
                stdout=json.dumps({"action": "followup", "tmux_pane": "%42"}),
                stderr="",
            )

        with patch.object(self.stop_hook.subprocess, "run", side_effect=fake_run):
            result = self.stop_hook.spawn_tmux_followup(
                ROOT,
                ticket,
                "building",
                current_run,
                "hook-driven follow-up",
            )

        self.assertEqual(result, {"action": "followup", "tmux_pane": "%42"})
        self.assertIn("--json", captured["cmd"])


class StopHookGroundingSummaryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.stop_hook = load_stop_hook_module()

    def test_extract_grounding_summary_uses_first_non_empty_line_only(self) -> None:
        summary = self.stop_hook.extract_grounding_summary(
            "\n".join(
                [
                    "GROUNDING_SUMMARY: initial summary",
                    "working notes",
                    "GROUNDING_SUMMARY: reviewing TASK-0026 acceptance criteria",
                    "IMPL_RESULT: status=continue_impl next=building reason=test",
                ]
            )
        )

        self.assertEqual(summary, "initial summary")


class StopHookImplLoopGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.stop_hook = load_stop_hook_module()
        self.ticket = {
            "ticket_id": "TASK-0053",
            "title": "define impl session activation and stop-hook loop gating",
            "phase": "building",
            "status": "building",
        }
        self.current_run = {
            "ticket_id": "TASK-0053",
            "phase": "building",
            "status": "waiting_for_worker",
            "skill_name": "impl",
            "session_id": "sess-123",
            "impl_loop_active": True,
        }
        self.runtime_claim = {
            "ticket_id": "TASK-0053",
            "phase": "building",
            "status": "running",
            "skill_name": "impl",
            "session_id": "sess-123",
        }

    def test_impl_loop_continuation_allowed_requires_flag_ticket_and_session_match(self) -> None:
        self.assertTrue(
            self.stop_hook.impl_loop_continuation_allowed(
                self.ticket,
                self.current_run,
                self.runtime_claim,
                "sess-123",
            )
        )

    def test_impl_loop_continuation_rejects_auto_continue_without_activation_flag(self) -> None:
        current_run = dict(self.current_run)
        current_run["impl_loop_active"] = False
        current_run["auto_continue"] = True

        self.assertFalse(
            self.stop_hook.impl_loop_continuation_allowed(
                self.ticket,
                current_run,
                self.runtime_claim,
                "sess-123",
            )
        )

    def test_impl_loop_continuation_rejects_mismatched_session_claim(self) -> None:
        runtime_claim = dict(self.runtime_claim)
        runtime_claim["session_id"] = "sess-other"

        self.assertFalse(
            self.stop_hook.impl_loop_continuation_allowed(
                self.ticket,
                self.current_run,
                runtime_claim,
                "sess-123",
            )
        )

    def test_next_impl_loop_active_for_action_clears_terminal_paths(self) -> None:
        self.assertTrue(
            self.stop_hook.next_impl_loop_active_for_action(
                "repeat_impl",
                next_phase="building",
                current_phase="building",
            )
        )
        self.assertTrue(
            self.stop_hook.next_impl_loop_active_for_action(
                "continue_same_ticket",
                current_phase="building",
            )
        )
        self.assertFalse(
            self.stop_hook.next_impl_loop_active_for_action(
                "block_ticket",
                current_phase="building",
            )
        )
        self.assertFalse(
            self.stop_hook.next_impl_loop_active_for_action(
                "route_to_orchestrator",
                current_phase="building",
            )
        )


class StopHookLoopModeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.stop_hook = load_stop_hook_module()

    def test_evaluate_loop_contract_continues_when_predicate_is_unsatisfied(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            project_root = Path(td)
            current_run = {
                "skill_name": "loop",
                "loop_active": True,
                "loop_contract": {
                    "done_when": [{"kind": "path_exists", "path": ".harness/tmp/done.flag"}],
                    "retry_message": "keep looping",
                },
            }

            verdict = self.stop_hook.evaluate_loop_contract(
                project_root=project_root,
                current_run=current_run,
                message="still working",
                last_user_turn={"raw_text": "$loop keep going"},
            )

        self.assertEqual(verdict["decision"], "continue_loop")
        self.assertEqual(verdict["status"], "running")
        self.assertEqual(verdict["retry_message"], "keep looping")

    def test_evaluate_loop_contract_completes_when_all_predicates_pass(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            project_root = Path(td)
            target = project_root / ".harness" / "tmp" / "done.flag"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("done", encoding="utf-8")
            current_run = {
                "skill_name": "loop",
                "loop_active": True,
                "loop_contract": {
                    "done_when": [{"kind": "path_exists", "path": ".harness/tmp/done.flag"}],
                    "completion_marker": "DONE",
                    "retry_message": "keep looping",
                },
            }

            verdict = self.stop_hook.evaluate_loop_contract(
                project_root=project_root,
                current_run=current_run,
                message="work complete\nDONE",
                last_user_turn={"raw_text": "$loop keep going"},
            )

        self.assertEqual(verdict["decision"], "complete_loop")
        self.assertEqual(verdict["status"], "complete")

    def test_evaluate_loop_contract_stops_on_explicit_stop_request(self) -> None:
        verdict = self.stop_hook.evaluate_loop_contract(
            project_root=None,
            current_run={
                "skill_name": "loop",
                "loop_active": True,
                "loop_contract": {
                    "done_when": [{"kind": "completion_marker_seen", "text": "DONE"}],
                    "retry_message": "keep looping",
                },
            },
            message="stopping now",
            last_user_turn={"explicit_loop_stop_requested": True, "raw_text": "stop loop"},
        )

        self.assertEqual(verdict["decision"], "stop_loop")
        self.assertEqual(verdict["status"], "blocked")


class StopHookReviewPacketGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.stop_hook = load_stop_hook_module()

    def test_load_ticket_exposes_updated_at_for_review_packet_gate(self) -> None:
        with tempfile.TemporaryDirectory(prefix="stop-hook-ticket-") as td:
            ticket_path = Path(td) / "TASK-9999.md"
            ticket_path.write_text(
                """---
ticket_id: TASK-9999
title: stale packet fixture
phase: building
status: building
owner: codex
priority: medium
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-05T00:00:00Z
updated_at: 2026-04-05T01:30:00Z
next_action: test fixture
last_verification: none
linked_docs: []
---

# TASK-9999: stale packet fixture

## Acceptance Criteria
- [x] AC-1

## Evidence
- [x] Tests

## Blockers
- none

## Review Packet
- `reviewed_at:` 2026-04-05 00:00 +0100
- `rubrics_used:` ["evidence-quality", "integration-readiness"]
- `overall_score:` 4.5
- `overall_threshold:` 4.0
- `overall_verdict:` pass
- `rerun_required:` false
- `evidence_quality:` pass
- `integration_readiness:` pass
- `traceability:` pass
- `freshness:` pass
- `hard_gate_failures:` []
- `blocking_findings:` []
- `next_action:` none
""",
                encoding="utf-8",
            )

            ticket = self.stop_hook.load_ticket(ticket_path)
            ok, reason, failures = self.stop_hook.review_packet_gate(ticket)

            self.assertEqual(ticket["updated_at"], "2026-04-05T01:30:00Z")
            self.assertFalse(ok)
            self.assertEqual(reason, "review packet gates are not passing")
            self.assertIn("reviewed_at=stale", failures)


if __name__ == "__main__":
    unittest.main()
