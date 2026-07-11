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
import shutil
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

CORE_DIR = Path(__file__).resolve().parent / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from farplane_config_doctor import config_doctor
from runtime_config import load_runtime_env
from validation.boundary import base_boundary, explicit_boundary, unavailable_boundary
from validation.run import validate_ticket
from validators.farplane_checks import build_registry


CORE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CODEX_HOME = Path.home() / ".codex"
DEFAULT_FARPLANE_HOME = Path.home() / ".farplane"
CONFIG_PATH = DEFAULT_FARPLANE_HOME / "farplane-cli.json"
UI_ENV = "FARPLANE_UI_REPO"
DELEGATED_COMMANDS = {
    "agent",
    "bank",
    "gateway",
    "onboarding",
    "office",
    "resource-bank",
    "status",
    "team",
    "whoami",
}
OLD_CONVEX_SITE_URL = "https://agreeable-finch-230.convex.site"
PREVIOUS_NOTIFY_FLAG = "--previous-notify"


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


def toml_array(value: list[str]) -> str:
    return json.dumps(value, separators=(", ", ": "))


def farplane_notify_command(codex_home: Path) -> list[str]:
    return ["python3", str(codex_home / "bin" / "notify.py")]


def is_farplane_notify_command(command: object, codex_home: Path) -> bool:
    if not isinstance(command, list) or len(command) < 2:
        return False
    if not all(isinstance(item, str) for item in command):
        return False
    try:
        script_path = Path(command[1]).expanduser().resolve()
    except OSError:
        return False
    return script_path == (codex_home / "bin" / "notify.py").expanduser().resolve()


def parse_notify_command(config_text: str, config_path: Path) -> list[str] | None:
    try:
        parsed = tomllib.loads(config_text)
    except tomllib.TOMLDecodeError as exc:
        raise CliError(f"invalid_toml:{config_path}:{exc}") from exc
    notify = parsed.get("notify")
    if notify is None:
        return None
    if not isinstance(notify, list) or not all(isinstance(item, str) for item in notify):
        raise CliError(f"invalid_notify:{config_path}:expected_string_array")
    return notify


def previous_notify_command(command: list[str]) -> list[str] | None:
    if PREVIOUS_NOTIFY_FLAG not in command:
        return None
    index = command.index(PREVIOUS_NOTIFY_FLAG)
    if index + 1 >= len(command):
        return None
    try:
        value = json.loads(command[index + 1])
    except json.JSONDecodeError:
        return None
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        return None
    return value


def is_notify_wrapper(command: object) -> bool:
    return isinstance(command, list) and all(isinstance(item, str) for item in command) and "turn-ended" in command


def replace_notify_line(config_text: str, next_command: list[str] | None) -> str:
    lines = config_text.splitlines(keepends=True)
    replacement = None if next_command is None else f"notify = {toml_array(next_command)}\n"

    for index, line in enumerate(lines):
        if line.startswith("notify") and line.split("=", 1)[0].strip() == "notify":
            if replacement is None:
                del lines[index]
            else:
                lines[index] = replacement
            return "".join(lines)

    if replacement is None:
        return config_text

    for index, line in enumerate(lines):
        if line.lstrip().startswith("["):
            lines.insert(index, replacement)
            if index > 0 and lines[index - 1].strip():
                lines.insert(index, "\n")
            return "".join(lines)

    if config_text and not config_text.endswith("\n"):
        config_text += "\n"
    return config_text + replacement


