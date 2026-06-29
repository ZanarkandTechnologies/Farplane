#!/usr/bin/env python3
"""Check Taste Loop progress.md uses hypothesis cycles after opt-in."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_FIELDS = [
    "phase:",
    "current_hypothesis:",
    "planned_attempt:",
    "artifact_refs:",
    "human_question:",
    "expected_signal:",
    "skill_delta_candidate:",
    "human_signal:",
    "learning:",
    "next_hypothesis:",
    "promotion_decision:",
]

FORBIDDEN = [
    r"(?m)^\s*experiment:\s*$",
    r"(?m)^\s*id:\s*TL-EXP-\d+\s*$",
    r"(?m)^\s*-\s*`(?:feedback_request_for|reminder_for):`\s*`?TL-EXP-\d+`?",
    r"(?m)^\s*-\s*`worker_title:`.*TL-EXP-\d+",
]

START_MARKERS = [
    "progress_unit = hypothesis_cycle",
    "`progress_unit = hypothesis_cycle`",
    "hypothesis ledger",
    "hypothesis cycles instead of",
]


def opted_in(program: str) -> bool:
    return bool(re.search(r"(?m)^\s*progress_unit\s*=\s*hypothesis_cycle\s*$", program))


def entries_after_marker(progress: str) -> list[tuple[int, str]]:
    parts = list(re.finditer(r"(?m)^##\s+.*$", progress))
    if not parts:
        return []

    entries: list[tuple[int, str]] = []
    for i, heading in enumerate(parts):
        end = parts[i + 1].start() if i + 1 < len(parts) else len(progress)
        line = progress[: heading.start()].count("\n") + 1
        entries.append((line, progress[heading.start() : end]))

    for i, (_, body) in enumerate(entries):
        if any(marker in body for marker in START_MARKERS):
            return entries[i:]
    return entries


def check_entry(line: int, body: str) -> list[str]:
    errors: list[str] = []

    for pattern in FORBIDDEN:
        if re.search(pattern, body):
            errors.append(
                f"line {line}: use `hypothesis_cycle`, not a fresh TL-EXP primary work unit"
            )

    if re.search(r"(?m)^\s*hypothesis_cycle:\s*$", body):
        for field in REQUIRED_FIELDS:
            if field not in body:
                errors.append(f"line {line}: hypothesis_cycle missing `{field}`")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("program", type=Path)
    parser.add_argument("progress", type=Path)
    args = parser.parse_args()

    program = args.program.read_text()
    progress = args.progress.read_text()
    if not opted_in(program):
        print("taste-loop progress hypothesis cycles skipped")
        return 0

    errors: list[str] = []
    for line, body in entries_after_marker(progress):
        errors.extend(check_entry(line, body))

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print("taste-loop progress hypothesis cycles OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
