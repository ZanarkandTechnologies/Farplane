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

import import_installed_skills as importer


def write_installed_skill(
    source: Path,
    name: str,
    description: str = "Turn input into output.",
    tier: str = "2",
    skill_source: str = "local",
    embedded_todos: bool = False,
) -> None:
    skill_dir = source / name
    skill_dir.mkdir(parents=True)
    lines = [
        "---",
        f"name: {name}",
        f"description: {description}",
        f"tier: {tier}",
        f"source: {skill_source}",
        "---",
        "",
        "# Skill",
        "",
        "Body.",
    ]
    if embedded_todos:
        lines.extend(
            [
                "",
                importer.EMBEDDED_TODOS_BEGIN,
                "## Embedded Skill Todo List",
                "",
                "- [ ] Generated installed-only todo.",
                importer.EMBEDDED_TODOS_END,
            ]
        )
        (skill_dir / "todos.md").write_text(
            "- [ ] Generated installed-only todo.\n", encoding="utf-8"
        )
    (skill_dir / "SKILL.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (skill_dir / "references").mkdir()
    (skill_dir / "references" / "note.md").write_text("Reference.\n", encoding="utf-8")


def write_repo_skill(repo: Path, name: str, body: str = "Old body.\n") -> None:
    skill_dir = repo / "skills" / name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(body, encoding="utf-8")


class ImportInstalledSkillsTests(unittest.TestCase):
    def test_list_marks_repo_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / ".codex" / "skills"
            repo = root / "repo"
            write_installed_skill(source, "new-skill")
            write_installed_skill(source, "existing-skill")
            write_repo_skill(repo, "existing-skill")

            rows = [
                importer.skill_row(skill, repo)
                for skill in importer.discover_skills(source)
            ]

            self.assertEqual(
                {row["name"]: row["repo_status"] for row in rows},
                {"existing-skill": "exists", "new-skill": "new"},
            )

    def test_import_new_skill_copies_files_and_strips_embedded_todos(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / ".codex" / "skills"
            repo = root / "repo"
            write_installed_skill(source, "review-plus", embedded_todos=True)

            result = importer.import_skills(
                source, repo, ["review-plus"], overwrite=False, dry_run=False
            )

            self.assertEqual(result.imported, ["review-plus"])
            dest = repo / "skills" / "review-plus"
            self.assertTrue((dest / "references" / "note.md").exists())
            self.assertFalse((dest / "todos.md").exists())
            skill_text = (dest / "SKILL.md").read_text(encoding="utf-8")
            self.assertNotIn(importer.EMBEDDED_TODOS_BEGIN, skill_text)
            self.assertNotIn("Generated installed-only todo", skill_text)
            self.assertTrue(
                any(
                    "removed generated embedded todo block" in note
                    for note in result.warnings["review-plus"]
                )
            )

    def test_existing_skill_is_skipped_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / ".codex" / "skills"
            repo = root / "repo"
            write_installed_skill(source, "review")
            write_repo_skill(repo, "review", "Keep me.\n")

            result = importer.import_skills(
                source, repo, ["review"], overwrite=False, dry_run=False
            )

            self.assertEqual(result.imported, [])
            self.assertEqual(result.skipped_existing, ["review"])
            self.assertEqual(
                (repo / "skills" / "review" / "SKILL.md").read_text(encoding="utf-8"),
                "Keep me.\n",
            )

    def test_overwrite_backs_up_existing_skill(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / ".codex" / "skills"
            repo = root / "repo"
            write_installed_skill(source, "review")
            write_repo_skill(repo, "review", "Old source.\n")

            result = importer.import_skills(
                source, repo, ["review"], overwrite=True, dry_run=False
            )

            self.assertEqual(result.imported, ["review"])
            self.assertEqual(result.overwritten, ["review"])
            backup = Path(result.backup_root) / "skills" / "review" / "SKILL.md"
            self.assertEqual(backup.read_text(encoding="utf-8"), "Old source.\n")
            self.assertIn(
                "Turn input into output.",
                (repo / "skills" / "review" / "SKILL.md").read_text(encoding="utf-8"),
            )

    def test_missing_skill_returns_missing_result_and_main_exits_one(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / ".codex" / "skills"
            repo = root / "repo"
            source.mkdir(parents=True)

            output = StringIO()
            with redirect_stdout(output):
                code = importer.main(
                    [
                        "--repo",
                        str(repo),
                        "--source",
                        str(source),
                        "--skills",
                        "missing",
                        "--json",
                    ]
                )

            self.assertEqual(code, 1)
            payload = json.loads(output.getvalue())
            self.assertEqual(payload["missing"], ["missing"])
            self.assertEqual(payload["imported"], [])

    def test_dry_run_json_does_not_write_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / ".codex" / "skills"
            repo = root / "repo"
            write_installed_skill(source, "dry-run-skill")

            output = StringIO()
            with redirect_stdout(output):
                code = importer.main(
                    [
                        "--repo",
                        str(repo),
                        "--source",
                        str(source),
                        "--skills",
                        "dry-run-skill",
                        "--dry-run",
                        "--json",
                    ]
                )

            self.assertEqual(code, 0)
            payload = json.loads(output.getvalue())
            self.assertTrue(payload["dry_run"])
            self.assertEqual(payload["imported"], ["dry-run-skill"])
            self.assertFalse((repo / "skills" / "dry-run-skill").exists())


if __name__ == "__main__":
    unittest.main()
