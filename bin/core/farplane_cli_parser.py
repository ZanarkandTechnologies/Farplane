"""Argument parser construction for the Farplane CLI."""

from __future__ import annotations

import argparse
import os
from datetime import datetime, timezone

from farplane_cli_base import CORE_ROOT, DEFAULT_CODEX_HOME
from farplane_cli_commands import (
    run_adoption_scan_cli, run_content_add_cli, run_content_list_cli,
    run_content_select_cli, run_content_validate_cli, run_doctor,
    run_entities_compile_cli, run_harness_health_compile_cli,
    run_metrics_primitives_cli, run_mining_cli, run_project_snapshot_cli,
    run_reports_index_cli, run_reports_repair_refs_cli, run_response_check_cli,
    run_skill_rollout_scan_cli, run_ticket_finalize_cli, run_ticket_history_cli,
    run_validate_ticket,
)
from farplane_cli_hooks import (
    run_hooks_doctor, run_hooks_install, run_hooks_list, run_install,
    run_with_doppler,
)
from farplane_cli_ui import (
    delegate_to_ui, run_notify_disable, run_notify_enable, run_notify_status,
    run_ui_link, run_ui_start,
)

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="farplane",
        description="Farplane Core CLI for install, hooks, doctor, and UI module routing.",
    )
    sub = parser.add_subparsers(dest="command")

    install = sub.add_parser("install", help="Install/reinstall Farplane Core into Codex home.")
    install.add_argument("--target", help="Codex home target. Defaults to ~/.codex.")
    install.add_argument("--dry-run", action="store_true", help="Print the install command without running it.")
    install.add_argument("extra", nargs=argparse.REMAINDER, help="Extra install.sh args after --.")
    install.set_defaults(func=run_install)

    doctor = sub.add_parser("doctor", help="Check Core install, hooks, config, and linked UI repo.")
    doctor.add_argument("--target", help="Codex home target. Defaults to stored codexHome or ~/.codex.")
    doctor.add_argument("--json", action="store_true")
    doctor.set_defaults(func=run_doctor)

    run = sub.add_parser("run", help="Run a command through this project's Doppler secret environment.")
    run.add_argument("--dry-run", action="store_true", help="Print the Doppler-wrapped command without running it.")
    run.add_argument("extra", nargs=argparse.REMAINDER, help="Command to run after --.")
    run.set_defaults(func=run_with_doppler)

    validate = sub.add_parser("validate", help="Run phase-aware Farplane validation.")
    validate_sub = validate.add_subparsers(dest="validate_command")
    validate_ticket_parser = validate_sub.add_parser("ticket", help="Validate one ticket at a lifecycle phase.")
    validate_ticket_parser.add_argument("ticket")
    validate_ticket_parser.add_argument("--phase", choices=("planning", "complete"), required=True)
    validate_ticket_parser.add_argument("--root", default=str(CORE_ROOT))
    validate_ticket_parser.add_argument("--path", action="append", default=[], help="Explicit changed path; may be repeated.")
    validate_ticket_parser.add_argument("--base", help="Explicit Git base ref used to derive committed changed paths.")
    validate_ticket_parser.add_argument("--no-write", action="store_true", help="Do not write the ticket validation receipt.")
    validate_ticket_parser.add_argument("--json", action="store_true")
    validate_ticket_parser.set_defaults(func=run_validate_ticket)

    hooks = sub.add_parser("hooks", help="Install or check Codex lifecycle hooks.")
    hooks_sub = hooks.add_subparsers(dest="hooks_command")
    hooks_list = hooks_sub.add_parser("list", help="List managed Core hook commands.")
    hooks_list.add_argument("--target", help="Codex home target. Defaults to ~/.codex.")
    hooks_list.add_argument("--json", action="store_true")
    hooks_list.set_defaults(func=run_hooks_list)
    hooks_install = hooks_sub.add_parser("install", help="Install/relink Core hooks through install.sh.")
    hooks_install.add_argument("--target", help="Codex home target. Defaults to ~/.codex.")
    hooks_install.add_argument("--dry-run", action="store_true")
    hooks_install.add_argument("--json", action="store_true")
    hooks_install.set_defaults(func=run_hooks_install)
    hooks_doctor_parser = hooks_sub.add_parser("doctor", help="Check hook links and rendered config.")
    hooks_doctor_parser.add_argument("--target", help="Codex home target. Defaults to ~/.codex.")
    hooks_doctor_parser.add_argument("--json", action="store_true")
    hooks_doctor_parser.set_defaults(func=run_hooks_doctor)
    notify = sub.add_parser("notify", help="Enable, disable, or inspect the Farplane turn-complete notify script.")
    notify_sub = notify.add_subparsers(dest="notify_command")
    notify_status = notify_sub.add_parser("status", help="Show whether the Farplane notify script is enabled.")
    notify_status.add_argument("--target", help="Codex home target. Defaults to stored codexHome or ~/.codex.")
    notify_status.add_argument("--json", action="store_true")
    notify_status.set_defaults(func=run_notify_status)
    notify_enable = notify_sub.add_parser("enable", help="Enable the Farplane notify script.")
    notify_enable.add_argument("--target", help="Codex home target. Defaults to stored codexHome or ~/.codex.")
    notify_enable.add_argument("--dry-run", action="store_true")
    notify_enable.add_argument("--json", action="store_true")
    notify_enable.set_defaults(func=run_notify_enable)
    notify_disable = notify_sub.add_parser("disable", help="Disable the Farplane notify script.")
    notify_disable.add_argument("--target", help="Codex home target. Defaults to stored codexHome or ~/.codex.")
    notify_disable.add_argument("--dry-run", action="store_true")
    notify_disable.add_argument("--json", action="store_true")
    notify_disable.set_defaults(func=run_notify_disable)

    ui = sub.add_parser("ui", help="Link or start the Farplane-UI checkout.")
    ui_sub = ui.add_subparsers(dest="ui_command")
    ui_link = ui_sub.add_parser("link", help="Store the Farplane-UI checkout path.")
    ui_link.add_argument("path")
    ui_link.add_argument("--json", action="store_true")
    ui_link.set_defaults(func=run_ui_link)
    ui_start = ui_sub.add_parser("start", help="Start the linked Farplane-UI dev server.")
    ui_start.add_argument("--dry-run", action="store_true")
    ui_start.add_argument("--json", action="store_true")
    ui_start.add_argument("extra", nargs=argparse.REMAINDER)
    ui_start.set_defaults(func=run_ui_start)

    resource_bank = sub.add_parser(
        "resource-bank",
        help="Delegate Resource Bank creative reference commands to Farplane-UI.",
    )
    resource_bank.add_argument("extra", nargs=argparse.REMAINDER)
    resource_bank.set_defaults(func=lambda args: delegate_to_ui("resource-bank", args.extra))

    bank = sub.add_parser("bank", help="Alias for `resource-bank`.")
    bank.add_argument("extra", nargs=argparse.REMAINDER)
    bank.set_defaults(func=lambda args: delegate_to_ui("bank", args.extra))

    delegate = sub.add_parser("delegate", help="Delegate a command to the linked Farplane-UI CLI.")
    delegate.add_argument("--dry-run", action="store_true")
    delegate.add_argument("delegate_command")
    delegate.add_argument("extra", nargs=argparse.REMAINDER)
    delegate.set_defaults(func=lambda args: delegate_to_ui(args.delegate_command, args.extra, args.dry_run))

    adoption = sub.add_parser("adoption", help="Inspect Farplane adoption across local project manifests.")
    adoption_sub = adoption.add_subparsers(dest="adoption_command")
    adoption_scan = adoption_sub.add_parser("scan", help="Resolve project manifest pins, drift, and local skill presence.")
    adoption_scan.add_argument("--standard-root", default=str(CORE_ROOT))
    adoption_scan.add_argument("--project-root", action="append", help="Project root to scan. May be repeated.")
    adoption_scan.add_argument("--roots-file", help="JSON file containing project roots.")
    adoption_scan.add_argument("--no-state", action="store_true", help="Do not read ~/.farplane global state project roots.")
    adoption_scan.add_argument("--include-standard", action="store_true", help="Scan the standard root when no project roots are found.")
    adoption_scan.add_argument("--feature-registry", help="Feature registry JSONL path.")
    adoption_scan.add_argument("--template-registry", help="Template registry JSONL path.")
    adoption_scan.add_argument("--json", action="store_true")
    adoption_scan.set_defaults(func=run_adoption_scan_cli)

    skills = sub.add_parser("skills", help="Inspect Farplane skill rollout and registry projections.")
    skills_sub = skills.add_subparsers(dest="skills_command")
    skills_rollout = skills_sub.add_parser("rollout", help="Inspect skill rollout status.")
    skills_rollout_sub = skills_rollout.add_subparsers(dest="skills_rollout_command")
    skills_rollout_scan = skills_rollout_sub.add_parser("scan", help="Resolve skill rollout status for UI rendering.")
    skills_rollout_scan.add_argument("--standard-root", default=str(CORE_ROOT))
    skills_rollout_scan.add_argument("--registry", help="Skill registry JSONL path.")
    skills_rollout_scan.add_argument("--intelligence", help="Skill template intelligence JSON path.")
    skills_rollout_scan.add_argument("--json", action="store_true")
    skills_rollout_scan.set_defaults(func=run_skill_rollout_scan_cli)

    harness = sub.add_parser("harness", help="Compile and inspect local harness projections.")
    harness_sub = harness.add_subparsers(dest="harness_command")
    harness_health = harness_sub.add_parser("health", help="Compile local skill, eval, and rollout health.")
    harness_health_sub = harness_health.add_subparsers(dest="harness_health_command")
    harness_health_compile = harness_health_sub.add_parser(
        "compile", help="Write .farplane/state/harness-health.json."
    )
    harness_health_compile.add_argument("--project-root", default=os.getcwd())
    harness_health_compile.add_argument("--standard-root", default=str(CORE_ROOT))
    harness_health_compile.add_argument("--evals-root")
    harness_health_compile.add_argument("--output")
    harness_health_compile.add_argument("--date", default=datetime.now(timezone.utc).date().isoformat())
    harness_health_compile.add_argument("--no-write", action="store_true")
    harness_health_compile.add_argument("--json", action="store_true")
    harness_health_compile.set_defaults(func=run_harness_health_compile_cli)

    response = sub.add_parser("response", help="Inspect user-facing response budgets.")
    response_sub = response.add_subparsers(dest="response_command")
    response_check = response_sub.add_parser(
        "check", help="Count prose and report excluded presentation blocks."
    )
    response_check.add_argument("path", nargs="?", help="Markdown file; stdin when omitted.")
    response_check.add_argument("--stdin", action="store_true", help="Read Markdown from stdin.")
    response_check.add_argument("--max-words", type=int, default=500)
    response_check.add_argument("--max-lines", type=int, default=20)
    response_check.add_argument("--json", action="store_true")
    response_check.set_defaults(func=run_response_check_cli)

    ticket = sub.add_parser("ticket", help="Apply canonical Farplane ticket lifecycle transitions.")
    ticket_sub = ticket.add_subparsers(dest="ticket_command")
    ticket_finalize = ticket_sub.add_parser(
        "finalize",
        help="Verify a closed issue, mine completion, index it, and delete the local packet.",
    )
    ticket_finalize.add_argument("ticket_id")
    ticket_finalize.add_argument("--github-issue-url", required=True)
    ticket_finalize.add_argument("--project-root", default=os.getcwd())
    ticket_finalize.add_argument("--json", action="store_true")
    ticket_finalize.set_defaults(func=run_ticket_finalize_cli)

    tickets = sub.add_parser("tickets", help="Inspect Farplane ticket projections.")
    tickets_sub = tickets.add_subparsers(dest="tickets_command")
    tickets_history = tickets_sub.add_parser(
        "history",
        help="Query compact active and archived ticket Reward history.",
    )
    from farplane_ticket_history import add_history_arguments

    add_history_arguments(tickets_history)
    tickets_history.set_defaults(func=run_ticket_history_cli)

    metrics = sub.add_parser("metrics", help="Refresh Farplane primitive metric readings.")
    metrics_sub = metrics.add_subparsers(dest="metrics_command")
    metrics_primitives = metrics_sub.add_parser("primitives", help="Refresh Core primitive metrics for one project/date.")
    metrics_primitives.add_argument("--project-root", default=os.getcwd())
    metrics_primitives.add_argument("--date", help="Snapshot date in YYYY-MM-DD. Defaults to today UTC.")
    metrics_primitives.add_argument("--codex-home", default=str(DEFAULT_CODEX_HOME))
    metrics_primitives.add_argument("--monthly-spend", type=float, help="Optional monthly AI subscription spend for burn allocation.")
    metrics_primitives.add_argument("--ticket-status", help="Optional ticket status/phase filter for companion ticket_count_by_kpi_status readings.")
    metrics_primitives.add_argument("--no-write", action="store_true", help="Print readings without writing .farplane metric files.")
    metrics_primitives.add_argument("--json", action="store_true")
    metrics_primitives.set_defaults(func=run_metrics_primitives_cli)

    project = sub.add_parser("project", help="Compile project-level projections for UI and intervals.")
    project_sub = project.add_subparsers(dest="project_command")
    project_snapshot = project_sub.add_parser("snapshot", help="Write .farplane/project/ui/latest.json.")
    project_snapshot.add_argument("--project-root", default=os.getcwd())
    project_snapshot.add_argument("--date", help="Metric date in YYYY-MM-DD. Defaults to latest daily metrics snapshot.")
    project_snapshot.add_argument("--no-write", action="store_true")
    project_snapshot.add_argument("--json", action="store_true")
    project_snapshot.set_defaults(func=run_project_snapshot_cli)

    reports = sub.add_parser("reports", help="Build Core-owned report registries.")
    reports_sub = reports.add_subparsers(dest="reports_command")
    reports_index = reports_sub.add_parser("index", help="Write .farplane/reports/index.json from report Markdown frontmatter.")
    reports_index.add_argument("--project-root", default=os.getcwd())
    reports_index.add_argument("--no-write", action="store_true")
    reports_index.add_argument("--json", action="store_true")
    reports_index.set_defaults(func=run_reports_index_cli)
    reports_repair_refs = reports_sub.add_parser(
        "repair-refs",
        help="Add missing path-derived report refs, then rebuild .farplane/reports/index.json.",
    )
    reports_repair_refs.add_argument("--project-root", default=os.getcwd())
    reports_repair_refs.add_argument("--no-write", action="store_true")
    reports_repair_refs.add_argument("--no-index", action="store_true")
    reports_repair_refs.add_argument("--json", action="store_true")
    reports_repair_refs.set_defaults(func=run_reports_repair_refs_cli)

    entities = sub.add_parser("entities", help="Compile flat Markdown-owned entities into generated views.")
    entities_sub = entities.add_subparsers(dest="entities_command")
    entities_compile = entities_sub.add_parser(
        "compile",
        help="Write .farplane/entities/index.json, world.json, and crm.json from flat entity Markdown.",
    )
    entities_compile.add_argument("--project-root", default=os.getcwd())
    entities_compile.add_argument("--no-write", action="store_true")
    entities_compile.add_argument("--json", action="store_true")
    entities_compile.set_defaults(func=run_entities_compile_cli)

    mining = sub.add_parser("mining", help="Capture, route, replay, and inspect Core mining runs.")
    mining_sub = mining.add_subparsers(dest="mining_group")

    mining_programs = mining_sub.add_parser("programs", help="Inspect immutable Core mining programs.")
    mining_programs_sub = mining_programs.add_subparsers(dest="mining_action")
    mining_programs_list = mining_programs_sub.add_parser("list")
    mining_programs_list.add_argument("--project-root", default=os.getcwd())
    mining_programs_list.add_argument("--json", action="store_true")
    mining_programs_list.set_defaults(func=run_mining_cli)

    mining_routes = mining_sub.add_parser("routes", help="Inspect or edit project event routes.")
    mining_routes_sub = mining_routes.add_subparsers(dest="mining_action")
    for route_action in ("list", "validate"):
        route_parser = mining_routes_sub.add_parser(route_action)
        route_parser.add_argument("--project-root", default=os.getcwd())
        route_parser.add_argument("--json", action="store_true")
        route_parser.set_defaults(func=run_mining_cli)
    mining_routes_set = mining_routes_sub.add_parser("set")
    mining_routes_set.add_argument("route_id")
    mining_routes_set.add_argument("event_name")
    mining_routes_set.add_argument("program_ref")
    mining_routes_set.add_argument("--project-root", default=os.getcwd())
    mining_routes_set.add_argument("--json", action="store_true")
    mining_routes_set.set_defaults(func=run_mining_cli)
    mining_routes_remove = mining_routes_sub.add_parser("remove")
    mining_routes_remove.add_argument("route_id")
    mining_routes_remove.add_argument("--project-root", default=os.getcwd())
    mining_routes_remove.add_argument("--json", action="store_true")
    mining_routes_remove.set_defaults(func=run_mining_cli)

    mining_runs = mining_sub.add_parser("runs", help="Inspect or replay deterministic mining runs.")
    mining_runs_sub = mining_runs.add_subparsers(dest="mining_action")
    mining_runs_list = mining_runs_sub.add_parser("list")
    mining_runs_list.add_argument("--project-root", default=os.getcwd())
    mining_runs_list.add_argument("--json", action="store_true")
    mining_runs_list.set_defaults(func=run_mining_cli)
    for run_action in ("show", "replay", "rerun"):
        run_parser = mining_runs_sub.add_parser(run_action)
        run_parser.add_argument("run_id")
        run_parser.add_argument("--project-root", default=os.getcwd())
        run_parser.add_argument("--json", action="store_true")
        run_parser.set_defaults(func=run_mining_cli)

    mining_outputs = mining_sub.add_parser("outputs", help="Record reviewer verdicts for run outputs.")
    mining_outputs_sub = mining_outputs.add_subparsers(dest="mining_action")
    mining_outputs_verdict = mining_outputs_sub.add_parser("verdict")
    mining_outputs_verdict.add_argument("run_id")
    mining_outputs_verdict.add_argument("output_id")
    mining_outputs_verdict.add_argument("verdict", choices=("unreviewed", "promoted", "rejected"))
    mining_outputs_verdict.add_argument("--project-root", default=os.getcwd())
    mining_outputs_verdict.add_argument("--json", action="store_true")
    mining_outputs_verdict.set_defaults(func=run_mining_cli)

    mining_drain = mining_sub.add_parser("drain", help="Retry all pending local event routes.")
    mining_drain.add_argument("--project-root", default=os.getcwd())
    mining_drain.add_argument("--json", action="store_true")
    mining_drain.set_defaults(func=run_mining_cli, mining_action=None)

    mining_ticket = mining_sub.add_parser("ticket", help="Mine one completed ticket by canonical ID.")
    mining_ticket.add_argument("ticket_id")
    mining_ticket.add_argument("--project-root", default=os.getcwd())
    mining_ticket.add_argument("--json", action="store_true")
    mining_ticket.set_defaults(func=run_mining_cli, mining_action=None)

    content = sub.add_parser("content", help="Append or inspect local Farplane content ledger rows.")
    content_sub = content.add_subparsers(dest="content_command")
    content_add = content_sub.add_parser("add", help="Add or update a content ledger row.")
    content_add.add_argument("--project-root", default=str(CORE_ROOT))
    content_add.add_argument("--content-id")
    content_add.add_argument("--platform", required=True)
    content_add.add_argument("--external-id")
    content_add.add_argument("--url")
    content_add.add_argument("--status", default="posted")
    content_add.add_argument("--approval", default="approved")
    content_add.add_argument("--published-at")
    content_add.add_argument("--campaign")
    content_add.add_argument("--kpis", required=True, help="Comma-separated KPI IDs.")
    content_add.add_argument("--title")
    content_add.add_argument("--source-ref")
    content_add.add_argument("--approval-ref")
    content_add.add_argument("--notes")
    content_add.set_defaults(func=run_content_add_cli)
    content_list = content_sub.add_parser("list", help="List content ledger rows.")
    content_list.add_argument("--project-root", default=str(CORE_ROOT))
    content_list.add_argument("--platform")
    content_list.add_argument("--status")
    content_list.add_argument("--kpi")
    content_list.add_argument("--since-date", help="Only include content published on or after this UTC date.")
    content_list.add_argument("--until-date", help="Only include content published before this UTC date.")
    content_list.set_defaults(func=run_content_list_cli)
    content_validate = content_sub.add_parser("validate", help="Validate content ledger JSONL rows.")
    content_validate.add_argument("--project-root", default=str(CORE_ROOT))
    content_validate.set_defaults(func=run_content_validate_cli)
    content_select = content_sub.add_parser("select", help="Select posted content rows for metric refresh.")
    content_select.add_argument("--project-root", default=str(CORE_ROOT))
    content_select.add_argument("--platform", required=True)
    content_select.add_argument("--kpi", required=True)
    content_select.add_argument("--date", required=True, help="Snapshot date in YYYY-MM-DD.")
    content_select.add_argument("--window-days", type=int, default=7)
    content_select.set_defaults(func=run_content_select_cli)

    return parser
