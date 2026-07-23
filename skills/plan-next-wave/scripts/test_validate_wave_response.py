from __future__ import annotations

import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path

import yaml


MODULE_PATH = Path(__file__).with_name("validate_wave_response.py")
SPEC = importlib.util.spec_from_file_location("validate_wave_response", MODULE_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)
PROJECT_ROOT = MODULE_PATH.parents[3]


def valid_call(call_id: str = "content-1") -> dict:
    return {
        "call_id": call_id,
        "title": "Turn the accepted ablation into one evidence-led launch package",
        "skill_ref": "farplane-content-creation",
        "area_id": "framework_delivery",
        "arguments": {
            "product_bet_ref": "autonomous_teams_24_7",
            "system_ref": "SYS-0005",
            "feature_refs": ["FEAT-0008"],
            "source_or_idea": "tickets/TASK-0384/artifacts/accepted-ablation.md",
            "audience": "harness engineers evaluating agent reliability",
            "content_goal": "make the accepted recovery proof understandable and reusable",
            "channels": ["article", "video", "x"],
        },
        "expected_artifact": "an approved skeleton, optimized exemplar, and controlled channel variants",
        "current_alternative": "the proof remains buried in a ticket artifact",
        "why_now": "the ablation is accepted and distribution reach is below target",
        "evidence_refs": ["tickets/TASK-0384/artifacts/accepted-ablation.md"],
        "objective_contribution": {
            "ultimate_kpi_id": "evidence_distribution_reach",
            "contribution_type": "enabler",
            "kpi_or_guard_id": "planner_idea_keep_rate",
            "causal_mechanism": "turn accepted evidence into an audience-usable exemplar",
            "expected_change": "one reviewed distribution package ready for a separately gated handoff",
            "forecast_basis": {
                "kind": "configured_threshold",
                "ref": "tickets/TASK-0384/artifacts/bootstrap/eval-version.yaml",
            },
            "metric_provider": "blinded human proposal decisions",
            "signal_horizon": "delayed",
            "check_in_at": "unscheduled",
        },
        "lifecycle": {"status": "todo", "depends_on": [], "human_gate": ["publish", "separate approval"]},
        "proof": {
            "success": "a reviewer accepts the exemplar and every variant preserves its proof spine",
            "falsifier": "the exemplar is rejected or variants overstate the accepted evidence",
        },
        "dedupe": {
            "compared_against": ["tickets/TASK-0384/ticket.md"],
            "decision": "materially_distinct",
        },
        "ranking": {
            "reason": "accepted evidence and a short path to an inspectable audience artifact",
            "confidence": "medium",
            "time_to_signal": "one review cycle",
            "cost": "low",
            "risk": "low",
            "human_load": "two bounded approvals",
            "interference": "none",
        },
    }


def valid_payload() -> dict:
    call = valid_call()
    return {
        "global_query_receipt": {"command": "farplane tickets history --json", "limit": 20},
        "diagnosis": {
            "goal_state": {"active": [], "completed": [], "source_gaps": []},
            "objective_progress": [],
            "wave_size": 1,
            "dogfood_role": "not_supplied",
            "hard_guard": {"status": "healthy"},
        },
        "skill_receipts": [{"skill_ref": "farplane-content-creation", "contract_read": True}],
        "progressive_queries": [],
        "proposed_skill_calls": [call],
        "rejections": [],
        "decision": {
            "admitted_call_ids": [call["call_id"]],
            "source_gaps": [],
            "human_request": None,
            "unused_capacity_reason": None,
            "validation_receipt": {"ok": True},
            "no_materialization_receipt": {
                "tickets_written": 0,
                "materialized": False,
                "executed": False,
                "owner": "pulse-update",
            },
        },
    }


