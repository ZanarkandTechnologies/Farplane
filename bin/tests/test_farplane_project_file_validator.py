from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import yaml

from bin.validators.check_farplane_project_files import validate
from bin.validators.test_check_farplane_project_files import write_framework_manifest, write_required_project_files


def select_project_objective(farplane: Path, metric_id: str, *, guards: list[str] | None = None) -> None:
    harness_path = farplane / "harness.yaml"
    harness = yaml.safe_load(harness_path.read_text(encoding="utf-8"))
    harness["metric_refs"] = {
        "objectives": [{"metric_id": metric_id, "priority": 1}],
        "guards": guards or [],
    }
    harness_path.write_text(yaml.safe_dump(harness, sort_keys=False), encoding="utf-8")


class FarplaneProjectFileValidatorTests(unittest.TestCase):
    def test_optional_goals_bind_selected_objectives_without_mutable_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            write_framework_manifest(farplane)
            write_required_project_files(root)
            harness_path = farplane / "harness.yaml"
            harness = yaml.safe_load(harness_path.read_text(encoding="utf-8"))
            harness["goals"] = [
                {
                    "goal_id": "accepted-output-target",
                    "metric_id": "accepted_output_events",
                    "target_value": 10,
                    "target_date": "2026-08-01",
                }
            ]
            harness_path.write_text(yaml.safe_dump(harness, sort_keys=False), encoding="utf-8")

            errors = validate(root)

        self.assertFalse(any("goals" in error or "goal ID" in error for error in errors), errors)

    def test_goals_reject_invalid_rows_and_nonobjective_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            write_framework_manifest(farplane)
            write_required_project_files(root)
            harness_path = farplane / "harness.yaml"
            harness = yaml.safe_load(harness_path.read_text(encoding="utf-8"))
            harness["goals"] = [
                {
                    "goal_id": "duplicate",
                    "metric_id": "accepted_product_output",
                    "target_value": True,
                    "target_date": "August",
                    "status": "completed",
                },
                {
                    "goal_id": "duplicate",
                    "metric_id": "unknown",
                    "target_value": float("inf"),
                    "target_date": "2026-08-01T12:00:00Z",
                },
            ]
            harness_path.write_text(yaml.safe_dump(harness, sort_keys=False), encoding="utf-8")

            errors = validate(root)

        joined = "\n".join(errors)
        self.assertIn("goals[0] has unsupported fields: status", joined)
        self.assertIn("goals[0].metric_id must reference a selected objective metric", joined)
        self.assertIn("goals[0].target_value must be a finite number", joined)
        self.assertIn("goals[0].target_date must be an ISO date", joined)
        self.assertIn("goals[1].metric_id must reference a selected objective metric", joined)
        self.assertIn("goal IDs must be unique: duplicate", joined)

    def test_planning_area_requires_canonical_instruction_and_rejects_typo(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            write_framework_manifest(farplane)
            write_required_project_files(root)
            harness_path = farplane / "harness.yaml"
            harness = yaml.safe_load(harness_path.read_text(encoding="utf-8"))
            instruction = harness["areas"]["test_output"].pop("planner_instruction")
            harness["areas"]["test_output"]["planner_instrcuitions"] = instruction
            harness_path.write_text(yaml.safe_dump(harness, sort_keys=False), encoding="utf-8")

            errors = validate(root)

        self.assertIn(
            "farplane/harness.yaml areas.test_output has controller or unsupported fields: planner_instrcuitions.",
            errors,
        )
        self.assertIn(
            "farplane/harness.yaml areas.test_output.planner_instruction must be a non-empty string.",
            errors,
        )

    def test_active_planning_area_requires_structured_icp(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            write_framework_manifest(farplane)
            write_required_project_files(root)
            harness_path = farplane / "harness.yaml"
            harness = yaml.safe_load(harness_path.read_text(encoding="utf-8"))
            harness["status"] = "active"
            harness["areas"]["test_output"]["icp"] = {
                "label": "Test builders",
                "description": "Builders deciding whether a test artifact is credible.",
                "jobs_to_be_done": ["Compare the artifact with a named baseline."],
                "pain_points": ["Generic claims without reproducible evidence."],
                "evidence_bar": "A repeatable comparison with source evidence.",
            }
            harness_path.write_text(yaml.safe_dump(harness, sort_keys=False), encoding="utf-8")

            errors = validate(root)

        self.assertFalse(any("areas.test_output.icp" in error for error in errors), errors)

    def test_active_planning_area_rejects_missing_or_malformed_icp(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            write_framework_manifest(farplane)
            write_required_project_files(root)
            harness_path = farplane / "harness.yaml"
            harness = yaml.safe_load(harness_path.read_text(encoding="utf-8"))
            harness["status"] = "active"
            harness["areas"]["test_output"]["icp"] = {
                "label": "Test builders",
                "description": "",
                "jobs_to_be_done": [],
                "pain_points": ["Generic claims."],
                "evidence_bar": "Repeatable comparison.",
                "trend_score": 7,
            }
            harness_path.write_text(yaml.safe_dump(harness, sort_keys=False), encoding="utf-8")

            errors = validate(root)

        joined = "\n".join(errors)
        self.assertIn("areas.test_output.icp has unsupported fields: trend_score", joined)
        self.assertIn("areas.test_output.icp.description must be a non-empty string", joined)
        self.assertIn("areas.test_output.icp.jobs_to_be_done must be a non-empty list of strings", joined)

    def test_draft_harness_may_defer_area_skill_selection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            write_framework_manifest(farplane)
            write_required_project_files(root)
            harness_path = farplane / "harness.yaml"
            harness = yaml.safe_load(harness_path.read_text(encoding="utf-8"))
            harness["status"] = "draft"
            harness["areas"]["test_output"]["skill_refs"] = []
            harness_path.write_text(yaml.safe_dump(harness, sort_keys=False), encoding="utf-8")

            errors = validate(root)

        self.assertNotIn(
            "farplane/harness.yaml areas.test_output.skill_refs must be a non-empty list.",
            errors,
        )

    def test_selected_metric_without_definition_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            write_framework_manifest(farplane)
            write_required_project_files(root)
            select_project_objective(farplane, "unknown_metric")

            errors = validate(root)

        self.assertIn("farplane/harness.yaml metric refs lack metrics.yaml definitions: unknown_metric.", errors)

    def test_objective_metric_does_not_require_area_owner(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            write_framework_manifest(farplane)
            write_required_project_files(root)
            select_project_objective(farplane, "accepted_harness_improvements")
            (farplane / "metrics.yaml").write_text(
                """kind: project-metrics
framework_template_version: "0.2.0"
metrics:
  accepted_harness_improvements:
    refresh: Count ticket Reward rows.
    label: Accepted harness improvements
    description: Accepted improvements with ticket proof.
    kind: daily_count
    unit: improvements
    display: bar_plus_cumulative
    direction: maximize
    max_age_days: 7
  accepted_product_output:
    refresh: Count accepted product outputs.
    label: Accepted product output
    description: Accepted product output.
    kind: daily_count
    unit: artifacts
    display: bar_plus_cumulative
    direction: maximize
    max_age_days: 7
""",
                encoding="utf-8",
            )
            (farplane / "bindings.yaml").write_text(
                """kind: project-bindings
framework_template_version: "0.1.0"
project: {}
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

    def test_selected_rows_require_direction_freshness_and_guard_rule(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            write_framework_manifest(farplane)
            write_required_project_files(root)
            select_project_objective(farplane, "accepted_harness_improvements", guards=["todo_unclaimed_ticket_count"])
            (farplane / "metrics.yaml").write_text(
                """kind: project-metrics
framework_template_version: "0.2.0"
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
  accepted_product_output:
    label: Accepted product output
    description: Accepted product output.
    kind: daily_count
    unit: artifacts
    display: bar_plus_cumulative
    direction: maximize
    max_age_days: 7
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
  accepted_product_output:
    refresh: Count accepted product outputs.
""",
                encoding="utf-8",
            )

            errors = validate(root)

        self.assertIn(
            "farplane/metrics.yaml selected objective definitions must declare direction: accepted_harness_improvements.",
            errors,
        )
        self.assertIn(
            "farplane/harness.yaml guard refs lack metrics.yaml guard rules: todo_unclaimed_ticket_count.",
            errors,
        )
        self.assertIn(
            "farplane/metrics.yaml selected definitions must declare positive max_age_days: accepted_harness_improvements, todo_unclaimed_ticket_count.",
            errors,
        )

    def test_objective_metric_without_unit_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            write_framework_manifest(farplane)
            write_required_project_files(root)
            select_project_objective(farplane, "accepted_harness_improvements")
            (farplane / "metrics.yaml").write_text(
                """kind: project-metrics
framework_template_version: "0.2.0"
metrics:
  accepted_harness_improvements:
    label: Accepted harness improvements
    description: Accepted improvements.
    kind: daily_count
    display: bar_plus_cumulative
    direction: maximize
    max_age_days: 7
  accepted_product_output:
    label: Accepted product output
    description: Accepted product output.
    kind: daily_count
    unit: artifacts
    display: bar_plus_cumulative
    direction: maximize
    max_age_days: 7
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
  accepted_product_output:
    refresh: Count accepted product outputs.
""",
                encoding="utf-8",
            )

            errors = validate(root)

        self.assertIn(
            "farplane/metrics.yaml selected metric definitions lack unit: accepted_harness_improvements.",
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
                json.dumps({"sources": [{"path": "farplane/metrics.yaml", "hash": "sha256:not-current"}]}),
                encoding="utf-8",
            )

            errors = validate(root)

        self.assertIn(".farplane/project/ui/latest.json is stale for farplane/metrics.yaml; regenerate project snapshot.", errors)


if __name__ == "__main__":
    unittest.main()
