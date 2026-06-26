#!/usr/bin/env python3
"""Generate and validate Farplane's feature registry from spec metadata."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "docs" / "features" / "registry.jsonl"
SOURCE_REGISTRY = ROOT / "docs" / "sources" / "registry.jsonl"
SPEC_ROOT = ROOT / "docs" / "specs"

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


def extract_frontmatter(text: str, path: Path, errors: list[str]) -> str | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        errors.append(f"{path.relative_to(ROOT)}: unterminated frontmatter")
        return None
    return text[4:end]


def extract_block(frontmatter: str, key: str) -> str | None:
    lines = frontmatter.splitlines()
    for index, line in enumerate(lines):
        if line.strip() != f"{key}: |":
            continue
        block: list[str] = []
        for raw in lines[index + 1 :]:
            if raw and not raw.startswith((" ", "\t")):
                break
            block.append(raw[2:] if raw.startswith("  ") else raw.lstrip())
        return "\n".join(block).strip()
    return None


def spec_paths(root: Path = SPEC_ROOT) -> list[Path]:
    return sorted(
        path
        for path in root.glob("*.md")
        if path.name not in {"README.md", "AGENTS.md"}
    )


def load_spec_feature_records(root: Path = ROOT) -> tuple[list[dict[str, Any]], list[str]]:
    errors: list[str] = []
    records: list[dict[str, Any]] = []
    specs_root = root / "docs" / "specs"

    for path in spec_paths(specs_root):
        text = path.read_text(encoding="utf-8")
        frontmatter = extract_frontmatter(text, path, errors)
        if frontmatter is None:
            continue
        raw_records = extract_block(frontmatter, "feature_records_json")
        if raw_records is None:
            continue
        try:
            parsed = json.loads(raw_records)
        except json.JSONDecodeError as exc:
            errors.append(f"{path.relative_to(root)}: invalid feature_records_json: {exc}")
            continue
        if not isinstance(parsed, list) or not all(isinstance(item, dict) for item in parsed):
            errors.append(
                f"{path.relative_to(root)}: feature_records_json must be a JSON array of objects"
            )
            continue
        for record in parsed:
            records.append(record)

    return records, errors


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

    records, load_errors = load_spec_feature_records(ROOT)
    errors.extend(load_errors)
    if not records:
        errors.append("docs/specs: no feature_records_json entries found")
        return errors

    for line_no, record in enumerate(records, 1):
        missing = REQUIRED_FIELDS - record.keys()
        extra = record.keys() - REQUIRED_FIELDS
        if missing:
            errors.append(f"record {line_no}: missing fields: {sorted(missing)}")
        if extra:
            errors.append(f"record {line_no}: unknown fields: {sorted(extra)}")

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

    generated = render_registry(records)
    if REGISTRY.exists():
        current = REGISTRY.read_text(encoding="utf-8")
        if current != generated:
            errors.append(
                "docs/features/registry.jsonl is stale; run "
                "python3 docs/features/validate_features.py --write"
            )
    else:
        errors.append(f"{REGISTRY.relative_to(ROOT)}: missing generated registry")

    return errors


def render_registry(records: list[dict[str, Any]]) -> str:
    rows = sorted(records, key=lambda row: row.get("id", ""))
    return "".join(json.dumps(row, separators=(",", ":"), ensure_ascii=False) + "\n" for row in rows)


def write_registry() -> None:
    records, errors = load_spec_feature_records(ROOT)
    if errors:
        raise SystemExit("\n".join(errors))
    REGISTRY.write_text(render_registry(records), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write generated registry")
    args = parser.parse_args()

    if args.write:
        write_registry()

    errors = validate()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    count = sum(1 for line in REGISTRY.read_text(encoding="utf-8").splitlines() if line.strip())
    print(f"feature registry contract OK ({count} generated records)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
