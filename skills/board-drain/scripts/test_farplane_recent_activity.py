from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from farplane_recent_activity import summarize_local_recent_activity, summarize_recent_activity


class _FakeResponse:
    def __init__(self, payload: dict[str, object]) -> None:
        self.payload = payload

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


class FarplaneRecentActivityTests(unittest.TestCase):
    def test_queries_farplane_console_activity_endpoint(self) -> None:
        captured_urls: list[str] = []

        def fake_urlopen(request: object, timeout: float = 0) -> _FakeResponse:
            captured_urls.append(request.full_url)  # type: ignore[attr-defined]
            self.assertEqual(timeout, 2.0)
            self.assertEqual(request.headers["Authorization"], "Bearer secret")  # type: ignore[attr-defined]
            return _FakeResponse(
                {
                    "ok": True,
                    "active": True,
                    "windowMinutes": 60,
                    "eventCount": 1,
                    "latestEvent": {"eventType": "turn_start", "receivedAt": 123},
                }
            )

        with tempfile.TemporaryDirectory() as tmp, patch("urllib.request.urlopen", fake_urlopen):
            root = Path(tmp)
            summary = summarize_recent_activity(
                root,
                activity_url="https://console.example.com/api/activity/recent",
                key="secret",
                project_name="Farplane",
                project_directory=str(root),
            )

        self.assertTrue(summary["ok"])
        self.assertTrue(summary["active"])
        self.assertEqual(summary["provider"], "farplane_console")
        self.assertIn("projectName=Farplane", captured_urls[0])
        self.assertIn("projectDirectory=", captured_urls[0])

    def test_reports_unknown_without_console_config_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            summary = summarize_recent_activity(Path(tmp), activity_url="", key="")

        self.assertFalse(summary["ok"])
        self.assertFalse(summary["active"])
        self.assertEqual(summary["provider"], "farplane_console")
        self.assertEqual(summary["error"], "missing_activity_url")

    def test_local_fallback_is_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            events = root / ".farplane" / "events"
            events.mkdir(parents=True)
            (events / "2026-06-15.jsonl").write_text(
                json.dumps({"event_type": "turn_start", "timestamp": "2026-06-15T00:45:00Z"}) + "\n",
                encoding="utf-8",
            )

            summary = summarize_recent_activity(
                root,
                activity_url="",
                key="",
                allow_local_fallback=True,
                now=datetime(2026, 6, 15, 1, 0, tzinfo=timezone.utc),
                window_minutes=60,
            )

        self.assertTrue(summary["ok"])
        self.assertTrue(summary["active"])
        self.assertEqual(summary["provider"], "local_events")
        self.assertEqual(summary["fallbackReason"], "missing_activity_url")

    def test_local_summary_reports_idle_when_only_old_events_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            events = root / ".farplane" / "events"
            events.mkdir(parents=True)
            (events / "2026-06-15.jsonl").write_text(
                json.dumps({"event_type": "turn_start", "timestamp": "2026-06-14T23:30:00Z"}) + "\n",
                encoding="utf-8",
            )

            summary = summarize_local_recent_activity(
                root,
                now=datetime(2026, 6, 15, 1, 0, tzinfo=timezone.utc),
                window_minutes=60,
            )

        self.assertFalse(summary["active"])
        self.assertEqual(summary["eventCount"], 0)


if __name__ == "__main__":
    unittest.main()
