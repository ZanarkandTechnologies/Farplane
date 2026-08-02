#!/usr/bin/env python3
"""Fetch read-only Instagram Login metrics and write Farplane KPI observations."""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import urlopen

from runtime_env import env_value, load_runtime_values

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bin.core.farplane_metric_schema import MetricObservationBatch


def instagram_get(version: str, path: str, token: str, params: dict[str, str] | None = None) -> dict[str, Any]:
    query_params = dict(params or {})
    query_params["access_token"] = token
    urls = [
        f"https://graph.instagram.com/{version}{path}?{urlencode(query_params)}",
        f"https://graph.instagram.com{path}?{urlencode(query_params)}",
    ]
    last_error: HTTPError | None = None
    for url in urls:
        try:
            with urlopen(url, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            last_error = exc
    if last_error:
        raise last_error
    raise RuntimeError("Instagram Login request failed without an HTTP error")


def observation(metric_id: str, value: float, snapshot_date: str) -> dict[str, Any]:
    return {"metric_id": metric_id, "date": snapshot_date, "value": value, "status": "available"}


def parse_date(value: str | None) -> date | None:
    return date.fromisoformat(value) if value else None


def parse_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def in_date_window(timestamp: str | None, since_date: date | None, until_date: date | None) -> bool:
    parsed = parse_timestamp(timestamp)
    if parsed is None:
        return False
    media_date = parsed.astimezone(timezone.utc).date()
    if since_date and media_date < since_date:
        return False
    if until_date and media_date >= until_date:
        return False
    return True


def is_reel(item: dict[str, Any]) -> bool:
    return "REELS" in {
        str(item.get("media_type") or "").upper(),
        str(item.get("media_product_type") or "").upper(),
    }


def content_item_from_media(item: dict[str, Any], gaps: list[str] | None = None) -> dict[str, Any]:
    return {
        "platform": "instagram",
        "content_id": str(item.get("id") or ""),
        "url": item.get("permalink"),
        "published_at": item.get("timestamp"),
        "kind": str(item.get("media_product_type") or item.get("media_type") or "media").lower(),
        "media_type": item.get("media_type"),
        "media_product_type": item.get("media_product_type"),
        "content_metrics": {
            "views": None,
            "reach": None,
            "likes": item.get("like_count"),
            "engagements": None,
            "comments": item.get("comments_count"),
            "shares": None,
            "saves": None,
            "profile_clicks": None,
            "url_clicks": None,
            "avg_watch_time": None,
            "total_watch_time": None,
            "retention_score": None,
        },
        "source_metric_ids": ["instagram_likes", "instagram_comments"],
        "gaps": gaps or [],
    }


def observation_values(observations: list[dict[str, Any]]) -> dict[str, float]:
    return {
        str(item["metric_id"]): float(item["value"])
        for item in observations
        if isinstance(item.get("metric_id"), str) and isinstance(item.get("value"), (int, float))
    }


def enrich_single_content_item(content_items: list[dict[str, Any]], observations: list[dict[str, Any]]) -> None:
    if len(content_items) != 1:
        return
    values = observation_values(observations)
    metrics = content_items[0].setdefault("content_metrics", {})
    metrics["views"] = values.get("instagram_views")
    metrics["reach"] = values.get("instagram_reach")
    metrics["likes"] = values.get("instagram_likes", metrics.get("likes"))
    metrics["engagements"] = values.get("instagram_total_interactions")
    metrics["comments"] = values.get("instagram_comments", metrics.get("comments"))
    metrics["shares"] = values.get("instagram_shares")
    metrics["saves"] = values.get("instagram_saves")
    metrics["avg_watch_time"] = values.get("instagram_avg_watch_time")
    metrics["total_watch_time"] = values.get("instagram_total_watch_time")
    metrics["retention_score"] = values.get("instagram_retention_score")
    content_items[0]["source_metric_ids"] = sorted(values.keys())


def compact_metrics(observations: list[dict[str, Any]], content_items: list[dict[str, Any]]) -> dict[str, Any]:
    metrics = {
        str(item["metric_id"]): {"value": item["value"]}
        for item in observations
        if isinstance(item.get("metric_id"), str) and isinstance(item.get("value"), (int, float))
    }
    item_metric_map = {
        "instagram_views": "views",
        "instagram_reach": "reach",
        "instagram_likes": "likes",
        "instagram_total_interactions": "engagements",
        "instagram_comments": "comments",
        "instagram_shares": "shares",
        "instagram_saves": "saves",
        "instagram_avg_watch_time": "avg_watch_time",
        "instagram_total_watch_time": "total_watch_time",
        "instagram_retention_score": "retention_score",
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
                    "id": f"instagram:{content.get('content_id')}",
                    "value": value,
                    "kind": content.get("kind"),
                    "media_type": content.get("media_type"),
                    "media_product_type": content.get("media_product_type"),
                    "url": content.get("url"),
                }
            )
        if items:
            metrics[metric_id]["items"] = items
    return metrics


