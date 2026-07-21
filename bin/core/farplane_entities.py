#!/usr/bin/env python3
"""Compile flat Markdown-owned entities into generated project views."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import tempfile
from dataclasses import dataclass
from datetime import date as date_type
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml


ENTITY_ROOT = Path(".farplane/entities")
VIEW_CONFIG_PATH = Path(".farplane/views.yaml")
ENTITY_INDEX_PATH = ENTITY_ROOT / "index.json"
WORLD_VIEW_PATH = ENTITY_ROOT / "world.json"
CRM_VIEW_PATH = ENTITY_ROOT / "crm.json"
REQUIRED_FIELDS = ("id", "kind", "name")
REFERENCE_FIELDS = (
    "company_ref",
    "entity_refs",
    "opportunity_refs",
    "organization_ref",
    "person_refs",
    "relationship_refs",
)
ENTITY_LINK_PATTERN = re.compile(r"(?<!!)\[([^\]\n]+)\]\(entity:([^\s)]+)\)")
QUESTION_REF_PATTERN = re.compile(r"\[\^(q-[a-z0-9][a-z0-9_-]*)\]")
QUESTION_DEFINITION_PATTERN = re.compile(
    r"^\[\^(q-[a-z0-9][a-z0-9_-]*)\]:[ \t]*(.*?)[ \t]*$",
    re.MULTILINE,
)
HEADING_PATTERN = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)
PROJECT_ID_PATTERN = re.compile(r"[^a-z0-9]+")
INLINE_CODE_PATTERN = re.compile(r"(`+)[^\n]*?\1")


@dataclass(frozen=True)
class EntityIssue:
    path: str
    reason: str


class UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects mappings with duplicate keys."""


class DuplicateKeyError(yaml.constructor.ConstructorError):
    """Raised before YAML mappings can collapse duplicate authored keys."""


def construct_unique_mapping(
    loader: UniqueKeyLoader,
    node: yaml.nodes.MappingNode,
    deep: bool = False,
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found unacceptable key {key!r}",
                key_node.start_mark,
            ) from exc
        if duplicate:
            raise DuplicateKeyError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    construct_unique_mapping,
)


