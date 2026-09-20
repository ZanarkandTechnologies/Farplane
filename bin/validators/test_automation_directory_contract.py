from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from bin.validators.check_farplane_project_files import validate, validate_automations_dir
from bin.validators.test_check_farplane_project_files import write_required_project_files


class AutomationDirectoryContractTests(unittest.TestCase):
    def test_rejects_legacy_monolith_beside_folder(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            write_required_project_files(root)
            (root / "farplane" / "automations.toml").write_text("schema = 'legacy'\n")
            errors = validate(root)

        self.assertIn(
            "farplane/automations.toml is retired; use one file per automation in farplane/automations/.",
            errors,
        )

    def test_rejects_index_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "farplane" / "automations"
            folder.mkdir(parents=True)
            (folder / "index.md").write_text("---\nschema: farplane_project_automation\n---\nprompt\n")
            errors = validate_automations_dir(root, folder)

        self.assertIn(
            "farplane/automations/index.md is forbidden; each Markdown file must be one automation.",
            errors,
        )

    def test_rejects_toml_file_beside_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "farplane" / "automations"
            folder.mkdir(parents=True)
            (folder / "pulse.md").write_text("---\nid: pulse\n---\nprompt\n")
            (folder / "old.toml").write_text("id = 'old'\n")

            errors = validate_automations_dir(root, folder)

        self.assertIn(
            "farplane/automations/old.toml is retired; use one Markdown file per automation.",
            errors,
        )

    def test_rejects_duplicate_front_matter_keys(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "farplane" / "automations"
            folder.mkdir(parents=True)
            (folder / "pulse.md").write_text(
                "---\nid: pulse\nstatus: paused\nstatus: active\n---\nUse $pulse-update.\n",
                encoding="utf-8",
            )

            errors = validate_automations_dir(root, folder)

        self.assertTrue(
            any("duplicate frontmatter keys: status" in error for error in errors),
            errors,
        )


if __name__ == "__main__":
    unittest.main()
