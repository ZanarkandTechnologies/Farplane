"""Each running test's versions, counted where their numbers live, by `farplane metrics refresh`.

A test (Convex `abTests`) compares versions. A version that names a `metricSource` is counted here once a
day, from the moment its test started:

- `whop_plan`: the plan's paid sales (successes) out of every payment attempted on it (attempts). Whop
  doesn't report checkout views, so attempts are payments tried, not visitors.
- `zernio_posts`: the listed posts' clicks (successes) out of their views (attempts). The ref is the post
  ids, comma-separated.

The totals go to Convex (`/experiments/ab`, op `source-totals`); a rerun the same day replaces them. A source
it can't read is reported as a gap, never written as zero. Versions of other kinds are left to whoever runs
that step (`office-ab outcome`).
"""

from __future__ import annotations

import json
import re
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

WHOP = "https://api.whop.com/api/v1"
ZERNIO = "https://zernio.com/api/v1"
Fetch = Callable[[str, str], Any]


def _get(url: str, api_key: str) -> Any:
    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def _ms(value: Any) -> int | None:
    if not value:
        return None
    try:
        return int(datetime.fromisoformat(str(value).replace("Z", "+00:00")).timestamp() * 1000)
    except ValueError:
        return None


def whop_company(bindings_text: str) -> str | None:
    """The Whop company a business repo binds: `whop:` then `company: biz_…` in farplane/bindings.yaml."""
    match = re.search(r"^whop:\s*\n(?:[ \t]+.*\n)*?[ \t]+company:\s*['\"]?(biz_[A-Za-z0-9]+)", bindings_text, re.M)
    return match.group(1) if match else None


def whop_plan_totals(company: str, plan: str, since_ms: int, api_key: str, fetch: Fetch = _get) -> tuple[int, int]:
    """(paid sales, payments attempted) on one plan since a moment, newest pages first."""
    successes = attempts = 0
    after = None
    while True:
        query = {"account_id": company, "first": 100, **({"after": after} if after else {})}
        body = fetch(f"{WHOP}/payments?{urllib.parse.urlencode(query)}", api_key)
        rows = body.get("data") or []
        for payment in rows:
            if payment.get("plan_id") != plan or (_ms(payment.get("created_at")) or 0) < since_ms:
                continue
            attempts += 1
            paid = payment.get("status") == "paid" and float(payment.get("usd_total") or 0) > 0
            successes += 1 if paid and not payment.get("refunded_at") else 0
        info = body.get("page_info") or {}
        oldest = min((_ms(p.get("created_at")) or 0 for p in rows), default=0)
        if not info.get("has_next_page") or oldest < since_ms:
            return successes, attempts
        after = info.get("end_cursor")


def zernio_post_totals(post_ids: list[str], api_key: str, fetch: Fetch = _get) -> tuple[int, int]:
    """(clicks, views) across the listed Zernio posts."""
    clicks = views = 0
    for post_id in post_ids:
        body = fetch(f"{ZERNIO}/analytics?{urllib.parse.urlencode({'postId': post_id})}", api_key)
        analytics = (body.get("analytics") or (body.get("posts") or [{}])[0].get("analytics") or {}) if isinstance(body, dict) else {}
        clicks += int(analytics.get("clicks") or 0) + int(analytics.get("websiteClicks") or 0)
        views += int(analytics.get("views") or 0)
    return clicks, views


def refresh_versions(
    tests: list[dict[str, Any]],
    roots: dict[str, Path],
    keys: dict[str, str],
    record: Callable[[dict[str, Any]], Any],
    now_ms: int,
    fetch: Fetch = _get,
) -> list[dict[str, Any]]:
    """Counts every running test's sourced versions and records the totals; one result line per version."""
    results: list[dict[str, Any]] = []
    for test in tests:
        since = _ms(test.get("startedAt"))
        if test.get("status") != "running" or since is None:
            continue
        for option in test.get("options") or []:
            source = option.get("metricSource") or {}
            kind, ref = source.get("kind"), str(source.get("ref") or "")
            line = {"test": f"{test.get('project')}/{test.get('id')}", "version": option.get("id"), "kind": kind}
            try:
                if kind == "whop_plan":
                    root = roots.get(str(test.get("project")))
                    bindings = root / "farplane" / "bindings.yaml" if root else None
                    company = whop_company(bindings.read_text(encoding="utf-8")) if bindings and bindings.exists() else None
                    if not company or not keys.get("whop"):
                        results.append({**line, "status": "gap", "reason": "no Whop company bound or no WHOP_API_KEY"})
                        continue
                    successes, attempts = whop_plan_totals(company, ref, since, keys["whop"], fetch)
                elif kind == "zernio_posts":
                    if not keys.get("zernio"):
                        results.append({**line, "status": "gap", "reason": "no ZERNIO_API_KEY"})
                        continue
                    successes, attempts = zernio_post_totals([p.strip() for p in ref.split(",") if p.strip()], keys["zernio"], fetch)
                else:
                    continue
            except Exception as exc:  # a source down is that version's gap; the rest carry on
                results.append({**line, "status": "gap", "reason": f"{kind} unreadable: {type(exc).__name__}"})
                continue
            record({"op": "source-totals", "project": test.get("project"), "testId": test.get("id"), "option": option.get("id"), "successes": successes, "attempts": max(attempts, successes), "at": now_ms})
            results.append({**line, "status": "counted", "successes": successes, "attempts": max(attempts, successes)})
    return results
