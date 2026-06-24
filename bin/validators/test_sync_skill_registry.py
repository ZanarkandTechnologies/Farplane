#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "sync_skill_registry",
    ROOT / "bin" / "validators" / "sync_skill_registry.py",
)
assert SPEC and SPEC.loader
sync_skill_registry = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sync_skill_registry)


def write_skill(
    repo: Path,
    name: str,
    *,
    template_version: str | None = None,
    feature_refs: list[str] | None = None,
    eval_surface: str | None = None,
    qa_checklist: str | None = None,
    skill_ui: str | None = None,
    workflow: bool = False,
    todo_lines: list[str] | None = None,
) -> None:
    skill_dir = repo / "skills" / name
    skill_dir.mkdir(parents=True)
    template_line = (
        f"skill_template_version: {template_version}\n"
        if template_version is not None
        else ""
    )
    feature_lines = ""
    if feature_refs:
        feature_lines = "feature_refs:\n" + "".join(
            f"  - {feature_ref}\n" for feature_ref in feature_refs
        )
    (skill_dir / "SKILL.md").write_text(
        "\n".join(
            [
                "---",
                f"name: {name}",
                "description: Test skill.",
                "tier: 2",
                "source: local",
                "workflow: true" if workflow else "",
                template_line.rstrip(),
                feature_lines.rstrip(),
                f"eval: {eval_surface}" if eval_surface else "",
                f"qa_checklist: {qa_checklist}" if qa_checklist else "",
                f"skill_ui: {skill_ui}" if skill_ui else "",
                "---",
                "",
                f"# {name}",
                "",
                "<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->",
                "## Todo List",
                "",
                "\n".join(todo_lines or ["- [ ] Test."]),
                "<!-- END FARPLANE_IMPORTANT_CHECKLIST -->",
                "",
            ]
        )
        .replace("\n\n---", "\n---")
        .replace("\n\n\n---", "\n---"),
        encoding="utf-8",
    )


class SyncSkillRegistryTests(unittest.TestCase):
    def test_copies_skill_template_version_when_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "example", template_version="0.1.0")

            rows = sync_skill_registry.build_registry(repo)

            self.assertEqual(rows[0]["skill_template_version"], "0.1.0")

    def test_omits_skill_template_version_when_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "example")

            rows = sync_skill_registry.build_registry(repo)

            self.assertNotIn("skill_template_version", rows[0])

    def test_rejects_skill_level_feature_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "example", feature_refs=["FEAT-0001"])

            with self.assertRaisesRegex(sync_skill_registry.RegistryError, "template metadata"):
                sync_skill_registry.build_registry(repo)

    def test_copies_skill_surface_fields_when_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(
                repo,
                "example",
                eval_surface="eval_task.json",
                qa_checklist="qa_checklist.md",
                skill_ui="skills/example/ui/index.html",
            )

            rows = sync_skill_registry.build_registry(repo)

            self.assertEqual(rows[0]["eval"], "eval_task.json")
            self.assertEqual(rows[0]["qa_checklist"], "qa_checklist.md")
            self.assertEqual(rows[0]["skill_ui"], "skills/example/ui/index.html")

    def test_workflow_true_extracts_ordered_todo_skill_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "horizon-advisor")
            write_skill(repo, "goal-advisor")
            write_skill(repo, "eval")
            write_skill(repo, "plan")
            write_skill(
                repo,
                "weekly-workflow",
                workflow=True,
                todo_lines=[
                    "- [ ] 1. Load [horizon](../horizon-advisor/SKILL.md).",
                    "- [ ] 2. Call `goal-advisor` after goals are ready.",
                    "- [ ] 3. Mention `horizon-advisor` again without duplicating it.",
                    "- [ ] 4. Keep Reference Map prose out of this test; use `eval` last.",
                    "- [ ] 5. Plain prose can say plan without becoming a skill edge.",
                ],
            )

            rows = sync_skill_registry.build_registry(repo)
            row = next(row for row in rows if row["name"] == "weekly-workflow")

            self.assertTrue(row["workflow"])
            self.assertEqual(row["workflow_refs"], ["horizon-advisor", "goal-advisor", "eval"])

    def test_workflow_field_must_be_boolean_true(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "example")
            skill_path = repo / "skills" / "example" / "SKILL.md"
            skill_path.write_text(skill_path.read_text().replace("source: local", "source: local\nworkflow: yes"))

            with self.assertRaisesRegex(sync_skill_registry.RegistryError, "workflow must be true"):
                sync_skill_registry.build_registry(repo)


if __name__ == "__main__":
    unittest.main()
