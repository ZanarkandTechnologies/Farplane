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
    tier: int = 2,
    group: str | None = None,
    template_version: str | None = None,
    feature_refs: list[str] | None = None,
    with_eval: bool = False,
    skill_ui: str | None = None,
    capability: str | None = None,
    common_chain_after: list[str] | None = None,
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
    common_chain_lines = ""
    if common_chain_after:
        common_chain_lines = f"common_chains:\n  after: {common_chain_after!r}\n"
    (skill_dir / "SKILL.md").write_text(
        "\n".join(
            [
                "---",
                f"name: {name}",
                "description: Test skill.",
                f"tier: {tier}",
                f"group: {group}" if group else "",
                "source: local",
                capability or "",
                common_chain_lines.rstrip(),
                template_line.rstrip(),
                feature_lines.rstrip(),
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
    if with_eval:
        eval_path = skill_dir / "evals" / "evals.json"
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

    def test_projects_derived_eval_and_declared_skill_ui_when_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(
                repo,
                "example",
                with_eval=True,
                skill_ui="skills/example/ui/index.html",
            )

            rows = sync_skill_registry.build_registry(repo)

            self.assertEqual(rows[0]["eval"], "evals/evals.json")
            self.assertEqual(rows[0]["skill_ui"], "skills/example/ui/index.html")

    def test_projects_canonical_eval_without_frontmatter_declaration(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "example")
            eval_path = repo / "skills" / "example" / "evals" / "evals.json"
            eval_path.parent.mkdir(parents=True)
            eval_path.write_text('{"skill_name":"example","evals":[]}\n')

            rows = sync_skill_registry.build_registry(repo)

            self.assertEqual(rows[0]["eval"], "evals/evals.json")

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

    def test_rejects_retired_portfolio_and_profiles(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "example")
            path = repo / "skills" / "example" / "SKILL.md"
            path.write_text(
                path.read_text().replace(
                    "source: local", "source: local\nportfolio: domain\nprofiles: [content-specialist]"
                )
            )

            with self.assertRaisesRegex(sync_skill_registry.RegistryError, "Extra inputs"):
                sync_skill_registry.build_registry(repo)

    def test_projects_an_artifact_capability_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "thread-writer")
            path = repo / "skills" / "thread-writer" / "SKILL.md"
            path.write_text(
                path.read_text().replace(
                    "source: local",
                    """source: local
capability:
  kind: artifact
  consumes:
    - content-brief
  produces:
    - x-thread-draft""",
                )
            )

            rows = sync_skill_registry.build_registry(repo)

            self.assertEqual(
                rows[0]["capability"],
                {
                    "kind": "artifact",
                    "consumes": ["content-brief"],
                    "produces": ["x-thread-draft"],
                },
            )

    def test_rejects_invalid_capability_contracts(self) -> None:
        cases = (
            (
                """capability:
  kind: artifact
  produces:
    - thread-draft
    - carousel-draft""",
                "at most 1 item",
            ),
            (
                """capability:
  kind: artifact
  produces:
    - thread-draft
  consumes:
    - thread-draft""",
                "must not consume",
            ),
            (
                """capability:
  kind: unknown""",
                "does not match any of the expected tags",
            ),
        )
        for capability, message in cases:
            with self.subTest(capability=capability), tempfile.TemporaryDirectory() as tmp:
                repo = Path(tmp)
                write_skill(repo, "example")
                path = repo / "skills" / "example" / "SKILL.md"
                path.write_text(
                    path.read_text().replace("source: local", f"source: local\n{capability}")
                )

                with self.assertRaisesRegex(sync_skill_registry.RegistryError, message):
                    sync_skill_registry.build_registry(repo)

    def test_rejects_a_redundant_integration_system_field(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "example")
            path = repo / "skills" / "example" / "SKILL.md"
            path.write_text(
                path.read_text().replace(
                    "source: local",
                    """source: local
capability:
  kind: integration
  system: x""",
                )
            )

            with self.assertRaisesRegex(sync_skill_registry.RegistryError, "Extra inputs"):
                sync_skill_registry.build_registry(repo)

    def test_projects_integration_without_portfolio(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "example")
            path = repo / "skills" / "example" / "SKILL.md"
            path.write_text(
                path.read_text().replace(
                    "source: local",
                    """source: local
capability:
  kind: integration
  consumes:
    - thread-draft""",
                )
            )

            rows = sync_skill_registry.build_registry(repo)
            self.assertEqual(rows[0]["capability"]["kind"], "integration")

    def test_rejects_duplicate_frontmatter_keys_in_nested_mappings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "example")
            path = repo / "skills" / "example" / "SKILL.md"
            path.write_text(
                path.read_text().replace(
                    "source: local",
                    """source: local
capability:
  kind: artifact
  kind: integration
  system: x""",
                )
            )

            with self.assertRaisesRegex(
                sync_skill_registry.RegistryError,
                "duplicate frontmatter keys: kind",
            ):
                sync_skill_registry.build_registry(repo)

    def test_rejects_todo_references_to_shortcuts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "unslop", capability="capability:\n  kind: shortcut")
            write_skill(
                repo,
                "writer",
                todo_lines=["- [ ] Rewrite the draft with `unslop`."],
            )

            with self.assertRaisesRegex(
                sync_skill_registry.RegistryError,
                "target explicit-only shortcut skill.*todo_skill_refs=unslop",
            ):
                sync_skill_registry.build_registry(repo)

    def test_rejects_skill_links_targeting_shortcuts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "unslop", capability="capability:\n  kind: shortcut")
            write_skill(repo, "writer")
            path = repo / "skills" / "writer" / "SKILL.md"
            path.write_text(path.read_text() + "\n[Unslop](../unslop/SKILL.md)\n")

            with self.assertRaisesRegex(
                sync_skill_registry.RegistryError,
                "target explicit-only shortcut skill.*skill_links=unslop",
            ):
                sync_skill_registry.build_registry(repo)

    def test_rejects_common_chains_targeting_shortcuts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "unslop", capability="capability:\n  kind: shortcut")
            write_skill(
                repo,
                "writer",
                tier=3,
                group="operations",
                common_chain_after=["unslop"],
            )

            with self.assertRaisesRegex(
                sync_skill_registry.RegistryError,
                "target explicit-only shortcut skill.*common_chains=unslop",
            ):
                sync_skill_registry.build_registry(repo)

    def test_rejects_outbound_shortcut_todo_references(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "writer")
            write_skill(
                repo,
                "unslop",
                capability="capability:\n  kind: shortcut",
                todo_lines=["- [ ] Hand off to `writer`."],
            )

            with self.assertRaisesRegex(
                sync_skill_registry.RegistryError,
                "explicit-only shortcut must be a composition leaf.*todo_skill_refs=writer",
            ):
                sync_skill_registry.build_registry(repo)

    def test_rejects_outbound_shortcut_skill_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "writer")
            write_skill(repo, "unslop", capability="capability:\n  kind: shortcut")
            path = repo / "skills" / "unslop" / "SKILL.md"
            path.write_text(path.read_text() + "\n[Writer](../writer/SKILL.md)\n")

            with self.assertRaisesRegex(
                sync_skill_registry.RegistryError,
                "explicit-only shortcut must be a composition leaf.*skill_links=writer",
            ):
                sync_skill_registry.build_registry(repo)

    def test_rejects_outbound_shortcut_common_chains(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            write_skill(repo, "writer")
            write_skill(
                repo,
                "unslop",
                tier=3,
                group="operations",
                capability="capability:\n  kind: shortcut",
                common_chain_after=["writer"],
            )

            with self.assertRaisesRegex(
                sync_skill_registry.RegistryError,
                "explicit-only shortcut must be a composition leaf.*common_chains=writer",
            ):
                sync_skill_registry.build_registry(repo)


if __name__ == "__main__":
    unittest.main()
