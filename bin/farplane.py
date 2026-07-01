#!/usr/bin/env python3
"""Core-owned Farplane CLI.

Owns the global `farplane` command for Core install, hooks, doctor, and local
UI checkout routing. UI/office/team implementation stays in Farplane-UI and is
delegated by explicit repo path so this file remains a thin control plane.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

CORE_DIR = Path(__file__).resolve().parent / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from farplane_adoption import run_scan as run_adoption_scan
from farplane_content import run_content_add, run_content_list
from farplane_metrics import run_compile as run_metrics_compile
from farplane_skill_rollout import SkillRolloutError, run_scan as run_skill_rollout_scan
from runtime_config import load_runtime_env


CORE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CODEX_HOME = Path.home() / ".codex"
DEFAULT_FARPLANE_HOME = Path.home() / ".farplane"
CONFIG_PATH = DEFAULT_FARPLANE_HOME / "farplane-cli.json"
UI_ENV = "FARPLANE_UI_REPO"
DELEGATED_COMMANDS = {"agent", "gateway", "onboarding", "office", "status", "team", "whoami"}
OLD_CONVEX_SITE_URL = "https://agreeable-finch-230.convex.site"


@dataclass(frozen=True)
class CliConfig:
    ui_repo_path: Path | None
    codex_home: Path
    created_at: str | None
    updated_at: str | None


class CliError(Exception):
    def __init__(self, message: str, code: int = 1) -> None:
        super().__init__(message)
        self.code = code


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def print_payload(payload: dict[str, Any], as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return

    status = "ok" if payload.get("ok") else "failed"
    print(f"farplane {status}: {payload.get('summary', 'done')}")
    for issue in payload.get("issues", []):
        print(f"- {issue}")
    for hint in payload.get("hints", []):
        print(f"- next: {hint}")


def passthrough_args(args: list[str]) -> list[str]:
    if args and args[0] == "--":
        return args[1:]
    return args


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise CliError(f"invalid_config_json:{path}:{exc}") from exc
    if not isinstance(value, dict):
        raise CliError(f"invalid_config_shape:{path}:expected_object")
    return value


def load_config() -> CliConfig:
    raw = read_json(CONFIG_PATH)
    ui_value = os.environ.get(UI_ENV) or raw.get("uiRepoPath")
    codex_value = raw.get("codexHome") or str(DEFAULT_CODEX_HOME)
    return CliConfig(
        ui_repo_path=Path(ui_value).expanduser().resolve() if ui_value else None,
        codex_home=Path(codex_value).expanduser().resolve(),
        created_at=raw.get("createdAt") if isinstance(raw.get("createdAt"), str) else None,
        updated_at=raw.get("updatedAt") if isinstance(raw.get("updatedAt"), str) else None,
    )


def write_config(next_config: CliConfig) -> None:
    previous = read_json(CONFIG_PATH)
    created_at = next_config.created_at or previous.get("createdAt") or now_iso()
    payload = {
        "uiRepoPath": str(next_config.ui_repo_path) if next_config.ui_repo_path else None,
        "codexHome": str(next_config.codex_home),
        "createdAt": created_at,
        "updatedAt": now_iso(),
    }
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = CONFIG_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    tmp.replace(CONFIG_PATH)


def path_points_to(path: Path, expected: Path) -> bool:
    return path.is_symlink() and os.readlink(path) == str(expected)


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


def run_process(args: list[str], cwd: Path, dry_run: bool = False) -> int:
    if dry_run:
        print(json.dumps({"cwd": str(cwd), "command": args}, indent=2))
        return 0
    child = subprocess.run(args, cwd=str(cwd), env=load_runtime_env(os.environ))
    return child.returncode


def run_install(args: argparse.Namespace) -> int:
    command = ["bash", str(CORE_ROOT / "install.sh")]
    if args.target:
        command.extend(["--target", args.target])
    if args.extra:
        command.extend(passthrough_args(args.extra))
    return run_process(command, CORE_ROOT, args.dry_run)


def hooks_doctor(target: Path | None = None) -> dict[str, Any]:
    codex_home = (target or DEFAULT_CODEX_HOME).expanduser().resolve()
    hook_src = CORE_ROOT / "hooks" / "farplane_console_ping.py"
    hooks_json_src = CORE_ROOT / "hooks.json"
    hook_dest = codex_home / "hooks" / "farplane_console_ping.py"
    hooks_json_dest = codex_home / "hooks.json"
    config_toml = codex_home / "config.toml"
    issues: list[str] = []
    hints: list[str] = []

    if not path_points_to(hook_dest, hook_src):
        issues.append(f"hook_not_linked:{hook_dest}")
        hints.append("run `farplane hooks install`")
    if hooks_json_src.exists() and not path_points_to(hooks_json_dest, hooks_json_src):
        issues.append(f"hooks_json_not_linked:{hooks_json_dest}")
        hints.append("run `farplane hooks install`")
    if not config_toml.exists():
        issues.append(f"config_missing:{config_toml}")
        hints.append("run `farplane install`")
    else:
        config_text = config_toml.read_text(errors="replace")
        if "FARPLANE_CONVEX_SITE_URL" not in config_text:
            issues.append("config_missing_farplane_convex_site_url")
        if OLD_CONVEX_SITE_URL in config_text:
            issues.append("config_uses_old_convex_site_url")
            hints.append("update ~/.farplane/config.toml and rerun `farplane install`")

    return {
        "ok": not issues,
        "summary": "hooks linked and config rendered" if not issues else "hooks/config need attention",
        "codexHome": str(codex_home),
        "hook": {"path": str(hook_dest), "expected": str(hook_src), "linked": path_points_to(hook_dest, hook_src)},
        "hooksJson": {
            "path": str(hooks_json_dest),
            "expected": str(hooks_json_src),
            "linked": (not hooks_json_src.exists()) or path_points_to(hooks_json_dest, hooks_json_src),
        },
        "configToml": str(config_toml),
        "issues": issues,
        "hints": hints,
    }


def run_hooks_install(args: argparse.Namespace) -> int:
    command = ["bash", str(CORE_ROOT / "install.sh")]
    if args.target:
        command.extend(["--target", args.target])
    return run_process(command, CORE_ROOT, args.dry_run)


def run_hooks_doctor(args: argparse.Namespace) -> int:
    target = Path(args.target).expanduser() if args.target else None
    payload = hooks_doctor(target)
    print_payload(payload, args.json)
    return 0 if payload["ok"] else 1


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


def run_doctor(args: argparse.Namespace) -> int:
    config = load_config()
    ui_repo, ui_issues = discover_ui_repo(config)
    hook_report = hooks_doctor(Path(args.target).expanduser() if args.target else config.codex_home)
    issues = [*hook_report["issues"], *ui_issues]
    payload = {
        "ok": not issues,
        "summary": "Core install, hooks, and UI link look healthy" if not issues else "Farplane doctor found issues",
        "coreRoot": str(CORE_ROOT),
        "configPath": str(CONFIG_PATH),
        "codexHome": str(config.codex_home),
        "uiRepoPath": str(ui_repo) if ui_repo else None,
        "hooks": hook_report,
        "issues": issues,
        "hints": [
            *hook_report.get("hints", []),
            *(["run `farplane ui link /path/to/Farplane-UI`"] if ui_issues else []),
        ],
    }
    print_payload(payload, args.json)
    return 0 if payload["ok"] else 1


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

    hooks = sub.add_parser("hooks", help="Install or check Codex lifecycle hooks.")
    hooks_sub = hooks.add_subparsers(dest="hooks_command")
    hooks_install = hooks_sub.add_parser("install", help="Install/relink Core hooks through install.sh.")
    hooks_install.add_argument("--target", help="Codex home target. Defaults to ~/.codex.")
    hooks_install.add_argument("--dry-run", action="store_true")
    hooks_install.set_defaults(func=run_hooks_install)
    hooks_doctor_parser = hooks_sub.add_parser("doctor", help="Check hook links and rendered config.")
    hooks_doctor_parser.add_argument("--target", help="Codex home target. Defaults to ~/.codex.")
    hooks_doctor_parser.add_argument("--json", action="store_true")
    hooks_doctor_parser.set_defaults(func=run_hooks_doctor)

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
    adoption_scan.set_defaults(func=run_adoption_scan)

    skills = sub.add_parser("skills", help="Inspect Farplane skill rollout and registry projections.")
    skills_sub = skills.add_subparsers(dest="skills_command")
    skills_rollout = skills_sub.add_parser("rollout", help="Inspect skill rollout status.")
    skills_rollout_sub = skills_rollout.add_subparsers(dest="skills_rollout_command")
    skills_rollout_scan = skills_rollout_sub.add_parser("scan", help="Resolve skill rollout status for UI rendering.")
    skills_rollout_scan.add_argument("--standard-root", default=str(CORE_ROOT))
    skills_rollout_scan.add_argument("--registry", help="Skill registry JSONL path.")
    skills_rollout_scan.add_argument("--intelligence", help="Skill template intelligence JSON path.")
    skills_rollout_scan.add_argument("--json", action="store_true")
    skills_rollout_scan.set_defaults(func=run_skill_rollout_scan)

    metrics = sub.add_parser("metrics", help="Compile Farplane metric observations for interval reports and UI.")
    metrics_sub = metrics.add_subparsers(dest="metrics_command")
    metrics_compile = metrics_sub.add_parser("compile", help="Compile existing KPI observations into UI snapshot JSON.")
    metrics_compile.add_argument("--project-root", default=str(CORE_ROOT))
    metrics_compile.add_argument("--date", help="Snapshot date in YYYY-MM-DD. Defaults to today UTC.")
    metrics_compile.add_argument("--json", action="store_true")
    metrics_compile.set_defaults(func=run_metrics_compile)

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
    content_add.set_defaults(func=run_content_add)
    content_list = content_sub.add_parser("list", help="List content ledger rows.")
    content_list.add_argument("--project-root", default=str(CORE_ROOT))
    content_list.add_argument("--platform")
    content_list.add_argument("--status")
    content_list.add_argument("--kpi")
    content_list.add_argument("--since-date", help="Only include content published on or after this UTC date.")
    content_list.add_argument("--until-date", help="Only include content published before this UTC date.")
    content_list.set_defaults(func=run_content_list)

    return parser


def main(argv: list[str]) -> int:
    if len(argv) > 1 and argv[1] in DELEGATED_COMMANDS:
        return delegate_to_ui(argv[1], argv[2:])
    if len(argv) == 2 and argv[1] == "ui":
        return run_ui_start(argparse.Namespace(extra=[], dry_run=False, json=False))

    parser = build_parser()
    args = parser.parse_args(argv[1:])
    if getattr(args, "command", None) == "hooks" and getattr(args, "hooks_command", None) is None:
        parser.error("hooks requires a subcommand: install or doctor")
    if getattr(args, "command", None) == "ui" and getattr(args, "ui_command", None) is None:
        return run_ui_start(argparse.Namespace(extra=[], dry_run=False, json=False))
    if getattr(args, "command", None) == "adoption" and getattr(args, "adoption_command", None) is None:
        parser.error("adoption requires a subcommand: scan")
    if getattr(args, "command", None) == "skills" and getattr(args, "skills_command", None) is None:
        parser.error("skills requires a subcommand: rollout")
    if getattr(args, "skills_command", None) == "rollout" and getattr(args, "skills_rollout_command", None) is None:
        parser.error("skills rollout requires a subcommand: scan")
    if getattr(args, "command", None) == "metrics" and getattr(args, "metrics_command", None) is None:
        parser.error("metrics requires a subcommand: compile")
    if getattr(args, "command", None) == "content" and getattr(args, "content_command", None) is None:
        parser.error("content requires a subcommand: add or list")
    if not hasattr(args, "func"):
        parser.print_help()
        return 0
    try:
        return int(args.func(args))
    except CliError as exc:
        print(f"farplane: {exc}", file=sys.stderr)
        return exc.code
    except SkillRolloutError as exc:
        print(f"farplane skill rollout: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
