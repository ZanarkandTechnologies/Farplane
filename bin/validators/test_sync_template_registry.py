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


def write_config(root: Path, *paths: str) -> Path:
    path = root / "config" / "template-registry.toml"
    path.parent.mkdir(parents=True)
    rendered_paths = ", ".join(f'"{item}"' for item in paths)
    path.write_text(f"[template_registry]\npaths = [{rendered_paths}]\n", encoding="utf-8")
    return path


class TemplateRegistryTests(unittest.TestCase):
    def test_builds_registry_from_yaml_frontmatter(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            template = root / "templates" / "prompt.md"
            template.parent.mkdir()
            template.write_text(
                textwrap.dedent(
                    """\
                    ---
                    template_id: prompt-template
                    template_version: "1.2.3"
                    consumer_scope: skill
                    applies_to:
                      - skills/*/SKILL.md
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
        self.assertEqual(rows[0]["consumer_scope"], "skill")
        self.assertEqual(rows[0]["applies_to"], ["skills/*/SKILL.md"])

    def test_builds_registry_from_html_comment_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            template = root / "templates" / "AGENTS.md"
            template.parent.mkdir()
            template.write_text(
                textwrap.dedent(
                    """\
                    <!--
                    template_id: global-agents-template
                    template_version: 0.2.2
                    -->
                    Body
                    """
                ),
                encoding="utf-8",
            )
            config = write_config(root, "templates/AGENTS.md")

            rows = sync_template_registry.build_registry(root, config)

        self.assertEqual(rows[0]["template_id"], "global-agents-template")

    def test_requires_template_version(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            template = root / "templates" / "prompt.md"
            template.parent.mkdir()
            template.write_text(
                "---\ntemplate_id: prompt\n---\n",
                encoding="utf-8",
            )
            config = write_config(root, "templates/prompt.md")

            with self.assertRaisesRegex(
                sync_template_registry.TemplateRegistryError, "missing template_version"
            ):
                sync_template_registry.build_registry(root, config)


if __name__ == "__main__":
    unittest.main()
