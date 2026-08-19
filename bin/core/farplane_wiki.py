#!/usr/bin/env python3
"""Search and incrementally project canonical Farplane Wiki Markdown."""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any

from farplane_entities import (
    CRM_VIEW_PATH,
    ENTITY_INDEX_PATH,
    ENTITY_ROOT,
    VIEW_PROJECTION_ROOT,
    GRAPH_VIEW_PATH,
    EntityIssue,
    build_crm_projection,
    build_entity_index,
    build_entity_registry,
    build_view_projections,
    build_graph_projection,
    finalize_entity_registry,
    parse_entity_record,
)
from farplane_wiki_store import (
    WIKI_DATABASE_PATH,
    WIKI_SCHEMA_VERSION,
    WikiStoreError,
    connect_database,
    delete_page_by_path,
    discard_generated_bundle,
    metadata,
    normalize_identity,
    promote_generated_bundle,
    replace_page,
    require_runtime,
    runtime_status,
    set_metadata,
    source_hash,
    stage_incremental_bundle,
    stage_rebuild_bundle,
    views_hash,
)


WORD_PATTERN = re.compile(r"[^\W_]+", re.UNICODE)


class WikiError(RuntimeError):
    """Actionable Wiki command failure."""


def build_bundle(project_root: Path, registry: dict[str, Any]) -> dict[str, Any]:
    index = build_entity_index(registry)
    graph = build_graph_projection(registry, project_root)
    crm = build_crm_projection(registry, project_root)
    views = build_view_projections(registry, graph)
    view_issues = [
        issue
        for projection in views.values()
        for issue in projection.get("issues", [])
    ]
    return {
        "registry": registry,
        "index": index,
        "graph": graph,
        "crm": crm,
        "views": views,
        "diagnostics": {
            "issues": [*registry["issues"], *view_issues],
            "counts": registry["counts"],
            "view_issue_count": len(view_issues),
        },
    }


def public_bundle_payload(
    bundle: dict[str, Any],
    action: str,
    changed_pages: list[str],
    removed_pages: list[str],
    written: bool,
) -> dict[str, Any]:
    return {
        "ok": not bundle["diagnostics"]["issues"],
        "action": action,
        "written": written,
        "changed_pages": changed_pages,
        "removed_pages": removed_pages,
        "database_path": WIKI_DATABASE_PATH.as_posix(),
        "projection_paths": [
            ENTITY_INDEX_PATH.as_posix(),
            GRAPH_VIEW_PATH.as_posix(),
            CRM_VIEW_PATH.as_posix(),
            *[
                (VIEW_PROJECTION_ROOT / f"{view_id}.json").as_posix()
                for view_id in sorted(bundle["views"])
            ],
        ],
        "source_fingerprint": bundle["registry"]["source_fingerprint"],
        "counts": {
            **bundle["registry"]["counts"],
            "edges": len(bundle["graph"]["edges"]),
        },
        "diagnostics": bundle["diagnostics"],
    }


def discover_hashes(project_root: Path) -> tuple[dict[str, str], list[EntityIssue]]:
    root = project_root / ENTITY_ROOT
    hashes: dict[str, str] = {}
    issues: list[EntityIssue] = []
    if not root.exists():
        return hashes, issues
    for path in sorted(root.rglob("*.md")):
        relative = path.relative_to(project_root).as_posix()
        if path.parent != root:
            issues.append(EntityIssue(relative, "nested_entity_path"))
            continue
        hashes[relative] = source_hash(path)
    return hashes, issues


def rebuild(project_root: Path, no_write: bool = False) -> dict[str, Any]:
    registry = build_entity_registry(project_root)
    bundle = build_bundle(project_root, registry)
    hashes, _hash_issues = discover_hashes(project_root)
    changed_pages = sorted(hashes)
    written = False
    if not bundle["diagnostics"]["issues"] and not no_write:
        require_runtime()
        stage_root = stage_rebuild_bundle(project_root, bundle, hashes)
        promote_generated_bundle(project_root, stage_root, bundle)
        written = True
    return public_bundle_payload(bundle, "rebuild", changed_pages, [], written)


