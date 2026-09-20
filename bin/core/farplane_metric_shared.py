"""Shared parsing helpers for Farplane metric reducers."""

from __future__ import annotations

import json
from datetime import date as date_type
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

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


def row_date(row: dict[str, Any]) -> str:
    raw = row.get("ts") or row.get("timestamp") or row.get("created_at") or row.get("date") or ""
    parsed = parse_iso_datetime(raw)
    return parsed.date().isoformat() if parsed else str(raw)[:10]


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


def read_jsonl_glob(root: Path, pattern: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(root.glob(pattern)):
        rows.extend(read_jsonl(path))
    return rows


def markdown_heading_section(markdown: str, heading: str) -> str:
    target = f"## {heading}"
    lines = markdown.splitlines()
    start: int | None = None
    for index, line in enumerate(lines):
        if line.strip() == target:
            start = index + 1
            break
    if start is None:
        return ""
    end = len(lines)
    for index in range(start, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return "\n".join(lines[start:end]).strip()


def parse_ticket_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") or "\n---\n" not in text:
        return {}
    raw = text.split("\n---\n", 1)[0][4:]
    try:
        loaded = yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        loaded = {}
        for line in raw.splitlines():
            if ":" not in line or line.startswith(("  ", "- ")):
                continue
            key, value = line.split(":", 1)
            loaded[key.strip()] = value.strip().strip('"')
    if not isinstance(loaded, dict):
        return {}
    return {str(key): "" if value is None else str(value) for key, value in loaded.items()}


def iter_ticket_files(ticket_dir: Path) -> list[Path]:
    roots = [ticket_dir, ticket_dir / "archive"]
    tickets: list[Path] = []
    for root in roots:
        if root.exists():
            tickets.extend(root.glob("TASK-*/ticket.md"))
    return sorted(set(tickets))


def ticket_completion_date(fm: dict[str, str], fallback_date: str) -> str:
    for key in ("completed_at", "closed_at", "updated_at"):
        parsed = parse_iso_datetime(fm.get(key, ""))
        if parsed:
            return parsed.date().isoformat()
    return fallback_date


def ticket_is_complete(fm: dict[str, str]) -> bool:
    status = str(fm.get("status") or "").strip().lower()
    phase = str(fm.get("phase") or "").strip().lower()
    return status == "done" and phase in {"", "complete"}


def ticket_has_completion_proof(markdown: str) -> bool:
    done = markdown_heading_section(markdown, "Done / Proof") or markdown_heading_section(markdown, "Done")
    lowered = done.lower()
    return any(
        token in lowered
        for token in ("passed", "proof", "evidence", "artifact", "artifacts/", "review", "receipt", "verification")
    )


def ticket_has_acceptance_evidence(ticket: Path, markdown: str) -> bool:
    review_root = ticket.parent / "artifacts" / "review"
    for path in sorted(review_root.rglob("*")) if review_root.exists() else []:
        if not path.is_file() or path.suffix.lower() not in {".md", ".json"}:
            continue
        lowered = path.read_text(encoding="utf-8", errors="ignore").lower()
        if ("verdict: pass" in lowered or '"verdict": "pass"' in lowered) and (
            "tas-a" in lowered or '"overall_tas": "tas-a"' in lowered
        ):
            return True
    done = (markdown_heading_section(markdown, "Done / Proof") or "").lower()
    return "tas-a" in done and "verdict" in done and "pass" in done and "pending" not in done

