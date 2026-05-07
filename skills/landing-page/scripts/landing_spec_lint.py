#!/usr/bin/env python3
"""Validate the planning gates for a premium landing-page spec."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_SECTIONS = (
    "Offer",
    "Audience",
    "Non-goals",
    "Decision Boundaries",
    "Taste References",
    "Narrative Arc",
    "Low-fi ASCII Flow",
    "Section Matrix",
    "Asset Plan",
    "Motion Plan",
    "Proof Plan",
    "Designer Judgment Plan",
    "QA Gates",
    "Executor Handoff",
)

MATRIX_COLUMNS = (
    "Section",
    "User job",
    "Narrative claim",
    "Visual carrier",
    "Asset plan",
    "Motion/effect",
    "Proof/copy payload",
    "QA assertion",
)

MAIN_SECTION_WORDS = ("hero", "problem", "solution", "capabilities", "proof", "cta")

QA_TERMS = (
    "section quality",
    "section_quality_qa",
    "designer judgment",
    "mobile",
    "reduced-motion",
    "reduced motion",
    "console",
    "runtime",
)

PLACEHOLDER_PATTERNS = (
    r"\bTBD\b",
    r"\bTODO\b",
    r"REPLACE_ME",
    r"CHANGEME",
    r"<[^>\n]+>",
)


def strip_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end].strip()
    meta: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"')
    return meta, text[end + 4 :]


def section_body(markdown: str, heading: str) -> str:
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(markdown)
    if not match:
        return ""
    next_match = re.search(r"^##\s+", markdown[match.end() :], re.MULTILINE)
    if not next_match:
        return markdown[match.end() :].strip()
    return markdown[match.end() : match.end() + next_match.start()].strip()


def table_rows(body: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|") or not stripped.endswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")) for cell in cells):
            continue
        rows.append(cells)
    return rows


def lint_spec(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    meta, body = strip_frontmatter(text)
    findings: list[str] = []

    if meta.get("status", "").lower() != "approved":
        findings.append("frontmatter status must be approved")
    if not meta.get("approval_source"):
        findings.append("frontmatter approval_source is required")

    for heading in REQUIRED_SECTIONS:
        content = section_body(body, heading)
        if not content:
            findings.append(f"missing section: {heading}")
        elif len(content.replace("|", "").strip()) < 20:
            findings.append(f"section is too thin: {heading}")

    matrix = section_body(body, "Section Matrix")
    rows = table_rows(matrix)
    if not rows:
        findings.append("Section Matrix must be a markdown table")
    else:
        header = rows[0]
        for column in MATRIX_COLUMNS:
            if column not in header:
                findings.append(f"Section Matrix missing column: {column}")
        data_rows = rows[1:]
        covered = set()
        for row in data_rows:
            joined = row[0].lower() if row else ""
            for word in MAIN_SECTION_WORDS:
                if word in joined:
                    covered.add(word)
            if len(row) >= len(MATRIX_COLUMNS):
                for index, column in enumerate(MATRIX_COLUMNS):
                    min_length = 3 if column == "Section" else 5
                    if not row[index] or len(row[index]) < min_length:
                        findings.append(f"Section Matrix row has thin {column}: {row[0] or 'unnamed'}")
        for word in MAIN_SECTION_WORDS:
            if word not in covered:
                findings.append(f"Section Matrix missing main section coverage: {word}")

    qa_gates = section_body(body, "QA Gates")
    for term in QA_TERMS:
        if term not in qa_gates.lower():
            findings.append(f"QA Gates missing term: {term}")

    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, text):
            findings.append(f"placeholder remains: {pattern}")

    return {
        "path": str(path),
        "verdict": "PASS" if not findings else "FAIL",
        "findings": findings,
        "required_sections": list(REQUIRED_SECTIONS),
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = lint_spec(args.spec)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"{result['verdict']} {result['path']}")
        for finding in result["findings"]:
            print(f"- {finding}")
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
