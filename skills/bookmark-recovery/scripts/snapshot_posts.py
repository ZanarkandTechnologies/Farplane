#!/usr/bin/env python3
"""Render X posts to PNG reminders through X's public embed page (no login, no API, no visible window)."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path

EMBED = "https://platform.twitter.com/embed/Tweet.html?id={id}&theme=dark&dnt=true"


def headless_chrome() -> str:
    configured = os.environ.get("FARPLANE_HEADLESS_CHROME")
    candidate = Path(configured) if configured else Path.home() / ".farplane/browsers/chrome-headless-shell/chrome-headless-shell"
    if not candidate.is_file():
        raise SystemExit(f"headless Chrome not found at {candidate}; set FARPLANE_HEADLESS_CHROME")
    return str(candidate)


def trim(path: Path) -> None:
    from PIL import Image, ImageChops

    image = Image.open(path).convert("RGB")
    background = Image.new("RGB", image.size, image.getpixel((image.width - 1, image.height - 1)))
    box = ImageChops.difference(image, background).getbbox()
    if box:
        image.crop((0, 0, image.width, min(image.height, box[3] + 8))).save(path)


def snapshot(post_id: str, out: Path, chrome: str) -> bool:
    with tempfile.TemporaryDirectory() as profile:
        try:
            subprocess.run(
                [chrome, "--disable-gpu", "--hide-scrollbars", "--window-size=560,1400",
                 "--virtual-time-budget=10000", f"--user-data-dir={profile}",
                 f"--screenshot={out}", EMBED.format(id=post_id)],
                capture_output=True, timeout=60, check=False,
            )
        except subprocess.TimeoutExpired:
            return False
    if not out.is_file() or out.stat().st_size < 5_000:
        return False
    trim(out)
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", type=Path, required=True, help="x.sources.json from a frozen run")
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--ids", nargs="*", help="limit to these post IDs")
    args = parser.parse_args()
    items = json.loads(args.cache.read_text(encoding="utf-8"))["items"]
    wanted = set(args.ids or [item["source_id"] for item in items])
    chrome = headless_chrome()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    results = {}
    for item in items:
        if item["source_id"] in wanted:
            out = args.out_dir / f"{item['source_id']}.png"
            results[item["canonical_key"]] = str(out) if out.is_file() or snapshot(item["source_id"], out, chrome) else None
    print(json.dumps({"snapshots": results, "missing": [key for key, path in results.items() if not path]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
