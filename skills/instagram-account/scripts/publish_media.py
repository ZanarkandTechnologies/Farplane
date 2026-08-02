#!/usr/bin/env python3
"""Publish an approved Instagram image, carousel, or Reel payload."""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from runtime_env import env_value, load_runtime_values

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bin.core.farplane_content import add_content_row

DEFAULT_KPIS = ["instagram_views", "instagram_likes", "evidence_distribution_reach"]
CAPTION_LIMIT = 2200


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_payload(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("payload must be a JSON object")
    return raw


def graph_base(version: str) -> str:
    normalized = version if version.startswith("v") else f"v{version}"
    return f"https://graph.instagram.com/{normalized}"


def graph_post(version: str, path: str, token: str, params: dict[str, Any]) -> dict[str, Any]:
    body = dict(params)
    body["access_token"] = token
    request = Request(
        f"{graph_base(version)}{path}",
        data=urlencode(body, doseq=True).encode("utf-8"),
        method="POST",
        headers={"User-Agent": "Farplane instagram-account publisher"},
    )
    with urlopen(request, timeout=60) as response:
        raw = response.read().decode("utf-8")
    return json.loads(raw) if raw else {}


def graph_get(version: str, path: str, token: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
    query = dict(params or {})
    query["access_token"] = token
    request = Request(
        f"{graph_base(version)}{path}?{urlencode(query, doseq=True)}",
        headers={"User-Agent": "Farplane instagram-account publisher"},
    )
    with urlopen(request, timeout=60) as response:
        raw = response.read().decode("utf-8")
    return json.loads(raw) if raw else {}


def http_issue(exc: HTTPError | URLError) -> str:
    if isinstance(exc, HTTPError):
        body = exc.read().decode("utf-8", errors="replace")[:500]
        return f"http_error:{exc.code}:{body}"
    return f"url_error:{exc.reason}"


def media_items(payload: dict[str, Any]) -> list[dict[str, Any]]:
    raw = payload.get("media_items") or payload.get("media")
    if isinstance(raw, str):
        return [{"url": raw}]
    if isinstance(raw, list):
        items: list[dict[str, Any]] = []
        for item in raw:
            if isinstance(item, str):
                items.append({"url": item})
            elif isinstance(item, dict):
                items.append(item)
        return items
    if isinstance(raw, dict):
        return [raw]
    return []


def media_url(item: dict[str, Any], media_type: str) -> str | None:
    if media_type == "reel":
        return item.get("video_url") or item.get("url")
    return item.get("image_url") or item.get("url")


def validate(payload: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    caption = payload.get("caption")
    if not isinstance(caption, str) or not caption.strip():
        issues.append("missing_caption")
    elif len(caption) > CAPTION_LIMIT:
        issues.append(f"caption_over_limit:{len(caption)}>{CAPTION_LIMIT}")
    kind = str(payload.get("media_type") or payload.get("type") or "image").lower()
    items = media_items(payload)
    if kind not in {"image", "video", "carousel", "reel"}:
        issues.append(f"unsupported_media_type:{kind}")
    if not items:
        issues.append("missing_media")
    if kind == "carousel" and len(items) > 10:
        issues.append("carousel_over_limit:more_than_10_items")
    if kind == "reel" and len(items) != 1:
        issues.append("reel_requires_one_video")
    for index, item in enumerate(items, start=1):
        item_kind = str(item.get("media_type") or item.get("type") or kind).lower()
        if not media_url(item, "reel" if item_kind == "reel" else item_kind):
            issues.append(f"media_{index}_missing_url")
        if str(media_url(item, item_kind) or "").startswith("file:"):
            issues.append(f"media_{index}_must_be_public_url")
    return issues


def container_id(response: dict[str, Any]) -> str:
    identifier = response.get("id") or (response.get("data") or {}).get("id")
    if not identifier:
        raise RuntimeError("missing_container_id")
    return str(identifier)


def create_child_container(version: str, user_id: str, token: str, item: dict[str, Any], fallback_type: str) -> str:
    kind = str(item.get("media_type") or item.get("type") or fallback_type).lower()
    params: dict[str, Any] = {"is_carousel_item": "true"}
    if kind in {"video", "reel"}:
        params["media_type"] = "VIDEO"
        params["video_url"] = media_url(item, "reel")
    else:
        params["image_url"] = media_url(item, "image")
    return container_id(graph_post(version, f"/{user_id}/media", token, params))


def create_container(version: str, user_id: str, token: str, payload: dict[str, Any]) -> str:
    caption = str(payload.get("caption") or "")
    kind = str(payload.get("media_type") or payload.get("type") or "image").lower()
    items = media_items(payload)
    if kind == "carousel":
        child_ids = [create_child_container(version, user_id, token, item, "image") for item in items]
        return container_id(graph_post(version, f"/{user_id}/media", token, {"media_type": "CAROUSEL", "children": ",".join(child_ids), "caption": caption}))
    item = items[0]
    if kind == "reel":
        return container_id(graph_post(version, f"/{user_id}/media", token, {"media_type": "REELS", "video_url": media_url(item, "reel"), "caption": caption}))
    if kind == "video":
        return container_id(graph_post(version, f"/{user_id}/media", token, {"media_type": "VIDEO", "video_url": media_url(item, "video"), "caption": caption}))
    return container_id(graph_post(version, f"/{user_id}/media", token, {"image_url": media_url(item, "image"), "caption": caption}))


def wait_for_container(version: str, container: str, token: str, timeout_seconds: int) -> str:
    deadline = time.time() + timeout_seconds
    last_status = "UNKNOWN"
    while time.time() < deadline:
        payload = graph_get(version, f"/{container}", token, {"fields": "status_code"})
        last_status = str(payload.get("status_code") or last_status)
        if last_status == "FINISHED":
            return last_status
        if last_status == "ERROR":
            raise RuntimeError("container_processing_error")
        time.sleep(5)
    raise TimeoutError(f"container_processing_timeout:{last_status}")


def publish_container(version: str, user_id: str, token: str, container: str) -> str:
    response = graph_post(version, f"/{user_id}/media_publish", token, {"creation_id": container})
    media_id = response.get("id") or (response.get("data") or {}).get("id")
    if not media_id:
        raise RuntimeError("missing_media_id")
    return str(media_id)


def permalink(version: str, media_id: str, token: str) -> str | None:
    try:
        response = graph_get(version, f"/{media_id}", token, {"fields": "permalink"})
    except (HTTPError, URLError):
        return None
    value = response.get("permalink")
    return str(value) if value else None


def publish(args: argparse.Namespace) -> dict[str, Any]:
    payload = load_payload(Path(args.payload))
    issues = validate(payload)
    if issues:
        return {"ok": False, "mutated": False, "issues": issues, "redacted": True}
    runtime_values = load_runtime_values()
    token = env_value("FARPLANE_INSTAGRAM_LOGIN_ACCESS_TOKEN", runtime_values) or env_value("FARPLANE_INSTAGRAM_ACCESS_TOKEN", runtime_values)
    user_id = args.instagram_user_id or env_value("FARPLANE_INSTAGRAM_BUSINESS_ACCOUNT_ID", runtime_values) or env_value("FARPLANE_INSTAGRAM_LOGIN_USER_ID", runtime_values)
    version = args.graph_version or env_value("FARPLANE_META_GRAPH_VERSION", runtime_values) or "v21.0"
    dry_run = not args.execute
    if args.execute and not args.approval_ref:
        return {"ok": False, "mutated": False, "issues": ["missing_approval_ref"], "redacted": True}
    if args.execute and not token:
        return {"ok": False, "mutated": False, "issues": ["missing:FARPLANE_INSTAGRAM_LOGIN_ACCESS_TOKEN"], "redacted": True}
    if args.execute and not user_id:
        return {"ok": False, "mutated": False, "issues": ["missing_instagram_user_id"], "redacted": True}
    if dry_run:
        return {
            "ok": True,
            "mutated": False,
            "dry_run": True,
            "account_alias": args.account_alias,
            "media_type": str(payload.get("media_type") or payload.get("type") or "image").lower(),
            "media_count": len(media_items(payload)),
            "redacted": True,
        }
    try:
        container = create_container(version, user_id or "", token or "", payload)
        wait_for_container(version, container, token or "", args.container_timeout_seconds)
        media_id = publish_container(version, user_id or "", token or "", container)
        url = permalink(version, media_id, token or "")
    except (HTTPError, URLError) as exc:
        return {"ok": False, "mutated": True, "issues": [http_issue(exc)], "redacted": True}
    except (RuntimeError, TimeoutError, ValueError) as exc:
        return {"ok": False, "mutated": True, "issues": [str(exc)], "redacted": True}
    timestamp = now_iso()
    ledger = None
    if not args.no_ledger:
        result = add_content_row(
            Path(args.project_root),
            {
                "content_id": f"instagram:{media_id}",
                "platform": "instagram",
                "external_id": media_id,
                "url": url,
                "status": "posted",
                "approval": "approved",
                "published_at": timestamp,
                "campaign": args.campaign or payload.get("campaign"),
                "kpis": args.kpis.split(",") if args.kpis else DEFAULT_KPIS,
                "source_ref": args.payload,
                "approval_ref": args.approval_ref,
            },
        )
        ledger = str(result.ledger_path)
    return {
        "ok": True,
        "mutated": True,
        "dry_run": False,
        "account_alias": args.account_alias,
        "container_id": container,
        "media_id": media_id,
        "url": url,
        "published_at": timestamp,
        "ledger": ledger,
        "redacted": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--payload", required=True, help="JSON file with caption, media_type, and public media URL(s).")
    parser.add_argument("--account-alias", required=True)
    parser.add_argument("--approval-ref", help="Ticket/report path proving explicit approval.")
    parser.add_argument("--execute", action="store_true", help="Actually mutate the Instagram account. Default is dry-run.")
    parser.add_argument("--project-root", default=str(ROOT))
    parser.add_argument("--campaign")
    parser.add_argument("--kpis", default=",".join(DEFAULT_KPIS))
    parser.add_argument(
        "--instagram-user-id",
        help="Overrides the injected Instagram user/business account ID.",
    )
    parser.add_argument("--graph-version")
    parser.add_argument("--container-timeout-seconds", type=int, default=300)
    parser.add_argument("--no-ledger", action="store_true")
    args = parser.parse_args()
    result = publish(args)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
