#!/usr/bin/env python3
"""Thin global CLI edge for Farplane Core commands."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

CORE_DIR = Path(__file__).resolve().parent / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))
CORE_ROOT = Path(__file__).resolve().parents[1]
if str(CORE_ROOT) not in sys.path:
    sys.path.insert(0, str(CORE_ROOT))

from farplane_cli_base import (
    CONFIG_PATH, DEFAULT_CODEX_HOME, DEFAULT_FARPLANE_HOME, DELEGATED_COMMANDS,
    MANAGED_HOOK_FILES, RETIRED_HOOK_FILES, CliConfig, CliError,
    farplane_notify_command, is_farplane_notify_command, is_linked_worktree,
    is_notify_wrapper, load_config, notify_status_payload, parse_notify_command,
    passthrough_args, previous_notify_command, print_payload,
    replace_notify_line, require_primary_checkout_install, set_notify_enabled,
    write_codex_notify, write_config,
)
from farplane_cli_hooks import (
    hook_command_inventory,
    hook_inventory_issues,
    hooks_doctor,
    hooks_list_payload,
    install_hooks,
    run_hooks_doctor,
    run_hooks_install,
    run_hooks_list,
    run_install,
    run_with_doppler,
)
from farplane_cli_parser import build_parser
from farplane_cli_ui import delegate_to_ui, run_notify_status, run_ui_start

def main(argv: list[str]) -> int:
    if len(argv) > 1 and argv[1] in DELEGATED_COMMANDS:
        return delegate_to_ui(argv[1], argv[2:])
    if len(argv) == 2 and argv[1] == "ui":
        return run_ui_start(argparse.Namespace(extra=[], dry_run=False, json=False))

    parser = build_parser()
    args = parser.parse_args(argv[1:])
    if getattr(args, "command", None) == "hooks" and getattr(args, "hooks_command", None) is None:
        parser.error("hooks requires a subcommand: install or doctor")
    if getattr(args, "command", None) == "eval" and getattr(args, "eval_command", None) is None:
        parser.error("eval requires a subcommand: init or promptfoo")
    if getattr(args, "command", None) == "response" and getattr(args, "response_command", None) is None:
        parser.error("response requires a subcommand: check")
    if getattr(args, "command", None) == "notify" and getattr(args, "notify_command", None) is None:
        return run_notify_status(argparse.Namespace(target=None, json=False))
    if getattr(args, "command", None) == "ui" and getattr(args, "ui_command", None) is None:
        return run_ui_start(argparse.Namespace(extra=[], dry_run=False, json=False))
    if getattr(args, "command", None) == "adoption" and getattr(args, "adoption_command", None) is None:
        parser.error("adoption requires a subcommand: scan")
    if getattr(args, "command", None) == "skills" and getattr(args, "skills_command", None) is None:
        parser.error("skills requires a subcommand: rollout or sync")
    if getattr(args, "skills_command", None) == "rollout" and getattr(args, "skills_rollout_command", None) is None:
        parser.error("skills rollout requires a subcommand: scan")
    if getattr(args, "command", None) == "harness" and getattr(args, "harness_command", None) is None:
        parser.error("harness requires a subcommand: health")
    if getattr(args, "harness_command", None) == "health" and getattr(args, "harness_health_command", None) is None:
        parser.error("harness health requires a subcommand: compile")
    if getattr(args, "command", None) == "tickets" and getattr(args, "tickets_command", None) is None:
        parser.error("tickets requires a subcommand: history")
    if getattr(args, "command", None) == "ticket" and getattr(args, "ticket_command", None) is None:
        parser.error("ticket requires a subcommand: check or finalize")
    if getattr(args, "command", None) == "metrics" and getattr(args, "metrics_command", None) is None:
        parser.error("metrics requires a subcommand: primitives")
    if getattr(args, "command", None) == "project" and getattr(args, "project_command", None) is None:
        parser.error("project requires a subcommand: snapshot")
    if getattr(args, "command", None) == "capability-profiles" and getattr(args, "capability_profiles_command", None) is None:
        parser.error("capability-profiles requires a subcommand: read, resolve, write, or snapshot")
    if getattr(args, "command", None) == "reports" and getattr(args, "reports_command", None) is None:
        parser.error("reports requires a subcommand: index")
    if getattr(args, "command", None) == "wiki" and getattr(args, "wiki_command", None) is None:
        parser.error("wiki requires a subcommand: doctor, rebuild, sync, or search")
    if getattr(args, "command", None) == "mining" and getattr(args, "mining_group", None) is None:
        parser.error("mining requires a subcommand")
    if getattr(args, "mining_group", None) in {"programs", "routes", "runs", "outputs"} and getattr(args, "mining_action", None) is None:
        parser.error(f"mining {args.mining_group} requires a subcommand")
    if getattr(args, "command", None) == "content" and getattr(args, "content_command", None) is None:
        parser.error("content requires a subcommand: add, list, validate, or select")
    if not hasattr(args, "func"):
        parser.print_help()
        return 0
    try:
        return int(args.func(args))
    except CliError as exc:
        print(f"farplane: {exc}", file=sys.stderr)
        return exc.code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
