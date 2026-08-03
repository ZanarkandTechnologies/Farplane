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
import shlex
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
CORE_ROOT = Path(__file__).resolve().parents[1]
if str(CORE_ROOT) not in sys.path:
    sys.path.insert(0, str(CORE_ROOT))

from farplane_config_doctor import config_doctor
from runtime_config import load_runtime_env
from validation.boundary import base_boundary, explicit_boundary, unavailable_boundary
from validation.run import validate_ticket
from validators.farplane_checks import build_registry


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
MANAGED_HOOK_FILES = (
    "final_response_gate.py",
    "farplane_console_ping.py",
    "shared_checkout_guard.py",
)
RETIRED_HOOK_FILES = (
    "farplane_file_change.py",
    "farplane_local_event.py",
)


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


def is_linked_worktree(root: Path = CORE_ROOT) -> bool:
    """Return whether root is a linked worktree rather than the primary checkout."""
    commands = (
        ["git", "-C", str(root), "rev-parse", "--path-format=absolute", "--git-dir"],
        ["git", "-C", str(root), "rev-parse", "--path-format=absolute", "--git-common-dir"],
    )
    paths: list[Path] = []
    for command in commands:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0 or not result.stdout.strip():
            return False
        paths.append(Path(result.stdout.strip()).resolve())
    return paths[0] != paths[1]


def require_primary_checkout_install(action: str, root: Path = CORE_ROOT) -> None:
    if is_linked_worktree(root):
        raise CliError(
            f"{action}_from_linked_worktree_blocked: global Codex installation must "
            "come from the primary Farplane checkout; merge or restore the change "
            "there, then rerun the install",
            2,
        )


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


def _read_json_file(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError as exc:
        raise CliError(f"invalid_json:{path}:{exc}") from exc
    if not isinstance(payload, dict):
        raise CliError(f"invalid_json_shape:{path}:expected_object")
    return payload


def _hooks_entries(hooks_json: Path) -> list[dict[str, Any]]:
    payload = _read_json_file(hooks_json)
    hooks = payload.get("hooks")
    if not isinstance(hooks, dict):
        return []
    entries: list[dict[str, Any]] = []
    for event_name, groups in hooks.items():
        if not isinstance(groups, list):
            continue
        for group_index, group in enumerate(groups):
            if not isinstance(group, dict):
                continue
            matcher = group.get("matcher")
            commands = group.get("hooks")
            if not isinstance(commands, list):
                continue
            for hook_index, hook in enumerate(commands):
                if not isinstance(hook, dict):
                    continue
                command = hook.get("command")
                entries.append(
                    {
                        "event": str(event_name),
                        "matcher": str(matcher or ""),
                        "group_index": group_index,
                        "hook_index": hook_index,
                        "type": hook.get("type"),
                        "command": command if isinstance(command, str) else "",
                        "statusMessage": hook.get("statusMessage"),
                        "timeout": hook.get("timeout"),
                    }
                )
    return entries


def _target_hook_path(token: str, codex_home: Path) -> Path | None:
    text = token.strip().strip("'\"")
    if not text:
        return None
    replacements = {
        "$HOME/.codex": str(codex_home),
        "${HOME}/.codex": str(codex_home),
        "~/.codex": str(codex_home),
    }
    for prefix, replacement in replacements.items():
        if text.startswith(prefix):
            text = replacement + text[len(prefix) :]
            break
    if text.startswith("$HOME/"):
        text = str(Path.home()) + text[len("$HOME") :]
    if text.startswith("${HOME}/"):
        text = str(Path.home()) + text[len("${HOME}") :]
    if text.startswith("~/"):
        text = str(Path.home()) + text[1:]
    if (
        ".codex/hooks/" not in text
        and ".codex/bin/" not in text
        and str(codex_home / "hooks") not in text
        and str(codex_home / "bin") not in text
    ):
        return None
    return Path(text).expanduser()


def _command_tokens(command: str) -> list[str]:
    try:
        return shlex.split(command)
    except ValueError:
        return command.split()


def hook_command_inventory(codex_home: Path, hooks_json: Path | None = None) -> list[dict[str, Any]]:
    source = hooks_json or (codex_home / "hooks.json")
    entries = _hooks_entries(source)
    inventory = []
    for entry in entries:
        command = str(entry.get("command") or "")
        tokens = _command_tokens(command)
        interpreter = tokens[0] if tokens else ""
        target = None
        if interpreter in {"python", "python3"} and len(tokens) >= 2:
            target = _target_hook_path(tokens[1], codex_home)
        elif interpreter in {"sh", "bash"}:
            for token in tokens[1:]:
                target = target or _target_hook_path(token, codex_home)
        else:
            for token in tokens:
                target = target or _target_hook_path(token, codex_home)
        target_expected = None
        if target and target.name in MANAGED_HOOK_FILES:
            target_expected = CORE_ROOT / "hooks" / target.name
        elif target and target.parent.name == "bin":
            target_expected = CORE_ROOT / "bin" / target.name
        inventory.append(
            {
                **entry,
                "interpreter": interpreter,
                "interpreterPath": shutil.which(interpreter) if interpreter else None,
                "target": str(target) if target else None,
                "expected": str(target_expected) if target_expected else None,
                "targetExists": bool(target and target.exists()),
                "targetLinked": bool(target and target_expected and path_points_to(target, target_expected)),
                "source": str(source),
            }
        )
    return inventory


def hook_inventory_issues(commands: list[dict[str, Any]]) -> tuple[list[str], list[str]]:
    issues: list[str] = []
    hints: list[str] = []
    for index, row in enumerate(commands):
        prefix = f"managed_command.{index}:{row.get('event')}:{row.get('matcher') or '*'}"
        command = str(row.get("command") or "")
        interpreter = str(row.get("interpreter") or "")
        if not command:
            issues.append(f"{prefix}:command_missing")
            hints.append("run `farplane hooks install`")
        if "FARPLANE_UI_REPO" in command or "node_modules/.bin/tsx" in command or "/hooks/skill-invocation-listener/" in command or "/hooks/thread-lineage-listener/" in command:
            issues.append(f"{prefix}:ui_dependent_command")
            hints.append("replace UI listener with Core hook command and rerun `farplane hooks install`")
        if interpreter and shutil.which(interpreter) is None:
            issues.append(f"{prefix}:interpreter_missing:{interpreter}")
            hints.append(f"install `{interpreter}` or update the managed hook command")
        target = row.get("target")
        if target is None:
            issues.append(f"{prefix}:managed_target_unresolved")
            hints.append("run `farplane hooks install`")
        elif not row.get("targetExists"):
            issues.append(f"{prefix}:target_missing:{target}")
            hints.append("run `farplane hooks install`")
        elif row.get("expected") and not row.get("targetLinked"):
            issues.append(f"{prefix}:target_not_core_link:{target}")
            hints.append("run `farplane hooks install`")
    return issues, sorted(set(hints))


def hooks_list_payload(target: Path | None = None) -> dict[str, Any]:
    codex_home = (target or DEFAULT_CODEX_HOME).expanduser().resolve()
    hooks_json_dest = codex_home / "hooks.json"
    hooks_json_src = CORE_ROOT / "hooks.json"
    source = hooks_json_dest if hooks_json_dest.exists() else hooks_json_src
    commands = hook_command_inventory(codex_home, source)
    issues, hints = hook_inventory_issues(commands)
    return {
        "ok": not issues,
        "summary": "managed hook commands inspected" if not issues else "managed hook commands need attention",
        "codexHome": str(codex_home),
        "hooksJson": str(source),
        "commands": commands,
        "issues": issues,
        "hints": hints,
    }


def _replace_symlink(src: Path, dest: Path, *, backup_root: Path | None, dry_run: bool) -> dict[str, Any]:
    linked = path_points_to(dest, src)
    row = {"src": str(src), "dest": str(dest), "changed": False, "linked": linked}
    if linked:
        return row
    if dry_run:
        row["changed"] = True
        return row
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() or dest.is_symlink():
        if backup_root:
            backup = backup_root / dest.name
            backup.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(dest), str(backup))
            row["backup"] = str(backup)
        else:
            dest.unlink()
    os.symlink(src, dest)
    row["changed"] = True
    row["linked"] = True
    return row


