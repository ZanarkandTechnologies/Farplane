#!/usr/bin/env python3
"""Validate direct skill todo lists."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


TODO_HEADING = "## Todo List"
CONTEXT_HEADING = "## Context"
CHECKLIST_BEGIN = "<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->"
CHECKLIST_END = "<!-- END FARPLANE_IMPORTANT_CHECKLIST -->"
SOURCE_RE = re.compile(r"^Source: `[^`\n]+`\n\n?", re.MULTILINE)
MARKED_SECTION_RE = re.compile(
    rf"^{re.escape(CHECKLIST_BEGIN)}\n.*?^{re.escape(CHECKLIST_END)}\n?",
    re.MULTILINE | re.DOTALL,
)
SECTION_RE = re.compile(
    rf"^{re.escape(TODO_HEADING)}\n.*?(?=^## |\Z)",
    re.MULTILINE | re.DOTALL,
)


class ChecklistError(Exception):
    pass


def find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "bin/validators/sync_skill_registry.py").exists() and (candidate / "skills").exists():
            return candidate
    raise ChecklistError("could not find Farplane repo root")


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ChecklistError(f"{path}: missing frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        raise ChecklistError(f"{path}: unterminated frontmatter")

    metadata: dict[str, str] = {}
    for raw_line in text[4:end].splitlines():
        if not raw_line.strip() or raw_line.startswith(" "):
            continue
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        metadata[key.strip()] = value.strip().strip("\"'")
    return metadata


def strip_source_line(checklist_text: str) -> str:
    return SOURCE_RE.sub("", checklist_text.strip(), count=1).strip()


def normalize_checklist(checklist_text: str) -> str:
    return "\n".join(line.rstrip() for line in strip_source_line(checklist_text).splitlines()).strip()


def extract_marked_checklist(skill_text: str) -> str | None:
    match = MARKED_SECTION_RE.search(skill_text)
    if not match:
        return None
    section = match.group(0)
    lines = section.strip().splitlines()
    if lines and lines[0].strip() == CHECKLIST_BEGIN:
        lines = lines[1:]
    if lines and lines[0].strip() == TODO_HEADING:
        lines = lines[1:]
    if lines and lines[-1].strip() == CHECKLIST_END:
        lines = lines[:-1]
    return strip_source_line("\n".join(lines))


def render_section(checklist_text: str) -> str:
    checklist = strip_source_line(checklist_text)
    if not checklist:
        raise ChecklistError("checklist is empty")
    return (
        f"{CHECKLIST_BEGIN}\n"
        f"{TODO_HEADING}\n\n"
        f"{checklist}\n"
        f"{CHECKLIST_END}\n"
    )


def body_start(lines: list[str]) -> int:
    if not lines or lines[0].strip() != "---":
        return 0
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            next_index = index + 1
            while next_index < len(lines) and not lines[next_index].strip():
                next_index += 1
            return next_index
    return 0


def insertion_index(lines: list[str]) -> int:
    start = body_start(lines)
    for index in range(start, len(lines)):
        if lines[index].startswith("# "):
            next_index = index + 1
            while next_index < len(lines) and not lines[next_index].strip():
                next_index += 1
            if next_index < len(lines) and lines[next_index].strip() == CONTEXT_HEADING:
                for context_index in range(next_index + 1, len(lines)):
                    if lines[context_index].startswith("## "):
                        return context_index
                return len(lines)
            return next_index
    return start


def insert_section(skill_text: str, section: str) -> str:
    lines = skill_text.rstrip().splitlines()
    index = insertion_index(lines)
    before = "\n".join(lines[:index]).rstrip()
    after = "\n".join(lines[index:]).lstrip("\n")
    return f"{before}\n\n{section}\n{after}\n"


def normalize_skill_text(skill_text: str) -> str:
    checklist = extract_marked_checklist(skill_text)
    if checklist is None:
        if SECTION_RE.search(skill_text.rstrip()):
            raise ChecklistError(
                f"unmarked {TODO_HEADING!r} section; remove it or wrap it in "
                f"{CHECKLIST_BEGIN} / {CHECKLIST_END} markers before syncing"
            )
        raise ChecklistError("missing direct Todo List section")
    section = render_section(checklist)
    return MARKED_SECTION_RE.sub(section.rstrip() + "\n", skill_text.rstrip(), count=1).rstrip() + "\n"


def iter_skill_dirs(repo_root: Path) -> list[Path]:
    return sorted(
        skill_dir
        for skill_dir in (repo_root / "skills").iterdir()
        if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists()
    )


def sync_repo(repo_root: Path, write: bool) -> int:
    stale: list[str] = []
    missing: list[str] = []
    legacy: list[str] = []
    updated: list[str] = []
    skipped_external: list[str] = []

    for skill_dir in iter_skill_dirs(repo_root):
        skill_path = skill_dir / "SKILL.md"
        todos_path = skill_dir / "todos.md"
        metadata = parse_frontmatter(skill_path)
        source = metadata.get("source", "local")

        current = skill_path.read_text(encoding="utf-8")

        if todos_path.exists():
            legacy.append(str(todos_path.relative_to(repo_root)))
            continue

        if source == "external" and extract_marked_checklist(current) is None:
            skipped_external.append(skill_dir.name)
            continue

        try:
            expected = normalize_skill_text(current)
        except ChecklistError as exc:
            missing.append(f"{skill_path.relative_to(repo_root)}: {exc}")
            continue
        if current != expected:
            stale.append(str(skill_path.relative_to(repo_root)))
            if write:
                skill_path.write_text(expected, encoding="utf-8")
                updated.append(str(skill_path.relative_to(repo_root)))

    if missing:
        print("skills missing required direct todo lists:", file=sys.stderr)
        for item in missing:
            print(f"- {item}", file=sys.stderr)
    if legacy:
        print("skill-local todos.md files are no longer supported:", file=sys.stderr)
        for item in legacy:
            print(f"- {item}", file=sys.stderr)
    if stale and not write:
        print("skill todo lists need normalization; run with --write:", file=sys.stderr)
        for item in stale:
            print(f"- {item}", file=sys.stderr)
    if updated:
        print(f"synced {len(updated)} skill todo list section(s)")
    else:
        print("skill todo list sections OK")
    if skipped_external:
        names = ", ".join(skipped_external)
        print(f"external skills without direct todo lists skipped: {names}")

    return 1 if missing or legacy or (stale and not write) else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="update stale SKILL.md todo lists")
    parser.add_argument(
        "--repo",
        type=Path,
        default=find_repo_root(Path(__file__).resolve()),
        help="Farplane repo root",
    )
    args = parser.parse_args()
    return sync_repo(args.repo.resolve(), args.write)


if __name__ == "__main__":
    raise SystemExit(main())
