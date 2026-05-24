#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sync_skill_plugins as syncer


def write_skill(root: Path, name: str, description: str, source: str = "local") -> None:
    skill_dir = root / "skills" / name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "\n".join(
            [
                "---",
                f"name: {name}",
                f"description: {description}",
                "tier: 2",
                f"source: {source}",
                "---",
                "",
                "Body.",
            ]
        ),
        encoding="utf-8",
    )
    (skill_dir / "references").mkdir()
    (skill_dir / "references" / "notes.md").write_text("notes\n", encoding="utf-8")


class SyncSkillPluginsTests(unittest.TestCase):
    def test_sync_generates_one_plugin_per_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "review", "Run quality checks.")
            write_skill(repo, "visual-qa", "Inspect browser screenshots.")

            result = syncer.sync_skill_plugins(repo)

            self.assertEqual(result.skill_count, 2)
            self.assertEqual(result.plugin_count, 4)
            manifest = json.loads(
                (repo / "plugins" / "review" / ".codex-plugin" / "plugin.json").read_text()
            )
            self.assertEqual(manifest["name"], "review")
            self.assertEqual(manifest["skills"], "./skills/")
            self.assertEqual(manifest["interface"]["capabilities"], ["Skills"])
            self.assertTrue((repo / "plugins" / "review" / "skills" / "review" / "SKILL.md").exists())
            self.assertTrue(
                (repo / "plugins" / "review" / "skills" / "review" / "references" / "notes.md").exists()
            )

    def test_sync_generates_curated_bundle_plugins(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "review", "Run quality checks.")
            write_skill(repo, "plan", "Plan the work.")
            write_skill(repo, "execute", "Execute the work.")
            write_skill(repo, "frontend-craft", "Build frontend surfaces.")
            write_skill(repo, "visual-qa", "Inspect browser screenshots.")

            result = syncer.sync_skill_plugins(repo)

            self.assertEqual(result.bundle_count, 2)
            core = repo / "plugins" / "codexter-core"
            frontend = repo / "plugins" / "codexter-frontend"
            self.assertTrue((core / "skills" / "review" / "SKILL.md").exists())
            self.assertTrue((core / "skills" / "plan" / "SKILL.md").exists())
            self.assertTrue((frontend / "skills" / "frontend-craft" / "SKILL.md").exists())
            manifest = json.loads((core / ".codex-plugin" / "plugin.json").read_text())
            self.assertEqual(manifest["name"], "codexter-core")
            self.assertEqual(manifest["interface"]["displayName"], "Codexter Core")

    def test_sync_generates_marketplace_entries(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "review", "Run quality checks.")

            syncer.sync_skill_plugins(repo)

            marketplace = json.loads((repo / ".agents" / "plugins" / "marketplace.json").read_text())
            self.assertEqual(marketplace["name"], "codexter-skills")
            self.assertEqual(marketplace["interface"]["displayName"], "Codexter Skills")
            self.assertEqual(
                marketplace["plugins"][0],
                {
                    "name": "codexter-core",
                    "source": {"source": "local", "path": "./plugins/codexter-core"},
                    "policy": {
                        "installation": "AVAILABLE",
                        "authentication": "ON_INSTALL",
                    },
                    "category": "Productivity",
                },
            )
            self.assertEqual(
                marketplace["plugins"][1],
                {
                    "name": "review",
                    "source": {"source": "local", "path": "./plugins/review"},
                    "policy": {
                        "installation": "AVAILABLE",
                        "authentication": "ON_INSTALL",
                    },
                    "category": "Productivity",
                },
            )

    def test_check_detects_stale_generated_plugins(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "review", "Run quality checks.")
            syncer.sync_skill_plugins(repo)
            (repo / "plugins" / "review" / "skills" / "review" / "SKILL.md").write_text("stale\n")

            errors = syncer.check_in_sync(repo)

            self.assertTrue(errors)
            self.assertIn("plugins", errors[0])


if __name__ == "__main__":
    unittest.main()
