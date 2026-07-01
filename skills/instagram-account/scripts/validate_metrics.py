#!/usr/bin/env python3
"""Validate Instagram account metric snapshots without calling external APIs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ALLOWED_METRICS = {
    "instagram_followers",
    "instagram_views",
    "instagram_likes",
    "instagram_reach",
    "instagram_saves",
    "instagram_shares",
    "instagram_comments",
    "instagram_likes_from_insights",
    "instagram_total_interactions",
    "instagram_avg_watch_time",
    "instagram_total_watch_time",
    "instagram_retention_score",
}
ALLOWED_SOURCES = {"instagram_account_api", "manual_instagram_account"}
FORBIDDEN_KEYS = {"access_token", "app_secret", "client_secret", "refresh_token"}
SECRET_FRAGMENTS = ("authorization", "secret", "token")


def walk_keys(value: Any) -> list[str]:
    keys: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            keys.append(str(key))
            keys.extend(walk_keys(nested))
    elif isinstance(value, list):
        for item in value:
            keys.extend(walk_keys(item))
    return keys


def validate(payload: dict[str, Any], expect_metric: set[str], allow_blocked: bool) -> tuple[bool, list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    status = payload.get("status")
    if status not in {"available", "source_gap", "blocked"}:
        errors.append("status must be available, source_gap, or blocked")
    if status == "blocked" and not allow_blocked:
        errors.append("blocked snapshot requires --allow-blocked")
    if payload.get("source_id") not in ALLOWED_SOURCES:
        errors.append(f"source_id must be one of {sorted(ALLOWED_SOURCES)}")
    if not payload.get("date"):
        errors.append("date is required")
    if payload.get("redacted") is not True:
        errors.append("redacted must be true")

    observations = payload.get("observations")
    if not isinstance(observations, list):
        errors.append("observations must be a list")
        observations = []

    seen_metrics: set[str] = set()
    for index, observation in enumerate(observations):
        if not isinstance(observation, dict):
            errors.append(f"observations[{index}] must be an object")
            continue
        metric_id = observation.get("metric_id")
        seen_metrics.add(str(metric_id))
        if metric_id not in ALLOWED_METRICS:
            errors.append(f"observations[{index}].metric_id is not allowed: {metric_id}")
        if observation.get("date") != payload.get("date"):
            errors.append(f"observations[{index}].date must match snapshot date")
        if observation.get("status") != "available":
            errors.append(f"observations[{index}].status must be available")
        value = observation.get("value")
        if not isinstance(value, (int, float)):
            errors.append(f"observations[{index}].value must be numeric")
        elif value < 0:
            errors.append(f"observations[{index}].value must not be negative")

    missing_expected = sorted(expect_metric - seen_metrics)
    if missing_expected:
        errors.append(f"missing expected metrics: {', '.join(missing_expected)}")
    if status == "available" and not observations:
        errors.append("available snapshot must contain at least one observation")
    if status in {"blocked", "source_gap"} and not payload.get("gaps"):
        errors.append("blocked/source_gap snapshot must include gaps")
    if payload.get("gaps") and not isinstance(payload.get("gaps"), list):
        errors.append("gaps must be a list when present")

    lower_keys = {key.lower() for key in walk_keys(payload)}
    leaked_keys = sorted(key for key in lower_keys if key in FORBIDDEN_KEYS or any(fragment == key for fragment in SECRET_FRAGMENTS))
    if leaked_keys:
        errors.append(f"possible secret-bearing keys present: {', '.join(leaked_keys)}")
    if payload.get("deep") and not payload.get("media_ids"):
        warnings.append("deep mode without media_ids may not produce media retention metrics")

    return not errors, errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", required=True)
    parser.add_argument("--expect-metric", action="append", default=[])
    parser.add_argument("--allow-blocked", action="store_true")
    args = parser.parse_args()

    payload = json.loads(Path(args.snapshot).read_text(encoding="utf-8"))
    ok, errors, warnings = validate(payload, set(args.expect_metric), args.allow_blocked)
    print(json.dumps({"ok": ok, "snapshot": args.snapshot, "errors": errors, "warnings": warnings}, indent=2, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
