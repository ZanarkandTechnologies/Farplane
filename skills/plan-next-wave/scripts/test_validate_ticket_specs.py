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
    "metric_refs": {
        "objectives": [
            {"metric_id": "activated_projects", "priority": 1},
            {"metric_id": "accepted_harness_improvements", "priority": 2},
        ],
        "guards": ["rejected_ai_ticket_count"],
    },
    "areas": {
        "delivery": {
            "planner_instruction": "Ship executable project value.",
            "icp": {"label": "Harness engineers"},
            "metric_refs": [{"metric_id": "activated_projects"}],
        },
        "self_improvement": {
            "planner_instruction": "Improve an evidenced harness behavior.",
            "icp": {"label": "Harness maintainers"},
            "metric_refs": [{"metric_id": "accepted_harness_improvements"}],
        },
    },
}
METRICS = {"metrics": {"activated_projects": {}, "accepted_harness_improvements": {}, "rejected_ai_ticket_count": {}}}


def valid_spec() -> dict:
    return {
        "title": "Activate project",
        "area_id": "delivery",
        "audience_context": {
            "icp_ref": "harness.areas.delivery.icp",
            "job_or_problem": "activate an agent project without hidden stalls",
            "baseline_or_default": "manual scripts and unverified setup",
            "belief_or_behavior_delta": "adopt the visible activation workflow after reproducible proof",
            "world_memory_refs": [".farplane/feed-scout/memory.md#proof-led-agent-engineering"],
            "evidence_refs": ["https://example.com/agent-builder-source"],
        },
        "objective_contribution": {
            "kpi_or_guard_id": "activated_projects",
            "causal_mechanism": "remove install blocker and run Pulse",
            "expected_change": "one project activates",
            "metric_provider": "farplane metrics primitives",
            "signal_horizon": "7 days",
            "check_in_at": "2026-07-19T00:00:00Z",
        },
        "reward": {"expected_reward": "one activation", "proof_route": "manifest plus Pulse receipt"},
        "execution": {
            "inputs": ["project root"],
            "output": "activated project",
            "setup_changes": [],
            "output_artifacts": [{
                "value_class": "direct_value",
                "kind": "working_product",
                "ref": "activated-project",
                "independent_value": "a real project runs the Farplane loop",
                "use_path": "operators can inspect it and sales can reuse the demo",
            }],
            "unattended_safe": True,
            "operator_dependency": "none",
            "stop_condition": "receipt exists",
        },
        "proof": {"checks": ["doctor passes"], "evidence_artifact": "artifacts/activation.json"},
        "ranking": {
            "lane": "delivery",
            "area_instruction_ref": "harness.areas.delivery.planner_instruction",
            "area_instruction_applied": "ships an executable activation rather than setup",
            "creation_reason": "blocked activation", "bottleneck": "install", "lever": "repair",
            "why_now": "project is drifted", "positive_output": "one activated external project",
            "setup_burden": "none", "bundled_setup": None, "first_exemplar": None,
            "priority_trace": {
                "objective_priority": 1,
                "current_value": "2",
                "target_value": "10",
                "target_date": "2026-08-01",
                "target_gap": "8 projects",
                "progress_status": "behind",
                "metric_freshness": "fresh through 2026-07-13",
                "metric_source_ref": ".farplane/metrics/observations/activated_projects/latest.json",
                "rank_reason": "highest expected activation movement after risk and time-to-signal",
            },
        },
        "trajectory": {
            "expected_metric_delta": "+1", "confidence": "medium", "duration": "1 day",
            "time_to_signal": "1 day", "cost": "low", "risk": "low", "reversibility": "high",
            "information_gain": "medium", "compounding_value": "high", "interference": "none",
            "human_load": "none",
            "horizon": "near-term", "reward_shape": "activation observed within 7 days",
            "prerequisites": [],
        },
    }