def load_cached_pages(
    connection: sqlite3.Connection,
) -> tuple[dict[str, dict[str, Any]], dict[str, str]]:
    cached: dict[str, dict[str, Any]] = {}
    hashes: dict[str, str] = {}
    try:
        rows = connection.execute(
            "SELECT path, source_hash, record_json FROM pages ORDER BY path"
        )
        for row in rows:
            path = str(row["path"])
            cached[path] = json.loads(str(row["record_json"]))
            hashes[path] = str(row["source_hash"])
    except (sqlite3.Error, json.JSONDecodeError) as exc:
        raise WikiError(f"wiki_database_invalid:{exc}") from exc
    return cached, hashes


def validate_requested_paths(project_root: Path, requested: list[str]) -> set[str]:
    resolved_root = project_root.resolve()
    entity_root = (resolved_root / ENTITY_ROOT).resolve()
    relative_paths: set[str] = set()
    for raw in requested:
        candidate = Path(raw).expanduser()
        resolved = (
            candidate.resolve()
            if candidate.is_absolute()
            else (resolved_root / candidate).resolve()
        )
        if resolved.parent != entity_root or resolved.suffix != ".md":
            raise WikiError(f"wiki_sync_path_outside_entity_root:{raw}")
        relative_paths.add(resolved.relative_to(resolved_root).as_posix())
    return relative_paths


def sync(
    project_root: Path,
    requested_paths: list[str] | None = None,
    no_write: bool = False,
) -> dict[str, Any]:
    requested = requested_paths or []
    selected_paths = validate_requested_paths(project_root, requested)
    database_path = project_root / WIKI_DATABASE_PATH
    if not database_path.exists():
        return rebuild(project_root, no_write=no_write)
    connection = connect_database(database_path)
    try:
        meta = metadata(connection)
        if meta.get("schema_version") != str(WIKI_SCHEMA_VERSION):
            return rebuild(project_root, no_write=no_write)
        cached, cached_hashes = load_cached_pages(connection)
    finally:
        connection.close()

    current_hashes, discovery_issues = discover_hashes(project_root)
    all_dirty_paths = {
        path for path, digest in current_hashes.items() if cached_hashes.get(path) != digest
    }
    all_removed_paths = set(cached_hashes) - set(current_hashes)
    dirty_paths = sorted(
        all_dirty_paths & selected_paths if selected_paths else all_dirty_paths
    )
    removed_paths = sorted(
        all_removed_paths & selected_paths if selected_paths else all_removed_paths
    )
    candidate_records = {
        path: record
        for path, record in cached.items()
        if path not in set(dirty_paths) | set(removed_paths)
    }
    parse_issues = list(discovery_issues)
    for relative in dirty_paths:
        record, issue = parse_entity_record(project_root, project_root / relative)
        if issue is not None:
            parse_issues.append(issue)
            continue
        assert record is not None
        candidate_records[relative] = record
    registry = finalize_entity_registry(
        project_root,
        list(candidate_records.values()),
        parse_issues,
        {issue.path for issue in parse_issues},
    )
    bundle = build_bundle(project_root, registry)
    written = False
    if not bundle["diagnostics"]["issues"] and not no_write:
        require_runtime()
        stage_root = stage_incremental_bundle(project_root, bundle)
        try:
            connection = connect_database(stage_root / WIKI_DATABASE_PATH)
            try:
                connection.execute("BEGIN IMMEDIATE")
                for relative in removed_paths:
                    delete_page_by_path(connection, relative)
                graph_edges = bundle["graph"]["edges"]
                records_by_path = {
                    record["path"]: record for record in registry["entities"]
                }
                for relative in dirty_paths:
                    delete_page_by_path(connection, relative)
                    record = records_by_path[relative]
                    replace_page(
                        connection, record, current_hashes[relative], graph_edges
                    )
                set_metadata(
                    connection,
                    {
                        "schema_version": WIKI_SCHEMA_VERSION,
                        "source_fingerprint": registry["source_fingerprint"],
                        "views_hash": views_hash(project_root),
                    },
                )
                connection.commit()
            except BaseException:
                connection.rollback()
                raise
            finally:
                connection.close()
        except BaseException:
            discard_generated_bundle(stage_root)
            raise
        promote_generated_bundle(project_root, stage_root, bundle)
        written = True
    return public_bundle_payload(bundle, "sync", dirty_paths, removed_paths, written)