def json_value(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date_type):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(key): json_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_value(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def read_entity(path: Path) -> tuple[dict[str, Any] | None, str, str | None]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n") or "\n---\n" not in text:
        return None, "", "missing_frontmatter"
    raw, body = text[4:].split("\n---\n", 1)
    try:
        loaded = yaml.safe_load(raw) or {}
    except yaml.YAMLError as exc:
        return None, "", f"invalid_frontmatter:{exc.__class__.__name__}"
    if not isinstance(loaded, dict):
        return None, "", "frontmatter_not_object"
    return {str(key): json_value(value) for key, value in loaded.items()}, body.lstrip("\n"), None


def field_text(frontmatter: dict[str, Any], field: str) -> str:
    value = frontmatter.get(field)
    return "" if value is None else str(value).strip()


def validate_id(entity_id: str) -> str | None:
    if not entity_id:
        return "missing:id"
    if entity_id.startswith(('.', '-')) or any(char not in "abcdefghijklmnopqrstuvwxyz0123456789-_" for char in entity_id):
        return "invalid_id"
    return None


def load_entity_views(
    project_root: Path,
    known_ids: set[str],
) -> tuple[list[dict[str, Any]], list[EntityIssue]]:
    """Load one local named-view config and validate canonical entity membership."""
    config_path = project_root / VIEW_CONFIG_PATH
    if not config_path.exists():
        return [], []
    relative_path = VIEW_CONFIG_PATH.as_posix()
    try:
        loaded = yaml.load(config_path.read_text(encoding="utf-8"), Loader=UniqueKeyLoader)
    except DuplicateKeyError:
        return [], [EntityIssue(relative_path, "invalid_views_yaml:duplicate_key")]
    except yaml.YAMLError as exc:
        return [], [EntityIssue(relative_path, f"invalid_views_yaml:{exc.__class__.__name__}")]
    except OSError as exc:
        return [], [EntityIssue(relative_path, f"views_read_error:{exc.__class__.__name__}")]
    if loaded is None:
        loaded = {}
    if not isinstance(loaded, dict):
        return [], [EntityIssue(relative_path, "views_config_not_object")]
    raw_views = loaded.get("views")
    if not isinstance(raw_views, dict):
        return [], [EntityIssue(relative_path, "views_not_object")]

    views: list[dict[str, Any]] = []
    issues: list[EntityIssue] = []
    for raw_view_id, raw_view in raw_views.items():
        if not isinstance(raw_view_id, str):
            issues.append(EntityIssue(relative_path, f"invalid_view_id:{raw_view_id}"))
            continue
        view_id = raw_view_id.strip()
        if validate_id(view_id):
            issues.append(EntityIssue(relative_path, f"invalid_view_id:{view_id}"))
            continue
        if not isinstance(raw_view, dict):
            issues.append(EntityIssue(relative_path, f"invalid_view:{view_id}:not_object"))
            continue
        name = field_text(raw_view, "name")
        if not name:
            issues.append(EntityIssue(relative_path, f"invalid_view:{view_id}:missing_name"))
            continue
        raw_entity_ids = raw_view.get("entity_ids")
        if not isinstance(raw_entity_ids, list):
            issues.append(EntityIssue(relative_path, f"invalid_view:{view_id}:entity_ids_not_list"))
            continue
        if not raw_entity_ids:
            issues.append(EntityIssue(relative_path, f"invalid_view:{view_id}:empty_entity_ids"))
            continue

        entity_ids: list[str] = []
        seen_entity_ids: set[str] = set()
        view_valid = True
        for raw_entity_id in raw_entity_ids:
            if not isinstance(raw_entity_id, str):
                issues.append(
                    EntityIssue(relative_path, f"invalid_view:{view_id}:invalid_entity_id:{raw_entity_id}")
                )
                view_valid = False
                continue
            entity_id = raw_entity_id.strip()
            if validate_id(entity_id):
                issues.append(
                    EntityIssue(relative_path, f"invalid_view:{view_id}:invalid_entity_id:{entity_id}")
                )
                view_valid = False
                continue
            if entity_id in seen_entity_ids:
                issues.append(
                    EntityIssue(relative_path, f"invalid_view:{view_id}:duplicate_entity_id:{entity_id}")
                )
                view_valid = False
                continue
            seen_entity_ids.add(entity_id)
            entity_ids.append(entity_id)
            if entity_id not in known_ids:
                issues.append(
                    EntityIssue(relative_path, f"invalid_view:{view_id}:unresolved_entity_id:{entity_id}")
                )
                view_valid = False
        if view_valid:
            views.append({"id": view_id, "name": name, "entity_ids": entity_ids})

    views.sort(key=lambda item: item["id"])
    return views, issues


def reference_values(frontmatter: dict[str, Any]) -> list[tuple[str, str]]:
    references: list[tuple[str, str]] = []
    for field in REFERENCE_FIELDS:
        value = frontmatter.get(field)
        if value is None:
            continue
        values = value if isinstance(value, list) else [value]
        for item in values:
            ref = str(item).strip()
            if ref:
                references.append((field, ref))
    return references


def project_identity(project_root: Path) -> dict[str, str]:
    """Return a deterministic identity suitable for merging project projections."""
    manifest_path = project_root / "farplane/manifest.json"
    name = project_root.name
    explicit_id = ""
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            manifest = {}
        if isinstance(manifest, dict):
            project = manifest.get("project")
            if isinstance(project, dict):
                name = str(project.get("name") or name).strip()
                explicit_id = str(project.get("id") or "").strip()
            explicit_id = str(manifest.get("project_id") or explicit_id).strip()
    raw_id = explicit_id or name or project_root.name
    normalized = PROJECT_ID_PATTERN.sub("-", raw_id.lower()).strip("-")
    if explicit_id:
        project_id = normalized or "project"
    else:
        root_hash = hashlib.sha256(str(project_root.resolve()).encode("utf-8")).hexdigest()[:10]
        project_id = f"{normalized or 'project'}-{root_hash}"
    return {
        "id": project_id,
        "name": name or project_root.name,
        "source": "manifest" if explicit_id else "local_path_fallback",
    }


def coordinate_values(frontmatter: dict[str, Any]) -> tuple[float | None, float | None, str | None]:
    latitude = frontmatter.get("latitude")
    longitude = frontmatter.get("longitude")
    if latitude is None and longitude is None:
        return None, None, None
    if latitude is None or longitude is None:
        return None, None, "coordinates_unpaired"
    if isinstance(latitude, bool) or isinstance(longitude, bool):
        return None, None, "coordinates_not_numeric"
    try:
        lat_value = float(latitude)
        lon_value = float(longitude)
    except (TypeError, ValueError):
        return None, None, "coordinates_not_numeric"
    if not math.isfinite(lat_value) or not math.isfinite(lon_value):
        return None, None, "coordinates_not_finite"
    if not -90 <= lat_value <= 90:
        return None, None, "latitude_out_of_range"
    if not -180 <= lon_value <= 180:
        return None, None, "longitude_out_of_range"
    return lat_value, lon_value, None


def section_at(body: str, offset: int) -> str | None:
    section: str | None = None
    for match in HEADING_PATTERN.finditer(body, 0, offset):
        section = match.group(1).strip()
    return section


def containing_sentence(body: str, start: int, end: int) -> str:
    """Extract normalized sentence text containing an entity link."""
    left = start
    while left > 0:
        if body[left - 1] in ".!?" and (left == len(body) or body[left].isspace()):
            break
        if body[left - 1] == "\n" and left >= 2 and body[left - 2] == "\n":
            break
        left -= 1
    right = end
    while right < len(body):
        if body[right] in ".!?" and (right + 1 == len(body) or body[right + 1].isspace()):
            right += 1
            break
        if body[right] == "\n" and right + 1 < len(body) and body[right + 1] == "\n":
            break
        right += 1
    sentence = body[left:right].strip()
    return re.sub(r"^(?:[-*+]\s+|\d+[.)]\s+)", "", sentence)


def containing_block_bounds(body: str, start: int, end: int) -> tuple[int, int]:
    """Return the blank-line-delimited Markdown block containing an offset."""
    left_boundary = body.rfind("\n\n", 0, start)
    left = 0 if left_boundary < 0 else left_boundary + 2
    right_boundary = body.find("\n\n", end)
    right = len(body) if right_boundary < 0 else right_boundary
    return left, right


def normalized_claim_context(context: str) -> str:
    """Remove provenance markers while preserving the semantic Markdown claim."""
    without_refs = QUESTION_REF_PATTERN.sub("", context)
    without_marker = re.sub(r"^(?:[-*+]\s+|\d+[.)]\s+)", "", without_refs.strip())
    normalized = re.sub(r"\s+", " ", without_marker).strip()
    return re.sub(r"\s+([.!?,;:])", r"\1", normalized)


def mask_markdown_code(body: str) -> str:
    """Mask fenced and inline code while preserving offsets for link context."""
    characters = list(body)
    offset = 0
    fence_character: str | None = None
    fence_length = 0
    for line in body.splitlines(keepends=True):
        stripped = line.lstrip()
        marker = re.match(r"(`{3,}|~{3,})", stripped)
        is_boundary = marker is not None and (
            fence_character is None
            or (marker.group(1)[0] == fence_character and len(marker.group(1)) >= fence_length)
        )
        if fence_character is not None or is_boundary:
            for index in range(offset, offset + len(line)):
                if characters[index] not in "\r\n":
                    characters[index] = " "
        if is_boundary and marker is not None:
            if fence_character is None:
                fence_character = marker.group(1)[0]
                fence_length = len(marker.group(1))
            else:
                fence_character = None
                fence_length = 0
        offset += len(line)
    masked = "".join(characters)
    for match in INLINE_CODE_PATTERN.finditer(masked):
        masked = masked[:match.start()] + " " * (match.end() - match.start()) + masked[match.end():]
    return masked


def mask_question_definitions(body: str) -> str:
    """Mask question-definition lines while preserving offsets."""
    characters = list(body)
    for match in QUESTION_DEFINITION_PATTERN.finditer(body):
        for index in range(match.start(), match.end()):
            if characters[index] not in "\r\n":
                characters[index] = " "
    return "".join(characters)


def parse_question_definition(raw: str) -> tuple[str, str | None]:
    """Parse `<question> | session=<optional local session id>`."""
    question = raw.strip()
    session_id: str | None = None
    separator = " | session="
    if separator in question:
        question, raw_session = question.rsplit(separator, 1)
        session_id = raw_session.strip().strip("`") or None
    return question.strip(), session_id


def question_definitions(record: dict[str, Any]) -> list[dict[str, Any]]:
    body = str(record.get("body") or "")
    searchable_body = mask_markdown_code(body)
    definitions: list[dict[str, Any]] = []
    for match in QUESTION_DEFINITION_PATTERN.finditer(searchable_body):
        question, session_id = parse_question_definition(match.group(2))
        definitions.append({
            "id": match.group(1),
            "question": question,
            "session_id": session_id,
            "entity_id": record["id"],
            "path": record["path"],
        })
    return definitions


def body_claims(record: dict[str, Any]) -> list[dict[str, Any]]:
    """Return blank-line-delimited claim blocks carrying question references."""
    body = str(record.get("body") or "")
    searchable_body = mask_question_definitions(mask_markdown_code(body))
    claims_by_key: dict[str, dict[str, Any]] = {}
    for match in QUESTION_REF_PATTERN.finditer(searchable_body):
        left, right = containing_block_bounds(body, match.start(), match.end())
        searchable_block = searchable_body[left:right]
        refs = sorted(set(QUESTION_REF_PATTERN.findall(searchable_block)))
        context = normalized_claim_context(body[left:right])
        if not context or context.startswith("#"):
            continue
        display_context = ENTITY_LINK_PATTERN.sub(lambda link: link.group(1), context)
        claim_material = "\0".join((record["id"], display_context))
        claim_hash = hashlib.sha256(claim_material.encode("utf-8")).hexdigest()[:16]
        claim_key = f"claim:{claim_hash}"
        claims_by_key[claim_key] = {
            "key": claim_key,
            "entity_id": record["id"],
            "context": context,
            "display_context": display_context,
            "path": record["path"],
            "section": section_at(body, left),
            "question_refs": refs,
        }
    return [claims_by_key[key] for key in sorted(claims_by_key)]


def body_links(record: dict[str, Any]) -> list[dict[str, Any]]:
    body = str(record.get("body") or "")
    searchable_body = mask_question_definitions(mask_markdown_code(body))
    links: list[dict[str, Any]] = []
    for occurrence, match in enumerate(ENTITY_LINK_PATTERN.finditer(searchable_body), start=1):
        context = normalized_claim_context(containing_sentence(body, match.start(), match.end()))
        block_start, block_end = containing_block_bounds(body, match.start(), match.end())
        links.append({
            "label": match.group(1).strip(),
            "target_entity_id": match.group(2).strip(),
            "context": context,
            "display_context": ENTITY_LINK_PATTERN.sub(lambda link: link.group(1), context),
            "section": section_at(body, match.start()),
            "occurrence": occurrence,
            "question_refs": sorted(set(QUESTION_REF_PATTERN.findall(searchable_body[block_start:block_end]))),
        })
    return links


def build_entity_index(project_root: Path) -> dict[str, Any]:
    root = project_root / ENTITY_ROOT
    issues: list[EntityIssue] = []
    records: list[dict[str, Any]] = []
    seen_ids: dict[str, str] = {}
    excluded_paths: set[str] = set()

    if root.exists():
        for path in sorted(root.rglob("*.md")):
            rel_path = path.relative_to(project_root).as_posix()
            if path.parent != root:
                issues.append(EntityIssue(rel_path, "nested_entity_path"))
                excluded_paths.add(rel_path)
                continue
            frontmatter, body, issue = read_entity(path)
            if issue or frontmatter is None:
                issues.append(EntityIssue(rel_path, issue or "invalid_frontmatter"))
                excluded_paths.add(rel_path)
                continue
            missing = [field for field in REQUIRED_FIELDS if not field_text(frontmatter, field)]
            if missing:
                issues.append(EntityIssue(rel_path, "missing_required:" + ",".join(missing)))
                excluded_paths.add(rel_path)
                continue
            entity_id = field_text(frontmatter, "id")
            id_issue = validate_id(entity_id)
            if id_issue:
                issues.append(EntityIssue(rel_path, id_issue))
                excluded_paths.add(rel_path)
                continue
            if path.stem != entity_id:
                issues.append(EntityIssue(rel_path, f"filename_id_mismatch:{path.stem}:{entity_id}"))
                excluded_paths.add(rel_path)
                continue
            if entity_id in seen_ids:
                issues.append(EntityIssue(rel_path, f"duplicate_id:{entity_id}:{seen_ids[entity_id]}"))
                excluded_paths.add(rel_path)
                continue
            seen_ids[entity_id] = rel_path
            records.append({
                "id": entity_id,
                "kind": field_text(frontmatter, "kind"),
                "name": field_text(frontmatter, "name"),
                "path": rel_path,
                "body": body,
                "frontmatter": frontmatter,
            })

    known_ids = {record["id"] for record in records}
    questions_by_id: dict[str, dict[str, Any]] = {}
    claims: list[dict[str, Any]] = []
    for record in records:
        record_definitions = question_definitions(record)
        record_claims = body_claims(record)
        local_question_ids = {definition["id"] for definition in record_definitions}
        unresolved_local_refs = sorted({
            question_ref
            for claim in record_claims
            for question_ref in claim["question_refs"]
            if question_ref not in local_question_ids
        })
        for question_ref in unresolved_local_refs:
            issues.append(EntityIssue(record["path"], f"unresolved_question_ref:{question_ref}"))
        claims.extend(record_claims)
        record["question_refs"] = sorted({
            definition["id"] for definition in record_definitions
        } | {
            question_ref
            for claim in record_claims
            for question_ref in claim["question_refs"]
        })
        for definition in record_definitions:
            question_id = definition["id"]
            if not definition["question"]:
                issues.append(EntityIssue(record["path"], f"empty_question_definition:{question_id}"))
                continue
            existing = questions_by_id.get(question_id)
            if existing is None:
                questions_by_id[question_id] = {
                    "id": question_id,
                    "question": definition["question"],
                    "session_ids": [definition["session_id"]] if definition["session_id"] else [],
                    "entity_ids": [record["id"]],
                    "paths": [record["path"]],
                }
            elif existing["question"] != definition["question"]:
                issues.append(EntityIssue(record["path"], f"conflicting_question_definition:{question_id}"))
            else:
                if definition["session_id"]:
                    existing["session_ids"] = sorted(set(existing["session_ids"] + [definition["session_id"]]))
                existing["entity_ids"] = sorted(set(existing["entity_ids"] + [record["id"]]))
                existing["paths"] = sorted(set(existing["paths"] + [record["path"]]))

    for record in records:
        for field, ref in reference_values(record["frontmatter"]):
            if ref not in known_ids:
                issues.append(EntityIssue(record["path"], f"unresolved_ref:{field}:{ref}"))
        funnel = record["frontmatter"].get("funnel")
        if funnel is not None and not isinstance(funnel, dict):
            issues.append(EntityIssue(record["path"], "invalid_funnel:not_object"))
        _latitude, _longitude, coordinate_issue = coordinate_values(record["frontmatter"])
        if coordinate_issue:
            issues.append(EntityIssue(record["path"], coordinate_issue))
        for link in body_links(record):
            target_id = link["target_entity_id"]
            if validate_id(target_id):
                issues.append(EntityIssue(record["path"], f"invalid_entity_link:{target_id}"))
            elif target_id == record["id"]:
                issues.append(EntityIssue(record["path"], f"self_entity_link:{target_id}"))
            elif target_id not in known_ids:
                issues.append(EntityIssue(record["path"], f"unresolved_entity_link:{target_id}"))

    views, view_issues = load_entity_views(project_root, known_ids)
    issues.extend(view_issues)

    records.sort(key=lambda item: (str(item["kind"]), str(item["name"]), str(item["id"])))
    claims.sort(key=lambda item: item["key"])
    questions = [questions_by_id[key] for key in sorted(questions_by_id)]
    issue_rows = [issue.__dict__ for issue in issues]
    source_material = json.dumps(
        {
            "entities": records,
            "views": views,
            "questions": questions,
            "claims": claims,
            "issues": issue_rows,
        },
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    source_fingerprint = hashlib.sha256(source_material.encode("utf-8")).hexdigest()
    return {
        "schema_version": 3,
        "source_fingerprint": source_fingerprint,
        "entity_root": ENTITY_ROOT.as_posix(),
        "view_config_path": VIEW_CONFIG_PATH.as_posix(),
        "index_path": ENTITY_INDEX_PATH.as_posix(),
        "required_frontmatter": list(REQUIRED_FIELDS),
        "entities": records,
        "by_id": {record["id"]: record for record in records},
        "views": views,
        "views_by_id": {view["id"]: view for view in views},
        "questions": questions,
        "claims": claims,
        "issues": issue_rows,
        "counts": {
            "included": len(records),
            "excluded": len(excluded_paths),
            "issues": len(issues),
        },
    }


def build_world_projection(registry: dict[str, Any], project_root: Path) -> dict[str, Any]:
    identity = project_identity(project_root)
    project_id = identity["id"]
    known_ids = set(registry["by_id"])
    nodes: list[dict[str, Any]] = []
    edges_by_key: dict[str, dict[str, Any]] = {}
    world_claims: list[dict[str, Any]] = []

    for record in registry["entities"]:
        frontmatter = record["frontmatter"]
        latitude, longitude, _issue = coordinate_values(frontmatter)
        node = {
            "key": f"{project_id}:{record['id']}",
            "project_id": project_id,
            "entity_id": record["id"],
            "kind": record["kind"],
            "name": record["name"],
            "path": record["path"],
            "location": field_text(frontmatter, "location") or None,
            "aliases": frontmatter.get("aliases", []),
            "frontmatter": frontmatter,
            "question_refs": record.get("question_refs", []),
        }
        if latitude is not None and longitude is not None:
            node["latitude"] = latitude
            node["longitude"] = longitude
        nodes.append(node)

        for link in body_links(record):
            target_id = link["target_entity_id"]
            if validate_id(target_id) or target_id not in known_ids or target_id == record["id"]:
                continue
            edge_material = "\0".join((record["id"], target_id, link["display_context"]))
            edge_hash = hashlib.sha256(edge_material.encode("utf-8")).hexdigest()[:16]
            edge_key = f"{project_id}:association:{edge_hash}"
            edges_by_key[edge_key] = {
                "key": edge_key,
                "project_id": project_id,
                "kind": "association",
                "directed": False,
                "source_key": f"{project_id}:{record['id']}",
                "source_entity_id": record["id"],
                "target_key": f"{project_id}:{target_id}",
                "target_entity_id": target_id,
                "label": link["label"],
                "context": link["context"],
                "display_context": link["display_context"],
                "path": record["path"],
                "section": link["section"],
                "question_refs": link["question_refs"],
            }

    nodes.sort(key=lambda item: item["key"])
    edges = [edges_by_key[key] for key in sorted(edges_by_key)]
    for claim in registry.get("claims", []):
        world_claims.append({
            **claim,
            "key": f"{project_id}:{claim['key']}",
            "project_id": project_id,
            "entity_key": f"{project_id}:{claim['entity_id']}",
        })

    world_questions: list[dict[str, Any]] = []
    for question in registry.get("questions", []):
        question_id = question["id"]
        entity_ids = sorted({
            *question["entity_ids"],
            *(
                claim["entity_id"]
                for claim in registry.get("claims", [])
                if question_id in claim["question_refs"]
            ),
        })
        world_questions.append({
            **question,
            "key": f"{project_id}:question:{question_id}",
            "project_id": project_id,
            "entity_ids": entity_ids,
            "entity_keys": [f"{project_id}:{entity_id}" for entity_id in entity_ids],
            "claim_keys": [
                f"{project_id}:{claim['key']}"
                for claim in registry.get("claims", [])
                if question_id in claim["question_refs"]
            ],
            "edge_keys": [edge["key"] for edge in edges if question_id in edge["question_refs"]],
        })
    issues = list(registry["issues"])
    return {
        "schema_version": 3,
        "source_fingerprint": registry["source_fingerprint"],
        "project": {
            "project_id": project_id,
            "name": identity["name"],
            "identity_source": identity["source"],
        },
        "nodes": nodes,
        "edges": edges,
        "questions": world_questions,
        "claims": world_claims,
        "views": list(registry.get("views", [])),
        "issues": issues,
        "counts": {
            "nodes": len(nodes),
            "located_nodes": sum("latitude" in node for node in nodes),
            "edges": len(edges),
            "issues": len(issues),
        },
    }


def build_crm_projection(registry: dict[str, Any], project_root: Path) -> dict[str, Any]:
    """Project funnel-bearing entities without creating a second source of truth."""
    identity = project_identity(project_root)
    project_id = identity["id"]
    entries: list[dict[str, Any]] = []
    for record in registry["entities"]:
        funnel = record["frontmatter"].get("funnel")
        if not isinstance(funnel, dict) or not funnel:
            continue
        entries.append({
            "key": f"{project_id}:{record['id']}",
            "project_id": project_id,
            "entity_id": record["id"],
            "kind": record["kind"],
            "name": record["name"],
            "path": record["path"],
            "funnel": funnel,
            "frontmatter": record["frontmatter"],
        })
    entries.sort(key=lambda item: item["key"])
    return {
        "schema_version": 3,
        "source_fingerprint": registry["source_fingerprint"],
        "project": {
            "project_id": project_id,
            "name": identity["name"],
            "identity_source": identity["source"],
        },
        "entities": entries,
        "by_id": {entry["entity_id"]: entry for entry in entries},
        "views": list(registry.get("views", [])),
        "issues": list(registry["issues"]),
        "counts": {
            "entities": len(entries),
            "issues": len(registry["issues"]),
        },
    }


def atomic_write_json(path: Path, payload: dict[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    file_descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(file_descriptor, "w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise
    return path


def write_entity_projections(
    project_root: Path,
    index: dict[str, Any],
    world: dict[str, Any],
    crm: dict[str, Any],
) -> tuple[Path, Path, Path]:
    index_path = atomic_write_json(project_root / ENTITY_INDEX_PATH, index)
    world_path = atomic_write_json(project_root / WORLD_VIEW_PATH, world)
    crm_path = atomic_write_json(project_root / CRM_VIEW_PATH, crm)
    return index_path, world_path, crm_path


def run_compile(args: argparse.Namespace) -> int:
    project_root = Path(args.project_root).expanduser().resolve()
    index = build_entity_index(project_root)
    world = build_world_projection(index, project_root)
    crm = build_crm_projection(index, project_root)
    if not args.no_write:
        write_entity_projections(project_root, index, world, crm)
    if args.json:
        print(json.dumps({"index": index, "world": world, "crm": crm}, indent=2, sort_keys=True))
    else:
        counts = index["counts"]
        action = "would compile" if args.no_write else "compiled"
        print(
            f"farplane entities {action}: {counts['included']} included, {counts['excluded']} excluded; "
            f"{world['counts']['edges']} associations, {crm['counts']['entities']} CRM entries -> "
            f"{project_root / ENTITY_INDEX_PATH}, {project_root / WORLD_VIEW_PATH}, {project_root / CRM_VIEW_PATH}"
        )
    return 1 if index["issues"] else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command")
    compile_parser = sub.add_parser("compile")
    compile_parser.add_argument("--project-root", default=".")
    compile_parser.add_argument("--no-write", action="store_true")
    compile_parser.add_argument("--json", action="store_true")
    compile_parser.set_defaults(func=run_compile)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
