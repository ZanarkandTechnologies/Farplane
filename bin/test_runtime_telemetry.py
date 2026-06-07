from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime_telemetry import build_event, emit_hook_telemetry, write_local_event


class RuntimeTelemetryTests(unittest.TestCase):
    def test_build_event_redacts_prompt_and_carries_runtime_identity(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)

            event = build_event(
                event_type="skill_requested",
                source="test",
                project_root=project_root,
                payload={"session_id": "sess-123", "turn_id": "turn-1"},
                runtime_claim={"ticket_id": "TASK-0160", "skill_name": "impl"},
                summary="requested $impl",
                counts={"skill_mention_count": 1, "ignored": "nope"},
                metadata={"prompt": "secret prompt", "skill_name": "impl", "raw_text": "secret raw"},
            )

        self.assertEqual(event["event_type"], "skill_requested")
        self.assertEqual(event["session_id"], "sess-123")
        self.assertEqual(event["ticket_id"], "TASK-0160")
        self.assertEqual(event["skill_name"], "impl")
        self.assertEqual(event["counts"], {"skill_mention_count": 1})
        self.assertNotIn("prompt", event["metadata"])
        self.assertNotIn("raw_text", event["metadata"])
        self.assertFalse(event["privacy"]["prompt_included"])
        self.assertFalse(event["privacy"]["raw_transcript_included"])

    def test_write_local_event_appends_jsonl_by_day(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            path = write_local_event(
                project_root,
                {
                    "timestamp": "2026-05-26T00:00:00Z",
                    "event_id": "evt-test",
                    "event_type": "hook_result",
                },
            )

            lines = path.read_text(encoding="utf-8").splitlines()

        self.assertEqual(path.name, "2026-05-26.jsonl")
        self.assertEqual(len(lines), 1)
        self.assertEqual(json.loads(lines[0])["event_type"], "hook_result")

    def test_emit_hook_telemetry_writes_locally_when_remote_is_not_configured(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            with patch.dict(os.environ, {}, clear=True):
                posted = emit_hook_telemetry(
                    event_type="learning_window_updated",
                    hook_event_name="Stop",
                    payload={"session_id": "sess-123", "cwd": str(project_root)},
                    project_root=project_root,
                    runtime_claim={"ticket_id": "TASK-0160", "skill_name": "impl"},
                    extra={
                        "source": "test",
                        "summary": "learning window updated",
                        "counts": {"turn_count": 10},
                    },
                )
            files = list((project_root / ".farplane" / "events").glob("*.jsonl"))
            event = json.loads(files[0].read_text(encoding="utf-8").splitlines()[0])

        self.assertFalse(posted)
        self.assertEqual(event["event_type"], "learning_window_updated")
        self.assertEqual(event["summary"], "learning window updated")
        self.assertEqual(event["counts"], {"turn_count": 10})
        self.assertEqual(event["ticket_id"], "TASK-0160")


if __name__ == "__main__":
    unittest.main()
