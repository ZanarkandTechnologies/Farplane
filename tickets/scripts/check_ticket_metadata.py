#!/usr/bin/env python3
"""
Validate the Codexter ticket metadata contract.

This validator is intentionally small. It exists to catch trust-breaking drift
in ticket metadata, not to become a second orchestration system.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TICKETS_DIR = ROOT / "tickets"
ALLOWED_PHASES = {"planning", "building", "documenting", "complete", "failed"}
ALLOWED_STATUSES = {"todo", "review", "building", "blocked", "done", "failed"}
REQUIRED_FIELDS = {
    "ticket_id",
    "title",
    "phase",
    "status",
    "owner",
    "priority",
    "depends_on",
    "blocked_by",
    "ready",
    "approval_required",
    "created_at",
    "updated_at",
    "next_action",
    "last_verification",
    "linked_docs",
}
TICKET_ID_RE = re.compile(r"^TASK-\d{4}$")
TICKET_ID_IN_FILENAME_RE = re.compile(r"^(TASK-\d{4})(?:-|$)")
CANONICAL_TICKET_FILENAME = "ticket.md"


def load_ticket(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter start")

    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        raise ValueError("missing frontmatter end")

    raw_frontmatter = parts[0][4:]
    body = parts[1]
    data: dict[str, object] = {}
    lines = raw_frontmatter.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line!r}")
        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        if value == "":
            items: list[str] = []
            i += 1
            while i < len(lines) and lines[i].startswith("  - "):
                items.append(lines[i][4:].strip())
                i += 1
            data[key] = items
            continue
        if value == "[]":
            data[key] = []
            i += 1
            continue
        if value in {"true", "false"}:
            data[key] = value == "true"
        else:
            data[key] = value
        i += 1
    return data, body


def validate_ticket(path: Path) -> list[str]:
    errors: list[str] = []
    rel = path.relative_to(ROOT)
    try:
        frontmatter, body = load_ticket(path)
    except Exception as exc:
        return [f"{rel}: {exc}"]

    missing = sorted(REQUIRED_FIELDS - set(frontmatter))
    if missing:
        errors.append(f"{rel}: missing required fields: {', '.join(missing)}")

    if "lane" in frontmatter:
        errors.append(f"{rel}: lane must not appear in frontmatter")

    if "session_id" in frontmatter:
        errors.append(
            f"{rel}: session_id must not appear in frontmatter; use claimed_by for the human-facing alias only"
        )

    ticket_id = str(frontmatter.get("ticket_id", "")).strip()
    if not TICKET_ID_RE.match(ticket_id):
        errors.append(f"{rel}: invalid ticket_id {ticket_id!r}")
    else:
        if path.name == CANONICAL_TICKET_FILENAME:
            if path.parent.name != ticket_id:
                errors.append(f"{rel}: parent directory does not match ticket_id {ticket_id}")
        else:
            match = TICKET_ID_IN_FILENAME_RE.match(path.stem)
            if not match or match.group(1) != ticket_id:
                errors.append(f"{rel}: filename does not match ticket_id {ticket_id}")

    phase = str(frontmatter.get("phase", "")).strip()
    if phase and phase not in ALLOWED_PHASES:
        errors.append(f"{rel}: invalid phase {phase!r}")

    status = str(frontmatter.get("status", "")).strip()
    if status and status not in ALLOWED_STATUSES:
        errors.append(f"{rel}: invalid status {status!r}")

    blocked_by = frontmatter.get("blocked_by", [])
    if not isinstance(blocked_by, list):
        errors.append(f"{rel}: blocked_by must be a list")
        blocked_by = []
    else:
        for item in blocked_by:
            if not TICKET_ID_RE.match(str(item).strip()):
                errors.append(f"{rel}: blocked_by entries must be ticket IDs only: {item!r}")

    approval_required = bool(frontmatter.get("approval_required", False))
    requires_qa = frontmatter.get("requires_qa", None)
    requires_demo = frontmatter.get("requires_demo", None)
    if requires_qa is not None and not isinstance(requires_qa, bool):
        errors.append(f"{rel}: requires_qa must be true|false when present")
    if requires_demo is not None and not isinstance(requires_demo, bool):
        errors.append(f"{rel}: requires_demo must be true|false when present")
    if requires_demo is True and requires_qa is False:
        errors.append(f"{rel}: requires_demo=true requires requires_qa=true")
    ready = bool(frontmatter.get("ready", False))
    if approval_required and ready:
        errors.append(f"{rel}: approval_required=true requires ready=false")

    if status == "blocked" and ready:
        errors.append(f"{rel}: status=blocked requires ready=false")

    if status == "building" and approval_required:
        errors.append(f"{rel}: status=building cannot contain approval-gated work")

    if "## Status" in body:
        errors.append(f"{rel}: legacy '## Status' block is not allowed")

    if phase == "documenting" and status not in {"building", "review"}:
        errors.append(f"{rel}: documenting tickets should stay in an active execution/planning state until writeback finishes")

    return errors


def main() -> int:
    ticket_files = sorted(
        [
            *(p for p in TICKETS_DIR.glob("TASK-*/ticket.md") if p.is_file()),
            *(p for p in TICKETS_DIR.glob("TASK-*.md") if p.is_file()),
        ]
    )
    errors: list[str] = []
    for path in ticket_files:
        errors.extend(validate_ticket(path))
    if errors:
        for err in errors:
            print(err)
        return 1
    print(f"ticket metadata OK ({len(ticket_files)} ticket files checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
