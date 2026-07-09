#!/usr/bin/env python3
"""Optional Shazam-style music recognition for media-ingest snippets."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any


def _maybe_reexec_stable_python() -> None:
    """Avoid importing shazamio under Python versions known to crash locally."""
    if os.environ.get("FARPLANE_SHAZAMIO_REEXEC") == "1":
        return

    candidates = [
        Path.home() / ".codex/.venvs/shazamio/bin/python",
        Path.cwd() / ".farplane/tools/shazamio-venv/bin/python",
    ]
    for candidate in candidates:
        if candidate.exists() and candidate != Path(sys.executable):
            os.environ["FARPLANE_SHAZAMIO_REEXEC"] = "1"
            os.execv(str(candidate), [str(candidate), __file__, *sys.argv[1:]])


def _compact_track(track: dict[str, Any] | None) -> dict[str, Any]:
    if not track:
        return {
            "status": "no_match",
            "title": None,
            "artist": None,
            "album": None,
            "shazam_url": None,
            "confidence": None,
            "raw_track": None,
        }

    sections = track.get("sections") or []
    metadata = {}
    for section in sections:
        for item in section.get("metadata") or []:
            title = item.get("title")
            text = item.get("text")
            if title and text:
                metadata[str(title).lower()] = text

    return {
        "status": "matched",
        "title": track.get("title"),
        "artist": track.get("subtitle"),
        "album": metadata.get("album"),
        "shazam_url": (track.get("share") or {}).get("href"),
        "confidence": track.get("score"),
        "raw_track": {
            "key": track.get("key"),
            "title": track.get("title"),
            "subtitle": track.get("subtitle"),
            "share": track.get("share"),
            "sections": sections[:2],
        },
    }


async def _recognize(path: Path) -> dict[str, Any]:
    try:
        from shazamio import Shazam
    except Exception as exc:  # pragma: no cover - depends on local optional dep
        return {
            "status": "missing_dependency",
            "error": f"Install optional dependency: python3 -m pip install --user shazamio ({exc})",
        }

    shazam = Shazam()
    result = await shazam.recognize(str(path))
    return _compact_track(result.get("track"))


def main() -> int:
    _maybe_reexec_stable_python()

    parser = argparse.ArgumentParser(
        description="Recognize a music track from an audio snippet using shazamio."
    )
    parser.add_argument("audio_file", help="Path to an audio snippet, e.g. WAV/MP3/M4A.")
    parser.add_argument("--json", action="store_true", help="Emit JSON output.")
    args = parser.parse_args()

    path = Path(args.audio_file).expanduser()
    if not path.exists():
        payload = {"status": "error", "error": f"Audio file not found: {path}"}
    else:
        payload = asyncio.run(_recognize(path))

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        if payload.get("status") == "matched":
            print(f"{payload.get('artist')} - {payload.get('title')}")
            if payload.get("shazam_url"):
                print(payload["shazam_url"])
        else:
            print(json.dumps(payload, indent=2, sort_keys=True))

    return 0 if payload.get("status") in {"matched", "no_match"} else 1


if __name__ == "__main__":
    sys.exit(main())