def notify_status_payload(codex_home: Path) -> dict[str, Any]:
    config_path = codex_home / "config.toml"
    issues: list[str] = []
    hints: list[str] = []
    command: list[str] | None = None
    previous_command: list[str] | None = None

    if not config_path.exists():
        issues.append(f"config_missing:{config_path}")
        hints.append("run `farplane install`")
    else:
        command = parse_notify_command(config_path.read_text(encoding="utf-8"), config_path)
        if command is not None:
            previous_command = previous_notify_command(command)

    farplane_direct = is_farplane_notify_command(command, codex_home)
    farplane_previous = is_farplane_notify_command(previous_command, codex_home)
    wrapped = is_notify_wrapper(command)

    if farplane_direct:
        status = "enabled"
        mode = "direct"
    elif farplane_previous:
        status = "enabled"
        mode = "wrapped"
    elif wrapped:
        status = "disabled"
        mode = "wrapped"
    elif command is None:
        status = "disabled"
        mode = "none"
    else:
        status = "custom"
        mode = "custom"
        hints.append("notify is custom; `farplane notify disable` only removes Farplane notify commands")

    return {
        "ok": not issues,
        "summary": f"Farplane notify is {status}",
        "codexHome": str(codex_home),
        "configToml": str(config_path),
        "status": status,
        "mode": mode,
        "notify": command,
        "previousNotify": previous_command,
        "issues": issues,
        "hints": hints,
    }


