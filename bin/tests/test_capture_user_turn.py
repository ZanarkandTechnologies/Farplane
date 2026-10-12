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
for RUNTIME_DIR in (ROOT / "hooks" / "user-turn", ROOT / "hooks" / "shared", ROOT / "bin" / "core"):
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
                        "name": "code-health",
                        "source": "local",
                        "path": "skills/code-health/SKILL.md",
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            events = self.run_hook(
                project_root,
                "Use [$code-health](/skills/code-health/SKILL.md) then $unknown.",
            )

        turn_start = next(event for event in events if event["event_type"] == "turn_start")
        requested = next(event for event in events if event["event_type"] == "skill_requested")
        self.assertEqual(turn_start["extra"]["counts"]["skill_mention_count"], 1)
        self.assertEqual(turn_start["extra"]["registry_status"], "loaded")
        self.assertEqual(requested["extra"]["source"], "user_explicit_request")
        self.assertEqual(requested["extra"]["status"], "requested")
        self.assertEqual(requested["extra"]["producer"], "capture_user_turn.py")
        self.assertEqual(requested["extra"]["registry_skill_source"], "local")
        self.assertEqual(requested["extra"]["registry_skill_path"], "skills/code-health/SKILL.md")

    def test_written_skill_event_has_requested_source_and_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            (project_root / ".farplane").mkdir()
            registry_path = project_root / "docs" / "skills" / "registry.jsonl"
            registry_path.parent.mkdir(parents=True)
            registry_path.write_text(
                json.dumps({"name": "code-health", "source": "local"}) + "\n",
                encoding="utf-8",
            )
            payload = {
                "hook_event_name": "UserPromptSubmit",
                "session_id": "session-1",
                "turn_id": "turn-1",
                "cwd": str(project_root),
                "prompt": "$code-health",
            }

            posted: list[dict[str, object]] = []

            class Accepted:
                status = 200

                def __enter__(self) -> "Accepted":
                    return self

                def __exit__(self, *_: object) -> None:
                    return None

                def read(self, *_: object) -> bytes:
                    return b'{"ok":true}'

            def fake_urlopen(req: object, timeout: float = 0) -> Accepted:
                posted.append(json.loads(req.data))  # type: ignore[attr-defined]
                return Accepted()

            env = {"FARPLANE_TELEMETRY_API_URL": "https://example-site.convex.site/ingest", "FARPLANE_TELEMETRY_TOKEN": "test-token"}
            with patch.object(sys, "stdin", io.StringIO(json.dumps(payload))):
                with patch.dict(os.environ, env, clear=False), patch("urllib.request.urlopen", side_effect=fake_urlopen):
                    self.assertEqual(capture_user_turn.main(), 0)
            local_events = list((project_root / ".farplane").glob("events/*.jsonl"))

        self.assertEqual(local_events, [])
        requested = next(row for row in posted if row["activityType"] == "skill_requested")
        detail = json.loads(str(requested["detail"]))
        self.assertEqual(requested["source"], "user_explicit_request")
        self.assertEqual(requested["skillId"], "code-health")
        self.assertEqual(detail["status"], "requested")
        self.assertEqual(detail["metadata"]["producer"], "capture_user_turn.py")
        self.assertEqual(detail["metadata"]["registry_source"], "docs/skills/registry.jsonl")

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

    def test_injects_advisory_context_for_jev_suggestion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            (project_root / ".farplane").mkdir()
            registry_path = project_root / "docs" / "skills" / "registry.jsonl"
            registry_path.parent.mkdir(parents=True)
            registry_path.write_text(
                json.dumps(
                    {
                        "name": "research",
                        "description": "Research current external evidence.",
                        "source": "local",
                        "path": "skills/research/SKILL.md",
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            payload = {
                "hook_event_name": "UserPromptSubmit",
                "session_id": "session-1",
                "turn_id": "turn-1",
                "cwd": str(project_root),
                "prompt": "Find current external evidence.",
            }
            events: list[dict[str, object]] = []

            with patch.object(sys, "stdin", io.StringIO(json.dumps(payload))):
                with patch.object(sys, "stdout", new_callable=io.StringIO) as stdout:
                    with patch.object(capture_user_turn, "suggest_entry_skill", return_value="research"):
                        with patch.object(
                            capture_user_turn,
                            "emit_hook_telemetry",
                            side_effect=lambda **kwargs: events.append(dict(kwargs)) or True,
                        ):
                            self.assertEqual(capture_user_turn.main(), 0)

            hook_output = json.loads(stdout.getvalue())

        self.assertEqual(
            hook_output["hookSpecificOutput"]["hookEventName"], "UserPromptSubmit"
        )
        self.assertIn(
            "Relevant to the current request: research",
            hook_output["hookSpecificOutput"]["additionalContext"],
        )
        suggested = next(event for event in events if event["event_type"] == "skill_suggested")
        self.assertEqual(suggested["extra"]["skill_name"], "research")

    def test_explicit_skill_bypasses_jev_suggestion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            registry_path = project_root / "docs" / "skills" / "registry.jsonl"
            registry_path.parent.mkdir(parents=True)
            registry_path.write_text(
                json.dumps({"name": "research", "description": "Research evidence."}) + "\n",
                encoding="utf-8",
            )
            with patch.object(capture_user_turn, "suggest_entry_skill") as suggest:
                self.run_hook(project_root, "$research this topic")
        suggest.assert_not_called()


if __name__ == "__main__":
    unittest.main()
