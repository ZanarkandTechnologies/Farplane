#!/usr/bin/env python3
"""Validate the structural and provenance contract of the Feed Scout Brief."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path
from typing import Any

import yaml


REQUIRED_SECTIONS = ("ICPs", "Trends", "Other Notable Things", "Source Gaps")
EVIDENCE_LEVELS = {"observed", "analogous", "hypothesis", "source_gap"}
FRONTMATTER_REQUIRED = ("kind", "status", "updated_at", "canonical_icp_ref", "source_ledger")
MAX_NON_EMPTY_LINES = 100
PLACEHOLDER_RE = re.compile(r"<[^>]+>")
ENTRY_RE = re.compile(r"^### (.+?)\s*$", flags=re.MULTILINE)
BULLET_RE = re.compile(r"^- (.+?)\s*$", flags=re.MULTILINE)


def compact(value: str) -> str:
    return " ".join(value.split())


def non_empty_line_count(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip())


def section_body(body: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)",
        body,
        flags=re.MULTILINE | re.DOTALL,
    )
    return match.group(1) if match else ""


def entries(section: str) -> list[tuple[str, str]]:
    matches = list(ENTRY_RE.finditer(section))
    return [
        (match.group(1).strip(), section[match.end(): matches[index + 1].start() if index + 1 < len(matches) else len(section)])
        for index, match in enumerate(matches)
    ]


def field(entry_body: str, label: str) -> str | None:
    match = re.search(rf"^- {re.escape(label)}:\s*(.+?)\s*$", entry_body, flags=re.MULTILINE)
    return match.group(1).strip() if match else None


def bullets(section: str) -> list[str]:
    return [match.group(1).strip() for match in BULLET_RE.finditer(section)]


def parse_bullet_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for part in [part.strip() for part in text.split("|")]:
        if "=" in part:
            key, value = part.split("=", 1)
            fields[key.strip().lower()] = value.strip()
        elif ":" in part:
            key, value = part.split(":", 1)
            fields[key.strip().lower()] = value.strip()
        elif "kind" not in fields:
            fields["kind"] = part
    return fields


def has_ref(value: str | None) -> bool:
    return bool(value and ("`" in value or "http://" in value or "https://" in value or "eval-fixture://" in value))


def validate_sourced_entries(section: str, *, kind: str, required_fields: tuple[str, ...]) -> list[str]:
    errors: list[str] = []
    for title, entry_body in entries(section):
        for label in required_fields:
            value = field(entry_body, label)
            if not value or value.lower() in {"none", "null", "n/a"}:
                errors.append(f"{kind} entry {title!r} is missing {label}")
        source_refs = field(entry_body, "Source refs")
        if source_refs and not ("`" in source_refs or "http://" in source_refs or "https://" in source_refs):
            errors.append(f"{kind} entry {title!r} Source refs must contain a file or URL ref")
    return errors


def validate_simple_sourced_bullets(
    section: str,
    *,
    kind: str,
    required_fields: tuple[str, ...],
    require_confidence: bool = False,
) -> list[str]:
    errors: list[str] = []
    entries = [bullet for bullet in bullets(section) if bullet.lower() not in {"none.", "none observed."}]
    for index, bullet in enumerate(entries, start=1):
        fields = parse_bullet_fields(bullet)
        evidence_level = (fields.get("kind") or fields.get("evidence") or "").lower()
        if evidence_level not in EVIDENCE_LEVELS:
            errors.append(f"{kind} bullet {index} must start with evidence level observed, analogous, hypothesis, or source_gap")
        for label in required_fields:
            if not fields.get(label):
                errors.append(f"{kind} bullet {index} is missing {label}=")
        if require_confidence and fields.get("conf", "").lower() not in {"low", "medium", "high"}:
            errors.append(f"{kind} bullet {index} conf must be low, medium, or high")
        if fields.get("seen"):
            try:
                date.fromisoformat(fields["seen"])
            except ValueError:
                errors.append(f"{kind} bullet {index} seen must be an ISO date")
        if not has_ref(fields.get("refs")):
            errors.append(f"{kind} bullet {index} refs must contain a file or URL ref")
    return errors


def load_expected_icps(harness_path: Path | None) -> dict[str, dict[str, Any]]:
    if harness_path is None or not harness_path.is_file():
        return {}
    payload = yaml.safe_load(harness_path.read_text(encoding="utf-8")) or {}
    areas = payload.get("areas") if isinstance(payload, dict) else {}
    return {
        str(area_id): area["icp"]
        for area_id, area in (areas.items() if isinstance(areas, dict) else [])
        if isinstance(area, dict) and isinstance(area.get("icp"), dict)
    }


def validate_scout_brief_text(
    text: str,
    *,
    allow_template_placeholders: bool = False,
    expected_icps: dict[str, dict[str, Any]] | None = None,
) -> list[str]:
    errors: list[str] = []
    if not text.startswith("---\n"):
        return ["Scout Brief must start with YAML frontmatter"]
    line_count = non_empty_line_count(text)
    if not allow_template_placeholders and line_count > MAX_NON_EMPTY_LINES:
        errors.append(
            f"Scout Brief has {line_count} non-empty lines; maximum is {MAX_NON_EMPTY_LINES}. "
            "Merge, replace, or demote detail to the dated report."
        )
    try:
        _, frontmatter_text, body = text.split("---", 2)
        frontmatter = yaml.safe_load(frontmatter_text) or {}
    except (ValueError, yaml.YAMLError) as exc:
        return [f"invalid YAML frontmatter: {exc}"]
    if not isinstance(frontmatter, dict):
        return ["frontmatter must be an object"]
    for key in FRONTMATTER_REQUIRED:
        if key not in frontmatter:
            errors.append(f"frontmatter is missing {key}")
    if frontmatter.get("kind") != "feed-scout-brief":
        errors.append("frontmatter kind must be feed-scout-brief")
    if not allow_template_placeholders and not frontmatter.get("updated_at"):
        errors.append("live Scout Brief frontmatter updated_at must be populated")
    headings = re.findall(r"^## (.+?)\s*$", body, flags=re.MULTILINE)
    for section in REQUIRED_SECTIONS:
        count = headings.count(section)
        if count != 1:
            errors.append(f"Scout Brief must contain exactly one ## {section} section")
    unexpected_headings = sorted(set(headings) - set(REQUIRED_SECTIONS))
    if unexpected_headings:
        errors.append(f"Scout Brief has unsupported H2 sections: {', '.join(unexpected_headings)}")
    if not allow_template_placeholders and PLACEHOLDER_RE.search(body):
        errors.append("live Scout Brief must not contain template placeholders")
    if "append-only" not in body and "not a daily log" not in body:
        errors.append("Scout Brief must state its update-in-place/non-timeline boundary")
    if re.search(r"^### ", body, flags=re.MULTILINE):
        errors.append("Scout Brief must use simple bullets, not H3 entry blocks")
    icp_section = section_body(body, "ICPs")
    icp_bullets = [bullet for bullet in bullets(icp_section) if bullet.lower() not in {"none.", "none observed."}]
    if not icp_bullets:
        errors.append("Scout Brief ICP section must include at least one bullet entry")
    observed_icp_ids: list[str] = []
    for index, bullet in enumerate(icp_bullets, start=1):
        match = re.match(r"`([^`]+)`\s+—\s*([^|]+)", bullet)
        area_id = match.group(1) if match else ""
        if not area_id:
            errors.append(f"ICP bullet {index} must start with a backticked area ID and label")
            continue
        observed_icp_ids.append(area_id)
        label = compact(match.group(2)) if match else ""
        fields = parse_bullet_fields(bullet)
        expected_ref = f"`farplane/harness.yaml#areas.{area_id}.icp`"
        if not allow_template_placeholders and fields.get("ref") != expected_ref:
            errors.append(f"ICP bullet {area_id!r} has an invalid ref")
        if not allow_template_placeholders and not has_ref(fields.get("refs")):
            errors.append(f"ICP bullet {area_id!r} is missing refs")
        expected = (expected_icps or {}).get(area_id)
        if expected:
            expected_label = compact(str(expected.get("label") or ""))
            if expected_label and label != expected_label:
                errors.append(f"ICP bullet {area_id!r} label does not match harness.yaml")
    if expected_icps:
        missing = sorted(set(expected_icps) - set(observed_icp_ids))
        extra = sorted(set(observed_icp_ids) - set(expected_icps))
        if missing:
            errors.append(f"Scout Brief is missing configured ICP areas: {', '.join(missing)}")
        if extra:
            errors.append(f"Scout Brief has unknown ICP areas: {', '.join(extra)}")
        duplicates = sorted({area_id for area_id in observed_icp_ids if observed_icp_ids.count(area_id) > 1})
        if duplicates:
            errors.append(f"Scout Brief has duplicate ICP areas: {', '.join(duplicates)}")

    if not allow_template_placeholders:
        trend_section = section_body(body, "Trends")
        errors.extend(validate_simple_sourced_bullets(
            trend_section,
            kind="trend",
            required_fields=("icp", "claim", "use", "seen", "conf", "refs"),
            require_confidence=True,
        ))

        notable_section = section_body(body, "Other Notable Things")
        errors.extend(validate_simple_sourced_bullets(
            notable_section,
            kind="notable",
            required_fields=("type", "icp", "note", "use", "seen", "refs"),
        ))
    return errors


def validate_scout_brief(
    path: Path,
    *,
    allow_template_placeholders: bool = False,
    harness_path: Path | None = None,
) -> list[str]:
    if not path.is_file():
        return [f"Scout Brief file does not exist: {path}"]
    if harness_path is None and not allow_template_placeholders:
        candidate = path.resolve().parents[2] / "farplane" / "harness.yaml" if len(path.resolve().parents) > 2 else None
        harness_path = candidate if candidate and candidate.is_file() else None
    return validate_scout_brief_text(
        path.read_text(encoding="utf-8"),
        allow_template_placeholders=allow_template_placeholders,
        expected_icps=load_expected_icps(harness_path),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--allow-template-placeholders", action="store_true")
    parser.add_argument("--harness", type=Path)
    args = parser.parse_args()
    errors = validate_scout_brief(
        args.path,
        allow_template_placeholders=args.allow_template_placeholders,
        harness_path=args.harness,
    )
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
