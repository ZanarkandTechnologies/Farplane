#!/usr/bin/env python3
"""Compile flat Markdown-owned entities into generated project views."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
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
VIEW_PROJECTION_ROOT = Path(".farplane/views")
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
TIMELINE_ITEM_PATTERN = re.compile(
    r"^[ \t]*[-*+]\s+(\d{4}-\d{2}-\d{2})\s+(.+?)[ \t]*$",
    re.MULTILINE,
)
LIST_ITEM_PATTERN = re.compile(r"^[ \t]*[-*+]\s+", re.MULTILINE)
TIMELINE_TAG_PATTERN = re.compile(r"\[([a-z][a-z0-9-]*):([^\]\n]+)\]")
MARKDOWN_LINK_PATTERN = re.compile(r"\[([^\]\n]+)\]\([^\s)]+\)")
MARKDOWN_SOURCE_URL_PATTERN = re.compile(
    r"\[[^\]\n]+\]\((https?://[^\s)]+)\)"
)
VIEW_HEADING_PATTERN = re.compile(r"^view:\s*(.+)$", re.IGNORECASE)
AS_OF_PATTERN = re.compile(
    r"_?\s*as of:?\s*(\d{4}-\d{2}-\d{2})\s*_?",
    re.IGNORECASE,
)
TAG_QUANTITY_PATTERN = re.compile(
    r"^\s*([0-9][0-9,]*(?:\.[0-9]+)?)\s+([A-Za-z][A-Za-z0-9-]*)"
    r"(?:\s+(?:by|@)\s+(.+?))?\s*$",
    re.IGNORECASE,
)


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
            view = {"id": view_id, "name": name, "entity_ids": entity_ids}
            for field in (
                "resources",
                "problems",
                "relations",
                "resource_tags",
                "metric_tags",
                "status_weights",
                "confidence_weights",
            ):
                value = raw_view.get(field)
                if value is not None:
                    view[field] = value
            views.append(view)

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


def heading_path_at(body: str, offset: int) -> list[str]:
    """Return the active Markdown heading stack at one body offset."""
    stack: list[tuple[int, str]] = []
    for match in HEADING_PATTERN.finditer(body, 0, offset):
        level = len(match.group(0)) - len(match.group(0).lstrip("#"))
        while stack and stack[-1][0] >= level:
            stack.pop()
        stack.append((level, match.group(1).strip()))
    return [title for _level, title in stack]


def view_name_from_heading_path(path: list[str]) -> str | None:
    for heading in reversed(path):
        match = VIEW_HEADING_PATTERN.match(heading)
        if match:
            return match.group(1).strip()
    return None


def tagged_values(context: str) -> dict[str, list[str]]:
    tags: dict[str, list[str]] = {}
    for match in TIMELINE_TAG_PATTERN.finditer(context):
        key = match.group(1).strip()
        value = match.group(2).strip()
        if key and value:
            tags.setdefault(key, []).append(value)
    return {key: sorted(set(values)) for key, values in sorted(tags.items())}


def display_markdown_context(context: str) -> str:
    without_tags = TIMELINE_TAG_PATTERN.sub("", context)
    display = ENTITY_LINK_PATTERN.sub(lambda link: link.group(1), without_tags)
    display = MARKDOWN_LINK_PATTERN.sub(lambda link: link.group(1), display)
    return re.sub(r"\s+", " ", display).strip()


def source_urls(context: str) -> list[str]:
    return sorted(set(MARKDOWN_SOURCE_URL_PATTERN.findall(context)))


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
            "display_context": display_markdown_context(context),
            "section": section_at(body, match.start()),
            "occurrence": occurrence,
            "question_refs": sorted(set(QUESTION_REF_PATTERN.findall(searchable_body[block_start:block_end]))),
            "source_urls": source_urls(body[block_start:block_end]),
        })
    return links


def body_view_statuses(record: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract freeform per-view latest-status sections as node context."""
    body = str(record.get("body") or "")
    headings = list(HEADING_PATTERN.finditer(body))
    statuses: list[dict[str, Any]] = []
    for index, heading in enumerate(headings):
        if heading.group(1).strip().casefold() != "latest status":
            continue
        path = heading_path_at(body, heading.start())
        view_name = view_name_from_heading_path(path)
        if not view_name:
            continue
        level = len(heading.group(0)) - len(heading.group(0).lstrip("#"))
        end = len(body)
        for candidate in headings[index + 1:]:
            candidate_level = len(candidate.group(0)) - len(candidate.group(0).lstrip("#"))
            if candidate_level <= level:
                end = candidate.start()
                break
        context = normalized_claim_context(body[heading.end():end])
        if not context:
            continue
        as_of_match = AS_OF_PATTERN.search(context)
        without_as_of = AS_OF_PATTERN.sub("", context)
        display_context = display_markdown_context(without_as_of).strip(" -")
        key_material = "\0".join(
            (record["id"], view_name.casefold(), as_of_match.group(1) if as_of_match else "", display_context)
        )
        status_hash = hashlib.sha256(key_material.encode("utf-8")).hexdigest()[:16]
        statuses.append({
            "key": f"view-status:{status_hash}",
            "entity_id": record["id"],
            "view_name": view_name,
            "as_of": as_of_match.group(1) if as_of_match else None,
            "context": context,
            "display_context": display_context,
            "tags": tagged_values(context),
            "source_urls": source_urls(context),
            "path": record["path"],
        })
    return statuses


