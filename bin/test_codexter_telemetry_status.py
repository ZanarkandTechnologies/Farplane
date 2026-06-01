from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from codexter_telemetry_status import build_cloud_payload, build_status


class CodexterTelemetryStatusTests(unittest.TestCase):
    def test_build_status_summarizes_events_and_learning_runs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            event_dir = project_root / ".harness" / "events"
            event_dir.mkdir(parents=True)
            (event_dir / "2026-05-26.jsonl").write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "event_type": "skill_requested",
                                "skill_name": "impl",
                                "hook_name": "UserPromptSubmit",
                                "ticket_id": "TASK-0160",
                                "status": "",
                            }
                        ),
                        json.dumps(
                            {
                                "event_type": "learning_review_launched",
                                "skill_name": "impl",
                                "hook_name": "Stop",
                                "ticket_id": "TASK-0160",
                                "status": "launched",
                            }
                        ),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            windows_dir = project_root / ".harness" / "state" / "self-improve" / "windows"
            windows_dir.mkdir(parents=True)
            (windows_dir / "sess-123.json").write_text(
                json.dumps({"session_id": "sess-123", "turn_count": 10, "last_review_turn_count": 10}),
                encoding="utf-8",
            )
            run_dir = project_root / ".harness" / "state" / "self-improve" / "applications" / "20260526-sess-123"
            run_dir.mkdir(parents=True)
            (run_dir / "input.json").write_text(
                json.dumps(
                    {
                        "session_id": "sess-123",
                        "trigger": {"cadence": 10, "turn_count": 10, "last_review_turn_count": 0},
                        "window": {
                            "rolling_exchanges": [
                                {
                                    "user_turn": {
                                        "turn_id": "turn-1",
                                        "captured_at": "2026-05-26T00:00:00Z",
                                        "summary": "asked for $impl",
                                        "raw_text": "please $impl /Users/example/secret/file",
                                    },
                                    "assistant_text": "I will run the implementation plan and capture proof.",
                                    "assistant_captured_at": "2026-05-26T00:00:01Z",
                                }
                            ]
                        },
                    }
                ),
                encoding="utf-8",
            )
            (run_dir / "report.json").write_text(
                json.dumps(
                    {
                        "status": "task_created",
                        "speak": "Created a ticket to improve impl proof.",
                        "notion_tasks": [{"title": "Improve impl proof", "target": "skills/impl"}],
                        "decisions": [{"summary": "Improve impl proof", "target": "skills/impl", "confidence": "medium"}],
                        "proof_hops": [
                            {"name": "user_capture", "status": "present"},
                            {"name": "assistant_capture", "status": "present"},
                            {"name": "notion_task_creation", "status": "missing"},
                        ],
                    }
                ),
                encoding="utf-8",
            )

            status = build_status(project_root)

        self.assertEqual(status["events"]["total"], 2)
        self.assertEqual(status["events"]["by_event_type"]["skill_requested"], 1)
        self.assertEqual(status["events"]["by_status"]["launched"], 1)
        self.assertEqual(status["learning"]["window_count"], 1)
        self.assertEqual(status["learning"]["turn_count"], 10)
        self.assertEqual(status["learning"]["run_count"], 1)
        run = status["learning"]["latest_runs"][0]
        self.assertEqual(run["status"], "task_created")
        self.assertEqual(run["candidate_title"], "Improve impl proof")
        self.assertEqual(run["recommended_owner"], "skills/impl")
        self.assertEqual(run["proof_hops_present"], 2)
        self.assertEqual(run["proof_hops_total"], 3)
        self.assertEqual(run["proof_hops_missing"], ["notion_task_creation"])
        self.assertEqual(run["message_count"], 2)
        self.assertIn("[local path]", run["messages"][0]["redacted_excerpt"])

    def test_build_status_handles_empty_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            status = build_status(Path(tmp))

        self.assertEqual(status["events"]["total"], 0)
        self.assertEqual(status["learning"]["run_count"], 0)
        self.assertEqual(status["learning"]["window_count"], 0)

    def test_build_cloud_payload_strips_local_paths_and_event_metadata(self) -> None:
        status = {
            "project_root": "/Users/example/private/Codexter",
            "project_name": "Codexter",
            "events": {
                "latest": [
                    {
                        "event_id": "evt-1",
                        "event_type": "turn_start",
                        "project_root": "/Users/example/private/Codexter",
                        "metadata": {"cwd": "/Users/example/private/Codexter"},
                        "summary": "user turn captured",
                    }
                ]
            },
            "learning": {
                "latest_runs": [
                    {
                        "run_path": "/Users/example/private/Codexter/.harness/state/self-improve/applications/run-1",
                        "candidate_title": "Improve proof",
                        "messages": [{"role": "user", "summary": "hello", "redacted_excerpt": "[local path]"}],
                        "artifacts": {
                            "input": "/Users/example/private/Codexter/input.json",
                            "report": "/Users/example/private/Codexter/report.json",
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
        self.assertEqual(payload["learning"]["latest_runs"][0]["run_path"], "run-1")
        self.assertEqual(payload["learning"]["latest_runs"][0]["artifacts"], {"input": "present", "report": "present"})


if __name__ == "__main__":
    unittest.main()
