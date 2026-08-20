"""Domain command adapters for the Farplane CLI."""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import sys
from pathlib import Path
from typing import Any

from farplane_cli_base import (
    CONFIG_PATH, CORE_ROOT, DEFAULT_FARPLANE_HOME, CliError, load_config,
    print_payload,
)
from farplane_cli_hooks import hooks_doctor
from farplane_cli_ui import discover_ui_repo
from farplane_config_doctor import config_doctor
from validation.boundary import base_boundary, explicit_boundary, unavailable_boundary
from validation.run import validate_ticket
from validators.farplane_checks import build_registry

def run_adoption_scan_cli(args: argparse.Namespace) -> int:
    from farplane_adoption import run_scan

    return int(run_scan(args))


def run_skill_rollout_scan_cli(args: argparse.Namespace) -> int:
    from farplane_skill_rollout import SkillRolloutError, run_scan

    try:
        return int(run_scan(args))
    except SkillRolloutError as exc:
        print(f"farplane skill rollout: {exc}", file=sys.stderr)
        return 1


def run_harness_health_compile_cli(args: argparse.Namespace) -> int:
    from farplane_harness_health import HarnessHealthError, run_compile

    try:
        return int(run_compile(args))
    except HarnessHealthError as exc:
        print(f"farplane harness health: {exc}", file=sys.stderr)
        return 1


def run_response_check_cli(args: argparse.Namespace) -> int:
    from farplane_response import check_response

    if args.stdin and args.path:
        raise CliError("response_check_error:choose either --stdin or PATH", code=2)
    if args.max_words <= 0 or args.max_lines <= 0:
        raise CliError("response_check_error:limits must be positive integers", code=2)
    try:
        markdown = (
            Path(args.path).expanduser().read_text(encoding="utf-8")
            if args.path
            else sys.stdin.read()
        )
    except OSError as exc:
        raise CliError(f"response_check_error:{exc}", code=2) from exc

    payload = check_response(markdown, args.max_words, args.max_lines)
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        counts = payload["counts"]
        print(
            "farplane response check: "
            f"{'pass' if payload['ok'] else 'fail'} "
            f"(prose_words={counts['prose_words']}/{args.max_words}, "
            f"prose_lines={counts['prose_nonblank_lines']}/{args.max_lines}, "
            f"quote_spacers={counts['blockquote_spacers']}, "
            f"mermaid={counts['mermaid_blocks']}, media={counts['media_embeds']}, "
            f"references={counts['reference_entries']})"
        )
        for violation in payload["violations"]:
            print(f"- over limit: {violation}")
    return 0 if payload["ok"] else 1


def run_ticket_history_cli(args: argparse.Namespace) -> int:
    from farplane_ticket_history import run_history

    return int(run_history(args))


def run_ticket_finalize_cli(args: argparse.Namespace) -> int:
    from farplane_ticket_close import TicketFinalizeError, finalize_ticket

    try:
        payload = finalize_ticket(
            Path(args.project_root).expanduser().resolve(),
            args.ticket_id,
            args.media,
        )
    except (OSError, TicketFinalizeError) as exc:
        raise CliError(f"ticket_finalize_error:{exc}") from exc
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(
            f"farplane ticket finalize {payload['ticket_id']}: {payload['status']} "
            f"(mining={payload['mining_status']})"
        )
        print(f"receipt: {payload['receipt_path']}")
    return 0 if payload["ok"] else 1


def run_metrics_primitives_cli(args: argparse.Namespace) -> int:
    from farplane_primitive_metrics import run_primitives

    return int(run_primitives(args))


def run_project_snapshot_cli(args: argparse.Namespace) -> int:
    from farplane_project_snapshot import run_snapshot

    return int(run_snapshot(args))


def run_reports_index_cli(args: argparse.Namespace) -> int:
    from farplane_reports import run_index

    return int(run_index(args))


def run_reports_repair_refs_cli(args: argparse.Namespace) -> int:
    from farplane_reports import run_repair_refs

    return int(run_repair_refs(args))


def run_wiki_cli(args: argparse.Namespace) -> int:
    from farplane_wiki import (
        WikiError,
        WikiStoreError,
        run_doctor,
        run_rebuild,
        run_search,
        run_sync,
    )

    try:
        action = args.wiki_command
        if action == "doctor":
            return int(run_doctor(args))
        if action == "rebuild":
            return int(run_rebuild(args))
        if action == "sync":
            return int(run_sync(args))
        if action == "search":
            return int(run_search(args))
        raise WikiError(f"unsupported_wiki_command:{action}")
    except (OSError, sqlite3.Error, WikiError, WikiStoreError) as exc:
        raise CliError(f"wiki_error:{exc}") from exc