def _retire_path(path: Path, *, backup_root: Path, dry_run: bool) -> dict[str, Any]:
    present = path.exists() or path.is_symlink()
    row: dict[str, Any] = {"dest": str(path), "retired": present, "changed": False}
    if not present or dry_run:
        row["changed"] = present
        return row
    backup = backup_root / path.name
    backup.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(path), str(backup))
    row["backup"] = str(backup)
    row["changed"] = True
    return row


def install_hooks(codex_home: Path, *, dry_run: bool = False) -> dict[str, Any]:
    codex_home = codex_home.expanduser().resolve()
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_root = codex_home / ".install-backups" / f"hooks-{stamp}"
    operations = [
        _replace_symlink(CORE_ROOT / "hooks.json", codex_home / "hooks.json", backup_root=backup_root, dry_run=dry_run),
        _replace_symlink(CORE_ROOT / "bin" / "_compat.py", codex_home / "bin" / "_compat.py", backup_root=backup_root / "bin", dry_run=dry_run),
        _replace_symlink(
            CORE_ROOT / "bin" / "capture_user_turn.py",
            codex_home / "bin" / "capture_user_turn.py",
            backup_root=backup_root / "bin",
            dry_run=dry_run,
        ),
        _replace_symlink(CORE_ROOT / "bin" / "core", codex_home / "bin" / "core", backup_root=backup_root / "bin", dry_run=dry_run),
        _replace_symlink(
            CORE_ROOT / "bin" / "runtime",
            codex_home / "bin" / "runtime",
            backup_root=backup_root / "bin",
            dry_run=dry_run,
        ),
    ]
    for hook_name in RETIRED_HOOK_FILES:
        operations.append(
            _retire_path(
                codex_home / "hooks" / hook_name,
                backup_root=backup_root / "retired-hooks",
                dry_run=dry_run,
            )
        )
    for hook_name in MANAGED_HOOK_FILES:
        operations.append(
            _replace_symlink(
                CORE_ROOT / "hooks" / hook_name,
                codex_home / "hooks" / hook_name,
                backup_root=backup_root / "hooks",
                dry_run=dry_run,
            )
        )
    doctor = hooks_doctor(codex_home) if not dry_run else {"ok": True, "issues": [], "hints": []}
    return {
        "ok": bool(doctor["ok"]),
        "summary": "Core hooks installed" if doctor["ok"] else "Core hooks installed with remaining issues",
        "codexHome": str(codex_home),
        "dryRun": dry_run,
        "operations": operations,
        "doctor": doctor,
        "issues": doctor.get("issues", []),
        "hints": doctor.get("hints", []),
    }


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
    require_primary_checkout_install("install")
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
    hooks_json_src = CORE_ROOT / "hooks.json"
    hooks_json_dest = codex_home / "hooks.json"
    issues: list[str] = []
    hints: list[str] = []
    hook_links = []

    for hook_name in MANAGED_HOOK_FILES:
        source = CORE_ROOT / "hooks" / hook_name
        dest = codex_home / "hooks" / hook_name
        linked = path_points_to(dest, source)
        hook_links.append({"path": str(dest), "expected": str(source), "linked": linked})
        if not linked:
            issues.append(f"hook_not_linked:{dest}")
            hints.append("run `farplane hooks install`")
    if hooks_json_src.exists() and not path_points_to(hooks_json_dest, hooks_json_src):
        issues.append(f"hooks_json_not_linked:{hooks_json_dest}")
        hints.append("run `farplane hooks install`")

    try:
        commands = hook_command_inventory(codex_home, hooks_json_dest if hooks_json_dest.exists() else hooks_json_src)
        command_issues, command_hints = hook_inventory_issues(commands)
        issues.extend(command_issues)
        hints.extend(command_hints)
    except CliError as exc:
        commands = []
        issues.append(str(exc))
        hints.append("run `farplane hooks install`")

    return {
        "ok": not issues,
        "summary": "Core hooks linked and commands executable" if not issues else "Core hook install needs attention",
        "codexHome": str(codex_home),
        "hooks": hook_links,
        "hooksJson": {
            "path": str(hooks_json_dest),
            "expected": str(hooks_json_src),
            "linked": (not hooks_json_src.exists()) or path_points_to(hooks_json_dest, hooks_json_src),
        },
        "commands": commands,
        "optionalTelemetry": {
            "configToml": str(codex_home / "config.toml"),
            "requiredForLocalHealth": False,
        },
        "issues": issues,
        "hints": sorted(set(hints)),
    }


