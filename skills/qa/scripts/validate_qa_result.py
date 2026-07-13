#!/usr/bin/env python3
"""Validate the canonical Farplane QA result receipt."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


TOP_LEVEL_FIELDS = {
    "schema_version",
    "ticket_id",
    "phase",
    "proof_type",
    "runtime_target",
    "proof_policy",
    "verdict",
    "summary",
    "gate_results",
    "best_evidence",
    "artifacts",
    "blockers",
    "residual_risk",
    "judgment_receipts",
    "learning",
}
PROOF_TYPES = {"cli", "api", "browser", "ui", "artifact", "agent"}
VERDICTS = {"pass", "revise", "fail", "blocked", "not_provable"}
GATE_FIELDS = {"contract", "mechanism", "journey", "adversarial", "receipt"}
GATE_VERDICTS = {"pass", "fail", "blocked"}
LEARNING_OUTCOMES = {"ticket_only", "cookbook_update", "instrumentation_ticket"}
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
TICKET_ID = re.compile(r"^TASK-\d{4,}$")
JUDGMENT_PATH_MARKERS = {
    "visual-qa": "visual-qa",
    "agent-qa-test": "agent-qa-test",
    "reviewer": "review",
}


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _string_list(payload: dict[str, Any], field: str, errors: list[str]) -> list[str]:
    value = payload.get(field)
    if not isinstance(value, list) or any(not _nonempty_string(item) for item in value):
        errors.append(f"{field}: expected a list of non-empty strings")
        return []
    if len(value) != len(set(value)):
        errors.append(f"{field}: duplicate paths or entries are not allowed")
    return value


def validate(payload: Any) -> list[str]:
    """Return structural and conditional invariant violations."""

    if not isinstance(payload, dict):
        return ["result: expected a JSON object"]

    errors: list[str] = []
    fields = set(payload)
    missing = sorted(TOP_LEVEL_FIELDS - fields)
    extra = sorted(fields - TOP_LEVEL_FIELDS)
    if missing:
        errors.append(f"result: missing fields: {', '.join(missing)}")
    if extra:
        errors.append(f"result: unknown fields: {', '.join(extra)}")

    if payload.get("schema_version") != "1":
        errors.append('schema_version: expected "1"')
    if not _nonempty_string(payload.get("ticket_id")) or not TICKET_ID.fullmatch(payload["ticket_id"]):
        errors.append("ticket_id: expected TASK- followed by at least four digits")
    if payload.get("phase") != "qa":
        errors.append('phase: expected "qa"')

    proof_type = payload.get("proof_type")
    if proof_type not in PROOF_TYPES:
        errors.append(f"proof_type: expected one of {sorted(PROOF_TYPES)}")
    verdict = payload.get("verdict")
    if verdict not in VERDICTS:
        errors.append(f"verdict: expected one of {sorted(VERDICTS)}")
    if not _nonempty_string(payload.get("proof_policy")):
        errors.append("proof_policy: expected a non-empty string")
    if not _nonempty_string(payload.get("summary")):
        errors.append("summary: expected a non-empty string")

    runtime_target = payload.get("runtime_target")
    if runtime_target is not None and not _nonempty_string(runtime_target):
        errors.append("runtime_target: expected null or a non-empty string")
    if proof_type in {"api", "browser", "ui"} and not _nonempty_string(runtime_target):
        errors.append(f"runtime_target: required for {proof_type} proof")

    gates = payload.get("gate_results")
    if not isinstance(gates, dict):
        errors.append("gate_results: expected an object")
        gates = {}
    else:
        missing_gates = sorted(GATE_FIELDS - set(gates))
        extra_gates = sorted(set(gates) - GATE_FIELDS)
        if missing_gates:
            errors.append(f"gate_results: missing gates: {', '.join(missing_gates)}")
        if extra_gates:
            errors.append(f"gate_results: unknown gates: {', '.join(extra_gates)}")
    for gate, gate_verdict in gates.items():
        if gate_verdict not in GATE_VERDICTS:
            errors.append(f"gate_results.{gate}: expected one of {sorted(GATE_VERDICTS)}")

    artifacts = _string_list(payload, "artifacts", errors)
    blockers = _string_list(payload, "blockers", errors)
    _string_list(payload, "residual_risk", errors)
    judgment_receipts = _string_list(payload, "judgment_receipts", errors)
    if not artifacts:
        errors.append("artifacts: at least one artifact is required")

    best_evidence = payload.get("best_evidence")
    if best_evidence is not None and not _nonempty_string(best_evidence):
        errors.append("best_evidence: expected null or a non-empty artifact path")
    elif _nonempty_string(best_evidence) and best_evidence not in artifacts:
        errors.append("best_evidence: must also appear in artifacts")
    if verdict == "pass" and not _nonempty_string(best_evidence):
        errors.append("best_evidence: a passing result requires a concrete artifact path")
    if verdict == "pass" and proof_type in {"browser", "ui"} and _nonempty_string(best_evidence):
        if Path(best_evidence).suffix.lower() not in IMAGE_SUFFIXES:
            errors.append("best_evidence: browser/ui proof requires an image path")

    if verdict == "pass":
        if blockers:
            errors.append("blockers: a passing result cannot contain blockers")
        if set(gates) == GATE_FIELDS and any(value != "pass" for value in gates.values()):
            errors.append("gate_results: every gate must pass when verdict is pass")
        policy = str(payload.get("proof_policy", "")).lower()
        for judgment, path_marker in JUDGMENT_PATH_MARKERS.items():
            if judgment in policy and not any(path_marker in path.lower() for path in judgment_receipts):
                errors.append(
                    f"judgment_receipts: passing proof policy requires a {judgment} receipt path"
                )
    elif verdict in VERDICTS and not blockers:
        errors.append("blockers: a non-pass result requires at least one blocker")

    learning = payload.get("learning")
    if not isinstance(learning, dict):
        errors.append("learning: expected an object")
    else:
        if set(learning) != {"outcome", "ref"}:
            errors.append("learning: expected exactly outcome and ref")
        outcome = learning.get("outcome")
        ref = learning.get("ref")
        if outcome not in LEARNING_OUTCOMES:
            errors.append(f"learning.outcome: expected one of {sorted(LEARNING_OUTCOMES)}")
        elif outcome == "ticket_only" and ref is not None:
            errors.append("learning.ref: ticket_only requires null")
        elif outcome != "ticket_only" and not _nonempty_string(ref):
            errors.append(f"learning.ref: {outcome} requires a non-empty reference")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result", type=Path)
    args = parser.parse_args()
    try:
        payload = json.loads(args.result.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"{args.result}: {exc}")
        return 1
    errors = validate(payload)
    if errors:
        print("\n".join(f"{args.result}: {error}" for error in errors))
        return 1
    print(f"QA result OK: {args.result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
