#!/usr/bin/env python3
"""Fetch authenticated X bookmarks into a bounded, redacted collection cache."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import quote

from fetch_metrics import api_get, bearer_header, oauth2_header, resolve_user
from runtime_env import load_runtime_values, refresh_oauth2_access_token


def fetch_bookmarks(max_pages: int = 10) -> dict[str, Any]:
    values = load_runtime_values()
    auth = oauth2_header(values)
    if not auth:
        raise RuntimeError("FARPLANE_X_OAUTH2_ACCESS_TOKEN is required for bookmark reads")
    try:
        user_id, user_payload, endpoints = resolve_user(values, auth)
    except HTTPError as error:
        # User access tokens expire after about two hours; refresh once and retry.
        if error.code != 401:
            raise
        auth = bearer_header(refresh_oauth2_access_token(values))
        user_id, user_payload, endpoints = resolve_user(values, auth)
    username = str((user_payload.get("data") or {}).get("username") or "").lstrip("@")
    items: list[dict[str, Any]] = []
    token: str | None = None
    pages = 0
    while pages < max_pages:
        params = {
            "max_results": "100",
            "tweet.fields": "author_id,created_at,entities,lang,public_metrics,attachments",
            "expansions": "author_id,attachments.media_keys",
            "user.fields": "username,name",
            "media.fields": "type,url,preview_image_url,alt_text,width,height,duration_ms",
        }
        if token:
            params["pagination_token"] = token
        payload = api_get(f"/users/{quote(user_id)}/bookmarks", auth, params)
        pages += 1
        includes = payload.get("includes") or {}
        users = {str(row.get("id")): row for row in includes.get("users") or []}
        for post in payload.get("data") or []:
            post_id = str(post.get("id") or "")
            author = users.get(str(post.get("author_id") or ""), {})
            handle = str(author.get("username") or "")
            items.append({
                "canonical_key": f"x:{post_id}",
                "source": "x",
                "source_id": post_id,
                "url": f"https://x.com/{handle or 'i/web'}/status/{post_id}",
                "author": {"id": post.get("author_id"), "username": handle or None, "name": author.get("name")},
                "text": post.get("text"),
                "published_at": post.get("created_at"),
                "bookmark_saved_at": None,
                "attachments": post.get("attachments"),
                "public_metrics": post.get("public_metrics"),
            })
        token = str((payload.get("meta") or {}).get("next_token") or "") or None
        if not token:
            break
    return {
        "schema_version": 1,
        "source": "x",
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "coverage": {
            "status": "partial" if token else ("complete" if items else "empty"),
            "pages": pages,
            "item_count": len(items),
            "next_token_present": bool(token),
            "limitation": "max_pages reached before pagination completed" if token else "X does not expose bookmark-save timestamps",
        },
        "account": {"id": user_id, "username": username or None},
        "endpoints": [*endpoints, "/2/users/:id/bookmarks"],
        "items": items,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-pages", type=int, default=10)
    args = parser.parse_args()
    if args.max_pages < 1 or args.max_pages > 100:
        parser.error("--max-pages must be between 1 and 100")
    payload = fetch_bookmarks(args.max_pages)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "coverage": payload["coverage"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
