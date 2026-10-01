"""`farplane metrics push`: send snapshot metric readings and the company's cash to Convex.

Each project's `.farplane/project/ui/latest.json` holds every metric's observed series; each point becomes
one reading (project slug from company.json, metric id, value, day). Cash is the Whop balance of every
company a project binds (`whop: company:` in its `farplane/bindings.yaml`), summed as metric `cash`
(source `whop`) for project `company`; the operator can also report a balance (`--cash`, source
`operator`). There is no bank feed. The deployment replaces a reading with the same project + metric +
time, so pushing again the same day is safe.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

try:
    from farplane_convex import ConvexUnavailable, convex_settings, project_slug, push_readings, to_ms
    from runtime_config import farplane_home
except ImportError:  # pragma: no cover - package import path used by tests
    from bin.core.farplane_convex import ConvexUnavailable, convex_settings, project_slug, push_readings, to_ms
    from bin.core.runtime_config import farplane_home

SNAPSHOT_PATH = Path(".farplane") / "project" / "ui" / "latest.json"
COMPANY_PROJECT = "company"  # the company's own numbers (cash) in Convex
METRIC_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,99}$")


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def display(value: float, unit: str) -> str:
    if float(value).is_integer():
        number = f"{value:,.0f}"
    elif abs(value) >= 1:
        number = f"{value:,.2f}"
    else:
        number = f"{value:.4g}"
    if unit.upper() == "USD":
        return f"-${number[1:]}" if number.startswith("-") else f"${number}"
    return f"{number} {unit}".strip()


def reading(project: str, metric: str, value: float, unit: str, at: int, source: str, note: str = "") -> dict[str, Any]:
    row: dict[str, Any] = {
        "project": project,
        "metric": metric,
        "value": value,
        "display": display(value, unit),
        "at": at,
        "source": source[:60],
    }
    if unit:
        row["unit"] = unit[:40]
    if note:
        row["note"] = note[:500]
    return row


def snapshot_readings(snapshot: dict[str, Any], project: str) -> tuple[list[dict[str, Any]], list[str]]:
    """Every available point of every metric series the snapshot holds."""
    metrics = snapshot.get("metrics") if isinstance(snapshot.get("metrics"), dict) else {}
    definitions = metrics.get("definitions") if isinstance(metrics.get("definitions"), dict) else {}
    by_key: dict[tuple[str, int], dict[str, Any]] = {}
    gaps: list[str] = []
    for card in metrics.get("series") or []:
        if not isinstance(card, dict):
            continue
        metric_id = str(card.get("metric_id") or "")
        if not METRIC_ID.match(metric_id):
            gaps.append(f"invalid_metric_id:{metric_id[:60]}")
            continue
        recipe = definitions.get(metric_id) if isinstance(definitions.get(metric_id), dict) else {}
        unit = str(card.get("unit") or recipe.get("unit") or "")
        source = str(recipe.get("refresh_ref") or recipe.get("primitive_id") or card.get("primitive_id") or "snapshot")
        for point in card.get("series") or []:
            value = point.get("value") if isinstance(point, dict) else None
            at = to_ms(point.get("date")) if isinstance(point, dict) else None
            if at is None or isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                continue
            by_key[(metric_id, at)] = reading(project, metric_id, float(value), unit, at, source)
    return list(by_key.values()), gaps


def cash_metric(currency: str, account: str) -> str:
    """`cash` for the USD balance; another currency or a named account gets its own metric id."""
    metric = "cash"
    if account:
        metric += "." + project_slug(account)
    if currency and currency.upper() != "USD":
        metric += "." + currency.lower()
    return metric


WHOP_COMPANY = re.compile(r"^whop:\s*\n(?:[ \t]+.*\n)*?[ \t]+company:\s*['\"]?(biz_[A-Za-z0-9]+)", re.MULTILINE)
WHOP_LEDGER = "https://api.whop.com/api/v1/ledger_accounts/{company}"


def whop_companies(roots: list[Path]) -> list[str]:
    """Whop companies bound by the projects' `farplane/bindings.yaml`, once each."""
    found: list[str] = []
    for root in roots:
        try:
            text = (root / "farplane" / "bindings.yaml").read_text(encoding="utf-8")
        except OSError:
            continue
        match = WHOP_COMPANY.search(text + "\n")
        if match and match.group(1) not in found:
            found.append(match.group(1))
    return found


def today_ms() -> int:
    return int(time.mktime(time.strptime(time.strftime("%Y-%m-%d"), "%Y-%m-%d")) * 1000)


