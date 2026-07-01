#!/usr/bin/env python3
"""Fetch read-only X account metrics and write Farplane KPI observations."""

from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import os
import secrets
import time
from datetime import date, datetime, timedelta, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from social_config import env_value, load_config_values

BASE_URL = "https://api.x.com/2"


def oauth_ready(file_values: dict[str, str]) -> bool:
    required = [
        "FARPLANE_X_ACCESS_TOKEN",
        "FARPLANE_X_ACCESS_TOKEN_SECRET",
        "FARPLANE_X_API_KEY",
        "FARPLANE_X_API_KEY_SECRET",
    ]
    return all(env_value(key, file_values) for key in required)


def oauth2_ready(file_values: dict[str, str]) -> bool:
    return bool(env_value("FARPLANE_X_OAUTH2_ACCESS_TOKEN", file_values))


def bearer_header(token: str) -> str:
    return f"Bearer {token}"


def app_bearer_header(file_values: dict[str, str]) -> str | None:
    token = env_value("FARPLANE_X_BEARER_TOKEN", file_values)
    return bearer_header(token) if token else None


def oauth2_header(file_values: dict[str, str]) -> str | None:
    token = env_value("FARPLANE_X_OAUTH2_ACCESS_TOKEN", file_values)
    return bearer_header(token) if token else None


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
    base_string = "&".join(
        quote(part, safe="")
        for part in (method.upper(), url, encoded_params)
    )
    signing_key = f"{quote(api_secret, safe='')}&{quote(access_secret, safe='')}"
    digest = hmac.new(signing_key.encode("utf-8"), base_string.encode("utf-8"), hashlib.sha1).digest()
    oauth_params["oauth_signature"] = base64.b64encode(digest).decode("ascii")
    return "OAuth " + ", ".join(
        f'{quote(str(key), safe="")}="{quote(str(value), safe="")}"'
        for key, value in sorted(oauth_params.items())
    )


def api_get(path: str, auth_header: str, params: dict[str, str] | None = None) -> dict[str, Any]:
    query = f"?{urlencode(params)}" if params else ""
    request = Request(
        f"{BASE_URL}{path}{query}",
        headers={"Authorization": auth_header, "User-Agent": "Farplane x-account metrics fetcher"},
    )
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def observation(metric_id: str, value: float, snapshot_date: str) -> dict[str, Any]:
    return {"metric_id": metric_id, "date": snapshot_date, "value": value, "status": "available"}


def parse_date(value: str | None) -> date | None:
    return date.fromisoformat(value) if value else None


def parse_created_at(value: str | None) -> datetime | None:
    if not value:
        return None
    normalized = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return None


def in_date_window(created_at: str | None, since_date: date | None, until_date: date | None) -> bool:
    parsed = parse_created_at(created_at)
    if parsed is None:
        return False
    created_date = parsed.astimezone(timezone.utc).date()
    if since_date and created_date < since_date:
        return False
    if until_date and created_date >= until_date:
        return False
    return True


def tweet_url(username: str | None, tweet_id: str) -> str | None:
    if not username:
        return None
    return f"https://x.com/{username.lstrip('@')}/status/{tweet_id}"


def content_item_from_tweet(tweet: dict[str, Any], username: str | None) -> dict[str, Any]:
    metrics = tweet.get("public_metrics") or {}
    return {
        "platform": "x",
        "content_id": str(tweet.get("id") or ""),
        "url": tweet_url(username, str(tweet.get("id") or "")),
        "published_at": tweet.get("created_at"),
        "kind": "post",
        "content_metrics": {
            "views": metrics.get("impression_count"),
            "likes": metrics.get("like_count"),
            "engagements": None,
            "comments": metrics.get("reply_count"),
            "shares": metrics.get("retweet_count"),
            "saves": None,
            "profile_clicks": None,
            "url_clicks": None,
            "retention_score": None,
        },
        "source_metric_ids": ["x_views", "x_likes"],
        "gaps": [],
    }


