#!/usr/bin/env python3
"""Run the standard Farplane skill-system checks."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "bin/validators/sync_skill_registry.py").exists() and (candidate / "skills").exists():
            return candidate
    raise RuntimeError("could not find Farplane repo root")


REPO_ROOT = find_repo_root(Path(__file__).resolve())
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from bin.validators.template_usage import template_target_basis
from bin.core.lint.source import MarkdownFrontmatterError, parse_markdown_frontmatter

REQUIRED_TEMPLATE_HEADINGS = ("Context", "Skill Signature", "Todo List", "Gotchas", "Output")
REQUIRED_METHOD_REFERENCE_HEADINGS = ("Use When", "Inputs", "Workflow", "Output Shape", "Quality Gates", "Bad Output")
CURRENT_METHOD_REFERENCE_VERSION = "0.1.0"
HEADING_RE = re.compile(r"^## (?P<heading>.+?)\s*$")
TOP_LEVEL_NUMBERED_TODO_RE = re.compile(r"^\d+\. ")
MARKDOWN_TASK_TODO_RE = re.compile(r"^\s*- \[ \] ")
ORDERED_CHECKBOX_TODO_RE = re.compile(r"^\s*\d+\. \[ \] ")
TIP_LIKE_TOP_LEVEL_TODO_RE = re.compile(r"^\d+\. (?:Use .+ when\b|Keep\b|Do not\b|Avoid\b)")
UNORDERED_PROSE_TODO_RE = re.compile(r"^\s+- ")
GOLDEN_NODE_RE = re.compile(r"^- \[ \] \*\*N(?P<id>\d+) — .+\*\*\s*$", re.MULTILINE)
NODE_SIGNATURE_RE = re.compile(r"^\s{2}`[^`]+ -> [^`]+`\s*$", re.MULTILINE)


def run(command: list[str]) -> None:
    print("+ " + " ".join(command))
    subprocess.run(command, cwd=REPO_ROOT, check=True)


def registry_summary() -> dict[str, object]:
    rows = [
        json.loads(line)
        for line in (REPO_ROOT / "docs/skills/registry.jsonl").read_text().splitlines()
        if line.strip()
    ]
    return {
        "rows": len(rows),
        "tiers": dict(sorted(Counter(row["tier"] for row in rows).items())),
        "sources": dict(sorted(Counter(row["source"] for row in rows).items())),
        "checklists": dict(
            sorted(
                Counter("has" if row.get("has_checklist") else "missing" for row in rows).items()
            )
        ),
        "skill_template_versions": dict(
            sorted(Counter(str(row.get("skill_template_version") or "missing") for row in rows).items())
        ),
        "template_uses": dict(
            sorted(
                Counter(
                    template_id
                    for row in rows
                    for template_id in (row.get("template_uses") or {}).keys()
                ).items()
            )
        ),
        "missing_skill_template_version": [
            {
                "name": row["name"],
                "tier": row["tier"],
                "source": row["source"],
            }
            for row in rows
            if not row.get("skill_template_version")
        ],
        "missing_checklists": [
            {
                "name": row["name"],
                "tier": row["tier"],
                "source": row["source"],
                "upstream_url": row.get("upstream_url"),
            }
            for row in rows
            if not row.get("has_checklist")
        ],
    }


def iter_markdown_headings(text: str) -> list[tuple[int, str]]:
    headings: list[tuple[int, str]] = []
    in_fence = False
    for line_number, line in enumerate(text.splitlines(), start=1):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING_RE.match(line)
        if match:
            headings.append((line_number, match.group("heading")))
    return headings


def markdown_section(text: str, heading: str) -> str | None:
    lines = text.splitlines()
    in_fence = False
    start: int | None = None
    for index, line in enumerate(lines):
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING_RE.match(line)
        if not match:
            continue
        if start is None:
            if match.group("heading") == heading:
                start = index + 1
            continue
        return "\n".join(lines[start:index])
    if start is None:
        return None
    return "\n".join(lines[start:])


def marker_counts(text: str) -> tuple[int, int, int]:
    real_markers = 0
    fenced_markers = 0
    in_fence = False
    for line in text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if "<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->" not in line:
            continue
        if in_fence:
            fenced_markers += 1
        else:
            real_markers += 1
    return real_markers, fenced_markers, text.count("<!-- END FARPLANE_IMPORTANT_CHECKLIST -->")


def template_structure_errors(current_version: str) -> list[str]:
    rows = [
        json.loads(line)
        for line in (REPO_ROOT / "docs/skills/registry.jsonl").read_text().splitlines()
        if line.strip()
    ]
    errors: list[str] = []
    for row in rows:
        if row.get("skill_template_version") != current_version:
            continue
        path = Path(str(row["path"]))
        skill_path = REPO_ROOT / path
        if not skill_path.exists():
            errors.append(f"{row['name']}: missing skill file at {path}")
            continue

        text = skill_path.read_text(encoding="utf-8")
        real_begin_count, fenced_begin_count, end_count = marker_counts(text)
        if real_begin_count != 1:
            errors.append(f"{row['name']}: expected exactly one real todo-list marker section")
        if fenced_begin_count:
            errors.append(f"{row['name']}: do not put todo-list marker comments inside fenced examples")
        if end_count != real_begin_count + fenced_begin_count:
            errors.append(f"{row['name']}: mismatched todo-list marker comments")

        headings = iter_markdown_headings(text)
        heading_names = [heading for _, heading in headings]
        heading_lines = {heading: line_number for line_number, heading in headings}

        for required_heading in REQUIRED_TEMPLATE_HEADINGS:
            if required_heading not in heading_names:
                errors.append(f"{row['name']}: missing ## {required_heading}")

        if "Job" in heading_names:
            errors.append(f"{row['name']}: remove generic ## Job; fold work into Context/Todo List")

        if "Context" in heading_lines and "Todo List" in heading_lines:
            if heading_lines["Context"] > heading_lines["Todo List"]:
                errors.append(f"{row['name']}: ## Context must appear before ## Todo List")

        todo_body = markdown_section(text, "Todo List")
        if todo_body is None:
            continue
        if current_version == "0.5.0":
            node_matches = list(GOLDEN_NODE_RE.finditer(todo_body))
            if not node_matches:
                errors.append(
                    f"{row['name']}: ## Todo List needs Golden Workflow Nodes like "
                    "`- [ ] **N1 — Produce the outcome.**`"
                )
                continue
            node_ids = [int(match.group("id")) for match in node_matches]
            if node_ids != list(range(1, len(node_ids) + 1)):
                errors.append(f"{row['name']}: Golden Workflow Node IDs must be sequential from N1")
            for index, match in enumerate(node_matches):
                end = node_matches[index + 1].start() if index + 1 < len(node_matches) else len(todo_body)
                node_body = todo_body[match.end():end]
                node_id = match.group("id")
                if not NODE_SIGNATURE_RE.search(node_body):
                    errors.append(f"{row['name']}: N{node_id} needs an inline `input -> output | branch` signature")
                if not re.search(r"^\s{2}Rule: \S", node_body, re.MULTILINE):
                    errors.append(f"{row['name']}: N{node_id} needs a non-empty Rule")
                if not re.search(r"^\s{2}Assert:\s*$", node_body, re.MULTILINE):
                    errors.append(f"{row['name']}: N{node_id} needs an Assert block")
            continue

        if not any(TOP_LEVEL_NUMBERED_TODO_RE.match(line) for line in todo_body.splitlines()):
            errors.append(f"{row['name']}: ## Todo List needs plain numbered items like `1. ...`")
        for line_number, line in enumerate(todo_body.splitlines(), start=1):
            if ORDERED_CHECKBOX_TODO_RE.match(line):
                errors.append(
                    f"{row['name']}: ordered checkbox in ## Todo List line {line_number}; "
                    "use a plain numbered item like `1. ...`"
                )
                break
            if TIP_LIKE_TOP_LEVEL_TODO_RE.match(line):
                errors.append(
                    f"{row['name']}: tip-like top-level todo in ## Todo List line {line_number}; "
                    "make the item an action with an observable result or move the tip to Gotchas/Core Rules"
                )
                break
            if MARKDOWN_TASK_TODO_RE.match(line):
                errors.append(
                    f"{row['name']}: Markdown task item in ## Todo List line {line_number}; "
                    "use plain numbered items and indented Expected/Assert lines"
                )
                break
            if UNORDERED_PROSE_TODO_RE.match(line):
                errors.append(
                    f"{row['name']}: unordered prose bullet in ## Todo List line {line_number}; "
                    "use numbered branch items or indented Expected/Assert lines"
                )
                break

    return errors


def validate_template_version(current_version: str, require: bool) -> int:
    rows = [
        json.loads(line)
        for line in (REPO_ROOT / "docs/skills/registry.jsonl").read_text().splitlines()
        if line.strip()
    ]
    missing = [
        row
        for row in rows
        if not row.get("skill_template_version")
    ]
    not_current = [
        row
        for row in rows
        if row.get("skill_template_version") and row.get("skill_template_version") != current_version
    ]

    report = {
        "current_skill_template_version": current_version,
        "missing": [row["name"] for row in missing],
        "not_current": [
            {
                "name": row["name"],
                "skill_template_version": row.get("skill_template_version"),
            }
            for row in not_current
        ],
    }
    print("skill template version report:")
    print(json.dumps(report, indent=2, sort_keys=True))

    structure_errors = template_structure_errors(current_version)
    if structure_errors:
        print("skill template structure errors:")
        for error in structure_errors:
            print(f"- {error}")
        return 1

    if require and (missing or not_current):
        return 1
    return 0


def parse_simple_frontmatter(path: Path) -> dict[str, object]:
    """Read method-reference metadata through the shared static parser."""

    try:
        return parse_markdown_frontmatter(path) or {}
    except (MarkdownFrontmatterError, OSError, UnicodeDecodeError):
        return {}


def method_reference_structure_errors(current_version: str) -> list[str]:
    errors: list[str] = []
    for path in sorted((REPO_ROOT / "skills").glob("*/references/*.md")):
        text = path.read_text(encoding="utf-8")
        metadata = parse_simple_frontmatter(path)
        template_uses = metadata.get("template_uses")
        if not isinstance(template_uses, dict):
            continue
        used_version = template_uses.get("skill-method-reference")
        if used_version is None:
            continue
        label = str(path.relative_to(REPO_ROOT))
        if used_version != current_version:
            errors.append(
                f"{label}: skill-method-reference version {used_version!r} is not current {current_version!r}"
            )
        headings = [heading for _, heading in iter_markdown_headings(text)]
        for required_heading in REQUIRED_METHOD_REFERENCE_HEADINGS:
            if required_heading not in headings:
                errors.append(f"{label}: missing ## {required_heading}")
    return errors


def method_reference_template_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in sorted((REPO_ROOT / "skills").glob("*/references/*.md")):
        metadata = parse_simple_frontmatter(path)
        template_uses = metadata.get("template_uses")
        if not isinstance(template_uses, dict):
            continue
        used_version = template_uses.get("skill-method-reference")
        if used_version is None:
            continue
        rows.append(
            {
                "name": str(path.relative_to(REPO_ROOT)),
                "template_uses": {"skill-method-reference": used_version},
            }
        )
    return rows


def skill_template_target_rows(rows: list[dict[str, object]], template_id: str) -> list[dict[str, object]]:
    if template_id == "skill-method-reference":
        return method_reference_template_rows()
    if template_id == "skill-template":
        return [
            row
            for row in rows
            if (row.get("template_uses") or {}).get("skill-template") or row.get("skill_template_version")
        ]
    if template_id == "skill-eval-task":
        return [row for row in rows if row.get("eval")]
    if template_id == "skill-qa-checklist":
        return [row for row in rows if row.get("qa_checklist")]
    return [row for row in rows if template_id in (row.get("template_uses") or {})]


def validate_skill_template_rollout(template_id: str, current_version: str, require: bool) -> int:
    rows = [
        json.loads(line)
        for line in (REPO_ROOT / "docs/skills/registry.jsonl").read_text().splitlines()
        if line.strip()
    ]
    targets = skill_template_target_rows(rows, template_id)
    missing = [
        row
        for row in targets
        if not (row.get("template_uses") or {}).get(template_id)
    ]
    not_current = [
        row
        for row in targets
        if (row.get("template_uses") or {}).get(template_id)
        and (row.get("template_uses") or {}).get(template_id) != current_version
    ]

    report = {
        "template_id": template_id,
        "current_version": current_version,
        "target_basis": template_target_basis(template_id),
        "target_count": len(targets),
        "current_count": len(targets) - len(missing) - len(not_current),
        "missing": [row["name"] for row in missing],
        "not_current": [
            {
                "name": row["name"],
                "used_version": (row.get("template_uses") or {}).get(template_id),
            }
            for row in not_current
        ],
    }
    print("skill template rollout report:")
    print(json.dumps(report, indent=2, sort_keys=True))

    if template_id == "skill-template":
        structure_errors = template_structure_errors(current_version)
        if structure_errors:
            print("skill template structure errors:")
            for error in structure_errors:
                print(f"- {error}")
            return 1
    if template_id == "skill-method-reference":
        structure_errors = method_reference_structure_errors(current_version)
        if structure_errors:
            print("skill method reference structure errors:")
            for error in structure_errors:
                print(f"- {error}")
            return 1

    if require and (missing or not_current):
        return 1
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="regenerate docs/skills/registry.jsonl before checking it",
    )
    parser.add_argument(
        "--strict-tier3",
        action="store_true",
        help="disallow peer Tier 3 todo links; default allows intentional Tier 3 handoffs",
    )
    parser.add_argument(
        "--capture-hardcase",
        action="store_true",
        help="write a deduplicated hardcase seed on tier violations; validation stays pure by default",
    )
    parser.add_argument(
        "--template-version",
        help="report skills missing or differing from this current skill template version",
    )
    parser.add_argument(
        "--template-id",
        default="skill-template",
        help="template id to report with --template-version",
    )
    parser.add_argument(
        "--require-template-version",
        action="store_true",
        help="fail when --template-version finds missing or non-current skill template versions",
    )
    parser.add_argument(
        "--method-reference-contract",
        action="store_true",
        help="check only the static skill-method-reference template contract",
    )
    args = parser.parse_args()
    if args.require_template_version and not args.template_version:
        parser.error("--require-template-version requires --template-version")

    if args.method_reference_contract:
        errors = method_reference_structure_errors(CURRENT_METHOD_REFERENCE_VERSION)
        if errors:
            print("skill method reference structure errors:")
            for error in errors:
                print(f"- {error}")
            return 1
        print("skill method reference templates OK")
        return 0

    try:
        if args.write:
            run(["python3", "skills/skill-maintenance/scripts/sync_skill_checklists.py", "--write"])
            run(["python3", "bin/validators/sync_skill_registry.py", "--write"])
            run(["python3", "bin/validators/sync_template_registry.py", "--write"])
            run(["python3", "skills/skill-maintenance/scripts/generate_template_intelligence.py"])

        # The pure repository contracts have one route: the lint registry.
        # This skill-maintenance command only adds explicit writers, optional
        # strict/hardcase behavior, rollout reporting, and compile smoke tests.
        run(["python3", "bin/farplane.py", "lint", "skills"])

        if args.strict_tier3 or args.capture_hardcase:
            tier_command = ["python3", "bin/validators/check_skill_todo_tiers.py"]
            if not args.strict_tier3:
                tier_command.append("--allow-peer-tier3")
            if args.capture_hardcase:
                tier_command.append("--hardcase-on-failure")
            run(tier_command)

        run(
            [
                "python3",
                "-m",
                "py_compile",
                "bin/core/lint/models.py",
                "bin/core/lint/registry.py",
                "bin/core/lint/runner.py",
                "bin/core/lint/source.py",
                "bin/validators/sync_skill_registry.py",
                "bin/validators/check_skill_frontmatter.py",
                "bin/validators/sync_template_registry.py",
                "bin/validators/template_usage.py",
                "bin/validators/check_doc_refs.py",
                "bin/validators/check_skill_todo_tiers.py",
                "bin/validators/check_tier0_phase_protocol.py",
                "bin/validators/check_skill_surface_budget.py",
                "bin/validators/check_skill_capabilities.py",
                "bin/validators/check_eval_contract.py",
                "bin/core/eval_contract.py",
                "skills/skill-maintenance/scripts/check_skills.py",
                "skills/skill-maintenance/scripts/minimize_skill_surface.py",
                "skills/skill-maintenance/scripts/sync_skill_checklists.py",
                "skills/skill-maintenance/scripts/generate_template_intelligence.py",
                "skills/eval/scripts/check_eval_queries.py",
            ]
        )
    except subprocess.CalledProcessError as exc:
        return exc.returncode

    print("skill system summary:")
    print(json.dumps(registry_summary(), indent=2, sort_keys=True))
    if args.template_version:
        return validate_skill_template_rollout(
            args.template_id, args.template_version, args.require_template_version
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
