from __future__ import annotations

import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import URLError

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_DIR = ROOT / "bin" / "runtime"
if str(RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(RUNTIME_DIR))

from runtime_telemetry import build_event, emit_hook_telemetry, telemetry_config


class RuntimeTelemetryTests(unittest.TestCase):
    def test_build_event_redacts_prompt_and_carries_runtime_identity(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)

            event = build_event(
                event_type="skill_requested",
                source="test",
                project_root=project_root,
                payload={"session_id": "sess-123", "turn_id": "turn-1"},
                runtime_claim={"ticket_id": "TASK-0160", "skill_name": "goal-advisor"},
                summary="requested $goal-advisor",
                counts={"skill_mention_count": 1, "ignored": "nope"},
                metadata={"prompt": "secret prompt", "skill_name": "goal-advisor", "raw_text": "secret raw"},
            )

        self.assertEqual(event["event_type"], "skill_requested")
        self.assertEqual(event["session_id"], "sess-123")
        self.assertEqual(event["ticket_id"], "TASK-0160")
        self.assertEqual(event["skill_name"], "goal-advisor")
        self.assertEqual(event["counts"], {"skill_mention_count": 1})
        self.assertNotIn("prompt", event["metadata"])
        self.assertNotIn("raw_text", event["metadata"])
        self.assertFalse(event["privacy"]["prompt_included"])
        self.assertFalse(event["privacy"]["raw_transcript_included"])

    def emit(self, project_root: Path, env: dict[str, str], urlopen: object) -> bool:
        with patch.dict(os.environ, env, clear=True), patch("urllib.request.urlopen", side_effect=urlopen):
            return emit_hook_telemetry(
                event_type="learning_window_updated",
                hook_event_name="Stop",
                payload={"session_id": "sess-123", "turn_id": "turn-7", "cwd": str(project_root)},
                project_root=project_root,
                runtime_claim={"ticket_id": "TASK-0160", "skill_name": "goal-advisor"},
                extra={"source": "test", "summary": "learning window updated", "counts": {"turn_count": 10}},
            )

    def test_emit_posts_a_convex_runtime_row_and_writes_nothing_locally(self) -> None:
        posted: list[tuple[str, dict[str, str], dict[str, object]]] = []

        class Accepted:
            status = 200

            def __enter__(self) -> "Accepted":
                return self

            def __exit__(self, *_: object) -> None:
                return None

            def read(self, *_: object) -> bytes:
                return b'{"ok":true}'

        def urlopen(req: object, timeout: float = 0) -> Accepted:
            posted.append((req.full_url, dict(req.header_items()), json.loads(req.data)))  # type: ignore[attr-defined]
            return Accepted()

        env = {"FARPLANE_CONVEX_SITE_URL": "https://example-site.convex.site", "FARPLANE_TELEMETRY_TOKEN": "test-token", "FARPLANE_CONFIG_DISABLE": "1"}
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp) / "Globex App"
            project_root.mkdir()
            sent = self.emit(project_root, env, urlopen)
            local = list(project_root.glob(".farplane/**/*"))

        self.assertTrue(sent)
        self.assertEqual(local, [])
        url, headers, row = posted[0]
        self.assertEqual(url, "https://example-site.convex.site/ingest")
        self.assertEqual(headers["Authorization"], "Bearer test-token")
        self.assertEqual(row["eventType"], "activity_log")
        self.assertEqual(row["activityType"], "learning_window_updated")
        self.assertEqual(row["agentId"], "farplane-runtime")
        self.assertEqual(row["teamId"], "farplane")
        self.assertTrue(str(row["projectId"]).startswith("codex-proj-") and str(row["projectId"]).endswith("globex-app"))
        self.assertEqual(row["sessionKey"], "sess-123")
        self.assertEqual(row["taskId"], "TASK-0160")
        self.assertEqual(row["skillId"], "goal-advisor")
        self.assertIsInstance(row["occurredAt"], int)
        detail = json.loads(str(row["detail"]))
        self.assertEqual(detail["turnId"], "turn-7")
        self.assertEqual(detail["counts"], {"turn_count": 10})

    def test_unconfigured_or_unreachable_convex_returns_false_without_a_local_log(self) -> None:
        def unreachable(req: object, timeout: float = 0) -> None:
            raise URLError("offline")

        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            self.assertFalse(self.emit(project_root, {"FARPLANE_CONFIG_DISABLE": "1"}, unreachable))
            env = {"FARPLANE_CONVEX_SITE_URL": "https://example-site.convex.site", "FARPLANE_CONFIG_DISABLE": "1"}
            with patch("sys.stderr", io.StringIO()) as stderr:
                self.assertFalse(self.emit(project_root, env, unreachable))
            self.assertFalse((project_root / ".farplane").exists())
        self.assertIn("not delivered to Convex", stderr.getvalue())


class TelemetryConfigTests(unittest.TestCase):
    def test_runtime_events_go_to_the_convex_site_ingest_when_no_endpoint_is_set(self) -> None:
        with patch.dict(os.environ, {"FARPLANE_CONVEX_SITE_URL": "https://example-site.convex.site/"}, clear=True):
            url, token, _ = telemetry_config()
        self.assertEqual(url, "https://example-site.convex.site/ingest")
        self.assertEqual(token, "")

    def test_an_explicit_endpoint_wins(self) -> None:
        env = {"FARPLANE_TELEMETRY_API_URL": "https://events.example/in", "FARPLANE_CONVEX_SITE_URL": "https://example-site.convex.site"}
        with patch.dict(os.environ, env, clear=True):
            self.assertEqual(telemetry_config()[0], "https://events.example/in")


if __name__ == "__main__":
    unittest.main()
