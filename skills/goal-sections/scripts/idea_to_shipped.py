#!/usr/bin/env python3
"""Idea to shipped: median days from a GitHub issue opening to closing as done.

Reads closed issues through `gh` for one repository and prints the median, the
slowest quarter and the same-day share over a recent window. Issues closed as
"not planned" are left out.
"""
import argparse
import json
import statistics
import subprocess
from datetime import datetime, timedelta, timezone


def parse(stamp: str) -> datetime:
    return datetime.fromisoformat(stamp.replace("Z", "+00:00"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default="ZanarkandTechnologies/Farplane")
    parser.add_argument("--days", type=int, default=30)
    args = parser.parse_args()

    raw = subprocess.run(
        ["gh", "issue", "list", "--repo", args.repo, "--state", "closed", "--limit", "500",
         "--json", "createdAt,closedAt,stateReason"],
        check=True, capture_output=True, text=True,
    ).stdout
    since = datetime.now(timezone.utc) - timedelta(days=args.days)
    days = sorted(
        (parse(i["closedAt"]) - parse(i["createdAt"])).total_seconds() / 86400
        for i in json.loads(raw)
        if i.get("stateReason") != "NOT_PLANNED" and parse(i["closedAt"]) >= since
    )
    if not days:
        print(json.dumps({"repo": args.repo, "window_days": args.days, "issues": 0}))
        return
    print(json.dumps({
        "repo": args.repo,
        "window_days": args.days,
        "issues": len(days),
        "median_days": round(statistics.median(days), 2),
        "slowest_quarter_over_days": round(days[int(len(days) * 0.75)], 2),
        "same_day_share": round(sum(d < 1 for d in days) / len(days), 2),
    }))


if __name__ == "__main__":
    main()
