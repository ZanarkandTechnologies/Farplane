#!/usr/bin/env python3
"""Validate content-impl-plan's owner-separated production program."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT_FIELDS = {"schema_version", "content_kind", "creative_input_bundle", "advisor_actions"}
BUNDLE_FIELDS = {
    "brand_kit_snapshot", "tasty_pack_ref", "selected_element_ids",
    "conflict_decisions", "icp", "platform", "proof", "proof_limits",
    "production_policy",
}
ACTION_FIELDS = {"owner", "accepted_inputs", "authored_output", "acceptance_or_blocker", "next_handoff"}
VERDICT_FIELDS = {"state", "evidence_refs", "reason"}
REQUIRED_VISUAL_OWNERS = {"storyboard", "asset-advisor", "editing-advisor", "remotion", "review"}
UPSTREAM_RENDER_OWNERS = {"storyboard", "asset-advisor", "editing-advisor"}
BRAND_SNAPSHOT_FIELDS = {"id", "kit_revision", "prompt_revision", "prompt", "elements", "resolution_state"}


def _nonempty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _exact_fields(value: Any, fields: set[str], path: str, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{path} must be an object")
        return {}
    missing = sorted(fields - set(value))
    extra = sorted(set(value) - fields)
    if missing:
        errors.append(f"{path} missing fields: {', '.join(missing)}")
    if extra:
        errors.append(f"{path} unsupported fields: {', '.join(extra)}")
    return value


def validate(payload: Any) -> list[str]:
    errors: list[str] = []
    root = _exact_fields(payload, ROOT_FIELDS, "program", errors)
    if root.get("schema_version") != "1.0":
        errors.append("program.schema_version must be 1.0")
    if not _nonempty_text(root.get("content_kind")):
        errors.append("program.content_kind must be a non-empty string")

    bundle = _exact_fields(root.get("creative_input_bundle"), BUNDLE_FIELDS, "creative_input_bundle", errors)
    brand = bundle.get("brand_kit_snapshot")
    if not isinstance(brand, dict) or not brand:
        errors.append("creative_input_bundle.brand_kit_snapshot must be a resolved non-empty object")
    else:
        missing_brand = sorted(BRAND_SNAPSHOT_FIELDS - set(brand))
        if missing_brand:
            errors.append("creative_input_bundle.brand_kit_snapshot missing fields: " + ", ".join(missing_brand))
        if brand.get("resolution_state") != "resolved":
            errors.append("creative_input_bundle.brand_kit_snapshot.resolution_state must be resolved")
        for field in ("id", "prompt"):
            if not _nonempty_text(brand.get(field)):
                errors.append(f"creative_input_bundle.brand_kit_snapshot.{field} must be a non-empty string")
        for field in ("kit_revision", "prompt_revision"):
            value = brand.get(field)
            if isinstance(value, bool) or not isinstance(value, int) or value < 1:
                errors.append(f"creative_input_bundle.brand_kit_snapshot.{field} must be a positive integer")
        elements = brand.get("elements")
        if not isinstance(elements, list) or not elements or not all(_nonempty_text(item) for item in elements):
            errors.append("creative_input_bundle.brand_kit_snapshot.elements must be a non-empty list of IDs")
    for field in ("icp", "platform"):
        if not _nonempty_text(bundle.get(field)):
            errors.append(f"creative_input_bundle.{field} must be a non-empty string")
    for field in ("proof", "production_policy"):
        if not isinstance(bundle.get(field), dict) or not bundle.get(field):
            errors.append(f"creative_input_bundle.{field} must be a non-empty object")
    for field in ("selected_element_ids", "conflict_decisions", "proof_limits"):
        if not isinstance(bundle.get(field), list):
            errors.append(f"creative_input_bundle.{field} must be a list")
        elif not all(_nonempty_text(item) for item in bundle[field]):
            errors.append(f"creative_input_bundle.{field} must contain only non-empty strings")
    selected_ids = bundle.get("selected_element_ids")
    if isinstance(selected_ids, list) and not selected_ids:
        errors.append("creative_input_bundle.selected_element_ids must not be empty for a resolved Brand Kit")
    tasty_pack_ref = bundle.get("tasty_pack_ref")
    if tasty_pack_ref is not None and not _nonempty_text(tasty_pack_ref):
        errors.append("creative_input_bundle.tasty_pack_ref must be null or a non-empty ref")
    if "style_profile" in bundle:
        errors.append("creative_input_bundle.style_profile is not allowed on the Brand Kit/Tasty path")

    actions = root.get("advisor_actions")
    if not isinstance(actions, list):
        errors.append("program.advisor_actions must be a list")
        return errors

    states: dict[str, str] = {}
    action_by_owner: dict[str, dict[str, Any]] = {}
    positions: dict[str, int] = {}
    for index, raw in enumerate(actions):
        path = f"advisor_actions[{index}]"
        action = _exact_fields(raw, ACTION_FIELDS, path, errors)
        owner = action.get("owner")
        if not _nonempty_text(owner):
            errors.append(f"{path}.owner must be a non-empty string")
            continue
        if any(token in owner for token in ("/", ",", "->", " + ")):
            errors.append(f"{path}.owner must name exactly one owner")
        if owner in states:
            errors.append(f"{path}.owner duplicates {owner}")
        inputs = action.get("accepted_inputs")
        if not isinstance(inputs, list) or not inputs or not all(_nonempty_text(item) for item in inputs):
            errors.append(f"{path}.accepted_inputs must be a non-empty list of refs")
        if not _nonempty_text(action.get("authored_output")):
            errors.append(f"{path}.authored_output must be a non-empty ref")
        if not _nonempty_text(action.get("next_handoff")):
            errors.append(f"{path}.next_handoff must be a non-empty string")
        verdict = _exact_fields(action.get("acceptance_or_blocker"), VERDICT_FIELDS, f"{path}.acceptance_or_blocker", errors)
        state = verdict.get("state")
        if state not in {"accepted", "blocked"}:
            errors.append(f"{path}.acceptance_or_blocker.state must be accepted or blocked")
        refs = verdict.get("evidence_refs")
        if not isinstance(refs, list) or not all(_nonempty_text(ref) for ref in refs):
            errors.append(f"{path}.acceptance_or_blocker.evidence_refs must be a list of refs")
        if state == "accepted" and not refs:
            errors.append(f"{path} accepted state requires evidence_refs")
        if not _nonempty_text(verdict.get("reason")):
            errors.append(f"{path}.acceptance_or_blocker.reason must be non-empty")
        states[owner] = str(state)
        action_by_owner[owner] = action
        positions[owner] = index

    missing_owners = sorted(REQUIRED_VISUAL_OWNERS - set(states))
    if missing_owners:
        errors.append("program is missing required visual owners: " + ", ".join(missing_owners))
    required_order = ("storyboard", "asset-advisor", "editing-advisor", "remotion", "review")
    present_order = [positions[owner] for owner in required_order if owner in positions]
    if present_order != sorted(present_order):
        errors.append("program visual owners are out of dependency order")
    if states.get("remotion") == "accepted":
        blocked = sorted(owner for owner in UPSTREAM_RENDER_OWNERS if states.get(owner) != "accepted")
        if blocked:
            errors.append("remotion cannot be accepted before accepted upstream owners: " + ", ".join(blocked))
        required_inputs = {
            str(action_by_owner[owner].get("authored_output") or "")
            for owner in UPSTREAM_RENDER_OWNERS if owner in action_by_owner
        }
        remotion_inputs = set(action_by_owner["remotion"].get("accepted_inputs") or [])
        missing_inputs = sorted(required_inputs - remotion_inputs)
        if missing_inputs:
            errors.append("remotion accepted_inputs missing upstream outputs: " + ", ".join(missing_inputs))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("program", type=Path)
    args = parser.parse_args()
    errors = validate(json.loads(args.program.read_text(encoding="utf-8")))
    print(json.dumps({"ok": not errors, "errors": errors}, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
