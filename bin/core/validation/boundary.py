"""Resolve explicit changed-path boundaries without reading a shared dirty worktree."""

from __future__ import annotations

import subprocess
from pathlib import Path, PurePosixPath

from .models import PathBoundary
from .select import normalize_path


def _safe_relative(path: str) -> str:
    normalized = normalize_path(path)
    parsed = PurePosixPath(normalized)
    if parsed.is_absolute() or ".." in parsed.parts or not normalized:
        raise ValueError(f"changed path must be repository-relative without traversal: {path}")
    return normalized


def explicit_boundary(paths: list[str]) -> PathBoundary:
    return PathBoundary(source="explicit", paths=tuple(sorted(set(_safe_relative(path) for path in paths))))


def base_boundary(root: Path, base: str) -> PathBoundary:
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMR", f"{base}...HEAD"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise ValueError(result.stdout.strip() or result.stderr.strip() or f"git diff failed for {base}")
    paths = tuple(sorted(_safe_relative(line) for line in result.stdout.splitlines() if line.strip()))
    return PathBoundary(source="git-base", paths=paths, base=base)


def unavailable_boundary() -> PathBoundary:
    return PathBoundary(source="unavailable")
