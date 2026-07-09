from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from bin.validators.check_farplane_project_files import validate
from bin.validators.test_check_farplane_project_files import write_framework_manifest, write_required_project_files


class FarplaneProjectFileValidatorTests(unittest.TestCase):
    def test_goal_kpi_without_metric_recipe_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            write_framework_manifest(farplane)
            write_required_project_files(root)
            (farplane / "goals.yaml").write_text(
                """kind: project-goals
framework_template_version: "0.1.0"
goals:
  test_axis:
    smart_goals:
      - id: missing_recipe
        kpis:
          - id: unknown_metric
""",
                encoding="utf-8",
            )

            errors = validate(root)

        self.assertIn("farplane/goals.yaml KPI ids lack bindings.yaml metric recipes: unknown_metric.", errors)

    def test_metric_product_without_product_row_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            write_framework_manifest(farplane)
            write_required_project_files(root)
            (farplane / "bindings.yaml").write_text(
                """kind: project-bindings
framework_template_version: "0.1.0"
project: {}
metrics:
  accepted_harness_improvements:
    product: missing_product
""",
                encoding="utf-8",
            )

            errors = validate(root)

        self.assertIn("farplane/bindings.yaml metric products are not in product registry: missing_product.", errors)

    def test_goal_kpi_metric_recipe_without_product_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            write_framework_manifest(farplane)
            write_required_project_files(root)
            (farplane / "goals.yaml").write_text(
                """kind: project-goals
framework_template_version: "0.1.0"
goals:
  test_axis:
    smart_goals:
      - id: productless_kpi
        kpis:
          - id: accepted_harness_improvements
""",
                encoding="utf-8",
            )
            (farplane / "bindings.yaml").write_text(
                """kind: project-bindings
framework_template_version: "0.1.0"
project: {}
metrics:
  accepted_harness_improvements:
    label: Accepted harness improvements
""",
                encoding="utf-8",
            )

            errors = validate(root)

        self.assertIn(
            "farplane/goals.yaml KPI ids have bindings.yaml metric recipes without product: accepted_harness_improvements.",
            errors,
        )

    def test_metric_recipe_requires_description_and_valid_types(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            write_framework_manifest(farplane)
            write_required_project_files(root)
            (farplane / "bindings.yaml").write_text(
                """kind: project-bindings
framework_template_version: "0.1.0"
project: {}
metrics:
  accepted_harness_improvements:
    label: Accepted harness improvements
    product: test
    kind: weekly_magic
    unit: improvements
    display: sparkles
    pinned: "true"
    refresh: Count tickets.
""",
                encoding="utf-8",
            )

            errors = validate(root)

        self.assertIn(
            "farplane/bindings.yaml metrics.accepted_harness_improvements.description must be a non-empty string.",
            errors,
        )
        self.assertIn(
            "farplane/bindings.yaml metrics.accepted_harness_improvements.kind must be one of: daily, daily_count, point.",
            errors,
        )
        self.assertIn(
            "farplane/bindings.yaml metrics.accepted_harness_improvements.display must be one of: bar_plus_cumulative, line, reading.",
            errors,
        )
        self.assertIn(
            "farplane/bindings.yaml metrics.accepted_harness_improvements.pinned must be boolean when present.",
            errors,
        )

    def test_goal_kpi_without_complete_target_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            write_framework_manifest(farplane)
            write_required_project_files(root)
            (farplane / "goals.yaml").write_text(
                """kind: project-goals
framework_template_version: "0.1.0"
goals:
  test_axis:
    smart_goals:
      - id: partial_target
        kpis:
          - id: accepted_harness_improvements
            target: 20
          - id: ready_unclaimed_ticket_count
            direction: below
""",
                encoding="utf-8",
            )
            (farplane / "bindings.yaml").write_text(
                """kind: project-bindings
framework_template_version: "0.1.0"
project: {}
metrics:
  accepted_harness_improvements:
    product: test
    unit: improvements
  ready_unclaimed_ticket_count:
    product: test
    unit: tickets
""",
                encoding="utf-8",
            )

            errors = validate(root)

        self.assertIn("farplane/goals.yaml KPI ids need explicit target values: ready_unclaimed_ticket_count.", errors)
        self.assertIn("farplane/goals.yaml KPI ids need explicit target directions: accepted_harness_improvements.", errors)

    def test_goal_kpi_metric_recipe_without_unit_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            write_framework_manifest(farplane)
            write_required_project_files(root)
            (farplane / "goals.yaml").write_text(
                """kind: project-goals
framework_template_version: "0.1.0"
goals:
  test_axis:
    smart_goals:
      - id: missing_unit
        kpis:
          - id: accepted_harness_improvements
            target: 20
            direction: above
""",
                encoding="utf-8",
            )
            (farplane / "bindings.yaml").write_text(
                """kind: project-bindings
framework_template_version: "0.1.0"
project: {}
metrics:
  accepted_harness_improvements:
    product: test
""",
                encoding="utf-8",
            )

            errors = validate(root)

        self.assertIn(
            "farplane/goals.yaml KPI ids have bindings.yaml metric recipes without unit: accepted_harness_improvements.",
            errors,
        )

    def test_stale_project_snapshot_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            write_framework_manifest(farplane)
            write_required_project_files(root)
            snapshot = root / ".farplane" / "project" / "ui" / "latest.json"
            snapshot.write_text(
                json.dumps({"sources": [{"path": "farplane/goals.yaml", "hash": "sha256:not-current"}]}),
                encoding="utf-8",
            )

            errors = validate(root)

        self.assertIn(".farplane/project/ui/latest.json is stale for farplane/goals.yaml; regenerate project snapshot.", errors)


if __name__ == "__main__":
    unittest.main()
