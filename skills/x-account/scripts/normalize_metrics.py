#!/usr/bin/env python3
"""Normalize X metrics exports into Farplane KPI observations."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


FIELD_MAP = {
    "x_followers": ["x_followers", "followers", "followers_count", "follower_count"],
    "x_views": ["x_views", "views", "impressions", "impression_count"],
    "x_likes": ["x_likes", "likes", "like_count", "favorites"],
}


def read_source(path: Path) -> dict[str, Any]:
    if path.suffix.lower() == ".json":
        raw = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            return raw
        raise ValueError("JSON source must be an object")
    if path.suffix.lower() == ".csv":
        with path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        if not rows:
            return {}
        return {key: value for row in rows for key, value in row.items()}
    raise ValueError("source must be .json or .csv")


def value_for(raw: dict[str, Any], names: list[str]) -> float | None:
    lowered = {str(key).lower(): value for key, value in raw.items()}
    for name in names:
        value = lowered.get(name.lower())
        if value in (None, ""):
            continue
        try:
            return float(str(value).replace(",", ""))
        except ValueError:
            continue
    return None


def normalize(source: Path, date: str) -> dict[str, Any]:
    raw = read_source(source)
    observations = []
    for metric_id, names in FIELD_MAP.items():
        value = value_for(raw, names)
        if value is None:
            continue
        observations.append({"metric_id": metric_id, "date": date, "value": value, "status": "available"})
    status = "available" if observations else "source_gap"
    return {
        "source_id": "manual_x_account",
        "date": date,
        "status": status,
        "observations": observations,
        "gaps": [] if observations else ["no_supported_x_metric_fields"],
        "source_file": str(source),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--out", default=".farplane/metrics/manual/x_account.json")
    args = parser.parse_args()
    payload = normalize(Path(args.source), args.date)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "out": str(out), "status": payload["status"], "observations": len(payload["observations"])}, indent=2, sort_keys=True))
    return 0 if payload["status"] == "available" else 1


if __name__ == "__main__":
    raise SystemExit(main())
