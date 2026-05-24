#!/usr/bin/env python3
"""Search and install selected Codexter skills into a Codex home."""

from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Sequence


EMBEDDED_TODOS_BEGIN = "<!-- BEGIN CODEXTER_EMBEDDED_TODOS -->"
EMBEDDED_TODOS_END = "<!-- END CODEXTER_EMBEDDED_TODOS -->"


@dataclass(frozen=True)
class Skill:
    name: str
    path: Path
    description: str
    source: str
    tier: str


@dataclass(frozen=True)
class InstallResult:
    installed: list[str]
    skipped: list[str]
    pruned: list[str]
    backup_root: str
    dry_run: bool


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    data: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip().strip("\"'")
        data[key.strip()] = value
    return data


def discover_skills(skills_dir: Path) -> list[Skill]:
    if not skills_dir.exists():
        raise FileNotFoundError(f"Skills directory does not exist: {skills_dir}")

    skills: list[Skill] = []
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name == ".system":
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        meta = parse_frontmatter(skill_file)
        skills.append(
            Skill(
                name=meta.get("name", skill_dir.name),
                path=skill_dir,
                description=meta.get("description", ""),
                source=meta.get("source", ""),
                tier=meta.get("tier", ""),
            )
        )
    return skills


def filter_skills(skills: Sequence[Skill], query: str | None) -> list[Skill]:
    if not query:
        return list(skills)

    terms = [term.casefold() for term in query.split() if term.strip()]
    if not terms:
        return list(skills)

    matches: list[Skill] = []
    for skill in skills:
        haystack = " ".join(
            [skill.name, skill.description, skill.source, skill.tier]
        ).casefold()
        if all(term in haystack for term in terms):
            matches.append(skill)
    return matches


def parse_skill_names(raw: str | None, repeated: Sequence[str] | None) -> list[str]:
    values: list[str] = []
    if raw:
        values.extend(raw.split(","))
    if repeated:
        for item in repeated:
            values.extend(item.split(","))
    names = [value.strip() for value in values if value.strip()]
    return sorted(dict.fromkeys(names))


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def backup_existing(dest: Path, backup_root: Path, dry_run: bool) -> None:
    relative = dest.relative_to(dest.parents[1])
    backup_dest = backup_root / relative
    if dry_run:
        return
    backup_dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(dest), str(backup_dest))


def render_skill_markdown(
    skill_md: str, todos_md: str | None, source_label: str
) -> str:
    """Return installed SKILL.md text with todos embedded for first-load context."""
    stripped = skill_md.rstrip()
    if not todos_md or not todos_md.strip():
        return stripped + "\n"

    return (
        stripped
        + "\n\n"
        + EMBEDDED_TODOS_BEGIN
        + "\n"
        + "## Embedded Skill Checklist\n\n"
        + "This generated section is copied from the skill package checklist so "
        + "agents see required steps on first skill load.\n\n"
        + f"Source: `{source_label}`\n\n"
        + todos_md.strip()
        + "\n"
        + EMBEDDED_TODOS_END
        + "\n"
    )


def package_files(root: Path) -> dict[Path, Path]:
    return {
        path.relative_to(root): path
        for path in root.rglob("*")
        if path.is_file() or path.is_symlink()
    }


def files_match(source: Path, installed: Path) -> bool:
    if source.is_symlink() or installed.is_symlink():
        return installed.is_symlink() and source.is_symlink() and (
            installed.readlink() == source.readlink()
        )
    return source.read_bytes() == installed.read_bytes()


def rendered_skill_matches(src: Path, dest: Path) -> bool:
    if not dest.is_dir() or dest.is_symlink():
        return False

    source_files = package_files(src)
    installed_files = package_files(dest)
    if set(source_files) != set(installed_files):
        return False

    source_skill = src / "SKILL.md"
    source_todos = src / "todos.md"
    rendered_skill = render_skill_markdown(
        source_skill.read_text(encoding="utf-8"),
        source_todos.read_text(encoding="utf-8") if source_todos.exists() else None,
        f"{src.name}/todos.md",
    )
    installed_skill = dest / "SKILL.md"
    if not installed_skill.exists():
        return False
    if installed_skill.read_text(encoding="utf-8") != rendered_skill:
        return False

    for relative_path, source_path in source_files.items():
        if relative_path == Path("SKILL.md"):
            continue
        if not files_match(source_path, installed_files[relative_path]):
            return False
    return True