def body_timeline(record: dict[str, Any]) -> list[dict[str, Any]]:
    """Compile dated Timeline bullets without promoting them to graph nodes."""
    body = str(record.get("body") or "")
    searchable_body = mask_question_definitions(mask_markdown_code(body))
    item_matches = list(TIMELINE_ITEM_PATTERN.finditer(searchable_body))
    entries: list[dict[str, Any]] = []

    for match in item_matches:
        heading_path = heading_path_at(body, match.start())
        section = heading_path[-1] if heading_path else None
        if not section or section.casefold() != "timeline":
            continue
        try:
            date_type.fromisoformat(match.group(1))
        except ValueError:
            continue

        end = match.end()
        cursor = match.end()
        while cursor < len(searchable_body) and searchable_body[cursor] == "\n":
            line_start = cursor + 1
            line_end = searchable_body.find("\n", line_start)
            if line_end == -1:
                line_end = len(searchable_body)
            line = searchable_body[line_start:line_end]
            if not line.strip() or not line[:1].isspace():
                break
            end = line_end
            cursor = line_end
        content = match.group(2) + body[match.end():end]
        context = normalized_claim_context(content)
        tags = tagged_values(context)
        display_context = display_markdown_context(context)
        entity_ids = sorted({
            record["id"],
            *(link.group(2).strip() for link in ENTITY_LINK_PATTERN.finditer(context)),
        })
        source_url_material = "\0".join(source_urls(context))
        tag_material = json.dumps(tags, sort_keys=True, separators=(",", ":"))
        key_material = "\0".join(
            (
                record["id"],
                match.group(1),
                "\0".join(entity_ids),
                source_url_material,
                display_context,
                tag_material,
            )
        )
        entry_hash = hashlib.sha256(key_material.encode("utf-8")).hexdigest()[:16]
        entries.append({
            "key": f"timeline:{entry_hash}",
            "date": match.group(1),
            "source_entity_id": record["id"],
            "entity_ids": entity_ids,
            "context": context,
            "display_context": display_context,
            "tags": tags,
            "view_name": view_name_from_heading_path(heading_path),
            "source_urls": source_urls(context),
            "path": record["path"],
            "section": section,
            "question_refs": sorted(set(QUESTION_REF_PATTERN.findall(content))),
        })

    return entries


