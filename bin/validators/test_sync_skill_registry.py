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
    if eval_surface:
        eval_path = skill_dir / eval_surface
        eval_path.parent.mkdir(parents=True, exist_ok=True)
        eval_path.write_text('{"skill_name":"' + name + '","evals":[]}\n', encoding="utf-8")


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
                eval_surface="evals/evals.json",
                qa_checklist="qa_checklist.md",
                skill_ui="skills/example/ui/index.html",
            )

            rows = sync_skill_registry.build_registry(repo)

            self.assertEqual(rows[0]["eval"], "evals/evals.json")
            self.assertEqual(rows[0]["qa_checklist"], "qa_checklist.md")
            self.assertEqual(rows[0]["skill_ui"], "skills/example/ui/index.html")

    def test_rejects_undeclared_canonical_eval_surface(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "example")
            eval_path = repo / "skills" / "example" / "evals" / "evals.json"
            eval_path.parent.mkdir(parents=True)
            eval_path.write_text('{"skill_name":"example","evals":[]}\n')

            with self.assertRaisesRegex(sync_skill_registry.RegistryError, "frontmatter must declare"):
                sync_skill_registry.build_registry(repo)

    def test_extracts_ordered_todo_skill_refs_without_manual_workflow_flag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "horizon-advisor")
            write_skill(repo, "goal-advisor")
            write_skill(repo, "eval")
            write_skill(repo, "plan")
            write_skill(
                repo,
                "weekly-workflow",
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

            self.assertEqual(row["todo_skill_refs"], ["horizon-advisor", "goal-advisor", "eval"])

    def test_workflow_frontmatter_is_retired(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "example")
            skill_path = repo / "skills" / "example" / "SKILL.md"
            skill_path.write_text(skill_path.read_text().replace("source: local", "source: local\nworkflow: true"))

            with self.assertRaisesRegex(sync_skill_registry.RegistryError, "retired frontmatter field"):
                sync_skill_registry.build_registry(repo)


if __name__ == "__main__":
    unittest.main()
