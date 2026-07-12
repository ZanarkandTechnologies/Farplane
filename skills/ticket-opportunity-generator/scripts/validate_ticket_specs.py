#!/usr/bin/env python3
"""Validate planner ticket specs before Work Pulse materializes them."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


def read_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return value if isinstance(value, dict) else {}


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_spec(spec: dict[str, Any], harness: dict[str, Any], metrics: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    areas = harness.get("areas") if isinstance(harness.get("areas"), dict) else {}
    metric_defs = metrics.get("metrics") if isinstance(metrics.get("metrics"), dict) else {}
    area_id = str(spec.get("area_id") or "").strip()
    if area_id not in areas:
        errors.append("area_id must name an existing harness area")

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
        guards = harness.get("metric_refs", {}).get("guards", []) if isinstance(harness.get("metric_refs"), dict) else []
        guard_ids = {
            str(ref.get("metric_id") if isinstance(ref, dict) else ref).strip()
            for ref in (guards if isinstance(guards, list) else [])
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

    reward = spec.get("reward") if isinstance(spec.get("reward"), dict) else {}
    for field in ("expected_reward", "proof_route"):
        if not nonempty(reward.get(field)):
            errors.append(f"reward.{field} is required")

    execution = spec.get("execution") if isinstance(spec.get("execution"), dict) else {}
    if not isinstance(execution.get("inputs"), list) or not execution.get("inputs"):
        errors.append("execution.inputs must be a non-empty list")
    for field in ("output", "stop_condition"):
        if not nonempty(execution.get(field)):
            errors.append(f"execution.{field} is required")

    proof = spec.get("proof") if isinstance(spec.get("proof"), dict) else {}
    if not isinstance(proof.get("checks"), list) or not proof.get("checks"):
        errors.append("proof.checks must be a non-empty list")
    if not nonempty(proof.get("evidence_artifact")):
        errors.append("proof.evidence_artifact is required")

    ranking = spec.get("ranking") if isinstance(spec.get("ranking"), dict) else {}
    for field in ("creation_reason", "bottleneck", "lever", "why_now"):
        if not nonempty(ranking.get(field)):
            errors.append(f"ranking.{field} is required")
    trajectory = spec.get("trajectory") if isinstance(spec.get("trajectory"), dict) else {}
    for field in (
        "expected_metric_delta", "confidence", "duration", "time_to_signal",
        "cost", "risk", "reversibility", "information_gain",
        "compounding_value", "interference",
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
