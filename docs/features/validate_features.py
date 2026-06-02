#!/usr/bin/env python3
"""Validate Farplane's feature registry."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "docs" / "features" / "registry.jsonl"
SOURCE_REGISTRY = ROOT / "docs" / "sources" / "registry.jsonl"

REQUIRED_FIELDS = {
    "id",
    "name",
    "status",
    "category",
    "surfaces",
    "source_refs",
    "external_refs",
    "evidence_refs",
    "known_limits",
    "metrics",
    "last_verified",
}
ALLOWED_STATUSES = {
    "implemented",
    "partial",
    "proposed",
    "designed",
    "deferred",
    "retired",
}
FEATURE_ID_RE = re.compile(r"^FEAT-\d{4}$")
SOURCE_ID_RE = re.compile(r"^SRC-\d{4}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def is_url(value: str) -> bool:
    return value.startswith(("http://", "https://"))


def local_path(value: str) -> str:
    return value.split("#", 1)[0]


def local_ref_exists(ref: str) -> bool:
    path = local_path(ref)
    return bool(path) and (ROOT / path).exists()


def load_source_ids() -> set[str]:
    ids: set[str] = set()
    if not SOURCE_REGISTRY.exists():
        return ids

    for line in SOURCE_REGISTRY.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        source_id = record.get("id")
        if isinstance(source_id, str):
            ids.add(source_id)
    return ids


def require_string(record: dict[str, Any], field: str, feature_id: str, errors: list[str]) -> None:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{feature_id}: {field} must be a non-empty string")


def require_string_list(
    record: dict[str, Any], field: str, feature_id: str, errors: list[str]
) -> list[str]:
    value = record.get(field)
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        errors.append(f"{feature_id}: {field} must be a list of strings")
        return []
    return value


def validate_local_refs(
    feature_id: str, field: str, refs: list[str], source_ids: set[str], errors: list[str]
) -> None:
    for ref in refs:
        if is_url(ref):
            continue
        if field == "source_refs" and SOURCE_ID_RE.match(ref):
            if source_ids and ref not in source_ids:
                errors.append(f"{feature_id}: unknown source ref {ref}")
            continue
        if not local_ref_exists(ref):
            errors.append(f"{feature_id}: {field} local ref does not exist: {ref}")


def validate() -> list[str]:
    errors: list[str] = []
    feature_ids: set[str] = set()
    source_ids = load_source_ids()

    if not REGISTRY.exists():
        return [f"{REGISTRY.relative_to(ROOT)}: missing registry"]

    for line_no, line in enumerate(REGISTRY.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_no}: invalid JSON: {exc}")
            continue

        missing = REQUIRED_FIELDS - record.keys()
        extra = record.keys() - REQUIRED_FIELDS
        if missing:
            errors.append(f"line {line_no}: missing fields: {sorted(missing)}")
        if extra:
            errors.append(f"line {line_no}: unknown fields: {sorted(extra)}")

        feature_id = record.get("id")
        if not isinstance(feature_id, str) or not FEATURE_ID_RE.match(feature_id):
            errors.append(f"line {line_no}: id must match FEAT-####")
            feature_id = f"line-{line_no}"
        if feature_id in feature_ids:
            errors.append(f"line {line_no}: duplicate id {feature_id}")
        feature_ids.add(feature_id)

        if record.get("status") not in ALLOWED_STATUSES:
            errors.append(f"{feature_id}: invalid status {record.get('status')!r}")

        for field in ("name", "category", "known_limits", "last_verified"):
            require_string(record, field, feature_id, errors)

        last_verified = record.get("last_verified")
        if isinstance(last_verified, str) and not DATE_RE.match(last_verified):
            errors.append(f"{feature_id}: last_verified must use YYYY-MM-DD")

        surfaces = require_string_list(record, "surfaces", feature_id, errors)
        source_refs = require_string_list(record, "source_refs", feature_id, errors)
        require_string_list(record, "external_refs", feature_id, errors)
        evidence_refs = require_string_list(record, "evidence_refs", feature_id, errors)
        require_string_list(record, "metrics", feature_id, errors)

        if record.get("status") == "implemented" and not surfaces:
            errors.append(f"{feature_id}: implemented records need at least one surface")
        if record.get("status") == "implemented" and not evidence_refs:
            errors.append(f"{feature_id}: implemented records need evidence refs")

        validate_local_refs(feature_id, "surfaces", surfaces, source_ids, errors)
        validate_local_refs(feature_id, "source_refs", source_refs, source_ids, errors)
        validate_local_refs(feature_id, "evidence_refs", evidence_refs, source_ids, errors)

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    count = sum(1 for line in REGISTRY.read_text(encoding="utf-8").splitlines() if line.strip())
    print(f"feature registry contract OK ({count} records)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
