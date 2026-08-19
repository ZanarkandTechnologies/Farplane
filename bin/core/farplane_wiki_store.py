#!/usr/bin/env python3
"""SQLite storage and grouped projection promotion for Farplane Wiki."""

from __future__ import annotations

import json
import os
import shutil
import sqlite3
import tempfile
import unicodedata
from pathlib import Path
from typing import Any

from farplane_entities import (
    CRM_VIEW_PATH,
    ENTITY_INDEX_PATH,
    ENTITY_ROOT,
    GRAPH_VIEW_PATH,
    VIEW_CONFIG_PATH,
    VIEW_PROJECTION_ROOT,
    field_text,
    write_entity_projections,
)


WIKI_ROOT = Path(".farplane/wiki")
WIKI_DATABASE_PATH = WIKI_ROOT / "wiki.sqlite"
WIKI_SCHEMA_VERSION = 1
RETIRED_PROJECTION_PATHS = (ENTITY_ROOT / "world.json",)


class WikiStoreError(RuntimeError):
    """Actionable generated-store failure."""


def normalize_identity(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value).casefold()
    return "".join(character for character in decomposed if character.isalnum())


def source_hash(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def views_hash(project_root: Path) -> str:
    path = project_root / VIEW_CONFIG_PATH
    return source_hash(path) if path.exists() else "absent"


def runtime_status() -> dict[str, Any]:
    connection = sqlite3.connect(":memory:")
    fts5 = False
    trigram = False
    try:
        connection.execute("CREATE VIRTUAL TABLE fts_probe USING fts5(value)")
        fts5 = True
        connection.execute(
            "CREATE VIRTUAL TABLE trigram_probe USING fts5(value, tokenize='trigram')"
        )
        trigram = True
    except sqlite3.Error:
        pass
    finally:
        connection.close()
    return {
        "sqlite_version": sqlite3.sqlite_version,
        "fts5": fts5,
        "trigram": trigram,
        "ready": fts5 and trigram,
    }


def require_runtime() -> dict[str, Any]:
    status = runtime_status()
    if not status["ready"]:
        raise WikiStoreError(
            "wiki_runtime_unavailable:Python sqlite3 requires FTS5 and trigram support"
        )
    return status


def connect_database(path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
        CREATE TABLE pages (
          entity_id TEXT PRIMARY KEY,
          path TEXT NOT NULL UNIQUE,
          kind TEXT NOT NULL,
          name TEXT NOT NULL,
          normalized_id TEXT NOT NULL,
          normalized_name TEXT NOT NULL,
          location TEXT,
          source_hash TEXT NOT NULL,
          record_json TEXT NOT NULL
        );
        CREATE INDEX pages_normalized_name_idx ON pages(normalized_name);
        CREATE INDEX pages_kind_idx ON pages(kind);
        CREATE TABLE aliases (
          entity_id TEXT NOT NULL REFERENCES pages(entity_id) ON DELETE CASCADE,
          alias TEXT NOT NULL,
          normalized_alias TEXT NOT NULL,
          PRIMARY KEY(entity_id, normalized_alias)
        );
        CREATE INDEX aliases_normalized_idx ON aliases(normalized_alias);
        CREATE TABLE edge_claims (
          edge_key TEXT PRIMARY KEY,
          origin_page_id TEXT NOT NULL REFERENCES pages(entity_id) ON DELETE CASCADE,
          target_entity_id TEXT NOT NULL,
          payload_json TEXT NOT NULL
        );
        CREATE INDEX edge_claims_origin_idx ON edge_claims(origin_page_id);
        """
    )
    connection.execute(
        "CREATE VIRTUAL TABLE entity_fts USING fts5("
        "entity_id UNINDEXED, name, aliases, body, "
        "tokenize='unicode61 remove_diacritics 2', prefix='2 3')"
    )
    connection.execute(
        "CREATE VIRTUAL TABLE entity_trigram USING fts5("
        "entity_id UNINDEXED, identity_text, tokenize='trigram')"
    )


def metadata(connection: sqlite3.Connection) -> dict[str, str]:
    try:
        return {
            str(row["key"]): str(row["value"])
            for row in connection.execute("SELECT key, value FROM meta")
        }
    except sqlite3.Error as exc:
        raise WikiStoreError(f"wiki_database_invalid:{exc}") from exc


def set_metadata(connection: sqlite3.Connection, values: dict[str, Any]) -> None:
    connection.executemany(
        "INSERT OR REPLACE INTO meta(key, value) VALUES (?, ?)",
        [(key, str(value)) for key, value in values.items()],
    )


def aliases_for(record: dict[str, Any]) -> list[str]:
    raw = record["frontmatter"].get("aliases")
    if not isinstance(raw, list):
        return []
    by_normalized: dict[str, str] = {}
    for alias in sorted({str(value).strip() for value in raw if str(value).strip()}):
        normalized = normalize_identity(alias)
        if normalized:
            by_normalized.setdefault(normalized, alias)
    return list(by_normalized.values())


def replace_page(
    connection: sqlite3.Connection,
    record: dict[str, Any],
    digest: str,
    graph_edges: list[dict[str, Any]],
) -> None:
    entity_id = str(record["id"])
    aliases = aliases_for(record)
    connection.execute("DELETE FROM entity_fts WHERE entity_id = ?", (entity_id,))
    connection.execute("DELETE FROM entity_trigram WHERE entity_id = ?", (entity_id,))
    connection.execute("DELETE FROM aliases WHERE entity_id = ?", (entity_id,))
    connection.execute("DELETE FROM edge_claims WHERE origin_page_id = ?", (entity_id,))
    connection.execute(
        """
        INSERT INTO pages(
          entity_id, path, kind, name, normalized_id, normalized_name,
          location, source_hash, record_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(entity_id) DO UPDATE SET
          path=excluded.path, kind=excluded.kind, name=excluded.name,
          normalized_id=excluded.normalized_id,
          normalized_name=excluded.normalized_name,
          location=excluded.location, source_hash=excluded.source_hash,
          record_json=excluded.record_json
        """,
        (
            entity_id,
            record["path"],
            record["kind"],
            record["name"],
            normalize_identity(entity_id),
            normalize_identity(str(record["name"])),
            field_text(record["frontmatter"], "location") or None,
            digest,
            json.dumps(record, sort_keys=True, separators=(",", ":")),
        ),
    )
    connection.executemany(
        "INSERT INTO aliases(entity_id, alias, normalized_alias) VALUES (?, ?, ?)",
        [(entity_id, alias, normalize_identity(alias)) for alias in aliases],
    )
    connection.execute(
        "INSERT INTO entity_fts(entity_id, name, aliases, body) VALUES (?, ?, ?, ?)",
        (entity_id, record["name"], " ".join(aliases), record["body"]),
    )
    identity_text = " ".join(
        normalize_identity(label) for label in [entity_id, record["name"], *aliases]
    )
    connection.execute(
        "INSERT INTO entity_trigram(entity_id, identity_text) VALUES (?, ?)",
        (entity_id, identity_text),
    )
    connection.executemany(
        "INSERT INTO edge_claims(edge_key, origin_page_id, target_entity_id, payload_json) "
        "VALUES (?, ?, ?, ?)",
        [
            (
                edge["key"],
                entity_id,
                edge["target_entity_id"],
                json.dumps(edge, sort_keys=True, separators=(",", ":")),
            )
            for edge in graph_edges
            if edge["source_entity_id"] == entity_id
        ],
    )


def delete_page_by_path(connection: sqlite3.Connection, path: str) -> None:
    row = connection.execute(
        "SELECT entity_id FROM pages WHERE path = ?", (path,)
    ).fetchone()
    if row is None:
        return
    entity_id = str(row["entity_id"])
    connection.execute("DELETE FROM entity_fts WHERE entity_id = ?", (entity_id,))
    connection.execute("DELETE FROM entity_trigram WHERE entity_id = ?", (entity_id,))
    connection.execute("DELETE FROM pages WHERE entity_id = ?", (entity_id,))


def create_database(
    path: Path,
    bundle: dict[str, Any],
    hashes: dict[str, str],
    current_views_hash: str,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = connect_database(path)
    try:
        create_schema(connection)
        graph_edges = bundle["graph"]["edges"]
        for record in bundle["registry"]["entities"]:
            replace_page(connection, record, hashes[record["path"]], graph_edges)
        set_metadata(
            connection,
            {
                "schema_version": WIKI_SCHEMA_VERSION,
                "source_fingerprint": bundle["registry"]["source_fingerprint"],
                "views_hash": current_views_hash,
            },
        )
        connection.commit()
    finally:
        connection.close()


def stage_generated_bundle(project_root: Path, bundle: dict[str, Any]) -> Path:
    stage_parent = project_root / ".farplane"
    stage_parent.mkdir(parents=True, exist_ok=True)
    stage_root = Path(tempfile.mkdtemp(prefix=".wiki-stage-", dir=stage_parent))
    try:
        write_entity_projections(
            stage_root,
            bundle["index"],
            bundle["graph"],
            bundle["crm"],
            bundle["views"],
        )
    except BaseException:
        shutil.rmtree(stage_root, ignore_errors=True)
        raise
    return stage_root


def stage_rebuild_bundle(
    project_root: Path,
    bundle: dict[str, Any],
    hashes: dict[str, str],
) -> Path:
    stage_root = stage_generated_bundle(project_root, bundle)
    try:
        create_database(
            stage_root / WIKI_DATABASE_PATH,
            bundle,
            hashes,
            views_hash(project_root),
        )
    except BaseException:
        shutil.rmtree(stage_root, ignore_errors=True)
        raise
    return stage_root


def stage_incremental_bundle(project_root: Path, bundle: dict[str, Any]) -> Path:
    stage_root = stage_generated_bundle(project_root, bundle)
    try:
        staged_database = stage_root / WIKI_DATABASE_PATH
        staged_database.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(project_root / WIKI_DATABASE_PATH, staged_database)
    except BaseException:
        shutil.rmtree(stage_root, ignore_errors=True)
        raise
    return stage_root


def discard_generated_bundle(stage_root: Path) -> None:
    shutil.rmtree(stage_root, ignore_errors=True)


def projection_paths(bundle: dict[str, Any]) -> list[Path]:
    paths = [ENTITY_INDEX_PATH, GRAPH_VIEW_PATH, CRM_VIEW_PATH]
    paths.extend(
        VIEW_PROJECTION_ROOT / f"{view_id}.json" for view_id in sorted(bundle["views"])
    )
    return paths


def promote_generated_bundle(
    project_root: Path,
    stage_root: Path,
    bundle: dict[str, Any],
) -> None:
    desired = [WIKI_DATABASE_PATH, *projection_paths(bundle)]
    view_root = project_root / VIEW_PROJECTION_ROOT
    stale = [
        path
        for path in RETIRED_PROJECTION_PATHS
        if (project_root / path).exists() and path not in desired
    ]
    if view_root.exists():
        stale.extend(
            path.relative_to(project_root)
            for path in view_root.glob("*.json")
            if path.relative_to(project_root) not in desired
        )
    backup_root = stage_root / ".backup"
    moved_existing: list[Path] = []
    promoted: list[Path] = []
    try:
        for relative in [*desired, *stale]:
            target = project_root / relative
            if not target.exists():
                continue
            backup = backup_root / relative
            backup.parent.mkdir(parents=True, exist_ok=True)
            os.replace(target, backup)
            moved_existing.append(relative)
        for relative in desired:
            staged = stage_root / relative
            target = project_root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            os.replace(staged, target)
            promoted.append(relative)
    except BaseException:
        for relative in reversed(promoted):
            (project_root / relative).unlink(missing_ok=True)
        for relative in reversed(moved_existing):
            backup = backup_root / relative
            target = project_root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            if backup.exists():
                os.replace(backup, target)
        raise
    finally:
        shutil.rmtree(stage_root, ignore_errors=True)