def run_mining_cli(args: argparse.Namespace) -> int:
    from farplane_mining import (
        MiningError,
        drain_pending,
        list_programs,
        list_routes,
        list_runs,
        mine_ticket,
        remove_route,
        replay_run,
        rerun_run,
        set_output_verdict,
        set_route,
        show_run,
        validate_routes,
    )

    project_root = Path(args.project_root).expanduser().resolve()
    try:
        group = args.mining_group
        action = args.mining_action
        if group == "programs" and action == "list":
            payload: Any = {"ok": True, "programs": list_programs()}
        elif group == "routes" and action == "list":
            payload = {"ok": True, "routes": list_routes(project_root)}
        elif group == "routes" and action == "validate":
            payload = validate_routes(project_root)
        elif group == "routes" and action == "set":
            payload = {
                "ok": True,
                "routes": set_route(
                    project_root,
                    route_id=args.route_id,
                    event_name=args.event_name,
                    program_ref=args.program_ref,
                ),
            }
        elif group == "routes" and action == "remove":
            payload = {"ok": True, "routes": remove_route(project_root, args.route_id)}
        elif group == "runs" and action == "list":
            payload = {"ok": True, "runs": list_runs(project_root)}
        elif group == "runs" and action == "show":
            payload = {"ok": True, **show_run(project_root, args.run_id)}
        elif group == "runs" and action == "replay":
            payload = {"ok": True, "run": replay_run(project_root, args.run_id)}
        elif group == "runs" and action == "rerun":
            payload = {"ok": True, "run": rerun_run(project_root, args.run_id)}
        elif group == "outputs" and action == "verdict":
            payload = {
                "ok": True,
                "output": set_output_verdict(
                    project_root,
                    args.run_id,
                    args.output_id,
                    args.verdict,
                ),
            }
        elif group == "drain":
            payload = drain_pending(project_root)
        elif group == "ticket":
            payload = {"ok": True, **mine_ticket(project_root, args.ticket_id)}
        else:
            raise MiningError(f"unsupported_mining_command:{group}:{action}")
    except (MiningError, OSError, json.JSONDecodeError) as exc:
        raise CliError(f"mining_error:{exc}") from exc

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        count = len(payload.get("programs", payload.get("routes", payload.get("runs", [])))) if isinstance(payload, dict) else 0
        status = "ok" if isinstance(payload, dict) and payload.get("ok", True) else "failed"
        print(f"farplane mining {status}: {group} {action or ''}".rstrip() + (f" ({count})" if count else ""))
        if isinstance(payload, dict):
            for issue in payload.get("issues", []):
                print(f"- {issue}")
            for failure in payload.get("failed", []):
                print(f"- {failure}")
    return 0 if not isinstance(payload, dict) or payload.get("ok", True) else 1


def run_content_add_cli(args: argparse.Namespace) -> int:
    from farplane_content import run_content_add

    return int(run_content_add(args))


def run_content_list_cli(args: argparse.Namespace) -> int:
    from farplane_content import run_content_list

    return int(run_content_list(args))


def run_content_validate_cli(args: argparse.Namespace) -> int:
    from farplane_content import run_content_validate

    return int(run_content_validate(args))


def run_content_select_cli(args: argparse.Namespace) -> int:
    from farplane_content import run_content_select

    return int(run_content_select(args))


def run_doctor(args: argparse.Namespace) -> int:
    config = load_config()
    ui_repo, ui_issues = discover_ui_repo(config)
    hook_report = hooks_doctor(Path(args.target).expanduser() if args.target else config.codex_home)
    config_report = config_doctor(
        codex_home=Path(args.target).expanduser().resolve() if args.target else config.codex_home,
        farplane_home=DEFAULT_FARPLANE_HOME,
        project_root=CORE_ROOT,
        process_env=dict(os.environ),
    )
    issues = [*hook_report["issues"], *ui_issues, *config_report["issues"]]
    payload = {
        "ok": not issues,
        "summary": "Core install, hooks, and UI link look healthy" if not issues else "Farplane doctor found issues",
        "coreRoot": str(CORE_ROOT),
        "configPath": str(CONFIG_PATH),
        "codexHome": str(config.codex_home),
        "uiRepoPath": str(ui_repo) if ui_repo else None,
        "hooks": hook_report,
        "config": config_report,
        "issues": issues,
        "hints": [
            *hook_report.get("hints", []),
            *config_report.get("hints", []),
            *(["run `farplane ui link /path/to/Farplane-UI`"] if ui_issues else []),
        ],
    }
    print_payload(payload, args.json)
    return 0 if payload["ok"] else 1


def run_validate_ticket(args: argparse.Namespace) -> int:
    root = Path(args.root).expanduser().resolve()
    ticket = Path(args.ticket).expanduser()
    if not ticket.is_absolute():
        ticket = root / ticket
    if args.path and args.base:
        raise CliError("validation_boundary_conflict: use --path or --base, not both")
    try:
        if args.path:
            boundary = explicit_boundary(args.path)
        elif args.base:
            boundary = base_boundary(root, args.base)
        else:
            boundary = unavailable_boundary()
        receipt = validate_ticket(
            root=root,
            ticket=ticket,
            phase=args.phase,
            boundary=boundary,
            registry=build_registry(),
            write=not args.no_write,
        )
    except ValueError as exc:
        raise CliError(f"validation_error:{exc}") from exc

    payload = receipt.as_dict()
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(
            f"ticket validation {'passed' if receipt.ok else 'failed'}: "
            f"{receipt.ticket} phase={receipt.phase} checks={len(receipt.results)}"
        )
        for result in receipt.results:
            print(f"[{result.status}:{result.mode}] {result.check_id} ({result.duration_ms} ms)")
            if result.status == "fail" and result.output:
                print(result.output)
    return 0 if receipt.ok else 1