def whop_cash_readings(companies: list[str], api_key: str, fetch=None) -> tuple[list[dict[str, Any]], list[str]]:
    """Today's summed Whop balance (USD) as `cash`; a company Whop won't show is a gap, never zero."""
    if not companies:
        return [], ["no_whop_company_bound"]
    if not api_key:
        return [], ["whop_api_key_missing"]
    fetch = fetch or _whop_get
    total, read, gaps = 0.0, [], []
    for company in companies:
        try:
            body = fetch(WHOP_LEDGER.format(company=company), api_key)
        except urllib.error.HTTPError as exc:
            gaps.append(f"whop_balance_{exc.code}:{company}" + (" (the key needs company:balance:read)" if exc.code == 403 else ""))
            continue
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            gaps.append(f"whop_unreachable:{company}:{str(exc)[:80]}")
            continue
        treasury = body.get("treasury_balance") if isinstance(body, dict) else None
        value = treasury.get("balance_usd") if isinstance(treasury, dict) else None
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            gaps.append(f"whop_balance_missing:{company}")
            continue
        total += float(value)
        read.append(company)
    if not read:
        return [], gaps
    note = "Whop balance of " + ", ".join(read) + ("; missing " + ", ".join(gaps) if gaps else "")
    return [reading(COMPANY_PROJECT, "cash", total, "USD", today_ms(), "whop", note)], gaps


def _whop_get(url: str, api_key: str) -> Any:
    request = urllib.request.Request(url, headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def company_projects(home: Path) -> list[dict[str, Any]]:
    company = read_json(home / "company.json")
    projects = company.get("projects") if isinstance(company, dict) else company
    return [row for row in projects or [] if isinstance(row, dict)]


def project_for_root(projects: list[dict[str, Any]], root: Path) -> dict[str, Any] | None:
    for row in projects:
        context = str(row.get("trackingContext") or "")
        if context and Path(context).expanduser().resolve() == root:
            return row
    return None


def push_project(root: Path, slug: str, settings: dict[str, str]) -> dict[str, Any]:
    snapshot = read_json(root / SNAPSHOT_PATH)
    if not isinstance(snapshot, dict):
        return {"project": slug, "status": "skipped", "reason": f"no {SNAPSHOT_PATH}"}
    readings, gaps = snapshot_readings(snapshot, slug)
    result: dict[str, Any] = {"project": slug, "status": "pushed", "readings": len(readings), "gaps": gaps}
    result.update(push_readings(readings, settings))
    return result


def run_push(args: argparse.Namespace) -> int:
    home = farplane_home()
    projects = company_projects(home)
    settings = convex_settings()
    results: list[dict[str, Any]] = []
    if args.project_root:
        root = Path(args.project_root).expanduser().resolve()
        row = project_for_root(projects, root)
        targets = [(root, project_slug(str(row.get("name") or "")) if row else "")]
    else:
        targets = [
            (Path(str(row["trackingContext"])).expanduser().resolve(), project_slug(str(row.get("name") or "")))
            for row in projects
            if row.get("trackingContext")
        ]
    for root, slug in targets:
        if not slug:
            results.append({"project": str(root), "status": "skipped", "reason": "not a company.json project"})
            continue
        try:
            results.append(push_project(root, slug, settings))
        except ConvexUnavailable as exc:
            results.append({"project": slug, "status": "failed", "reason": str(exc)})
    if not args.project_root:
        if getattr(args, "cash", None) is not None:
            cash = [reading(COMPANY_PROJECT, "cash", float(args.cash), "USD", today_ms(), "operator", "reported by the operator")]
            gaps: list[str] = []
        else:
            cash, gaps = whop_cash_readings(whop_companies([root for root, _ in targets]), os.environ.get("WHOP_API_KEY", "").strip())
        try:
            pushed = push_readings(cash, settings) if cash else {"inserted": 0, "updated": 0}
            results.append({"project": COMPANY_PROJECT, "status": "pushed", "readings": len(cash), "gaps": gaps, **pushed})
        except ConvexUnavailable as exc:
            results.append({"project": COMPANY_PROJECT, "status": "failed", "reason": str(exc)})

    if args.json:
        print(json.dumps({"results": results}, indent=2, sort_keys=True))
    else:
        for row in results:
            if row["status"] == "pushed":
                print(f"{row['project']}: pushed {row['readings']} readings ({row['inserted']} new, {row['updated']} replaced)")
            else:
                print(f"{row['project']}: {row['status']} ({row['reason']})")
    return 1 if any(row["status"] == "failed" for row in results) else 0
