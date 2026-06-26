#!/usr/bin/env python3
"""Generate and validate Farplane system and feature registries."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
FEATURE_REGISTRY = ROOT / "docs" / "features" / "registry.jsonl"
SYSTEM_REGISTRY = ROOT / "docs" / "systems" / "registry.jsonl"
SOURCE_REGISTRY = ROOT / "docs" / "sources" / "registry.jsonl"
SYSTEM_ROOT = ROOT / "docs" / "systems"

SOURCE_FEATURE_FIELDS = {
    "id",
    "name",
    "status",
    "category",
    "capability_role",
    "public",
    "surfaces",
    "source_refs",
    "external_refs",
    "evidence_refs",
    "known_limits",
    "metrics",
    "last_verified",
}
GENERATED_FEATURE_FIELDS = SOURCE_FEATURE_FIELDS | {
    "system_id",
    "system_name",
    "owner_spec",
}
SYSTEM_FIELDS = {
    "id",
    "name",
    "status",
    "summary",
    "owner_spec",
    "primary_feature_ref",
    "feature_refs",
    "refs",
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
ALLOWED_CAPABILITY_ROLES = {
    "primary",
    "subcapability",
    "implementation_detail",
    "retired_alias",
    "retired",
}
FEATURE_ID_RE = re.compile(r"^FEAT-\d{4}$")
SYSTEM_ID_RE = re.compile(r"^SYS-\d{4}$")
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


def system_paths(root: Path = SYSTEM_ROOT) -> list[Path]:
    if not root.exists():
        return []
    return sorted(
        path
        for path in root.glob("*.md")
        if path.name not in {"README.md", "AGENTS.md"}
    )


def load_json_block(frontmatter: str, path: Path, key: str, errors: list[str]) -> Any | None:
    raw = extract_block(frontmatter, key)
    if raw is None:
        errors.append(f"{path.relative_to(ROOT)}: missing {key}")
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid {key}: {exc}")
        return None


def load_system_sources(
    root: Path = ROOT,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    errors: list[str] = []
    systems: list[dict[str, Any]] = []
    features: list[dict[str, Any]] = []
    systems_root = root / "docs" / "systems"

    for path in system_paths(systems_root):
        text = path.read_text(encoding="utf-8")
        frontmatter = extract_frontmatter(text, path, errors)
        if frontmatter is None:
            continue

        system = load_json_block(frontmatter, path, "system_record_json", errors)
        raw_features = load_json_block(frontmatter, path, "capability_records_json", errors)
        if not isinstance(system, dict):
            errors.append(f"{path.relative_to(root)}: system_record_json must be an object")
            continue
        if not isinstance(raw_features, list) or not all(
            isinstance(item, dict) for item in raw_features
        ):
            errors.append(
                f"{path.relative_to(root)}: capability_records_json must be an array of objects"
            )
            continue

        system = dict(system)
        system["_source_path"] = str(path.relative_to(root))
        systems.append(system)
        for record in raw_features:
            feature = dict(record)
            feature["_system_id"] = system.get("id")
            feature["_system_name"] = system.get("name")
            feature["_owner_spec"] = system.get("owner_spec")
            feature["_source_path"] = str(path.relative_to(root))
            features.append(feature)

    return systems, features, errors


def require_string(record: dict[str, Any], field: str, record_id: str, errors: list[str]) -> None:
    value = record.get(field)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{record_id}: {field} must be a non-empty string")


def require_bool(record: dict[str, Any], field: str, record_id: str, errors: list[str]) -> None:
    if not isinstance(record.get(field), bool):
        errors.append(f"{record_id}: {field} must be a boolean")


def require_string_list(
    record: dict[str, Any], field: str, record_id: str, errors: list[str]
) -> list[str]:
    value = record.get(field)
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        errors.append(f"{record_id}: {field} must be a list of strings")
        return []
    return value


def validate_local_refs(
    record_id: str, field: str, refs: list[str], source_ids: set[str], errors: list[str]
) -> None:
    for ref in refs:
        if is_url(ref):
            continue
        if field == "source_refs" and SOURCE_ID_RE.match(ref):
            if source_ids and ref not in source_ids:
                errors.append(f"{record_id}: unknown source ref {ref}")
            continue
        if not local_ref_exists(ref):
            errors.append(f"{record_id}: {field} local ref does not exist: {ref}")


def validate_system(
    system: dict[str, Any],
    feature_ids: set[str],
    source_ids: set[str],
    errors: list[str],
) -> None:
    missing = SYSTEM_FIELDS - system.keys()
    extra = system.keys() - SYSTEM_FIELDS - {"_source_path"}
    source_path = system.get("_source_path", "unknown")
    system_id = system.get("id")

    if missing:
        errors.append(f"{source_path}: system missing fields: {sorted(missing)}")
    if extra:
        errors.append(f"{source_path}: system unknown fields: {sorted(extra)}")
    if not isinstance(system_id, str) or not SYSTEM_ID_RE.match(system_id):
        errors.append(f"{source_path}: id must match SYS-####")
        system_id = str(system_id or source_path)

    for field in ("name", "status", "summary", "owner_spec", "primary_feature_ref", "last_verified"):
        require_string(system, field, system_id, errors)
    if system.get("status") not in ALLOWED_STATUSES:
        errors.append(f"{system_id}: invalid status {system.get('status')!r}")
    if isinstance(system.get("last_verified"), str) and not DATE_RE.match(system["last_verified"]):
        errors.append(f"{system_id}: last_verified must use YYYY-MM-DD")

    feature_refs = require_string_list(system, "feature_refs", system_id, errors)
    refs = require_string_list(system, "refs", system_id, errors)

    owner_spec = system.get("owner_spec")
    if isinstance(owner_spec, str) and not local_ref_exists(owner_spec):
        errors.append(f"{system_id}: owner_spec local ref does not exist: {owner_spec}")
    validate_local_refs(system_id, "refs", refs, source_ids, errors)

    primary = system.get("primary_feature_ref")
    if isinstance(primary, str):
        if primary not in feature_refs:
            errors.append(f"{system_id}: primary_feature_ref must be included in feature_refs")
        if primary not in feature_ids:
            errors.append(f"{system_id}: unknown primary_feature_ref {primary}")

    for feature_id in feature_refs:
        if feature_id not in feature_ids:
            errors.append(f"{system_id}: unknown feature_ref {feature_id}")


def validate_feature_source(
    record: dict[str, Any],
    feature_ids: set[str],
    source_ids: set[str],
    errors: list[str],
) -> None:
    missing = SOURCE_FEATURE_FIELDS - record.keys()
    extra = record.keys() - SOURCE_FEATURE_FIELDS - {
        "_system_id",
        "_system_name",
        "_owner_spec",
        "_source_path",
    }
    feature_id = record.get("id")
    if not isinstance(feature_id, str) or not FEATURE_ID_RE.match(feature_id):
        errors.append(f"{record.get('_source_path', 'unknown')}: feature id must match FEAT-####")
        feature_id = str(feature_id or record.get("_source_path", "unknown"))

    if missing:
        errors.append(f"{feature_id}: missing fields: {sorted(missing)}")
    if extra:
        errors.append(f"{feature_id}: unknown fields: {sorted(extra)}")

    if record.get("status") not in ALLOWED_STATUSES:
        errors.append(f"{feature_id}: invalid status {record.get('status')!r}")
    if record.get("capability_role") not in ALLOWED_CAPABILITY_ROLES:
        errors.append(f"{feature_id}: invalid capability_role {record.get('capability_role')!r}")
    require_bool(record, "public", feature_id, errors)

    for field in ("name", "category", "known_limits", "last_verified"):
        require_string(record, field, feature_id, errors)
    if isinstance(record.get("last_verified"), str) and not DATE_RE.match(record["last_verified"]):
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
    if record.get("status") == "retired" and record.get("capability_role") not in {
        "retired",
        "retired_alias",
    }:
        errors.append(f"{feature_id}: retired records must use retired capability roles")

    if record.get("capability_role") == "primary" and record.get("public") is not True:
        errors.append(f"{feature_id}: primary capabilities must be public")
    if record.get("public") and record.get("capability_role") != "primary":
        errors.append(f"{feature_id}: only primary capabilities may be public")

    validate_local_refs(feature_id, "surfaces", surfaces, source_ids, errors)
    validate_local_refs(feature_id, "source_refs", source_refs, source_ids, errors)
    validate_local_refs(feature_id, "evidence_refs", evidence_refs, source_ids, errors)


def generated_feature_row(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": record["id"],
        "name": record["name"],
        "status": record["status"],
        "system_id": record["_system_id"],
        "system_name": record["_system_name"],
        "capability_role": record["capability_role"],
        "public": record["public"],
        "category": record["category"],
        "surfaces": record["surfaces"],
        "source_refs": record["source_refs"],
        "external_refs": record["external_refs"],
        "evidence_refs": record["evidence_refs"],
        "known_limits": record["known_limits"],
        "metrics": record["metrics"],
        "owner_spec": record["_owner_spec"],
        "last_verified": record["last_verified"],
    }


def generated_system_row(system: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": system["id"],
        "name": system["name"],
        "status": system["status"],
        "summary": system["summary"],
        "owner_spec": system["owner_spec"],
        "primary_feature_ref": system["primary_feature_ref"],
        "feature_refs": system["feature_refs"],
        "refs": system["refs"],
        "last_verified": system["last_verified"],
    }


def validate() -> list[str]:
    errors: list[str] = []
    source_ids = load_source_ids()
    systems, features, load_errors = load_system_sources(ROOT)
    errors.extend(load_errors)

    if not systems:
        errors.append("docs/systems: no system_record_json entries found")
    if not features:
        errors.append("docs/systems: no capability_records_json entries found")
        return errors

    feature_ids: set[str] = set()
    feature_systems: dict[str, str] = {}
    for line_no, record in enumerate(features, 1):
        feature_id = record.get("id")
        if not isinstance(feature_id, str) or not FEATURE_ID_RE.match(feature_id):
            errors.append(f"capability record {line_no}: id must match FEAT-####")
            continue
        if feature_id in feature_ids:
            errors.append(f"capability record {line_no}: duplicate id {feature_id}")
        feature_ids.add(feature_id)
        system_id = str(record.get("_system_id") or "")
        if feature_id in feature_systems and feature_systems[feature_id] != system_id:
            errors.append(
                f"{feature_id}: assigned to multiple systems: {feature_systems[feature_id]}, {system_id}"
            )
        feature_systems[feature_id] = system_id

    for system in systems:
        validate_system(system, feature_ids, source_ids, errors)

    feature_by_id = {str(record.get("id")): record for record in features}
    for record in features:
        validate_feature_source(record, feature_ids, source_ids, errors)

    for system in systems:
        primary = system.get("primary_feature_ref")
        if isinstance(primary, str) and primary in feature_by_id:
            primary_record = feature_by_id[primary]
            if primary_record.get("capability_role") != "primary":
                errors.append(f"{system.get('id')}: primary feature {primary} must have role primary")
            if primary_record.get("_system_id") != system.get("id"):
                errors.append(f"{system.get('id')}: primary feature {primary} belongs to another system")

        declared = set(system.get("feature_refs", []))
        actual = {
            str(record["id"])
            for record in features
            if record.get("_system_id") == system.get("id") and isinstance(record.get("id"), str)
        }
        missing_from_system = sorted(actual - declared)
        if missing_from_system:
            errors.append(
                f"{system.get('id')}: capability_records_json contains refs missing from feature_refs: {missing_from_system}"
            )

    generated_features = render_feature_registry(features)
    if FEATURE_REGISTRY.exists():
        current = FEATURE_REGISTRY.read_text(encoding="utf-8")
        if current != generated_features:
            errors.append(
                "docs/features/registry.jsonl is stale; run "
                "python3 docs/features/validate_features.py --write"
            )
    else:
        errors.append(f"{FEATURE_REGISTRY.relative_to(ROOT)}: missing generated registry")

    generated_systems = render_system_registry(systems)
    if SYSTEM_REGISTRY.exists():
        current_systems = SYSTEM_REGISTRY.read_text(encoding="utf-8")
        if current_systems != generated_systems:
            errors.append(
                "docs/systems/registry.jsonl is stale; run "
                "python3 docs/features/validate_features.py --write"
            )
    else:
        errors.append(f"{SYSTEM_REGISTRY.relative_to(ROOT)}: missing generated registry")

    return errors


def render_jsonl(rows: list[dict[str, Any]]) -> str:
    return "".join(
        json.dumps(row, separators=(",", ":"), ensure_ascii=False) + "\n" for row in rows
    )


def render_feature_registry(records: list[dict[str, Any]]) -> str:
    rows = [generated_feature_row(row) for row in records]
    return render_jsonl(sorted(rows, key=lambda row: row.get("id", "")))


def render_system_registry(systems: list[dict[str, Any]]) -> str:
    rows = [generated_system_row(system) for system in systems]
    return render_jsonl(sorted(rows, key=lambda row: row.get("id", "")))


def write_registries() -> None:
    systems, features, errors = load_system_sources(ROOT)
    if errors:
        raise SystemExit("\n".join(errors))
    FEATURE_REGISTRY.write_text(render_feature_registry(features), encoding="utf-8")
    SYSTEM_REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    SYSTEM_REGISTRY.write_text(render_system_registry(systems), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write generated registries")
    args = parser.parse_args()

    if args.write:
        write_registries()

    errors = validate()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    feature_count = sum(
        1 for line in FEATURE_REGISTRY.read_text(encoding="utf-8").splitlines() if line.strip()
    )
    system_count = sum(
        1 for line in SYSTEM_REGISTRY.read_text(encoding="utf-8").splitlines() if line.strip()
    )
    print(f"system + feature registry contract OK ({system_count} systems, {feature_count} capabilities)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