def compact_metrics(observations: list[dict[str, Any]], content_items: list[dict[str, Any]]) -> dict[str, Any]:
    metrics = {
        str(item["metric_id"]): {"value": item["value"]}
        for item in observations
        if isinstance(item.get("metric_id"), str) and isinstance(item.get("value"), (int, float))
    }
    item_metric_map = {
        "x_views": "views",
        "x_likes": "likes",
        "x_engagements": "engagements",
        "x_profile_clicks": "profile_clicks",
        "x_url_clicks": "url_clicks",
        "x_retention_score": "retention_score",
    }
    for metric_id, content_key in item_metric_map.items():
        if metric_id not in metrics:
            continue
        items: list[dict[str, Any]] = []
        for content in content_items:
            value = (content.get("content_metrics") or {}).get(content_key)
            if value is None:
                continue
            items.append(
                {
                    "id": f"x:{content.get('content_id')}",
                    "value": value,
                    "kind": content.get("kind"),
                    "url": content.get("url"),
                }
            )
        if items:
            metrics[metric_id]["items"] = items
    return metrics


def resolve_user(file_values: dict[str, str], auth_header: str) -> tuple[str, dict[str, Any], list[str]]:
    user_id = env_value("FARPLANE_X_USER_ID", file_values)
    username = env_value("FARPLANE_X_USERNAME", file_values)
    params = {"user.fields": "public_metrics"}
    if user_id:
        payload = api_get(f"/users/{quote(user_id)}", auth_header, params)
        return user_id, payload, ["/2/users/:id"]
    if username:
        clean_username = username.lstrip("@")
        payload = api_get(f"/users/by/username/{quote(clean_username)}", auth_header, params)
        data = payload.get("data") or {}
        resolved_id = str(data.get("id") or "")
        if not resolved_id:
            raise RuntimeError("X username lookup did not return a user id")
        return resolved_id, payload, ["/2/users/by/username/:username"]
    raise RuntimeError("Set FARPLANE_X_USER_ID or FARPLANE_X_USERNAME for read metrics")


def nested_metric(item: dict[str, Any], names: list[str]) -> float | None:
    for bucket in ("public_metrics", "non_public_metrics", "organic_metrics", "promoted_metrics"):
        metrics = item.get(bucket) or {}
        for name in names:
            value = metrics.get(name)
            if isinstance(value, (int, float)):
                return float(value)
    return None


def add_if_seen(
    observations: list[dict[str, Any]],
    gaps: list[str],
    metric_id: str,
    value: float | None,
    seen: bool,
    snapshot_date: str,
) -> None:
    if seen and value is not None:
        observations.append(observation(metric_id, value, snapshot_date))
    else:
        gaps.append(f"{metric_id}_unavailable")


