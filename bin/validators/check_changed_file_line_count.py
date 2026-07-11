#!/usr/bin/env python3
"""Warn when staged files exceed explicitly enrolled line-count limits."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from fnmatch import fnmatchcase
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = ROOT / "rules" / "git-review-gates.toml"


@dataclass(frozen=True)
class LineLimitRule:
    name: str
    globs: tuple[str, ...]
    max_lines: int


@dataclass(frozen=True)
class LineCountWarning:
    path: str
    line_count: int
    rule: LineLimitRule


def normalize_path(path: str) -> str:
    normalized = path.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def load_rules(config_path: Path) -> list[LineLimitRule]:
    with config_path.open("rb") as handle:
        config: dict[str, Any] = tomllib.load(handle)
    table = config.get("changed_file_line_count")
    if not isinstance(table, dict):
        raise ValueError("config is missing [changed_file_line_count]")
    raw_rules = table.get("rule")
    if not isinstance(raw_rules, list) or not raw_rules:
        raise ValueError("changed_file_line_count.rule must be a non-empty array of tables")

    rules: list[LineLimitRule] = []
    for index, raw in enumerate(raw_rules, start=1):
        if not isinstance(raw, dict):
            raise ValueError(f"changed_file_line_count.rule[{index}] must be a table")
        name = raw.get("name")
        globs = raw.get("globs")
        max_lines = raw.get("max_lines")
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"changed_file_line_count.rule[{index}].name must be non-empty")
        if (
            not isinstance(globs, list)
            or not globs
            or not all(isinstance(item, str) and item for item in globs)
        ):
            raise ValueError(
                f"changed_file_line_count.rule[{index}].globs must be a non-empty string list"
            )
        if not isinstance(max_lines, int) or max_lines <= 0:
            raise ValueError(f"changed_file_line_count.rule[{index}].max_lines must be positive")
        rules.append(
            LineLimitRule(
                name=name.strip(),
                globs=tuple(normalize_path(item) for item in globs),
                max_lines=max_lines,
            )
        )
    return rules


def git_output(root: Path, args: list[str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def staged_paths(root: Path) -> list[str]:
    result = git_output(root, ["diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"])
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(detail or "git staged-path lookup failed")
    return [
        normalize_path(item.decode("utf-8", errors="surrogateescape"))
        for item in result.stdout.split(b"\0")
        if item
    ]


def staged_blob(root: Path, path: str) -> bytes | None:
    result = git_output(root, ["show", f":{path}"])
    return result.stdout if result.returncode == 0 else None


def matching_rule(path: str, rules: list[LineLimitRule]) -> LineLimitRule | None:
    normalized = normalize_path(path)
    return next(
        (
            rule
            for rule in rules
            if any(fnmatchcase(normalized, pattern) for pattern in rule.globs)
        ),
        None,
    )


def line_count(blob: bytes) -> int:
    return len(blob.splitlines())


def collect_warnings(
    paths: list[str],
    rules: list[LineLimitRule],
    read_blob: Callable[[str], bytes | None],
) -> list[LineCountWarning]:
    warnings: list[LineCountWarning] = []
    for path in paths:
        rule = matching_rule(path, rules)
        if rule is None:
            continue
        blob = read_blob(path)
        if blob is None:
            continue
        count = line_count(blob)
        if count > rule.max_lines:
            warnings.append(LineCountWarning(path, count, rule))
    return warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--root", default=str(ROOT))
    args = parser.parse_args()

    root = Path(args.root).resolve()
    try:
        rules = load_rules(Path(args.config).resolve())
        paths = staged_paths(root)
        warnings = collect_warnings(paths, rules, lambda path: staged_blob(root, path))
    except (OSError, RuntimeError, ValueError, tomllib.TOMLDecodeError) as exc:
        print(f"changed-file line-count check failed: {exc}", file=sys.stderr)
        return 2

    if not warnings:
        print(f"changed-file line-count check OK ({len(paths)} staged files)")
        return 0

    for warning in warnings:
        print(
            f"warning: {warning.path} has {warning.line_count} staged lines; "
            f"configured {warning.rule.name!r} limit is {warning.rule.max_lines}. "
            "This detector does not rewrite or qualitatively review the file.",
            file=sys.stderr,
        )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