class WaveResponseValidatorTests(unittest.TestCase):
    def test_representative_compact_call_passes(self) -> None:
        self.assertEqual(validator.validate_wave_response(valid_payload(), PROJECT_ROOT), [])

    def test_empty_wave_with_exact_guard_reason_passes(self) -> None:
        payload = valid_payload()
        payload["proposed_skill_calls"] = []
        payload["decision"]["admitted_call_ids"] = []
        payload["decision"]["source_gaps"] = ["guard:api_error_rate stale at metrics observation ref"]
        self.assertEqual(validator.validate_wave_response(payload, PROJECT_ROOT), [])

    def test_only_configured_resolvable_skills_are_allowed(self) -> None:
        payload = valid_payload()
        payload["proposed_skill_calls"][0]["skill_ref"] = "research"
        errors = validator.validate_wave_response(payload, PROJECT_ROOT)
        self.assertTrue(any("must be configured" in error for error in errors))

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "farplane").mkdir()
            (root / "farplane" / "harness.yaml").write_text(
                yaml.safe_dump({"planning": {"skill_refs": ["missing-skill"]}}), encoding="utf-8"
            )
            payload["proposed_skill_calls"][0]["skill_ref"] = "missing-skill"
            errors = validator.validate_wave_response(payload, root)
            self.assertTrue(any("does not resolve" in error for error in errors))

    def test_agent_skill_contract_wins_and_arguments_are_exact(self) -> None:
        payload = valid_payload()
        arguments = payload["proposed_skill_calls"][0]["arguments"]
        arguments.pop("audience")
        arguments["ticket"] = "tickets/TASK-9999/ticket.md"
        arguments["taste_refs"] = ["not planner-owned"]
        errors = validator.validate_wave_response(payload, PROJECT_ROOT)
        self.assertTrue(any("missing planner-required arguments: audience" in error for error in errors))
        self.assertTrue(any("non-required arguments" in error and "ticket" in error for error in errors))
        self.assertTrue(any("non-required arguments" in error and "taste_refs" in error for error in errors))

    def test_planner_contract_arguments_must_exist_in_public_signature(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            skill = root / ".agents" / "skills" / "broken-skill"
            skill.mkdir(parents=True)
            (root / "farplane").mkdir()
            (root / "farplane" / "harness.yaml").write_text(
                yaml.safe_dump({"planning": {"skill_refs": ["broken-skill"]}}), encoding="utf-8"
            )
            (skill / "SKILL.md").write_text(
                """---
name: broken-skill
planner_contract:
  required_arguments: [\"question\", \"missing_decision\"]
---

## Skill Signature

```text
broken_skill(question, ticket?)
  -> result
```
""",
                encoding="utf-8",
            )
            payload = valid_payload()
            payload["proposed_skill_calls"][0]["skill_ref"] = "broken-skill"
            payload["proposed_skill_calls"][0]["arguments"] = {
                "question": "What changed?",
                "missing_decision": "ship or stop",
            }
            errors = validator.validate_wave_response(payload, root)

        self.assertTrue(any("missing from public signature: missing_decision" in error for error in errors))

    def test_blank_required_argument_fails(self) -> None:
        payload = valid_payload()
        payload["proposed_skill_calls"][0]["arguments"]["content_goal"] = " "
        errors = validator.validate_wave_response(payload, PROJECT_ROOT)
        self.assertTrue(any("content_goal must be concretely bound" in error for error in errors))

    def test_strategic_refs_must_belong_to_one_product_bet(self) -> None:
        payload = valid_payload()
        payload["proposed_skill_calls"][0]["arguments"]["system_ref"] = "SYS-0006"
        payload["proposed_skill_calls"][0]["arguments"]["feature_refs"] = ["FEAT-0022"]
        errors = validator.validate_wave_response(payload, PROJECT_ROOT)
        self.assertTrue(any("system_ref must belong" in error for error in errors))
        self.assertTrue(any("feature_refs must belong" in error for error in errors))

    def test_feature_refs_must_belong_to_selected_system(self) -> None:
        payload = valid_payload()
        arguments = payload["proposed_skill_calls"][0]["arguments"]
        arguments["product_bet_ref"] = "agent_sdlc"
        arguments["system_ref"] = "SYS-0005"
        arguments["feature_refs"] = ["FEAT-0022"]
        errors = validator.validate_wave_response(payload, PROJECT_ROOT)
        self.assertTrue(any("feature_refs must belong to system_ref" in error for error in errors))

    def test_admission_ids_are_unique_known_and_within_wave_size(self) -> None:
        payload = valid_payload()
        second = copy.deepcopy(payload["proposed_skill_calls"][0])
        second["call_id"] = "content-2"
        second["arguments"]["source_or_idea"] = "another accepted proof"
        payload["proposed_skill_calls"].append(second)
        payload["decision"]["admitted_call_ids"] = ["content-1", "content-2", "unknown"]
        errors = validator.validate_wave_response(payload, PROJECT_ROOT)
        self.assertTrue(any("unknown call IDs" in error for error in errors))
        self.assertTrue(any("exceeds diagnosis.wave_size" in error for error in errors))

    def test_duplicate_semantic_or_repeated_full_calls_fail(self) -> None:
        payload = valid_payload()
        duplicate = copy.deepcopy(payload["proposed_skill_calls"][0])
        duplicate["call_id"] = "renamed"
        duplicate["title"] = "A renamed duplicate"
        duplicate["ranking"]["reason"] = "different ranking prose"
        payload["proposed_skill_calls"].append(duplicate)
        payload["skill_receipts"].append(copy.deepcopy(payload["proposed_skill_calls"][0]))
        errors = validator.validate_wave_response(payload, PROJECT_ROOT)
        self.assertTrue(any("duplicate semantic calls" in error for error in errors))
        self.assertTrue(any("repeated outside" in error for error in errors))

    def test_legacy_lane_card_and_spec_shape_fails(self) -> None:
        payload = valid_payload()
        payload["lane_receipts"] = []
        payload["decision"]["admitted_specs"] = []
        errors = validator.validate_wave_response(payload, PROJECT_ROOT)
        self.assertTrue(any("unsupported fields" in error for error in errors))
        self.assertTrue(any("retired lane/card/spec/workflow fields" in error for error in errors))

    def test_objective_contract_enforces_attribution_and_basis(self) -> None:
        payload = valid_payload()
        objective = payload["proposed_skill_calls"][0]["objective_contribution"]
        objective["kpi_or_guard_id"] = "evidence_distribution_reach"
        objective["forecast_basis"] = {"kind": "source_gap", "ref": "invented-ref"}
        errors = validator.validate_wave_response(payload, PROJECT_ROOT)
        self.assertTrue(any("enabler contributions must not claim" in error for error in errors))
        self.assertTrue(any("source_gap is required" in error for error in errors))
        self.assertTrue(any("ref must be omitted" in error for error in errors))

    def test_lifecycle_proof_dedupe_and_ranking_gates_fail_closed(self) -> None:
        payload = valid_payload()
        call = payload["proposed_skill_calls"][0]
        call["lifecycle"] = {"status": "running", "depends_on": "none", "human_gate": ["publish"]}
        call["proof"]["falsifier"] = ""
        call["dedupe"] = {"compared_against": "recent only", "decision": "renamed_repeat"}
        call["ranking"]["confidence"] = "certain"
        errors = validator.validate_wave_response(payload, PROJECT_ROOT)
        for fragment in ("status must be todo", "depends_on must be a list", "human_gate", "falsifier", "compared_against", "materially_distinct", "confidence"):
            self.assertTrue(any(fragment in error for error in errors), fragment)

    def test_no_materialization_and_empty_wave_reason_are_mandatory(self) -> None:
        payload = valid_payload()
        payload["proposed_skill_calls"] = []
        payload["decision"]["admitted_call_ids"] = []
        payload["decision"]["no_materialization_receipt"]["tickets_written"] = 1
        errors = validator.validate_wave_response(payload, PROJECT_ROOT)
        self.assertTrue(any("empty wave must name" in error for error in errors))
        self.assertTrue(any("must prove zero writes" in error for error in errors))

        payload["decision"]["no_materialization_receipt"]["tickets_written"] = False
        errors = validator.validate_wave_response(payload, PROJECT_ROOT)
        self.assertTrue(any("must prove zero writes" in error for error in errors))

    def test_non_object_payload_fails(self) -> None:
        self.assertEqual(validator.validate_wave_response([]), ["wave response must be an object"])


if __name__ == "__main__":
    unittest.main()
