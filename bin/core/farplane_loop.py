"""`farplane loop monday`: the Monday run of each floor's step plans (the bunker PRD's "The operating loop").

For every floor of the running office that has a step plan (the front matter of `farplane/strategy/<step>.md`,
read by the office itself through `/office/local/plans`):

- review last week: the output metric's last reading of last week against the week before's, and whether it
  got worse two weeks running (Convex `/metrics/history`). Proposing the one change is the Morning job's call
  (`office-queue suggest`); this only gathers the numbers.
- seed this week: the office counts what the input has done since the plan began, with the CEO desk's own
  rule (`doneSince`, from the floor's metric snapshot and Convex history), turns it into this week's quota
  (`weeklyQuota`) and queues that many routine tasks, each carrying the strategy doc and the running test's
  pick, each once (`/office/local/seed`), so a rerun adds nothing. The rule lives only in the office.

A step whose input has no reading since the plan began is reported blocked, not seeded. Floors with no step
plan are named once under `skipped`.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Mapping
from urllib import error, request

try:
    from farplane_convex import ConvexUnavailable, convex_settings, site_post
except ImportError:  # pragma: no cover - package import path used by tests
    from bin.core.farplane_convex import ConvexUnavailable, convex_settings, site_post

STEPS = ("offer", "leads", "sales", "delivery")
TIMEOUT_SECS = 20.0
BY = "the Morning job"


class OfficeUnavailable(RuntimeError):
    """The office isn't running here, or refused; the message says which, never the token."""


def find_office(folder: Path) -> dict[str, str]:
    """The office's address and local token, from the `.agent-office` folder it writes them to on start."""
    for data in (folder / ".agent-office", folder):
        try:
            port = (data / "hook-port").read_text(encoding="utf-8").strip()
            token = (data / "local-token").read_text(encoding="utf-8").strip()
        except OSError:
            continue
        if port.isdigit() and token:
            return {"url": f"http://127.0.0.1:{port}", "token": token}
    raise OfficeUnavailable(f"no office in {folder}: start it, or pass --office <the folder it runs in>")


def office_call(office: Mapping[str, str], method: str, route: str, body: Mapping[str, Any] | None = None) -> dict[str, Any]:
    data = json.dumps(dict(body)).encode("utf-8") if body is not None else None
    headers = {"Authorization": f"Bearer {office['token']}"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = request.Request(f"{office['url']}/office/local/{route}", data=data, headers=headers, method=method)
    try:
        with request.urlopen(req, timeout=TIMEOUT_SECS) as response:
            return json.loads(response.read() or b"{}")
    except error.HTTPError as exc:
        try:
            reason = str(json.loads(exc.read() or b"{}").get("error") or "")
        except (ValueError, OSError, AttributeError):
            reason = ""
        raise OfficeUnavailable(f"/office/local/{route}: HTTP {exc.code}{': ' + reason[:200] if reason else ''}") from None
    except (error.URLError, TimeoutError, OSError) as exc:
        raise OfficeUnavailable(f"/office/local/{route}: unreachable ({getattr(exc, 'reason', exc)})") from None


def week_start(day: date) -> date:
    return day - timedelta(days=day.weekday())


def ms(day: date) -> int:
    return int(datetime(day.year, day.month, day.day, tzinfo=timezone.utc).timestamp() * 1000)


def review(readings: list[dict[str, Any]], monday: date) -> dict[str, Any]:
    """Last week's last output reading against the week before's (higher is better), and the week before that."""
    weeks: list[float | None] = []
    for back in (1, 2, 3):
        start, end = ms(monday - timedelta(days=7 * back)), ms(monday - timedelta(days=7 * (back - 1)))
        inside = [r for r in readings if isinstance(r.get("value"), (int, float)) and start <= int(r.get("at") or 0) < end]
        weeks.append(float(max(inside, key=lambda r: r["at"])["value"]) if inside else None)
    last, before, third = weeks
    if last is None or before is None:
        verdict = "no readings" if last is None and before is None else "one week only"
    else:
        verdict = "better" if last > before else "worse" if last < before else "same"
    worse_twice = None not in weeks and last < before < third  # type: ignore[operator]
    return {"last_week": last, "week_before": before, "verdict": verdict, "worse_two_weeks_running": worse_twice}


def run_monday(args: argparse.Namespace) -> int:
    today = date.fromisoformat(args.today) if args.today else date.today()
    monday = week_start(today)
    folder = Path(args.office or os.environ.get("AGENT_OFFICE_DIR") or os.getcwd()).expanduser()
    try:
        office = find_office(folder)
        floors = office_call(office, "GET", "plans").get("floors") or []
    except OfficeUnavailable as exc:
        print(json.dumps({"status": "blocked", "reason": str(exc)}) if args.json else f"blocked: {exc}")
        return 1
    settings = convex_settings()
    steps: list[dict[str, Any]] = []
    skipped: list[str] = []
    for floor in floors:
        plans = {step: plan for step, plan in (floor.get("plans") or {}).items() if step in STEPS and plan}
        if not plans:
            skipped.append(str(floor.get("name") or floor.get("id")))
            continue
        project = str(floor.get("project") or floor["id"])  # the floor's Convex project, as the office reads it
        for step, plan in plans.items():
            row: dict[str, Any] = {"floor": floor["id"], "project": project, "step": step, "input": plan["input"]["metric"], "output": plan["output"]["metric"]}
            try:
                history = site_post(
                    "/metrics/history",
                    {"project": project, "metric": plan["output"]["metric"], "since": ms(monday - timedelta(days=21))},
                    settings,
                ) or []
                row["review"] = review(history, monday)
            except ConvexUnavailable as exc:
                row["review"] = {"verdict": "unknown", "gap": str(exc)}
            body = {"floor": floor["id"], "step": step, "today": today.isoformat(), "by": BY, "dryRun": bool(args.dry_run)}
            try:
                seeded = office_call(office, "POST", "seed", body)
            except OfficeUnavailable as exc:
                row.update(status="failed", reason=str(exc))
            else:
                if seeded.get("blocked"):
                    row.update(status="blocked", reason=str(seeded["blocked"]))
                else:
                    row.update(status="dry-run" if args.dry_run else "seeded", **{k: seeded.get(k) for k in ("week", "done", "target", "weeksLeft", "quota", "added")})
            steps.append(row)

    result = {"today": today.isoformat(), "monday": monday.isoformat(), "steps": steps, "skipped": skipped}
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for row in steps:
            rv = row.get("review") or {}
            head = f"{row['floor']} {row['step']}: "
            if row["status"] in ("seeded", "dry-run"):
                print(f"{head}{row['done']}/{row['target']} done, {row['weeksLeft']} weeks left, quota {row['quota']}, {row['added']} queued ({row['week']}); output {rv.get('verdict')}")
            else:
                print(f"{head}{row['status']}: {row.get('reason')}; output {rv.get('verdict')}")
        if skipped:
            print(f"No step plans yet: {', '.join(skipped)}")
    return 0