def insight_value(payload: dict[str, Any]) -> float | None:
    for item in payload.get("data") or []:
        values = item.get("values") or []
        if not values:
            continue
        value = values[-1].get("value")
        if isinstance(value, dict):
            numeric_values = [v for v in value.values() if isinstance(v, (int, float))]
            if numeric_values:
                return float(sum(numeric_values))
        if isinstance(value, (int, float)):
            return float(value)
    return None


def insight_values(payload: dict[str, Any]) -> dict[str, float]:
    values: dict[str, float] = {}
    for item in payload.get("data") or []:
        name = item.get("name")
        if not name:
            continue
        value = insight_value({"data": [item]})
        if value is not None:
            values[str(name)] = value
    return values


def collect_media_metrics(
    version: str,
    token: str,
    media: list[dict[str, Any]],
    snapshot_date: str,
    insight_metrics: list[str],
    duration_seconds: float | None = None,
    deep: bool = False,
    content_items: list[dict[str, Any]] | None = None,
) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    endpoints: list[str] = []
    gaps: list[str] = []
    observations: list[dict[str, Any]] = []
    like_total = 0.0
    like_seen = False
    insight_totals: dict[str, float] = {}
    insight_seen: set[str] = set()
    requested_metrics = insight_metrics
    if deep and not any(is_reel(item) for item in media):
        gaps.append("instagram_retention_requires_reel_media")
        requested_metrics = [metric for metric in insight_metrics if not metric.startswith("ig_reels_")]

    metric_map = {
        "views": "instagram_views",
        "reach": "instagram_reach",
        "saved": "instagram_saves",
        "shares": "instagram_shares",
        "comments": "instagram_comments",
        "likes": "instagram_likes_from_insights",
        "total_interactions": "instagram_total_interactions",
        "ig_reels_avg_watch_time": "instagram_avg_watch_time",
        "ig_reels_video_view_total_time": "instagram_total_watch_time",
    }
    content_metric_map = {
        "views": "views",
        "reach": "reach",
        "saved": "saves",
        "shares": "shares",
        "comments": "comments",
        "likes": "likes",
        "total_interactions": "engagements",
        "ig_reels_avg_watch_time": "avg_watch_time",
        "ig_reels_video_view_total_time": "total_watch_time",
    }

    for index, item in enumerate(media):
        if "like_count" in item:
            like_total += float(item["like_count"])
            like_seen = True
        media_id = item.get("id")
        if not media_id:
            continue
        media_values: dict[str, float] = {}
        try:
            insight = instagram_get(version, f"/{quote(str(media_id))}/insights", token, {"metric": ",".join(requested_metrics)})
            endpoints.append("/:ig-media-id/insights")
            for metric, value in insight_values(insight).items():
                insight_totals[metric] = insight_totals.get(metric, 0.0) + value
                insight_seen.add(metric)
                media_values[metric] = value
        except (HTTPError, URLError, TimeoutError):
            for metric in requested_metrics:
                try:
                    insight = instagram_get(version, f"/{quote(str(media_id))}/insights", token, {"metric": metric})
                    endpoints.append("/:ig-media-id/insights")
                    value = insight_value(insight)
                    if value is not None:
                        insight_totals[metric] = insight_totals.get(metric, 0.0) + value
                        insight_seen.add(metric)
                        media_values[metric] = value
                except (HTTPError, URLError, TimeoutError):
                    continue
        if content_items is not None and index < len(content_items):
            content_metrics = content_items[index].setdefault("content_metrics", {})
            source_metric_ids = set(content_items[index].get("source_metric_ids") or [])
            for platform_metric, value in media_values.items():
                content_key = content_metric_map.get(platform_metric)
                metric_id = metric_map.get(platform_metric)
                if content_key:
                    content_metrics[content_key] = value
                if metric_id:
                    source_metric_ids.add(metric_id)
            content_items[index]["source_metric_ids"] = sorted(source_metric_ids)

    if like_seen:
        observations.append(observation("instagram_likes", like_total, snapshot_date))
    else:
        gaps.append("instagram_likes_unavailable")

    if "views" in insight_seen:
        observations.append(observation("instagram_views", insight_totals["views"], snapshot_date))
    elif "reach" in insight_seen:
        observations.append(observation("instagram_views", insight_totals["reach"], snapshot_date))
    else:
        gaps.append("instagram_views_unavailable")

    if deep:
        for platform_metric, metric_id in metric_map.items():
            if platform_metric == "views":
                continue
            if platform_metric in insight_seen:
                observations.append(observation(metric_id, insight_totals[platform_metric], snapshot_date))
            else:
                gaps.append(f"{metric_id}_unavailable")
        avg_watch = insight_totals.get("ig_reels_avg_watch_time")
        if avg_watch is not None and duration_seconds and duration_seconds > 0:
            observations.append(observation("instagram_retention_score", min(avg_watch / duration_seconds * 100, 100.0), snapshot_date))
        elif avg_watch is not None:
            gaps.append("instagram_retention_score_requires_duration_seconds")
        else:
            gaps.append("instagram_retention_score_unavailable")

    return observations, gaps, endpoints


