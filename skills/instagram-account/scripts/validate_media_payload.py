#!/usr/bin/env python3
"""Validate an Instagram post/reel/carousel payload without mutating account state."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


CAPTION_LIMIT = 2200


def load_payload(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("payload must be a JSON object")
    return raw


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--payload", required=True)
    args = parser.parse_args()
    payload = load_payload(Path(args.payload))
    caption = payload.get("caption")
    media = payload.get("media") or payload.get("media_items")
    media_type = payload.get("media_type") or payload.get("type")
    issues = []
    warnings = []
    if not isinstance(caption, str) or not caption.strip():
        issues.append("missing_caption")
    elif len(caption) > CAPTION_LIMIT:
        issues.append(f"caption_over_limit:{len(caption)}>{CAPTION_LIMIT}")
    if media is None:
        issues.append("missing_media")
    if media_type and str(media_type).lower() not in {"image", "video", "carousel", "reel"}:
        warnings.append(f"unknown_media_type:{media_type}")
    if isinstance(media, list) and len(media) > 10:
        issues.append("carousel_over_limit:more_than_10_items")
    result = {"ok": not issues, "issues": issues, "warnings": warnings, "mutated": False}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
