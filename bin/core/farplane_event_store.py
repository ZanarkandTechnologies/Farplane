#!/usr/bin/env python3
"""Small durable event store for explicit Farplane lifecycle events."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from datetime import date, datetime
from pathlib import Path
from typing import Any


def canonical_json(value: Any) -> str:
    def encode_scalar(item: Any) -> str:
        if isinstance(item, (datetime, date)):
            return item.isoformat()
        raise TypeError(f"Object of type {item.__class__.__name__} is not JSON serializable")

    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=encode_scalar)


def sha256_value(value: Any) -> str:
    text = value if isinstance(value, str) else canonical_json(value)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_json(path: Path, fallback: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return fallback


def atomic_write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, raw_tmp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    tmp = Path(raw_tmp)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        tmp.unlink(missing_ok=True)


def create_json_exclusive(path: Path, payload: Any) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, raw_tmp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    tmp = Path(raw_tmp)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(tmp, path)
        except FileExistsError:
            return False
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
        return True
    finally:
        tmp.unlink(missing_ok=True)


def event_record_path(project_root: Path, event_id: str) -> Path:
    return project_root / ".farplane" / "events" / "records" / f"{event_id}.json"


def outbox_path(project_root: Path, event_id: str) -> Path:
    return project_root / ".farplane" / "events" / "outbox" / f"{event_id}.json"


def enqueue_event(project_root: Path, event: dict[str, Any]) -> dict[str, Any]:
    event_id = str(event.get("event_id") or "")
    if not event_id:
        raise ValueError("event_id is required")
    record = event_record_path(project_root, event_id)
    outbox = outbox_path(project_root, event_id)
    created = create_json_exclusive(record, event)
    durable_event = event if created else read_json(record, None)
    if not isinstance(durable_event, dict) or durable_event.get("event_id") != event_id:
        raise ValueError(f"event_record_invalid:{event_id}")
    create_json_exclusive(outbox, durable_event)
    return {"event_record": str(record), "outbox_row": str(outbox), "event": durable_event}


def pending_events(project_root: Path) -> list[dict[str, Any]]:
    root = project_root / ".farplane" / "events" / "outbox"
    if not root.exists():
        return []
    rows = []
    for path in sorted(root.glob("*.json")):
        payload = read_json(path, None)
        if isinstance(payload, dict) and payload.get("event_id"):
            rows.append(payload)
    return rows


def acknowledge_event(project_root: Path, event_id: str) -> None:
    outbox_path(project_root, event_id).unlink(missing_ok=True)