def render_skill_package(src: Path, dest: Path, backup_root: Path, dry_run: bool) -> str:
    if rendered_skill_matches(src, dest):
        return "skipped"

    if dest.exists() or dest.is_symlink():
        backup_existing(dest, backup_root, dry_run)

    if dry_run:
        return "installed"

    shutil.copytree(src, dest, symlinks=True)
    skill_file = dest / "SKILL.md"
    todos_file = src / "todos.md"
    rendered = render_skill_markdown(
        (src / "SKILL.md").read_text(encoding="utf-8"),
        todos_file.read_text(encoding="utf-8") if todos_file.exists() else None,
        f"{src.name}/todos.md",
    )
    skill_file.write_text(rendered, encoding="utf-8")
    return "installed"


def install_skills(
    repo: Path,
    target: Path,
    names: Sequence[str],
    prune: bool,
    dry_run: bool,
) -> InstallResult:
    skills = {skill.name: skill for skill in discover_skills(repo / "skills")}
    missing = [name for name in names if name not in skills]
    if missing:
        known = ", ".join(sorted(skills))
        raise ValueError(f"Unknown skill(s): {', '.join(missing)}\nKnown skills: {known}")

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_root = target / ".install-backups" / stamp
    skills_target = target / "skills"
    selected = set(names)
    installed: list[str] = []
    skipped: list[str] = []
    pruned: list[str] = []

    for name in names:
        result = render_skill_package(
            skills[name].path, skills_target / name, backup_root, dry_run
        )
        if result == "installed":
            installed.append(name)
        else:
            skipped.append(name)

    if prune and skills_target.exists():
        repo_skills = repo / "skills"
        for dest in sorted(skills_target.iterdir()):
            if dest.name in selected:
                continue
            if dest.is_symlink():
                try:
                    resolved = dest.resolve(strict=True)
                except FileNotFoundError:
                    continue
                if not is_relative_to(resolved, repo_skills):
                    continue
                backup_existing(dest, backup_root, dry_run)
                pruned.append(dest.name)
                continue

            skill = skills.get(dest.name)
            if skill and rendered_skill_matches(skill.path, dest):
                backup_existing(dest, backup_root, dry_run)
                pruned.append(dest.name)

    return InstallResult(
        installed=installed,
        skipped=skipped,
        pruned=pruned,
        backup_root=str(backup_root),
        dry_run=dry_run,
    )


def skill_row(skill: Skill) -> dict[str, str]:
    return {
        "name": skill.name,
        "description": skill.description,
        "source": skill.source,
        "tier": skill.tier,
        "path": str(skill.path),
    }


def render_table(skills: Sequence[Skill]) -> str:
    if not skills:
        return "No matching skills."

    lines = [f"{'NAME':28} {'TIER':6} {'SOURCE':9} DESCRIPTION"]
    for skill in skills:
        description = skill.description.replace("\n", " ")
        if len(description) > 92:
            description = description[:89].rstrip() + "..."
        lines.append(
            f"{skill.name:28} {skill.tier[:6]:6} {skill.source[:9]:9} {description}"
        )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Search and install selected Codexter skills."
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Codexter repo root. Defaults to this script's repo.",
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=Path.home() / ".codex",
        help="Codex home to install into. Defaults to ~/.codex.",
    )
    parser.add_argument("--list", action="store_true", help="List available skills.")
    parser.add_argument("--search", help="Search skill names and descriptions.")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Install every discoverable skill from the repo.",
    )
    parser.add_argument("--skills", help="Comma-separated skill names to install.")
    parser.add_argument(
        "--skill",
        action="append",
        help="Skill name to install. Can be repeated or comma-separated.",
    )
    parser.add_argument(
        "--prune",
        action="store_true",
        help="Remove unselected symlinks that point into this repo's skills directory.",
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
    repo = args.repo.resolve()
    target = args.target.expanduser().resolve()
    names = parse_skill_names(args.skills, args.skill)

    if args.list or args.search:
        try:
            matches = filter_skills(discover_skills(repo / "skills"), args.search)
        except FileNotFoundError as exc:
            raise SystemExit(str(exc)) from exc
        if args.json:
            print(json.dumps([skill_row(skill) for skill in matches], indent=2))
        else:
            print(render_table(matches))
        return 0

    if args.all:
        try:
            names = [skill.name for skill in discover_skills(repo / "skills")]
        except FileNotFoundError as exc:
            raise SystemExit(str(exc)) from exc

    if not names:
        raise SystemExit("No skills selected. Use --list, --search, or --skills name1,name2.")

    try:
        result = install_skills(repo, target, names, args.prune, args.dry_run)
    except (FileNotFoundError, ValueError) as exc:
        raise SystemExit(str(exc)) from exc
    if args.json:
        print(json.dumps(asdict(result), indent=2))
    else:
        prefix = "dry-run " if result.dry_run else ""
        print(f"{prefix}installed: {', '.join(result.installed) or 'none'}")
        print(f"{prefix}already linked: {', '.join(result.skipped) or 'none'}")
        print(f"{prefix}pruned: {', '.join(result.pruned) or 'none'}")
        print(f"backups: {result.backup_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
