#!/usr/bin/env python3
"""Validate an optional separate visual companion for an impl-plan ticket."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


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
    linked = has_companion_link(ticket_text)
    exists = companion.is_file()
    if not linked and not exists:
        return []
    if linked and not exists:
        return [f"{companion}: linked companion does not exist"]
    if exists and not linked:
        return [f"{companion}: orphaned companion is not linked from ticket.md"]

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
    print(f"optional visual companion OK: {args.ticket}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
