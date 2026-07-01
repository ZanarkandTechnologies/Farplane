#!/usr/bin/env python3
"""Local Farplane content ledger helpers."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date as date_type
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CONTENT_LEDGER_PATH = Path(".farplane/content/ledger.jsonl")
VALID_STATUSES = {"idea", "draft", "approved", "posted", "measured", "archived"}
VALID_APPROVALS = {"not_required", "requested", "approved", "rejected"}


@dataclass(frozen=True)
class ContentLedgerResult:
    ledger_path: Path
    rows: list[dict[str, Any]]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            raw = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(raw, dict):
            rows.append(raw)
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def parse_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def parse_iso_datetime(value: Any) -> datetime | None:
    if not value:
        return None
    raw = str(value).strip()
    if not raw:
        return None
    try:
        if raw.endswith("Z"):
            raw = raw[:-1] + "+00:00"
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        try:
            parsed_date = date_type.fromisoformat(raw[:10])
        except ValueError:
            return None
        return datetime.combine(parsed_date, datetime.min.time(), tzinfo=timezone.utc)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def row_date(row: dict[str, Any]) -> str | None:
    parsed = parse_iso_datetime(row.get("published_at"))
    return parsed.date().isoformat() if parsed else None


def content_id(platform: str, external_id: str | None, url: str | None, published_at: str | None) -> str:
    if external_id:
        return f"{platform}:{external_id}"
    if url:
        return f"{platform}:url:{url}"
    stamp = (published_at or now_iso()).replace(":", "").replace("-", "")
    return f"{platform}:{stamp}"


def validate_row(row: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if not row.get("content_id"):
        issues.append("missing:content_id")
    if not row.get("platform"):
        issues.append("missing:platform")
    if row.get("status") not in VALID_STATUSES:
        issues.append(f"invalid_status:{row.get('status')}")
    if row.get("approval") not in VALID_APPROVALS:
        issues.append(f"invalid_approval:{row.get('approval')}")
    kpis = row.get("kpis")
    if not isinstance(kpis, list) or not all(isinstance(item, str) and item for item in kpis):
        issues.append("invalid:kpis")
    return issues


def ledger_path(project_root: Path) -> Path:
    return project_root.resolve() / CONTENT_LEDGER_PATH


def add_content_row(project_root: Path, row: dict[str, Any]) -> ContentLedgerResult:
    path = ledger_path(project_root)
    rows = read_jsonl(path)
    row = {
        key: value
        for key, value in row.items()
        if value is not None and value != "" and value != []
    }
    row.setdefault("created_at", now_iso())
    row["updated_at"] = now_iso()
    issues = validate_row(row)
    if issues:
        raise ValueError(",".join(issues))
    content_key = str(row["content_id"])
    replaced = False
    next_rows: list[dict[str, Any]] = []
    for existing in rows:
        if existing.get("content_id") != content_key:
            next_rows.append(existing)
            continue
        merged = {**existing, **row, "created_at": existing.get("created_at") or row.get("created_at")}
        next_rows.append(merged)
        replaced = True
    if not replaced:
        next_rows.append(row)
    write_jsonl(path, next_rows)
    return ContentLedgerResult(path, next_rows)


def filter_rows(
    rows: list[dict[str, Any]],
    platform: str | None = None,
    status: str | None = None,
    kpi: str | None = None,
    since_date: str | None = None,
    until_date: str | None = None,
) -> list[dict[str, Any]]:
    filtered: list[dict[str, Any]] = []
    for row in rows:
        if platform and row.get("platform") != platform:
            continue
        if status and row.get("status") != status:
            continue
        if kpi and kpi not in (row.get("kpis") if isinstance(row.get("kpis"), list) else []):
            continue
        published_date = row_date(row)
        if since_date and (published_date is None or published_date < since_date):
            continue
        if until_date and (published_date is None or published_date >= until_date):
            continue
        filtered.append(row)
    return filtered


def external_ids(rows: list[dict[str, Any]]) -> list[str]:
    ids: list[str] = []
    for row in rows:
        external_id = row.get("external_id")
        if isinstance(external_id, str) and external_id and external_id not in ids:
            ids.append(external_id)
    return ids


def run_content_add(args: argparse.Namespace) -> int:
    row = {
        "content_id": args.content_id or content_id(args.platform, args.external_id, args.url, args.published_at),
        "platform": args.platform,
        "external_id": args.external_id,
        "url": args.url,
        "status": args.status,
        "approval": args.approval,
        "published_at": args.published_at,
        "campaign": args.campaign,
        "kpis": parse_csv(args.kpis),
        "title": args.title,
        "source_ref": args.source_ref,
        "approval_ref": args.approval_ref,
        "notes": args.notes,
    }
    try:
        result = add_content_row(Path(args.project_root), row)
    except ValueError as exc:
        print(json.dumps({"ok": False, "issues": str(exc).split(",")}, indent=2, sort_keys=True))
        return 1
    payload = {
        "ok": True,
        "ledger": str(result.ledger_path),
        "content_id": row["content_id"],
        "row_count": len(result.rows),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def run_content_list(args: argparse.Namespace) -> int:
    path = ledger_path(Path(args.project_root))
    rows = filter_rows(read_jsonl(path), args.platform, args.status, args.kpi, args.since_date, args.until_date)
    payload = {
        "ok": True,
        "ledger": str(path),
        "row_count": len(rows),
        "external_ids": external_ids(rows),
        "rows": rows,
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0
