#!/usr/bin/env python3
"""Append idempotent bookmark observations and reduce them by canonical key."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def latest_by_key(rows: list[dict]) -> dict[str, dict]:
    latest: dict[str, dict] = {}
    for row in rows:
        key = row.get("canonical_key")
        if isinstance(key, str) and key:
            latest[key] = row
    return latest


def observation_rows(inbox: dict, existing: list[dict]) -> list[dict]:
    latest = latest_by_key(existing)
    seen_run_keys = {
        (row.get("run_id"), row.get("canonical_key"))
        for row in existing
        if row.get("run_id") and row.get("canonical_key")
    }
    output: list[dict] = []
    for disposition, field in (("candidate", "candidates"), ("duplicate", "duplicates"), ("excluded", "excluded")):
        for item in inbox.get(field) or []:
            key = item["canonical_key"]
            if (inbox["run_id"], key) in seen_run_keys:
                continue
            prior = latest.get(key) or {}
            output.append({
                "canonical_key": key,
                "source": item["source"],
                "first_seen": prior.get("first_seen") or inbox["generated_at"],
                "last_seen": inbox["generated_at"],
                "run_id": inbox["run_id"],
                "disposition": disposition,
                "canonical_ref": item.get("canonical_ref") or prior.get("canonical_ref"),
            })
    return output


def append_observations(inbox_path: Path, ledger_path: Path) -> dict:
    inbox = json.loads(inbox_path.read_text(encoding="utf-8"))
    existing = read_rows(ledger_path)
    additions = observation_rows(inbox, existing)
    if additions:
        ledger_path.parent.mkdir(parents=True, exist_ok=True)
        with ledger_path.open("a", encoding="utf-8") as handle:
            for row in additions:
                handle.write(json.dumps(row, sort_keys=True) + "\n")
    reduced = latest_by_key([*existing, *additions])
    return {"appended": len(additions), "canonical_keys": len(reduced)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inbox", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(append_observations(args.inbox, args.ledger)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