def fetch_tweet_metrics(
    auth_header: str,
    tweet_ids: list[str],
    snapshot_date: str,
    deep: bool = False,
    file_values: dict[str, str] | None = None,
) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    tweet_fields = "public_metrics,created_at,attachments"
    media_fields = "public_metrics,type"
    if deep:
        tweet_fields = "public_metrics,non_public_metrics,organic_metrics,created_at,attachments"
        media_fields = "public_metrics,non_public_metrics,organic_metrics,type"
    params = {
        "ids": ",".join(tweet_ids),
        "tweet.fields": tweet_fields,
        "expansions": "attachments.media_keys",
        "media.fields": media_fields,
    }
    if deep and file_values and oauth_ready(file_values):
        auth_header = oauth1_header("GET", f"{BASE_URL}/tweets", params, file_values)
    payload = api_get(
        "/tweets",
        auth_header,
        params,
    )
    observations: list[dict[str, Any]] = []
    gaps: list[str] = []
    endpoints = ["/2/tweets"]
    like_total = 0.0
    impression_total = 0.0
    video_view_total = 0.0
    engagement_total = 0.0
    profile_click_total = 0.0
    url_click_total = 0.0
    playback_start_total = 0.0
    playback_25_total = 0.0
    playback_50_total = 0.0
    playback_75_total = 0.0
    playback_100_total = 0.0
    like_seen = False
    impression_seen = False
    video_seen = False
    engagement_seen = False
    profile_click_seen = False
    url_click_seen = False
    playback_start_seen = False
    playback_25_seen = False
    playback_50_seen = False
    playback_75_seen = False
    playback_100_seen = False
    for tweet in payload.get("data") or []:
        like_count = nested_metric(tweet, ["like_count"])
        if like_count is not None:
            like_total += like_count
            like_seen = True
        impression_count = nested_metric(tweet, ["impression_count"])
        if impression_count is not None:
            impression_total += impression_count
            impression_seen = True
        engagement_count = nested_metric(tweet, ["engagements", "engagement_count", "user_engagements"])
        if engagement_count is not None:
            engagement_total += engagement_count
            engagement_seen = True
        profile_clicks = nested_metric(tweet, ["user_profile_clicks", "profile_clicks"])
        if profile_clicks is not None:
            profile_click_total += profile_clicks
            profile_click_seen = True
        url_clicks = nested_metric(tweet, ["url_link_clicks", "url_clicks"])
        if url_clicks is not None:
            url_click_total += url_clicks
            url_click_seen = True
    for media in (payload.get("includes") or {}).get("media") or []:
        view_count = nested_metric(media, ["view_count", "video_view_count"])
        if view_count is not None:
            video_view_total += view_count
            video_seen = True
        playback_start = nested_metric(media, ["playback_0_count", "video_playback_0_count"])
        if playback_start is not None:
            playback_start_total += playback_start
            playback_start_seen = True
        playback_25 = nested_metric(media, ["playback_25_count", "video_playback_25_count"])
        if playback_25 is not None:
            playback_25_total += playback_25
            playback_25_seen = True
        playback_50 = nested_metric(media, ["playback_50_count", "video_playback_50_count"])
        if playback_50 is not None:
            playback_50_total += playback_50
            playback_50_seen = True
        playback_75 = nested_metric(media, ["playback_75_count", "video_playback_75_count"])
        if playback_75 is not None:
            playback_75_total += playback_75
            playback_75_seen = True
        playback_100 = nested_metric(media, ["playback_100_count", "video_playback_100_count"])
        if playback_100 is not None:
            playback_100_total += playback_100
            playback_100_seen = True
    if like_seen:
        observations.append(observation("x_likes", like_total, snapshot_date))
    else:
        gaps.append("x_likes_unavailable")
    if impression_seen:
        observations.append(observation("x_views", impression_total, snapshot_date))
    elif video_seen:
        observations.append(observation("x_views", video_view_total, snapshot_date))
    else:
        gaps.append("x_views_unavailable")
    if deep:
        add_if_seen(observations, gaps, "x_engagements", engagement_total, engagement_seen, snapshot_date)
        add_if_seen(observations, gaps, "x_profile_clicks", profile_click_total, profile_click_seen, snapshot_date)
        add_if_seen(observations, gaps, "x_url_clicks", url_click_total, url_click_seen, snapshot_date)
        add_if_seen(observations, gaps, "x_video_starts", playback_start_total, playback_start_seen, snapshot_date)
        add_if_seen(observations, gaps, "x_video_25pct_views", playback_25_total, playback_25_seen, snapshot_date)
        add_if_seen(observations, gaps, "x_video_50pct_views", playback_50_total, playback_50_seen, snapshot_date)
        add_if_seen(observations, gaps, "x_video_75pct_views", playback_75_total, playback_75_seen, snapshot_date)
        add_if_seen(observations, gaps, "x_video_completions", playback_100_total, playback_100_seen, snapshot_date)
        if playback_start_seen and playback_start_total > 0 and playback_100_seen:
            observations.append(observation("x_retention_score", playback_100_total / playback_start_total * 100, snapshot_date))
        else:
            gaps.append("x_retention_score_unavailable")
    return observations, gaps, endpoints


