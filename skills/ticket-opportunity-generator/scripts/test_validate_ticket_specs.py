from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("validate_ticket_specs.py")
SPEC = importlib.util.spec_from_file_location("validate_ticket_specs", MODULE_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


HARNESS = {
    "metric_refs": {"guards": ["rejected_ai_ticket_count"]},
    "areas": {"delivery": {"metric_refs": [{"metric_id": "activated_projects"}]}},
}
METRICS = {"metrics": {"activated_projects": {}, "rejected_ai_ticket_count": {}}}


def valid_spec() -> dict:
    return {
        "title": "Activate project",
        "area_id": "delivery",
        "objective_contribution": {
            "kpi_or_guard_id": "activated_projects",
            "causal_mechanism": "remove install blocker and run Pulse",
            "expected_change": "one project activates",
            "metric_provider": "farplane metrics primitives",
            "signal_horizon": "7 days",
            "check_in_at": "2026-07-19T00:00:00Z",
        },
        "reward": {"expected_reward": "one activation", "proof_route": "manifest plus Pulse receipt"},
        "execution": {"inputs": ["project root"], "output": "activated project", "stop_condition": "receipt exists"},
        "proof": {"checks": ["doctor passes"], "evidence_artifact": "artifacts/activation.json"},
        "ranking": {"creation_reason": "blocked activation", "bottleneck": "install", "lever": "repair", "why_now": "project is drifted"},
        "trajectory": {
            "expected_metric_delta": "+1", "confidence": "medium", "duration": "1 day",
            "time_to_signal": "1 day", "cost": "low", "risk": "low", "reversibility": "high",
            "information_gain": "medium", "compounding_value": "high", "interference": "none",
            "prerequisites": [],
        },
    }


class TicketSpecValidatorTests(unittest.TestCase):
    def test_valid_complete_spec_passes(self) -> None:
        self.assertEqual(validator.validate_spec(valid_spec(), HARNESS, METRICS), [])

    def test_kpi_free_or_partial_spec_fails(self) -> None:
        spec = valid_spec()
        spec["objective_contribution"]["kpi_or_guard_id"] = ""
        spec["objective_contribution"]["metric_provider"] = "none mechanical"
        spec["objective_contribution"]["check_in_at"] = None
        errors = validator.validate_spec(spec, HARNESS, METRICS)
        self.assertIn("kpi_or_guard_id must name an existing metric", errors)
        self.assertIn("metric_provider cannot be none mechanical", errors)
        self.assertIn("delayed specs require objective_contribution.check_in_at", errors)

    def test_unknown_area_or_metric_fails(self) -> None:
        spec = valid_spec()
        spec["area_id"] = "unknown"
        spec["objective_contribution"]["kpi_or_guard_id"] = "made_up"
        errors = validator.validate_spec(spec, HARNESS, METRICS)
        self.assertIn("area_id must name an existing harness area", errors)
        self.assertIn("kpi_or_guard_id must name an existing metric", errors)


if __name__ == "__main__":
    unittest.main()
