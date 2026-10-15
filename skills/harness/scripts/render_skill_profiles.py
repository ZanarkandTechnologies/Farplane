#!/usr/bin/env python3
"""Render the default skill config and one launch profile per Capability Map desk.

A desk profile keeps the desk's own skills and every helper (a skill at no desk)
and turns off the other desks' skills, so a desk session routes among a short
list. Codex reads `profiles/<desk>.config.toml` through `codex -p <desk>`;
Claude reads `claude/<desk>.settings.json` through `claude --settings`.
`farplane desk` launches either one.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT / "bin" / "core") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "bin" / "core"))

from skill_departments import (  # noqa: E402
    CapabilityAdmissionConfigError,
    DepartmentTaxonomyError,
    desk_identity,
    load_skill_specialists,
)

PROFILE_MARKER_BEGIN = "# BEGIN FARPLANE GENERATED SKILL PROFILE"
PROFILE_MARKER_END = "# END FARPLANE GENERATED SKILL PROFILE"


class ProfileRenderError(ValueError):
    """Raised when the desk table cannot produce a safe config."""


def registry_skill_names(repo: Path) -> set[str]:
    registry_path = repo / "skills" / "registry.jsonl"
    try:
        rows = [json.loads(line) for line in registry_path.read_text(encoding="utf-8").splitlines() if line]
    except (OSError, json.JSONDecodeError) as exc:
        raise ProfileRenderError(f"invalid_skill_registry:{registry_path}") from exc
    names = {row.get("name") for row in rows if isinstance(row, dict) and isinstance(row.get("name"), str)}
    if not names:
        raise ProfileRenderError(f"empty_skill_registry:{registry_path}")
    return names


def load_desks(repo: Path, known_skills: set[str]) -> dict[str, dict[str, object]]:
    try:
        desks = load_skill_specialists(repo)
    except (CapabilityAdmissionConfigError, DepartmentTaxonomyError) as exc:
        raise ProfileRenderError(f"invalid_desk_table:{exc}") from exc
    for desk_id, desk in desks.items():
        missing = sorted(set(desk["skills"]).difference(known_skills))
        if missing:
            raise ProfileRenderError(f"desk_skills_missing_from_registry:{desk_id}:{','.join(missing)}")
    return dict(sorted(desks.items()))


def render_matrix(skill_names: tuple[str, ...], enabled_skills: tuple[str, ...], identity: str = "") -> str:
    enabled = set(enabled_skills)
    lines = [PROFILE_MARKER_BEGIN]
    if identity:
        lines.extend((f"developer_instructions = {json.dumps(identity)}", ""))
    for skill_name in skill_names:
        lines.extend(("[[skills.config]]", f'name = "{skill_name}"', f"enabled = {'true' if skill_name in enabled else 'false'}", ""))
    lines.append(PROFILE_MARKER_END)
    return "\n".join(lines) + "\n"


def render_profiles(repo: Path, output_dir: Path) -> dict[str, object]:
    resolved_repo = repo.resolve()
    known_skills = registry_skill_names(resolved_repo)
    desks = load_desks(resolved_repo, known_skills)
    managed_skills = tuple(sorted({skill for desk in desks.values() for skill in desk["skills"]}))
    base_skills = tuple(sorted(known_skills))
    codex_dir = output_dir / "profiles"
    claude_dir = output_dir / "claude"
    codex_dir.mkdir(parents=True, exist_ok=True)
    claude_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "base.config.toml").write_text(render_matrix(base_skills, base_skills), encoding="utf-8")
    profiles: dict[str, list[str]] = {}
    for desk_id, desk in desks.items():
        own = tuple(sorted(desk["skills"]))
        (codex_dir / f"{desk_id}.config.toml").write_text(render_matrix(managed_skills, own, desk_identity(desk_id, desk)), encoding="utf-8")
        hidden = {skill: "off" for skill in managed_skills if skill not in own}
        (claude_dir / f"{desk_id}.settings.json").write_text(
            json.dumps({"skillOverrides": hidden}, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        profiles[desk_id] = list(own)
    return {
        "managed_skill_count": len(managed_skills),
        "profile_count": len(profiles),
        "profiles": profiles,
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
        print(f"Rendered {result['profile_count']} desk profiles across {result['managed_skill_count']} desk skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