def build_entity_registry(project_root: Path) -> dict[str, Any]:
    """Parse canonical entity sources into the compiler's private working set."""
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
    timeline: list[dict[str, Any]] = []
    view_statuses: list[dict[str, Any]] = []
    for record in records:
        record_definitions = question_definitions(record)
        record_claims = body_claims(record)
        timeline.extend(body_timeline(record))
        view_statuses.extend(body_view_statuses(record))
        if re.search(r"```farplane(?:[ \t]|$)", str(record.get("body") or ""), re.MULTILINE):
            issues.append(EntityIssue(record["path"], "retired_farplane_metadata_fence"))
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
    timeline.sort(key=lambda item: (item["date"], item["key"]), reverse=True)
    view_statuses.sort(key=lambda item: (item["view_name"], item["entity_id"], item["key"]))
    questions = [questions_by_id[key] for key in sorted(questions_by_id)]
    issue_rows = [issue.__dict__ for issue in issues]
    source_material = json.dumps(
        {
            "entities": records,
            "views": views,
            "questions": questions,
            "claims": claims,
            "timeline": timeline,
            "view_statuses": view_statuses,
            "issues": issue_rows,
        },
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    source_fingerprint = hashlib.sha256(source_material.encode("utf-8")).hexdigest()
    return {
        "source_fingerprint": source_fingerprint,
        "entities": records,
        "by_id": {record["id"]: record for record in records},
        "views": views,
        "questions": questions,
        "claims": claims,
        "timeline": timeline,
        "view_statuses": view_statuses,
        "issues": issue_rows,
        "counts": {
            "included": len(records),
            "excluded": len(excluded_paths),
            "issues": len(issues),
        },
    }


def build_entity_index(registry: dict[str, Any]) -> dict[str, Any]:
    """Serialize the bounded lookup catalogue, not the parsed document store."""
    entities: list[dict[str, Any]] = []
    for record in registry["entities"]:
        frontmatter = record["frontmatter"]
        entry: dict[str, Any] = {
            "id": record["id"],
            "kind": record["kind"],
            "name": record["name"],
            "path": record["path"],
        }
        aliases = frontmatter.get("aliases")
        if isinstance(aliases, list):
            normalized_aliases = sorted({
                str(alias).strip()
                for alias in aliases
                if str(alias).strip()
            })
            if normalized_aliases:
                entry["aliases"] = normalized_aliases
        location = field_text(frontmatter, "location")
        if location:
            entry["location"] = location
        references: dict[str, list[str]] = {}
        for field, ref in reference_values(frontmatter):
            references.setdefault(field, []).append(ref)
        for field, refs in sorted(references.items()):
            entry[field] = sorted(set(refs)) if field.endswith("_refs") else refs[0]
        question_refs = record.get("question_refs", [])
        if question_refs:
            entry["question_refs"] = list(question_refs)
        entities.append(entry)

    return {
        "schema_version": 5,
        "source_fingerprint": registry["source_fingerprint"],
        "entities": entities,
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
                "source_urls": link["source_urls"],
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
    world_timeline = [
        {
            **entry,
            "key": f"{project_id}:{entry['key']}",
            "project_id": project_id,
            "entity_keys": [f"{project_id}:{entity_id}" for entity_id in entry["entity_ids"]],
        }
        for entry in registry.get("timeline", [])
    ]
    return {
        "schema_version": 4,
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
        "timeline": world_timeline,
        "views": [
            {key: view[key] for key in ("id", "name", "entity_ids")}
            for view in registry.get("views", [])
        ],
    }


def numeric_weight_map(
    value: Any,
    field: str,
    issues: list[dict[str, str]],
) -> dict[str, float]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        issues.append({"path": VIEW_CONFIG_PATH.as_posix(), "reason": f"{field}_not_object"})
        return {}
    weights: dict[str, float] = {}
    for raw_key, raw_weight in value.items():
        key = str(raw_key).strip()
        if validate_id(key):
            issues.append({
                "path": VIEW_CONFIG_PATH.as_posix(),
                "reason": f"invalid_{field}_key:{key}",
            })
            continue
        if isinstance(raw_weight, bool):
            issues.append({
                "path": VIEW_CONFIG_PATH.as_posix(),
                "reason": f"invalid_{field}_weight:{key}",
            })
            continue
        try:
            weight = float(raw_weight)
        except (TypeError, ValueError):
            issues.append({
                "path": VIEW_CONFIG_PATH.as_posix(),
                "reason": f"invalid_{field}_weight:{key}",
            })
            continue
        if not math.isfinite(weight) or not 0 <= weight <= 1:
            issues.append({
                "path": VIEW_CONFIG_PATH.as_posix(),
                "reason": f"invalid_{field}_weight:{key}",
            })
            continue
        weights[key] = weight
    return weights


def first_tag(tags: dict[str, list[str]], key: str) -> str:
    values = tags.get(key, [])
    return values[0].strip() if values else ""


def timeline_matches_view(entry: dict[str, Any], view: dict[str, Any]) -> bool:
    tags = entry.get("tags")
    if not isinstance(tags, dict):
        return False
    tagged_view = first_tag(tags, "view")
    if tagged_view:
        return tagged_view.casefold() in {view["id"].casefold(), view["name"].casefold()}
    section_view = str(entry.get("view_name") or "").strip()
    return section_view.casefold() in {view["id"].casefold(), view["name"].casefold()}


def detect_relation(context: str, tags: dict[str, list[str]], view: dict[str, Any]) -> str:
    explicit = first_tag(tags, "relation") or first_tag(tags, "type")
    if explicit:
        return explicit
    normalized_context = context.casefold()
    relations = view.get("relations", {})
    if not isinstance(relations, dict):
        return "event"
    for raw_relation, raw_definition in relations.items():
        relation = str(raw_relation).strip()
        if isinstance(raw_definition, dict):
            patterns = raw_definition.get("patterns", [])
        else:
            patterns = raw_definition
        if isinstance(patterns, list) and any(
            isinstance(pattern, str) and pattern.casefold() in normalized_context
            for pattern in patterns
        ):
            return relation
    return "event"


def parse_tag_quantity(raw: str) -> tuple[float, str, str | None] | None:
    match = TAG_QUANTITY_PATTERN.match(raw)
    if not match:
        return None
    value = float(match.group(1).replace(",", ""))
    return value, match.group(2), match.group(3).strip() if match.group(3) else None


def build_view_projection(
    registry: dict[str, Any],
    world: dict[str, Any],
    view: dict[str, Any],
) -> dict[str, Any]:
    """Compile one typed view without changing generic World graph semantics."""
    view_id = view["id"]
    issues: list[dict[str, str]] = []
    raw_resources = view.get("resources", {})
    if not isinstance(raw_resources, dict):
        issues.append({"path": VIEW_CONFIG_PATH.as_posix(), "reason": "resources_not_object"})
        raw_resources = {}
    resources: dict[str, dict[str, Any]] = {}
    for raw_resource_id, raw_resource in raw_resources.items():
        resource_id = str(raw_resource_id).strip()
        if validate_id(resource_id) or not isinstance(raw_resource, dict):
            issues.append({
                "path": VIEW_CONFIG_PATH.as_posix(),
                "reason": f"invalid_resource:{resource_id}",
            })
            continue
        name = field_text(raw_resource, "name")
        base_unit = field_text(raw_resource, "base_unit")
        raw_units = raw_resource.get("units")
        if not name or not base_unit or not isinstance(raw_units, dict) or not raw_units:
            issues.append({
                "path": VIEW_CONFIG_PATH.as_posix(),
                "reason": f"invalid_resource_schema:{resource_id}",
            })
            continue
        units: dict[str, float] = {}
        for raw_unit, raw_factor in raw_units.items():
            unit = str(raw_unit).strip()
            if not unit or isinstance(raw_factor, bool):
                continue
            try:
                factor = float(raw_factor)
            except (TypeError, ValueError):
                continue
            if math.isfinite(factor) and factor > 0:
                units[unit] = factor
        if base_unit not in units or not math.isclose(units[base_unit], 1.0):
            issues.append({
                "path": VIEW_CONFIG_PATH.as_posix(),
                "reason": f"invalid_resource_base_unit:{resource_id}:{base_unit}",
            })
            continue
        resources[resource_id] = {
            "id": resource_id,
            "name": name,
            "measure": field_text(raw_resource, "measure") or "quantity",
            "base_unit": base_unit,
            "units": units,
        }

    raw_problems = view.get("problems", {})
    if not isinstance(raw_problems, dict):
        issues.append({"path": VIEW_CONFIG_PATH.as_posix(), "reason": "problems_not_object"})
        raw_problems = {}
    problems: list[dict[str, Any]] = []
    for raw_problem_id, raw_problem in raw_problems.items():
        problem_id = str(raw_problem_id).strip()
        if validate_id(problem_id) or not isinstance(raw_problem, dict):
            issues.append({
                "path": VIEW_CONFIG_PATH.as_posix(),
                "reason": f"invalid_problem:{problem_id}",
            })
            continue
        resource_ids = raw_problem.get("resources")
        if not isinstance(resource_ids, list) or not resource_ids:
            issues.append({
                "path": VIEW_CONFIG_PATH.as_posix(),
                "reason": f"invalid_problem_resources:{problem_id}",
            })
            continue
        normalized_resource_ids = [str(item).strip() for item in resource_ids]
        unknown = [item for item in normalized_resource_ids if item not in resources]
        if unknown:
            issues.append({
                "path": VIEW_CONFIG_PATH.as_posix(),
                "reason": f"unknown_problem_resource:{problem_id}:{','.join(unknown)}",
            })
            continue
        problems.append({
            "id": problem_id,
            "name": field_text(raw_problem, "name") or problem_id.replace("-", " ").title(),
            "resources": normalized_resource_ids,
        })

    status_weights = numeric_weight_map(view.get("status_weights"), "status", issues)
    confidence_weights = numeric_weight_map(
        view.get("confidence_weights"), "confidence", issues
    )
    known_ids = set(registry["by_id"])
    view_entity_ids = set(view["entity_ids"])
    events: list[dict[str, Any]] = []
    observations: list[dict[str, Any]] = []
    resource_flows: list[dict[str, Any]] = []
    raw_resource_tags = view.get("resource_tags", {})
    if not isinstance(raw_resource_tags, dict):
        issues.append({"path": VIEW_CONFIG_PATH.as_posix(), "reason": "resource_tags_not_object"})
        raw_resource_tags = {}
    raw_metric_tags = view.get("metric_tags", {})
    if not isinstance(raw_metric_tags, dict):
        issues.append({"path": VIEW_CONFIG_PATH.as_posix(), "reason": "metric_tags_not_object"})
        raw_metric_tags = {}

    for entry in registry.get("timeline", []):
        if not timeline_matches_view(entry, view):
            continue
        tags = entry.get("tags", {})
        event_status = first_tag(tags, "status")
        event_confidence = first_tag(tags, "confidence")
        if event_status and event_status not in status_weights:
            issues.append({"path": entry["path"], "reason": f"unknown_status:{event_status}"})
        if event_confidence and event_confidence not in confidence_weights:
            issues.append({
                "path": entry["path"],
                "reason": f"unknown_confidence:{event_confidence}",
            })
        metrics: list[dict[str, Any]] = []
        for tag_key, raw_definition in raw_metric_tags.items():
            if tag_key not in tags or not isinstance(raw_definition, dict):
                continue
            for raw_value in tags[tag_key]:
                parsed = parse_tag_quantity(raw_value)
                if not parsed:
                    issues.append({
                        "path": entry["path"],
                        "reason": f"invalid_metric_tag:{tag_key}:{raw_value}",
                    })
                    continue
                value, unit, horizon = parsed
                expected_unit = field_text(raw_definition, "unit")
                if expected_unit and unit != expected_unit:
                    issues.append({
                        "path": entry["path"],
                        "reason": f"invalid_metric_unit:{tag_key}:{unit}",
                    })
                    continue
                metric = {"key": tag_key, "value": value, "unit": unit}
                if horizon:
                    metric["horizon"] = horizon
                metrics.append(metric)
        event = {
            **entry,
            "event_type": detect_relation(entry["display_context"], tags, view),
            "status": event_status or None,
            "confidence": event_confidence or None,
            "signals": tags.get("signal", []),
            "metrics": metrics,
        }
        events.append(event)

        for tag_key, raw_definition in raw_resource_tags.items():
            if tag_key not in tags:
                continue
            if not isinstance(raw_definition, dict):
                issues.append({
                    "path": VIEW_CONFIG_PATH.as_posix(),
                    "reason": f"invalid_resource_tag:{tag_key}:not_object",
                })
                continue
            resource_id = field_text(raw_definition, "resource")
            direction = field_text(raw_definition, "direction")
            entity_selector = field_text(raw_definition, "entity") or "source"
            transfer = field_text(raw_definition, "transfer")
            if resource_id not in resources:
                issues.append({
                    "path": VIEW_CONFIG_PATH.as_posix(),
                    "reason": f"invalid_resource_tag:{tag_key}:unknown_resource:{resource_id}",
                })
                continue
            if direction not in {"supply", "demand"}:
                issues.append({
                    "path": VIEW_CONFIG_PATH.as_posix(),
                    "reason": f"invalid_resource_tag:{tag_key}:invalid_direction:{direction}",
                })
                continue
            if transfer and transfer not in {"source-to-linked", "linked-to-source"}:
                issues.append({
                    "path": VIEW_CONFIG_PATH.as_posix(),
                    "reason": f"invalid_resource_tag:{tag_key}:invalid_transfer:{transfer}",
                })
                continue
            linked_ids = [
                entity_id
                for entity_id in entry["entity_ids"]
                if entity_id != entry["source_entity_id"]
            ]
            if entity_selector == "source":
                entity_id = entry["source_entity_id"]
            elif entity_selector == "linked" and len(linked_ids) == 1:
                entity_id = linked_ids[0]
            else:
                issues.append({
                    "path": entry["path"],
                    "reason": f"ambiguous_resource_entity:{tag_key}:{entity_selector}",
                })
                continue
            if entity_id not in known_ids:
                issues.append({"path": entry["path"], "reason": f"unknown_entity:{entity_id}"})
                continue
            for index, raw_value in enumerate(tags[tag_key]):
                parsed = parse_tag_quantity(raw_value)
                if not parsed:
                    issues.append({
                        "path": entry["path"],
                        "reason": f"invalid_resource_value:{tag_key}:{raw_value}",
                    })
                    continue
                value, unit, horizon = parsed
                if unit not in resources[resource_id]["units"]:
                    issues.append({
                        "path": entry["path"],
                        "reason": f"invalid_resource_unit:{tag_key}:{unit}",
                    })
                    continue
                normalized_value = value * resources[resource_id]["units"][unit]
                status_weight = status_weights.get(event_status, 1.0)
                confidence_weight = confidence_weights.get(event_confidence, 1.0)
                observation = {
                    "key": f"{entry['key']}:resource:{tag_key}:{index}",
                    "event_key": entry["key"],
                    "date": entry["date"],
                    "entity_id": entity_id,
                    "resource": resource_id,
                    "resource_tag": tag_key,
                    "direction": direction,
                    "value": value,
                    "unit": unit,
                    "normalized_value": normalized_value,
                    "base_unit": resources[resource_id]["base_unit"],
                    "status": event_status or None,
                    "confidence": event_confidence or None,
                    "status_weight": status_weight,
                    "confidence_weight": confidence_weight,
                    "weighted_value": normalized_value * status_weight * confidence_weight,
                    "horizon": horizon,
                    "evidence": entry["display_context"],
                    "source_urls": entry.get("source_urls", []),
                    "path": entry["path"],
                }
                observations.append(observation)
                if not transfer:
                    continue
                if len(linked_ids) != 1:
                    issues.append({
                        "path": entry["path"],
                        "reason": f"ambiguous_resource_transfer:{tag_key}",
                    })
                    continue
                linked_id = linked_ids[0]
                if linked_id not in view_entity_ids:
                    continue
                if transfer == "source-to-linked":
                    from_entity_id = entry["source_entity_id"]
                    to_entity_id = linked_id
                else:
                    from_entity_id = linked_id
                    to_entity_id = entry["source_entity_id"]
                resource_flows.append({
                    "key": f"{entry['key']}:flow:{tag_key}:{index}",
                    "event_key": entry["key"],
                    "date": entry["date"],
                    "resource": resource_id,
                    "resource_tag": tag_key,
                    "from_entity_id": from_entity_id,
                    "to_entity_id": to_entity_id,
                    "value": value,
                    "unit": unit,
                    "normalized_value": normalized_value,
                    "base_unit": resources[resource_id]["base_unit"],
                    "status": event_status or None,
                    "confidence": event_confidence or None,
                    "horizon": horizon,
                    "evidence": entry["display_context"],
                    "source_urls": entry.get("source_urls", []),
                    "path": entry["path"],
                })

    summaries: list[dict[str, Any]] = []
    for resource_id, resource in resources.items():
        rows = [row for row in observations if row["resource"] == resource_id]
        supply = sum(row["weighted_value"] for row in rows if row["direction"] == "supply")
        demand = sum(row["weighted_value"] for row in rows if row["direction"] == "demand")
        summaries.append({
            "resource": resource_id,
            "name": resource["name"],
            "base_unit": resource["base_unit"],
            "supply": supply,
            "demand": demand,
            "balance": supply - demand,
            "observation_count": len(rows),
        })

    entity_ids = view_entity_ids
    status_by_entity = {
        status["entity_id"]: status
        for status in registry.get("view_statuses", [])
        if str(status.get("view_name") or "").casefold()
        in {view_id.casefold(), view["name"].casefold()}
    }
    entities = [
        {**node, "view_status": status_by_entity.get(node["entity_id"])}
        for node in world["nodes"]
        if node["entity_id"] in entity_ids
    ]
    generic_edges = [
        edge
        for edge in world["edges"]
        if edge["source_entity_id"] in entity_ids and edge["target_entity_id"] in entity_ids
    ]
    observations_by_event: dict[str, list[dict[str, Any]]] = {}
    for observation in observations:
        observations_by_event.setdefault(observation["event_key"], []).append(observation)
    flows_by_event: dict[str, list[dict[str, Any]]] = {}
    for flow in resource_flows:
        flows_by_event.setdefault(flow["event_key"], []).append(flow)

    relationship_claims: dict[tuple[str, str], list[dict[str, Any]]] = {}
    seen_claims: set[tuple[tuple[str, str], str, str]] = set()
    for event in events:
        linked_ids = [
            entity_id
            for entity_id in event["entity_ids"]
            if entity_id != event["source_entity_id"] and entity_id in entity_ids
        ]
        event_resources = sorted({
            row["resource"] for row in observations_by_event.get(event["key"], [])
        })
        for linked_id in linked_ids:
            pair = tuple(sorted((event["source_entity_id"], linked_id)))
            event_flows = [
                flow
                for flow in flows_by_event.get(event["key"], [])
                if set((flow["from_entity_id"], flow["to_entity_id"])) == set(pair)
            ]
            fingerprint = (pair, event["path"], event["display_context"].casefold())
            seen_claims.add(fingerprint)
            relationship_claims.setdefault(pair, []).append({
                "key": event["key"],
                "date": event["date"],
                "event_key": event["key"],
                "relation": event["event_type"],
                "display_context": event["display_context"],
                "path": event["path"],
                "source_urls": event.get("source_urls", []),
                "resource_ids": event_resources,
                "resource_flows": event_flows,
            })

    for edge in generic_edges:
        pair = tuple(sorted((edge["source_entity_id"], edge["target_entity_id"])))
        display_context = display_markdown_context(edge["display_context"])
        fingerprint = (pair, edge["path"], display_context.casefold())
        timeline_pair = any(
            seen_pair == pair and seen_path == edge["path"]
            for seen_pair, seen_path, _context in seen_claims
        )
        if fingerprint in seen_claims or (
            str(edge.get("section") or "").casefold() == "timeline" and timeline_pair
        ):
            continue
        relationship_claims.setdefault(pair, []).append({
            "key": edge["key"],
            "date": None,
            "event_key": None,
            "relation": detect_relation(display_context, {}, view),
            "display_context": display_context,
            "path": edge["path"],
            "source_urls": edge.get("source_urls", []),
            "resource_ids": [],
            "resource_flows": [],
        })

    relationships: list[dict[str, Any]] = []
    for pair, claims in relationship_claims.items():
        claims.sort(
            key=lambda claim: (
                claim["date"] is not None,
                claim["date"] or "",
                claim["key"],
            ),
            reverse=True,
        )
        latest = claims[0]
        relationship_flows = {
            flow["key"]: flow
            for claim in claims
            for flow in claim["resource_flows"]
        }
        sorted_flows = sorted(
            relationship_flows.values(),
            key=lambda flow: (flow["date"], flow["key"]),
            reverse=True,
        )
        relationship_hash = hashlib.sha256("\0".join(pair).encode("utf-8")).hexdigest()[:16]
        relationships.append({
            "key": f"relationship:{relationship_hash}",
            "source_entity_id": pair[0],
            "target_entity_id": pair[1],
            "directed": False,
            "relation_types": sorted({claim["relation"] for claim in claims}),
            "resource_ids": sorted({
                resource_id
                for claim in claims
                for resource_id in claim["resource_ids"]
            }),
            "resource_flows": sorted_flows,
            "latest_date": latest["date"],
            "latest_context": latest["display_context"],
            "latest_event_key": latest["event_key"],
            "event_count": len(claims),
            "timeline": claims,
        })

    events.sort(key=lambda item: (item["date"], item["key"]), reverse=True)
    observations.sort(key=lambda item: (item["date"], item["key"]), reverse=True)
    resource_flows.sort(key=lambda item: (item["date"], item["key"]), reverse=True)
    relationships.sort(
        key=lambda item: (item["latest_date"] or "", item["key"]),
        reverse=True,
    )
    summaries.sort(key=lambda item: item["resource"])
    problems.sort(key=lambda item: item["id"])
    return {
        "schema_version": 4,
        "source_fingerprint": registry["source_fingerprint"],
        "project": world["project"],
        "view": {
            "id": view_id,
            "name": view["name"],
            "resources": resources,
            "problems": problems,
            "status_weights": status_weights,
            "confidence_weights": confidence_weights,
        },
        "entities": entities,
        "relationships": relationships,
        "events": events,
        "observations": observations,
        "resource_flows": resource_flows,
        "resource_summaries": summaries,
        "issues": issues,
        "counts": {
            "entities": len(entities),
            "edges": len(relationships),
            "events": len(events),
            "observations": len(observations),
            "resource_flows": len(resource_flows),
            "issues": len(issues),
        },
    }


def build_view_projections(
    registry: dict[str, Any],
    world: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    return {
        view["id"]: build_view_projection(registry, world, view)
        for view in registry.get("views", [])
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
        })
    entries.sort(key=lambda item: item["key"])
    return {
        "schema_version": 4,
        "source_fingerprint": registry["source_fingerprint"],
        "project": {
            "project_id": project_id,
            "name": identity["name"],
            "identity_source": identity["source"],
        },
        "entities": entries,
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
    view_projections: dict[str, dict[str, Any]] | None = None,
) -> tuple[Path, Path, Path]:
    index_path = atomic_write_json(project_root / ENTITY_INDEX_PATH, index)
    world_path = atomic_write_json(project_root / WORLD_VIEW_PATH, world)
    crm_path = atomic_write_json(project_root / CRM_VIEW_PATH, crm)
    projections = view_projections or {}
    view_root = project_root / VIEW_PROJECTION_ROOT
    for view_id, projection in projections.items():
        atomic_write_json(view_root / f"{view_id}.json", projection)
    if view_root.exists():
        current_view_ids = set(projections)
        for stale_path in view_root.glob("*.json"):
            if stale_path.stem not in current_view_ids:
                stale_path.unlink()
    return index_path, world_path, crm_path


def run_compile(args: argparse.Namespace) -> int:
    project_root = Path(args.project_root).expanduser().resolve()
    registry = build_entity_registry(project_root)
    index = build_entity_index(registry)
    world = build_world_projection(registry, project_root)
    crm = build_crm_projection(registry, project_root)
    view_projections = build_view_projections(registry, world)
    if not args.no_write:
        write_entity_projections(project_root, index, world, crm, view_projections)
    if args.json:
        print(json.dumps(
            {
                "index": index,
                "world": world,
                "crm": crm,
                "views": view_projections,
                "diagnostics": {
                    "issues": registry["issues"],
                    "counts": registry["counts"],
                    "view_issue_count": sum(
                        projection["counts"]["issues"]
                        for projection in view_projections.values()
                    ),
                },
            },
            indent=2,
            sort_keys=True,
        ))
    else:
        counts = registry["counts"]
        action = "would compile" if args.no_write else "compiled"
        print(
            f"farplane entities {action}: {counts['included']} included, {counts['excluded']} excluded; "
            f"{len(world['edges'])} associations, {len(crm['entities'])} CRM entries -> "
            f"{project_root / ENTITY_INDEX_PATH}, {project_root / WORLD_VIEW_PATH}, "
            f"{project_root / CRM_VIEW_PATH}, {project_root / VIEW_PROJECTION_ROOT}"
        )
        for issue in registry["issues"]:
            print(f"entity issue: {issue['path']}: {issue['reason']}", file=sys.stderr)
        for view_id, projection in view_projections.items():
            for issue in projection["issues"]:
                print(
                    f"view issue: {view_id}: {issue['path']}: {issue['reason']}",
                    file=sys.stderr,
                )
    view_issue_count = sum(
        projection["counts"]["issues"] for projection in view_projections.values()
    )
    return 1 if registry["issues"] or view_issue_count else 0


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
