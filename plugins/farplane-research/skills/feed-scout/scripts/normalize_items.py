#!/usr/bin/env python3
"""Normalize fixture-shaped discovery output into feed-scout ContentItem rows."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from dedupe_key import dedupe_key  # noqa: E402


ALLOWED_KINDS = {"post", "thread", "video", "short", "article"}


def _text_for_hash(raw: dict[str, Any]) -> str:
    parts = [
        str(raw.get("url", "")),
        str(raw.get("title", "")),
        str(raw.get("text", "")),
        str(raw.get("description", "")),
        str(raw.get("summary", "")),
    ]
    return "\n".join(parts)


def normalize(raw: dict[str, Any], discovered_at: str) -> dict[str, Any]:
    url = raw.get("canonical_url") or raw.get("url")
    if not isinstance(url, str) or not url.strip():
        raise ValueError("raw item requires url or canonical_url")

    result = dedupe_key(url, raw.get("title"))
    kind = raw.get("kind")
    if kind not in ALLOWED_KINDS:
        raise ValueError(f"invalid kind {kind!r}")

    profile_id = raw.get("profile_id")
    if not isinstance(profile_id, str) or not profile_id:
        raise ValueError("raw item requires profile_id")

    platform = raw.get("platform")
    if not isinstance(platform, str) or not platform:
        raise ValueError("raw item requires platform")

    title = raw.get("title") or raw.get("text") or result.canonical_url
    author = raw.get("author") or raw.get("channel") or raw.get("profile_id") or "unknown"
    published_at = raw.get("published_at") or raw.get("created_at") or discovered_at

    content_hash = hashlib.sha256(_text_for_hash(raw).encode("utf-8")).hexdigest()

    normalized = {
        "profile_id": profile_id,
        "platform": platform,
        "kind": kind,
        "canonical_url": result.canonical_url,
        "canonical_key": result.canonical_key,
        "title": str(title),
        "author": str(author),
        "published_at": str(published_at),
        "discovered_at": discovered_at,
        "content_hash": content_hash,
        "status": raw.get("status", "new"),
    }

    native_id = raw.get("native_id")
    if isinstance(native_id, str) and native_id:
        normalized["native_id"] = native_id

    return normalized


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--discovered-at", default=None)
    args = parser.parse_args()

    discovered_at = args.discovered_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    with args.path.open() as handle:
        for line_no, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                raw = json.loads(stripped)
                item = normalize(raw, discovered_at)
            except (json.JSONDecodeError, ValueError) as exc:
                print(f"line {line_no}: {exc}", file=sys.stderr)
                return 1
            print(json.dumps(item, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
