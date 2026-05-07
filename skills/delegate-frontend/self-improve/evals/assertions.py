#!/usr/bin/env python3
"""Deterministic binary assertions for delegate-frontend self-improvement evals."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class AssertionResult:
    name: str
    passed: bool
    message: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def add_result(results: list[AssertionResult], name: str, passed: bool, message: str) -> None:
    results.append(AssertionResult(name=name, passed=passed, message=message))


def numeric(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def phase_count(qa: dict[str, Any]) -> int:
    phases = {
        checkpoint.get("debug", {}).get("phase")
        for checkpoint in qa.get("checkpoints", [])
        if isinstance(checkpoint.get("debug"), dict) and checkpoint.get("debug", {}).get("phase")
    }
    return len(phases)


def max_changed_ratio(qa: dict[str, Any]) -> float:
    ratios = [float(item.get("changedRatio", 0)) for item in qa.get("screenshotDiffs", [])]
    return max(ratios) if ratios else 0.0


def summary_from(spec: dict[str, Any], output: dict[str, Any]) -> dict[str, Any]:
    if spec.get("output_key"):
        value = output.get(str(spec["output_key"]))
    else:
        value = spec.get("summary")
    return value if isinstance(value, dict) else {}


def evaluate_scroll_qa(case: dict[str, Any], output: dict[str, Any], results: list[AssertionResult]) -> None:
    for spec in as_list(case.get("scroll_qa")):
        label = str(spec.get("label", "scroll_qa"))
        qa = summary_from(spec, output)
        add_result(results, f"{label}:qa_summary_present", bool(qa), "QA summary present" if qa else "QA summary missing")
        if not qa:
            continue
        score = qa.get("score", {})

        if "verdict" in spec:
            expected = str(spec["verdict"])
            actual = str(qa.get("verdict"))
            add_result(
                results,
                f"{label}:verdict:{expected}",
                actual == expected,
                f"verdict {actual}, expected {expected}",
            )

        if "terminal_verdict" in spec:
            expected = str(spec["terminal_verdict"])
            actual = str(qa.get("terminalVerdict", "PASS" if score.get("terminalFinalReady") else "FAIL"))
            add_result(
                results,
                f"{label}:terminal_verdict:{expected}",
                actual == expected,
                f"terminalVerdict {actual}, expected {expected}",
            )

        for key in as_list(spec.get("require_score_true")):
            passed = bool(score.get(str(key)))
            add_result(
                results,
                f"{label}:score_true:{key}",
                passed,
                f"{key} is true" if passed else f"{key} is not true",
            )

        for key, minimum in dict(spec.get("min_score", {})).items():
            actual = float(score.get(str(key), 0))
            passed = actual >= float(minimum)
            add_result(
                results,
                f"{label}:min_score:{key}",
                passed,
                f"{key}={actual} >= {minimum}" if passed else f"{key}={actual} < {minimum}",
            )

        if spec.get("require_media_or_debug"):
            passed = bool(score.get("hasMediaScrub") or score.get("hasDebugScrub"))
            add_result(
                results,
                f"{label}:media_or_debug_scrub",
                passed,
                "media or debug scrub present" if passed else "no media/debug scrub signal",
            )

        if "min_phase_count" in spec:
            actual = phase_count(qa)
            minimum = int(spec["min_phase_count"])
            add_result(
                results,
                f"{label}:min_phase_count",
                actual >= minimum,
                f"phase_count={actual} >= {minimum}" if actual >= minimum else f"phase_count={actual} < {minimum}",
            )

        if "min_max_changed_ratio" in spec:
            actual = max_changed_ratio(qa)
            minimum = float(spec["min_max_changed_ratio"])
            add_result(
                results,
                f"{label}:min_max_changed_ratio",
                actual >= minimum,
                f"max_changed_ratio={actual:.5f} >= {minimum}" if actual >= minimum else f"max_changed_ratio={actual:.5f} < {minimum}",
            )


def evaluate_manifest(case: dict[str, Any], output: dict[str, Any], results: list[AssertionResult]) -> None:
    for spec in as_list(case.get("asset_manifest")):
        label = str(spec.get("label", "asset_manifest"))
        manifest = summary_from(spec, output)
        add_result(results, f"{label}:manifest_summary_present", bool(manifest), "manifest summary present" if manifest else "manifest summary missing")
        if not manifest:
            continue
        if "asset_strategy_not" in spec:
            blocked = {str(item) for item in as_list(spec["asset_strategy_not"])}
            actual = str(manifest.get("asset_strategy", ""))
            passed = actual not in blocked
            add_result(
                results,
                f"{label}:asset_strategy_not",
                passed,
                f"asset_strategy={actual} accepted" if passed else f"asset_strategy={actual} is blocked",
            )
        if "min_assets" in spec:
            assets = manifest.get("assets", [])
            actual = len(assets) if isinstance(assets, list) else 0
            minimum = int(spec["min_assets"])
            add_result(
                results,
                f"{label}:min_assets",
                actual >= minimum,
                f"assets={actual} >= {minimum}" if actual >= minimum else f"assets={actual} < {minimum}",
            )
        if "min_generated_or_rendered_count" in spec:
            actual = int(numeric(manifest.get("generated_or_rendered_count"), 0))
            minimum = int(spec["min_generated_or_rendered_count"])
            add_result(
                results,
                f"{label}:min_generated_or_rendered_count",
                actual >= minimum,
                f"generated_or_rendered_count={actual} >= {minimum}" if actual >= minimum else f"generated_or_rendered_count={actual} < {minimum}",
            )
        if "max_broken_refs" in spec:
            actual = int(numeric(manifest.get("broken_refs"), 0))
            maximum = int(spec["max_broken_refs"])
            add_result(
                results,
                f"{label}:max_broken_refs",
                actual <= maximum,
                f"broken_refs={actual} <= {maximum}" if actual <= maximum else f"broken_refs={actual} > {maximum}",
            )
        if "max_unsafe_refs" in spec:
            actual = int(numeric(manifest.get("unsafe_refs"), 0))
            maximum = int(spec["max_unsafe_refs"])
            add_result(
                results,
                f"{label}:max_unsafe_refs",
                actual <= maximum,
                f"unsafe_refs={actual} <= {maximum}" if actual <= maximum else f"unsafe_refs={actual} > {maximum}",
            )
        for key in as_list(spec.get("require_true")):
            passed = bool(manifest.get(str(key)))
            add_result(
                results,
                f"{label}:require_true:{key}",
                passed,
                f"{key} is true" if passed else f"{key} is not true",
            )
        if spec.get("require_source_prompts"):
            actual = int(numeric(manifest.get("source_prompt_count"), 0))
            minimum = int(numeric(manifest.get("generated_or_rendered_count"), 1))
            passed = actual >= minimum if minimum > 0 else actual >= 1
            add_result(
                results,
                f"{label}:source_prompts_present",
                passed,
                f"source_prompt_count={actual} >= {minimum}" if passed else f"source_prompt_count={actual} < {minimum}",
            )


def evaluate_spec(case: dict[str, Any], output: dict[str, Any], results: list[AssertionResult]) -> None:
    for spec in as_list(case.get("spec")):
        label = str(spec.get("label", "spec"))
        summary = summary_from(spec, output)
        add_result(results, f"{label}:spec_summary_present", bool(summary), "spec summary present" if summary else "spec summary missing")
        if not summary:
            continue
        allowed = {str(item) for item in as_list(spec.get("status_in"))}
        if allowed:
            actual = str(summary.get("status"))
            passed = actual in allowed
            add_result(
                results,
                f"{label}:status_in",
                passed,
                f"status={actual} accepted" if passed else f"status={actual} not in {sorted(allowed)}",
            )
        for field in as_list(spec.get("require_nonempty")):
            value = summary.get(str(field))
            passed = bool(str(value or "").strip())
            add_result(
                results,
                f"{label}:nonempty:{field}",
                passed,
                f"{field} present" if passed else f"{field} missing",
            )
        for field, minimum in dict(spec.get("min_fields", {})).items():
            actual = numeric(summary.get(str(field)), 0)
            passed = actual >= float(minimum)
            add_result(
                results,
                f"{label}:min_field:{field}",
                passed,
                f"{field}={actual:g} >= {minimum}" if passed else f"{field}={actual:g} < {minimum}",
            )


def evaluate_phase_completion(case: dict[str, Any], output: dict[str, Any], results: list[AssertionResult]) -> None:
    for spec in as_list(case.get("phase_completion")):
        label = str(spec.get("label", "phase_completion"))
        summary = summary_from(spec, output)
        add_result(results, f"{label}:phase_summary_present", bool(summary), "phase summary present" if summary else "phase summary missing")
        if not summary:
            continue
        allowed = {str(item) for item in as_list(spec.get("status_in"))}
        if allowed:
            actual = str(summary.get("status"))
            passed = actual in allowed
            add_result(
                results,
                f"{label}:status_in",
                passed,
                f"status={actual} accepted" if passed else f"status={actual} not in {sorted(allowed)}",
            )
        if spec.get("require_owned_outputs"):
            outputs = summary.get("owned_outputs")
            passed = isinstance(outputs, list) and len(outputs) > 0
            add_result(
                results,
                f"{label}:owned_outputs_present",
                passed,
                "owned outputs recorded" if passed else "owned outputs missing",
            )
        if spec.get("require_handoff"):
            passed = bool(str(summary.get("handoff_path", "")).strip())
            add_result(
                results,
                f"{label}:handoff_present",
                passed,
                "handoff path present" if passed else "handoff path missing",
            )
        required_sections = as_list(spec.get("require_handoff_sections"))
        if spec.get("require_handoff_first_write"):
            required_sections.append("first_write_evidence")
        handoff_contract = summary.get("handoff_contract", {})
        if not isinstance(handoff_contract, dict):
            handoff_contract = {}
        for section in required_sections:
            section_name = str(section)
            passed = bool(handoff_contract.get(section_name))
            add_result(
                results,
                f"{label}:handoff_section:{section_name}",
                passed,
                f"{section_name} section present" if passed else f"{section_name} section missing",
            )
        allowed_first_write = {str(item) for item in as_list(spec.get("first_write_status_in"))}
        if allowed_first_write:
            actual = str(summary.get("first_write_status"))
            passed = actual in allowed_first_write
            add_result(
                results,
                f"{label}:first_write_status_in",
                passed,
                f"first_write_status={actual} accepted" if passed else f"first_write_status={actual} not in {sorted(allowed_first_write)}",
            )


def evaluate_visual_geometry(case: dict[str, Any], output: dict[str, Any], results: list[AssertionResult]) -> None:
    for spec in as_list(case.get("visual_geometry")):
        label = str(spec.get("label", "visual_geometry"))
        summary = summary_from(spec, output)
        add_result(results, f"{label}:geometry_summary_present", bool(summary), "geometry summary present" if summary else "geometry summary missing")
        if not summary:
            continue
        for field, minimum in dict(spec.get("min_fields", {})).items():
            actual = numeric(summary.get(str(field)), 0)
            passed = actual >= float(minimum)
            add_result(
                results,
                f"{label}:min_field:{field}",
                passed,
                f"{field}={actual:g} >= {minimum}" if passed else f"{field}={actual:g} < {minimum}",
            )
        for field, maximum in dict(spec.get("max_fields", {})).items():
            actual = numeric(summary.get(str(field)), 0)
            passed = actual <= float(maximum)
            add_result(
                results,
                f"{label}:max_field:{field}",
                passed,
                f"{field}={actual:g} <= {maximum}" if passed else f"{field}={actual:g} > {maximum}",
            )
        for field in as_list(spec.get("require_false")):
            passed = not bool(summary.get(str(field)))
            add_result(
                results,
                f"{label}:require_false:{field}",
                passed,
                f"{field} is false" if passed else f"{field} is not false",
            )
        for field, allowed_values in dict(spec.get("field_in", {})).items():
            allowed = {str(item) for item in as_list(allowed_values)}
            actual = str(summary.get(str(field)))
            passed = actual in allowed
            add_result(
                results,
                f"{label}:field_in:{field}",
                passed,
                f"{field}={actual} accepted" if passed else f"{field}={actual} not in {sorted(allowed)}",
            )


def evaluate_startup(case: dict[str, Any], output: dict[str, Any], results: list[AssertionResult]) -> None:
    for spec in as_list(case.get("startup")):
        label = str(spec.get("label", "startup"))
        summary = summary_from(spec, output)
        add_result(results, f"{label}:startup_summary_present", bool(summary), "startup summary present" if summary else "startup summary missing")
        if not summary:
            continue
        allowed = {str(item) for item in as_list(spec.get("status_in"))}
        if allowed:
            actual = str(summary.get("status"))
            passed = actual in allowed
            add_result(
                results,
                f"{label}:status_in",
                passed,
                f"status={actual} accepted" if passed else f"status={actual} not in {sorted(allowed)}",
            )
        if "min_session_files" in spec:
            actual = int(numeric(summary.get("session_files"), 0))
            minimum = int(spec["min_session_files"])
            add_result(
                results,
                f"{label}:min_session_files",
                actual >= minimum,
                f"session_files={actual} >= {minimum}" if actual >= minimum else f"session_files={actual} < {minimum}",
            )


def evaluate_compiled_prompt(case: dict[str, Any], output: dict[str, Any], results: list[AssertionResult]) -> None:
    for spec in as_list(case.get("compiled_prompt")):
        label = str(spec.get("label", "compiled_prompt"))
        summary = summary_from(spec, output)
        add_result(results, f"{label}:prompt_summary_present", bool(summary), "prompt summary present" if summary else "prompt summary missing")
        if not summary:
            continue
        if "phase" in spec:
            expected = str(spec["phase"])
            actual = str(summary.get("phase"))
            add_result(
                results,
                f"{label}:phase:{expected}",
                actual == expected,
                f"phase={actual}, expected {expected}",
            )
        if "min_owned_outputs" in spec:
            outputs = summary.get("owned_outputs", [])
            actual = len(outputs) if isinstance(outputs, list) else 0
            minimum = int(spec["min_owned_outputs"])
            add_result(
                results,
                f"{label}:min_owned_outputs",
                actual >= minimum,
                f"owned_outputs={actual} >= {minimum}" if actual >= minimum else f"owned_outputs={actual} < {minimum}",
            )
        for key in as_list(spec.get("require_true")):
            passed = bool(summary.get(str(key)))
            add_result(
                results,
                f"{label}:require_true:{key}",
                passed,
                f"{key} is true" if passed else f"{key} is not true",
            )


def evaluate_first_write(case: dict[str, Any], output: dict[str, Any], results: list[AssertionResult]) -> None:
    for spec in as_list(case.get("first_write")):
        label = str(spec.get("label", "first_write"))
        first_write = summary_from(spec, output)
        add_result(results, f"{label}:first_write_summary_present", bool(first_write), "first_write summary present" if first_write else "first_write summary missing")
        if not first_write:
            continue
        allowed = {str(item) for item in as_list(spec.get("status_in"))}
        if allowed:
            actual = str(first_write.get("status"))
            passed = actual in allowed
            add_result(
                results,
                f"{label}:status_in",
                passed,
                f"status={actual} accepted" if passed else f"status={actual} not in {sorted(allowed)}",
            )
        if spec.get("require_expected_outputs"):
            outputs = first_write.get("expected_outputs")
            passed = isinstance(outputs, list) and len(outputs) > 0
            add_result(
                results,
                f"{label}:expected_outputs_present",
                passed,
                "expected outputs recorded" if passed else "expected outputs missing",
            )


def evaluate_text_output(case: dict[str, Any], output: dict[str, Any], results: list[AssertionResult]) -> None:
    text = str(output.get("output", ""))
    candidate_text = str(output.get("candidate_text", ""))
    if output.get("missing_candidate_output"):
        add_result(results, "candidate_output_present", False, "missing candidate output row")
    else:
        add_result(results, "candidate_output_present", True, "candidate output row present")
    for expected in as_list(case.get("must_contain")):
        add_result(
            results,
            f"must_contain:{expected}",
            str(expected) in text,
            "found required text" if str(expected) in text else "missing required text",
        )
    for forbidden in as_list(case.get("must_not_contain")):
        add_result(
            results,
            f"must_not_contain:{forbidden}",
            str(forbidden) not in text,
            "forbidden text absent" if str(forbidden) not in text else "forbidden text present",
        )
    for expected in as_list(case.get("candidate_must_contain")):
        add_result(
            results,
            f"candidate_must_contain:{expected}",
            str(expected) in candidate_text,
            "found candidate text" if str(expected) in candidate_text else "missing candidate text",
        )
    for forbidden in as_list(case.get("candidate_must_not_contain")):
        add_result(
            results,
            f"candidate_must_not_contain:{forbidden}",
            str(forbidden) not in candidate_text,
            "forbidden candidate text absent" if str(forbidden) not in candidate_text else "forbidden candidate text present",
        )


def evaluate_case(case: dict[str, Any], output: dict[str, Any]) -> list[AssertionResult]:
    results: list[AssertionResult] = []
    evaluate_text_output(case, output, results)
    evaluate_spec(case, output, results)
    evaluate_scroll_qa(case, output, results)
    evaluate_manifest(case, output, results)
    evaluate_phase_completion(case, output, results)
    evaluate_visual_geometry(case, output, results)
    evaluate_startup(case, output, results)
    evaluate_compiled_prompt(case, output, results)
    evaluate_first_write(case, output, results)
    if not results:
        add_result(results, "has_eval_definition", False, "case has no assertions")
    return results
