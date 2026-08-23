#!/usr/bin/env python3
"""
Validate the Farplane ticket metadata contract.

This validator is intentionally small. It exists to catch trust-breaking drift
in ticket metadata, not to become a second orchestration system.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = ROOT / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from farplane_ticket_reward import is_timezone_bearing_iso_datetime
from lint.source import MarkdownFrontmatterError, parse_markdown_frontmatter_document


TICKETS_DIR = ROOT / "tickets"
BINDINGS_PATH = ROOT / "farplane" / "bindings.yaml"
ALLOWED_STATUSES = {
    "todo",
    "active",
    "awaiting_review",
    "waiting_signal",
    "blocked",
    "done",
    "failed",
    "rejected",
}
ALLOWED_PRIORITIES = {"urgent", "high", "medium", "low"}
REQUIRED_FIELDS = {
    "ticket_id",
    "title",
    "status",
    "created_at",
    "updated_at",
}
OPTIONAL_FIELDS = {
    "priority",
    "due_at",
    "claimed_by",
    "thread_id",
    "depends_on",
    "human_gate",
    "compute_target",
    "ui_scope",
    "rejection_reason",
    # Registered template provenance is tolerated on instances but does not
    # participate in board routing and is never required.
    "template_id",
    "template_version",
    "feature_refs",
}
RETIRED_FIELDS = {
    "phase",
    "owner",
    "blocked_by",
    "ready",
    "approval_required",
    "requires_qa",
    "requires_demo",
    "next_action",
    "last_verification",
    "rewards",
    "rewards.kpi",
}
TICKET_ID_RE = re.compile(r"^TASK-\d{4}$")
TICKET_ID_IN_FILENAME_RE = re.compile(r"^(TASK-\d{4})(?:-|$)")
CANONICAL_TICKET_FILENAME = "ticket.md"
ALLOWED_COMPUTE_TARGETS = {
    "local_shared",
    "local_worktree",
    "symphony",
    "codex_cloud",
}
GENERIC_CODEX_CLAIM = "codex"
HUMAN_GATE_NONE = "none"


def normalize_optional_scalar(value: object) -> str:
    if isinstance(value, list):
        return ""
    return str(value or "").strip()


def load_allowed_human_gates() -> set[str]:
    if not BINDINGS_PATH.exists():
        return set()

    gates: set[str] = set()
    lines = BINDINGS_PATH.read_text(encoding="utf-8").splitlines()
    in_human_gates = False
    for line in lines:
        if line.startswith("human_gates:"):
            in_human_gates = True
            continue
        if in_human_gates:
            if line and not line.startswith(" "):
                break
            stripped = line.strip()
            if stripped.startswith("- "):
                gates.add(stripped[2:].strip().strip('"').strip("'"))
    return gates


def parse_human_gate(value: object) -> tuple[str, str] | None:
    if value is None:
        return None
    if isinstance(value, str):
        stripped = value.strip()
        if stripped == HUMAN_GATE_NONE:
            return (HUMAN_GATE_NONE, "")
        if stripped.startswith("[") and stripped.endswith("]"):
            inner = stripped[1:-1].strip()
            if "," not in inner:
                return ("", "")
            tag, reason = inner.split(",", 1)
            return (tag.strip().strip('"').strip("'"), reason.strip().strip('"').strip("'"))
    if isinstance(value, list) and len(value) == 2 and all(isinstance(item, str) for item in value):
        return (value[0].strip(), value[1].strip())
    return ("", "")


def load_ticket(path: Path) -> tuple[dict[str, object], str]:
    try:
        data, _raw, body = parse_markdown_frontmatter_document(
            path.read_text(encoding="utf-8"),
            path,
            required=True,
        )
    except MarkdownFrontmatterError as exc:
        raise ValueError(str(exc)) from exc
    assert data is not None
    return {key: normalize_frontmatter_value(value) for key, value in data.items()}, body


def normalize_frontmatter_value(value: object) -> object:
    """Keep YAML's structural types while comparing temporal values as text."""

    if hasattr(value, "isoformat"):
        return value.isoformat()
    if isinstance(value, list):
        return [normalize_frontmatter_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): normalize_frontmatter_value(item) for key, item in value.items()}
    return value


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

    retired = sorted(RETIRED_FIELDS & set(frontmatter))
    if retired:
        errors.append(
            f"{rel}: retired metadata fields must move to status/body/progress/QA Strategy: {', '.join(retired)}"
        )
    unknown = sorted(set(frontmatter) - REQUIRED_FIELDS - OPTIONAL_FIELDS - RETIRED_FIELDS)
    if unknown:
        errors.append(
            f"{rel}: unsupported metadata fields must move to the ticket body or progress.md: {', '.join(unknown)}"
        )

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

    title = str(frontmatter.get("title", "")).strip()
    expected_h1 = f"# {ticket_id}: {title}"
    actual_h1 = next((line.strip() for line in body.splitlines() if line.startswith("# ")), "")
    if actual_h1 != expected_h1:
        errors.append(f"{rel}: H1 must be exactly {expected_h1!r}")

    status = str(frontmatter.get("status", "")).strip()
    if status and status not in ALLOWED_STATUSES:
        errors.append(f"{rel}: invalid status {status!r}")

    priority = str(frontmatter.get("priority", "medium")).strip()
    if priority not in ALLOWED_PRIORITIES:
        errors.append(f"{rel}: priority must be one of: {', '.join(sorted(ALLOWED_PRIORITIES))}")

    if "due_at" in frontmatter and not is_timezone_bearing_iso_datetime(frontmatter["due_at"]):
        errors.append(f"{rel}: due_at must be a timezone-bearing ISO-8601 timestamp")

    depends_on = frontmatter.get("depends_on", [])
    if not isinstance(depends_on, list):
        errors.append(f"{rel}: depends_on must be a list when present")
    else:
        for item in depends_on:
            if not TICKET_ID_RE.match(str(item).strip()):
                errors.append(f"{rel}: depends_on entries must be ticket IDs only: {item!r}")

    claimed_by = normalize_optional_scalar(frontmatter.get("claimed_by", ""))
    thread_id = frontmatter.get("thread_id")
    compute_target = frontmatter.get("compute_target", None)
    ui_scope = frontmatter.get("ui_scope", None)
    human_gate = parse_human_gate(frontmatter.get("human_gate", None))
    if compute_target is not None:
        if not isinstance(compute_target, str) or compute_target not in ALLOWED_COMPUTE_TARGETS:
            allowed = ", ".join(sorted(ALLOWED_COMPUTE_TARGETS))
            errors.append(f"{rel}: compute_target must be one of: {allowed}")
    if ui_scope is not None and ui_scope is not True:
        errors.append(f"{rel}: ui_scope must be true when present; omit it otherwise")
    if human_gate is not None:
        tag, reason = human_gate
        allowed_human_gates = load_allowed_human_gates()
        if tag == HUMAN_GATE_NONE:
            if reason:
                errors.append(f"{rel}: human_gate none must not include a reason")
        elif not tag or not reason:
            errors.append(f"{rel}: human_gate must be none or [tag, \"reason\"]")
        elif not allowed_human_gates:
            errors.append(f"{rel}: human_gate cannot be validated because farplane/bindings.yaml human_gates is missing")
        elif tag not in allowed_human_gates:
            allowed = ", ".join(sorted(allowed_human_gates))
            errors.append(f"{rel}: human_gate tag {tag!r} must be one of: {allowed}")
    if status == "rejected":
        rejection_reason = str(frontmatter.get("rejection_reason", "")).strip()
        progress_path = path.parent / "progress.md"
        progress = progress_path.read_text(encoding="utf-8") if progress_path.is_file() else ""
        if not rejection_reason and "rejected" not in progress.lower():
            errors.append(f"{rel}: status=rejected requires rejection_reason or a rejection entry in progress.md")

    if claimed_by.lower() == GENERIC_CODEX_CLAIM:
        errors.append(
            f"{rel}: claimed_by must be a live session alias such as codex-019ef784, not plain codex"
        )

    if thread_id is not None:
        normalized_thread_id = normalize_optional_scalar(thread_id)
        if not isinstance(thread_id, str) or not normalized_thread_id:
            errors.append(f"{rel}: thread_id must be one non-empty Codex task thread id")
        elif len(normalized_thread_id) > 160 or any(ord(character) < 32 for character in normalized_thread_id):
            errors.append(f"{rel}: thread_id must be a bounded printable Codex task thread id")

    if status == "active" and not claimed_by:
        errors.append(f"{rel}: status=active requires claimed_by")
    if status != "active" and claimed_by:
        errors.append(f"{rel}: claimed_by must be absent or empty unless status=active")

    if "## Status" in body:
        errors.append(f"{rel}: legacy '## Status' block is not allowed")

    return errors


