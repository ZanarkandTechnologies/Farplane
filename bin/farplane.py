#!/usr/bin/env python3
"""Thin global CLI edge for Farplane Core commands."""

from __future__ import annotations

import argparse
import json
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
    MANAGED_HOOK_DIRS, RETIRED_HOOK_FILES, CliConfig, CliError,
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
    if getattr(args, "command", None) == "notify" and getattr(args, "notify_command", None) is None:
        return run_notify_status(argparse.Namespace(target=None, json=False))
    if getattr(args, "command", None) == "ui" and getattr(args, "ui_command", None) is None:
        return run_ui_start(argparse.Namespace(extra=[], dry_run=False, json=False))
    if not hasattr(args, "func"):
        # A group without its subcommand: show that group's help, which lists the subcommands.
        if len(argv) > 1:
            try:
                build_parser().parse_args([*argv[1:], "--help"])
            except SystemExit:
                pass
            print(f"farplane {' '.join(argv[1:])}: choose a subcommand from the list above", file=sys.stderr)
            return 2
        parser.print_help()
        return 0
    try:
        return int(args.func(args))
    except CliError as exc:
        if getattr(args, "json", False):
            print(json.dumps({"ok": False, "error": str(exc)}))
        else:
            print(f"farplane: {exc}", file=sys.stderr)
        return exc.code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
