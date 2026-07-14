#!/usr/bin/env python3
"""Validate planner ticket specs before Work Pulse materializes them."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


DIRECT_VALUE_ARTIFACT_KINDS = {
    "working_product",
    "product_surface",
    "rendered_media",
    "demo",
    "distribution_asset",
    "sales_asset",
    "customer_deliverable",
    "ablation_result",
    "experiment_result",
    "research_result",
    "preventive_mechanism",
}
EXPERIMENT_FEEDBACK_CLASSES = {"immediate", "delayed", "human_feedback"}
CANDIDATE_LANES = {"delivery", "ablation", "experiment", "rollout", "operations"}
PROGRESS_STATUSES = {"ahead", "on_track", "behind", "unknown", "guard"}
UNKNOWN_TRAJECTORY_VALUES = {"unknown", "unconfigured"}


def read_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return value if isinstance(value, dict) else {}


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_spec(spec: dict[str, Any], harness: dict[str, Any], metrics: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    areas = harness.get("areas") if isinstance(harness.get("areas"), dict) else {}
    metric_defs = metrics.get("metrics") if isinstance(metrics.get("metrics"), dict) else {}
    guards = harness.get("metric_refs", {}).get("guards", []) if isinstance(harness.get("metric_refs"), dict) else []
    objectives = harness.get("metric_refs", {}).get("objectives", []) if isinstance(harness.get("metric_refs"), dict) else []
    guard_ids = {
        str(ref.get("metric_id") if isinstance(ref, dict) else ref).strip()
        for ref in (guards if isinstance(guards, list) else [])
    }
    objective_priorities = {
        str(ref.get("metric_id") or "").strip(): ref.get("priority")
        for ref in (objectives if isinstance(objectives, list) else [])
        if isinstance(ref, dict) and str(ref.get("metric_id") or "").strip()
    }
    area_id = str(spec.get("area_id") or "").strip()
    if area_id not in areas:
        errors.append("area_id must name an existing harness area")
    elif not nonempty(areas[area_id].get("planner_instruction")):
        errors.append("selected harness area must define planner_instruction")

    audience_context = spec.get("audience_context")
    if not isinstance(audience_context, dict):
        errors.append("audience_context must be an object")
        audience_context = {}
    expected_icp_ref = f"harness.areas.{area_id}.icp"
    if str(audience_context.get("icp_ref") or "").strip() != expected_icp_ref:
        errors.append(f"audience_context.icp_ref must equal {expected_icp_ref}")
    for field in ("job_or_problem", "baseline_or_default", "belief_or_behavior_delta"):
        if not nonempty(audience_context.get(field)):
            errors.append(f"audience_context.{field} is required")
    world_memory_refs = audience_context.get("world_memory_refs")
    if not isinstance(world_memory_refs, list) or not all(nonempty(ref) for ref in world_memory_refs):
        errors.append("audience_context.world_memory_refs must be a list of non-empty refs")
        world_memory_refs = []
    evidence_refs = audience_context.get("evidence_refs")
    if not isinstance(evidence_refs, list) or not evidence_refs or not all(nonempty(ref) for ref in evidence_refs):
        errors.append("audience_context.evidence_refs must be a non-empty list of refs")
    if area_id != "self_improvement" and not world_memory_refs:
        errors.append("outward-facing specs require at least one audience_context.world_memory_refs entry")

    contribution = spec.get("objective_contribution")
    if not isinstance(contribution, dict):
        contribution = {}
    metric_id = str(contribution.get("kpi_or_guard_id") or "").strip()
    if not metric_id or metric_id not in metric_defs:
        errors.append("kpi_or_guard_id must name an existing metric")
    elif area_id in areas:
        area_refs = areas[area_id].get("metric_refs") if isinstance(areas[area_id], dict) else []
        area_metric_ids = {
            str(ref.get("metric_id") if isinstance(ref, dict) else ref).strip()
            for ref in (area_refs if isinstance(area_refs, list) else [])
        }
        if metric_id not in area_metric_ids and metric_id not in guard_ids:
            errors.append("kpi_or_guard_id must belong to the selected area or project guards")
    for field in ("causal_mechanism", "expected_change", "metric_provider", "signal_horizon"):
        if not nonempty(contribution.get(field)):
            errors.append(f"objective_contribution.{field} is required")
    if str(contribution.get("metric_provider") or "").strip().lower() == "none mechanical":
        errors.append("metric_provider cannot be none mechanical")
    delayed = str(contribution.get("signal_horizon") or "").strip().lower() not in {
        "immediate", "same_run", "same-run"
    }
    if delayed and not nonempty(contribution.get("check_in_at")):
        errors.append("delayed specs require objective_contribution.check_in_at")
    elif delayed:
        try:
            datetime.fromisoformat(str(contribution["check_in_at"]).replace("Z", "+00:00"))
        except ValueError:
            errors.append("delayed specs require objective_contribution.check_in_at as an ISO-8601 datetime")

    reward = spec.get("reward") if isinstance(spec.get("reward"), dict) else {}
    for field in ("expected_reward", "proof_route"):
        if not nonempty(reward.get(field)):
            errors.append(f"reward.{field} is required")

    experiment = spec.get("experiment")
    if experiment is not None:
        experiment = experiment if isinstance(experiment, dict) else {}
        feedback_class = str(experiment.get("feedback_class") or "").strip()
        if feedback_class not in EXPERIMENT_FEEDBACK_CLASSES:
            errors.append("experiment.feedback_class must be immediate, delayed, or human_feedback")
        for field in ("target_surface", "hypothesis", "baseline", "goal_route"):
            if not nonempty(experiment.get(field)):
                errors.append(f"experiment.{field} is required")
        check_in_program = experiment.get("check_in_program")
        if not isinstance(check_in_program, dict):
            errors.append("experiment.check_in_program must be an object")
            check_in_program = {}
        if feedback_class == "immediate":
            if check_in_program.get("mode") != "not_applicable":
                errors.append("immediate experiments require check_in_program.mode=not_applicable")
        elif feedback_class in {"delayed", "human_feedback"}:
            if not nonempty(experiment.get("reward_id")):
                errors.append("delayed and human-feedback experiments require experiment.reward_id")
            for field in ("procedure", "idempotency", "source_gaps"):
                if not nonempty(check_in_program.get(field)):
                    errors.append(f"delayed experiment check_in_program.{field} is required")
            decisions = check_in_program.get("decisions")
            if not isinstance(decisions, list) or not {"accept", "kill", "monitor"}.issubset(set(decisions)):
                errors.append("delayed experiment check_in_program.decisions must include accept, kill, and monitor")
        if feedback_class == "human_feedback":
            if str(experiment.get("goal_route") or "").strip() != "optimize-with-human":
                errors.append("human-feedback experiments require experiment.goal_route=optimize-with-human")
            if not nonempty(experiment.get("feedback_artifact")):
                errors.append("human-feedback experiments require experiment.feedback_artifact")

    ranking_hint = spec.get("ranking") if isinstance(spec.get("ranking"), dict) else {}
    setup_burden_hint = str(ranking_hint.get("setup_burden") or "").strip()
    is_guard_restoration = setup_burden_hint == "unavoidable_guard_restoration"
    if is_guard_restoration and metric_id not in guard_ids:
        errors.append("guard restoration must bind kpi_or_guard_id to a configured project guard")

    execution = spec.get("execution") if isinstance(spec.get("execution"), dict) else {}
    if not isinstance(execution.get("inputs"), list) or not execution.get("inputs"):
        errors.append("execution.inputs must be a non-empty list")
    for field in ("output", "stop_condition"):
        if not nonempty(execution.get(field)):
            errors.append(f"execution.{field} is required")
    setup_changes = execution.get("setup_changes")
    if not isinstance(setup_changes, list):
        errors.append("execution.setup_changes must be a list")
        setup_changes = []
    elif not all(nonempty(row) for row in setup_changes):
        errors.append("execution.setup_changes entries must be non-empty strings")
    output_artifacts = execution.get("output_artifacts")
    if not isinstance(output_artifacts, list) or not output_artifacts:
        expected = "guard-restoration metric observation" if is_guard_restoration else "direct-value artifact"
        errors.append(f"execution.output_artifacts must contain at least one {expected} record")
        output_artifacts = []
    direct_value_refs: set[str] = set()
    for index, artifact in enumerate(output_artifacts):
        prefix = f"execution.output_artifacts[{index}]"
        if not isinstance(artifact, dict):
            errors.append(f"{prefix} must be a structured artifact record")
            continue
        kind = str(artifact.get("kind") or "").strip()
        if is_guard_restoration:
            if artifact.get("value_class") != "guard_restoration":
                errors.append(f"{prefix}.value_class must be guard_restoration")
            if kind != "metric_observation":
                errors.append(f"{prefix}.kind must be metric_observation")
            artifact_guard_id = str(artifact.get("guard_id") or "").strip()
            if artifact_guard_id != metric_id or artifact_guard_id not in guard_ids:
                errors.append(f"{prefix}.guard_id must equal the configured guard bound by objective_contribution")
        else:
            if artifact.get("value_class") != "direct_value":
                errors.append(f"{prefix}.value_class must be direct_value")
            if kind not in DIRECT_VALUE_ARTIFACT_KINDS:
                errors.append(f"{prefix}.kind must name a supported direct-value artifact kind")
        for field in ("ref", "independent_value", "use_path"):
            if not nonempty(artifact.get(field)):
                errors.append(f"{prefix}.{field} is required")
        if nonempty(artifact.get("ref")):
            direct_value_refs.add(str(artifact["ref"]).strip())
    if execution.get("unattended_safe") is not True:
        errors.append("execution.unattended_safe must be true")
    if str(execution.get("operator_dependency") or "").strip().lower() != "none":
        errors.append("execution.operator_dependency must be none")

    proof = spec.get("proof") if isinstance(spec.get("proof"), dict) else {}
    if not isinstance(proof.get("checks"), list) or not proof.get("checks"):
        errors.append("proof.checks must be a non-empty list")
    if not nonempty(proof.get("evidence_artifact")):
        errors.append("proof.evidence_artifact is required")

    ranking = ranking_hint
    lane = str(ranking.get("lane") or "").strip()
    if lane not in CANDIDATE_LANES:
        errors.append("ranking.lane must be delivery, ablation, experiment, rollout, or operations")
    expected_instruction_ref = f"harness.areas.{area_id}.planner_instruction"
    if str(ranking.get("area_instruction_ref") or "").strip() != expected_instruction_ref:
        errors.append(
            "ranking.area_instruction_ref must equal "
            f"{expected_instruction_ref}"
        )
    if not nonempty(ranking.get("area_instruction_applied")):
        errors.append("ranking.area_instruction_applied is required")
    for field in ("creation_reason", "bottleneck", "lever", "why_now", "positive_output"):
        if not nonempty(ranking.get(field)):
            errors.append(f"ranking.{field} is required")
    setup_burden = str(ranking.get("setup_burden") or "").strip()
    allowed_setup_burdens = {"none", "bundled", "unavoidable_guard_restoration"}
    if setup_burden not in allowed_setup_burdens:
        errors.append("ranking.setup_burden must be none, bundled, or unavoidable_guard_restoration")
    if setup_changes and setup_burden == "none":
        errors.append("specs with execution.setup_changes must declare ranking.setup_burden as bundled or unavoidable_guard_restoration")
    if setup_burden == "bundled":
        if not setup_changes:
            errors.append("bundled setup requires non-empty execution.setup_changes")
        if not nonempty(ranking.get("bundled_setup")):
            errors.append("bundled setup requires ranking.bundled_setup")
        if not nonempty(ranking.get("first_exemplar")):
            errors.append("bundled setup requires ranking.first_exemplar")
        elif str(ranking["first_exemplar"]).strip() not in direct_value_refs:
            errors.append("ranking.first_exemplar must equal the ref of a direct-value output artifact")
    if area_id == "self_improvement":
        for field in ("recurring_failure", "preventive_mechanism", "next_run_proof"):
            if not nonempty(ranking.get(field)):
                errors.append(f"self-improvement ranking.{field} is required")
    priority_trace = ranking.get("priority_trace")
    if not isinstance(priority_trace, dict):
        errors.append("ranking.priority_trace must be an object")
        priority_trace = {}
    expected_priority: Any = (
        "guard" if metric_id in guard_ids
        else objective_priorities.get(metric_id, "unselected")
    )
    if priority_trace.get("objective_priority") != expected_priority:
        errors.append(
            "ranking.priority_trace.objective_priority must match the configured "
            "objective priority, guard, or unselected"
        )
    for field in (
        "current_value", "target_value", "target_date", "target_gap",
        "metric_freshness", "metric_source_ref", "rank_reason",
    ):
        if not nonempty(priority_trace.get(field)):
            errors.append(f"ranking.priority_trace.{field} is required")
    progress_status = str(priority_trace.get("progress_status") or "").strip()
    if progress_status not in PROGRESS_STATUSES:
        errors.append(
            "ranking.priority_trace.progress_status must be ahead, on_track, "
            "behind, unknown, or guard"
        )
    if progress_status == "guard" and metric_id not in guard_ids:
        errors.append("ranking.priority_trace.progress_status=guard requires a configured guard")
    if progress_status in {"ahead", "on_track", "behind"}:
        unknown_fields = [
            field
            for field in ("target_value", "target_date", "target_gap")
            if str(priority_trace.get(field) or "").strip().lower()
            in UNKNOWN_TRAJECTORY_VALUES
        ]
        if unknown_fields:
            errors.append(
                "ranking.priority_trace.progress_status="
                f"{progress_status} requires configured target_value, target_date, and target_gap"
            )
    trajectory = spec.get("trajectory") if isinstance(spec.get("trajectory"), dict) else {}
    for field in (
        "expected_metric_delta", "confidence", "duration", "time_to_signal",
        "cost", "risk", "reversibility", "information_gain",
        "compounding_value", "interference", "human_load", "horizon", "reward_shape",
    ):
        if not nonempty(trajectory.get(field)):
            errors.append(f"trajectory.{field} is required")
    if not isinstance(trajectory.get("prerequisites"), list):
        errors.append("trajectory.prerequisites must be a list")
    return errors


def validate_payload(payload: Any, harness: dict[str, Any], metrics: dict[str, Any]) -> dict[str, Any]:
    specs = payload if isinstance(payload, list) else payload.get("specs") if isinstance(payload, dict) else None
    if not isinstance(specs, list):
        return {"ok": False, "errors": ["payload must be a list or {specs: [...]}"]}
    results = []
    for index, spec in enumerate(specs):
        errors = validate_spec(spec, harness, metrics) if isinstance(spec, dict) else ["spec must be an object"]
        results.append({"index": index, "ok": not errors, "errors": errors})
    ordinary_setup_specs = [
        index for index, spec in enumerate(specs)
        if isinstance(spec, dict)
        and isinstance(spec.get("ranking"), dict)
        and spec["ranking"].get("setup_burden") == "bundled"
    ]
    if len(ordinary_setup_specs) > 1:
        message = "an ordinary wave may contain at most one bundled-setup exemplar spec"
        for index in ordinary_setup_specs:
            results[index]["ok"] = False
            results[index]["errors"].append(message)
    guard_restoration_specs = [
        index for index, spec in enumerate(specs)
        if isinstance(spec, dict)
        and isinstance(spec.get("ranking"), dict)
        and spec["ranking"].get("setup_burden") == "unavoidable_guard_restoration"
    ]
    if guard_restoration_specs and len(specs) != 1:
        message = "a guard-restoration wave must contain exactly one total spec and no ordinary delivery"
        for result in results:
            result["ok"] = False
            result["errors"].append(message)
    return {"ok": all(row["ok"] for row in results), "spec_count": len(specs), "results": results}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec_file")
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    payload = json.loads(Path(args.spec_file).read_text(encoding="utf-8"))
    result = validate_payload(
        payload,
        read_yaml(root / "farplane" / "harness.yaml"),
        read_yaml(root / "farplane" / "metrics.yaml"),
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