def validate_unique_thread_ids(ticket_files: list[Path]) -> list[str]:
    tickets_by_thread_id: dict[str, list[Path]] = {}
    for path in ticket_files:
        try:
            frontmatter, _ = load_ticket(path)
        except Exception:
            continue
        thread_id = normalize_optional_scalar(frontmatter.get("thread_id"))
        if thread_id:
            tickets_by_thread_id.setdefault(thread_id, []).append(path)

    errors: list[str] = []
    for thread_id, paths in sorted(tickets_by_thread_id.items()):
        if len(paths) < 2:
            continue
        locations = ", ".join(str(path.relative_to(ROOT)) for path in sorted(paths))
        errors.append(
            f"thread_id {thread_id!r} is bound to multiple tickets: {locations}"
        )
    return errors


def main() -> int:
    ticket_files = sorted(
        [
            *(p for p in TICKETS_DIR.glob("TASK-*/ticket.md") if p.is_file()),
            *(p for p in TICKETS_DIR.glob("TASK-*.md") if p.is_file()),
        ]
    )
    all_ticket_files = [
        *ticket_files,
        *(p for p in (TICKETS_DIR / "archive").glob("TASK-*/ticket.md") if p.is_file()),
    ]
    errors: list[str] = []
    for path in ticket_files:
        errors.extend(validate_ticket(path))
    errors.extend(validate_unique_thread_ids(all_ticket_files))
    if errors:
        for err in errors:
            print(err)
        return 1
    print(f"ticket metadata OK ({len(ticket_files)} ticket files checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
