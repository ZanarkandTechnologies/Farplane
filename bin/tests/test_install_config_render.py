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
            # The old reviewer profile is not a desk: it is backed up and not re-rendered.
            self.assertFalse((target / "reviewer.config.toml").exists())
            desk_profile = tomllib.loads((target / "engineer.config.toml").read_text(encoding="utf-8"))
            self.assertIn("Engineer desk", desk_profile["developer_instructions"])
            self.assertIn({"name": "impl-plan", "enabled": True}, desk_profile["skills"]["config"])
            self.assertIn({"name": "prospect", "enabled": False}, desk_profile["skills"]["config"])
            backups = list((target / ".install-backups").glob("*/reviewer.config.toml"))
            self.assertEqual(len(backups), 1)
            self.assertIn("legacy = true", backups[0].read_text(encoding="utf-8"))
            self.assertIn(
                "# BEGIN FARPLANE GENERATED SKILL PROFILE",
                (target / "config.toml").read_text(encoding="utf-8"),
            )

    def test_full_install_keeps_a_reapproved_hook_trust_hash(self) -> None:
        marker = "# Machine-local config appended from config.local.toml"
        key = '[hooks.state."/h/hooks.json:post_tool_use:1:0"]'
        with tempfile.TemporaryDirectory() as temp_dir:
            home = Path(temp_dir) / "home"
            target = home / ".codex"
            target.mkdir(parents=True)
            # Codex rewrote the existing entry in config.toml when the operator re-approved a changed hook.
            (target / "config.toml").write_text(f'model = "x"\n\n{marker}\n\n{key}\ntrusted_hash = "sha256:new"\n', encoding="utf-8")
            (target / "config.local.toml").write_text(f'{key}\ntrusted_hash = "sha256:old"\n', encoding="utf-8")
            env = {
                **os.environ,
                "HOME": str(home),
                "REF_API_KEY": "test-ref-key",
                "NOTION_TOKEN": "test-notion-token",
                "FARPLANE_SKIP_GLOBAL_CLI": "1",
            }
            result = subprocess.run(
                ["bash", str(INSTALL), "--target", str(target)], cwd=ROOT, env=env, capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

            for name in ("config.local.toml", "config.toml"):
                hooks = tomllib.loads((target / name).read_text(encoding="utf-8"))["hooks"]["state"]
                self.assertEqual(hooks["/h/hooks.json:post_tool_use:1:0"]["trusted_hash"], "sha256:new", name)


if __name__ == "__main__":
    unittest.main()
