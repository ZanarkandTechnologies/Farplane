#!/usr/bin/env python3
"""Render checked-in role skill selections as Codex profile config files."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path


PROFILE_MARKER_BEGIN = "# BEGIN FARPLANE GENERATED SKILL PROFILE"
PROFILE_MARKER_END = "# END FARPLANE GENERATED SKILL PROFILE"
PROFILE_NAME_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


class ProfileRenderError(ValueError):
    """Raised when the source profile contract cannot produce a safe config."""


def registry_skill_names(repo: Path) -> set[str]:
    registry_path = repo / "docs" / "skills" / "registry.jsonl"
    try:
        rows = [json.loads(line) for line in registry_path.read_text(encoding="utf-8").splitlines() if line]
    except (OSError, json.JSONDecodeError) as exc:
        raise ProfileRenderError(f"invalid_skill_registry:{registry_path}") from exc
    names = {row.get("name") for row in rows if isinstance(row, dict) and isinstance(row.get("name"), str)}
    if not names:
        raise ProfileRenderError(f"empty_skill_registry:{registry_path}")
    return names


def load_profile_map(repo: Path, known_skills: set[str]) -> dict[str, tuple[str, ...]]:
    manifest_path = repo / "rules" / "skill-profiles.toml"
    try:
        payload = tomllib.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ProfileRenderError(f"invalid_profile_manifest:{manifest_path}") from exc
    raw_profiles = payload.get("profiles")
    if not isinstance(raw_profiles, dict) or not raw_profiles:
        raise ProfileRenderError(f"invalid_profile_manifest:{manifest_path}:profiles must be a non-empty table")

    profiles: dict[str, tuple[str, ...]] = {}
    for raw_name, raw_skills in raw_profiles.items():
        if not isinstance(raw_name, str) or not PROFILE_NAME_RE.fullmatch(raw_name):
            raise ProfileRenderError(f"invalid_profile_name:{raw_name!r}")
        if not isinstance(raw_skills, list) or not raw_skills:
            raise ProfileRenderError(f"invalid_profile_skills:{raw_name}:must be a non-empty list")
        if not all(isinstance(skill, str) and skill for skill in raw_skills):
            raise ProfileRenderError(f"invalid_profile_skills:{raw_name}:values must be non-empty strings")
        skills = tuple(sorted(raw_skills))
        duplicates = sorted({skill for skill in skills if skills.count(skill) > 1})
        if duplicates:
            raise ProfileRenderError(f"duplicate_profile_skills:{raw_name}:{','.join(duplicates)}")
        missing = sorted(set(skills).difference(known_skills))
        if missing:
            raise ProfileRenderError(f"profile_skills_missing_from_registry:{raw_name}:{','.join(missing)}")
        profiles[raw_name] = skills
    return dict(sorted(profiles.items()))


def render_matrix(skill_names: tuple[str, ...], enabled_skills: tuple[str, ...]) -> str:
    enabled = set(enabled_skills)
    lines = [PROFILE_MARKER_BEGIN]
    for skill_name in skill_names:
        lines.extend(("[[skills.config]]", f'name = "{skill_name}"', f"enabled = {'true' if skill_name in enabled else 'false'}", ""))
    lines.append(PROFILE_MARKER_END)
    return "\n".join(lines) + "\n"


def render_profiles(repo: Path, output_dir: Path) -> dict[str, object]:
    resolved_repo = repo.resolve()
    profiles = load_profile_map(resolved_repo, registry_skill_names(resolved_repo))
    managed_skills = tuple(sorted({skill for skills in profiles.values() for skill in skills}))
    profile_dir = output_dir / "profiles"
    profile_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "base.config.toml").write_text(
        render_matrix(managed_skills, ()), encoding="utf-8"
    )
    for profile_name, enabled_skills in profiles.items():
        (profile_dir / f"{profile_name}.config.toml").write_text(
            render_matrix(managed_skills, enabled_skills), encoding="utf-8"
        )
    return {
        "managed_skill_count": len(managed_skills),
        "profile_count": len(profiles),
        "profiles": {name: list(skills) for name, skills in profiles.items()},
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = render_profiles(args.repo, args.output_dir)
    except ProfileRenderError as exc:
        print(f"skill profile render failed: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        print(f"Rendered {result['profile_count']} skill profiles across {result['managed_skill_count']} managed skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
