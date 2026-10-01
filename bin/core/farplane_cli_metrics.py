"""The `farplane metrics` and `farplane loop` commands: the daily metrics job and the weekly loop."""

from __future__ import annotations

import argparse
import os

from farplane_cli_base import DEFAULT_CODEX_HOME
from farplane_cli_commands import run_loop_monday_cli, run_metrics_primitives_cli, run_metrics_push_cli, run_metrics_refresh_cli


def add_metrics_and_loop(sub: argparse._SubParsersAction) -> None:
    metrics = sub.add_parser("metrics", help="Today's metric readings for every project, and Convex.")
    metrics_sub = metrics.add_subparsers(dest="metrics_command")
    metrics_refresh = metrics_sub.add_parser(
        "refresh",
        help="The daily job: each project's readings and snapshot for today, then one push to Convex.",
    )
    metrics_refresh.add_argument("--project-root", help="Only this project (default: every company.json project).")
    metrics_refresh.add_argument("--date", help="YYYY-MM-DD. Defaults to today on this machine's clock.")
    metrics_refresh.add_argument("--cash", type=float, help="Record a cash balance (USD) the operator reported.")
    metrics_refresh.add_argument("--no-push", action="store_true", help="Write readings and snapshots, skip Convex.")
    metrics_refresh.add_argument("--codex-home", default=str(DEFAULT_CODEX_HOME))
    metrics_refresh.add_argument("--json", action="store_true")
    metrics_refresh.set_defaults(func=run_metrics_refresh_cli)
    metrics_primitives = metrics_sub.add_parser("primitives", help="Refresh Core primitive metrics for one project/date.")
    metrics_primitives.add_argument("--project-root", default=os.getcwd())
    metrics_primitives.add_argument("--date", help="Snapshot date in YYYY-MM-DD. Defaults to today on this machine's clock.")
    metrics_primitives.add_argument("--codex-home", default=str(DEFAULT_CODEX_HOME))
    metrics_primitives.add_argument("--monthly-spend", type=float, help="Optional monthly AI subscription spend for burn allocation.")
    metrics_primitives.add_argument("--ticket-status", help="Optional ticket status/phase filter for companion ticket_count_by_kpi_status readings.")
    metrics_primitives.add_argument("--no-write", action="store_true", help="Print readings without writing .farplane metric files.")
    metrics_primitives.add_argument("--json", action="store_true")
    metrics_primitives.set_defaults(func=run_metrics_primitives_cli)
    metrics_push = metrics_sub.add_parser("push", help="Send snapshot readings and the company's Whop cash to Convex.")
    metrics_push.add_argument("--project-root", help="Push only this project's snapshot (default: all, plus cash).")
    metrics_push.add_argument("--cash", type=float, help="Record a cash balance (USD) the operator reported.")
    metrics_push.add_argument("--json", action="store_true")
    metrics_push.set_defaults(func=run_metrics_push_cli)

    loop = sub.add_parser("loop", help="Run the business loop's step plans in the office.")
    loop_sub = loop.add_subparsers(dest="loop_command")
    loop_monday = loop_sub.add_parser(
        "monday",
        help="Review each step plan's output week on week and seed this week's routine tasks on its floor's queue.",
    )
    loop_monday.add_argument("--office", help="Folder the office runs in (holds .agent-office). Default: $AGENT_OFFICE_DIR or here.")
    loop_monday.add_argument("--today", help="The run's date, YYYY-MM-DD. Default: today.")
    loop_monday.add_argument("--dry-run", action="store_true", help="Compute quotas without queueing.")
    loop_monday.add_argument("--json", action="store_true")
    loop_monday.set_defaults(func=run_loop_monday_cli)
