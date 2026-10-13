#!/usr/bin/env python3
"""Keep closeout demo videos on a repo's `demos` pre-release and stitch them into a release reel.

upload <issue> <mp4>   puts the video on the shelf as issue-<n>.mp4 and prints the
                       `🎬 Demo: <url>` line that leads the closing proof comment.
reel [--since <tag>]   joins the demos of issues closed since that release (default:
                       the latest published release) in closing order, into one MP4.

The fixed `demos` tag keeps every download link stable; a draft release's links
change when it is published.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

SHELF_TAG = "demos"
ASSET = re.compile(r"^issue-(\d+)\.mp4$")
DEMO_PREFIX = "🎬 Demo: "


def asset_name(issue: int) -> str:
    return f"issue-{issue}.mp4"


def demo_url(repo: str, issue: int) -> str:
    return f"https://github.com/{repo}/releases/download/{SHELF_TAG}/{asset_name(issue)}"


def demo_line(repo: str, issue: int) -> str:
    return DEMO_PREFIX + demo_url(repo, issue)


def shelf_issues(asset_names: list[str]) -> set[int]:
    """Issue numbers that have a demo on the shelf."""
    return {int(m.group(1)) for name in asset_names if (m := ASSET.match(name))}


def pick(issues: list[dict], on_shelf: set[int], since: str | None) -> list[dict]:
    """Closed issues with a demo, closed after `since` (ISO time), oldest close first."""
    chosen = [i for i in issues if i["number"] in on_shelf and i.get("closedAt") and (since is None or i["closedAt"] > since)]
    return sorted(chosen, key=lambda i: i["closedAt"])


def gh(*args: str) -> str:
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout


def resolve_repo(repo: str | None) -> str:
    return repo or gh("repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner").strip()


def ensure_shelf(repo: str) -> None:
    try:
        gh("release", "view", SHELF_TAG, "-R", repo, "--json", "tagName")
    except subprocess.CalledProcessError:
        gh("release", "create", SHELF_TAG, "-R", repo, "--prerelease", "--title", "Feature demos",
           "--notes", "Closeout demo videos, one per feature issue (issue-<n>.mp4). Not a release; the reel for each release is built from these.")


def upload(repo: str, issue: int, video: Path) -> str:
    if not video.is_file():
        raise SystemExit(f"No such video: {video}")
    ensure_shelf(repo)
    with tempfile.TemporaryDirectory() as tmp:
        named = Path(tmp) / asset_name(issue)
        shutil.copyfile(video, named)
        gh("release", "upload", SHELF_TAG, str(named), "-R", repo, "--clobber")
    return demo_line(repo, issue)


def since_time(repo: str, tag: str | None) -> tuple[str | None, str]:
    """When the given (or latest published) release came out, and its name for messages."""
    if tag:
        return json.loads(gh("release", "view", tag, "-R", repo, "--json", "publishedAt"))["publishedAt"], tag
    latest = json.loads(gh("release", "list", "-R", repo, "--exclude-drafts", "--exclude-pre-releases", "--limit", "1", "--json", "tagName,publishedAt"))
    return (latest[0]["publishedAt"], latest[0]["tagName"]) if latest else (None, "the start")


def normalise(src: Path, dst: Path) -> None:
    """Same size, rate and audio layout for every clip, so the concat can copy streams."""
    has_audio = bool(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", str(src)], capture_output=True, text=True).stdout.strip())
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(src)]
    if not has_audio:
        cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000", "-shortest"]
    cmd += ["-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30,format=yuv420p",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-ar", "48000", "-ac", "2", str(dst)]
    subprocess.run(cmd, check=True)


def reel(repo: str, tag: str | None, out: Path | None) -> Path:
    since, label = since_time(repo, tag)
    assets = json.loads(gh("release", "view", SHELF_TAG, "-R", repo, "--json", "assets"))["assets"]
    closed = json.loads(gh("issue", "list", "-R", repo, "--state", "closed", "--limit", "1000", "--json", "number,title,closedAt"))
    chosen = pick(closed, shelf_issues([a["name"] for a in assets]), since)
    if not chosen:
        raise SystemExit(f"No demos for issues closed since {label}.")
    root = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() or ".")
    out = out or root / ".farplane" / "demo-shelf" / f"reel-{date.today().isoformat()}.mp4"
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        parts = []
        for i in chosen:
            gh("release", "download", SHELF_TAG, "-R", repo, "-p", asset_name(i["number"]), "-D", tmp, "--clobber")
            part = Path(tmp) / f"part-{len(parts):03d}.mp4"
            normalise(Path(tmp) / asset_name(i["number"]), part)
            parts.append(part)
        listing = Path(tmp) / "parts.txt"
        listing.write_text("".join(f"file '{p}'\n" for p in parts))
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy", "-movflags", "+faststart", str(out)], check=True)
    for i in chosen:
        print(f"#{i['number']} {i['title']}")
    print(f"Reel of {len(chosen)} demos since {label}: {out}")
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--repo", help="owner/name; default: this checkout's GitHub repo")
    sub = p.add_subparsers(dest="cmd", required=True)
    up = sub.add_parser("upload", help="put a closeout video on the shelf and print its 🎬 Demo line")
    up.add_argument("issue", type=int)
    up.add_argument("video", type=Path)
    rl = sub.add_parser("reel", help="join the demos of issues closed since a release")
    rl.add_argument("--since", help="release tag; default: the latest published release")
    rl.add_argument("--out", type=Path)
    a = p.parse_args(argv)
    repo = resolve_repo(a.repo)
    if a.cmd == "upload":
        print(upload(repo, a.issue, a.video))
    else:
        reel(repo, a.since, a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