def fetch_metrics(
    snapshot_date: str,
    limit: int,
    insight_metrics: list[str],
    media_ids: list[str] | None = None,
    duration_seconds: float | None = None,
    deep: bool = False,
    since_date: str | None = None,
    until_date: str | None = None,
    latest: bool = False,
    latest_reel: bool = False,
    yesterday: bool = False,
) -> dict[str, Any]:
    runtime_values = load_runtime_values()
    token = env_value("FARPLANE_INSTAGRAM_LOGIN_ACCESS_TOKEN", runtime_values)
    version = env_value("FARPLANE_META_GRAPH_VERSION", runtime_values) or "v21.0"

    if not token:
        return {
            "schema_version": 1,
            "source_id": "instagram_account_api",
            "date": snapshot_date,
            "status": "blocked",
            "observations": [],
            "gaps": ["missing_FARPLANE_INSTAGRAM_LOGIN_ACCESS_TOKEN"],
            "payload": {"redacted": True},
        }

    endpoints = ["/me"]
    gaps: list[str] = []
    observations: list[dict[str, Any]] = []
    content_items: list[dict[str, Any]] = []

    profile = instagram_get(version, "/me", token, {"fields": "id,user_id,followers_count,media_count,username"})
    followers = profile.get("followers_count")
    if followers is not None:
        observations.append(observation("instagram_followers", float(followers), snapshot_date))
    else:
        gaps.append("instagram_followers_unavailable")

    explicit_media_ids = media_ids or []
    if explicit_media_ids:
        media = [
            instagram_get(
                version,
                f"/{quote(media_id)}",
                token,
                {"fields": "id,like_count,comments_count,media_type,media_product_type,timestamp,permalink"},
            )
            for media_id in explicit_media_ids
        ]
        content_items = [content_item_from_media(item) for item in media]
        endpoints.append("/:ig-media-id")
        media_observations, media_gaps, media_endpoints = collect_media_metrics(
            version, token, media, snapshot_date, insight_metrics, duration_seconds, deep, content_items
        )
        observations.extend(media_observations)
        gaps.extend(media_gaps)
        endpoints.extend(media_endpoints)
        enrich_single_content_item(content_items, media_observations)
    else:
        try:
            since = parse_date(since_date)
            until = parse_date(until_date)
            if yesterday:
                anchor = parse_date(snapshot_date) or date.today()
                since = anchor - timedelta(days=1)
                until = anchor
            media_payload = instagram_get(
                version,
                "/me/media",
                token,
                {
                    "fields": "id,like_count,comments_count,media_type,media_product_type,timestamp,permalink",
                    "limit": str(max(1, min(100 if (since or until or latest or latest_reel) else limit, 100))),
                },
            )
            endpoints.append("/me/media")
            media = media_payload.get("data") or []
            if since or until:
                media = [item for item in media if in_date_window(item.get("timestamp"), since, until)]
            if latest_reel:
                media = [item for item in media if is_reel(item)][:1]
                if not media:
                    gaps.append("instagram_latest_reel_unavailable")
            elif latest:
                media = media[:1]
            content_items = [content_item_from_media(item) for item in media]
            media_observations, media_gaps, media_endpoints = collect_media_metrics(
                version, token, media, snapshot_date, insight_metrics, duration_seconds, deep, content_items
            )
            observations.extend(media_observations)
            gaps.extend(media_gaps)
            endpoints.extend(media_endpoints)
            enrich_single_content_item(content_items, media_observations)
        except (HTTPError, URLError, TimeoutError) as exc:
            status = getattr(exc, "code", "network")
            gaps.append(f"instagram_media_metrics_fetch_failed:{status}")

    return {
        "schema_version": 1,
        "source_id": "instagram_account_api",
        "date": snapshot_date,
        "status": "available" if observations else "source_gap",
        "observations": observations,
        "gaps": gaps,
        "payload": {
            "source": "instagram_account_metrics",
            "metrics": compact_metrics(observations, content_items),
            "endpoints": sorted(set(endpoints)),
            "graph_version": version,
            "api_mode": "instagram_login",
            "media_ids": explicit_media_ids,
            "content_items": content_items,
            "selection": {
                "latest": latest,
                "latest_reel": latest_reel,
                "yesterday": yesterday,
                "since_date": str(parse_date(since_date)) if since_date else None,
                "until_date": str(parse_date(until_date)) if until_date else None,
                "limit": limit,
            },
            "deep": deep,
            "duration_seconds": duration_seconds,
            "redacted": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--media-id", action="append", default=[], help="Specific Instagram media ID to fetch metrics for; repeatable.")
    parser.add_argument("--deep", action="store_true", help="Request fuller Reels/media insights for retention and content-judgment metrics.")
    parser.add_argument("--duration-seconds", type=float, help="Optional media duration used to normalize average watch time into retention score.")
    parser.add_argument("--latest", action="store_true", help="Fetch only the most recent media item in account snapshot mode.")
    parser.add_argument("--latest-reel", action="store_true", help="Fetch only the most recent Reel in account snapshot mode.")
    parser.add_argument("--yesterday", action="store_true", help="Fetch media published on the day before --date, UTC.")
    parser.add_argument("--since-date", help="Only include media on or after this UTC date, YYYY-MM-DD.")
    parser.add_argument("--until-date", help="Only include media before this UTC date, YYYY-MM-DD.")
    parser.add_argument("--out", help="Output path. Defaults to .farplane/metrics/observations/<source_id>/<date>.json.")
    parser.add_argument(
        "--insight-metrics",
        default=os.environ.get("FARPLANE_INSTAGRAM_MEDIA_INSIGHT_METRICS"),
        help="Comma-separated media insight metrics to try for instagram_views.",
    )
    args = parser.parse_args()
    default_metrics = "views,reach,saved,shares,comments,likes,total_interactions,ig_reels_avg_watch_time,ig_reels_video_view_total_time"
    metrics_arg = args.insight_metrics or (default_metrics if args.deep else "views,reach")

    try:
        payload = fetch_metrics(
            args.date,
            args.limit,
            [item.strip() for item in metrics_arg.split(",") if item.strip()],
            args.media_id,
            args.duration_seconds,
            args.deep,
            args.since_date,
            args.until_date,
            args.latest,
            args.latest_reel,
            args.yesterday,
        )
    except (HTTPError, URLError, TimeoutError) as exc:
        status = getattr(exc, "code", "network")
        payload = {
            "schema_version": 1,
            "source_id": "instagram_account_api",
            "date": args.date,
            "status": "blocked",
            "observations": [],
            "gaps": [f"instagram_metrics_fetch_blocked:{status}"],
            "payload": {"redacted": True},
        }

    out = Path(args.out) if args.out else Path(".farplane") / "metrics" / "observations" / str(payload["source_id"]) / f"{args.date}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    MetricObservationBatch.model_validate(payload)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"ok": payload["status"] == "available", "out": str(out), "status": payload["status"], "observations": len(payload["observations"]), "gaps": payload.get("gaps", [])}, indent=2, sort_keys=True))
    return 0 if payload["status"] == "available" else 1


if __name__ == "__main__":
    raise SystemExit(main())
