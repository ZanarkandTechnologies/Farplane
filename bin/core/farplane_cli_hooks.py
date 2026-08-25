"""Install, Doppler, and Codex hook commands for the Farplane CLI."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

from farplane_cli_base import (
    CORE_ROOT, DEFAULT_CODEX_HOME, MANAGED_HOOK_FILES, RETIRED_HOOK_FILES,
    CliError, is_linked_worktree, passthrough_args, print_payload,
    require_primary_checkout_install,
)
from runtime_config import load_runtime_env

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


def run_with_doppler_command(command: list[str], cwd: Path, *, dry_run: bool = False) -> int:
    """Run one command through the configured Doppler environment for ``cwd``.

    Keep this as the shared execution seam for commands that need the same
    project-scoped credential contract as ``farplane run``.  The dry-run
    payload intentionally contains only argv and cwd; it never materializes
    or prints environment values.
    """

    doppler_file = nearest_doppler_file(cwd)
    if shutil.which("doppler") is None:
        raise CliError(
            "doppler_not_installed: install Doppler CLI, then " + doppler_setup_hint(doppler_file),
            127,
        )
    if not doppler_configured(cwd):
        raise CliError("doppler_not_configured: " + doppler_setup_hint(doppler_file), 2)
    doppler_command = ["doppler", "run", "--", *command]
    if dry_run:
        print(json.dumps({"cwd": str(cwd), "command": doppler_command}, indent=2))
        return 0
    child = subprocess.run(doppler_command, cwd=str(cwd), env=os.environ)
    return child.returncode


def run_with_doppler(args: argparse.Namespace) -> int:
    command = passthrough_args(args.extra)
    if not command:
        raise CliError("run_requires_command: use `farplane run -- <command>`")
    return run_with_doppler_command(command, Path.cwd(), dry_run=args.dry_run)


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
