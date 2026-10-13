#!/usr/bin/env python3
"""Text or transcript for any URL or media file, the whole summarize-first route in one command.

1. `farplane run -- summarize SOURCE --extract`.
2. If that came back as a login wall, a mirror's notice page, or next to nothing (Instagram answers a
   reel with the single word "Instagram"; X links can come back as Nitter's takedown notice),
   download the media with yt-dlp, trying the operator's browsers' cookies when a plain download
   is refused.
3. `farplane run -- summarize <downloaded file> --extract --timestamps`.

Prints the text on stdout and the route taken on stderr; exits 1 with the reason when every step fails.
The steps are the ones the intelligest todo lists; this keeps any of them from being
skipped.

    python3 skills/intelligest/scripts/extract_source.py "https://www.instagram.com/reel/…"
    python3 skills/intelligest/scripts/extract_source.py ./clip.mp4 --workdir /tmp/clip
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

# Fewer words than this after the stats line is dropped means the page held no real content.
MIN_WORDS = 40
# What a login wall's whole extraction looks like.
WALL = re.compile(r"^\s*(instagram|tiktok\b.*|log ?in\b.*|sign ?in\b.*|facebook|x|twitter)\s*$", re.I)
# A mirror's own notice standing in for the post: X links come back as Nitter's takedown page.
STAND_IN = re.compile(r"\bnitter\b.{0,600}\b(cease and desist|legal counsel|instance)", re.I | re.S)
BROWSERS = ["brave", "chrome", "safari", "firefox", "edge", "chromium", "arc"]


def summarize(source: str, timestamps: bool = False) -> tuple[int, str]:
    cmd = ["farplane", "run", "--", "summarize", source, "--extract"]
    if timestamps:
        cmd.append("--timestamps")
    run = subprocess.run(cmd, capture_output=True, text=True)
    return run.returncode, run.stdout.strip()


def body(text: str) -> str:
    """The extraction without summarize's closing stats line ("36s · markdown via readability")."""
    lines = [l for l in text.splitlines() if l.strip()]
    if lines and re.search(r"\d+s · ", lines[-1]):
        lines = lines[:-1]
    return "\n".join(lines).strip()


def thin(text: str) -> bool:
    b = body(text)
    return not b or bool(WALL.match(b)) or bool(STAND_IN.search(b)) or len(b.split()) < MIN_WORDS


def download(url: str, workdir: Path) -> Path | None:
    out = str(workdir / "source.%(ext)s")
    for cookies in [None, *BROWSERS]:
        cmd = ["yt-dlp", "-q", "--no-warnings", "-o", out]
        if cookies:
            cmd += ["--cookies-from-browser", cookies]
        if subprocess.run([*cmd, url], capture_output=True, text=True).returncode == 0:
            files = [p for p in workdir.glob("source.*") if p.suffix not in {".part", ".ytdl"}]
            if files:
                print(f"route: yt-dlp{' with ' + cookies + ' cookies' if cookies else ''} -> {files[0]}", file=sys.stderr)
                return files[0]
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("source", help="URL or local media/text file")
    ap.add_argument("--workdir", help="where a download goes (default: a temp folder)")
    args = ap.parse_args()

    local = Path(args.source).expanduser()
    if local.exists():
        code, text = summarize(str(local), timestamps=True)
        if code == 0 and body(text):
            print("route: summarize file", file=sys.stderr)
            print(text)
            return 0
        print(f"blocked: summarize could not read {local} (exit {code})", file=sys.stderr)
        return 1

    code, text = summarize(args.source)
    if code == 0 and not thin(text):
        print("route: summarize url", file=sys.stderr)
        print(text)
        return 0
    print(f"summarize url gave {'a login wall or too little' if code == 0 else f'exit {code}'}; downloading", file=sys.stderr)

    workdir = Path(args.workdir) if args.workdir else Path(tempfile.mkdtemp(prefix="extract-"))
    workdir.mkdir(parents=True, exist_ok=True)
    media = download(args.source, workdir)
    if not media:
        # Nothing to download: a short page that is not a login wall is still the page's text.
        if code == 0 and body(text) and not WALL.match(body(text)) and not STAND_IN.search(body(text)):
            print("route: summarize url (a short page; no media to download)", file=sys.stderr)
            print(text)
            return 0
        print("blocked: yt-dlp could not fetch it, with or without browser cookies", file=sys.stderr)
        return 1
    code, text = summarize(str(media), timestamps=True)
    if code == 0 and body(text):
        print("route: summarize downloaded file", file=sys.stderr)
        print(text)
        return 0
    print(f"blocked: summarize could not transcribe {media} (exit {code}); a missing transcriber is a setup blocker", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
