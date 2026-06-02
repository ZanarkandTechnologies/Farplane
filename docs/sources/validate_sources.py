#!/usr/bin/env python3
"""Validate Farplane's source provenance registry."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "docs" / "sources" / "registry.jsonl"
FEATURE_REGISTRY = ROOT / "docs" / "features" / "registry.jsonl"

REQUIRED_FIELDS = {
    "id",
    "title",
    "source_type",
    "origin",
    "canonical_url",
    "canonical_key",
    "visibility",
    "captured_at",
    "local_artifacts",
    "feature_refs",
    "decision",
    "duplicate_of",
    "status",
    "last_verified",
    "notes",
}
ALLOWED_TYPES = {
    "spec",
    "blog",
    "video",
    "docs",
    "repo",
    "paper",
    "user-provided",
    "research",
}
ALLOWED_VISIBILITY = {"public", "private", "internal", "customer", "unknown"}
ALLOWED_DECISIONS = {
    "adopt",
    "adapt",
    "reject",
    "defer",
    "duplicate",
    "reference-only",
}
ALLOWED_STATUSES = {"active", "archived", "superseded", "sensitive-redacted"}
SOURCE_ID_RE = re.compile(r"^SRC-\d{4}$")
FEATURE_ID_RE = re.compile(r"^FEAT-\d{4}$")
KEY_RE = re.compile(r"^[a-z0-9][a-z0-9._:-]*[a-z0-9]$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def load_feature_ids() -> set[str]:
    ids: set[str] = set()
    if not FEATURE_REGISTRY.exists():
        return ids
    for line in FEATURE_REGISTRY.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        feature_id = record.get("id")
        if isinstance(feature_id, str):
            ids.add(feature_id)
    return ids


def local_ref_exists(ref: str) -> bool:
    path = ref.split("#", 1)[0]
    return bool(path) and (ROOT / path).exists()


def require_string(record: dict[str, Any], field: str, source_id: str, errors: list[str]) -> None:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{source_id}: {field} must be a non-empty string")


def require_string_list(
    record: dict[str, Any], field: str, source_id: str, errors: list[str]
) -> list[str]:
    value = record.get(field)
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        errors.append(f"{source_id}: {field} must be a list of strings")
        return []
    return value


def validate() -> list[str]:
    errors: list[str] = []
    feature_ids = load_feature_ids()
    source_ids: set[str] = set()
    canonical_keys: set[str] = set()
    records: list[dict[str, Any]] = []

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

        source_id = record.get("id")
        if not isinstance(source_id, str) or not SOURCE_ID_RE.match(source_id):
            errors.append(f"line {line_no}: id must match SRC-####")
            source_id = f"line-{line_no}"
        if source_id in source_ids:
            errors.append(f"line {line_no}: duplicate id {source_id}")
        source_ids.add(source_id)
        records.append(record)

        for field in (
            "title",
            "origin",
            "canonical_url",
            "canonical_key",
            "captured_at",
            "last_verified",
            "notes",
        ):
            require_string(record, field, source_id, errors)

        source_type = record.get("source_type")
        if source_type not in ALLOWED_TYPES:
            errors.append(f"{source_id}: invalid source_type {source_type!r}")
        visibility = record.get("visibility")
        if visibility not in ALLOWED_VISIBILITY:
            errors.append(f"{source_id}: invalid visibility {visibility!r}")
        decision = record.get("decision")
        if decision not in ALLOWED_DECISIONS:
            errors.append(f"{source_id}: invalid decision {decision!r}")
        status = record.get("status")
        if status not in ALLOWED_STATUSES:
            errors.append(f"{source_id}: invalid status {status!r}")

        for field in ("captured_at", "last_verified"):
            value = record.get(field)
            if isinstance(value, str) and not DATE_RE.match(value):
                errors.append(f"{source_id}: {field} must use YYYY-MM-DD")

        canonical_key = record.get("canonical_key")
        if isinstance(canonical_key, str):
            if not KEY_RE.match(canonical_key):
                errors.append(f"{source_id}: canonical_key must be lowercase slug text")
            if canonical_key in canonical_keys:
                errors.append(f"{source_id}: duplicate canonical_key {canonical_key}")
            canonical_keys.add(canonical_key)

        for ref in require_string_list(record, "local_artifacts", source_id, errors):
            if not local_ref_exists(ref):
                errors.append(f"{source_id}: local artifact does not exist: {ref}")

        for ref in require_string_list(record, "feature_refs", source_id, errors):
            if not FEATURE_ID_RE.match(ref):
                errors.append(f"{source_id}: feature_refs entry must match FEAT-####: {ref}")
            elif feature_ids and ref not in feature_ids:
                errors.append(f"{source_id}: unknown feature ref {ref}")

        duplicate_of = record.get("duplicate_of")
        if duplicate_of is not None:
            if not isinstance(duplicate_of, str) or not SOURCE_ID_RE.match(duplicate_of):
                errors.append(f"{source_id}: duplicate_of must be null or SRC-####")
        if decision == "duplicate" and duplicate_of is None:
            errors.append(f"{source_id}: duplicate decision requires duplicate_of")
        if decision != "duplicate" and duplicate_of is not None:
            errors.append(f"{source_id}: duplicate_of is only valid for duplicate decisions")

    known_ids = {
        record["id"]
        for record in records
        if isinstance(record.get("id"), str) and SOURCE_ID_RE.match(record["id"])
    }
    for record in records:
        duplicate_of = record.get("duplicate_of")
        source_id = record.get("id", "<unknown>")
        if isinstance(duplicate_of, str) and duplicate_of not in known_ids:
            errors.append(f"{source_id}: duplicate_of points to unknown source {duplicate_of}")
        if duplicate_of == source_id:
            errors.append(f"{source_id}: duplicate_of cannot point to itself")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    count = sum(1 for line in REGISTRY.read_text(encoding="utf-8").splitlines() if line.strip())
    print(f"source registry contract OK ({count} records)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
