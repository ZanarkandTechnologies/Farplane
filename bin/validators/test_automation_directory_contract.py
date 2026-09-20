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
            (folder / "index.toml").write_text("schema = 'farplane_project_automation'\n")
            errors = validate_automations_dir(root, folder)

        self.assertIn(
            "farplane/automations/index.toml is forbidden; each TOML file must be one automation.",
            errors,
        )


if __name__ == "__main__":
    unittest.main()
