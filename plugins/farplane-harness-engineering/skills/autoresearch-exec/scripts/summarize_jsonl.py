#!/usr/bin/env python3
"""Summarize an autoresearch JSONL run log."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", nargs="?", default="autoresearch.jsonl")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def load_entries(path: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    if not path.exists():
        return entries
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            entries.append(value)
    return entries


def is_better(value: float, current: float, direction: str) -> bool:
    return value < current if direction == "lower" else value > current


def summarize(entries: list[dict[str, Any]]) -> dict[str, Any]:
    config = next((entry for entry in entries if entry.get("type") == "config"), {})
    direction = config.get("direction") if config.get("direction") in {"lower", "higher"} else "lower"
    runs = [entry for entry in entries if entry.get("type") == "run"]
    counts = Counter(str(run.get("status", "unknown")) for run in runs)

    baseline = next((run for run in runs if run.get("status") == "baseline"), runs[0] if runs else None)
    kept = [run for run in runs if run.get("status") in {"baseline", "keep"} and isinstance(run.get("metric"), (int, float))]
    best = None
    for run in kept:
        if best is None or is_better(float(run["metric"]), float(best["metric"]), direction):
            best = run

    return {
        "goal": config.get("goal"),
        "metric_name": config.get("metric_name", "metric"),
        "direction": direction,
        "run_count": len(runs),
        "counts": dict(sorted(counts.items())),
        "baseline": baseline,
        "best": best,
        "last": runs[-1] if runs else None,
    }


def print_text(summary: dict[str, Any]) -> None:
    print(f"Goal: {summary.get('goal') or '-'}")
    print(f"Metric: {summary['metric_name']} ({summary['direction']} is better)")
    print(f"Runs: {summary['run_count']} {summary['counts']}")
    baseline = summary.get("baseline")
    best = summary.get("best")
    last = summary.get("last")
    if baseline:
        print(f"Baseline: #{baseline.get('run')} {baseline.get('metric')} ({baseline.get('status')})")
    if best:
        print(f"Best: #{best.get('run')} {best.get('metric')} ({best.get('description')})")
    if last:
        print(f"Last: #{last.get('run')} {last.get('metric')} ({last.get('status')}) {last.get('description', '')}")


def main() -> int:
    args = parse_args()
    summary = summarize(load_entries(Path(args.jsonl)))
    if args.json:
        print(json.dumps(summary, sort_keys=True))
    else:
        print_text(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

