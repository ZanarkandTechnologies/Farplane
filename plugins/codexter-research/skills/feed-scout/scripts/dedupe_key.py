#!/usr/bin/env python3
"""Compute stable canonical URLs and dedupe keys for feed-scout content."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


TRACKING_PREFIXES = ("utm_",)
TRACKING_PARAMS = {
    "fbclid",
    "gclid",
    "mc_cid",
    "mc_eid",
    "ref",
    "source",
}


@dataclass(frozen=True)
class DedupeResult:
    canonical_url: str
    canonical_key: str


def _clean_netloc(netloc: str) -> str:
    netloc = netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    if netloc == "twitter.com":
        return "x.com"
    if netloc == "youtu.be":
        return "youtube.com"
    return netloc


def _keep_query_param(name: str) -> bool:
    lower = name.lower()
    if lower in TRACKING_PARAMS:
        return False
    return not any(lower.startswith(prefix) for prefix in TRACKING_PREFIXES)


def canonicalize_url(url: str) -> str:
    parsed = urlparse(url.strip())
    if not parsed.scheme:
        parsed = urlparse(f"https://{url.strip()}")

    scheme = "https"
    netloc = _clean_netloc(parsed.netloc)
    path = re.sub(r"/+", "/", parsed.path or "/")
    if path != "/":
        path = path.rstrip("/")

    query_pairs = [
        (key, value)
        for key, value in parse_qsl(parsed.query, keep_blank_values=False)
        if _keep_query_param(key)
    ]

    if netloc == "youtube.com" and parsed.netloc.lower() == "youtu.be":
        video_id = parsed.path.strip("/")
        path = "/watch"
        query_pairs = [("v", video_id)] if video_id else query_pairs

    query = urlencode(sorted(query_pairs))
    return urlunparse((scheme, netloc, path, "", query, ""))


def dedupe_key(url: str, title: str | None = None) -> DedupeResult:
    canonical_url = canonicalize_url(url)
    parsed = urlparse(canonical_url)
    host = parsed.netloc
    path = parsed.path.strip("/")
    query = dict(parse_qsl(parsed.query))

    if host == "youtube.com" and parsed.path == "/watch" and query.get("v"):
        key = f"youtube-video-{query['v'].lower()}"
    elif host == "x.com":
        parts = [part for part in path.split("/") if part]
        if len(parts) >= 3 and parts[1] == "status":
            key = f"x-status-{parts[0].lower()}-{parts[2].lower()}"
        else:
            key = "x-" + "-".join(parts).lower()
    else:
        base = f"{host}-{path}".strip("-")
        key = base.lower()

    if not key and title:
        key = title.lower()

    key = re.sub(r"[^a-z0-9]+", "-", key).strip("-")
    return DedupeResult(canonical_url=canonical_url, canonical_key=key or "unknown")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    parser.add_argument("--title", default=None)
    args = parser.parse_args()

    result = dedupe_key(args.url, args.title)
    print(result.canonical_key)
    print(result.canonical_url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
