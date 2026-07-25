from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("materialize_skill_call.py")
SPEC = importlib.util.spec_from_file_location("materialize_skill_call", MODULE_PATH)
assert SPEC and SPEC.loader
materializer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(materializer)


def call(call_id: str) -> dict:
    return {
        "call_id": call_id,
        "title": "Turn accepted proof into a content pack",
        "skill_ref": "farplane-content-creation",
        "area_id": "adoption_and_distribution",
        "arguments": {
            "source_or_idea": "tickets/TASK-1000/artifacts/accepted-proof.md",
            "audience": "harness engineers",
            "content_goal": "make the proof reproducible and worth sharing",
            "channels": ["video", "shorts", "carousel", "x", "linkedin"],
        },
        "expected_artifact": "one approved cross-format content pack",
        "objective_contribution": {
            "ultimate_kpi_id": "evidence_distribution_reach",
            "contribution_type": "enabler",
            "kpi_or_guard_id": "distribution_reach_per_artifact",
            "causal_mechanism": "transform accepted evidence into reusable formats",
            "expected_change": "one reviewed cross-format pack",
            "forecast_basis": {"kind": "configured_threshold", "ref": "farplane/metrics.yaml"},
            "metric_provider": "channel analytics after publication approval",
            "signal_horizon": "delayed",
            "check_in_at": "unscheduled",
        },
    }


class MaterializeSkillCallTests(unittest.TestCase):
    def test_admitted_call_ids_materialize_exact_generic_bindings(self) -> None:
        response = {
            "proposed_skill_calls": [call("content-1")],
            "decision": {"admitted_call_ids": ["content-1"]},
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paths = materializer.materialize_admitted_calls(
                root,
                response,
                ["TASK-1001"],
                created_at="2026-07-17T00:00:00Z",
            )
            text = paths[0].read_text(encoding="utf-8")

        self.assertIn("call_id: content-1", text)
        self.assertIn("skill_ref: farplane-content-creation", text)
        self.assertIn("source_or_idea:", text)
        self.assertIn("- linkedin", text)
        self.assertIn("area_id: adoption_and_distribution", text)
        self.assertNotIn("workflow_steps", text)
        self.assertNotIn("Todo List", text)
        self.assertNotIn("optimize-with-human", text)

    def test_refuses_missing_admitted_call_and_existing_ticket(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            response = {
                "proposed_skill_calls": [call("content-1")],
                "decision": {"admitted_call_ids": ["missing"]},
            }
            with self.assertRaisesRegex(ValueError, "admitted call 'missing' is missing"):
                materializer.materialize_admitted_calls(root, response, ["TASK-1001"])

            materializer.materialize_skill_call(root, "TASK-1001", call("content-1"))
            with self.assertRaises(FileExistsError):
                materializer.materialize_skill_call(root, "TASK-1001", call("content-1"))

    def test_materializes_optional_lifecycle_due_at_unchanged(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            dated = call("dated")
            dated["lifecycle"] = {
                "status": "todo",
                "depends_on": [],
                "human_gate": "none",
                "due_at": "2026-08-01T08:00:00+08:00",
            }
            dated_path = materializer.materialize_skill_call(root, "TASK-1001", dated)
            undated_path = materializer.materialize_skill_call(
                root, "TASK-1002", call("undated")
            )

            self.assertIn(
                "due_at: '2026-08-01T08:00:00+08:00'",
                dated_path.read_text(encoding="utf-8"),
            )
            self.assertNotIn("due_at:", undated_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
