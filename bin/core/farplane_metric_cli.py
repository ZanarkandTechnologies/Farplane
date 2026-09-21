"""CLI for Core-owned metric refresh and reducer helpers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from bin.core.farplane_metric_autonomy import (
    calculate_autonomy_savings,
    calculate_autonomy_time_ratio,
    calculate_ticket_intervention_metrics,
)
from bin.core.farplane_metric_refresh import (
    count_ticket_kpi_rewards,
    resolve_refresh_plan,
    select_content_metric_targets,
)

def print_json(payload: dict[str, Any]) -> int:
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect one Farplane metric reading.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    rewards = subparsers.add_parser("ticket-reward-count")
    rewards.add_argument("--ticket-dir", required=True)
    rewards.add_argument("--date", required=True)
    rewards.add_argument("--kpi-key", required=True)

    autonomy = subparsers.add_parser("autonomy-time-ratio")
    autonomy.add_argument("--runtime-dir", required=True)
    autonomy.add_argument("--date", required=True)

    interventions = subparsers.add_parser("ticket-intervention-metrics")
    interventions.add_argument("--ticket-dir", required=True)
    interventions.add_argument("--runtime-dir", required=True)
    interventions.add_argument("--date", required=True)

    savings = subparsers.add_parser("autonomy-savings")
    savings.add_argument("--ticket-dir", required=True)
    savings.add_argument("--runtime-dir", required=True)
    savings.add_argument("--date", required=True)
    savings.add_argument("--baseline-reasonable-hours", type=float)
    savings.add_argument("--baseline-max-hours", type=float)

    content_targets = subparsers.add_parser("content-targets")
    content_targets.add_argument("--content-ledger", required=True)
    content_targets.add_argument("--platform", required=True)
    content_targets.add_argument("--kpi-key", required=True)
    content_targets.add_argument("--date", required=True)
    content_targets.add_argument("--window-days", type=int, default=7)

    refresh_plan = subparsers.add_parser("refresh-plan")
    refresh_plan.add_argument("--metrics-file", required=True)
    refresh_plan.add_argument("--date", required=True)
    refresh_plan.add_argument("--metric-id", action="append", default=[])
    refresh_plan.add_argument("--fresh-metric-id", action="append", default=[])

    args = parser.parse_args()
    if args.command == "ticket-reward-count":
        return print_json(count_ticket_kpi_rewards(Path(args.ticket_dir), args.date, args.kpi_key))
    if args.command == "autonomy-time-ratio":
        return print_json(calculate_autonomy_time_ratio(Path(args.runtime_dir), args.date))
    if args.command == "ticket-intervention-metrics":
        return print_json(calculate_ticket_intervention_metrics(Path(args.ticket_dir), Path(args.runtime_dir), args.date))
    if args.command == "autonomy-savings":
        return print_json(calculate_autonomy_savings(Path(args.ticket_dir), Path(args.runtime_dir), args.date, args.baseline_reasonable_hours, args.baseline_max_hours))
    if args.command == "content-targets":
        return print_json(
            select_content_metric_targets(
                Path(args.content_ledger),
                args.platform,
                args.kpi_key,
                args.date,
                args.window_days,
            )
        )
    if args.command == "refresh-plan":
        return print_json(resolve_refresh_plan(Path(args.metrics_file), args.metric_id, args.date, set(args.fresh_metric_id)))
    return 2