def run_hooks_install(args: argparse.Namespace) -> int:
    require_primary_checkout_install("hooks_install")
    target = Path(args.target).expanduser() if args.target else DEFAULT_CODEX_HOME
    payload = install_hooks(target, dry_run=args.dry_run)
    print_payload(payload, args.json)
    return 0 if payload["ok"] else 1


def run_hooks_list(args: argparse.Namespace) -> int:
    target = Path(args.target).expanduser() if args.target else None
    payload = hooks_list_payload(target)
    print_payload(payload, args.json)
    return 0 if payload["ok"] else 1


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
            f"mermaid={counts['mermaid_blocks']}, media={counts['media_embeds']}, "
            f"references={counts['reference_entries']})"
        )
        for violation in payload["violations"]:
            print(f"- over limit: {violation}")
    return 0 if payload["ok"] else 1


def run_ticket_history_cli(args: argparse.Namespace) -> int:
    from farplane_ticket_history import run_history

    return int(run_history(args))


def run_ticket_close_cli(args: argparse.Namespace) -> int:
    from farplane_ticket_close import TicketCloseError, close_ticket

    try:
        payload = close_ticket(Path(args.project_root).expanduser().resolve(), args.ticket_id)
    except (OSError, TicketCloseError) as exc:
        raise CliError(f"ticket_close_error:{exc}") from exc
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(
            f"farplane ticket close {payload['ticket_id']}: {payload['status']} "
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


def run_entities_compile_cli(args: argparse.Namespace) -> int:
    from farplane_entities import run_compile

    return int(run_compile(args))


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
    ticket_close = ticket_sub.add_parser("close", help="Close, archive, and emit completion mining for one ticket.")
    ticket_close.add_argument("ticket_id")
    ticket_close.add_argument("--project-root", default=os.getcwd())
    ticket_close.add_argument("--json", action="store_true")
    ticket_close.set_defaults(func=run_ticket_close_cli)

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
    if getattr(args, "command", None) == "response" and getattr(args, "response_command", None) is None:
        parser.error("response requires a subcommand: check")
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
    if getattr(args, "command", None) == "harness" and getattr(args, "harness_command", None) is None:
        parser.error("harness requires a subcommand: health")
    if getattr(args, "harness_command", None) == "health" and getattr(args, "harness_health_command", None) is None:
        parser.error("harness health requires a subcommand: compile")
    if getattr(args, "command", None) == "tickets" and getattr(args, "tickets_command", None) is None:
        parser.error("tickets requires a subcommand: history")
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
