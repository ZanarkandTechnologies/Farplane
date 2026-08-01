import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

import yaml

SCRIPT = Path(__file__).parents[1] / "scripts" / "migrate_framework.py"
SPEC = importlib.util.spec_from_file_location("migrate_framework", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class MigrateFrameworkTest(unittest.TestCase):
    def _write_base_project(self, root: Path) -> None:
        (root / "farplane").mkdir()
        (root / "farplane" / "manifest.json").write_text(
            json.dumps(
                {
                    "spec_version": "2.0.9",
                    "template_uses": {"farplane-framework": "2.0.9"},
                    "project": {"name": "Keep me"},
                }
            ),
            encoding="utf-8",
        )

    def test_force_migrates_only_versions_and_metric_type(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._write_base_project(root)
            (root / "farplane" / "metrics.yaml").write_text(
                """kind: project-metrics
updated_at: 2026-01-01
framework_template_version: "0.3.0"
metrics:
  revenue:
    description: Keep this human definition.
    kind: daily_count
    unit: usd
    direction: maximize
""",
                encoding="utf-8",
            )

            result = MODULE.migrate_project(root, force=True)

            manifest = json.loads((root / "farplane" / "manifest.json").read_text())
            metrics = (root / "farplane" / "metrics.yaml").read_text()
            self.assertEqual(result["mode"], "applied")
            self.assertEqual(manifest["project"]["name"], "Keep me")
            self.assertEqual(manifest["spec_version"], "2.0.14")
            self.assertEqual(
                manifest["template_uses"]["farplane-framework"],
                "2.0.14",
            )
            self.assertEqual(
                manifest["_template_metadata"]["template_version"],
                "2.0.14",
            )
            self.assertIn("type: flow", metrics)
            self.assertIn("Keep this human definition.", metrics)
            self.assertNotIn("kind: daily_count", metrics)

    def test_removed_projection_fields_fail_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "farplane").mkdir()
            manifest = '{"spec_version":"2.0.11","template_uses":{"farplane-framework":"2.0.11"}}\n'
            metrics = """kind: project-metrics
updated_at: 2026-01-01
framework_template_version: "0.3.0"
metrics:
  revenue:
    type: flow
    aggregation: sum
"""
            (root / "farplane" / "manifest.json").write_text(manifest)
            (root / "farplane" / "metrics.yaml").write_text(metrics)

            with self.assertRaisesRegex(ValueError, "removed projection fields"):
                MODULE.migrate_project(root, force=True)

            self.assertEqual((root / "farplane" / "manifest.json").read_text(), manifest)
            self.assertEqual((root / "farplane" / "metrics.yaml").read_text(), metrics)

    def test_force_moves_products_and_removes_retired_bindings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._write_base_project(root)
            (root / "farplane" / "metrics.yaml").write_text(
                """kind: project-metrics
updated_at: 2026-01-01
framework_template_version: "0.3.0"
metrics:
  output:
    refresh: Read accepted output evidence.
    type: flow
""",
                encoding="utf-8",
            )
            (root / "farplane" / "harness.yaml").write_text(
                """kind: project-harness
updated_at: 2026-01-01
framework_template_version: "0.4.0"
identity:
  mission: Keep the mission.
products:
  accepted_output:
    description: Produce accepted output.
    output: One reviewed artifact.
    skill_refs: [review]
    metric_refs:
      - metric_id: output
goals: []
""",
                encoding="utf-8",
            )
            (root / "farplane" / "bindings.yaml").write_text(
                """kind: project-bindings
project: {id: sample}
metric_bindings: {}
""",
                encoding="utf-8",
            )

            MODULE.migrate_project(root, force=True)

            harness = yaml.safe_load((root / "farplane" / "harness.yaml").read_text())
            bindings = yaml.safe_load((root / "farplane" / "bindings.yaml").read_text())
            self.assertNotIn("products", harness)
            self.assertNotIn("goals", harness)
            self.assertEqual(harness["identity"]["mission"], "Keep the mission.")
            self.assertIn("accepted_output", harness["areas"])
            self.assertEqual(harness["planning"]["skill_refs"], ["review"])
            self.assertNotIn("metric_bindings", bindings)
            self.assertEqual(bindings["framework_template_version"], "0.5.0")


if __name__ == "__main__":
    unittest.main()
