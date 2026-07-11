"""Deterministic phase and changed-path check selection."""

from __future__ import annotations

from fnmatch import fnmatchcase
from pathlib import Path
import tomllib

from .models import PathBoundary, ValidationPhase


def normalize_path(path: str) -> str:
    value = path.replace("\\", "/")
    while value.startswith("./"):
        value = value[2:]
    return value


def select_checks(
    phase: ValidationPhase,
    boundary: PathBoundary,
    ticket_text: str,
    rules_path: Path,
) -> list[str]:
    with rules_path.open("rb") as handle:
        policy = tomllib.load(handle)
    phase_policy = policy.get("phase", {}).get(phase, {})
    selected = list(phase_policy.get("checks", []))
    if phase == "planning" or ("Visual companion:" in ticket_text and "diagrams.md" in ticket_text):
        selected.append("ticket.visual-companion")
    if phase == "complete":
        if boundary.source == "unavailable":
            raise ValueError("complete validation requires an explicit --path or --base boundary")
        normalized_paths = [normalize_path(path) for path in boundary.paths]
        for item in policy.get("path_check", []):
            globs = item.get("globs", [])
            check_ids = item.get("checks", [])
            if any(fnmatchcase(path, pattern) for path in normalized_paths for pattern in globs):
                for check_id in check_ids:
                    if check_id not in selected:
                        selected.append(check_id)
    return selected


def relative_ticket(ticket: Path, root: Path) -> str:
    try:
        return ticket.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(ticket.resolve())
