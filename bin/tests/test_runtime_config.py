from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = ROOT / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

import runtime_config


class RuntimeConfigTests(unittest.TestCase):
    def test_process_env_overrides_farplane_config_toml_and_rendered_toml(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane_home = root / "farplane"
            farplane_home.mkdir()
            codex_home = root / "codex"
            codex_home.mkdir()
            (codex_home / "config.toml").write_text(
                "\n".join(
                    [
                        "[env]",
                        'FARPLANE_CONVEX_SITE_URL = "https://rendered.convex.site"',
                        'FARPLANE_TELEMETRY_TOKEN = "rendered-token"',
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            (farplane_home / "config.toml").write_text(
                "\n".join(
                    [
                        "[runtime]",
                        'codex_app_server_url = "ws://127.0.0.1:9999"',
                        "",
                        "[convex]",
                        'site_url = "https://canonical.convex.site"',
                        'telemetry_token = "canonical-token"',
                        "",
                        "[integrations]",
                        'notion_token = "canonical-notion"',
                        "",
                        "[livekit]",
                        'url = "wss://example.livekit.cloud"',
                        'api_key = "livekit-key"',
                        'api_secret = "livekit-secret"',
                        'phone_number = "+15551234567"',
                        'phone_number_id = "PN_test"',
                        'sip_dispatch_rule_id = "SDR_test"',
                        "",
                        "[livekit.sip]",
                        'outbound_trunk_id = "ST_test"',
                        'outbound_address = "sip.example.com"',
                        'auth_username = "sip-user"',
                        'auth_password = "sip-pass"',
                        'telnyx_api_key = "telnyx-key"',
                        "",
                        "[fish_audio]",
                        'api_key = "fish-key"',
                        'reference_id = "fish-voice"',
                        'model = "s1"',
                        'latency_mode = "balanced"',
                        "",
                        "[phone_reminder]",
                        'recipient_phone = "+15557654321"',
                        'agent_name = "farplane-phone-reminder"',
                        'caller_number = "+15551234567"',
                        "",
                        "[env]",
                        'FARPLANE_STATE_BASE = "http://127.0.0.1:5173"',
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            env = runtime_config.load_runtime_env(
                {
                    "CODEX_HOME": str(codex_home),
                    "FARPLANE_STATE_DIR": str(farplane_home),
                    "FARPLANE_CONVEX_SITE_URL": "https://process.convex.site",
                }
            )

        self.assertEqual(env["FARPLANE_CONVEX_SITE_URL"], "https://process.convex.site")
        self.assertEqual(env["FARPLANE_TELEMETRY_TOKEN"], "canonical-token")
        self.assertEqual(env["NOTION_TOKEN"], "canonical-notion")
        self.assertNotIn("NOTION_API_KEY", env)
        self.assertEqual(env["CODEX_APP_SERVER_URL"], "ws://127.0.0.1:9999")
        self.assertEqual(env["FARPLANE_STATE_BASE"], "http://127.0.0.1:5173")
        self.assertEqual(env["LIVEKIT_URL"], "wss://example.livekit.cloud")
        self.assertEqual(env["LIVEKIT_API_KEY"], "livekit-key")
        self.assertEqual(env["LIVEKIT_API_SECRET"], "livekit-secret")
        self.assertEqual(env["LIVEKIT_PHONE_NUMBER"], "+15551234567")
        self.assertEqual(env["LIVEKIT_PHONE_NUMBER_ID"], "PN_test")
        self.assertEqual(env["LIVEKIT_SIP_DISPATCH_RULE_ID"], "SDR_test")
        self.assertEqual(env["LIVEKIT_SIP_TRUNK_ID"], "ST_test")
        self.assertEqual(env["LIVEKIT_SIP_OUTBOUND_ADDRESS"], "sip.example.com")
        self.assertEqual(env["LIVEKIT_SIP_AUTH_USERNAME"], "sip-user")
        self.assertEqual(env["LIVEKIT_SIP_AUTH_PASSWORD"], "sip-pass")
        self.assertEqual(env["TELNYX_API_KEY"], "telnyx-key")
        self.assertEqual(env["LIVEKIT_SIP_NUMBER"], "+15551234567")
        self.assertEqual(env["FISH_API_KEY"], "fish-key")
        self.assertEqual(env["FISH_AUDIO_REFERENCE_ID"], "fish-voice")
        self.assertEqual(env["FISH_AUDIO_MODEL"], "s1")
        self.assertEqual(env["FISH_AUDIO_LATENCY_MODE"], "balanced")
        self.assertEqual(env["FARPLANE_REMINDER_PHONE"], "+15557654321")
        self.assertEqual(env["FARPLANE_PHONE_REMINDER_AGENT_NAME"], "farplane-phone-reminder")

    def test_rendered_config_toml_env_is_loaded_when_farplane_config_is_absent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            codex_home = root / "codex"
            codex_home.mkdir()
            (codex_home / "config.toml").write_text(
                "\n".join(
                    [
                        "[env]",
                        'FARPLANE_CONVEX_SITE_URL = "https://rendered.convex.site"',
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            env = runtime_config.load_runtime_env(
                {
                    "CODEX_HOME": str(codex_home),
                    "FARPLANE_STATE_DIR": str(root / "farplane"),
                }
            )

        self.assertEqual(env["FARPLANE_CONVEX_SITE_URL"], "https://rendered.convex.site")

    def test_disable_flag_uses_process_values_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane_home = root / "farplane"
            farplane_home.mkdir()
            codex_home = root / "codex"
            codex_home.mkdir()
            (codex_home / "config.toml").write_text(
                "[env]\nFARPLANE_TELEMETRY_TOKEN = \"rendered-token\"\n",
                encoding="utf-8",
            )
            (farplane_home / "config.toml").write_text(
                "[env]\nFARPLANE_CONVEX_SITE_URL = \"https://canonical.convex.site\"\n",
                encoding="utf-8",
            )

            env = runtime_config.load_runtime_env(
                {
                    "CODEX_HOME": str(codex_home),
                    "FARPLANE_CONFIG_DISABLE": "1",
                    "FARPLANE_STATE_DIR": str(root / "farplane"),
                    "FARPLANE_CONVEX_SITE_URL": "https://env.convex.site",
                }
            )

        self.assertEqual(env["FARPLANE_CONVEX_SITE_URL"], "https://env.convex.site")
        self.assertNotIn("FARPLANE_TELEMETRY_TOKEN", env)


if __name__ == "__main__":
    unittest.main()
