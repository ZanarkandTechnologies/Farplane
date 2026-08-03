"""Farplane UI discovery, notification commands, and delegation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from farplane_cli_base import (
    CONFIG_PATH, CORE_ROOT, CliConfig, load_config, notify_status_payload,
    passthrough_args, print_payload, set_notify_enabled, write_config,
)
from farplane_cli_hooks import run_process

def validate_ui_repo(path: Path) -> list[str]:
    issues: list[str] = []
    package_json = path / "package.json"
    cli_entry = path / "cli" / "farplane-cli.ts"
    if not path.exists():
        issues.append(f"ui_repo_missing:{path}")
        return issues
    if not package_json.exists():
        issues.append(f"ui_repo_missing_package_json:{path}")
    if not cli_entry.exists():
        issues.append(f"ui_repo_missing_cli_entry:{cli_entry}")
    if package_json.exists():
        try:
            package = json.loads(package_json.read_text())
        except json.JSONDecodeError as exc:
            issues.append(f"ui_repo_invalid_package_json:{exc}")
        else:
            scripts = package.get("scripts") if isinstance(package, dict) else None
            if not isinstance(scripts, dict) or "shell" not in scripts:
                issues.append("ui_repo_missing_script:shell")
            if not isinstance(scripts, dict) or "ui" not in scripts:
                issues.append("ui_repo_missing_script:ui")
    return issues


def discover_ui_repo(config: CliConfig) -> tuple[Path | None, list[str]]:
    candidates: list[tuple[str, Path]] = []
    if config.ui_repo_path:
        candidates.append(("configured", config.ui_repo_path))
    candidates.append(("sibling", CORE_ROOT.parent / "Farplane-UI"))

    seen: set[Path] = set()
    for source, candidate in candidates:
        resolved = candidate.expanduser().resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        issues = validate_ui_repo(resolved)
        if not issues:
            return resolved, []
        if source == "configured":
            return resolved, issues
    return None, ["ui_repo_not_linked:run `farplane ui link /path/to/Farplane-UI`"]


def run_notify_status(args: argparse.Namespace) -> int:
    codex_home = Path(args.target).expanduser().resolve() if args.target else load_config().codex_home
    payload = notify_status_payload(codex_home)
    print_payload(payload, args.json)
    return 0 if payload["ok"] else 1


def run_notify_enable(args: argparse.Namespace) -> int:
    codex_home = Path(args.target).expanduser().resolve() if args.target else load_config().codex_home
    payload = set_notify_enabled(codex_home, True, args.dry_run)
    print_payload(payload, args.json)
    return 0


def run_notify_disable(args: argparse.Namespace) -> int:
    codex_home = Path(args.target).expanduser().resolve() if args.target else load_config().codex_home
    payload = set_notify_enabled(codex_home, False, args.dry_run)
    print_payload(payload, args.json)
    return 0


def run_ui_link(args: argparse.Namespace) -> int:
    ui_repo = Path(args.path).expanduser().resolve()
    issues = validate_ui_repo(ui_repo)
    payload = {
        "ok": not issues,
        "summary": f"linked UI repo {ui_repo}" if not issues else f"cannot link UI repo {ui_repo}",
        "uiRepoPath": str(ui_repo),
        "configPath": str(CONFIG_PATH),
        "issues": issues,
        "hints": [],
    }
    if not issues:
        current = load_config()
        write_config(CliConfig(ui_repo_path=ui_repo, codex_home=current.codex_home, created_at=current.created_at, updated_at=None))
    print_payload(payload, args.json)
    return 0 if payload["ok"] else 1


def run_ui_start(args: argparse.Namespace) -> int:
    config = load_config()
    ui_repo, issues = discover_ui_repo(config)
    if issues or ui_repo is None:
        print_payload(
            {
                "ok": False,
                "summary": "UI repo is not linked",
                "issues": issues,
                "hints": ["run `farplane ui link /path/to/Farplane-UI`"],
            },
            args.json,
        )
        return 1
    command = ["npm", "run", "ui", "--", *passthrough_args(args.extra)]
    return run_process(command, ui_repo, args.dry_run)


def delegate_to_ui(command_name: str, extra: list[str], dry_run: bool = False) -> int:
    config = load_config()
    ui_repo, issues = discover_ui_repo(config)
    if issues or ui_repo is None:
        print_payload(
            {
                "ok": False,
                "summary": f"cannot delegate `{command_name}` without a linked UI repo",
                "issues": issues,
                "hints": ["run `farplane ui link /path/to/Farplane-UI`"],
            },
            False,
        )
        return 1
    command = ["npm", "run", "shell", "--", command_name, *extra]
    return run_process(command, ui_repo, dry_run)
