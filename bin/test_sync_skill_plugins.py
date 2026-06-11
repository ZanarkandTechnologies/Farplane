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


def write_review_rubric(root: Path) -> None:
    rubric_dir = root / "docs/review/rubrics"
    rubric_dir.mkdir(parents=True)
    (rubric_dir / "notes.md").write_text("rubric notes\n", encoding="utf-8")


class SyncSkillPluginsTests(unittest.TestCase):
    def test_sync_generates_one_plugin_per_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "review", "Run quality checks.")
            write_skill(repo, "visual-qa", "Inspect browser screenshots.")
            write_review_rubric(repo)

            result = syncer.sync_skill_plugins(repo)

            self.assertEqual(result.skill_count, 2)
            self.assertEqual(result.plugin_count, 4)
            manifest = json.loads(
                (
                    repo
                    / ".farplane/generated/skill-plugins/plugins/review/.codex-plugin/plugin.json"
                ).read_text()
            )
            self.assertEqual(manifest["name"], "review")
            self.assertEqual(manifest["skills"], "./skills/")
            self.assertEqual(manifest["interface"]["capabilities"], ["Skills"])
            self.assertTrue(
                (
                    repo
                    / ".farplane/generated/skill-plugins/plugins/review/skills/review/SKILL.md"
                ).exists()
            )
            self.assertTrue(
                (
                    repo
                    / ".farplane/generated/skill-plugins/plugins/review/docs/review/rubrics/notes.md"
                ).exists()
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
            core = repo / ".farplane/generated/skill-plugins/plugins/farplane-core"
            frontend = repo / ".farplane/generated/skill-plugins/plugins/farplane-frontend"
            self.assertTrue((core / "skills" / "review" / "SKILL.md").exists())
            self.assertTrue((core / "skills" / "plan" / "SKILL.md").exists())
            self.assertTrue((frontend / "skills" / "frontend-craft" / "SKILL.md").exists())
            manifest = json.loads((core / ".codex-plugin" / "plugin.json").read_text())
            self.assertEqual(manifest["name"], "farplane-core")
            self.assertEqual(manifest["interface"]["displayName"], "Farplane Core")

    def test_sync_generates_marketplace_entries(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "review", "Run quality checks.")

            syncer.sync_skill_plugins(repo)

            marketplace = json.loads(
                (
                    repo
                    / ".farplane/generated/skill-plugins/.agents/plugins/marketplace.json"
                ).read_text()
            )
            self.assertEqual(marketplace["name"], "farplane-skills")
            self.assertEqual(marketplace["interface"]["displayName"], "Farplane Skills")
            self.assertEqual(
                marketplace["plugins"][0],
                {
                    "name": "farplane-core",
                    "source": {"source": "local", "path": "./plugins/farplane-core"},
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

    def test_sync_can_generate_selected_marketplace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "review", "Run quality checks.")
            write_skill(repo, "visual-qa", "Inspect browser screenshots.")

            result = syncer.sync_skill_plugins(
                repo,
                selected_names=["farplane-frontend", "review"],
            )

            self.assertEqual(result.plugin_count, 2)
            marketplace = json.loads(
                (
                    repo
                    / ".farplane/generated/skill-plugins/.agents/plugins/marketplace.json"
                ).read_text()
            )
            self.assertEqual(
                [plugin["name"] for plugin in marketplace["plugins"]],
                ["farplane-frontend", "review"],
            )
            self.assertTrue(
                (
                    repo
                    / ".farplane/generated/skill-plugins/plugins/farplane-frontend"
                ).exists()
            )
            self.assertTrue((repo / ".farplane/generated/skill-plugins/plugins/review").exists())
            self.assertFalse(
                (repo / ".farplane/generated/skill-plugins/plugins/visual-qa").exists()
            )

    def test_sync_rejects_unknown_selected_plugin(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "review", "Run quality checks.")

            with self.assertRaisesRegex(ValueError, "Unknown plugin"):
                syncer.sync_skill_plugins(repo, selected_names=["missing"])

    def test_listing_treats_farplane_named_skills_as_individual_plugins(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "farplane-invocation", "Invoke Farplane envelopes.")
            plugins = syncer.build_plugins(syncer.discover_skills(repo / "skills"))

            listing = syncer.plugin_listing(plugins)

            bundle_section, individual_section = listing.split("Individual skill plugins:")
            self.assertNotIn("- farplane-invocation:", bundle_section)
            self.assertIn("- farplane-invocation:", individual_section)

    def test_check_uses_fresh_generated_plugins(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "review", "Run quality checks.")
            syncer.sync_skill_plugins(repo)
            (
                repo
                / ".farplane/generated/skill-plugins/plugins/review/skills/review/SKILL.md"
            ).write_text("stale\n")

            errors = syncer.check_in_sync(repo)

            self.assertFalse(errors)

    def test_sync_can_install_personal_marketplace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "repo"
            home = root / "home"
            write_skill(repo, "review", "Run quality checks.")

            result = syncer.sync_personal_skill_plugins(repo, home=home)

            self.assertEqual(result.plugin_count, 2)
            self.assertTrue(
                (home / ".codex/plugins/farplane/review/.codex-plugin/plugin.json").exists()
            )
            marketplace = json.loads(
                (home / ".agents/plugins/marketplace.json").read_text()
            )
            self.assertEqual(
                marketplace["plugins"][0]["source"]["path"],
                "./.codex/plugins/farplane/farplane-core",
            )


if __name__ == "__main__":
    unittest.main()
