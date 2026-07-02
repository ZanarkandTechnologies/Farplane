#!/usr/bin/env python3
"""Validate a Feed Scout daily feed JSON artifact."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REQUIRED_TOP_LEVEL = {
    "schema",
    "schema_version",
    "config_ref",
    "date",
    "generated_at",
    "review_window",
    "summary",
    "groups",
    "items",
}

REQUIRED_ITEM_FIELDS = {
    "actionability",
    "canonical_key",
    "canonical_url",
    "date_basis",
    "discovered_at",
    "embed",
    "entity_group_id",
    "evidence_refs",
    "kind",
    "novelty",
    "platform",
    "published_at",
    "rank",
    "source_id",
    "source_snapshot",
    "summary",
    "title",
    "today_delta",
    "why_care_today",
}

ALLOWED_NOVELTY = {"new_today", "changed_today", "rediscovered", "context_only", "stale"}
DISALLOWED_MAIN_NOVELTY = {"context_only", "stale"}
DISALLOWED_DATE_BASIS = {"observed_at", "observed_at_only", "unknown"}


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    text = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        try:
            parsed = datetime.fromisoformat(f"{value}T00:00:00+00:00")
        except ValueError:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def validate_object(name: str, value: Any, errors: list[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        errors.append(f"{name}: expected object")
        return {}
    return value


def validate_feed(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED_TOP_LEVEL - set(payload))
    if missing:
        errors.append(f"top-level missing fields: {', '.join(missing)}")
    if "excluded_items" in payload:
        errors.append("excluded_items must not be returned in the UI-facing daily feed")

    items = payload.get("items")
    if not isinstance(items, list):
        errors.append("items: expected list")
        return errors

    generated_at = parse_time(payload.get("generated_at"))
    if generated_at is None:
        errors.append("generated_at: expected ISO timestamp")

    for index, raw_item in enumerate(items):
        item = validate_object(f"items[{index}]", raw_item, errors)
        if not item:
            continue

        missing_fields = sorted(REQUIRED_ITEM_FIELDS - set(item))
        if missing_fields:
            errors.append(f"items[{index}]: missing fields: {', '.join(missing_fields)}")

        rank = item.get("rank")
        if not isinstance(rank, int) or rank < 1:
            errors.append(f"items[{index}].rank: expected positive integer")

        novelty = item.get("novelty")
        if novelty not in ALLOWED_NOVELTY:
            errors.append(f"items[{index}].novelty: invalid value {novelty!r}")
        elif novelty in DISALLOWED_MAIN_NOVELTY:
            errors.append(f"items[{index}].novelty: {novelty!r} does not belong in the main daily feed")

        date_basis = item.get("date_basis")
        if date_basis in DISALLOWED_DATE_BASIS:
            errors.append(f"items[{index}].date_basis: {date_basis!r} cannot justify main feed inclusion")

        delta = validate_object(f"items[{index}].today_delta", item.get("today_delta"), errors)
        if delta:
            if not delta.get("kind"):
                errors.append(f"items[{index}].today_delta.kind: required")
            if delta.get("kind") == "no_material_change":
                errors.append(f"items[{index}].today_delta.kind: no_material_change does not belong in the main feed")
            if not delta.get("observed_at"):
                errors.append(f"items[{index}].today_delta.observed_at: required")

        actionability = validate_object(f"items[{index}].actionability", item.get("actionability"), errors)
        if actionability and actionability.get("label") == "ignore":
            errors.append(f"items[{index}].actionability.label: ignore does not belong in the main feed")

        if not isinstance(item.get("source_snapshot"), dict):
            errors.append(f"items[{index}].source_snapshot: expected object")
        if not isinstance(item.get("embed"), dict):
            errors.append(f"items[{index}].embed: expected object")
        if not isinstance(item.get("evidence_refs"), list) or not item.get("evidence_refs"):
            errors.append(f"items[{index}].evidence_refs: expected non-empty list")

        published_at = parse_time(item.get("published_at"))
        if item.get("date_basis") == "source_published_at" and published_at is None:
            errors.append(f"items[{index}].published_at: required when date_basis is source_published_at")

    summary = payload.get("summary")
    if isinstance(summary, dict):
        if summary.get("item_count") != len(items):
            errors.append("summary.item_count does not match len(items)")
        if "interesting_item_count" in summary:
            errors.append("summary.interesting_item_count is redundant; use item_count and item rank")
        if "excluded_item_count" in summary:
            errors.append("summary.excluded_item_count must stay in reports/debug evidence, not the daily feed")
    else:
        errors.append("summary: expected object")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--json", action="store_true", help="Emit machine-readable validation output.")
    args = parser.parse_args()

    try:
        payload = json.loads(args.path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors = [str(exc)]
    else:
        if not isinstance(payload, dict):
            errors = ["root: expected object"]
        else:
            errors = validate_feed(payload)

    result = {"path": str(args.path), "valid": not errors, "errors": errors}
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    elif errors:
        for error in errors:
            print(error)
    else:
        print(f"valid: {args.path}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
