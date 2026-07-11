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

        self.assertIn("farplane/goals.yaml KPI ids lack metrics.yaml definitions: unknown_metric.", errors)

    def test_goal_kpi_metric_recipe_does_not_require_product_owner(self) -> None:
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
      - id: project_kpi
        kpis:
          - id: accepted_harness_improvements
            target: 20
            direction: above
""",
                encoding="utf-8",
            )
            (farplane / "metrics.yaml").write_text(
                """kind: project-metrics
framework_template_version: "0.1.0"
metrics:
  accepted_harness_improvements:
    label: Accepted harness improvements
    description: Accepted improvements with ticket proof.
    kind: daily_count
    unit: improvements
    display: bar_plus_cumulative
""",
                encoding="utf-8",
            )
            (farplane / "bindings.yaml").write_text(
                """kind: project-bindings
framework_template_version: "0.1.0"
project: {}
metric_bindings:
  accepted_harness_improvements:
    refresh: Count ticket Reward rows.
""",
                encoding="utf-8",
            )

            errors = validate(root)

        self.assertEqual(errors, [])

    def test_metric_recipe_requires_description_and_valid_types(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            write_framework_manifest(farplane)
            write_required_project_files(root)
            (farplane / "metrics.yaml").write_text(
                """kind: project-metrics
framework_template_version: "0.1.0"
metrics:
  accepted_harness_improvements:
    label: Accepted harness improvements
    kind: weekly_magic
    unit: improvements
    display: sparkles
    pinned: "true"
""",
                encoding="utf-8",
            )
            (farplane / "bindings.yaml").write_text(
                """kind: project-bindings
framework_template_version: "0.1.0"
project: {}
metric_bindings:
  accepted_harness_improvements:
    refresh: Count tickets.
""",
                encoding="utf-8",
            )

            errors = validate(root)

        self.assertIn(
            "farplane/metrics.yaml metrics.accepted_harness_improvements.description must be a non-empty string.",
            errors,
        )
        self.assertIn(
            "farplane/metrics.yaml metrics.accepted_harness_improvements.kind must be one of: daily, daily_count, point.",
            errors,
        )
        self.assertIn(
            "farplane/metrics.yaml metrics.accepted_harness_improvements.display must be one of: bar_plus_cumulative, line, reading.",
            errors,
        )
        self.assertIn(
            "farplane/metrics.yaml metrics.accepted_harness_improvements.pinned must be boolean when present.",
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
          - id: todo_unclaimed_ticket_count
            direction: below
""",
                encoding="utf-8",
            )
            (farplane / "metrics.yaml").write_text(
                """kind: project-metrics
framework_template_version: "0.1.0"
metrics:
  accepted_harness_improvements:
    label: Accepted harness improvements
    description: Accepted improvements.
    kind: daily_count
    unit: improvements
    display: bar_plus_cumulative
  todo_unclaimed_ticket_count:
    label: Ready unclaimed tickets
    description: Ready unclaimed tickets.
    kind: point
    unit: tickets
    display: reading
""",
                encoding="utf-8",
            )
            (farplane / "bindings.yaml").write_text(
                """kind: project-bindings
framework_template_version: "0.1.0"
project: {}
metric_bindings:
  accepted_harness_improvements:
    refresh: Count accepted improvements.
  todo_unclaimed_ticket_count:
    refresh: Count ready unclaimed tickets.
""",
                encoding="utf-8",
            )

            errors = validate(root)

        self.assertIn("farplane/goals.yaml KPI ids need explicit target values: todo_unclaimed_ticket_count.", errors)
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
            (farplane / "metrics.yaml").write_text(
                """kind: project-metrics
framework_template_version: "0.1.0"
metrics:
  accepted_harness_improvements:
    label: Accepted harness improvements
    description: Accepted improvements.
    kind: daily_count
    display: bar_plus_cumulative
""",
                encoding="utf-8",
            )
            (farplane / "bindings.yaml").write_text(
                """kind: project-bindings
framework_template_version: "0.1.0"
project: {}
metric_bindings:
  accepted_harness_improvements:
    refresh: Count accepted improvements.
""",
                encoding="utf-8",
            )

            errors = validate(root)

        self.assertIn(
            "farplane/goals.yaml KPI ids have metrics.yaml definitions without unit: accepted_harness_improvements.",
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
