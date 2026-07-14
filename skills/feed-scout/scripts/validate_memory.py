#!/usr/bin/env python3
"""Validate the structural and provenance contract of Feed Scout memory."""

from __future__ import annotations

import argparse
import re
from datetime import date
from pathlib import Path
from typing import Any

import yaml


REQUIRED_SECTIONS = ("ICPs", "Trends", "Other Notable Things", "Source Gaps")
FRONTMATTER_REQUIRED = ("kind", "status", "updated_at", "canonical_icp_ref", "source_ledger")
PLACEHOLDER_RE = re.compile(r"<[^>]+>")
ENTRY_RE = re.compile(r"^### (.+?)\s*$", flags=re.MULTILINE)


def compact(value: str) -> str:
    return " ".join(value.split())


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


def validate_memory_text(
    text: str,
    *,
    allow_template_placeholders: bool = False,
    expected_icps: dict[str, dict[str, Any]] | None = None,
) -> list[str]:
    errors: list[str] = []
    if not text.startswith("---\n"):
        return ["memory must start with YAML frontmatter"]
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
    if frontmatter.get("kind") != "feed-scout-memory":
        errors.append("frontmatter kind must be feed-scout-memory")
    if not allow_template_placeholders and not frontmatter.get("updated_at"):
        errors.append("live memory frontmatter updated_at must be populated")
    headings = re.findall(r"^## (.+?)\s*$", body, flags=re.MULTILINE)
    for section in REQUIRED_SECTIONS:
        count = headings.count(section)
        if count != 1:
            errors.append(f"memory must contain exactly one ## {section} section")
    unexpected_headings = sorted(set(headings) - set(REQUIRED_SECTIONS))
    if unexpected_headings:
        errors.append(f"memory has unsupported H2 sections: {', '.join(unexpected_headings)}")
    if not allow_template_placeholders and PLACEHOLDER_RE.search(body):
        errors.append("live memory must not contain template placeholders")
    if "append-only" not in body and "not a daily log" not in body:
        errors.append("memory must state its update-in-place/non-timeline boundary")
    icp_section = section_body(body, "ICPs")
    icp_entries = entries(icp_section)
    if not icp_entries:
        errors.append("memory ICP section must include at least one H3 entry")
    observed_icp_ids: list[str] = []
    for title, entry_body in icp_entries:
        match = re.match(r"`([^`]+)`\s+—", title)
        area_id = match.group(1) if match else ""
        if not area_id:
            errors.append(f"ICP entry {title!r} must start with a backticked area ID")
            continue
        observed_icp_ids.append(area_id)
        expected_ref = f"`farplane/harness.yaml#areas.{area_id}.icp`"
        if field(entry_body, "Canonical ref") != expected_ref:
            errors.append(f"ICP entry {area_id!r} has an invalid Canonical ref")
        if not field(entry_body, "Source refs"):
            errors.append(f"ICP entry {area_id!r} is missing Source refs")
        expected = (expected_icps or {}).get(area_id)
        if expected:
            scalar_fields = {
                "Description": expected.get("description"),
                "Evidence bar": expected.get("evidence_bar"),
            }
            for label, expected_value in scalar_fields.items():
                actual_value = field(entry_body, label)
                if not actual_value or compact(actual_value) != compact(str(expected_value or "")):
                    errors.append(f"ICP entry {area_id!r} {label} does not match harness.yaml")
            list_fields = {
                "Jobs to be done": expected.get("jobs_to_be_done"),
                "Pain points": expected.get("pain_points"),
            }
            for label, expected_values in list_fields.items():
                actual_value = compact(field(entry_body, label) or "")
                for expected_value in expected_values if isinstance(expected_values, list) else []:
                    if compact(str(expected_value)) not in actual_value:
                        errors.append(f"ICP entry {area_id!r} {label} does not match harness.yaml")
                        break
    if expected_icps:
        missing = sorted(set(expected_icps) - set(observed_icp_ids))
        extra = sorted(set(observed_icp_ids) - set(expected_icps))
        if missing:
            errors.append(f"memory is missing configured ICP areas: {', '.join(missing)}")
        if extra:
            errors.append(f"memory has unknown ICP areas: {', '.join(extra)}")
        duplicates = sorted({area_id for area_id in observed_icp_ids if observed_icp_ids.count(area_id) > 1})
        if duplicates:
            errors.append(f"memory has duplicate ICP areas: {', '.join(duplicates)}")

    if not allow_template_placeholders:
        trend_section = section_body(body, "Trends")
        errors.extend(validate_sourced_entries(
            trend_section,
            kind="trend",
            required_fields=(
                "ICP refs", "Current synthesis", "Why it matters", "Baseline or default",
                "Last observed", "Confidence", "Source refs", "Candidate experiment shapes",
            ),
        ))
        for title, entry_body in entries(trend_section):
            confidence = (field(entry_body, "Confidence") or "").lower()
            if confidence and confidence not in {"low", "medium", "high"}:
                errors.append(f"trend entry {title!r} has invalid Confidence")
            observed = field(entry_body, "Last observed") or ""
            try:
                date.fromisoformat(observed)
            except ValueError:
                errors.append(f"trend entry {title!r} Last observed must be an ISO date")

        notable_section = section_body(body, "Other Notable Things")
        if entries(notable_section):
            errors.extend(validate_sourced_entries(
                notable_section,
                kind="notable",
                required_fields=("Type", "ICP refs", "Note", "Last observed", "Source refs"),
            ))
    return errors


def validate_memory(
    path: Path,
    *,
    allow_template_placeholders: bool = False,
    harness_path: Path | None = None,
) -> list[str]:
    if not path.is_file():
        return [f"memory file does not exist: {path}"]
    if harness_path is None and not allow_template_placeholders:
        candidate = path.resolve().parents[2] / "farplane" / "harness.yaml" if len(path.resolve().parents) > 2 else None
        harness_path = candidate if candidate and candidate.is_file() else None
    return validate_memory_text(
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
    errors = validate_memory(
        args.path,
        allow_template_placeholders=args.allow_template_placeholders,
        harness_path=args.harness,
    )
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
