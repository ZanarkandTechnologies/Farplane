from __future__ import annotations

import os
import subprocess
import tempfile
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
INSTALL = ROOT / "install.sh"


class InstallConfigRenderTests(unittest.TestCase):
    def test_full_install_preserves_disabled_notify_from_prior_managed_config(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            home = Path(temp_dir) / "home"
            target = home / ".codex"
            target.mkdir(parents=True)
            (target / "config.toml").write_text(
                "# Managed template for ~/.codex/config.toml.\n\n"
                'model = "gpt-5.5"\n',
                encoding="utf-8",
            )
            env = {
                **os.environ,
                "HOME": str(home),
                "REF_API_KEY": "test-ref-key",
                "NOTION_TOKEN": "test-notion-token",
                "FARPLANE_SKIP_GLOBAL_CLI": "1",
            }

            result = subprocess.run(
                ["bash", str(INSTALL), "--target", str(target)],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertNotIn("notify", tomllib.loads((target / "config.toml").read_text(encoding="utf-8")))

    def test_full_install_preserves_desktop_plugins_and_renders_profiles(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            home = Path(temp_dir) / "home"
            target = home / ".codex"
            target.mkdir(parents=True)
            (target / "config.toml").write_text(
                """[desktop]
followUpQueueMode = "queue"

[plugins."browser@openai-bundled"]
enabled = true
""",
                encoding="utf-8",
            )
            stale_profile = target / "reviewer.config.toml"
            stale_profile.write_text(
                "# BEGIN FARPLANE GENERATED SKILL PROFILE\nlegacy = true\n",
                encoding="utf-8",
            )
            env = {
                **os.environ,
                "HOME": str(home),
                "REF_API_KEY": "test-ref-key",
                "NOTION_TOKEN": "test-notion-token",
                "FARPLANE_SKIP_GLOBAL_CLI": "1",
            }
            result = subprocess.run(
                ["bash", str(INSTALL), "--target", str(target)],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

            rendered = tomllib.loads((target / "config.toml").read_text(encoding="utf-8"))
            self.assertEqual(rendered["desktop"]["followUpQueueMode"], "queue")
            self.assertTrue(rendered["plugins"]["browser@openai-bundled"]["enabled"])
            self.assertIn("Machine-local TOML", (target / "config.local.toml").read_text(encoding="utf-8"))
            self.assertTrue((target / "reviewer.config.toml").is_file())
            self.assertIn(
                "# BEGIN FARPLANE GENERATED SKILL PROFILE",
                (target / "reviewer.config.toml").read_text(encoding="utf-8"),
            )
            profile_content = (target / "reviewer.config.toml").read_text(encoding="utf-8")
            self.assertNotIn("legacy = true", profile_content)
            self.assertIn('name = "coderabbit-review"', profile_content)
            backups = list((target / ".install-backups").glob("*/reviewer.config.toml"))
            self.assertEqual(len(backups), 1)
            self.assertIn("legacy = true", backups[0].read_text(encoding="utf-8"))
            self.assertIn(
                "# BEGIN FARPLANE GENERATED SKILL PROFILE",
                (target / "config.toml").read_text(encoding="utf-8"),
            )


if __name__ == "__main__":
    unittest.main()
