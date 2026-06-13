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
    todos: str | None = None,
    direct_checklist: str | None = None,
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
                "## Context",
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
    if direct_checklist is not None:
        skill_file = skill_dir / "SKILL.md"
        skill_file.write_text(
            skill_file.read_text(encoding="utf-8").replace(
                "Use this for tests.",
                f"{checklists.CHECKLIST_BEGIN}\n"
                f"{checklists.TODO_HEADING}\n\n"
                f"{direct_checklist}\n"
                f"{checklists.CHECKLIST_END}\n\n"
                "Use this for tests.",
            ),
            encoding="utf-8",
        )
    return skill_dir


class SyncSkillChecklistsTests(unittest.TestCase):
    def test_check_fails_when_local_skill_has_legacy_todos_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "review", todos="# Todos\n\n- [ ] Do the important thing.\n")

            self.assertEqual(checklists.sync_repo(repo, write=False), 1)

    def test_legacy_todos_fails_even_when_direct_checklist_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            skill_dir = write_skill(repo, "review", direct_checklist="- [ ] Do the important thing.")
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
                    "## Todo List\n\n- [ ] Manual item.\n\nUse this for tests.",
                ),
                encoding="utf-8",
            )

            self.assertEqual(checklists.sync_repo(repo, write=True), 1)

            text = skill_file.read_text(encoding="utf-8")
            self.assertIn("Use this for tests.", text)
            self.assertNotIn(checklists.CHECKLIST_BEGIN, text)

    def test_local_skill_with_direct_checklist_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "review", direct_checklist="- [ ] Manual item.")

            self.assertEqual(checklists.sync_repo(repo, write=False), 0)

    def test_local_skill_without_todos_or_direct_checklist_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "review")

            self.assertEqual(checklists.sync_repo(repo, write=False), 1)

    def test_external_skill_without_todos_is_skipped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "agent-browser", source="external")

            self.assertEqual(checklists.sync_repo(repo, write=False), 0)


if __name__ == "__main__":
    unittest.main()
