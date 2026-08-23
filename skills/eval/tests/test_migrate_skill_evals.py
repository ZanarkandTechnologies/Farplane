from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "migrate_skill_evals.py"
SPEC = importlib.util.spec_from_file_location("migrate_skill_evals", SCRIPT)
assert SPEC and SPEC.loader
migration = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(migration)


class MigrateSkillEvalsTests(unittest.TestCase):
    def test_convert_preserves_current_runner_fields_and_discards_retired_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "skills" / "qa" / "eval_task.json"
            path.parent.mkdir(parents=True)
            path.write_text(
                json.dumps(
                    [
                        {
                            "id": "proof_01",
                            "title": "Capture proof",
                            "query": "Check the UI.",
                            "reference_points": ["Captures evidence", "Returns a verdict"],
                            "context": "Toy context",
                            "tags": ["qa"],
                            "notes": "Representative row",
                            "hardcase": True,
                        }
                    ]
                )
            )

            converted = migration.convert_file(path)

            self.assertEqual(converted["skill_name"], "qa")
            row = converted["evals"][0]
            self.assertEqual(row["prompt"], "Check the UI.")
            self.assertEqual(row["expected_output"], "Captures evidence; Returns a verdict")
            self.assertEqual(row["assertions"], ["Captures evidence", "Returns a verdict"])
            self.assertEqual(row["files"], [])
            self.assertEqual(row["metadata"]["farplane"]["context"], "Toy context")
            self.assertNotIn("hardcase", row["metadata"]["farplane"])

    def test_dry_run_does_not_write_and_write_creates_standard_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "skills" / "qa" / "eval_task.json"
            source.parent.mkdir(parents=True)
            source.write_text(
                json.dumps(
                    [
                        {
                            "id": "proof_01",
                            "title": "Capture proof",
                            "query": "Check the UI.",
                            "reference_points": ["Captures evidence"],
                        }
                    ]
                )
            )
            destination = source.parent / "evals" / "evals.json"

            self.assertEqual(migration.main(["--root", str(root), "--skill", "qa"]), 0)
            self.assertFalse(destination.exists())
            self.assertEqual(migration.main(["--root", str(root), "--skill", "qa", "--write"]), 0)
            self.assertTrue(destination.exists())

    def test_bulk_write_preflights_all_files_before_mutating(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for skill in ("alpha", "beta"):
                source = root / "skills" / skill / "eval_task.json"
                source.parent.mkdir(parents=True)
                source.write_text(
                    json.dumps([{"id": "one", "query": "Do it.", "reference_points": ["Does it"]}])
                )
            blocked = root / "skills" / "beta" / "evals" / "evals.json"
            blocked.parent.mkdir(parents=True)
            blocked.write_text("{}")

            self.assertEqual(migration.main(["--root", str(root), "--write"]), 2)
            self.assertFalse((root / "skills" / "alpha" / "evals" / "evals.json").exists())

    def test_skill_selector_rejects_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(migration.main(["--root", tmp, "--skill", "../outside"]), 2)

    def test_remove_legacy_requires_write_and_removes_only_after_conversion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "skills" / "qa" / "eval_task.json"
            source.parent.mkdir(parents=True)
            source.write_text(
                json.dumps([{"id": "one", "query": "Do it.", "reference_points": ["Does it"]}])
            )

            self.assertEqual(migration.main(["--root", str(root), "--remove-legacy"]), 2)
            self.assertTrue(source.exists())
            self.assertEqual(
                migration.main(["--root", str(root), "--write", "--remove-legacy"]),
                0,
            )
            self.assertFalse(source.exists())
            self.assertTrue((source.parent / "evals" / "evals.json").exists())

    def test_convert_accepts_older_expected_behavior_field(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "skills" / "copywriting-advisor" / "eval_task.json"
            path.parent.mkdir(parents=True)
            path.write_text(
                json.dumps(
                    [
                        {
                            "id": "copy_01",
                            "query": "Write landing page copy.",
                            "reference_points": ["Routes correctly"],
                            "expected_behavior": ["Produces usable copy", "Avoids unsupported claims"],
                            "failure_modes": ["Returns only generic strategy"],
                        }
                    ]
                )
            )

            row = migration.convert_file(path)["evals"][0]

            self.assertEqual(row["assertions"], ["Routes correctly"])
            self.assertNotIn("metadata", row)


if __name__ == "__main__":
    unittest.main()
