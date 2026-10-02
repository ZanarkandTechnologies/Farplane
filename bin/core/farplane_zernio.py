"""Zernio, read by `farplane metrics refresh` for a project whose `farplane/bindings.yaml` names a profile.

Zernio is the one source of a business's social numbers: it reads every account connected to it,
including posts published natively on the platform, so Farplane connects no platform itself
(docs/farplane-framework/cli.md). It gives the Distribution step `posts_published`, how many posts went out
each day (the input a step plan paces), and `views_per_post`, the average views of the posts published in
the seven days to that day (an output to hill-climb). For each connected account it also fills the
`<platform>_followers` and `<platform>_views` metrics the project defines (views of the posts published in
the 30 days to that day), tagged with the account so the Leverage lens can tell accounts apart. Every run
rewrites the last WINDOW_DAYS of daily observations, since views keep growing after a post goes out. The
full dashboard stays in Zernio.
"""

from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

import yaml

API = "https://zernio.com/api/v1"
SOURCE_ID = "zernio_content"
WINDOW_DAYS = 42
VIEWS_DAYS = 30
OBSERVATIONS = Path(".farplane") / "metrics" / "observations" / SOURCE_ID

Fetch = Callable[[str, str], Any]


def zernio_profile(bindings_text: str) -> str | None:
    """The profile a business binds: `zernio:` then `profile: <id>` in farplane/bindings.yaml."""
    match = re.search(r"^zernio:\s*\n(?:[ \t]+.*\n)*?[ \t]+profile:\s*['\"]?([A-Za-z0-9]+)", bindings_text, re.M)
    return match.group(1) if match else None


def _get(url: str, api_key: str) -> Any:
    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def fetch_posts(profile: str, api_key: str, since: date, until: date, fetch: Fetch = _get) -> list[dict[str, Any]]:
    """Every published post of the profile between two days, through Zernio's paginated analytics list."""
    posts: list[dict[str, Any]] = []
    page = 1
    while True:
        query = urllib.parse.urlencode({"profileId": profile, "fromDate": since.isoformat(), "toDate": until.isoformat(), "limit": 100, "page": page})
        body = fetch(f"{API}/analytics?{query}", api_key)
        posts += [p for p in body.get("posts") or [] if p.get("publishedAt")]
        if page >= int((body.get("pagination") or {}).get("pages") or 1):
            return posts
        page += 1


def fetch_accounts(profile: str, api_key: str, fetch: Fetch = _get) -> list[dict[str, Any]]:
    """The social accounts connected to the profile in Zernio."""
    body = fetch(f"{API}/accounts?{urllib.parse.urlencode({'profileId': profile})}", api_key)
    return [a for a in body.get("accounts") or [] if a.get("platform") and a.get("isActive", True)]


def defined_metrics(root: Path) -> set[str]:
    """The metric ids the project's farplane/metrics.yaml defines."""
    try:
        loaded = yaml.safe_load((root / "farplane" / "metrics.yaml").read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return set()
    metrics = loaded.get("metrics") if isinstance(loaded, dict) else None
    return set(metrics) if isinstance(metrics, dict) else set()


def account_readings(posts: list[dict[str, Any]], accounts: list[dict[str, Any]], defined: set[str], until: date, days: int = WINDOW_DAYS) -> dict[str, list[dict[str, Any]]]:
    """Each connected account's defined `<platform>_views` (every day) and `<platform>_followers` (today, the
    only day Zernio knows), by date, each tagged with its account."""
    out: dict[str, list[dict[str, Any]]] = {}
    for account in accounts:
        platform = str(account["platform"]).lower()
        handle = str(account.get("username") or account.get("_id") or "")
        tag = {"distribution_account": {"platform": platform, "account_id": handle, "label": str(account.get("displayName") or handle)}}
        mine = [
            (datetime.fromisoformat(str(p["publishedAt"]).replace("Z", "+00:00")).astimezone().date(), p)
            for p in posts
            if str(p.get("platform") or platform).lower() == platform
        ]
        if f"{platform}_views" in defined:
            for back in range(days):
                day = until - timedelta(days=back)
                views = sum(float((p.get("analytics") or {}).get("views") or 0) for d, p in mine if day - timedelta(days=VIEWS_DAYS - 1) <= d <= day)
                out.setdefault(day.isoformat(), []).append({"date": day.isoformat(), "metric_id": f"{platform}_views", "status": "available", "value": views, "payload": dict(tag)})
        if f"{platform}_followers" in defined and isinstance(account.get("followersCount"), (int, float)):
            out.setdefault(until.isoformat(), []).append({"date": until.isoformat(), "metric_id": f"{platform}_followers", "status": "available", "value": float(account["followersCount"]), "payload": dict(tag)})
    return out


def daily_readings(posts: list[dict[str, Any]], until: date, days: int = WINDOW_DAYS) -> dict[str, list[dict[str, Any]]]:
    """Each day's observations, by date: posts published that day, and views per post over the 7 days to it."""
    published = [(datetime.fromisoformat(str(p["publishedAt"]).replace("Z", "+00:00")).astimezone().date(), p) for p in posts]
    out: dict[str, list[dict[str, Any]]] = {}
    for back in range(days):
        day = until - timedelta(days=back)
        that_day = [p for d, p in published if d == day]
        week = [p for d, p in published if day - timedelta(days=6) <= d <= day]
        views = [float((p.get("analytics") or {}).get("views") or 0) for p in week]
        rows = [{"date": day.isoformat(), "metric_id": "posts_published", "status": "available", "value": float(len(that_day))}]
        rows.append(
            {"date": day.isoformat(), "metric_id": "views_per_post", "status": "available", "value": round(sum(views) / len(views), 1)}
            if views
            else {"date": day.isoformat(), "metric_id": "views_per_post", "status": "source_gap", "value": None}
        )
        out[day.isoformat()] = rows
    return out


def refresh_zernio(root: Path, api_key: str, today: date, fetch: Fetch = _get) -> dict[str, Any]:
    """Writes the project's Zernio observations for the last WINDOW_DAYS; says why when it can't."""
    bindings = root / "farplane" / "bindings.yaml"
    profile = zernio_profile(bindings.read_text(encoding="utf-8")) if bindings.exists() else None
    if not profile:
        return {"status": "none"}
    if not api_key:
        return {"status": "gap", "reason": "ZERNIO_API_KEY is not set (run through farplane run --)"}
    try:
        posts = fetch_posts(profile, api_key, today - timedelta(days=WINDOW_DAYS + VIEWS_DAYS), today, fetch)
        accounts = fetch_accounts(profile, api_key, fetch)
    except Exception as exc:  # Zernio down or the key refused: a gap, never a zero
        return {"status": "gap", "reason": f"zernio unreachable: {type(exc).__name__}"}
    fetched_at = datetime.now(timezone.utc).isoformat()
    folder = root / OBSERVATIONS
    folder.mkdir(parents=True, exist_ok=True)
    per_account = account_readings(posts, accounts, defined_metrics(root), today)
    for day, rows in daily_readings(posts, today).items():
        rows += per_account.get(day, [])
        for row in rows:
            row["payload"] = {**row.get("payload", {}), "source": {"provider": "zernio", "profile": profile, "fetched_at": fetched_at, "endpoint": "GET /v1/analytics, GET /v1/accounts"}}
        document = {"schema_version": 1, "source_id": SOURCE_ID, "date": day, "status": "available", "gaps": [], "observations": rows}
        (folder / f"{day}.json").write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
    return {"status": "read", "posts": len(posts), "accounts": len(accounts)}
