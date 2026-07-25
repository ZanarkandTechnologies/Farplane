#!/usr/bin/env python3
"""Validate and append minimal Interval highlight rows.

The ledger kind supplies the row kind, so canonical rows do not duplicate it.
Identity is the composite key ``(kind, team, report)``.
"""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import re
from pathlib import Path, PurePosixPath
from typing import Any, TextIO


KINDS = {"win", "failure"}
LEDGER_NAMES = {"win": "wins.jsonl", "failure": "failures.jsonl"}
FIELDS = {
    "win": frozenset({"team", "report", "summary", "links"}),
    "failure": frozenset({"team", "report", "summary", "lesson", "links"}),
}
REQUIRED_FIELDS = {
    "win": frozenset({"team", "report", "summary"}),
    "failure": frozenset({"team", "report", "summary", "lesson"}),
}
TEAM_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REPORT_PATTERN = re.compile(
    r"^reports/interval/[a-z][a-z0-9_-]*/[A-Za-z0-9][A-Za-z0-9T:+_.-]*$"
)


class HighlightValidationError(ValueError):
    """Raised when a row or its owning ledger is not canonical."""


def ledger_path(project_root: Path, kind: str) -> Path:
    """Return the canonical project-local ledger path for ``kind``."""
    _validate_kind(kind)
    return project_root / ".farplane" / "highlights" / LEDGER_NAMES[kind]


def highlight_key(kind: str, row: dict[str, Any]) -> tuple[str, str, str]:
    """Return the natural identity after row validation."""
    canonical = validate_highlight(kind, row)
    return kind, canonical["team"], canonical["report"]


def validate_highlight(kind: str, row: Any) -> dict[str, Any]:
    """Return a normalized minimal row or raise ``HighlightValidationError``."""
    _validate_kind(kind)
    if not isinstance(row, dict):
        raise HighlightValidationError("row_must_be_object")

    supplied = set(row)
    missing = REQUIRED_FIELDS[kind] - supplied
    extra = supplied - FIELDS[kind]
    if missing:
        raise HighlightValidationError(
            f"missing_fields:{','.join(sorted(missing))}"
        )
    if extra:
        raise HighlightValidationError(
            f"unsupported_fields:{','.join(sorted(extra))}"
        )

    canonical: dict[str, Any] = {}
    team = _single_line(row["team"], "team")
    if not TEAM_PATTERN.fullmatch(team):
        raise HighlightValidationError("invalid_team_slug")
    canonical["team"] = team

    report = _single_line(row["report"], "report")
    if not REPORT_PATTERN.fullmatch(report):
        raise HighlightValidationError("invalid_interval_report_ref")
    canonical["report"] = report
    canonical["summary"] = _single_line(row["summary"], "summary")

    if kind == "failure":
        canonical["lesson"] = _single_line(row["lesson"], "lesson")

    if "links" in row:
        links = row["links"]
        if not isinstance(links, list) or not links:
            raise HighlightValidationError("links_must_be_nonempty_array")
        canonical_links = [_validate_link(link) for link in links]
        if len(canonical_links) != len(set(canonical_links)):
            raise HighlightValidationError("duplicate_links")
        canonical["links"] = canonical_links
    return canonical


def validate_report_ref(project_root: Path, report_ref: str) -> Path:
    """Require the ref to resolve to the exact completed Interval report."""
    if not REPORT_PATTERN.fullmatch(report_ref):
        raise HighlightValidationError("invalid_interval_report_ref")
    report_path = project_root / ".farplane" / f"{report_ref}.md"
    if not report_path.is_file():
        raise HighlightValidationError(f"missing_report_ref:{report_ref}")

    frontmatter = _read_frontmatter(report_path)
    if frontmatter.get("ref") != report_ref:
        raise HighlightValidationError("report_ref_mismatch")
    if frontmatter.get("kind") != "interval-report":
        raise HighlightValidationError("report_is_not_interval_report")
    if frontmatter.get("status") != "complete":
        raise HighlightValidationError("report_is_not_complete")
    return report_path


def read_highlights(
    project_root: Path,
    kind: str,
    *,
    validate_reports: bool = False,
) -> list[dict[str, Any]]:
    """Read one strict ledger, rejecting malformed or duplicate canonical rows."""
    path = ledger_path(project_root, kind)
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_SH)
        return _read_locked_rows(
            handle,
            path,
            kind,
            project_root=project_root if validate_reports else None,
        )


