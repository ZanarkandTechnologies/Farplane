from __future__ import annotations

import subprocess
import tempfile
import textwrap
import unittest
import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "check_template_version_metadata",
    ROOT / "bin" / "validators" / "check_template_version_metadata.py",
)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


class TemplateVersionMetadataTests(unittest.TestCase):
    def test_watch_config_controls_template_paths(self) -> None:
        config = validator.WatchConfig(
            paths=frozenset({"skills/skill-creator/references/SKILL_TEMPLATE.md"}),
            globs=("tickets/templates/*", "tickets/templates/**/*"),
            exclude_globs=("tickets/templates/archive/*", "tickets/templates/archive/**/*"),
            source=Path("rules/template-version-watch.toml"),
        )

        self.assertTrue(
            validator.is_watched_path(
                "skills/skill-creator/references/SKILL_TEMPLATE.md",
                config,
            )
        )
        self.assertTrue(validator.is_watched_path("tickets/templates/ticket.md", config))
        self.assertFalse(validator.is_watched_path("prompt.md.tpl", config))
        self.assertFalse(
            validator.is_watched_path("tickets/templates/archive/old.md", config)
        )

    def test_loads_watch_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / "template-version-watch.toml"
            config_path.write_text(
                textwrap.dedent(
                    """\
                    [template_version_watch]
                    paths = ["skills/skill-creator/references/SKILL_TEMPLATE.md"]
                    globs = ["templates/**/*.md"]
                    exclude_globs = ["templates/archive/**/*"]
                    """
                ),
                encoding="utf-8",
            )

            config = validator.load_watch_config(config_path)

        self.assertIn("skills/skill-creator/references/SKILL_TEMPLATE.md", config.paths)
        self.assertEqual(config.globs, ("templates/**/*.md",))
        self.assertEqual(config.exclude_globs, ("templates/archive/**/*",))

    def test_extracts_yaml_frontmatter_metadata(self) -> None:
        metadata = validator.extract_metadata(
            textwrap.dedent(
                """\
                ---
                template_id: sample-prompt
                template_version: 1.2.3
                ---

                Body
                """
            )
        )

        self.assertIsNotNone(metadata)
        assert metadata is not None
        self.assertEqual(metadata.template_id, "sample-prompt")
        self.assertEqual(metadata.version, "1.2.3")

    def test_staged_template_change_requires_version_bump(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._git(root, "init")
            self._git(root, "config", "user.email", "test@example.com")
            self._git(root, "config", "user.name", "Test User")
            path = root / "templates" / "prompt.md"
            path.parent.mkdir()
            path.write_text(
                "---\ntemplate_id: prompt\ntemplate_version: 1.0.0\n---\n\nOld\n",
                encoding="utf-8",
            )
            self._write_config(root, "templates/prompt.md")
            self._git(root, "add", ".")
            self._git(root, "commit", "-m", "initial")

            path.write_text(
                "---\ntemplate_id: prompt\ntemplate_version: 1.0.0\n---\n\nNew\n",
                encoding="utf-8",
            )
            self._git(root, "add", ".")

            config = validator.load_watch_config(root / "rules" / "template-version-watch.toml")
            errors = validator.validate_staged(root, config)
            self.assertTrue(any("template_version stayed" in error for error in errors))

    def test_staged_template_change_passes_with_version_bump(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._git(root, "init")
            self._git(root, "config", "user.email", "test@example.com")
            self._git(root, "config", "user.name", "Test User")
            path = root / "templates" / "prompt.md"
            path.parent.mkdir()
            path.write_text(
                "---\ntemplate_id: prompt\ntemplate_version: 1.0.0\n---\n\nOld\n",
                encoding="utf-8",
            )
            self._write_config(root, "templates/prompt.md")
            self._git(root, "add", ".")
            self._git(root, "commit", "-m", "initial")

            path.write_text(
                "---\ntemplate_id: prompt\ntemplate_version: 1.1.0\n---\n\nNew\n",
                encoding="utf-8",
            )
            self._git(root, "add", ".")

            config = validator.load_watch_config(root / "rules" / "template-version-watch.toml")
            self.assertEqual(validator.validate_staged(root, config), [])

    def test_unwatched_template_like_file_is_ignored(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._git(root, "init")
            self._git(root, "config", "user.email", "test@example.com")
            self._git(root, "config", "user.name", "Test User")
            path = root / "prompt.md.tpl"
            path.write_text("No metadata\n", encoding="utf-8")
            self._write_config(root, "templates/only-this.md")
            self._git(root, "add", ".")

            config = validator.load_watch_config(root / "rules" / "template-version-watch.toml")
            self.assertEqual(validator.validate_staged(root, config), [])

    @staticmethod
    def _git(root: Path, *args: str) -> None:
        subprocess.run(
            ["git", *args],
            cwd=root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    @staticmethod
    def _write_config(root: Path, *paths: str) -> None:
        config = root / "rules" / "template-version-watch.toml"
        config.parent.mkdir()
        rendered_paths = ", ".join(f'"{path}"' for path in paths)
        config.write_text(
            f"[template_version_watch]\npaths = [{rendered_paths}]\nglobs = []\nexclude_globs = []\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    unittest.main()
