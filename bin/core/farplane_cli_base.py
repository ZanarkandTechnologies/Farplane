"""Shared values, configuration, and notification policy for the Farplane CLI."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tomllib
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CORE_ROOT = Path(__file__).resolve().parents[2]

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
    "skill_file_line_gate.py",
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
