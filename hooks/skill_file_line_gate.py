#!/usr/bin/env python3
"""Return PostToolUse repair feedback for oversized edited SKILL.md files."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any


DEFAULT_MAX_LINES = 200
PATCH_PATH_PREFIXES = (
    "*** Add File: ",
    "*** Update File: ",
    "*** Move to: ",
)


def touched_paths(command: str) -> list[str]:
    """Extract destination paths from an apply_patch command."""
    paths: list[str] = []
    for line in command.splitlines():
        for prefix in PATCH_PATH_PREFIXES:
            if line.startswith(prefix):
                path = line.removeprefix(prefix).strip()
                if path and path not in paths:
                    paths.append(path)
                break
    return paths


def discover_repo_root(cwd: Path) -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
        text=True,
    )
    if result.returncode == 0 and result.stdout.strip():
        return Path(result.stdout.strip()).resolve()
    return cwd.resolve()


def edited_skill_files(
    command: str,
    *,
    cwd: Path,
    repo_root: Path,
) -> list[tuple[str, Path]]:
    root = repo_root.resolve()
    matches: list[tuple[str, Path]] = []
    for raw_path in touched_paths(command):
        candidate = Path(raw_path)
        resolved = (candidate if candidate.is_absolute() else cwd / candidate).resolve()
        try:
            relative = resolved.relative_to(root)
        except ValueError:
            continue
        if relative.parts[:1] != ("skills",) or relative.name != "SKILL.md":
            continue
        if resolved.is_file():
            matches.append((relative.as_posix(), resolved))
    return matches


def gate_skill_files(
    payload: dict[str, Any],
    *,
    max_lines: int = DEFAULT_MAX_LINES,
    repo_root: Path | None = None,
) -> dict[str, Any] | None:
    if payload.get("hook_event_name") != "PostToolUse":
        return None
    if payload.get("tool_name") not in {"apply_patch", "Edit", "Write"}:
        return None
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict) or not isinstance(tool_input.get("command"), str):
        return None

    cwd_value = payload.get("cwd")
    cwd = Path(cwd_value).resolve() if isinstance(cwd_value, str) else Path.cwd().resolve()
    root = repo_root.resolve() if repo_root is not None else discover_repo_root(cwd)
    violations: list[tuple[str, int]] = []
    for relative, path in edited_skill_files(
        tool_input["command"],
        cwd=cwd,
        repo_root=root,
    ):
        lines = len(path.read_bytes().splitlines())
        if lines > max_lines:
            violations.append((relative, lines))

    if not violations:
        return None

    details = "\n".join(
        f"- {path}: {lines} lines (maximum {max_lines})" for path, lines in violations
    )
    reason = (
        "Post-edit SKILL.md line gate failed; the edit remains applied:\n"
        f"{details}\n"
        "Fix each listed file now before continuing. Preserve default-path behavior; "
        "move only conditional examples, templates, or rare branches behind precise references."
    )
    return {
        "decision": "block",
        "reason": reason,
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                f"Every edited skills/**/SKILL.md must be at most {max_lines} physical lines. "
                "Re-run the edit until the listed files pass."
            ),
        },
    }


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError):
        return 0
    if not isinstance(payload, dict):
        return 0
    result = gate_skill_files(payload)
    if result is not None:
        json.dump(result, sys.stdout)
        sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
