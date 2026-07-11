#!/usr/bin/env python3
"""Build the Core-owned Farplane report registry."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import date as date_type
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


REPORTS_ROOT = Path(".farplane/reports")
REPORT_INDEX_PATH = REPORTS_ROOT / "index.json"
REQUIRED_FIELDS = ("ref", "kind", "created_at", "ui_summary")


@dataclass(frozen=True)
class ReportIssue:
    path: str
    reason: str


@dataclass(frozen=True)
class ReportRepair:
    path: str
    ref: str
    action: str


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def json_value(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date_type):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(key): json_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_value(item) for item in value]
    if isinstance(value, tuple):
        return [json_value(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def read_frontmatter(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n") or "\n---\n" not in text:
        return None, "missing_frontmatter"
    raw = text.split("\n---\n", 1)[0][4:]
    try:
        loaded = yaml.safe_load(raw) or {}
    except yaml.YAMLError as exc:
        return None, f"invalid_frontmatter:{exc.__class__.__name__}"
    if not isinstance(loaded, dict):
        return None, "frontmatter_not_object"
    return {str(key): json_value(value) for key, value in loaded.items()}, None


def frontmatter_bounds(text: str) -> tuple[int, int] | None:
    if not text.startswith("---\n"):
        return None
    marker = "\n---\n"
    end = text.find(marker, 4)
    if end == -1:
        return None
    return 4, end


def field_text(frontmatter: dict[str, Any], field: str) -> str:
    value = frontmatter.get(field)
    if value is None:
        return ""
    return str(value).strip()


def ref_parts(ref: str) -> list[str]:
    return [part for part in ref.split("/") if part]


def validate_ref(ref: str) -> str | None:
    if not ref:
        return "missing:ref"
    parts = ref.split("/")
    if ref.startswith("/") or ref.endswith("/") or "" in parts:
        return "invalid_ref_path"
    if any(part in {".", ".."} for part in parts):
        return "invalid_ref_path"
    return None


def path_derived_ref(path: Path, project_root: Path) -> str:
    rel_path = path.relative_to(project_root / ".farplane").with_suffix("")
    return rel_path.as_posix()


def add_missing_ref(path: Path, project_root: Path, *, dry_run: bool = False) -> ReportRepair | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    bounds = frontmatter_bounds(text)
    if bounds is None:
        return None

    frontmatter, issue = read_frontmatter(path)
    if issue or frontmatter is None or field_text(frontmatter, "ref"):
        return None

    ref = path_derived_ref(path, project_root)
    if validate_ref(ref):
        return None

    if not dry_run:
        start, _end = bounds
        updated = text[:start] + f"ref: {ref}\n" + text[start:]
        path.write_text(updated, encoding="utf-8")
    return ReportRepair(path.relative_to(project_root).as_posix(), ref, "added_ref")


def repair_missing_refs(project_root: Path, *, dry_run: bool = False) -> list[ReportRepair]:
    root = project_root / REPORTS_ROOT
    repairs: list[ReportRepair] = []
    if not root.exists():
        return repairs
    for path in sorted(root.glob("**/*.md")):
        repair = add_missing_ref(path, project_root, dry_run=dry_run)
        if repair is not None:
            repairs.append(repair)
    return repairs


def ancestor_refs(ref: str) -> list[str]:
    parts = ref_parts(ref)
    return ["/".join(parts[:index]) for index in range(1, len(parts))]


def nearest_parent_ref(ref: str, included_refs: set[str]) -> str | None:
    for candidate in reversed(ancestor_refs(ref)):
        if candidate in included_refs:
            return candidate
    return None


def report_record(path: Path, project_root: Path, frontmatter: dict[str, Any]) -> dict[str, Any]:
    rel_path = path.relative_to(project_root).as_posix()
    ref = field_text(frontmatter, "ref")
    kind = field_text(frontmatter, "kind")
    created_at = field_text(frontmatter, "created_at")
    ui_summary = field_text(frontmatter, "ui_summary")
    ancestors = ancestor_refs(ref)
    return {
        "ref": ref,
        "kind": kind,
        "created_at": created_at,
        "ui_summary": ui_summary,
        "path": rel_path,
        "parent_ref": None,
        "children_refs": [],
        "ancestor_refs": ancestors,
        "group_ref": ancestors[-1] if ancestors else None,
        "depth": len(ref_parts(ref)),
        "source_ref": {"path": rel_path},
        "frontmatter": frontmatter,
    }


def build_report_registry(project_root: Path) -> dict[str, Any]:
    root = project_root / REPORTS_ROOT
    issues: list[ReportIssue] = []
    records: list[dict[str, Any]] = []
    seen_refs: set[str] = set()

    if root.exists():
        for path in sorted(root.glob("**/*.md")):
            rel_path = path.relative_to(project_root).as_posix()
            frontmatter, issue = read_frontmatter(path)
            if issue or frontmatter is None:
                issues.append(ReportIssue(rel_path, issue or "invalid_frontmatter"))
                continue

            missing = [field for field in REQUIRED_FIELDS if not field_text(frontmatter, field)]
            if missing:
                issues.append(ReportIssue(rel_path, "missing_required:" + ",".join(missing)))
                continue

            ref = field_text(frontmatter, "ref")
            ref_issue = validate_ref(ref)
            if ref_issue:
                issues.append(ReportIssue(rel_path, ref_issue))
                continue
            if ref in seen_refs:
                issues.append(ReportIssue(rel_path, f"duplicate_ref:{ref}"))
                continue

            seen_refs.add(ref)
            records.append(report_record(path, project_root, frontmatter))

    refs = {record["ref"] for record in records}
    children: dict[str, list[str]] = {ref: [] for ref in refs}
    for record in records:
        parent_ref = nearest_parent_ref(str(record["ref"]), refs)
        record["parent_ref"] = parent_ref
        if parent_ref is not None:
            children[parent_ref].append(str(record["ref"]))

    for record in records:
        record["children_refs"] = sorted(children[str(record["ref"])])

    records.sort(key=lambda item: (str(item["created_at"]), str(item["ref"])), reverse=True)

    return {
        "schema_version": 1,
        "generated_at": now_utc(),
        "report_root": REPORTS_ROOT.as_posix(),
        "index_path": REPORT_INDEX_PATH.as_posix(),
        "required_frontmatter": list(REQUIRED_FIELDS),
        "reports": records,
        "by_ref": {str(record["ref"]): record for record in sorted(records, key=lambda item: str(item["ref"]))},
        "issues": [issue.__dict__ for issue in issues],
        "counts": {
            "included": len(records),
            "excluded": len(issues),
        },
    }


def write_report_registry(project_root: Path, registry: dict[str, Any]) -> Path:
    path = project_root / REPORT_INDEX_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(registry, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def run_index(args: argparse.Namespace) -> int:
    project_root = Path(args.project_root).expanduser().resolve()
    registry = build_report_registry(project_root)
    if not args.no_write:
        write_report_registry(project_root, registry)
    if args.json:
        print(json.dumps(registry, indent=2, sort_keys=True))
    else:
        counts = registry["counts"]
        action = "would index" if args.no_write else "indexed"
        print(
            f"farplane reports {action}: {counts['included']} included, "
            f"{counts['excluded']} excluded -> {project_root / REPORT_INDEX_PATH}"
        )
    return 0


def run_repair_refs(args: argparse.Namespace) -> int:
    project_root = Path(args.project_root).expanduser().resolve()
    repairs = repair_missing_refs(project_root, dry_run=bool(args.no_write))
    registry = build_report_registry(project_root)
    if not args.no_index and not args.no_write:
        write_report_registry(project_root, registry)

    payload = {
        "project_root": str(project_root),
        "dry_run": bool(args.no_write),
        "repaired": [repair.__dict__ for repair in repairs],
        "counts": registry["counts"],
        "index_path": REPORT_INDEX_PATH.as_posix(),
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        action = "would repair" if args.no_write else "repaired"
        index_action = " without indexing" if args.no_index or args.no_write else " and indexed"
        print(
            f"farplane reports {action}: {len(repairs)} refs{index_action}; "
            f"{registry['counts']['included']} included, "
            f"{registry['counts']['excluded']} excluded"
        )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command")

    index = sub.add_parser("index", help="Write .farplane/reports/index.json from report Markdown frontmatter.")
    index.add_argument("--project-root", default=".")
    index.add_argument("--no-write", action="store_true")
    index.add_argument("--json", action="store_true")
    index.set_defaults(func=run_index)

    repair = sub.add_parser("repair-refs", help="Add missing path-derived ref frontmatter, then rebuild the report index.")
    repair.add_argument("--project-root", default=".")
    repair.add_argument("--no-write", action="store_true")
    repair.add_argument("--no-index", action="store_true")
    repair.add_argument("--json", action="store_true")
    repair.set_defaults(func=run_repair_refs)
    return parser


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if not argv or argv[0].startswith("-"):
        argv = ["index", *argv]
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
