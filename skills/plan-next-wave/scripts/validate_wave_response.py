#!/usr/bin/env python3
"""Validate a compact Plan Next Wave skill-call response."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml


CORE_DIR = Path(__file__).resolve().parents[3] / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from farplane_ticket_reward import is_timezone_bearing_iso_datetime


ROOT_FIELDS = {
    "global_query_receipt",
    "diagnosis",
    "skill_receipts",
    "progressive_queries",
    "proposed_skill_calls",
    "rejections",
    "decision",
}
CALL_FIELDS = {
    "call_id",
    "title",
    "skill_ref",
    "arguments",
    "expected_artifact",
    "current_alternative",
    "why_now",
    "evidence_refs",
    "objective_contribution",
    "lifecycle",
    "proof",
    "dedupe",
    "ranking",
}
OBJECTIVE_FIELDS = {
    "ultimate_kpi_id",
    "contribution_type",
    "kpi_or_guard_id",
    "causal_mechanism",
    "expected_change",
    "forecast_basis",
    "metric_provider",
    "signal_horizon",
    "check_in_at",
}
ULTIMATE_KPIS = {"revenue_usd", "evidence_distribution_reach", "active_subscriptions"}
CONTRIBUTION_TYPES = {"outcome", "enabler", "guard"}
FORECAST_KINDS = {"measured_baseline", "cited_comparable", "configured_threshold", "source_gap"}
CONFIDENCE_LEVELS = {"low", "medium", "high"}
DEDUPE_DECISIONS = {"novel", "materially_distinct"}
LEGACY_FIELDS = {
    "lane_receipts",
    "idea_cards",
    "candidate_comparison",
    "admitted_specs",
    "idea_qa",
    "proposal_type",
    "lane",
    "archetype",
    "ticket_spec",
    "workflow_steps",
    "phases",
    "todos",
}


def nonempty(value: Any) -> bool:
    if value is None or isinstance(value, bool):
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def concretely_bound(value: Any) -> bool:
    """Allow meaningful scalar bindings (including booleans and zero)."""
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def read_yaml(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(loaded, dict):
        raise ValueError(f"{path} must contain a YAML object")
    return loaded


def read_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError(f"{path} must begin with YAML frontmatter")
    loaded = yaml.safe_load(parts[1]) or {}
    if not isinstance(loaded, dict):
        raise ValueError(f"{path} frontmatter must be an object")
    return loaded


def feature_system_ids(path: Path) -> dict[str, str]:
    bindings: dict[str, str] = {}
    if not path.exists():
        return bindings
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(row, dict):
            continue
        feature_ref = row.get("id")
        system_ref = row.get("system_id")
        if isinstance(feature_ref, str) and isinstance(system_ref, str):
            bindings[feature_ref] = system_ref
    return bindings


def registry_ids(path: Path) -> set[str]:
    ids: set[str] = set()
    if not path.exists():
        return ids
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(row, dict) and nonempty(row.get("id")):
            ids.add(str(row["id"]).strip())
    return ids


def public_signature_arguments(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    section = text.partition("## Skill Signature")[2]
    match = re.search(r"```text\s*\n?\w+\((.*?)\)\s*\n?\s*->", section, re.DOTALL)
    if not match:
        raise ValueError(f"{path} has no parseable public Skill Signature")
    names: set[str] = set()
    for raw in match.group(1).replace("\n", " ").split(","):
        name = raw.strip().split("=", 1)[0].rstrip("?").strip()
        if name:
            names.add(name)
    return names


def planning_contract(project_root: Path, skill_ref: str) -> tuple[dict[str, Any] | None, str | None]:
    for base in (project_root / ".agents" / "skills", project_root / "skills"):
        path = base / skill_ref / "SKILL.md"
        if not path.is_file():
            continue
        try:
            frontmatter = read_frontmatter(path)
        except (OSError, ValueError, yaml.YAMLError) as exc:
            return None, str(exc)
        contract = frontmatter.get("planner_contract")
        if not isinstance(contract, dict):
            return None, f"{path} has no planner_contract object"
        required = contract.get("required_arguments")
        if not isinstance(required, list) or not all(nonempty(item) for item in required):
            return None, f"{path} planner_contract.required_arguments must be a list of names"
        required_names = [str(item).strip() for item in required]
        if len(set(required_names)) != len(required_names):
            return None, f"{path} planner_contract.required_arguments must be unique"
        try:
            signature_names = public_signature_arguments(path)
        except (OSError, ValueError) as exc:
            return None, str(exc)
        absent = sorted(set(required_names) - signature_names)
        if absent:
            return None, f"{path} planner contract arguments missing from public signature: {', '.join(absent)}"
        return contract, None
    return None, f"configured skill {skill_ref!r} does not resolve to .agents/skills or skills"


def require_object_fields(
    value: Any, required: set[str], prefix: str, errors: list[str], *, optional: set[str] | None = None
) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{prefix} must be an object")
        return {}
    optional = optional or set()
    missing = sorted(required - set(value))
    extra = sorted(set(value) - required - optional)
    if missing:
        errors.append(f"{prefix} is missing required fields: {', '.join(missing)}")
    if extra:
        errors.append(f"{prefix} contains unsupported fields: {', '.join(extra)}")
    return value


def require_nonempty_fields(value: dict[str, Any], fields: set[str], prefix: str, errors: list[str]) -> None:
    for field in sorted(fields):
        if not nonempty(value.get(field)):
            errors.append(f"{prefix}.{field} is required")


def find_legacy_fields(value: Any, path: str = "response") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key in LEGACY_FIELDS:
                found.append(child_path)
            found.extend(find_legacy_fields(child, child_path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.extend(find_legacy_fields(child, f"{path}[{index}]"))
    return found


def contains_equal_object(value: Any, target: dict[str, Any], *, skip_calls: bool = False) -> bool:
    if isinstance(value, dict):
        if value == target:
            return True
        return any(contains_equal_object(child, target) for child in value.values())
    if isinstance(value, list):
        return any(contains_equal_object(child, target) for child in value)
    return False


def validate_objective(value: Any, prefix: str, errors: list[str]) -> None:
    objective = require_object_fields(value, OBJECTIVE_FIELDS, prefix, errors)
    require_nonempty_fields(objective, OBJECTIVE_FIELDS - {"forecast_basis"}, prefix, errors)
    ultimate = objective.get("ultimate_kpi_id")
    contribution = objective.get("contribution_type")
    metric = objective.get("kpi_or_guard_id")
    if ultimate not in ULTIMATE_KPIS:
        errors.append(f"{prefix}.ultimate_kpi_id must name an allowed ultimate KPI")
    if contribution not in CONTRIBUTION_TYPES:
        errors.append(f"{prefix}.contribution_type must be outcome, enabler, or guard")
    if contribution == "outcome" and metric != ultimate:
        errors.append(f"{prefix} outcome contributions must bind kpi_or_guard_id to the ultimate KPI")
    if contribution in {"enabler", "guard"} and metric == ultimate:
        errors.append(f"{prefix} {contribution} contributions must not claim the ultimate KPI directly")

    basis = require_object_fields(
        objective.get("forecast_basis"), {"kind"}, f"{prefix}.forecast_basis", errors,
        optional={"ref", "source_gap"},
    )
    kind = basis.get("kind")
    if kind not in FORECAST_KINDS:
        errors.append(f"{prefix}.forecast_basis.kind must name a supported basis")
    if kind == "source_gap":
        if not nonempty(basis.get("source_gap")):
            errors.append(f"{prefix}.forecast_basis.source_gap is required for source_gap forecasts")
        if nonempty(basis.get("ref")):
            errors.append(f"{prefix}.forecast_basis.ref must be omitted for source_gap forecasts")
    elif kind in FORECAST_KINDS and not nonempty(basis.get("ref")):
        errors.append(f"{prefix}.forecast_basis.ref is required for grounded forecasts")


def validate_call(
    call: Any,
    index: int,
    allowed_refs: set[str],
    problem_ids: set[str],
    system_ids: set[str],
    feature_ids: set[str],
    feature_systems: dict[str, str],
    project_root: Path,
    errors: list[str],
) -> None:
    prefix = f"proposed_skill_calls[{index}]"
    row = require_object_fields(call, CALL_FIELDS, prefix, errors, optional={"area_id"})
    require_nonempty_fields(
        row,
        {"call_id", "title", "skill_ref", "expected_artifact", "current_alternative", "why_now"},
        prefix,
        errors,
    )
    skill_ref = str(row.get("skill_ref") or "").strip()
    if skill_ref not in allowed_refs:
        errors.append(f"{prefix}.skill_ref must be configured in farplane/harness.yaml#planning.skill_refs")
        contract = None
    else:
        contract, contract_error = planning_contract(project_root, skill_ref)
        if contract_error:
            errors.append(f"{prefix}.skill_ref: {contract_error}")

    arguments = row.get("arguments")
    if not isinstance(arguments, dict):
        errors.append(f"{prefix}.arguments must be an object")
        arguments = {}
    if contract:
        required = {str(item).strip() for item in contract["required_arguments"]}
        missing = sorted(required - set(arguments))
        extra = sorted(set(arguments) - required)
        if missing:
            errors.append(f"{prefix}.arguments is missing planner-required arguments: {', '.join(missing)}")
        if extra:
            errors.append(f"{prefix}.arguments contains non-required arguments: {', '.join(extra)}")
        for name in sorted(required & set(arguments)):
            if not concretely_bound(arguments[name]):
                errors.append(f"{prefix}.arguments.{name} must be concretely bound")

    strategic_names = {"problem_ref", "system_ref", "feature_refs"}
    if strategic_names & set(arguments):
        if not strategic_names <= set(arguments):
            missing_strategic = sorted(strategic_names - set(arguments))
            errors.append(f"{prefix}.arguments is missing strategic refs: {', '.join(missing_strategic)}")
        else:
            problem_ref = arguments.get("problem_ref")
            system_ref = arguments.get("system_ref")
            feature_refs = arguments.get("feature_refs")
            if problem_ref not in problem_ids:
                errors.append(f"{prefix}.arguments.problem_ref must name a configured stable problem")
            if system_ref not in system_ids:
                errors.append(f"{prefix}.arguments.system_ref must name a canonical system")
            if not isinstance(feature_refs, list) or not feature_refs or not all(
                isinstance(ref, str) and ref.strip() for ref in feature_refs
            ):
                errors.append(f"{prefix}.arguments.feature_refs must be a non-empty list of refs")
            else:
                unknown_features = sorted(set(feature_refs) - feature_ids)
                if unknown_features:
                    errors.append(
                        f"{prefix}.arguments.feature_refs must name canonical features: "
                        + ", ".join(unknown_features)
                    )
                incoherent_features = sorted(
                    ref for ref in feature_refs
                    if feature_systems.get(ref) and feature_systems[ref] != system_ref
                )
                if incoherent_features:
                    errors.append(
                        f"{prefix}.arguments.feature_refs must belong to system_ref: "
                        + ", ".join(incoherent_features)
                    )

    evidence = row.get("evidence_refs")
    if not isinstance(evidence, list) or not evidence or not all(nonempty(ref) for ref in evidence):
        errors.append(f"{prefix}.evidence_refs must be a non-empty list of refs")

    validate_objective(row.get("objective_contribution"), f"{prefix}.objective_contribution", errors)

    lifecycle = require_object_fields(
        row.get("lifecycle"),
        {"status", "depends_on", "human_gate"},
        f"{prefix}.lifecycle",
        errors,
        optional={"due_at"},
    )
    if lifecycle.get("status") != "todo":
        errors.append(f"{prefix}.lifecycle.status must be todo")
    if not isinstance(lifecycle.get("depends_on"), list):
        errors.append(f"{prefix}.lifecycle.depends_on must be a list")
    gate = lifecycle.get("human_gate")
    if gate != "none" and not (
        isinstance(gate, list) and len(gate) == 2 and all(nonempty(item) for item in gate)
    ):
        errors.append(f"{prefix}.lifecycle.human_gate must be none or [tag, reason]")
    if "due_at" in lifecycle and not is_timezone_bearing_iso_datetime(lifecycle["due_at"]):
        errors.append(f"{prefix}.lifecycle.due_at must be a timezone-bearing ISO-8601 timestamp")

    proof = require_object_fields(row.get("proof"), {"success", "falsifier"}, f"{prefix}.proof", errors)
    require_nonempty_fields(proof, {"success", "falsifier"}, f"{prefix}.proof", errors)

    dedupe = require_object_fields(
        row.get("dedupe"), {"compared_against", "decision"}, f"{prefix}.dedupe", errors
    )
    if not isinstance(dedupe.get("compared_against"), list):
        errors.append(f"{prefix}.dedupe.compared_against must be a list")
    if dedupe.get("decision") not in DEDUPE_DECISIONS:
        errors.append(f"{prefix}.dedupe.decision must be novel or materially_distinct")

    ranking_fields = {"reason", "confidence", "time_to_signal", "cost", "risk", "human_load", "interference"}
    ranking = require_object_fields(row.get("ranking"), ranking_fields, f"{prefix}.ranking", errors)
    require_nonempty_fields(ranking, ranking_fields, f"{prefix}.ranking", errors)
    if ranking.get("confidence") not in CONFIDENCE_LEVELS:
        errors.append(f"{prefix}.ranking.confidence must be low, medium, or high")


def validate_wave_response(payload: Any, project_root: Path | None = None) -> list[str]:
    if not isinstance(payload, dict):
        return ["wave response must be an object"]
    project_root = (project_root or Path(__file__).resolve().parents[3]).resolve()
    errors: list[str] = []

    missing = sorted(ROOT_FIELDS - set(payload))
    extra = sorted(set(payload) - ROOT_FIELDS)
    if missing:
        errors.append(f"response is missing required fields: {', '.join(missing)}")
    if extra:
        errors.append(f"response contains unsupported fields: {', '.join(extra)}")
    legacy = find_legacy_fields(payload)
    if legacy:
        errors.append("response contains retired lane/card/spec/workflow fields: " + ", ".join(legacy))

    try:
        harness = read_yaml(project_root / "farplane" / "harness.yaml")
        configured = harness.get("planning", {}).get("skill_refs")
        if not isinstance(configured, list) or not all(nonempty(ref) for ref in configured):
            raise ValueError("farplane/harness.yaml#planning.skill_refs must be a list of skill refs")
        allowed_refs = {str(ref).strip() for ref in configured}
        identity = harness.get("identity") if isinstance(harness.get("identity"), dict) else {}
        raw_problems = identity.get("problems")
        problem_ids = {
            str(row["id"]).strip()
            for row in raw_problems if isinstance(row, dict) and nonempty(row.get("id"))
        } if isinstance(raw_problems, list) else set()
        systems_registry = project_root / "docs" / "systems" / "registry.jsonl"
        features_registry = project_root / "docs" / "features" / "registry.jsonl"
        system_ids = registry_ids(systems_registry)
        feature_ids = registry_ids(features_registry)
        feature_systems = feature_system_ids(features_registry)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        errors.append(f"cannot resolve planner skill allowlist: {exc}")
        allowed_refs = set()
        problem_ids = set()
        system_ids = set()
        feature_ids = set()
        feature_systems = {}

    for skill_ref in sorted(allowed_refs):
        _, contract_error = planning_contract(project_root, skill_ref)
        if contract_error:
            errors.append(f"configured skill {skill_ref}: {contract_error}")

    for field in ("global_query_receipt",):
        if not isinstance(payload.get(field), dict):
            errors.append(f"{field} must be an object")
    for field in ("skill_receipts", "progressive_queries", "rejections"):
        if not isinstance(payload.get(field), list):
            errors.append(f"{field} must be a list")

    diagnosis = require_object_fields(
        payload.get("diagnosis"),
        {"problem_context", "objective_movement", "wave_size", "dogfood_role", "hard_guard"},
        "diagnosis",
        errors,
    )
    if not isinstance(diagnosis.get("problem_context"), list):
        errors.append("diagnosis.problem_context must be a list")
    if not isinstance(diagnosis.get("objective_movement"), list):
        errors.append("diagnosis.objective_movement must be a list")
    wave_size = diagnosis.get("wave_size")
    if isinstance(wave_size, bool) or not isinstance(wave_size, int) or wave_size < 0:
        errors.append("diagnosis.wave_size must be a non-negative integer")
        wave_size = 0
    if diagnosis.get("dogfood_role") not in {"current_context_only", "not_supplied"}:
        errors.append("diagnosis.dogfood_role must be current_context_only or not_supplied")
    if not isinstance(diagnosis.get("hard_guard"), dict):
        errors.append("diagnosis.hard_guard must be an object")

    calls = payload.get("proposed_skill_calls")
    if not isinstance(calls, list):
        errors.append("proposed_skill_calls must be a list")
        calls = []
    for index, call in enumerate(calls):
        validate_call(
            call, index, allowed_refs, problem_ids, system_ids, feature_ids,
            feature_systems, project_root, errors
        )

    call_ids = [str(call.get("call_id") or "").strip() for call in calls if isinstance(call, dict)]
    if len(call_ids) != len(set(call_ids)):
        errors.append("proposed_skill_calls call_ids must be unique")
    fingerprints: set[str] = set()
    for call in calls:
        if not isinstance(call, dict):
            continue
        fingerprint = json.dumps(
            {key: value for key, value in call.items() if key not in {"call_id", "title", "ranking"}},
            sort_keys=True,
            separators=(",", ":"),
        )
        if fingerprint in fingerprints:
            errors.append("proposed_skill_calls must not contain duplicate semantic calls")
            break
        fingerprints.add(fingerprint)

    for index, call in enumerate(calls):
        if not isinstance(call, dict):
            continue
        outside = {key: value for key, value in payload.items() if key != "proposed_skill_calls"}
        if contains_equal_object(outside, call):
            errors.append(f"proposed_skill_calls[{index}] is repeated outside the canonical call list")

    decision = require_object_fields(
        payload.get("decision"),
        {
            "admitted_call_ids",
            "source_gaps",
            "human_request",
            "unused_capacity_reason",
            "validation_receipt",
            "no_materialization_receipt",
        },
        "decision",
        errors,
    )
    admitted = decision.get("admitted_call_ids")
    if not isinstance(admitted, list) or not all(nonempty(item) for item in admitted):
        errors.append("decision.admitted_call_ids must be a list of call IDs")
        admitted = []
    if len(admitted) != len(set(admitted)):
        errors.append("decision.admitted_call_ids must be unique")
    unknown = sorted(set(admitted) - set(call_ids))
    if unknown:
        errors.append("decision.admitted_call_ids contains unknown call IDs: " + ", ".join(unknown))
    if len(admitted) > wave_size:
        errors.append("decision.admitted_call_ids exceeds diagnosis.wave_size")
    if not isinstance(decision.get("source_gaps"), list):
        errors.append("decision.source_gaps must be a list")
    if decision.get("human_request") is not None and not nonempty(decision.get("human_request")):
        errors.append("decision.human_request must be null or non-empty")
    if decision.get("unused_capacity_reason") is not None and not nonempty(decision.get("unused_capacity_reason")):
        errors.append("decision.unused_capacity_reason must be null or non-empty")
    if not isinstance(decision.get("validation_receipt"), dict):
        errors.append("decision.validation_receipt must be an object")
    reasons = [
        bool(payload.get("rejections")),
        bool(decision.get("source_gaps")),
        nonempty(decision.get("human_request")),
        nonempty(decision.get("unused_capacity_reason")),
    ]
    if not admitted and not any(reasons):
        errors.append("an empty wave must name an exact rejection, source gap, human request, or unused-capacity reason")

    receipt = require_object_fields(
        decision.get("no_materialization_receipt"),
        {"tickets_written", "materialized", "executed", "owner"},
        "decision.no_materialization_receipt",
        errors,
    )
    receipt_is_exact = (
        type(receipt.get("tickets_written")) is int
        and receipt.get("tickets_written") == 0
        and type(receipt.get("materialized")) is bool
        and receipt.get("materialized") is False
        and type(receipt.get("executed")) is bool
        and receipt.get("executed") is False
        and receipt.get("owner") == "pulse-update"
    )
    if receipt and not receipt_is_exact:
        errors.append("decision.no_materialization_receipt must prove zero writes, materialization, or execution and name pulse-update")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("wave_file")
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args()
    try:
        payload = json.loads(Path(args.wave_file).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "errors": [str(exc)]}, indent=2, sort_keys=True))
        return 1
    errors = validate_wave_response(payload, args.project_root)
    print(json.dumps({"ok": not errors, "errors": errors}, indent=2, sort_keys=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
