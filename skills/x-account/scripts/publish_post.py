#!/usr/bin/env python3
"""Publish an approved X post or thread from a JSON payload."""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import mimetypes
import secrets
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from social_config import env_value, farplane_config_path, load_config_values
from validate_post_payload import tweets_from

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bin.core.farplane_content import add_content_row

BASE_URL = "https://api.x.com/2"
DEFAULT_KPIS = ["x_views", "x_likes", "evidence_distribution_reach"]
VIDEO_CATEGORIES = {"video/mp4": "tweet_video", "image/gif": "tweet_gif"}
IMAGE_CATEGORIES = {"image/jpeg": "tweet_image", "image/png": "tweet_image", "image/webp": "tweet_image"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_payload(path: Path) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("payload must be a JSON object")
    return raw


def stable_content_id(account_alias: str, payload: dict[str, Any]) -> str:
    relevant = {
        "account_alias": account_alias,
        "text": payload.get("text"),
        "tweets": payload.get("tweets"),
        "media": payload.get("media") or payload.get("media_paths"),
    }
    digest = hashlib.sha256(json.dumps(relevant, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()[:16]
    return f"x:draft:{digest}"


def tweet_payloads(payload: dict[str, Any]) -> list[dict[str, Any]]:
    if isinstance(payload.get("text"), str):
        return [{"text": payload["text"], "media": payload.get("media") or payload.get("media_paths") or []}]
    raw_tweets = payload.get("tweets")
    items: list[dict[str, Any]] = []
    if isinstance(raw_tweets, list):
        for item in raw_tweets:
            if isinstance(item, str):
                items.append({"text": item, "media": []})
            elif isinstance(item, dict) and isinstance(item.get("text"), str):
                items.append({"text": item["text"], "media": item.get("media") or item.get("media_paths") or []})
    return items


def normalize_media_paths(value: Any) -> list[Path]:
    if value is None:
        return []
    raw_items = value if isinstance(value, list) else [value]
    paths: list[Path] = []
    for item in raw_items:
        if isinstance(item, str) and item.strip():
            paths.append(Path(item).expanduser())
    return paths


def api_request(method: str, path: str, token: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
    return api_request_with_auth(method, path, f"Bearer {token}", body)


def api_request_with_auth(method: str, path: str, auth_header: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
    data = json.dumps(body or {}).encode("utf-8") if body is not None else None
    request = Request(
        f"{BASE_URL}{path}",
        data=data,
        method=method,
        headers={
            "Authorization": auth_header,
            "Content-Type": "application/json",
            "User-Agent": "Farplane x-account publisher",
        },
    )
    with urlopen(request, timeout=60) as response:
        raw = response.read().decode("utf-8")
    return json.loads(raw) if raw else {}


def oauth2_refresh_ready(file_values: dict[str, str]) -> bool:
    required = [
        "FARPLANE_X_OAUTH2_CLIENT_ID",
        "FARPLANE_X_OAUTH2_CLIENT_SECRET",
        "FARPLANE_X_OAUTH2_REFRESH_TOKEN",
    ]
    return all(env_value(key, file_values) for key in required)


def request_oauth2_refresh(file_values: dict[str, str]) -> dict[str, Any]:
    client_id = env_value("FARPLANE_X_OAUTH2_CLIENT_ID", file_values) or ""
    client_secret = env_value("FARPLANE_X_OAUTH2_CLIENT_SECRET", file_values) or ""
    refresh_token = env_value("FARPLANE_X_OAUTH2_REFRESH_TOKEN", file_values) or ""
    basic = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("ascii")
    body = urlencode({"grant_type": "refresh_token", "refresh_token": refresh_token}).encode("utf-8")
    request = Request(
        "https://api.x.com/2/oauth2/token",
        data=body,
        method="POST",
        headers={
            "Authorization": f"Basic {basic}",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Farplane x-account oauth2 refresher",
        },
    )
    with urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError("oauth2_refresh_invalid_response")
    return payload


def refresh_oauth2_access_token(file_values: dict[str, str]) -> str:
    payload = request_oauth2_refresh(file_values)
    access_token = payload.get("access_token")
    if not isinstance(access_token, str) or not access_token:
        raise RuntimeError("oauth2_refresh_missing_access_token")
    return access_token


def toml_string(value: str) -> str:
    return json.dumps(value)


def update_toml_section_values(text: str, section: str, values: dict[str, str]) -> str:
    lines = text.splitlines()
    header = f"[{section}]"
    start = None
    end = len(lines)
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped == header:
            start = index
            continue
        if start is not None and index > start and stripped.startswith("[") and stripped.endswith("]"):
            end = index
            break
    rendered = {key: f"{key} = {toml_string(value)}" for key, value in values.items() if value}
    if start is None:
        next_lines = list(lines)
        if next_lines and next_lines[-1].strip():
            next_lines.append("")
        next_lines.append(header)
        next_lines.extend(rendered.values())
        return "\n".join(next_lines) + "\n"
    seen: set[str] = set()
    next_lines = list(lines[: start + 1])
    for line in lines[start + 1 : end]:
        stripped = line.strip()
        replaced = False
        for key, rendered_line in rendered.items():
            if stripped.startswith(f"{key}") and stripped[len(key) :].lstrip().startswith("="):
                next_lines.append(rendered_line)
                seen.add(key)
                replaced = True
                break
        if not replaced:
            next_lines.append(line)
    for key, rendered_line in rendered.items():
        if key not in seen:
            next_lines.append(rendered_line)
    next_lines.extend(lines[end:])
    return "\n".join(next_lines) + "\n"


def save_refreshed_oauth2_tokens(access_token: str, refresh_token: str | None, path: Path | None = None) -> Path:
    config_path = path or farplane_config_path()
    original = config_path.read_text(encoding="utf-8") if config_path.exists() else ""
    values = {"oauth2_access_token": access_token}
    if refresh_token:
        values["oauth2_refresh_token"] = refresh_token
    updated = update_toml_section_values(original, "social.x", values)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = config_path.with_name(f".{config_path.name}.tmp")
    tmp_path.write_text(updated, encoding="utf-8")
    if config_path.exists():
        tmp_path.chmod(config_path.stat().st_mode)
    else:
        tmp_path.chmod(0o600)
    tmp_path.replace(config_path)
    return config_path


def oauth1_ready(file_values: dict[str, str]) -> bool:
    required = [
        "FARPLANE_X_ACCESS_TOKEN",
        "FARPLANE_X_ACCESS_TOKEN_SECRET",
        "FARPLANE_X_API_KEY",
        "FARPLANE_X_API_KEY_SECRET",
    ]
    return all(env_value(key, file_values) for key in required)


def oauth1_header(method: str, url: str, params: dict[str, str], file_values: dict[str, str]) -> str:
    api_key = env_value("FARPLANE_X_API_KEY", file_values) or ""
    api_secret = env_value("FARPLANE_X_API_KEY_SECRET", file_values) or ""
    access_token = env_value("FARPLANE_X_ACCESS_TOKEN", file_values) or ""
    access_secret = env_value("FARPLANE_X_ACCESS_TOKEN_SECRET", file_values) or ""
    oauth_params = {
        "oauth_consumer_key": api_key,
        "oauth_nonce": secrets.token_hex(16),
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(int(time.time())),
        "oauth_token": access_token,
        "oauth_version": "1.0",
    }
    signature_params = {**params, **oauth_params}
    encoded_params = "&".join(
        f"{quote(str(key), safe='')}={quote(str(value), safe='')}"
        for key, value in sorted(signature_params.items())
    )
    base_string = "&".join(quote(part, safe="") for part in (method.upper(), url, encoded_params))
    signing_key = f"{quote(api_secret, safe='')}&{quote(access_secret, safe='')}"
    digest = hmac.new(signing_key.encode("utf-8"), base_string.encode("utf-8"), hashlib.sha1).digest()
    oauth_params["oauth_signature"] = base64.b64encode(digest).decode("ascii")
    return "OAuth " + ", ".join(
        f'{quote(str(key), safe="")}="{quote(str(value), safe="")}"'
        for key, value in sorted(oauth_params.items())
    )


def http_issue(exc: HTTPError | URLError) -> str:
    if isinstance(exc, HTTPError):
        body = exc.read().decode("utf-8", errors="replace")[:500]
        return f"http_error:{exc.code}:{body}"
    return f"url_error:{exc.reason}"


def media_category(media_type: str) -> str:
    if media_type in IMAGE_CATEGORIES:
        return IMAGE_CATEGORIES[media_type]
    if media_type in VIDEO_CATEGORIES:
        return VIDEO_CATEGORIES[media_type]
    raise ValueError(f"unsupported_media_type:{media_type}")


def upload_image(path: Path, token: str, media_type: str) -> str:
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    response = api_request(
        "POST",
        "/media/upload",
        token,
        {"media": encoded, "media_category": media_category(media_type), "media_type": media_type},
    )
    media_id = (response.get("data") or {}).get("id")
    if not media_id:
        raise RuntimeError("missing_media_id")
    return str(media_id)


def wait_for_processing(media_id: str, token: str, processing_info: dict[str, Any] | None, timeout_seconds: int) -> None:
    deadline = time.time() + timeout_seconds
    info = processing_info or {}
    while info:
        state = str(info.get("state") or "").lower()
        if state in {"succeeded", "success"}:
            return
        if state in {"failed", "error"}:
            raise RuntimeError(f"media_processing_failed:{info.get('error') or info}")
        if time.time() >= deadline:
            raise TimeoutError("media_processing_timeout")
        time.sleep(max(1, min(int(info.get("check_after_secs") or 5), 30)))
        status = api_request("GET", f"/media/upload?media_id={media_id}", token)
        info = (status.get("data") or {}).get("processing_info") or {}


def upload_chunked_media(path: Path, token: str, media_type: str, timeout_seconds: int) -> str:
    size = path.stat().st_size
    init = api_request(
        "POST",
        "/media/upload/initialize",
        token,
        {"media_category": media_category(media_type), "media_type": media_type, "total_bytes": size},
    )
    media_id = str((init.get("data") or {}).get("id") or "")
    if not media_id:
        raise RuntimeError("missing_media_id")
    chunk_size = 4 * 1024 * 1024
    with path.open("rb") as handle:
        index = 0
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            api_request(
                "POST",
                f"/media/upload/{media_id}/append",
                token,
                {"media": base64.b64encode(chunk).decode("ascii"), "segment_index": index},
            )
            index += 1
    final = api_request("POST", f"/media/upload/{media_id}/finalize", token)
    wait_for_processing(media_id, token, (final.get("data") or {}).get("processing_info"), timeout_seconds)
    return media_id


def upload_media(path: Path, token: str, timeout_seconds: int) -> str:
    if not path.exists():
        raise ValueError(f"missing_media_file:{path}")
    media_type = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
    if media_type in IMAGE_CATEGORIES:
        return upload_image(path, token, media_type)
    if media_type in VIDEO_CATEGORIES:
        return upload_chunked_media(path, token, media_type, timeout_seconds)
    raise ValueError(f"unsupported_media_type:{media_type}")


def create_tweet(text: str, media_ids: list[str], token: str, reply_to: str | None = None) -> str:
    return create_tweet_with_auth(text, media_ids, f"Bearer {token}", reply_to)


def create_tweet_with_auth(text: str, media_ids: list[str], auth_header: str, reply_to: str | None = None) -> str:
    body: dict[str, Any] = {"text": text}
    if media_ids:
        body["media"] = {"media_ids": media_ids}
    if reply_to:
        body["reply"] = {"in_reply_to_tweet_id": reply_to}
    response = api_request_with_auth("POST", "/tweets", auth_header, body)
    tweet_id = (response.get("data") or {}).get("id")
    if not tweet_id:
        raise RuntimeError("missing_tweet_id")
    return str(tweet_id)


def publish_text_with_oauth1(tweets: list[dict[str, Any]], file_values: dict[str, str]) -> list[str]:
    tweet_ids: list[str] = []
    for item in tweets:
        if normalize_media_paths(item.get("media")):
            raise RuntimeError("oauth1_fallback_does_not_upload_media")
        auth_header = oauth1_header("POST", f"{BASE_URL}/tweets", {}, file_values)
        tweet_ids.append(create_tweet_with_auth(item["text"], [], auth_header, tweet_ids[-1] if tweet_ids else None))
    return tweet_ids


def validate(payload: dict[str, Any], limit: int) -> list[str]:
    issues: list[str] = []
    tweets = tweets_from(payload)
    if not tweets:
        issues.append("missing_text_or_tweets")
    for index, tweet in enumerate(tweets, start=1):
        if not tweet.strip():
            issues.append(f"tweet_{index}_empty")
        if len(tweet) > limit:
            issues.append(f"tweet_{index}_over_limit:{len(tweet)}>{limit}")
    return issues


def publish(args: argparse.Namespace) -> dict[str, Any]:
    payload = load_payload(Path(args.payload))
    issues = validate(payload, args.limit)
    tweets = tweet_payloads(payload)
    if issues:
        return {"ok": False, "mutated": False, "issues": issues, "redacted": True}
    file_values = load_config_values()
    token = env_value("FARPLANE_X_OAUTH2_ACCESS_TOKEN", file_values)
    dry_run = not args.execute
    if args.execute and not args.approval_ref:
        return {"ok": False, "mutated": False, "issues": ["missing_approval_ref"], "redacted": True}
    if args.execute and not token:
        return {"ok": False, "mutated": False, "issues": ["missing:FARPLANE_X_OAUTH2_ACCESS_TOKEN"], "redacted": True}
    prepared = [
        {"text_length": len(item["text"]), "media_count": len(normalize_media_paths(item.get("media")))}
        for item in tweets
    ]
    content_id = args.content_id or stable_content_id(args.account_alias, payload)
    ledger = None
    if dry_run:
        if not args.no_ledger:
            result = add_content_row(
                Path(args.project_root),
                {
                    "content_id": content_id,
                    "platform": "x",
                    "status": "draft",
                    "approval": "requested",
                    "campaign": args.campaign or payload.get("campaign"),
                    "kpis": args.kpis.split(",") if args.kpis else DEFAULT_KPIS,
                    "title": tweets[0]["text"][:80] if tweets else None,
                    "source_ref": args.payload,
                    "approval_ref": args.approval_ref,
                    "notes": "created_by=x-account publish_post.py dry_run",
                },
            )
            ledger = str(result.ledger_path)
        return {
            "ok": True,
            "mutated": False,
            "dry_run": True,
            "account_alias": args.account_alias,
            "content_id": content_id,
            "ledger": ledger,
            "tweet_count": len(tweets),
            "prepared": prepared,
            "redacted": True,
        }
    used_auth_mode = "oauth2_user"
    saved_refreshed_token = False
    try:
        tweet_ids: list[str] = []
        for item in tweets:
            media_ids = [upload_media(path, token or "", args.media_timeout_seconds) for path in normalize_media_paths(item.get("media"))]
            tweet_ids.append(create_tweet(item["text"], media_ids, token or "", tweet_ids[-1] if tweet_ids else None))
    except (HTTPError, URLError) as exc:
        if isinstance(exc, HTTPError) and exc.code == 401 and oauth2_refresh_ready(file_values):
            try:
                refresh_payload = request_oauth2_refresh(file_values)
                refreshed_token = refresh_payload.get("access_token")
                if not isinstance(refreshed_token, str) or not refreshed_token:
                    raise RuntimeError("oauth2_refresh_missing_access_token")
                refreshed_refresh_token = refresh_payload.get("refresh_token")
                if not args.no_save_refreshed_token:
                    save_refreshed_oauth2_tokens(
                        refreshed_token,
                        refreshed_refresh_token if isinstance(refreshed_refresh_token, str) else None,
                    )
                    saved_refreshed_token = True
                tweet_ids = []
                for item in tweets:
                    media_ids = [upload_media(path, refreshed_token, args.media_timeout_seconds) for path in normalize_media_paths(item.get("media"))]
                    tweet_ids.append(create_tweet(item["text"], media_ids, refreshed_token, tweet_ids[-1] if tweet_ids else None))
                used_auth_mode = "oauth2_user_refreshed_in_memory"
            except (HTTPError, URLError) as refresh_exc:
                if not oauth1_ready(file_values):
                    return {"ok": False, "mutated": bool(tweet_ids), "issues": [http_issue(exc), f"oauth2_refresh:{http_issue(refresh_exc)}"], "tweet_ids": tweet_ids, "redacted": True}
                try:
                    tweet_ids = publish_text_with_oauth1(tweets, file_values)
                    used_auth_mode = "oauth1_user_context"
                except (HTTPError, URLError) as fallback_exc:
                    return {"ok": False, "mutated": bool(tweet_ids), "issues": [http_issue(exc), f"oauth2_refresh:{http_issue(refresh_exc)}", f"oauth1_fallback:{http_issue(fallback_exc)}"], "tweet_ids": tweet_ids, "redacted": True}
                except (RuntimeError, TimeoutError, ValueError) as fallback_exc:
                    return {"ok": False, "mutated": bool(tweet_ids), "issues": [http_issue(exc), f"oauth2_refresh:{http_issue(refresh_exc)}", f"oauth1_fallback:{fallback_exc}"], "tweet_ids": tweet_ids, "redacted": True}
            except (RuntimeError, TimeoutError, ValueError) as refresh_exc:
                if not oauth1_ready(file_values):
                    return {"ok": False, "mutated": bool(tweet_ids), "issues": [http_issue(exc), f"oauth2_refresh:{refresh_exc}"], "tweet_ids": tweet_ids, "redacted": True}
                try:
                    tweet_ids = publish_text_with_oauth1(tweets, file_values)
                    used_auth_mode = "oauth1_user_context"
                except (HTTPError, URLError) as fallback_exc:
                    return {"ok": False, "mutated": bool(tweet_ids), "issues": [http_issue(exc), f"oauth2_refresh:{refresh_exc}", f"oauth1_fallback:{http_issue(fallback_exc)}"], "tweet_ids": tweet_ids, "redacted": True}
                except (RuntimeError, TimeoutError, ValueError) as fallback_exc:
                    return {"ok": False, "mutated": bool(tweet_ids), "issues": [http_issue(exc), f"oauth2_refresh:{refresh_exc}", f"oauth1_fallback:{fallback_exc}"], "tweet_ids": tweet_ids, "redacted": True}
        elif isinstance(exc, HTTPError) and exc.code == 401 and oauth1_ready(file_values):
            try:
                tweet_ids = publish_text_with_oauth1(tweets, file_values)
                used_auth_mode = "oauth1_user_context"
            except (HTTPError, URLError) as fallback_exc:
                return {"ok": False, "mutated": bool(tweet_ids), "issues": [http_issue(exc), f"oauth1_fallback:{http_issue(fallback_exc)}"], "tweet_ids": tweet_ids, "redacted": True}
            except (RuntimeError, TimeoutError, ValueError) as fallback_exc:
                return {"ok": False, "mutated": bool(tweet_ids), "issues": [http_issue(exc), f"oauth1_fallback:{fallback_exc}"], "tweet_ids": tweet_ids, "redacted": True}
        else:
            return {"ok": False, "mutated": bool(tweet_ids), "issues": [http_issue(exc)], "tweet_ids": tweet_ids, "redacted": True}
    except (RuntimeError, TimeoutError, ValueError) as exc:
        return {"ok": False, "mutated": bool(tweet_ids), "issues": [str(exc)], "tweet_ids": tweet_ids, "redacted": True}
    timestamp = now_iso()
    urls = [f"https://x.com/{args.username or env_value('FARPLANE_X_USERNAME', file_values) or 'i'}/status/{tweet_id}" for tweet_id in tweet_ids]
    if not args.no_ledger:
        result = add_content_row(
            Path(args.project_root),
            {
                "content_id": content_id,
                "platform": "x",
                "external_id": tweet_ids[0],
                "url": urls[0],
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
        "content_id": content_id,
        "tweet_ids": tweet_ids,
        "urls": urls,
        "published_at": timestamp,
        "ledger": ledger,
        "auth_mode": used_auth_mode,
        "saved_refreshed_token": saved_refreshed_token,
        "redacted": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--payload", required=True, help="JSON file with text or tweets[].")
    parser.add_argument("--account-alias", required=True)
    parser.add_argument("--approval-ref", help="Ticket/report path proving explicit approval.")
    parser.add_argument("--execute", action="store_true", help="Actually mutate the X account. Default is dry-run.")
    parser.add_argument("--project-root", default=str(ROOT))
    parser.add_argument("--content-id", help="Stable ledger content ID to update from draft to posted.")
    parser.add_argument("--campaign")
    parser.add_argument("--kpis", default=",".join(DEFAULT_KPIS))
    parser.add_argument("--username", help="Username for result URLs; falls back to private config when set.")
    parser.add_argument("--limit", type=int, default=280)
    parser.add_argument("--media-timeout-seconds", type=int, default=300)
    parser.add_argument("--no-ledger", action="store_true")
    parser.add_argument("--no-save-refreshed-token", action="store_true", help="Refresh OAuth2 in memory only; default saves successful refreshed tokens to private config.")
    args = parser.parse_args()
    result = publish(args)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
