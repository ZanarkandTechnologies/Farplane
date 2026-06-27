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
    def test_farplane_config_toml_overrides_rendered_toml_and_process_env(self) -> None:
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
                        'NOTION_TOKEN = "rendered-notion"',
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

        self.assertEqual(env["FARPLANE_CONVEX_SITE_URL"], "https://canonical.convex.site")
        self.assertEqual(env["FARPLANE_TELEMETRY_TOKEN"], "canonical-token")
        self.assertEqual(env["NOTION_TOKEN"], "canonical-notion")
        self.assertEqual(env["CODEX_APP_SERVER_URL"], "ws://127.0.0.1:9999")
        self.assertEqual(env["FARPLANE_STATE_BASE"], "http://127.0.0.1:5173")

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
            (farplane_home / "config.toml").write_text(
                "[env]\nFARPLANE_CONVEX_SITE_URL = \"https://canonical.convex.site\"\n",
                encoding="utf-8",
            )

            env = runtime_config.load_runtime_env(
                {
                    "FARPLANE_CONFIG_DISABLE": "1",
                    "FARPLANE_STATE_DIR": str(root / "farplane"),
                    "FARPLANE_CONVEX_SITE_URL": "https://env.convex.site",
                }
            )

        self.assertEqual(env["FARPLANE_CONVEX_SITE_URL"], "https://env.convex.site")


if __name__ == "__main__":
    unittest.main()
