#!/usr/bin/env python3
"""Board adapter contracts for Farplane work items."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol


TICKET_ID_RE = re.compile(r"^TASK-\d{4}$")
COMPUTE_TARGETS = ("local_shared", "local_worktree", "symphony", "codex_cloud")


class BoardAdapterError(ValueError):
    """Raised when a board adapter cannot safely read or normalize a work item."""


@dataclass(frozen=True)
class WorkItem:
    source: str
    id: str
    identifier: str
    title: str
    description: str
    state: str
    phase: str
    status: str
    priority: str
    labels: tuple[str, ...]
    blocked_by: tuple[str, ...]
    depends_on: tuple[str, ...]
    ready: bool
    approval_required: bool
    requires_qa: bool
    requires_demo: bool
    compute_target: str | None
    local_ticket_path: str
    artifacts_path: str
    url: str | None
    metadata: dict[str, Any] = field(default_factory=dict)

    def public_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "id": self.id,
            "identifier": self.identifier,
            "title": self.title,
            "description": self.description,
            "state": self.state,
            "phase": self.phase,
            "status": self.status,
            "priority": self.priority,
            "labels": list(self.labels),
            "blockedBy": list(self.blocked_by),
            "dependsOn": list(self.depends_on),
            "ready": self.ready,
            "approvalRequired": self.approval_required,
            "requiresQa": self.requires_qa,
            "requiresDemo": self.requires_demo,
            "computeTarget": self.compute_target,
            "localTicketPath": self.local_ticket_path,
            "artifactsPath": self.artifacts_path,
            "url": self.url,
            "metadata": self.metadata,
        }


@dataclass(frozen=True)
class WorkItemSelector:
    work_item_id: str | None = None
    work_item_path: str | None = None


@dataclass(frozen=True)
class WriteResult:
    ok: bool
    changed: bool
    message: str
    path: str | None = None


class BoardAdapter(Protocol):
    kind: str

    def list_candidates(self, *, active_phases: tuple[str, ...] = ()) -> list[WorkItem]:
        ...

    def read_work_item(self, selector: WorkItemSelector) -> WorkItem:
        ...

    def write_evidence(
        self, item: WorkItem, artifact_path: str, *, label: str = ""
    ) -> WriteResult:
        ...


def resolve_path(path: str | Path, root: Path) -> Path:
    candidate = Path(path).expanduser()
    if not candidate.is_absolute():
        candidate = root / candidate
    return candidate.resolve()


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def normalize_ticket_id(value: str) -> str:
    ticket_id = value.strip().upper()
    if not TICKET_ID_RE.fullmatch(ticket_id):
        raise BoardAdapterError(f"invalid ticket id: {value}")
    return ticket_id


def parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if value in {"true", "false"}:
        return value == "true"
    if value == "[]":
        return []
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(part.strip()) for part in inner.split(",")]
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def parse_yaml_map(raw: str) -> dict[str, Any]:
    root: dict[str, Any] = {}
    lines = raw.splitlines()
    index = 0
    while index < len(lines):
        original = lines[index]
        if not original.strip() or original.lstrip().startswith("#"):
            index += 1
            continue
        if not original.startswith(" ") and ":" in original:
            key, raw_value = original.split(":", 1)
            key = key.strip()
            value = raw_value.strip()
            if value == "":
                items: list[Any] = []
                index += 1
                while index < len(lines) and lines[index].startswith("  - "):
                    items.append(parse_scalar(lines[index][4:].strip()))
                    index += 1
                root[key] = items
                continue
            root[key] = parse_scalar(value)
        index += 1
    return root


def parse_frontmatter_markdown(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text.strip()
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        raise BoardAdapterError("missing closing front matter marker")
    config = parse_yaml_map(parts[0][4:])
    return config, parts[1].strip()


def normalize_bool(value: Any) -> bool:
    return value is True or value == "true"


def normalize_string_list(value: Any) -> tuple[str, ...]:
    if isinstance(value, list):
        return tuple(str(item).strip() for item in value if str(item).strip())
    return ()


def require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise BoardAdapterError(f"{label} must be a non-empty string")
    return value.strip()


def h1_title(body: str) -> str:
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            title = stripped[2:].strip()
            if ": " in title:
                return title.split(": ", 1)[1].strip()
            return title
    return ""


def normalize_ticket(frontmatter: dict[str, Any], body: str, path: Path) -> WorkItem:
    ticket_id = normalize_ticket_id(str(frontmatter.get("ticket_id") or path.parent.name))
    compute_target = frontmatter.get("compute_target")
    if compute_target is not None:
        compute_target = require_string(compute_target, "compute_target")
        if compute_target not in COMPUTE_TARGETS:
            raise BoardAdapterError(f"unknown compute_target: {compute_target}")
    title = str(frontmatter.get("title") or h1_title(body) or ticket_id).strip()
    status = str(frontmatter.get("status") or "").strip()
    phase = str(frontmatter.get("phase") or "").strip()
    return WorkItem(
        source="filesystem",
        id=ticket_id,
        identifier=ticket_id,
        title=title,
        description=body.strip(),
        state=status,
        phase=phase,
        status=status,
        priority=str(frontmatter.get("priority") or "").strip(),
        labels=normalize_string_list(frontmatter.get("labels")),
        blocked_by=normalize_string_list(frontmatter.get("blocked_by")),
        depends_on=normalize_string_list(frontmatter.get("depends_on")),
        ready=normalize_bool(frontmatter.get("ready")),
        approval_required=normalize_bool(frontmatter.get("approval_required")),
        requires_qa=normalize_bool(frontmatter.get("requires_qa")),
        requires_demo=normalize_bool(frontmatter.get("requires_demo")),
        compute_target=compute_target,
        local_ticket_path=str(path),
        artifacts_path=str(path.parent / "artifacts"),
        url=None,
        metadata=dict(frontmatter),
    )


class FileTicketAdapter:
    kind = "filesystem"

    def __init__(self, root: str | Path, source: str = "tickets/") -> None:
        self.root = Path(root).resolve()
        self.source = source
        self.source_root = resolve_path(source, self.root)
        if not is_under(self.source_root, self.root):
            raise BoardAdapterError(f"board source must stay under project root: {self.source_root}")
        if not self.source_root.exists():
            raise BoardAdapterError(f"board source not found: {self.source_root}")
        if not self.source_root.is_dir():
            raise BoardAdapterError(f"board source must be a directory: {self.source_root}")

    def ticket_path_from_selector(self, selector: WorkItemSelector) -> Path:
        if selector.work_item_path:
            path = resolve_path(selector.work_item_path, self.root)
        elif selector.work_item_id:
            path = self.source_root / normalize_ticket_id(selector.work_item_id) / "ticket.md"
        else:
            raise BoardAdapterError("selector must include work_item_id or work_item_path")
        if not path.exists():
            raise BoardAdapterError(f"ticket not found: {path}")
        if path.name != "ticket.md":
            raise BoardAdapterError(f"ticket path must point to ticket.md: {path}")
        if not is_under(path, self.source_root):
            raise BoardAdapterError(f"ticket path must stay under {self.source}/: {path}")
        return path

    def read_work_item(self, selector: WorkItemSelector) -> WorkItem:
        path = self.ticket_path_from_selector(selector)
        frontmatter, body = parse_frontmatter_markdown(path.read_text(encoding="utf-8"))
        return normalize_ticket(frontmatter, body, path)

    def list_candidates(self, *, active_phases: tuple[str, ...] = ()) -> list[WorkItem]:
        items: list[WorkItem] = []
        for path in sorted(self.source_root.glob("TASK-*/ticket.md")):
            item = self.read_work_item(WorkItemSelector(work_item_path=str(path)))
            if active_phases and item.phase not in active_phases:
                continue
            items.append(item)
        return items

    def write_evidence(
        self, item: WorkItem, artifact_path: str, *, label: str = ""
    ) -> WriteResult:
        return WriteResult(
            ok=False,
            changed=False,
            message=(
                "filesystem evidence writeback is manual in BoardAdapter v1; "
                "link artifacts through the ticket Links or State section"
            ),
            path=item.local_ticket_path,
        )


def adapter_from_config(*, kind: str, root: str | Path, source: str = "tickets/") -> BoardAdapter:
    if kind == "filesystem":
        return FileTicketAdapter(root, source)
    raise BoardAdapterError(f"unsupported board adapter: {kind}")
