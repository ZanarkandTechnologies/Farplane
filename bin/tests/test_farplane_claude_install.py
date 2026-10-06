from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "bin" / "core"))

import farplane_claude_install as claude_install  # noqa: E402


class ClaudeInstallTests(unittest.TestCase):
    def test_install_renders_plugin_and_retires_settings_hooks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            operator_hook = {"hooks": [{"type": "command", "command": "echo mine"}]}
            legacy_hook = {"hooks": [{"type": "command", "command": f'python3 "{home}/farplane/hooks/user-turn/x.py"'}]}
            (home / "settings.json").write_text(json.dumps({"theme": "dark", "hooks": {"Stop": [operator_hook, legacy_hook]}}))
            (home / "CLAUDE.md").write_text("# mine\n")
            (home / "agents").mkdir()
            (home / "agents" / "farplane-reviewer.md").write_text(claude_install.AGENT_MARKER)

            first = claude_install.install(ROOT, home, register=False)
            second = claude_install.install(ROOT, home, register=False)

            settings = json.loads((home / "settings.json").read_text())
            self.assertEqual(settings, {"theme": "dark", "hooks": {"Stop": [operator_hook]}})
            self.assertEqual(first["retired_agents"], ["farplane-reviewer"])

            plugin = home / "farplane" / "plugin"
            hooks = json.loads((plugin / "hooks" / "hooks.json").read_text())["hooks"]
            for entry in hooks["Stop"]:
                for hook in entry["hooks"]:
                    self.assertTrue(hook["command"].startswith("FARPLANE_AGENT_RUNTIME=claude "))
                    self.assertNotIn(".codex/hooks", hook["command"])
            reviewer = (plugin / "agents" / "reviewer.md").read_text()
            self.assertIn("name: reviewer", reviewer)
            self.assertIn("disallowedTools:", reviewer)
            self.assertNotIn("gpt-", reviewer.split("---", 2)[1])
            manifest = json.loads((plugin / ".claude-plugin" / "plugin.json").read_text())
            self.assertEqual(manifest["name"], "farplane")
            self.assertTrue((home / "farplane" / ".claude-plugin" / "marketplace.json").is_file())

            claude_md = (home / "CLAUDE.md").read_text()
            self.assertTrue(claude_md.startswith("# mine\n"))
            self.assertEqual(claude_md.count(claude_install.CLAUDE_MD_BEGIN), 1)
            self.assertIn("@~/.farplane/USER.md", claude_md)

            self.assertTrue(first["plugin"])
            self.assertFalse(second["plugin"] or second["claude_md"] or second["retired_agents"])


if __name__ == "__main__":
    unittest.main()