def valid_guard_restoration_spec() -> dict:
    spec = valid_spec()
    spec["title"] = "Restore rejected ticket guard observation"
    spec["objective_contribution"]["kpi_or_guard_id"] = "rejected_ai_ticket_count"
    spec["objective_contribution"]["causal_mechanism"] = "refresh the stale hard-guard reading"
    spec["objective_contribution"]["expected_change"] = "one fresh guard observation"
    spec["execution"]["output"] = "fresh rejected ticket guard observation"
    spec["execution"]["output_artifacts"] = [{
        "value_class": "guard_restoration",
        "kind": "metric_observation",
        "guard_id": "rejected_ai_ticket_count",
        "ref": "artifacts/guards/rejected-ai-ticket-count.json",
        "independent_value": "restores the hard admission signal",
        "use_path": "the next planner run can safely decide ordinary admission",
    }]
    spec["ranking"]["setup_burden"] = "unavoidable_guard_restoration"
    spec["ranking"]["positive_output"] = "fresh hard-guard reading"
    spec["ranking"]["priority_trace"].update({
        "objective_priority": "guard",
        "progress_status": "guard",
        "rank_reason": "restores the stale hard guard before ordinary admission",
    })
    return spec


def valid_experiment_spec(feedback_class: str = "immediate") -> dict:
    spec = valid_spec()
    spec["title"] = "Test a ticket allocator guard"
    spec["area_id"] = "self_improvement"
    spec["audience_context"].update({
        "icp_ref": "harness.areas.self_improvement.icp",
        "job_or_problem": "prevent duplicate ticket IDs",
        "baseline_or_default": "manual next-ID guessing",
        "belief_or_behavior_delta": "maintainers trust one canonical allocator after collision proof",
        "world_memory_refs": [],
        "evidence_refs": ["tickets/TASK-0001/artifacts/duplicate-id-failure.md"],
    })
    spec["objective_contribution"]["kpi_or_guard_id"] = "accepted_harness_improvements"
    spec["ranking"].update({
        "lane": "experiment",
        "area_instruction_ref": "harness.areas.self_improvement.planner_instruction",
        "area_instruction_applied": "tests a preventive mechanism for an observed harness failure",
        "recurring_failure": "duplicate ticket IDs",
        "preventive_mechanism": "canonical allocator experiment",
        "next_run_proof": "create ten collision-free IDs",
    })
    spec["ranking"]["priority_trace"]["objective_priority"] = 2
    spec["execution"]["output_artifacts"][0]["kind"] = "experiment_result"
    spec["experiment"] = {
        "feedback_class": feedback_class,
        "target_surface": "ticket allocator",
        "hypothesis": "one allocator prevents duplicate IDs",
        "baseline": "duplicate IDs have occurred",
        "goal_route": "self-improve",
        "check_in_program": {"mode": "not_applicable"},
    }
    if feedback_class in {"delayed", "human_feedback"}:
        spec["experiment"].update({
            "reward_id": "allocator-result-7d",
            "check_in_program": {
                "procedure": "read the original ticket evidence and current allocator results",
                "idempotency": "update the same Reward row only",
                "source_gaps": "record missing ticket evidence without deciding",
                "decisions": ["accept", "kill", "monitor"],
            },
        })
    if feedback_class == "human_feedback":
        spec["experiment"]["goal_route"] = "optimize-with-human"
        spec["experiment"]["feedback_artifact"] = "artifacts/operator-feedback.md"
    return spec


