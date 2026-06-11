#!/usr/bin/env python3
"""Import selected installed Codex skills back into Farplane source."""

from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Sequence

from install_selected_skills import (
    EMBEDDED_TODOS_BEGIN,
    EMBEDDED_TODOS_END,
    Skill,
    discover_skills,
    filter_skills,
    parse_skill_names,
)


DESCRIPTION_MAX_CHARS = 220
IGNORE_NAMES = {
    ".DS_Store",
    "__pycache__",
    ".pytest_cache",
}


@dataclass(frozen=True)
class ImportResult:
    imported: list[str]
    overwritten: list[str]
    skipped_existing: list[str]
    missing: list[str]
    warnings: dict[str, list[str]]
    backup_root: str
    dry_run: bool


def repo_skills_dir(repo: Path) -> Path:
    return repo / "skills"


def skill_row(skill: Skill, repo: Path) -> dict[str, object]:
    dest = repo_skills_dir(repo) / skill.name
    description = skill.description or ""
    warnings = skill_warnings(skill)
    return {
        "name": skill.name,
        "description": description,
        "description_chars": len(description),
        "source": skill.source,
        "tier": skill.tier,
        "path": str(skill.path),
        "repo_status": "exists" if dest.exists() else "new",
        "warnings": warnings,
    }


def skill_warnings(skill: Skill) -> list[str]:
    warnings: list[str] = []
    if not skill.description:
        warnings.append("missing description")
    elif len(skill.description) > DESCRIPTION_MAX_CHARS:
        warnings.append(
            f"description over {DESCRIPTION_MAX_CHARS} chars ({len(skill.description)})"
        )
    if not skill.tier:
        warnings.append("missing tier")
    if not skill.source:
        warnings.append("missing source")
    return warnings


def render_table(skills: Sequence[Skill], repo: Path) -> str:
    if not skills:
        return "No matching installed skills."

    lines = [f"{'NAME':28} {'STATUS':8} {'TIER':6} {'SOURCE':9} DESCRIPTION"]
    for skill in skills:
        row = skill_row(skill, repo)
        description = str(row["description"]).replace("\n", " ")
        if len(description) > 78:
            description = description[:75].rstrip() + "..."
        lines.append(
            f"{skill.name:28} {str(row['repo_status'])[:8]:8} "
            f"{skill.tier[:6]:6} {skill.source[:9]:9} {description}"
        )
    return "\n".join(lines)


def strip_embedded_todos(text: str) -> tuple[str, bool]:
    """Remove install-rendered todo blocks so repo source stays canonical."""
    changed = False
    while True:
        begin = text.find(EMBEDDED_TODOS_BEGIN)
        if begin < 0:
            break
        end = text.find(EMBEDDED_TODOS_END, begin)
        if end < 0:
            break
        end += len(EMBEDDED_TODOS_END)
        text = text[:begin].rstrip() + "\n" + text[end:].lstrip("\n")
        changed = True
    return text.rstrip() + "\n", changed


def copy_ignore(_dir: str, names: list[str]) -> set[str]:
    return {name for name in names if name in IGNORE_NAMES}


def copy_skill_package(src: Path, dest: Path, dry_run: bool) -> bool:
    if dry_run:
        return False

    shutil.copytree(src, dest, symlinks=True, ignore=copy_ignore)
    skill_file = dest / "SKILL.md"
    skill_text, stripped = strip_embedded_todos(skill_file.read_text(encoding="utf-8"))
    skill_file.write_text(skill_text, encoding="utf-8")
    return stripped


def backup_existing(dest: Path, backup_root: Path, dry_run: bool) -> None:
    if dry_run:
        return
    backup_dest = backup_root / "skills" / dest.name
    backup_dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(dest), str(backup_dest))


def import_skills(
    source: Path,
    repo: Path,
    names: Sequence[str],
    overwrite: bool,
    dry_run: bool,
) -> ImportResult:
    installed = {skill.name: skill for skill in discover_skills(source)}
    missing = [name for name in names if name not in installed]
    selected = [installed[name] for name in names if name in installed]

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_root = repo / ".farplane" / "import-backups" / stamp
    dest_root = repo_skills_dir(repo)

    imported: list[str] = []
    overwritten: list[str] = []
    skipped_existing: list[str] = []
    warnings: dict[str, list[str]] = {}

    for skill in selected:
        dest = dest_root / skill.name
        skill_notes = skill_warnings(skill)
        if dest.exists() or dest.is_symlink():
            if not overwrite:
                skipped_existing.append(skill.name)
                warnings[skill.name] = skill_notes + ["repo skill exists; use --overwrite"]
                continue
            overwritten.append(skill.name)
            backup_existing(dest, backup_root, dry_run)

        stripped = copy_skill_package(skill.path, dest, dry_run)
        if stripped:
            skill_notes.append("removed generated embedded todo block from SKILL.md")
        if skill_notes:
            warnings[skill.name] = skill_notes
        imported.append(skill.name)

    for name in missing:
        warnings[name] = ["not found in installed skills source"]

    return ImportResult(
        imported=imported,
        overwritten=overwritten,
        skipped_existing=skipped_existing,
        missing=missing,
        warnings=warnings,
        backup_root=str(backup_root),
        dry_run=dry_run,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Import selected installed Codex skills into Farplane source."
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Farplane repo root. Defaults to this script's repo.",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=Path.home() / ".codex" / "skills",
        help="Installed Codex skills directory. Defaults to ~/.codex/skills.",
    )
    parser.add_argument("--list", action="store_true", help="List installed skills.")
    parser.add_argument("--search", help="Search installed skill names and descriptions.")
    parser.add_argument("--skills", help="Comma-separated skill names to import.")
    parser.add_argument(
        "--skill",
        action="append",
        help="Skill name to import. Can be repeated or comma-separated.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace existing repo skill directories after backing them up.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would happen without changing files.",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo = args.repo.expanduser().resolve()
    source = args.source.expanduser().resolve()
    names = parse_skill_names(args.skills, args.skill)

    if args.list or args.search:
        try:
            matches = filter_skills(discover_skills(source), args.search)
        except FileNotFoundError as exc:
            raise SystemExit(str(exc)) from exc
        if args.json:
            print(json.dumps([skill_row(skill, repo) for skill in matches], indent=2))
        else:
            print(render_table(matches, repo))
        return 0

    if not names:
        raise SystemExit("No skills selected. Use --list, --search, or --skills name1,name2.")

    try:
        result = import_skills(source, repo, names, args.overwrite, args.dry_run)
    except FileNotFoundError as exc:
        raise SystemExit(str(exc)) from exc

    if args.json:
        print(json.dumps(asdict(result), indent=2))
    else:
        prefix = "dry-run " if result.dry_run else ""
        print(f"{prefix}imported: {', '.join(result.imported) or 'none'}")
        print(f"{prefix}overwritten: {', '.join(result.overwritten) or 'none'}")
        print(f"{prefix}skipped existing: {', '.join(result.skipped_existing) or 'none'}")
        print(f"{prefix}missing: {', '.join(result.missing) or 'none'}")
        print(f"backups: {result.backup_root}")
        for name, notes in result.warnings.items():
            print(f"warning {name}: {'; '.join(notes)}")

    return 1 if result.missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
