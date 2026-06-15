from __future__ import annotations

import importlib.util
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "sync_template_registry",
    ROOT / "bin" / "validators" / "sync_template_registry.py",
)
assert SPEC and SPEC.loader
sync_template_registry = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = sync_template_registry
SPEC.loader.exec_module(sync_template_registry)


def write_feature_registry(root: Path) -> None:
    path = root / "docs" / "features" / "registry.jsonl"
    path.parent.mkdir(parents=True)
    path.write_text(
        '{"id":"FEAT-0001","name":"Test","status":"implemented","category":"test","surfaces":[],"source_refs":[],"external_refs":[],"evidence_refs":[],"known_limits":"","metrics":[],"last_verified":"2026-06-16"}\n',
        encoding="utf-8",
    )


def write_config(root: Path, *paths: str) -> Path:
    path = root / "rules" / "template-registry.toml"
    path.parent.mkdir(parents=True)
    rendered_paths = ", ".join(f'"{item}"' for item in paths)
    path.write_text(f"[template_registry]\npaths = [{rendered_paths}]\n", encoding="utf-8")
    return path


class TemplateRegistryTests(unittest.TestCase):
    def test_builds_registry_from_yaml_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_feature_registry(root)
            template = root / "templates" / "prompt.md"
            template.parent.mkdir()
            template.write_text(
                textwrap.dedent(
                    """\
                    ---
                    template_id: prompt-template
                    template_version: "1.2.3"
                    feature_refs:
                      - FEAT-0001
                    ---

                    Body
                    """
                ),
                encoding="utf-8",
            )
            config = write_config(root, "templates/prompt.md")

            rows = sync_template_registry.build_registry(root, config)

        self.assertEqual(rows[0]["template_id"], "prompt-template")
        self.assertEqual(rows[0]["template_version"], "1.2.3")
        self.assertEqual(rows[0]["feature_refs"], ["FEAT-0001"])

    def test_builds_registry_from_html_comment_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_feature_registry(root)
            template = root / "templates" / "AGENTS.md"
            template.parent.mkdir()
            template.write_text(
                textwrap.dedent(
                    """\
                    <!--
                    template_id: global-agents-template
                    template_version: 0.2.2
                    feature_refs:
                      - FEAT-0001
                    -->
                    Body
                    """
                ),
                encoding="utf-8",
            )
            config = write_config(root, "templates/AGENTS.md")

            rows = sync_template_registry.build_registry(root, config)

        self.assertEqual(rows[0]["template_id"], "global-agents-template")
        self.assertEqual(rows[0]["feature_refs"], ["FEAT-0001"])

    def test_rejects_unknown_feature_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_feature_registry(root)
            template = root / "templates" / "prompt.md"
            template.parent.mkdir()
            template.write_text(
                "---\ntemplate_id: prompt\ntemplate_version: 1.0.0\nfeature_refs:\n  - FEAT-MISSING\n---\n",
                encoding="utf-8",
            )
            config = write_config(root, "templates/prompt.md")

            with self.assertRaisesRegex(
                sync_template_registry.TemplateRegistryError, "unknown feature_refs"
            ):
                sync_template_registry.build_registry(root, config)

    def test_requires_feature_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_feature_registry(root)
            template = root / "templates" / "prompt.md"
            template.parent.mkdir()
            template.write_text(
                "---\ntemplate_id: prompt\ntemplate_version: 1.0.0\n---\n",
                encoding="utf-8",
            )
            config = write_config(root, "templates/prompt.md")

            with self.assertRaisesRegex(
                sync_template_registry.TemplateRegistryError, "feature_refs"
            ):
                sync_template_registry.build_registry(root, config)


if __name__ == "__main__":
    unittest.main()
