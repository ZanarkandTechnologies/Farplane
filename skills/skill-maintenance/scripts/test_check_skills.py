#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import check_skills


def write_registry(repo: Path, name: str, *, version: str = "0.1.0") -> None:
    registry_dir = repo / "docs" / "skills"
    registry_dir.mkdir(parents=True)
    row = {
        "name": name,
        "path": f"skills/{name}/SKILL.md",
        "source": "local",
        "tier": 2,
        "skill_template_version": version,
    }
    (registry_dir / "registry.jsonl").write_text(json.dumps(row) + "\n", encoding="utf-8")


def write_skill(repo: Path, name: str, body: str) -> None:
    skill_dir = repo / "skills" / name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(body, encoding="utf-8")


VALID_SKILL = """---
name: example
description: Test skill.
tier: 2
source: local
skill_template_version: "0.1.0"
---

# Example

## Context

Use this for tests.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

1. [ ] Read context.
2. [ ] Choose the branch.
   1. [ ] Default branch.
   2. [ ] Repair branch.
3. [ ] Review before completion.
   - [ ] Repeatability from files alone.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

- Template.

## Gotchas

- Gotcha.

## Reference Map

- Reference.

## Output

- Output.
"""


class CheckSkillsTemplateStructureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.original_repo_root = check_skills.REPO_ROOT

    def tearDown(self) -> None:
        check_skills.REPO_ROOT = self.original_repo_root

    def test_template_structure_accepts_current_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            check_skills.REPO_ROOT = repo
            write_registry(repo, "example")
            write_skill(repo, "example", VALID_SKILL)

            self.assertEqual(check_skills.template_structure_errors("0.1.0"), [])

    def test_template_structure_rejects_generic_job_heading(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            check_skills.REPO_ROOT = repo
            write_registry(repo, "example")
            write_skill(repo, "example", VALID_SKILL.replace("## Templates", "## Job\n\nDo it.\n\n## Templates"))

            errors = check_skills.template_structure_errors("0.1.0")

            self.assertTrue(any("remove generic ## Job" in error for error in errors))

    def test_template_structure_rejects_top_level_plain_todos(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            check_skills.REPO_ROOT = repo
            write_registry(repo, "example")
            write_skill(repo, "example", VALID_SKILL.replace("1. [ ] Read context.", "- [ ] Read context."))

            errors = check_skills.template_structure_errors("0.1.0")

            self.assertTrue(any("top-level plain todo" in error for error in errors))
            self.assertFalse(any("numbered task items" in error for error in errors))

    def test_template_structure_rejects_unordered_prose_bullets_in_todos(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            check_skills.REPO_ROOT = repo
            write_registry(repo, "example")
            write_skill(
                repo,
                "example",
                VALID_SKILL.replace(
                    "   1. [ ] Default branch.",
                    "   - Default branch.",
                ),
            )

            errors = check_skills.template_structure_errors("0.1.0")

            self.assertTrue(any("unordered prose bullet" in error for error in errors))

    def test_template_structure_rejects_marker_comments_inside_fenced_examples(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            check_skills.REPO_ROOT = repo
            write_registry(repo, "example")
            write_skill(
                repo,
                "example",
                VALID_SKILL.replace(
                    "## Templates\n\n- Template.",
                    "## Templates\n\n```markdown\n"
                    "<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->\n"
                    "## Todo List\n"
                    "<!-- END FARPLANE_IMPORTANT_CHECKLIST -->\n"
                    "```",
                ),
            )

            errors = check_skills.template_structure_errors("0.1.0")

            self.assertTrue(any("fenced examples" in error for error in errors))

    def test_template_structure_rejects_missing_numbered_todos(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            check_skills.REPO_ROOT = repo
            write_registry(repo, "example")
            write_skill(
                repo,
                "example",
                VALID_SKILL.replace("1. [ ] Read context.", "[TODO: describe the work]")
                .replace("2. [ ] Choose the branch.", "[TODO: choose branch]")
                .replace("3. [ ] Review before completion.", "[TODO: review]"),
            )

            errors = check_skills.template_structure_errors("0.1.0")

            self.assertTrue(any("numbered task items" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
