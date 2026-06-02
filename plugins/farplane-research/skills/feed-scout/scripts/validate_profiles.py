#!/usr/bin/env python3
"""Validate feed-scout tracked-profile JSONL files."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


ALLOWED_PLATFORMS = {"x", "youtube", "blog"}
ALLOWED_CONTENT_KINDS = {
    "x": {"post", "thread"},
    "youtube": {"video", "short"},
    "blog": {"article"},
}
ALLOWED_SIGNAL = {"low", "medium", "high"}


def _is_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def validate_record(record: object, line_no: int) -> list[str]:
    errors: list[str] = []
    if not isinstance(record, dict):
        return [f"line {line_no}: record must be an object"]

    record_id = record.get("id", f"line-{line_no}")
    if not isinstance(record_id, str) or not re.match(r"^[a-z0-9][a-z0-9-]*$", record_id):
        errors.append(f"{record_id}: id must be a non-empty slug")

    platform = record.get("platform")
    if platform not in ALLOWED_PLATFORMS:
        errors.append(f"{record_id}: platform must be one of {sorted(ALLOWED_PLATFORMS)}")

    profile_url = record.get("profile_url")
    if not isinstance(profile_url, str) or not _is_url(profile_url):
        errors.append(f"{record_id}: profile_url must be an http(s) URL")

    kinds = record.get("content_kinds")
    if not isinstance(kinds, list) or not kinds or not all(isinstance(k, str) for k in kinds):
        errors.append(f"{record_id}: content_kinds must be a non-empty string list")
    elif platform in ALLOWED_CONTENT_KINDS:
        invalid = sorted(set(kinds) - ALLOWED_CONTENT_KINDS[platform])
        if invalid:
            errors.append(f"{record_id}: invalid content_kinds for {platform}: {invalid}")

    tags = record.get("tags", [])
    if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
        errors.append(f"{record_id}: tags must be a string list")

    cadence = record.get("cadence")
    if not isinstance(cadence, str) or not cadence.strip():
        errors.append(f"{record_id}: cadence must be a non-empty string")

    fetch_method = record.get("fetch_method")
    if not isinstance(fetch_method, str) or not fetch_method.strip():
        errors.append(f"{record_id}: fetch_method must be a non-empty string")

    enabled = record.get("enabled")
    if not isinstance(enabled, bool):
        errors.append(f"{record_id}: enabled must be a boolean")

    min_signal = record.get("min_signal")
    if min_signal not in ALLOWED_SIGNAL:
        errors.append(f"{record_id}: min_signal must be one of {sorted(ALLOWED_SIGNAL)}")

    return errors


def validate(path: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    seen_ids: set[str] = set()
    count = 0

    with path.open() as handle:
        for line_no, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            count += 1
            try:
                record = json.loads(stripped)
            except json.JSONDecodeError as exc:
                errors.append(f"line {line_no}: invalid JSON: {exc}")
                continue
            if isinstance(record, dict):
                record_id = record.get("id")
                if isinstance(record_id, str):
                    if record_id in seen_ids:
                        errors.append(f"{record_id}: duplicate id")
                    seen_ids.add(record_id)
            errors.extend(validate_record(record, line_no))

    if count == 0:
        errors.append("profile file must contain at least one record")

    return count, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    count, errors = validate(args.path)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(f"feed-scout profile validation OK ({count} records)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
