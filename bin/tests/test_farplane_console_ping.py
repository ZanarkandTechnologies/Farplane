from __future__ import annotations

import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
HOOK_PATH = ROOT / "hooks" / "farplane_console_ping.py"

spec = importlib.util.spec_from_file_location("farplane_console_ping", HOOK_PATH)
assert spec is not None
farplane_console_ping = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(farplane_console_ping)


class FarplaneConsolePingTests(unittest.TestCase):
    def test_default_endpoint_uses_hook_telemetry_ingress(self) -> None:
        with patch.dict(
            os.environ,
            {
                "FARPLANE_CONFIG_DISABLE": "1",
                "FARPLANE_CONVEX_SITE_URL": "https://example.convex.site",
            },
            clear=True,
        ):
            self.assertEqual(
                farplane_console_ping.telemetry_endpoint(),
                "https://example.convex.site/telemetry/hooks",
            )

    def test_endpoint_uses_saved_runtime_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane_home = root / "farplane"
            farplane_home.mkdir()
            (farplane_home / "config.json").write_text(
                json.dumps({"env": {"FARPLANE_CONVEX_SITE_URL": "https://saved.convex.site"}}),
                encoding="utf-8",
            )
            with patch.dict(os.environ, {"FARPLANE_STATE_DIR": str(farplane_home)}, clear=True):
                self.assertEqual(
                    farplane_console_ping.telemetry_endpoint(),
                    "https://saved.convex.site/telemetry/hooks",
                )

    def test_build_ping_wraps_turn_start_as_hook_telemetry(self) -> None:
        with patch.dict(
            os.environ,
            {
                "AIKAGE_AGENT_NAME": "codex",
                "AIKAGE_MACHINE_NAME": "Studio Mac",
                "FARPLANE_CONFIG_DISABLE": "1",
            },
            clear=True,
        ):
            body = farplane_console_ping.build_ping(
                {
                    "hook_event_name": "UserPromptSubmit",
                    "session_id": "session-1",
                    "turn_id": "turn-1",
                    "cwd": "/Users/kenji/Farplane UI",
                    "prompt": "secret prompt longer than needed",
                }
            )

        self.assertEqual(body["hookName"], "farplane-console-ping")
        self.assertEqual(body["hookType"], "UserPromptSubmit")
        self.assertEqual(body["sessionId"], "session-1")
        self.assertEqual(body["eventKey"], "codex-lifecycle:session-1:turn-1:UserPromptSubmit")
        self.assertEqual(body["projectId"], "codex-proj-users-kenji-farplane-ui")
        self.assertEqual(body["payload"]["eventType"], "turn_start")
        self.assertEqual(body["payload"]["source"], "codex-user-prompt")
        self.assertEqual(body["payload"]["turnId"], "turn-1")
        self.assertEqual(body["payload"]["projectName"], "Farplane UI")
        self.assertEqual(body["payload"]["projectDirectory"], "/Users/kenji/Farplane UI")

    def test_build_ping_wraps_stop_as_hook_telemetry(self) -> None:
        with patch.dict(os.environ, {"AIKAGE_MACHINE_NAME": "Studio Mac", "FARPLANE_CONFIG_DISABLE": "1"}, clear=True):
            body = farplane_console_ping.build_ping(
                {
                    "hook_event_name": "Stop",
                    "session_id": "session-1",
                    "turn_id": "turn-1",
                    "cwd": "/Users/kenji/Farplane UI",
                }
            )

        self.assertEqual(body["hookType"], "Stop")
        self.assertEqual(body["payload"]["eventType"], "turn_end")
        self.assertEqual(body["payload"]["source"], "codex-stop")


if __name__ == "__main__":
    unittest.main()
