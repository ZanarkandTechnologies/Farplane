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

import runtime_config


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


class RuntimeConfigTests(unittest.TestCase):
    def test_saved_config_and_secrets_override_legacy_env_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            local_env = root / "config.local.env"
            local_env.write_text(
                "\n".join(
                    [
                        "FARPLANE_CONVEX_SITE_URL=https://legacy.convex.site",
                        "FARPLANE_TELEMETRY_TOKEN=legacy-token",
                        "NOTION_TOKEN=legacy-notion",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            write_json(
                root / "farplane" / "config.json",
                {"env": {"FARPLANE_CONVEX_SITE_URL": "https://saved.convex.site"}},
            )
            write_json(
                root / "farplane" / "secrets.json",
                {
                    "env": {"FARPLANE_TELEMETRY_TOKEN": "saved-token"},
                    "integrations": {"notionApiKey": "saved-notion"},
                },
            )

            env = runtime_config.load_runtime_env(
                {"FARPLANE_STATE_DIR": str(root / "farplane")},
                local_env,
            )

        self.assertEqual(env["FARPLANE_CONVEX_SITE_URL"], "https://saved.convex.site")
        self.assertEqual(env["FARPLANE_TELEMETRY_TOKEN"], "saved-token")
        self.assertEqual(env["NOTION_TOKEN"], "saved-notion")

    def test_disable_flag_uses_process_or_legacy_values_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_json(
                root / "farplane" / "config.json",
                {"env": {"FARPLANE_CONVEX_SITE_URL": "https://saved.convex.site"}},
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