def cache_is_stale(project_root: Path, connection: sqlite3.Connection) -> bool:
    _cached, cached_hashes = load_cached_pages(connection)
    current_hashes, issues = discover_hashes(project_root)
    meta = metadata(connection)
    return bool(
        issues
        or cached_hashes != current_hashes
        or meta.get("views_hash") != views_hash(project_root)
    )


def doctor(project_root: Path) -> dict[str, Any]:
    status = runtime_status()
    database_path = project_root / WIKI_DATABASE_PATH
    status.update(
        {
            "database_path": WIKI_DATABASE_PATH.as_posix(),
            "database_exists": database_path.exists(),
            "schema_version": None,
            "stale": None,
        }
    )
    if database_path.exists():
        try:
            connection = connect_database(database_path)
            try:
                meta = metadata(connection)
                status["schema_version"] = meta.get("schema_version")
                status["stale"] = cache_is_stale(project_root, connection)
            finally:
                connection.close()
        except (OSError, WikiError, WikiStoreError, sqlite3.Error) as exc:
            status["database_error"] = str(exc)
            status["ready"] = False
    return status


def fts_query(value: str) -> str:
    tokens = WORD_PATTERN.findall(value.casefold())
    return " AND ".join(f'"{token.replace(chr(34), chr(34) * 2)}"*' for token in tokens)


def trigram_query(value: str) -> str:
    normalized = normalize_identity(value)
    trigrams = sorted({normalized[index : index + 3] for index in range(len(normalized) - 2)})
    return " OR ".join(f'"{trigram}"' for trigram in trigrams[:64])


