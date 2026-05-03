#!/usr/bin/env python3
"""Parse METRIC lines from autoresearch command output."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path


METRIC_RE = re.compile(r"^METRIC\s+([\w.µ-]+)=(-?(?:\d+(?:\.\d*)?|\.\d+))\s*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metric-name", required=True)
    parser.add_argument("--file", help="Read output from file instead of stdin")
    parser.add_argument("--allow-number", action="store_true", help="Accept one bare numeric final line")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of the primary value")
    return parser.parse_args()


def read_text(path: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()


def parse_metrics(text: str) -> dict[str, float]:
    metrics: dict[str, float] = {}
    for line in text.splitlines():
        match = METRIC_RE.match(line.strip())
        if not match:
            continue
        name, value_text = match.groups()
        value = float(value_text)
        if math.isfinite(value):
            metrics[name] = value
    return metrics


def parse_bare_number(text: str) -> float | None:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) != 1:
        return None
    try:
        value = float(lines[0])
    except ValueError:
        return None
    return value if math.isfinite(value) else None


def main() -> int:
    args = parse_args()
    text = read_text(args.file)
    metrics = parse_metrics(text)

    if args.metric_name not in metrics and args.allow_number:
        value = parse_bare_number(text)
        if value is not None:
            metrics[args.metric_name] = value

    if args.metric_name not in metrics:
        print(f"Metric {args.metric_name!r} not found in output", file=sys.stderr)
        return 2

    result = {
        "metric_name": args.metric_name,
        "value": metrics[args.metric_name],
        "metrics": metrics,
    }
    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        print(result["value"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

