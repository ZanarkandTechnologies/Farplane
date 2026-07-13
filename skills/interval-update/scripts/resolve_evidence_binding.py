#!/usr/bin/env python3
"""Resolve Interval's configured kanban evidence source without reading evidence."""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path
from typing import Any

import yaml


DEFAULT_PRIVATE_CONTEXT = Path.home() / ".codex" / "private" / "docs" / "notion.md"
SUPPORTED_PROVIDERS = {"filesystem_tickets", "notion"}
FILESYSTEM_POLICIES = {"include", "exclude"}
PRIVATE_HANDLE_PATTERN = re.compile(r"^[a-z][a-z0-9_-]*(?:\.[a-z][a-z0-9_-]*)+$")


def read_bindings(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid_bindings_yaml:{exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("invalid_bindings_shape:expected_object")
    return payload


def source_gap(code: str, effect: str) -> dict[str, str]:
    return {"code": code, "effect": effect, "fallback": "none"}


def safe_relative_path(value: Any, default: str) -> str:
    raw = str(value or default).strip()
    path = Path(raw)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"unsafe_project_relative_path:{raw}")
    return path.as_posix()


def resolve_binding(
    project_root: Path,
    *,
    private_context: Path = DEFAULT_PRIVATE_CONTEXT,
    ntn_executable: str = "ntn",
) -> dict[str, Any]:
    bindings_path = project_root / "farplane" / "bindings.yaml"
    bindings = read_bindings(bindings_path)
    if bindings is None:
        return {
            "bindings_ref": None,
            "provider": "filesystem_tickets",
            "provider_coordinates": {
                "tickets_dir": "tickets",
                "archive_dir": "tickets/archive",
            },
            "filesystem_ticket_policy": "include",
            "access_route": "project_filesystem",
            "access_ready": (project_root / "tickets").is_dir(),
            "legacy_default": True,
            "source_gaps": []
            if (project_root / "tickets").is_dir()
            else [source_gap("filesystem_tickets_unavailable", "ticket evidence unavailable")],
        }

    integrations = bindings.get("integrations")
    integrations = integrations if isinstance(integrations, dict) else {}
    kanban = integrations.get("kanban")
    if not isinstance(kanban, dict):
        return {
            "bindings_ref": "farplane/bindings.yaml#integrations.kanban",
            "provider": None,
            "provider_coordinates": {},
            "filesystem_ticket_policy": "exclude",
            "access_route": None,
            "access_ready": False,
            "legacy_default": False,
            "source_gaps": [source_gap("kanban_binding_missing", "kanban evidence unavailable")],
        }

    provider = str(kanban.get("provider") or "").strip()
    filesystem_policy = str(kanban.get("filesystem_ticket_policy") or "").strip()
    if not filesystem_policy:
        filesystem_policy = "include" if provider == "filesystem_tickets" else "exclude"
    if filesystem_policy not in FILESYSTEM_POLICIES:
        raise ValueError(f"unsupported_filesystem_ticket_policy:{filesystem_policy}")
    if provider not in SUPPORTED_PROVIDERS:
        return {
            "bindings_ref": "farplane/bindings.yaml#integrations.kanban",
            "provider": provider or None,
            "provider_coordinates": {},
            "filesystem_ticket_policy": filesystem_policy,
            "access_route": None,
            "access_ready": False,
            "legacy_default": False,
            "source_gaps": [source_gap("kanban_provider_unsupported", "kanban evidence unavailable")],
        }

    if provider == "filesystem_tickets":
        if filesystem_policy == "exclude":
            return {
                "bindings_ref": "farplane/bindings.yaml#integrations.kanban",
                "provider": provider,
                "provider_coordinates": {},
                "filesystem_ticket_policy": filesystem_policy,
                "access_route": None,
                "access_ready": False,
                "legacy_default": False,
                "source_gaps": [
                    source_gap("filesystem_tickets_excluded", "ticket evidence excluded by policy")
                ],
            }
        coordinates = {
            "tickets_dir": safe_relative_path(kanban.get("tickets_dir"), "tickets"),
            "archive_dir": safe_relative_path(kanban.get("archive_dir"), "tickets/archive"),
        }
        tickets_root = project_root / coordinates["tickets_dir"]
        gaps = [] if tickets_root.is_dir() else [
            source_gap("filesystem_tickets_unavailable", "ticket evidence unavailable")
        ]
        return {
            "bindings_ref": "farplane/bindings.yaml#integrations.kanban",
            "provider": provider,
            "provider_coordinates": coordinates,
            "filesystem_ticket_policy": filesystem_policy,
            "access_route": "project_filesystem",
            "access_ready": not gaps,
            "legacy_default": False,
            "source_gaps": gaps,
        }

    private_handle = str(kanban.get("task_source_handle") or "notion.tasks.source").strip()
    gaps: list[dict[str, str]] = []
    if not PRIVATE_HANDLE_PATTERN.fullmatch(private_handle):
        gaps.append(source_gap("notion_private_handle_invalid", "Notion task evidence unavailable"))
    private_context_text = ""
    if not private_context.is_file():
        gaps.append(source_gap("notion_private_context_missing", "Notion task evidence unavailable"))
    else:
        private_context_text = private_context.read_text(encoding="utf-8", errors="replace")
        if PRIVATE_HANDLE_PATTERN.fullmatch(private_handle) and private_handle not in private_context_text:
            gaps.append(source_gap("notion_private_handle_unresolved", "Notion task evidence unavailable"))
    if shutil.which(ntn_executable) is None:
        gaps.append(source_gap("ntn_unavailable", "Notion task evidence unavailable"))
    return {
        "bindings_ref": "farplane/bindings.yaml#integrations.kanban",
        "provider": provider,
        "provider_coordinates": (
            {"task_source_handle": private_handle}
            if PRIVATE_HANDLE_PATTERN.fullmatch(private_handle)
            else {}
        ),
        "filesystem_ticket_policy": filesystem_policy,
        "access_route": "private_handle_ntn",
        "access_ready": None if not gaps else False,
        "access_check": "required_compact_ntn_query" if not gaps else "blocked",
        "legacy_default": False,
        "source_gaps": gaps,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--private-context", default=str(DEFAULT_PRIVATE_CONTEXT))
    parser.add_argument("--ntn-executable", default="ntn")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = resolve_binding(
            Path(args.project_root).resolve(),
            private_context=Path(args.private_context).expanduser(),
            ntn_executable=args.ntn_executable,
        )
    except ValueError as exc:
        result = {
            "bindings_ref": "farplane/bindings.yaml",
            "provider": None,
            "provider_coordinates": {},
            "filesystem_ticket_policy": "exclude",
            "access_route": None,
            "access_ready": False,
            "legacy_default": False,
            "source_gaps": [source_gap(str(exc).split(":", 1)[0], "kanban evidence unavailable")],
        }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