def search(
    project_root: Path,
    query: str,
    kind: str | None = None,
    limit: int = 10,
) -> dict[str, Any]:
    if limit <= 0:
        raise WikiError("wiki_search_invalid_limit")
    require_runtime()
    database_path = project_root / WIKI_DATABASE_PATH
    if not database_path.exists():
        raise WikiError("wiki_database_missing:run farplane wiki rebuild")
    connection = connect_database(database_path)
    try:
        meta = metadata(connection)
        if meta.get("schema_version") != str(WIKI_SCHEMA_VERSION):
            raise WikiError("wiki_database_schema_mismatch:run farplane wiki rebuild")
        if cache_is_stale(project_root, connection):
            raise WikiError("wiki_database_stale:run farplane wiki sync")
        normalized = normalize_identity(query)
        rows = connection.execute(
            "SELECT entity_id, path, kind, name, location, normalized_id, normalized_name "
            "FROM pages" + (" WHERE kind = ?" if kind else ""),
            ((kind,) if kind else ()),
        ).fetchall()
        pages = {str(row["entity_id"]): dict(row) for row in rows}
        aliases: dict[str, list[str]] = {entity_id: [] for entity_id in pages}
        for row in connection.execute(
            "SELECT entity_id, alias, normalized_alias FROM aliases ORDER BY alias"
        ):
            entity_id = str(row["entity_id"])
            if entity_id in aliases:
                aliases[entity_id].append(str(row["alias"]))
        match_types: dict[str, set[str]] = {entity_id: set() for entity_id in pages}
        for entity_id, page in pages.items():
            if page["normalized_id"] == normalized:
                match_types[entity_id].add("exact_id")
            if page["normalized_name"] == normalized:
                match_types[entity_id].add("exact_name")
            if any(normalize_identity(alias) == normalized for alias in aliases[entity_id]):
                match_types[entity_id].add("exact_alias")

        lexical = fts_query(query)
        if lexical:
            for row in connection.execute(
                "SELECT entity_id FROM entity_fts WHERE entity_fts MATCH ? LIMIT ?",
                (lexical, max(limit * 4, 20)),
            ):
                entity_id = str(row["entity_id"])
                if entity_id in match_types:
                    match_types[entity_id].add("lexical")
        trigrams = trigram_query(query)
        if trigrams:
            for row in connection.execute(
                "SELECT entity_id FROM entity_trigram WHERE entity_trigram MATCH ? LIMIT ?",
                (trigrams, max(limit * 6, 30)),
            ):
                entity_id = str(row["entity_id"])
                if entity_id in match_types:
                    match_types[entity_id].add("trigram")

        candidates: list[dict[str, Any]] = []
        for entity_id, types in match_types.items():
            if not types:
                continue
            page = pages[entity_id]
            labels = [entity_id, str(page["name"]), *aliases[entity_id]]
            matched_label = max(
                labels,
                key=lambda label: difflib.SequenceMatcher(
                    None, normalized, normalize_identity(label)
                ).ratio(),
            )
            similarity = difflib.SequenceMatcher(
                None, normalized, normalize_identity(matched_label)
            ).ratio()
            candidate: dict[str, Any] = {
                "id": entity_id,
                "name": page["name"],
                "kind": page["kind"],
                "path": page["path"],
                "matched_label": matched_label,
                "match_types": sorted(types),
                "similarity": round(similarity, 6),
            }
            if page["location"]:
                candidate["location"] = page["location"]
            candidates.append(candidate)
        candidates.sort(
            key=lambda candidate: (
                not any(kind.startswith("exact_") for kind in candidate["match_types"]),
                -candidate["similarity"],
                str(candidate["name"]).casefold(),
                candidate["id"],
            )
        )
        return {
            "query": query,
            "normalized_query": normalized,
            "kind": kind,
            "candidates": candidates[:limit],
        }
    except sqlite3.Error as exc:
        raise WikiError(f"wiki_search_error:{exc}") from exc
    finally:
        connection.close()


def print_operation(payload: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return
    if "candidates" in payload:
        print(f"farplane wiki search: {len(payload['candidates'])} candidate(s)")
        for candidate in payload["candidates"]:
            print(
                f"- {candidate['id']}: {candidate['name']} "
                f"({','.join(candidate['match_types'])}; {candidate['similarity']:.3f})"
            )
        return
    print(
        f"farplane wiki {payload['action']}: "
        f"{'wrote' if payload['written'] else 'checked'} "
        f"{payload['counts']['included']} pages, {payload['counts']['edges']} edges; "
        f"{len(payload['diagnostics']['issues'])} issue(s)"
    )
    for issue in payload["diagnostics"]["issues"]:
        print(f"wiki issue: {issue['path']}: {issue['reason']}", file=sys.stderr)


def run_doctor(args: argparse.Namespace) -> int:
    payload = doctor(Path(args.project_root).expanduser().resolve())
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(
            "farplane wiki doctor: "
            f"{'ready' if payload['ready'] else 'blocked'} "
            f"(sqlite={payload['sqlite_version']}, fts5={payload['fts5']}, "
            f"trigram={payload['trigram']}, database={payload['database_exists']})"
        )
    return 0 if payload["ready"] else 1


def run_rebuild(args: argparse.Namespace) -> int:
    payload = rebuild(Path(args.project_root).expanduser().resolve(), args.no_write)
    print_operation(payload, args.json)
    return 0 if payload["ok"] else 1


def run_sync(args: argparse.Namespace) -> int:
    payload = sync(
        Path(args.project_root).expanduser().resolve(),
        requested_paths=args.path,
        no_write=args.no_write,
    )
    print_operation(payload, args.json)
    return 0 if payload["ok"] else 1


def run_search(args: argparse.Namespace) -> int:
    payload = search(
        Path(args.project_root).expanduser().resolve(),
        args.query,
        kind=args.kind,
        limit=args.limit,
    )
    print_operation(payload, args.json)
    return 0
