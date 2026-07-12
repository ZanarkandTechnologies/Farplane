from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = ROOT / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from farplane_telemetry_status import build_cloud_payload, build_status


class FarplaneTelemetryStatusTests(unittest.TestCase):
    def test_build_status_summarizes_events_and_learning_runs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            event_dir = project_root / ".farplane" / "events"
            event_dir.mkdir(parents=True)
            (event_dir / "2026-05-26.jsonl").write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "event_type": "skill_requested",
                                "skill_name": "goal-advisor",
                                "hook_name": "UserPromptSubmit",
                                "ticket_id": "TASK-0160",
                                "status": "",
                            }
                        ),
                        json.dumps(
                            {
                                "event_type": "ticket_completion_learning",
                                "skill_name": "goal-advisor",
                                "hook_name": "PostToolUse",
                                "ticket_id": "TASK-0160",
                                "status": "complete",
                            }
                        ),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            windows_dir = project_root / ".farplane" / "state" / "message-windows"
            windows_dir.mkdir(parents=True)
            (windows_dir / "sess-123.json").write_text(
                json.dumps({"session_id": "sess-123", "turn_count": 10}),
                encoding="utf-8",
            )
            run_dir = project_root / ".farplane" / "mine" / "runs" / ("a" * 64)
            run_dir.mkdir(parents=True)
            (run_dir / "run.json").write_text(
                json.dumps(
                    {
                        "run_id": "a" * 64,
                        "program_ref": "core:ticket-completion-learning@1.1.0",
                        "status": "complete",
                    }
                ),
                encoding="utf-8",
            )
            (run_dir / "input.json").write_text(
                json.dumps(
                    {
                        "event": {"entity_ref": {"kind": "ticket", "id": "TASK-0160", "path": "tickets/TASK-0160/ticket.md"}},
                        "semantic_context": {"thread_id": "sess-123", "conversation_window_found": True},
                    }
                ),
                encoding="utf-8",
            )
            (run_dir / "report.json").write_text(
                json.dumps(
                    {
                        "status": "complete",
                        "summary": "One reusable proof improvement found.",
                        "material_findings": [
                            {
                                "problem": "Completion proof was repeatedly incomplete.",
                                "reusable_pattern": "Make proof routing explicit.",
                                "proposed_solution": "Refine the owning skill.",
                                "owner_surface": "skill",
                                "evidence_refs": ["tickets/TASK-0160/ticket.md", "turn-1"],
                                "confidence": "medium",
                                "recovery_eligible": False,
                            }
                        ],
                        "source_gaps": [],
                        "escalation": {"decision": "dogfood", "reason_codes": ["skill_candidate"]},
                        "ticket_output": {
                            "decision": "created",
                            "ticket_id": "TASK-0161",
                            "mode": "prove_or_reject",
                            "status": "todo"
                        },
                    }
                ),
                encoding="utf-8",
            )

            status = build_status(project_root)

        self.assertEqual(status["events"]["total"], 2)
        self.assertEqual(status["events"]["by_event_type"]["skill_requested"], 1)
        self.assertEqual(status["events"]["by_status"]["complete"], 1)
        self.assertEqual(status["learning"]["window_count"], 1)
        self.assertNotIn("turn_count", status["learning"])
        self.assertEqual(status["learning"]["run_count"], 1)
        run = status["learning"]["latest_runs"][0]
        self.assertEqual(run["status"], "complete")
        self.assertIn("proof was repeatedly incomplete", run["candidate_title"])
        self.assertEqual(run["recommended_owner"], "skill")
        self.assertEqual(run["ticket_id"], "TASK-0160")
        self.assertEqual(run["finding_count"], 1)
        self.assertFalse(run["recovery_eligible"])
        self.assertEqual(run["ticket_decision"], "created")
        self.assertEqual(run["projected_ticket_id"], "TASK-0161")
        self.assertEqual(run["projected_ticket_mode"], "prove_or_reject")

    def test_build_status_handles_empty_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            status = build_status(Path(tmp))

        self.assertEqual(status["events"]["total"], 0)
        self.assertEqual(status["learning"]["run_count"], 0)
        self.assertEqual(status["learning"]["window_count"], 0)

    def test_build_cloud_payload_strips_local_paths_and_event_metadata(self) -> None:
        status = {
            "project_root": "/Users/example/private/Farplane",
            "project_name": "Farplane",
            "events": {
                "latest": [
                    {
                        "event_id": "evt-1",
                        "event_type": "turn_start",
                        "project_root": "/Users/example/private/Farplane",
                        "metadata": {"cwd": "/Users/example/private/Farplane"},
                        "summary": "user turn captured",
                    }
                ]
            },
            "learning": {
                "latest_runs": [
                    {
                        "run_path": "/Users/example/private/Farplane/.farplane/mine/runs/run-1",
                        "ticket_id": "TASK-0160",
                        "candidate_title": "Improve proof",
                        "evidence_refs": ["tickets/TASK-0160/ticket.md"],
                        "artifacts": {
                            "input": "/Users/example/private/Farplane/input.json",
                            "report": "/Users/example/private/Farplane/report.json",
                        },
                    }
                ]
            },
        }

        payload = build_cloud_payload(status)
        encoded = json.dumps(payload)

        self.assertNotIn("project_root", payload)
        self.assertNotIn("metadata", payload["events"]["latest"][0])
        self.assertNotIn("/Users/example", encoded)
        self.assertNotIn("candidate_title", payload["learning"]["latest_runs"][0])
        self.assertNotIn("evidence_refs", payload["learning"]["latest_runs"][0])
        self.assertEqual(payload["learning"]["latest_runs"][0]["run_path"], "run-1")
        self.assertEqual(payload["learning"]["latest_runs"][0]["artifacts"], {"input": "present", "report": "present"})


if __name__ == "__main__":
    unittest.main()
