#!/usr/bin/env python3
"""Check opt-in Farplane skill surface budgets."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bin.core.lint.source import MarkdownFrontmatterError, parse_markdown_frontmatter

TODO_RE = re.compile(
    r"<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->\n## Todo List\n\n(.*?)\n<!-- END FARPLANE_IMPORTANT_CHECKLIST -->",
    re.DOTALL,
)
TOP_LEVEL_TODO_RE = re.compile(r"^(?:\d+\. |- \[ \] \d+\. )")
DEFAULT_TEMPLATE_ID = "skill-surface-budget"
DEFAULT_VERSION = "0.1.0"


@dataclass(frozen=True)
class SurfaceLimits:
    skill_todos: int = 10
    eval_tasks: int = 5


@dataclass(frozen=True)
class SurfaceCounts:
    skill_todos: int
    eval_tasks: int


@dataclass(frozen=True)
class BudgetViolation:
    skill: str
    surface: str
    path: Path
    count: int
    limit: int


@dataclass(frozen=True)
class BudgetResult:
    checked: int
    skipped: int
    violations: list[BudgetViolation]


def parse_frontmatter(path: Path) -> dict[str, Any]:
    try:
        metadata = parse_markdown_frontmatter(path)
    except (MarkdownFrontmatterError, OSError, UnicodeDecodeError):
        return {}
    return metadata or {}


def template_uses(metadata: dict[str, Any]) -> dict[str, str]:
    raw = metadata.get("template_uses")
    if isinstance(raw, dict):
        return {str(key): str(value) for key, value in raw.items()}
    return {}


def count_skill_todos(skill_path: Path) -> int:
    text = skill_path.read_text(encoding="utf-8")
    match = TODO_RE.search(text)
    if not match:
        return 0
    return sum(1 for line in match.group(1).splitlines() if TOP_LEVEL_TODO_RE.match(line))


def count_eval_tasks(path: Path) -> int:
    if not path.exists():
        return 0
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return len(payload)
    if isinstance(payload, dict):
        for key in ("tasks", "tests", "cases", "evals"):
            value = payload.get(key)
            if isinstance(value, list):
                return len(value)
    return 0


def count_skill_surfaces(skill_dir: Path) -> SurfaceCounts:
    return SurfaceCounts(
        skill_todos=count_skill_todos(skill_dir / "SKILL.md"),
        eval_tasks=count_eval_tasks(skill_dir / "evals/evals.json"),
    )


def collect_budget_results(
    repo_root: Path,
    *,
    template_id: str = DEFAULT_TEMPLATE_ID,
    template_version: str | None = DEFAULT_VERSION,
    limits: SurfaceLimits = SurfaceLimits(),
) -> BudgetResult:
    checked = 0
    skipped = 0
    violations: list[BudgetViolation] = []
    for skill_dir in sorted((repo_root / "skills").glob("*/")):
        skill_path = skill_dir / "SKILL.md"
        if not skill_path.exists():
            continue
        metadata = parse_frontmatter(skill_path)
        uses = template_uses(metadata)
        used_version = uses.get(template_id)
        if used_version is None:
            skipped += 1
            continue
        checked += 1
        if template_version is not None and used_version != template_version:
            violations.append(
                BudgetViolation(skill_dir.name, template_id, skill_path, 0, 0)
            )
            continue
        counts = count_skill_surfaces(skill_dir)
        surfaces = [
            ("skill_todos", skill_path, counts.skill_todos, limits.skill_todos),
            ("eval_tasks", skill_dir / "evals/evals.json", counts.eval_tasks, limits.eval_tasks),
        ]
        for surface, path, count, limit in surfaces:
            if count > limit:
                violations.append(BudgetViolation(skill_dir.name, surface, path, count, limit))
    return BudgetResult(checked=checked, skipped=skipped, violations=violations)


def minimizer_command(violation: BudgetViolation) -> str:
    surface_arg = {
        "skill_todos": "todos",
        "eval_tasks": "eval",
    }.get(violation.surface, violation.surface)
    return (
        "python3 skills/skill-maintenance/scripts/minimize_skill_surface.py "
        f"skills/{violation.skill} --surface {surface_arg} --limit {violation.limit}"
    )


def format_violation(violation: BudgetViolation, repo_root: Path) -> str:
    path = violation.path.relative_to(repo_root) if violation.path.is_absolute() else violation.path
    if violation.surface == DEFAULT_TEMPLATE_ID:
        return f"skills/{violation.skill}/SKILL.md: {DEFAULT_TEMPLATE_ID} version is not current"
    return (
        f"{path}: {violation.skill} {violation.surface} has {violation.count} items; "
        f"limit is {violation.limit}\n  Run: {minimizer_command(violation)}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument("--template-id", default=DEFAULT_TEMPLATE_ID)
    parser.add_argument("--template-version", default=DEFAULT_VERSION)
    parser.add_argument("--skill-todos-limit", type=int, default=10)
    parser.add_argument("--eval-tasks-limit", type=int, default=5)
    args = parser.parse_args()

    repo_root = Path(args.root).resolve()
    result = collect_budget_results(
        repo_root,
        template_id=args.template_id,
        template_version=args.template_version,
        limits=SurfaceLimits(
            skill_todos=args.skill_todos_limit,
            eval_tasks=args.eval_tasks_limit,
        ),
    )
    print(
        "skill surface budget: "
        f"checked={result.checked} skipped={result.skipped} failed={len(result.violations)}"
    )
    if result.violations:
        for violation in result.violations:
            print(format_violation(violation, repo_root), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