def write_codex_notify(
    *,
    codex_home: Path,
    next_command: list[str] | None,
    dry_run: bool,
) -> Path | None:
    config_path = codex_home / "config.toml"
    if not config_path.exists():
        raise CliError(f"config_missing:{config_path}: run `farplane install` first")
    current_text = config_path.read_text(encoding="utf-8")
    next_text = replace_notify_line(current_text, next_command)
    if next_text == current_text:
        return None
    if dry_run:
        return None
    backup_path = config_path.with_name(f"config.toml.bak.farplane-notify-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
    shutil.copy2(config_path, backup_path)
    config_path.write_text(next_text, encoding="utf-8")
    return backup_path


def set_notify_enabled(codex_home: Path, enabled: bool, dry_run: bool) -> dict[str, Any]:
    config_path = codex_home / "config.toml"
    if not config_path.exists():
        raise CliError(f"config_missing:{config_path}: run `farplane install` first")
    current_text = config_path.read_text(encoding="utf-8")
    command = parse_notify_command(current_text, config_path)
    default_command = farplane_notify_command(codex_home)
    next_command: list[str] | None

    if enabled:
        if command and PREVIOUS_NOTIFY_FLAG in command:
            next_command = list(command)
            previous_json = json.dumps(default_command, separators=(",", ":"))
            index = next_command.index(PREVIOUS_NOTIFY_FLAG)
            if index + 1 < len(next_command):
                next_command[index + 1] = previous_json
            else:
                next_command.append(previous_json)
        elif is_notify_wrapper(command):
            previous_json = json.dumps(default_command, separators=(",", ":"))
            next_command = list(command) + [PREVIOUS_NOTIFY_FLAG, previous_json]
        elif command and not is_farplane_notify_command(command, codex_home):
            raise CliError("notify_custom: refusing to overwrite custom notify command")
        else:
            next_command = default_command
    else:
        if command and PREVIOUS_NOTIFY_FLAG in command:
            next_command = list(command)
            index = next_command.index(PREVIOUS_NOTIFY_FLAG)
            del next_command[index : index + 2]
        elif is_farplane_notify_command(command, codex_home):
            next_command = None
        else:
            next_command = command

    backup_path = write_codex_notify(codex_home=codex_home, next_command=next_command, dry_run=dry_run)
    payload = notify_status_payload(codex_home)
    payload["ok"] = True
    payload["dryRun"] = dry_run
    payload["backup"] = str(backup_path) if backup_path else None
    if dry_run:
        payload["summary"] = f"Farplane notify would be {'enabled' if enabled else 'disabled'}"
        payload["wouldWrite"] = str(config_path)
        payload["nextNotify"] = next_command
        payload["nextStatus"] = "enabled" if enabled else "disabled"
    else:
        payload["summary"] = f"Farplane notify {'enabled' if enabled else 'disabled'}"
    return payload


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


def nearest_doppler_file(start: Path) -> Path | None:
    current = start.resolve()
    for candidate_root in [current, *current.parents]:
        candidate = candidate_root / "doppler.yaml"
        if candidate.exists():
            return candidate
        candidate = candidate_root / "doppler.yml"
        if candidate.exists():
            return candidate
    return None


def doppler_setup_hint(doppler_file: Path | None) -> str:
    if doppler_file is None:
        return "run `doppler login` and `doppler setup --project <project> --config <config>` from this project"
    project = ""
    config = ""
    for line in doppler_file.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if stripped.startswith("project:"):
            project = stripped.split(":", 1)[1].strip()
        if stripped.startswith("config:"):
            config = stripped.split(":", 1)[1].strip()
    if project and config:
        return f"run `doppler login` and `doppler setup --project {project} --config {config}` from {doppler_file.parent}"
    return f"run `doppler login` and `doppler setup` from {doppler_file.parent}"


def doppler_configured(cwd: Path) -> bool:
    checks = [
        ["doppler", "configure", "get", "project", "--plain"],
        ["doppler", "configure", "get", "config", "--plain"],
    ]
    for command in checks:
        result = subprocess.run(command, cwd=str(cwd), capture_output=True, text=True)
        if result.returncode != 0 or not result.stdout.strip():
            return False
    return True


def run_with_doppler(args: argparse.Namespace) -> int:
    command = passthrough_args(args.extra)
    if not command:
        raise CliError("run_requires_command: use `farplane run -- <command>`")
    cwd = Path.cwd()
    doppler_file = nearest_doppler_file(cwd)
    if shutil.which("doppler") is None:
        raise CliError(
            "doppler_not_installed: install Doppler CLI, then " + doppler_setup_hint(doppler_file),
            127,
        )
    if not doppler_configured(cwd):
        raise CliError("doppler_not_configured: " + doppler_setup_hint(doppler_file), 2)
    doppler_command = ["doppler", "run", "--", *command]
    if args.dry_run:
        print(json.dumps({"cwd": str(cwd), "command": doppler_command}, indent=2))
        return 0
    child = subprocess.run(doppler_command, cwd=str(cwd), env=os.environ)
    return child.returncode


def run_install(args: argparse.Namespace) -> int:
    command = ["bash", str(CORE_ROOT / "install.sh")]
    if args.target:
        command.extend(["--target", args.target])
    if args.extra:
        command.extend(passthrough_args(args.extra))
    if nearest_doppler_file(CORE_ROOT) is not None and not os.environ.get("DOPPLER_PROJECT"):
        if shutil.which("doppler") is None:
            raise CliError("doppler_not_installed: " + doppler_setup_hint(nearest_doppler_file(CORE_ROOT)), 127)
        if not doppler_configured(CORE_ROOT):
            raise CliError("doppler_not_configured: " + doppler_setup_hint(nearest_doppler_file(CORE_ROOT)), 2)
        command = ["doppler", "run", "--", *command]
        if args.dry_run:
            print(json.dumps({"cwd": str(CORE_ROOT), "command": command}, indent=2))
            return 0
        child = subprocess.run(command, cwd=str(CORE_ROOT), env=os.environ)
        return child.returncode
    return run_process(command, CORE_ROOT, args.dry_run)


def hooks_doctor(target: Path | None = None) -> dict[str, Any]:
    codex_home = (target or DEFAULT_CODEX_HOME).expanduser().resolve()
    hook_src = CORE_ROOT / "hooks" / "farplane_console_ping.py"
    file_event_hook_src = CORE_ROOT / "hooks" / "farplane_file_change.py"
    hooks_json_src = CORE_ROOT / "hooks.json"
    hook_dest = codex_home / "hooks" / "farplane_console_ping.py"
    file_event_hook_dest = codex_home / "hooks" / "farplane_file_change.py"
    hooks_json_dest = codex_home / "hooks.json"
    config_toml = codex_home / "config.toml"
    issues: list[str] = []
    hints: list[str] = []

    if not path_points_to(hook_dest, hook_src):
        issues.append(f"hook_not_linked:{hook_dest}")
        hints.append("run `farplane hooks install`")
    if not path_points_to(file_event_hook_dest, file_event_hook_src):
        issues.append(f"hook_not_linked:{file_event_hook_dest}")
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
        "fileEventHook": {
            "path": str(file_event_hook_dest),
            "expected": str(file_event_hook_src),
            "linked": path_points_to(file_event_hook_dest, file_event_hook_src),
        },
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


def run_mining_cli(args: argparse.Namespace) -> int:
    from farplane_file_events import FileEventError
    from farplane_mining import (
        MiningError,
        drain_pending,
        handle_file_change,
        list_programs,
        list_routes,
        list_runs,
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
        elif group == "handle-file-change":
            raw = sys.stdin.read() if args.payload == "-" else Path(args.payload).read_text(encoding="utf-8")
            parsed = json.loads(raw)
            if not isinstance(parsed, dict):
                raise MiningError("file_change_payload_must_be_object")
            payload = handle_file_change(parsed, project_root)
        else:
            raise MiningError(f"unsupported_mining_command:{group}:{action}")
    except (FileEventError, MiningError, OSError, json.JSONDecodeError) as exc:
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
    hooks_install = hooks_sub.add_parser("install", help="Install/relink Core hooks through install.sh.")
    hooks_install.add_argument("--target", help="Codex home target. Defaults to ~/.codex.")
    hooks_install.add_argument("--dry-run", action="store_true")
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

    mining_handle = mining_sub.add_parser("handle-file-change", help="Handle one Codex PostToolUse JSON payload.")
    mining_handle.add_argument("--payload", required=True, help="JSON payload path or - for stdin.")
    mining_handle.add_argument("--project-root", default=os.getcwd())
    mining_handle.add_argument("--json", action="store_true")
    mining_handle.set_defaults(func=run_mining_cli, mining_action=None)

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


def main(argv: list[str]) -> int:
    if len(argv) > 1 and argv[1] in DELEGATED_COMMANDS:
        return delegate_to_ui(argv[1], argv[2:])
    if len(argv) == 2 and argv[1] == "ui":
        return run_ui_start(argparse.Namespace(extra=[], dry_run=False, json=False))

    parser = build_parser()
    args = parser.parse_args(argv[1:])
    if getattr(args, "command", None) == "hooks" and getattr(args, "hooks_command", None) is None:
        parser.error("hooks requires a subcommand: install or doctor")
    if getattr(args, "command", None) == "validate" and getattr(args, "validate_command", None) is None:
        parser.error("validate requires a subcommand: ticket")
    if getattr(args, "command", None) == "notify" and getattr(args, "notify_command", None) is None:
        return run_notify_status(argparse.Namespace(target=None, json=False))
    if getattr(args, "command", None) == "ui" and getattr(args, "ui_command", None) is None:
        return run_ui_start(argparse.Namespace(extra=[], dry_run=False, json=False))
    if getattr(args, "command", None) == "adoption" and getattr(args, "adoption_command", None) is None:
        parser.error("adoption requires a subcommand: scan")
    if getattr(args, "command", None) == "skills" and getattr(args, "skills_command", None) is None:
        parser.error("skills requires a subcommand: rollout")
    if getattr(args, "skills_command", None) == "rollout" and getattr(args, "skills_rollout_command", None) is None:
        parser.error("skills rollout requires a subcommand: scan")
    if getattr(args, "command", None) == "metrics" and getattr(args, "metrics_command", None) is None:
        parser.error("metrics requires a subcommand: primitives")
    if getattr(args, "command", None) == "project" and getattr(args, "project_command", None) is None:
        parser.error("project requires a subcommand: snapshot")
    if getattr(args, "command", None) == "reports" and getattr(args, "reports_command", None) is None:
        parser.error("reports requires a subcommand: index")
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
