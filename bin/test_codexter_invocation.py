from __future__ import annotations

import json
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import codexter_invocation


WORKFLOW_TEXT = """\
---
workflow:
  name: codexter-invocation
  version: 1

board:
  adapter: filesystem
  source: tickets/
  active_phases: ["planning", "building", "documenting"]
  terminal_statuses: ["done", "failed"]

compute:
  default: local_shared
  allowed: ["local_shared", "local_worktree"]
  ticket_override_field: compute_target

routing:
  planning: impl-plan
  building: impl
  qa: qa
  review: review
  documenting: close-ticket

quality:
  writes_proof_packet: true
---

# Test Workflow
"""


TICKET_TEXT = """\
---
ticket_id: TASK-1234
title: add invocation contract
phase: planning
status: review
owner: codex
claimed_by:
priority: high
depends_on: []
blocked_by: []
ready: false
approval_required: true
requires_qa: false
requires_demo: false
created_at: 2026-05-05T00:00:00Z
updated_at: 2026-05-05T00:00:00Z
next_action: approve the plan
last_verification: none
---

# TASK-1234: add invocation contract

## Summary
Fixture ticket.
"""


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(text), encoding="utf-8")


class CodexterInvocationTests(unittest.TestCase):
    def test_workflow_parses_nested_frontmatter_and_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "WORKFLOW.md", WORKFLOW_TEXT)
            policy = codexter_invocation.load_workflow("WORKFLOW.md", root)
            self.assertEqual(policy.name, "codexter-invocation")
            self.assertEqual(policy.compute_allowed, ("local_shared", "local_worktree"))
            self.assertEqual(policy.routing["planning"], "impl-plan")
            self.assertIn("Test Workflow", policy.prompt_template)

    def test_prepare_planning_invocation_routes_to_impl_plan(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "WORKFLOW.md", WORKFLOW_TEXT)
            write(root / "tickets" / "TASK-1234" / "ticket.md", TICKET_TEXT)
            envelope = codexter_invocation.parse_run_envelope(
                json.dumps(
                    {
                        "workflowPath": "WORKFLOW.md",
                        "workItemId": "TASK-1234",
                        "phase": "planning",
                        "mode": "local_codex",
                        "requestedBy": "test",
                        "requestedAt": "2026-05-05T00:00:00Z",
                        "proofPacketPath": ".harness/results/task-1234-proof.json",
                    }
                ),
                root,
            )
            plan = codexter_invocation.prepare_invocation(envelope, root)
            self.assertEqual(plan.status, "ready")
            self.assertEqual(plan.route.skill_name, "impl-plan")
            self.assertEqual(plan.work_item.identifier, "TASK-1234")
            self.assertTrue(plan.compute.allowed)

    def test_prepare_uses_configured_board_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(
                root / "WORKFLOW.md",
                WORKFLOW_TEXT.replace("source: tickets/", "source: project-tickets/"),
            )
            write(root / "project-tickets" / "TASK-1234" / "ticket.md", TICKET_TEXT)
            envelope = codexter_invocation.parse_run_envelope(
                json.dumps(
                    {
                        "workflowPath": "WORKFLOW.md",
                        "workItemId": "TASK-1234",
                        "phase": "planning",
                        "proofPacketPath": ".harness/results/task-1234-proof.json",
                    }
                ),
                root,
            )

            plan = codexter_invocation.prepare_invocation(envelope, root)

            self.assertEqual(plan.status, "ready")
            self.assertIn("project-tickets/TASK-1234/ticket.md", plan.work_item.local_ticket_path)

    def test_symphony_envelope_template_prepares_from_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "WORKFLOW.md", WORKFLOW_TEXT)
            write(
                root / "tickets" / "TASK-0112" / "ticket.md",
                TICKET_TEXT.replace("TASK-1234", "TASK-0112"),
            )
            template = (
                Path(__file__).resolve().parents[1]
                / "skills"
                / "codexter-invocation"
                / "templates"
                / "symphony-run-envelope.json"
            )

            envelope = codexter_invocation.parse_run_envelope(template, root)
            plan = codexter_invocation.prepare_invocation(envelope, root)

            self.assertEqual(plan.status, "ready")
            self.assertEqual(plan.envelope.mode, "symphony_worker")
            self.assertEqual(plan.compute.target, "local_shared")
            self.assertEqual(plan.route.skill_name, "impl-plan")
            expected_proof = (
                root / ".harness" / "results" / "symphony-task-0112.proof.json"
            ).resolve()
            self.assertEqual(
                plan.proof_packet_path,
                str(expected_proof),
            )

    def test_building_invocation_blocks_approval_gated_ticket(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "WORKFLOW.md", WORKFLOW_TEXT)
            write(root / "tickets" / "TASK-1234" / "ticket.md", TICKET_TEXT)
            envelope = codexter_invocation.parse_run_envelope(
                json.dumps(
                    {
                        "workflowPath": "WORKFLOW.md",
                        "workItemId": "TASK-1234",
                        "phase": "building",
                        "proofPacketPath": ".harness/results/task-1234-proof.json",
                    }
                ),
                root,
            )
            plan = codexter_invocation.prepare_invocation(envelope, root)
            self.assertEqual(plan.status, "blocked")
            self.assertFalse(plan.compute.allowed)
            self.assertIn("approval", " ".join(plan.compute.blockers))

    def test_future_compute_target_blocks_explicitly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "WORKFLOW.md", WORKFLOW_TEXT)
            write(root / "tickets" / "TASK-1234" / "ticket.md", TICKET_TEXT)
            envelope = codexter_invocation.parse_run_envelope(
                json.dumps(
                    {
                        "workflowPath": "WORKFLOW.md",
                        "workItemId": "TASK-1234",
                        "phase": "planning",
                        "computeTarget": "symphony",
                        "proofPacketPath": ".harness/results/task-1234-proof.json",
                    }
                ),
                root,
            )
            plan = codexter_invocation.prepare_invocation(envelope, root)
            self.assertEqual(plan.status, "blocked")
            self.assertIn("not allowed", plan.compute.reason)

    def test_proof_packet_writes_parseable_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "WORKFLOW.md", WORKFLOW_TEXT)
            write(root / "tickets" / "TASK-1234" / "ticket.md", TICKET_TEXT)
            envelope = codexter_invocation.parse_run_envelope(
                json.dumps(
                    {
                        "workflowPath": "WORKFLOW.md",
                        "workItemId": "TASK-1234",
                        "phase": "planning",
                        "proofPacketPath": ".harness/results/task-1234-proof.json",
                    }
                ),
                root,
            )
            plan = codexter_invocation.prepare_invocation(envelope, root)
            packet = codexter_invocation.build_proof_packet(
                plan=plan,
                verdict="pass",
                next_action="continue",
                phase_status="completed",
                artifacts=("tickets/TASK-1234/artifacts/review.json",),
                commands=("python3 -m unittest",),
            )
            codexter_invocation.write_proof_packet(packet, plan.proof_packet_path)
            loaded = json.loads(Path(plan.proof_packet_path).read_text(encoding="utf-8"))
            self.assertEqual(loaded["schemaVersion"], 1)
            self.assertEqual(loaded["workItem"]["identifier"], "TASK-1234")
            self.assertEqual(loaded["verdict"], "pass")
            self.assertIn("planning", loaded["phases"])

    def test_rejects_proof_path_outside_allowed_roots(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "WORKFLOW.md", WORKFLOW_TEXT)
            write(root / "tickets" / "TASK-1234" / "ticket.md", TICKET_TEXT)
            envelope = codexter_invocation.parse_run_envelope(
                json.dumps(
                    {
                        "workflowPath": "WORKFLOW.md",
                        "workItemId": "TASK-1234",
                        "phase": "planning",
                        "proofPacketPath": "../escape.json",
                    }
                ),
                root,
            )
            with self.assertRaises(codexter_invocation.InvocationError):
                codexter_invocation.prepare_invocation(envelope, root)


if __name__ == "__main__":
    unittest.main()
