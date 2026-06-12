#!/usr/bin/env python3
"""Validate local file references in tracked Farplane text files."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
TEXT_SUFFIXES = {
    ".json",
    ".jsonl",
    ".md",
    ".py",
    ".sh",
    ".toml",
    ".tpl",
    ".txt",
    ".yaml",
    ".yml",
}
ROOT_TEXT_FILES = {"AGENTS.md", "ARCHITECTURE.md", "README.md"}
DEFAULT_SCAN_PREFIXES = (
    "docs/features/",
    "docs/fundamentals/",
    "docs/review/",
    "docs/skills/",
    "docs/sources/",
    "docs/specs/",
)
SKIP_FILE_PREFIXES = (
    ".git/",
    ".farplane/",
    "agents/",
    "bin/test_",
    "docs/archive/",
    "docs/doc-audit/",
    "node_modules/",
    "skills/skill-maintenance/graph/",
    "tests/",
    "tickets/",
    "tickets/archive/",
)
SKIP_TARGET_PREFIXES = (
    ".git/",
    ".farplane/",
)
KNOWN_TOP_LEVELS = {
    "AGENTS.md",
    "ARCHITECTURE.md",
    "README.md",
    "agents",
    "assets",
    "bin",
    "docs",
    "experiments",
    "qa",
    "rules",
    "skills",
    "templates",
    "tests",
    "tickets",
}
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_LINK_RE = re.compile(r"""(?:href|src)=["']([^"']+)["']""")
PATH_TOKEN_RE = re.compile(
    r"(?<![A-Za-z0-9_@:/.-])"
    r"(?P<path>(?:\.{1,2}/)?(?:AGENTS\.md|ARCHITECTURE\.md|README\.md|"
    r"(?:agents|assets|bin|docs|experiments|qa|rules|skills|templates|tests|tickets)/"
    r"[A-Za-z0-9_./@+=:%#-]+))"
)


@dataclass(frozen=True)
class Ref:
    source: Path
    line_number: int
    raw: str
    target: Path


def tracked_files(root: Path) -> list[Path]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=root,
            check=True,
            capture_output=True,
            text=False,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return sorted(
            path.relative_to(root)
            for path in root.rglob("*")
            if path.is_file() and ".git" not in path.parts
        )
    return [
        Path(raw.decode("utf-8"))
        for raw in result.stdout.split(b"\0")
        if raw
    ]


def is_scanned_file(path: Path) -> bool:
    path_string = path.as_posix()
    if any(path_string.startswith(prefix) for prefix in SKIP_FILE_PREFIXES):
        return False
    if path.name in ROOT_TEXT_FILES:
        return True
    return path.suffix in TEXT_SUFFIXES


def looks_like_local_ref(raw: str) -> bool:
    if not raw:
        return False
    if raw.startswith(("#", "http://", "https://", "mailto:", "tel:")):
        return False
    if raw.startswith("data:"):
        return False
    if any(marker in raw for marker in ("*", "<", ">", "{", "}", "$(", "...")):
        return False
    if re.search(r"\b(?:TASK-\d{4}|TASK-XXXX|TASK-\*)\b|tickets/TASK-", raw):
        return False
    if re.search(r"\b(?:YYYY|MM|DD|HHMM|my-skill|name|example)\b", raw):
        return False
    if raw in {"docs/bootstrap-brief.md"}:
        return False
    if raw in {".", "..", "/"}:
        return False
    return True


def strip_ref(raw: str) -> str:
    value = unquote(raw.strip().strip("`'\""))
    value = value.split("#", 1)[0]
    value = value.split("?", 1)[0]
    while value.endswith((".", ",", ":", ";")):
        value = value[:-1]
    return value


def resolve_ref(root: Path, source: Path, raw: str) -> Path | None:
    value = strip_ref(raw)
    if not looks_like_local_ref(value):
        return None

    if value.startswith("/"):
        absolute = Path(value)
        try:
            relative = absolute.resolve().relative_to(root.resolve())
        except ValueError:
            return None
        return root / relative

    local_relative = (root / source.parent / value).resolve()
    first_part = value.split("/", 1)[0]
    if value.startswith(("./", "../")):
        return local_relative
    if local_relative.exists():
        return local_relative
    if first_part in KNOWN_TOP_LEVELS:
        return root / value
    return None


def iter_line_refs(root: Path, source: Path, line: str, line_number: int) -> list[Ref]:
    refs: list[Ref] = []
    seen: set[tuple[str, Path]] = set()

    raw_values = [match.group(1) for match in MARKDOWN_LINK_RE.finditer(line)]
    raw_values.extend(match.group(1) for match in HTML_LINK_RE.finditer(line))
    raw_values.extend(match.group("path") for match in PATH_TOKEN_RE.finditer(line))

    for raw in raw_values:
        target = resolve_ref(root, source, raw)
        if target is None:
            continue
        key = (raw, target)
        if key in seen:
            continue
        seen.add(key)
        refs.append(Ref(source=source, line_number=line_number, raw=raw, target=target))
    return refs


def is_existing_target(target: Path) -> bool:
    path_string = target.as_posix()
    if any(path_string.endswith(prefix.rstrip("/")) for prefix in SKIP_TARGET_PREFIXES):
        return True
    return target.exists()


def is_default_scope(path: Path) -> bool:
    path_string = path.as_posix()
    if len(path.parts) == 1 and path.name in ROOT_TEXT_FILES:
        return True
    return any(path_string.startswith(prefix) for prefix in DEFAULT_SCAN_PREFIXES)


def validate_root(root: Path, all_files: bool = False) -> list[str]:
    errors: list[str] = []
    checked_refs = 0
    for source in tracked_files(root):
        if not all_files and not is_default_scope(source):
            continue
        if not is_scanned_file(source):
            continue
        path = root / source
        if not path.exists():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        in_fence = False
        for line_number, line in enumerate(text.splitlines(), start=1):
            if path.suffix == ".md" and line.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            for ref in iter_line_refs(root, source, line, line_number):
                checked_refs += 1
                if is_existing_target(ref.target):
                    continue
                target_display = ref.target
                try:
                    target_display = ref.target.relative_to(root)
                except ValueError:
                    pass
                errors.append(
                    f"{ref.source}:{ref.line_number}: missing local ref "
                    f"{ref.raw!r} -> {target_display}"
                )
    if not errors:
        print(f"doc refs OK ({checked_refs} refs checked)")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check tracked text files for stale local file references."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="Repository root to validate (defaults to the current repo).",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help=(
            "Scan every tracked text file, including tests, tickets, experiments, "
            "and historical material. This is useful for cleanup audits and may "
            "surface example placeholders."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    errors = validate_root(root, all_files=args.all)
    if errors:
        for error in errors:
            print(error)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
