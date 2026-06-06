#!/usr/bin/env python3
"""Check that skill first-load todo lists link only to allowed tier dependencies."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path


SYNC_SCRIPT = Path(__file__).with_name("sync_skill_registry.py")
SYNC_SPEC = importlib.util.spec_from_file_location("sync_skill_registry", SYNC_SCRIPT)
if SYNC_SPEC is None or SYNC_SPEC.loader is None:
    raise RuntimeError(f"failed to load {SYNC_SCRIPT}")
sync_skill_registry = importlib.util.module_from_spec(SYNC_SPEC)
SYNC_SPEC.loader.exec_module(sync_skill_registry)


@dataclass(frozen=True)
class ChecklistTierViolation:
    path: Path
    line: int
    source: str
    source_tier: int
    target: str
    target_tier: int | None
    reason: str


def iter_text_skill_links(text: str, source_name: str) -> list[tuple[int, str]]:
    links: list[tuple[int, str]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for match in sync_skill_registry.SKILL_LINK_RE.finditer(line):
            target, anchor = match.groups()
            if target in {".", source_name}:
                continue
            links.append((line_number, f"{target}#{anchor}" if anchor else target))
        for match in sync_skill_registry.LOCAL_METHOD_RE.finditer(line):
            local_ref = f"{source_name}#{match.group(1)}"
            links.append((line_number, local_ref))
    return links


def load_skill_tiers(repo_root: Path) -> dict[str, int]:
    tiers: dict[str, int] = {}
    for skill_path in sorted((repo_root / "skills").glob("*/SKILL.md")):
        metadata = sync_skill_registry.parse_frontmatter(skill_path)
        name = metadata.get("name")
        tier = metadata.get("tier")
        if name != skill_path.parent.name:
            raise sync_skill_registry.RegistryError(
                f"{skill_path}: name must match directory {skill_path.parent.name!r}"
            )
        if tier not in (1, 2, 3):
            raise sync_skill_registry.RegistryError(f"{skill_path}: tier must be 1, 2, or 3")
        tiers[name] = tier
    return tiers


def checklist_text_and_start(skill_dir: Path) -> tuple[str, Path, int]:
    skill_path = skill_dir / "SKILL.md"
    skill_text = skill_path.read_text()
    match = sync_skill_registry.CHECKLIST_RE.search(skill_text)
    if match:
        return match.group(1).strip(), skill_path, skill_text[: match.start(1)].count("\n") + 1

    todos_path = skill_dir / "todos.md"
    if todos_path.exists():
        return sync_skill_registry.checklist_source_text(skill_dir), todos_path, 1

    return "", skill_path, 1


def collect_violations(repo_root: Path, allow_peer_tier3: bool) -> list[ChecklistTierViolation]:
    tiers = load_skill_tiers(repo_root)
    violations: list[ChecklistTierViolation] = []

    for source, source_tier in sorted(tiers.items()):
        skill_dir = repo_root / "skills" / source
        checklist, source_path, line_offset = checklist_text_and_start(skill_dir)
        if not checklist:
            continue

        for line_number, ref in iter_text_skill_links(checklist, source):
            actual_line = line_offset + line_number - 1
            target = sync_skill_registry.skill_ref_name(ref)
            if target == source:
                continue

            target_tier = tiers.get(target)
            if target_tier is None:
                violations.append(
                    ChecklistTierViolation(
                        path=source_path,
                        line=actual_line,
                        source=source,
                        source_tier=source_tier,
                        target=ref,
                        target_tier=None,
                        reason="unknown skill target",
                    )
                )
                continue

            expected_tier = source_tier - 1
            if target_tier == expected_tier:
                continue
            if allow_peer_tier3 and source_tier == 3 and target_tier == 3:
                continue

            violations.append(
                ChecklistTierViolation(
                    path=source_path,
                    line=actual_line,
                    source=source,
                    source_tier=source_tier,
                    target=ref,
                    target_tier=target_tier,
                    reason=f"expected tier {expected_tier}",
                )
            )

    return violations


def format_violation(violation: ChecklistTierViolation, repo_root: Path) -> str:
    target_tier = "unknown" if violation.target_tier is None else str(violation.target_tier)
    path = violation.path.relative_to(repo_root)
    return (
        f"{path}:{violation.line}: {violation.source} tier {violation.source_tier} -> "
        f"{violation.target} tier {target_tier} ({violation.reason})"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--allow-peer-tier3",
        action="store_true",
        help="allow Tier 3 todo lists to link peer Tier 3 execution handoffs",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    try:
        violations = collect_violations(repo_root, allow_peer_tier3=args.allow_peer_tier3)
    except sync_skill_registry.RegistryError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if violations:
        for violation in violations:
            print(format_violation(violation, repo_root), file=sys.stderr)
        print(f"skill todo tier check failed ({len(violations)} violation(s))", file=sys.stderr)
        return 1

    print("skill todo tier check OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