def fetch_metrics(
    snapshot_date: str,
    limit: int,
    tweet_ids: list[str] | None = None,
    deep: bool = False,
    since_date: str | None = None,
    until_date: str | None = None,
    latest: bool = False,
    yesterday: bool = False,
) -> dict[str, Any]:
    file_values = load_config_values()
    app_auth = app_bearer_header(file_values)
    user_auth = oauth2_header(file_values)
    if not app_auth and not user_auth:
        return {
            "source_id": "x_account_api",
            "date": snapshot_date,
            "status": "blocked",
            "observations": [],
            "gaps": ["missing_FARPLANE_X_BEARER_TOKEN_or_FARPLANE_X_OAUTH2_ACCESS_TOKEN"],
            "redacted": True,
        }

    profile_auth = user_auth or app_auth
    tweet_auth = user_auth or app_auth
    auth_mode = "oauth2_user_context" if user_auth else "app_bearer"
    deep_oauth_ready = oauth_ready(file_values)
    if deep and deep_oauth_ready:
        auth_mode = "oauth2_user_context" if user_auth else "oauth1_user_context"

    endpoints: list[str] = []
    gaps: list[str] = []
    observations: list[dict[str, Any]] = []
    content_items: list[dict[str, Any]] = []

    if profile_auth is None or tweet_auth is None:
        raise RuntimeError("X auth header unavailable after readiness check")

    try:
        user_id, user_payload, user_endpoints = resolve_user(file_values, profile_auth)
    except HTTPError as exc:
        if exc.code != 401 or not user_auth or not app_auth:
            raise
        gaps.append("x_oauth2_user_context_rejected_401_used_app_bearer")
        profile_auth = app_auth
        tweet_auth = app_auth
        auth_mode = "app_bearer_fallback_after_oauth2_401"
        user_id, user_payload, user_endpoints = resolve_user(file_values, profile_auth)
    username = env_value("FARPLANE_X_USERNAME", file_values)
    endpoints.extend(user_endpoints)
    public_metrics = (user_payload.get("data") or {}).get("public_metrics") or {}
    followers = public_metrics.get("followers_count")
    if followers is not None:
        observations.append(observation("x_followers", float(followers), snapshot_date))
    else:
        gaps.append("x_followers_unavailable")

    explicit_tweet_ids = tweet_ids or []
    if explicit_tweet_ids:
        if deep and not user_auth and not deep_oauth_ready:
            gaps.append("x_deep_metrics_need_oauth2_or_oauth1_user_context_credentials")
        try:
            tweet_observations, tweet_gaps, tweet_endpoints = fetch_tweet_metrics(
                tweet_auth,
                explicit_tweet_ids,
                snapshot_date,
                deep,
                file_values if not user_auth else None,
            )
        except HTTPError as exc:
            if exc.code != 401 or not user_auth or not app_auth:
                raise
            gaps.append("x_oauth2_tweet_metrics_rejected_401_used_app_bearer")
            auth_mode = "app_bearer_fallback_after_oauth2_401"
            tweet_observations, tweet_gaps, tweet_endpoints = fetch_tweet_metrics(
                app_auth,
                explicit_tweet_ids,
                snapshot_date,
                deep=False,
                file_values=None,
            )
        observations.extend(tweet_observations)
        gaps.extend(tweet_gaps)
        endpoints.extend(tweet_endpoints)
    elif deep:
        gaps.append("x_deep_metrics_require_tweet_id")
    else:
        try:
            since = parse_date(since_date)
            until = parse_date(until_date)
            if yesterday:
                anchor = parse_date(snapshot_date) or date.today()
                since = anchor - timedelta(days=1)
                until = anchor
            tweets_payload = api_get(
                f"/users/{quote(user_id)}/tweets",
                tweet_auth,
                {
                    "max_results": str(max(5, min(100 if (since or until or latest) else limit, 100))),
                    "tweet.fields": "public_metrics,created_at",
                    "exclude": "retweets,replies",
                },
            )
            endpoints.append("/2/users/:id/tweets")
            tweets = tweets_payload.get("data") or []
            if since or until:
                tweets = [tweet for tweet in tweets if in_date_window(tweet.get("created_at"), since, until)]
            if latest and tweets:
                tweets = tweets[:1]
            content_items = [content_item_from_tweet(tweet, username) for tweet in tweets]
            like_total = 0.0
            view_total = 0.0
            like_seen = False
            view_seen = False
            for tweet in tweets:
                metrics = tweet.get("public_metrics") or {}
                if "like_count" in metrics:
                    like_total += float(metrics["like_count"])
                    like_seen = True
                if "impression_count" in metrics:
                    view_total += float(metrics["impression_count"])
                    view_seen = True
            if like_seen:
                observations.append(observation("x_likes", like_total, snapshot_date))
            else:
                gaps.append("x_likes_unavailable")
            if view_seen:
                observations.append(observation("x_views", view_total, snapshot_date))
            else:
                gaps.append("x_views_unavailable")
        except (HTTPError, URLError, TimeoutError) as exc:
            status = getattr(exc, "code", "network")
            gaps.append(f"x_tweet_metrics_fetch_failed:{status}")

    return {
        "source_id": "x_account_api",
        "source": "x_account_metrics",
        "date": snapshot_date,
        "status": "available" if observations else "source_gap",
        "metrics": compact_metrics(observations, content_items),
        "observations": observations,
        "gaps": gaps,
        "endpoints": endpoints,
        "post_ids": explicit_tweet_ids,
        "content_items": content_items,
        "selection": {
            "latest": latest,
            "yesterday": yesterday,
            "since_date": str(parse_date(since_date)) if since_date else None,
            "until_date": str(parse_date(until_date)) if until_date else None,
            "limit": limit,
        },
        "deep": deep,
        "auth_mode": auth_mode,
        "redacted": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--tweet-id", action="append", default=[], help="Specific X Post ID to fetch metrics for; repeatable.")
    parser.add_argument("--deep", action="store_true", help="Request owned-content analytics fields for retention/click metrics when authorized.")
    parser.add_argument("--latest", action="store_true", help="Fetch only the most recent timeline post in account snapshot mode.")
    parser.add_argument("--yesterday", action="store_true", help="Fetch posts published on the day before --date, UTC.")
    parser.add_argument("--since-date", help="Only include timeline posts on or after this UTC date, YYYY-MM-DD.")
    parser.add_argument("--until-date", help="Only include timeline posts before this UTC date, YYYY-MM-DD.")
    parser.add_argument("--out", default=".farplane/metrics/manual/x_account.json")
    args = parser.parse_args()

    try:
        payload = fetch_metrics(args.date, args.limit, args.tweet_id, args.deep, args.since_date, args.until_date, args.latest, args.yesterday)
    except (HTTPError, URLError, TimeoutError, RuntimeError) as exc:
        status = getattr(exc, "code", "runtime")
        payload = {
            "source_id": "x_account_api",
            "date": args.date,
            "status": "blocked",
            "observations": [],
            "gaps": [f"x_metrics_fetch_blocked:{status}"],
            "redacted": True,
        }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"ok": payload["status"] == "available", "out": str(out), "status": payload["status"], "observations": len(payload["observations"]), "gaps": payload.get("gaps", [])}, indent=2, sort_keys=True))
    return 0 if payload["status"] == "available" else 1


if __name__ == "__main__":
    raise SystemExit(main())