def append_highlight(project_root: Path, kind: str, row: Any) -> str:
    """Append once after finalization; return ``appended`` or ``already_exists``."""
    root = project_root.resolve()
    canonical = validate_highlight(kind, row)
    validate_report_ref(root, canonical["report"])
    path = ledger_path(root, kind)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("a+", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        rows = _read_locked_rows(
            handle,
            path,
            kind,
            project_root=root,
        )
        key = (kind, canonical["team"], canonical["report"])
        if any((kind, item["team"], item["report"]) == key for item in rows):
            return "already_exists"

        handle.seek(0, os.SEEK_END)
        handle.write(
            json.dumps(canonical, ensure_ascii=False, separators=(",", ":")) + "\n"
        )
        handle.flush()
        os.fsync(handle.fileno())
    return "appended"


def _validate_kind(kind: str) -> None:
    if kind not in KINDS:
        raise HighlightValidationError(f"unsupported_kind:{kind}")


def _single_line(value: Any, field: str) -> str:
    if not isinstance(value, str):
        raise HighlightValidationError(f"{field}_must_be_string")
    normalized = value.strip()
    if not normalized:
        raise HighlightValidationError(f"{field}_must_not_be_empty")
    if "\n" in normalized or "\r" in normalized:
        raise HighlightValidationError(f"{field}_must_be_single_line")
    return normalized


def _validate_link(value: Any) -> str:
    link = _single_line(value, "link")
    if "://" in link or link.startswith(("/", "~", "#")):
        raise HighlightValidationError(f"unsafe_project_relative_link:{link}")
    path_part = link.split("#", 1)[0]
    if not path_part or "?" in path_part:
        raise HighlightValidationError(f"unsafe_project_relative_link:{link}")
    path = PurePosixPath(path_part)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise HighlightValidationError(f"unsafe_project_relative_link:{link}")
    return link


def _read_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise HighlightValidationError("report_frontmatter_missing")
    result: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return result
        if ":" not in line or line[:1].isspace():
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip("\"'")
    raise HighlightValidationError("report_frontmatter_unclosed")


def _read_locked_rows(
    handle: TextIO,
    path: Path,
    kind: str,
    *,
    project_root: Path | None,
) -> list[dict[str, Any]]:
    handle.seek(0)
    rows: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for line_number, line in enumerate(handle, start=1):
        if not line.strip():
            continue
        try:
            raw = json.loads(line)
        except json.JSONDecodeError as exc:
            raise HighlightValidationError(
                f"malformed_jsonl:{path}:{line_number}:{exc.msg}"
            ) from exc
        try:
            row = validate_highlight(kind, raw)
            if project_root is not None:
                validate_report_ref(project_root, row["report"])
        except HighlightValidationError as exc:
            raise HighlightValidationError(
                f"invalid_ledger_row:{path}:{line_number}:{exc}"
            ) from exc
        key = (kind, row["team"], row["report"])
        if key in seen:
            raise HighlightValidationError(
                f"duplicate_ledger_key:{path}:{line_number}"
            )
        seen.add(key)
        rows.append(row)
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("append", "validate"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("--kind", required=True, choices=sorted(KINDS))
        subparser.add_argument("--row-json", required=True)
    read_parser = subparsers.add_parser("read")
    read_parser.add_argument("--kind", required=True, choices=sorted(KINDS))
    read_parser.add_argument("--validate-reports", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    try:
        if args.command == "read":
            result: Any = read_highlights(
                project_root,
                args.kind,
                validate_reports=args.validate_reports,
            )
        else:
            row = json.loads(args.row_json)
            if args.command == "validate":
                result = validate_highlight(args.kind, row)
                validate_report_ref(project_root, result["report"])
            else:
                status = append_highlight(project_root, args.kind, row)
                result = {
                    "status": status,
                    "kind": args.kind,
                    "key": [args.kind, row.get("team"), row.get("report")],
                    "path": str(ledger_path(project_root, args.kind)),
                }
    except (HighlightValidationError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "invalid", "error": str(exc)}))
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
