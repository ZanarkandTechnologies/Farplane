from __future__ import annotations

import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_DIR = ROOT / "bin" / "runtime"
if str(RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(RUNTIME_DIR))

import capture_user_turn


class CaptureUserTurnTelemetryTests(unittest.TestCase):
    def run_hook(self, project_root: Path, prompt: str) -> list[dict[str, object]]:
        (project_root / ".farplane").mkdir(parents=True, exist_ok=True)
        payload = {
            "hook_event_name": "UserPromptSubmit",
            "session_id": "session-1",
            "turn_id": "turn-1",
            "cwd": str(project_root),
            "prompt": prompt,
        }
        events: list[dict[str, object]] = []

        def capture_event(**kwargs: object) -> bool:
            events.append(dict(kwargs))
            return True

        with patch.object(sys, "stdin", io.StringIO(json.dumps(payload))):
            with patch.object(capture_user_turn, "emit_hook_telemetry", side_effect=capture_event):
                self.assertEqual(capture_user_turn.main(), 0)
        return events

    def test_emits_requested_skill_with_registry_and_producer_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            registry_path = project_root / "docs" / "skills" / "registry.jsonl"
            registry_path.parent.mkdir(parents=True)
            registry_path.write_text(
                json.dumps(
                    {
                        "name": "lean-check",
                        "source": "local",
                        "path": "skills/lean-check/SKILL.md",
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            events = self.run_hook(
                project_root,
                "Use [$lean-check](/skills/lean-check/SKILL.md) then $unknown.",
            )

        turn_start = next(event for event in events if event["event_type"] == "turn_start")
        requested = next(event for event in events if event["event_type"] == "skill_requested")
        self.assertEqual(turn_start["extra"]["counts"]["skill_mention_count"], 1)
        self.assertEqual(turn_start["extra"]["registry_status"], "loaded")
        self.assertEqual(requested["extra"]["source"], "user_explicit_request")
        self.assertEqual(requested["extra"]["status"], "requested")
        self.assertEqual(requested["extra"]["producer"], "capture_user_turn.py")
        self.assertEqual(requested["extra"]["registry_skill_source"], "local")
        self.assertEqual(requested["extra"]["registry_skill_path"], "skills/lean-check/SKILL.md")

    def test_written_skill_event_has_requested_source_and_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            (project_root / ".farplane").mkdir()
            registry_path = project_root / "docs" / "skills" / "registry.jsonl"
            registry_path.parent.mkdir(parents=True)
            registry_path.write_text(
                json.dumps({"name": "lean-check", "source": "local"}) + "\n",
                encoding="utf-8",
            )
            payload = {
                "hook_event_name": "UserPromptSubmit",
                "session_id": "session-1",
                "turn_id": "turn-1",
                "cwd": str(project_root),
                "prompt": "$lean-check",
            }

            with patch.object(sys, "stdin", io.StringIO(json.dumps(payload))):
                with patch.dict(os.environ, {"FARPLANE_TELEMETRY_API_URL": ""}, clear=False):
                    self.assertEqual(capture_user_turn.main(), 0)

            event_path = next((project_root / ".farplane" / "events").glob("*.jsonl"))
            events = [json.loads(line) for line in event_path.read_text(encoding="utf-8").splitlines()]

        requested = next(event for event in events if event["event_type"] == "skill_requested")
        self.assertEqual(requested["source"], "user_explicit_request")
        self.assertEqual(requested["status"], "requested")
        self.assertEqual(requested["metadata"]["producer"], "capture_user_turn.py")
        self.assertEqual(requested["metadata"]["registry_source"], "docs/skills/registry.jsonl")

    def test_missing_registry_is_observable_and_control_detection_survives(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            events = self.run_hook(Path(tmp), "Run [$qa](/skills/qa/SKILL.md).")

        turn_start = next(event for event in events if event["event_type"] == "turn_start")
        controls = [event for event in events if event["event_type"] == "control_surface_detected"]
        requested = [event for event in events if event["event_type"] == "skill_requested"]
        self.assertEqual(turn_start["extra"]["registry_status"], "missing")
        self.assertEqual(turn_start["extra"]["counts"]["registry_error_count"], 1)
        self.assertEqual(turn_start["extra"]["counts"]["skill_mention_count"], 0)
        self.assertEqual([event["extra"]["skill_name"] for event in controls], ["qa"])
        self.assertEqual(requested, [])

    def test_invalid_registry_is_observable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            registry_path = project_root / "docs" / "skills" / "registry.jsonl"
            registry_path.parent.mkdir(parents=True)
            registry_path.write_text("{invalid}\n", encoding="utf-8")

            events = self.run_hook(project_root, "$qa")

        turn_start = next(event for event in events if event["event_type"] == "turn_start")
        self.assertEqual(turn_start["extra"]["registry_status"], "invalid")
        self.assertEqual(turn_start["extra"]["counts"]["registry_error_count"], 1)
        self.assertTrue(turn_start["extra"]["registry_error"])


if __name__ == "__main__":
    unittest.main()
