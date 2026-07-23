#!/usr/bin/env python3
"""Canonical ticket terminal transition and completion-event producer."""

from __future__ import annotations

import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from farplane_event_store import atomic_write_json, pending_events
from farplane_mining import CodexRunner, MiningError, mine_ticket


TICKET_ID_RE = re.compile(r"^TASK-\d{4}$")
SUCCESS_STATUSES = {"done", "complete", "completed", "closed"}


class TicketCloseError(RuntimeError):
    """Raised when a ticket cannot be closed safely."""


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _frontmatter(text: str) -> tuple[dict[str, Any], list[str], str]:
    match = re.match(r"^---\s*\n(.*?)\n---(?:\s*\n|$)", text, flags=re.S)
    if not match:
        raise TicketCloseError("ticket_frontmatter_missing")
    try:
        payload = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        raise TicketCloseError(f"ticket_frontmatter_invalid:{exc}") from exc
    if not isinstance(payload, dict):
        raise TicketCloseError("ticket_frontmatter_invalid_shape")
    return payload, match.group(1).splitlines(), text[match.end() :]


def _closed_text(text: str, *, updated_at: str) -> tuple[str, dict[str, Any]]:
    before, lines, body = _frontmatter(text)
    status = str(before.get("status") or "").strip().lower()
    if status in {"failed", "rejected"}:
        raise TicketCloseError(f"ticket_has_non_success_terminal_status:{status}")

    output: list[str] = []
    saw_status = False
    saw_updated = False
    for line in lines:
        key = line.split(":", 1)[0].strip() if ":" in line else ""
        if key == "claimed_by":
            continue
        if key == "status":
            output.append("status: done")
            saw_status = True
            continue
        if key == "updated_at":
            output.append(f"updated_at: {updated_at}")
            saw_updated = True
            continue
        output.append(line)
    if not saw_status:
        output.append("status: done")
    if not saw_updated:
        output.append(f"updated_at: {updated_at}")
    frontmatter_text = "\n".join(output)
    return f"---\n{frontmatter_text}\n---\n{body}", before


def _atomic_write_text(path: Path, text: str) -> None:
    descriptor, raw_tmp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    tmp = Path(raw_tmp)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def close_ticket(
    project_root: Path,
    ticket_id: str,
    *,
    codex_runner: CodexRunner | None = None,
) -> dict[str, Any]:
    """Close, archive, and mine one ticket; repeated calls reuse the same event/run."""

    root = project_root.resolve()
    normalized = ticket_id.strip().upper()
    if not TICKET_ID_RE.fullmatch(normalized):
        raise TicketCloseError(f"invalid_ticket_id:{ticket_id}")

    active_dir = root / "tickets" / normalized
    archive_dir = root / "tickets" / "archive" / normalized
    active_ticket = active_dir / "ticket.md"
    archived_ticket = archive_dir / "ticket.md"
    already_closed = archived_ticket.is_file() and not active_ticket.exists()

    if active_ticket.is_file() and archived_ticket.exists():
        raise TicketCloseError(f"ticket_exists_active_and_archived:{normalized}")
    if not active_ticket.is_file() and not archived_ticket.is_file():
        raise TicketCloseError(f"ticket_not_found:{normalized}")

    before: dict[str, Any] = {}
    if not already_closed:
        closed_at = now_iso()
        closed_text, before = _closed_text(active_ticket.read_text(encoding="utf-8"), updated_at=closed_at)
        _atomic_write_text(active_ticket, closed_text)
        archive_dir.parent.mkdir(parents=True, exist_ok=True)
        os.replace(active_dir, archive_dir)
    else:
        current, _, _ = _frontmatter(archived_ticket.read_text(encoding="utf-8"))
        if str(current.get("status") or "").strip().lower() not in SUCCESS_STATUSES:
            raise TicketCloseError(f"archived_ticket_not_successful:{normalized}")

    try:
        mining = mine_ticket(root, normalized, codex_runner=codex_runner)
        mining_status = "complete"
        mining_error = None
    except MiningError as exc:
        mining = None
        mining_status = "pending"
        mining_error = str(exc)

    pending_event_id = next(
        (
            str(event.get("event_id"))
            for event in pending_events(root)
            if (event.get("entity_ref") or {}).get("id") == normalized
        ),
        None,
    )

    receipt = {
        "schema_version": 1,
        "ok": mining_status == "complete",
        "ticket_id": normalized,
        "ticket_path": archived_ticket.relative_to(root).as_posix(),
        "status": "already_closed" if already_closed else "closed",
        "metadata_delta": {
            "status": {"before": before.get("status"), "after": "done"} if before else {},
            "claimed_by_cleared": bool(before.get("claimed_by")) if before else False,
        },
        "mining_status": mining_status,
        "mining_error": mining_error,
        "event_id": mining.get("event_id") if isinstance(mining, dict) else pending_event_id,
        "runs": mining.get("runs", []) if isinstance(mining, dict) else [],
        "closed_at": now_iso(),
    }
    receipt_path = root / ".farplane" / "tickets" / "closures" / f"{normalized}.json"
    atomic_write_json(receipt_path, receipt)
    return {**receipt, "receipt_path": str(receipt_path)}