class TicketSpecValidatorTests(unittest.TestCase):
    def test_valid_complete_spec_passes(self) -> None:
        self.assertEqual(validator.validate_spec(valid_spec(), HARNESS, METRICS), [])

    def test_outward_spec_requires_icp_baseline_delta_and_world_memory(self) -> None:
        spec = valid_spec()
        spec["audience_context"] = {
            "icp_ref": "harness.areas.delivery.icp",
            "job_or_problem": "",
            "baseline_or_default": "",
            "belief_or_behavior_delta": "",
            "world_memory_refs": [],
            "evidence_refs": [],
        }
        errors = validator.validate_spec(spec, HARNESS, METRICS)
        self.assertIn("audience_context.job_or_problem is required", errors)
        self.assertIn("audience_context.baseline_or_default is required", errors)
        self.assertIn("audience_context.belief_or_behavior_delta is required", errors)
        self.assertIn("audience_context.evidence_refs must be a non-empty list of refs", errors)
        self.assertIn("outward-facing specs require at least one audience_context.world_memory_refs entry", errors)

    def test_kpi_free_or_partial_spec_fails(self) -> None:
        spec = valid_spec()
        spec["objective_contribution"]["kpi_or_guard_id"] = ""
        spec["objective_contribution"]["metric_provider"] = "none mechanical"
        spec["objective_contribution"]["check_in_at"] = None
        errors = validator.validate_spec(spec, HARNESS, METRICS)
        self.assertIn("kpi_or_guard_id must name an existing metric", errors)
        self.assertIn("metric_provider cannot be none mechanical", errors)
        self.assertIn("delayed specs require objective_contribution.check_in_at", errors)

    def test_delayed_check_in_must_be_iso_datetime(self) -> None:
        spec = valid_spec()
        spec["objective_contribution"]["check_in_at"] = "after artifact review"
        self.assertIn(
            "delayed specs require objective_contribution.check_in_at as an ISO-8601 datetime",
            validator.validate_spec(spec, HARNESS, METRICS),
        )

    def test_unknown_area_or_metric_fails(self) -> None:
        spec = valid_spec()
        spec["area_id"] = "unknown"
        spec["objective_contribution"]["kpi_or_guard_id"] = "made_up"
        errors = validator.validate_spec(spec, HARNESS, METRICS)
        self.assertIn("area_id must name an existing harness area", errors)
        self.assertIn("kpi_or_guard_id must name an existing metric", errors)

    def test_area_instruction_traceability_is_required(self) -> None:
        spec = valid_spec()
        spec["ranking"]["area_instruction_ref"] = "harness.areas.self_improvement.planner_instruction"
        spec["ranking"]["area_instruction_applied"] = ""
        errors = validator.validate_spec(spec, HARNESS, METRICS)
        self.assertIn(
            "ranking.area_instruction_ref must equal harness.areas.delivery.planner_instruction",
            errors,
        )
        self.assertIn("ranking.area_instruction_applied is required", errors)

    def test_lane_and_metric_priority_trace_are_required(self) -> None:
        spec = valid_spec()
        spec["ranking"]["lane"] = ""
        spec["ranking"]["priority_trace"] = {}
        errors = validator.validate_spec(spec, HARNESS, METRICS)
        self.assertIn(
            "ranking.lane must be delivery, ablation, experiment, rollout, or operations",
            errors,
        )
        self.assertIn(
            "ranking.priority_trace.objective_priority must match the configured objective priority, guard, or unselected",
            errors,
        )
        self.assertIn("ranking.priority_trace.current_value is required", errors)
        self.assertIn(
            "ranking.priority_trace.progress_status must be ahead, on_track, behind, unknown, or guard",
            errors,
        )

    def test_unknown_progress_is_valid_when_target_is_unconfigured(self) -> None:
        spec = valid_spec()
        spec["ranking"]["priority_trace"].update({
            "target_value": "unconfigured",
            "target_date": "unconfigured",
            "target_gap": "unknown",
            "progress_status": "unknown",
            "rank_reason": "target pace is unknown; ranking uses priority and evidenced marginal movement",
        })
        self.assertEqual(validator.validate_spec(spec, HARNESS, METRICS), [])

    def test_directional_progress_requires_configured_target_trajectory(self) -> None:
        spec = valid_spec()
        spec["ranking"]["priority_trace"].update({
            "target_value": "unconfigured",
            "target_date": "unconfigured",
            "target_gap": "unknown",
            "progress_status": "behind",
        })
        self.assertIn(
            "ranking.priority_trace.progress_status=behind requires configured "
            "target_value, target_date, and target_gap",
            validator.validate_spec(spec, HARNESS, METRICS),
        )

    def test_selected_area_requires_canonical_instruction(self) -> None:
        spec = valid_spec()
        harness = {
            **HARNESS,
            "areas": {**HARNESS["areas"], "delivery": {"metric_refs": [{"metric_id": "activated_projects"}]}},
        }
        self.assertIn(
            "selected harness area must define planner_instruction",
            validator.validate_spec(spec, harness, METRICS),
        )

    def test_output_and_horizon_are_required(self) -> None:
        spec = valid_spec()
        spec["ranking"]["positive_output"] = ""
        spec["trajectory"]["horizon"] = ""
        spec["trajectory"]["reward_shape"] = ""
        errors = validator.validate_spec(spec, HARNESS, METRICS)
        self.assertIn("ranking.positive_output is required", errors)
        self.assertIn("trajectory.horizon is required", errors)
        self.assertIn("trajectory.reward_shape is required", errors)

    def test_independent_output_artifact_and_use_path_are_required(self) -> None:
        spec = valid_spec()
        spec["execution"]["output_artifacts"] = []
        errors = validator.validate_spec(spec, HARNESS, METRICS)
        self.assertIn("execution.output_artifacts must contain at least one direct-value artifact record", errors)

    def test_setup_and_proof_only_artifacts_are_rejected(self) -> None:
        spec = valid_spec()
        spec["execution"]["output_artifacts"] = [
            {"value_class": "setup", "kind": "schema", "ref": "schema.yaml", "independent_value": "future setup", "use_path": "future ticket"},
            {"value_class": "proof", "kind": "test_report", "ref": "tests.txt", "independent_value": "passing receipt", "use_path": "review"},
        ]
        errors = validator.validate_spec(spec, HARNESS, METRICS)
        self.assertIn("execution.output_artifacts[0].value_class must be direct_value", errors)
        self.assertIn("execution.output_artifacts[0].kind must name a supported direct-value artifact kind", errors)
        self.assertIn("execution.output_artifacts[1].value_class must be direct_value", errors)
        self.assertIn("execution.output_artifacts[1].kind must name a supported direct-value artifact kind", errors)

    def test_false_none_setup_burden_is_rejected(self) -> None:
        spec = valid_spec()
        spec["execution"]["setup_changes"] = ["creator schema", "render template"]
        errors = validator.validate_spec(spec, HARNESS, METRICS)
        self.assertIn(
            "specs with execution.setup_changes must declare ranking.setup_burden as bundled or unavoidable_guard_restoration",
            errors,
        )

    def test_bundled_setup_requires_first_exemplar(self) -> None:
        spec = valid_spec()
        spec["ranking"]["setup_burden"] = "bundled"
        spec["execution"]["setup_changes"] = ["minimal creator voice and render template"]
        errors = validator.validate_spec(spec, HARNESS, METRICS)
        self.assertIn("bundled setup requires ranking.bundled_setup", errors)
        self.assertIn("bundled setup requires ranking.first_exemplar", errors)
        spec["ranking"]["bundled_setup"] = "minimal creator voice and render template"
        spec["ranking"]["first_exemplar"] = "activated-project"
        self.assertEqual(validator.validate_spec(spec, HARNESS, METRICS), [])

    def test_wave_rejects_multiple_setup_bearing_specs(self) -> None:
        first = valid_spec()
        second = valid_spec()
        for spec in (first, second):
            spec["ranking"]["setup_burden"] = "bundled"
            spec["ranking"]["bundled_setup"] = "creator setup"
            spec["ranking"]["first_exemplar"] = "activated-project"
            spec["execution"]["setup_changes"] = ["creator setup"]
        result = validator.validate_payload([first, second], HARNESS, METRICS)
        self.assertFalse(result["ok"])
        self.assertIn(
            "an ordinary wave may contain at most one bundled-setup exemplar spec",
            result["results"][0]["errors"],
        )

    def test_honest_guard_observation_passes_alone(self) -> None:
        result = validator.validate_payload([valid_guard_restoration_spec()], HARNESS, METRICS)
        self.assertTrue(result["ok"])

    def test_guard_restoration_rejects_mixed_delivery_wave(self) -> None:
        result = validator.validate_payload([valid_guard_restoration_spec(), valid_spec()], HARNESS, METRICS)
        self.assertFalse(result["ok"])
        self.assertIn(
            "a guard-restoration wave must contain exactly one total spec and no ordinary delivery",
            result["results"][0]["errors"],
        )
        self.assertIn(
            "a guard-restoration wave must contain exactly one total spec and no ordinary delivery",
            result["results"][1]["errors"],
        )

    def test_guard_restoration_must_bind_configured_guard(self) -> None:
        spec = valid_guard_restoration_spec()
        spec["objective_contribution"]["kpi_or_guard_id"] = "activated_projects"
        errors = validator.validate_spec(spec, HARNESS, METRICS)
        self.assertIn("guard restoration must bind kpi_or_guard_id to a configured project guard", errors)
        self.assertIn(
            "execution.output_artifacts[0].guard_id must equal the configured guard bound by objective_contribution",
            errors,
        )

    def test_ordinary_spec_cannot_use_guard_restoration_artifact(self) -> None:
        spec = valid_spec()
        spec["execution"]["output_artifacts"] = valid_guard_restoration_spec()["execution"]["output_artifacts"]
        errors = validator.validate_spec(spec, HARNESS, METRICS)
        self.assertIn("execution.output_artifacts[0].value_class must be direct_value", errors)
        self.assertIn("execution.output_artifacts[0].kind must name a supported direct-value artifact kind", errors)

    def test_guard_restoration_cannot_masquerade_as_direct_value(self) -> None:
        spec = valid_guard_restoration_spec()
        spec["execution"]["output_artifacts"] = valid_spec()["execution"]["output_artifacts"]
        errors = validator.validate_spec(spec, HARNESS, METRICS)
        self.assertIn("execution.output_artifacts[0].value_class must be guard_restoration", errors)
        self.assertIn("execution.output_artifacts[0].kind must be metric_observation", errors)

    def test_unattended_safety_is_required(self) -> None:
        spec = valid_spec()
        spec["execution"]["unattended_safe"] = False
        spec["execution"]["operator_dependency"] = "migration choice"
        errors = validator.validate_spec(spec, HARNESS, METRICS)
        self.assertIn("execution.unattended_safe must be true", errors)
        self.assertIn("execution.operator_dependency must be none", errors)

    def test_self_improvement_requires_prevention_fields(self) -> None:
        spec = valid_spec()
        spec["area_id"] = "self_improvement"
        spec["audience_context"].update({
            "icp_ref": "harness.areas.self_improvement.icp",
            "world_memory_refs": [],
            "evidence_refs": ["tickets/TASK-0001/artifacts/duplicate-id-failure.md"],
        })
        spec["objective_contribution"]["kpi_or_guard_id"] = "accepted_harness_improvements"
        spec["ranking"]["area_instruction_ref"] = "harness.areas.self_improvement.planner_instruction"
        spec["ranking"]["area_instruction_applied"] = "tests an evidenced preventive mechanism"
        errors = validator.validate_spec(spec, HARNESS, METRICS)
        self.assertIn("self-improvement ranking.recurring_failure is required", errors)
        self.assertIn("self-improvement ranking.preventive_mechanism is required", errors)
        self.assertIn("self-improvement ranking.next_run_proof is required", errors)

        spec["ranking"].update({
            "recurring_failure": "duplicate ticket IDs",
            "preventive_mechanism": "canonical allocator",
            "next_run_proof": "create ten collision-free IDs",
        })
        spec["ranking"]["priority_trace"]["objective_priority"] = 2
        self.assertEqual(validator.validate_spec(spec, HARNESS, METRICS), [])

    def test_immediate_experiment_has_no_delayed_checkin_debt(self) -> None:
        self.assertEqual(validator.validate_spec(valid_experiment_spec(), HARNESS, METRICS), [])
        spec = valid_experiment_spec()
        spec["experiment"]["check_in_program"] = {"mode": "delayed"}
        self.assertIn(
            "immediate experiments require check_in_program.mode=not_applicable",
            validator.validate_spec(spec, HARNESS, METRICS),
        )

    def test_delayed_and_human_feedback_experiment_contracts(self) -> None:
        self.assertEqual(validator.validate_spec(valid_experiment_spec("delayed"), HARNESS, METRICS), [])
        self.assertEqual(validator.validate_spec(valid_experiment_spec("human_feedback"), HARNESS, METRICS), [])
        spec = valid_experiment_spec("human_feedback")
        spec["experiment"]["feedback_artifact"] = ""
        self.assertIn(
            "human-feedback experiments require experiment.feedback_artifact",
            validator.validate_spec(spec, HARNESS, METRICS),
        )


if __name__ == "__main__":
    unittest.main()
