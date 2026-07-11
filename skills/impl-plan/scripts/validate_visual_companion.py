#!/usr/bin/env python3
"""Validate the mandatory separate visual companion for an impl-plan ticket."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


DIAGRAM_FENCES = re.compile(r"```(?:mermaid|plantuml|dot|graphviz)\b", re.I)
DIAGRAM_WORD = r"(?:diagram|flow|architecture|system[-_ ]?map|mermaid|plantuml|graphviz)"
MARKDOWN_DIAGRAM = re.compile(
    rf"!\[[^\]]*\]\([^)]*{DIAGRAM_WORD}[^)]*\)|"
    rf"!\[[^\]]*{DIAGRAM_WORD}[^\]]*\]\([^)]*\)",
    re.I,
)
HTML_DIAGRAM = re.compile(rf"<img\b[^>]*(?:src|alt)=[\"'][^\"']*{DIAGRAM_WORD}[^\"']*[\"'][^>]*>", re.I)
def section_body(text: str, name: str) -> str | None:
    match = re.search(rf"^## {name}(?:[ \t]*:[^\n]*)?$\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return match.group(1) if match else None


def has_companion_link(text: str) -> bool:
    return bool(re.search(
        r"^- Visual companion:\s+(?:`(?:tickets/[^`]+/)?diagrams\.md`|\[[^\]]+\]\((?:tickets/[^)]+/)?diagrams\.md\))\s*$",
        text,
        re.M | re.I,
    ))


def validate(ticket: Path) -> list[str]:
    errors: list[str] = []
    companion = ticket.with_name("diagrams.md")
    ticket_text = ticket.read_text(encoding="utf-8")
    if DIAGRAM_FENCES.search(ticket_text) or MARKDOWN_DIAGRAM.search(ticket_text) or HTML_DIAGRAM.search(ticket_text):
        errors.append(f"{ticket}: embeds diagram content; move it to {companion}")
    if not has_companion_link(ticket_text):
        errors.append(f"{ticket}: missing required visual companion link to diagrams.md")
    if not companion.is_file():
        return errors + [f"{companion}: required companion does not exist"]

    text = companion.read_text(encoding="utf-8")
    requirements = {
        "canonical_contract: ticket.md": "canonical contract metadata",
        "blocks_approval: false": "non-blocking metadata",
    }
    for needle, label in requirements.items():
        if needle not in text:
            errors.append(f"{companion}: missing {label} ({needle!r})")
    for name in ("Before", "After"):
        body = section_body(text, name)
        if body is None:
            errors.append(f"{companion}: missing anchored ## {name} section")
            continue
        if "```mermaid" not in body:
            errors.append(f"{companion}: {name} section lacks a Mermaid diagram")
        definitions = {
            match.group(1)
            for match in re.finditer(
                r"^\s*classDef\s+([A-Za-z][\w-]*)\s+[^\n]*(?:fill|stroke):#[0-9A-Fa-f]{3,8}",
                body,
                re.M,
            )
        }
        applications = set(re.findall(r":::([A-Za-z][\w-]*)", body))
        if not definitions or not applications or not applications.issubset(definitions):
            errors.append(f"{companion}: {name} diagram lacks matching defined, colored, and applied semantic classes")
        if not re.search(r"^Legend\s*:", body, re.M):
            errors.append(f"{companion}: {name} section lacks an explicit Legend")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("ticket", type=Path)
    args = parser.parse_args()
    errors = validate(args.ticket)
    if errors:
        print("\n".join(errors))
        return 1
    print(f"visual companion OK: {args.ticket.with_name('diagrams.md')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
