#!/usr/bin/env python3
"""Fetch read-only Instagram Graph metrics and write Farplane KPI observations."""

from __future__ import annotations

import argparse
import json
import os
from datetime import date
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import urlopen


ENV_PATH = Path.home() / ".codex" / "private" / "social.env"


def load_env_file(path: Path = ENV_PATH) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :]
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def env_value(key: str, file_values: dict[str, str]) -> str | None:
    return os.environ.get(key) or file_values.get(key) or None


def graph_get(version: str, path: str, token: str, params: dict[str, str] | None = None) -> dict[str, Any]:
    query_params = dict(params or {})
    query_params["access_token"] = token
    url = f"https://graph.facebook.com/{version}{path}?{urlencode(query_params)}"
    with urlopen(url, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def observation(metric_id: str, value: float, snapshot_date: str) -> dict[str, Any]:
    return {"metric_id": metric_id, "date": snapshot_date, "value": value, "status": "available"}


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
        value_payload = insight_value({"data": [item]})
        if value_payload is not None:
            values[str(name)] = value_payload
    return values


def collect_media_metrics(
    version: str,
    token: str,
    media: list[dict[str, Any]],
    snapshot_date: str,
    insight_metrics: list[str],
    duration_seconds: float | None = None,
    deep: bool = False,
) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    endpoints: list[str] = []
    gaps: list[str] = []
    observations: list[dict[str, Any]] = []
    like_total = 0.0
    like_seen = False
    insight_totals: dict[str, float] = {}
    insight_seen: set[str] = set()
    for item in media:
        if "like_count" in item:
            like_total += float(item["like_count"])
            like_seen = True
        media_id = item.get("id")
        if not media_id:
            continue
        try:
            insight = graph_get(
                version,
                f"/{quote(str(media_id))}/insights",
                token,
                {"metric": ",".join(insight_metrics)},
            )
            endpoints.append("/:ig-media-id/insights")
            for metric, value in insight_values(insight).items():
                insight_totals[metric] = insight_totals.get(metric, 0.0) + value
                insight_seen.add(metric)
        except (HTTPError, URLError, TimeoutError):
            for metric in insight_metrics:
                try:
                    insight = graph_get(version, f"/{quote(str(media_id))}/insights", token, {"metric": metric})
                    endpoints.append("/:ig-media-id/insights")
                    value = insight_value(insight)
                    if value is not None:
                        insight_totals[metric] = insight_totals.get(metric, 0.0) + value
                        insight_seen.add(metric)
                except (HTTPError, URLError, TimeoutError):
                    continue
    if like_seen:
        observations.append(observation("instagram_likes", like_total, snapshot_date))
    else:
        gaps.append("instagram_likes_unavailable")

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
    if "views" in insight_seen:
        observations.append(observation("instagram_views", insight_totals["views"], snapshot_date))
    elif "reach" in insight_seen:
        observations.append(observation("instagram_views", insight_totals["reach"], snapshot_date))
    else:
        gaps.append("instagram_views_unavailable")

    if deep:
        for platform_metric, metric_id in metric_map.items():
            if platform_metric in {"views"}:
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
) -> dict[str, Any]:
    file_values = load_env_file()
    token = env_value("FARPLANE_INSTAGRAM_ACCESS_TOKEN", file_values)
    ig_user_id = env_value("FARPLANE_INSTAGRAM_BUSINESS_ACCOUNT_ID", file_values)
    version = env_value("FARPLANE_META_GRAPH_VERSION", file_values) or "v21.0"

    missing = []
    if not token:
        missing.append("missing_FARPLANE_INSTAGRAM_ACCESS_TOKEN")
    if not ig_user_id:
        missing.append("missing_FARPLANE_INSTAGRAM_BUSINESS_ACCOUNT_ID")
    if missing:
        return {
            "source_id": "instagram_account_api",
            "date": snapshot_date,
            "status": "blocked",
            "observations": [],
            "gaps": missing,
            "redacted": True,
        }

    endpoints = ["/:ig-user-id"]
    gaps: list[str] = []
    observations: list[dict[str, Any]] = []

    profile = graph_get(version, f"/{quote(ig_user_id)}", token, {"fields": "followers_count,media_count,username"})
    followers = profile.get("followers_count")
    if followers is not None:
        observations.append(observation("instagram_followers", float(followers), snapshot_date))
    else:
        gaps.append("instagram_followers_unavailable")

    explicit_media_ids = media_ids or []
    if explicit_media_ids:
        media = [
            graph_get(version, f"/{quote(media_id)}", token, {"fields": "id,like_count,comments_count,media_type,timestamp"})
            for media_id in explicit_media_ids
        ]
        endpoints.append("/:ig-media-id")
        media_observations, media_gaps, media_endpoints = collect_media_metrics(
            version, token, media, snapshot_date, insight_metrics, duration_seconds, deep
        )
        observations.extend(media_observations)
        gaps.extend(media_gaps)
        endpoints.extend(media_endpoints)
    else:
        try:
            media_payload = graph_get(
                version,
                f"/{quote(ig_user_id)}/media",
                token,
                {"fields": "id,like_count,comments_count,media_type,timestamp", "limit": str(max(1, min(limit, 100)))},
            )
            endpoints.append("/:ig-user-id/media")
            media = media_payload.get("data") or []
            media_observations, media_gaps, media_endpoints = collect_media_metrics(
                version, token, media, snapshot_date, insight_metrics, duration_seconds, deep
            )
            observations.extend(media_observations)
            gaps.extend(media_gaps)
            endpoints.extend(media_endpoints)
        except (HTTPError, URLError, TimeoutError) as exc:
            status = getattr(exc, "code", "network")
            gaps.append(f"instagram_media_metrics_fetch_failed:{status}")

    return {
        "source_id": "instagram_account_api",
        "date": snapshot_date,
        "status": "available" if observations else "source_gap",
        "observations": observations,
        "gaps": gaps,
        "endpoints": sorted(set(endpoints)),
        "graph_version": version,
        "media_ids": explicit_media_ids,
        "deep": deep,
        "duration_seconds": duration_seconds,
        "redacted": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", default=date.today().isoformat())
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--media-id", action="append", default=[], help="Specific Instagram media ID to fetch metrics for; repeatable.")
    parser.add_argument("--deep", action="store_true", help="Request fuller Reels/media insights for retention and content-judgment metrics.")
    parser.add_argument("--duration-seconds", type=float, help="Optional media duration used to normalize average watch time into retention score.")
    parser.add_argument("--out", default=".farplane/metrics/manual/instagram_account.json")
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
        )
    except (HTTPError, URLError, TimeoutError) as exc:
        status = getattr(exc, "code", "network")
        payload = {
            "source_id": "instagram_account_api",
            "date": args.date,
            "status": "blocked",
            "observations": [],
            "gaps": [f"instagram_metrics_fetch_blocked:{status}"],
            "redacted": True,
        }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"ok": payload["status"] == "available", "out": str(out), "status": payload["status"], "observations": len(payload["observations"]), "gaps": payload.get("gaps", [])}, indent=2, sort_keys=True))
    return 0 if payload["status"] == "available" else 1


if __name__ == "__main__":
    raise SystemExit(main())
