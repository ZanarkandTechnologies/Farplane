#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import install_selected_skills as installer


def write_skill(
    root: Path,
    name: str,
    description: str,
    source: str = "local",
    todos: str | None = "- [ ] Follow the checklist.",
) -> None:
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
    if todos is not None:
        (skill_dir / "todos.md").write_text(todos + "\n", encoding="utf-8")
    (skill_dir / "references").mkdir()
    (skill_dir / "references" / "note.md").write_text("Reference.\n", encoding="utf-8")


class InstallSelectedSkillsTests(unittest.TestCase):
    def test_discover_and_search_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "review", "Run quality checks.")
            write_skill(repo, "visual-qa", "Inspect browser screenshots.")

            skills = installer.discover_skills(repo / "skills")
            self.assertEqual([skill.name for skill in skills], ["review", "visual-qa"])

            matches = installer.filter_skills(skills, "browser")
            self.assertEqual([skill.name for skill in matches], ["visual-qa"])

    def test_installs_only_selected_skills_as_rendered_packages(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            target = Path(tmp) / "codex"
            write_skill(repo, "review", "Run quality checks.", todos="- [ ] Read proof.")
            write_skill(repo, "visual-qa", "Inspect browser screenshots.")

            result = installer.install_skills(repo, target, ["review"], False, False)

            self.assertEqual(result.installed, ["review"])
            installed = target / "skills" / "review"
            self.assertTrue(installed.is_dir())
            self.assertFalse(installed.is_symlink())
            skill_text = (installed / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn(installer.EMBEDDED_TODOS_BEGIN, skill_text)
            self.assertIn("## Embedded Skill Checklist", skill_text)
            self.assertIn("- [ ] Read proof.", skill_text)
            self.assertEqual(
                (installed / "todos.md").read_text(encoding="utf-8"),
                "- [ ] Read proof.\n",
            )
            self.assertTrue((installed / "references" / "note.md").exists())
            self.assertFalse((target / "skills" / "visual-qa").exists())

    def test_install_without_todos_keeps_skill_body_unembedded(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            target = Path(tmp) / "codex"
            write_skill(repo, "review", "Run quality checks.", todos=None)

            installer.install_skills(repo, target, ["review"], False, False)

            skill_text = (target / "skills" / "review" / "SKILL.md").read_text(
                encoding="utf-8"
            )
            self.assertNotIn(installer.EMBEDDED_TODOS_BEGIN, skill_text)
            self.assertFalse((target / "skills" / "review" / "todos.md").exists())

    def test_install_with_direct_checklist_skips_generated_embedding(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            target = Path(tmp) / "codex"
            write_skill(repo, "review", "Run quality checks.", todos="- [ ] Legacy proof.")
            skill_file = repo / "skills" / "review" / "SKILL.md"
            skill_file.write_text(
                skill_file.read_text(encoding="utf-8")
                + "\n## Important Checklist\n\n- [ ] Direct proof.\n",
                encoding="utf-8",
            )

            installer.install_skills(repo, target, ["review"], False, False)

            skill_text = (target / "skills" / "review" / "SKILL.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("- [ ] Direct proof.", skill_text)
            self.assertNotIn(installer.EMBEDDED_TODOS_BEGIN, skill_text)
            self.assertNotIn("- [ ] Legacy proof.", skill_text)
            self.assertTrue((target / "skills" / "review" / "todos.md").exists())

    def test_mentioning_direct_checklist_heading_still_embeds_legacy_todos(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            target = Path(tmp) / "codex"
            write_skill(repo, "review", "Run quality checks.", todos="- [ ] Legacy proof.")
            skill_file = repo / "skills" / "review" / "SKILL.md"
            skill_file.write_text(
                skill_file.read_text(encoding="utf-8")
                + "\nMention `## Important Checklist` in prose.\n",
                encoding="utf-8",
            )

            installer.install_skills(repo, target, ["review"], False, False)

            skill_text = (target / "skills" / "review" / "SKILL.md").read_text(
                encoding="utf-8"
            )
            self.assertIn(installer.EMBEDDED_TODOS_BEGIN, skill_text)
            self.assertIn("- [ ] Legacy proof.", skill_text)

    def test_reinstall_skips_existing_matching_rendered_package(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            target = Path(tmp) / "codex"
            write_skill(repo, "review", "Run quality checks.")

            installer.install_skills(repo, target, ["review"], False, False)
            result = installer.install_skills(repo, target, ["review"], False, False)

            self.assertEqual(result.installed, [])
            self.assertEqual(result.skipped, ["review"])

    def test_reinstall_refreshes_changed_support_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            target = Path(tmp) / "codex"
            write_skill(repo, "review", "Run quality checks.")
            reference = repo / "skills" / "review" / "references" / "note.md"

            installer.install_skills(repo, target, ["review"], False, False)
            reference.write_text("Changed reference.\n", encoding="utf-8")
            result = installer.install_skills(repo, target, ["review"], False, False)

            self.assertEqual(result.installed, ["review"])
            self.assertEqual(result.skipped, [])
            self.assertEqual(
                (target / "skills" / "review" / "references" / "note.md").read_text(
                    encoding="utf-8"
                ),
                "Changed reference.\n",
            )

    def test_prune_only_removes_repo_managed_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            target = Path(tmp) / "codex"
            write_skill(repo, "review", "Run quality checks.")
            write_skill(repo, "visual-qa", "Inspect browser screenshots.")
            external = Path(tmp) / "external"
            write_skill(external, "outside", "External skill.")

            installer.install_skills(repo, target, ["review", "visual-qa"], False, False)
            outside_dest = target / "skills" / "outside"
            outside_dest.symlink_to(external / "skills" / "outside")

            result = installer.install_skills(repo, target, ["review"], True, False)

            self.assertEqual(result.pruned, ["visual-qa"])
            self.assertFalse((target / "skills" / "visual-qa").exists())
            self.assertTrue(outside_dest.exists())

    def test_dry_run_does_not_create_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            target = Path(tmp) / "codex"
            write_skill(repo, "review", "Run quality checks.")

            result = installer.install_skills(repo, target, ["review"], False, True)

            self.assertTrue(result.dry_run)
            self.assertEqual(result.installed, ["review"])
            self.assertFalse(target.exists())

    def test_main_all_installs_every_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            target = Path(tmp) / "codex"
            write_skill(repo, "review", "Run quality checks.")
            write_skill(repo, "visual-qa", "Inspect browser screenshots.")

            output = StringIO()
            with redirect_stdout(output):
                code = installer.main(
                    ["--repo", str(repo), "--target", str(target), "--all", "--json"]
                )

            self.assertEqual(code, 0)
            payload = json.loads(output.getvalue())
            self.assertEqual(payload["installed"], ["review", "visual-qa"])
            self.assertTrue((target / "skills" / "review" / "SKILL.md").exists())
            self.assertTrue((target / "skills" / "visual-qa" / "SKILL.md").exists())

    def test_main_json_search(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            write_skill(repo, "review", "Run quality checks.")
            output = StringIO()

            with redirect_stdout(output):
                code = installer.main(["--repo", str(repo), "--search", "quality", "--json"])

            self.assertEqual(code, 0)
            payload = json.loads(output.getvalue())
            self.assertEqual(payload[0]["name"], "review")

    def test_unknown_skill_exits_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            write_skill(repo, "review", "Run quality checks.")

            with self.assertRaises(SystemExit) as raised:
                installer.main(["--repo", str(repo), "--skills", "missing"])

            self.assertIn("Unknown skill", str(raised.exception))


if __name__ == "__main__":
    unittest.main()
