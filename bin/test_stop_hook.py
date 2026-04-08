#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


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
                "rerun_required": False,
                "blocking_findings": [],
            }
        )

        self.assertTrue(ok)
        self.assertEqual(reason, "")
        self.assertEqual(failures, [])


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
