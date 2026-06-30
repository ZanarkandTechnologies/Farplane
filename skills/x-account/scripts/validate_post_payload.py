#!/usr/bin/env python3
"""Validate an X post/thread payload without mutating account state."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


DEFAULT_LIMIT = 280


def load_payload(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("payload must be a JSON object")
    return raw


def tweets_from(payload: dict[str, Any]) -> list[str]:
    if isinstance(payload.get("text"), str):
        return [payload["text"]]
    raw_tweets = payload.get("tweets")
    if isinstance(raw_tweets, list):
        tweets = []
        for item in raw_tweets:
            if isinstance(item, str):
                tweets.append(item)
            elif isinstance(item, dict) and isinstance(item.get("text"), str):
                tweets.append(item["text"])
        return tweets
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--payload", required=True)
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    args = parser.parse_args()
    payload = load_payload(Path(args.payload))
    tweets = tweets_from(payload)
    issues = []
    warnings = []
    if not tweets:
        issues.append("missing_text_or_tweets")
    for index, tweet in enumerate(tweets, start=1):
        if len(tweet) > args.limit:
            issues.append(f"tweet_{index}_over_limit:{len(tweet)}>{args.limit}")
        if not tweet.strip():
            issues.append(f"tweet_{index}_empty")
        if len(tweet.splitlines()) > 12:
            warnings.append(f"tweet_{index}_many_line_breaks")
    result = {"ok": not issues, "tweet_count": len(tweets), "issues": issues, "warnings": warnings, "mutated": False}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
