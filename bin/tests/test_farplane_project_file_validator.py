from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

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
    def test_harness_goals_are_rejected_as_duplicate_mutable_strategy(self) -> None:
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

        self.assertIn(
            "farplane/harness.yaml goals is retired; keep objective metric movement in metric "
            "observations and mutable urgency, due dates, and proof on tickets.",
            errors,
        )

    def test_planning_allowlist_requires_resolvable_unique_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            write_framework_manifest(farplane)
            write_required_project_files(root)
            harness_path = farplane / "harness.yaml"
            harness = yaml.safe_load(harness_path.read_text(encoding="utf-8"))
            harness["planning"] = {
                "skill_refs": ["test-output", "test-output", "missing-skill"]
            }
            harness_path.write_text(yaml.safe_dump(harness, sort_keys=False), encoding="utf-8")

            errors = validate(root)

        self.assertIn(
            "farplane/harness.yaml planning.skill_refs must be unique: test-output.",
            errors,
        )
        self.assertIn(
            "farplane/harness.yaml planning.skill_refs are unresolved: missing-skill.",
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
    type: flow
    unit: improvements
    display: bar_plus_cumulative
    direction: maximize
    max_age_days: 7
  accepted_product_output:
    refresh: Count accepted product outputs.
    label: Accepted product output
    description: Accepted product output.
    type: flow
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

    def test_metric_recipe_requires_lean_semantics_and_rejects_projection_config(self) -> None:
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
    formula: revenue - cost
    windows: [week]
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
            "farplane/metrics.yaml metrics.accepted_harness_improvements uses unsupported derived/projection config: formula, kind, windows; declare only type: flow|stock|markdown and let refreshers emit facts while Core derives window views.",
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

    def test_selected_guard_needs_its_guard_rule(self) -> None:
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
    type: flow
    unit: improvements
    display: bar_plus_cumulative
  todo_unclaimed_ticket_count:
    label: Ready unclaimed tickets
    description: Ready unclaimed tickets.
    type: stock
    unit: tickets
    display: reading
  accepted_product_output:
    label: Accepted product output
    description: Accepted product output.
    type: flow
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
            "farplane/harness.yaml guard refs lack metrics.yaml guard rules: todo_unclaimed_ticket_count.",
            errors,
        )
        self.assertFalse([error for error in errors if "direction" in error or "max_age_days" in error])

    def test_a_metric_needs_only_its_name_and_how_to_read_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            write_framework_manifest(farplane)
            write_required_project_files(root)
            select_project_objective(farplane, "accepted_harness_improvements")
            metrics = yaml.safe_load((farplane / "metrics.yaml").read_text(encoding="utf-8"))
            metrics["metrics"]["accepted_harness_improvements"] = {
                "label": "Accepted harness improvements",
                "refresh": "Count accepted improvements.",
            }
            (farplane / "metrics.yaml").write_text(yaml.safe_dump(metrics, sort_keys=False), encoding="utf-8")

            errors = validate(root)

        self.assertFalse([error for error in errors if "metrics.yaml" in error])

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

    def test_gate_snapshot_skips_local_cache_freshness(self) -> None:
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

            with patch.dict(os.environ, {"FARPLANE_GIT_GATE_SNAPSHOT": "1"}):
                errors = validate(root)

        self.assertFalse([error for error in errors if "is stale" in error])

    def test_missing_ignored_paths_pass_and_wrong_type_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            farplane = root / "farplane"
            farplane.mkdir()
            write_framework_manifest(farplane)
            write_required_project_files(root)
            ui = root / ".farplane" / "project" / "ui"
            for child in ui.iterdir():
                child.unlink()
            ui.rmdir()

            missing_errors = validate(root)
            ui.write_text("not a directory", encoding="utf-8")
            wrong_type_errors = validate(root)

        self.assertFalse([error for error in missing_errors if "standard.ignored" in error])
        self.assertIn("farplane/manifest.json standard.ignored path is not a directory: .farplane/project/ui/.",
                      wrong_type_errors)


if __name__ == "__main__":
    unittest.main()
