#!/usr/bin/env python3
"""Print an advisory minimization worksheet for a Farplane skill surface."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bin.validators.check_skill_surface_budget import (  # noqa: E402
    DEFAULT_TEMPLATE_ID,
    count_skill_surfaces,
    parse_frontmatter,
    template_uses,
)


TODO_RE = re.compile(
    r"<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->\n## Todo List\n\n(.*?)\n<!-- END FARPLANE_IMPORTANT_CHECKLIST -->",
    re.DOTALL,
)
TOP_LEVEL_TODO_RE = re.compile(r"^- \[ \] \d+\. ")


def skill_dir_from_arg(value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = ROOT / path
    if path.name == "SKILL.md":
        path = path.parent
    if not (path / "SKILL.md").exists():
        raise SystemExit(f"{value}: expected a skill directory or SKILL.md")
    return path


def todo_units(skill_dir: Path) -> list[str]:
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    match = TODO_RE.search(text)
    if not match:
        return []
    return [line for line in match.group(1).splitlines() if TOP_LEVEL_TODO_RE.match(line)]


def eval_units(skill_dir: Path) -> list[str]:
    path = skill_dir / "evals/evals.json"
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload if isinstance(payload, list) else []
    if isinstance(payload, dict):
        for key in ("tasks", "tests", "cases", "evals"):
            value = payload.get(key)
            if isinstance(value, list):
                rows = value
                break
    units: list[str] = []
    for index, row in enumerate(rows, start=1):
        if isinstance(row, dict):
            label = row.get("id") or row.get("title") or f"eval-{index}"
        else:
            label = f"eval-{index}"
        units.append(str(label))
    return units


def build_minimizer_report(skill_dir: Path, surface: str, limit: int) -> str:
    metadata = parse_frontmatter(skill_dir / "SKILL.md")
    enrolled = DEFAULT_TEMPLATE_ID in template_uses(metadata)
    counts = count_skill_surfaces(skill_dir)
    surface_map = {
        "todos": ("skill_todos", counts.skill_todos, todo_units(skill_dir)),
        "eval": ("eval_tasks", counts.eval_tasks, eval_units(skill_dir)),
    }
    if surface not in surface_map:
        raise SystemExit("--surface must be one of: todos, eval")

    label, count, units = surface_map[surface]
    overflow = max(0, count - limit)
    keep = units[:limit]
    candidates = units[limit:]
    lines = [
        f"# Skill Surface Minimizer: {skill_dir.relative_to(ROOT)}",
        "",
        f"- enrolled: {'yes' if enrolled else 'no'}",
        f"- surface: {label}",
        f"- current_count: {count}",
        f"- limit: {limit}",
        f"- overflow: {overflow}",
        "",
        "## Keep",
    ]
    lines.extend(f"- {unit}" for unit in keep)
    lines.extend(["", "## Combine / Move / Delete Candidates"])
    if candidates:
        lines.extend(f"- {unit}" for unit in candidates)
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Consolidation Guidance",
            "- `keep`: highest execution, proof, routing, reuse, memory, or user value.",
            "- `merge`: overlapping units that prevent the same failure mode.",
            "- `move`: rare examples, branch-specific detail, or long rationale that belongs in references.",
            "- `delete`: duplicated, stale, or todo-restating units with no distinct guardrail value.",
            "",
            "## Handoff",
            "Run `skill-maintenance.refine_skill` with `consolidate(target = edited_skill, structure = skill)` before enrolling over-budget skills.",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill", help="skill directory or SKILL.md path")
    parser.add_argument("--surface", choices=["todos", "eval"], required=True)
    parser.add_argument("--limit", type=int, required=True)
    args = parser.parse_args()

    print(build_minimizer_report(skill_dir_from_arg(args.skill), args.surface, args.limit))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
