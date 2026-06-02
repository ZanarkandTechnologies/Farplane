#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import sync_skill_checklists as checklists


def write_skill(
    repo: Path,
    name: str,
    source: str = "local",
    todos: str | None = "# Todos\n\n- [ ] Do the important thing.\n",
) -> Path:
    skill_dir = repo / "skills" / name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "\n".join(
            [
                "---",
                f"name: {name}",
                "description: Test skill.",
                "tier: 2",
                f"source: {source}",
                "---",
                "",
                f"# {name}",
                "",
                "Use this for tests.",
                "",
                "## Workflow",
                "",
                "1. Work.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    if todos is not None:
        (skill_dir / "todos.md").write_text(todos, encoding="utf-8")
    return skill_dir


class SyncSkillChecklistsTests(unittest.TestCase):
    def test_check_fails_when_local_skill_has_unembedded_todos(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "review")

            self.assertEqual(checklists.sync_repo(repo, write=False), 1)

    def test_write_inserts_checklist_after_title(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            skill_dir = write_skill(repo, "review")

            self.assertEqual(checklists.sync_repo(repo, write=True), 0)

            text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("## Important Checklist\n\nSource: `SKILL.md`", text)
            self.assertLess(text.index("## Important Checklist"), text.index("Use this for tests."))
            self.assertNotIn("# Todos", text)
            self.assertTrue((skill_dir / "todos.md").exists())

    def test_write_removes_redundant_todos_after_direct_checklist_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            skill_dir = write_skill(repo, "review")
            checklists.sync_repo(repo, write=True)

            self.assertEqual(checklists.sync_repo(repo, write=True), 0)

            self.assertFalse((skill_dir / "todos.md").exists())
            self.assertEqual(checklists.sync_repo(repo, write=False), 0)

    def test_divergent_direct_checklist_and_todos_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            skill_dir = write_skill(repo, "review")
            checklists.sync_repo(repo, write=True)
            (skill_dir / "todos.md").write_text(
                "# Todos\n\n- [ ] Do the changed thing.\n",
                encoding="utf-8",
            )

            self.assertEqual(checklists.sync_repo(repo, write=True), 1)

            text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("- [ ] Do the important thing.", text)
            self.assertNotIn("- [ ] Do the changed thing.", text)

    def test_unmarked_direct_checklist_fails_instead_of_guessing_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            skill_dir = write_skill(repo, "review")
            skill_file = skill_dir / "SKILL.md"
            skill_file.write_text(
                skill_file.read_text(encoding="utf-8").replace(
                    "Use this for tests.",
                    "## Important Checklist\n\n- [ ] Manual item.\n\nUse this for tests.",
                ),
                encoding="utf-8",
            )

            self.assertEqual(checklists.sync_repo(repo, write=True), 1)

            text = skill_file.read_text(encoding="utf-8")
            self.assertIn("Use this for tests.", text)
            self.assertNotIn(checklists.CHECKLIST_BEGIN, text)

    def test_local_skill_without_todos_but_direct_checklist_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            skill_dir = write_skill(repo, "review", todos=None)
            skill_file = skill_dir / "SKILL.md"
            skill_file.write_text(
                skill_file.read_text(encoding="utf-8").replace(
                    "Use this for tests.",
                    f"{checklists.CHECKLIST_BEGIN}\n"
                    f"{checklists.CHECKLIST_HEADING}\n\n"
                    "Source: `SKILL.md`\n\n"
                    "- [ ] Manual item.\n"
                    f"{checklists.CHECKLIST_END}\n\n"
                    "Use this for tests.",
                ),
                encoding="utf-8",
            )

            self.assertEqual(checklists.sync_repo(repo, write=False), 0)

    def test_local_skill_without_todos_or_direct_checklist_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "review", todos=None)

            self.assertEqual(checklists.sync_repo(repo, write=False), 1)

    def test_external_skill_without_todos_is_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "agent-browser", source="external", todos=None)

            self.assertEqual(checklists.sync_repo(repo, write=False), 0)


if __name__ == "__main__":
    unittest.main()
