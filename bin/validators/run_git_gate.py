#!/usr/bin/env python3
"""Run configurable Farplane Git review gates."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from fnmatch import fnmatchcase
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = ROOT / "rules" / "git-review-gates.toml"


@dataclass(frozen=True)
class CommandResult:
    name: str
    mode: str
    returncode: int


def normalize_path(path: str) -> str:
    normalized = path.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def run_command(args: list[str], *, root: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )


def run_streaming(args: list[str], *, root: Path = ROOT) -> int:
    return subprocess.run(args, cwd=root, check=False).returncode


def git_lines(args: list[str]) -> list[str]:
    result = run_command(["git", *args])
    if result.returncode != 0:
        raise SystemExit(result.stdout.strip() or f"git {' '.join(args)} failed")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def staged_paths() -> list[str]:
    return [
        normalize_path(path)
        for path in git_lines(["diff", "--cached", "--name-only", "--diff-filter=ACMR"])
    ]


def branch_paths(base: str) -> list[str]:
    result = run_command(["git", "diff", "--name-only", f"{base}...HEAD", "--diff-filter=ACMR"])
    if result.returncode != 0:
        print(result.stdout.rstrip())
        print(f"warning: could not diff against {base!r}; falling back to staged paths")
        return staged_paths()
    return [normalize_path(path) for path in result.stdout.splitlines() if path.strip()]


def load_config(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise SystemExit(f"missing git gate config: {path}")
    with path.open("rb") as handle:
        config = tomllib.load(handle)
    if not isinstance(config, dict):
        raise SystemExit(f"{path}: expected TOML object")
    return config


def as_string_list(value: object, *, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise SystemExit(f"{label} must be a list of strings")
    return list(value)


def stage_config(config: dict[str, Any], stage: str) -> dict[str, Any]:
    value = config.get(stage)
    if not isinstance(value, dict):
        raise SystemExit(f"config is missing [{stage}] table")
    return value


def format_argv(argv: list[str], *, base: str) -> list[str]:
    return [part.replace("{base}", base) for part in argv]


def check_mode(config: dict[str, Any], stage: dict[str, Any], check_name: str) -> str:
    checks = config.get("checks", {})
    override = checks.get(check_name, {}) if isinstance(checks, dict) else {}
    mode = override.get("mode") if isinstance(override, dict) else None
    stage_mode = stage.get("mode", "block")
    if mode is None:
        mode = stage_mode
    if mode not in {"block", "warn"}:
        raise SystemExit(f"{check_name}: mode must be 'block' or 'warn'")
    return mode


def configured_argv(config: dict[str, Any], check_name: str, *, base: str) -> list[str]:
    checks = config.get("checks", {})
    if not isinstance(checks, dict) or check_name not in checks:
        raise SystemExit(f"{check_name}: no [checks.{check_name}] entry")
    check = checks[check_name]
    if not isinstance(check, dict):
        raise SystemExit(f"{check_name}: expected check table")
    argv = as_string_list(check.get("argv"), label=f"{check_name}.argv")
    return format_argv(argv, base=base)


def skip_env(config: dict[str, Any], check_name: str) -> str | None:
    checks = config.get("checks", {})
    check = checks.get(check_name, {}) if isinstance(checks, dict) else {}
    value = check.get("skip_env") if isinstance(check, dict) else None
    return value if isinstance(value, str) and value else None


def path_matches(path: str, patterns: list[str]) -> bool:
    normalized = normalize_path(path)
    return any(fnmatchcase(normalized, normalize_path(pattern)) for pattern in patterns)


def select_checks(stage: dict[str, Any], paths: list[str]) -> list[str]:
    selected: list[str] = []
    for check_name in as_string_list(stage.get("checks", []), label="checks"):
        if check_name not in selected:
            selected.append(check_name)
    path_checks = stage.get("path_check", [])
    if not isinstance(path_checks, list):
        raise SystemExit("path_check must be a list of tables")
    for item in path_checks:
        if not isinstance(item, dict):
            raise SystemExit("path_check entries must be tables")
        globs = as_string_list(item.get("globs", []), label="path_check.globs")
        checks = as_string_list(item.get("checks", []), label="path_check.checks")
        if any(path_matches(path, globs) for path in paths):
            for check_name in checks:
                if check_name not in selected:
                    selected.append(check_name)
    return selected


def large_file_errors(config: dict[str, Any], paths: list[str]) -> list[str]:
    guard = config.get("large_file_guard", {})
    if not isinstance(guard, dict):
        raise SystemExit("[large_file_guard] must be a table")
    max_bytes = guard.get("max_bytes", 1048576)
    if not isinstance(max_bytes, int) or max_bytes <= 0:
        raise SystemExit("large_file_guard.max_bytes must be a positive integer")
    skip_globs = as_string_list(guard.get("skip_globs", []), label="large_file_guard.skip_globs")
    errors: list[str] = []
    for path in paths:
        if path_matches(path, skip_globs):
            continue
        result = run_command(["git", "cat-file", "-s", f":{path}"])
        if result.returncode != 0:
            continue
        try:
            size = int(result.stdout.strip())
        except ValueError:
            continue
        if size > max_bytes:
            errors.append(f"{path}: staged blob is {size} bytes; max is {max_bytes}")
    return errors


def run_check(
    config: dict[str, Any],
    stage: dict[str, Any],
    check_name: str,
    *,
    base: str,
    paths: list[str],
    dry_run: bool,
) -> CommandResult:
    mode = check_mode(config, stage, check_name)
    env_name = skip_env(config, check_name)
    if env_name and os.environ.get(env_name, "").lower() in {"1", "true", "yes"}:
        print(f"[skip] {check_name}: {env_name} is set", flush=True)
        return CommandResult(check_name, mode, 0)

    print(f"[run:{mode}] {check_name}", flush=True)
    if check_name == "large_file_guard":
        if dry_run:
            print("  builtin: large_file_guard", flush=True)
            return CommandResult(check_name, mode, 0)
        errors = large_file_errors(config, paths)
        if errors:
            print("\n".join(errors), flush=True)
            return CommandResult(check_name, mode, 1)
        print("large file guard OK", flush=True)
        return CommandResult(check_name, mode, 0)

    argv = configured_argv(config, check_name, base=base)
    if dry_run:
        print("  " + " ".join(argv), flush=True)
        return CommandResult(check_name, mode, 0)

    return CommandResult(check_name, mode, run_streaming(argv))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=("pre_commit", "pre_push"), required=True)
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--base", help="Override the pre-push base branch.")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = load_config(Path(args.config))
    stage = stage_config(config, args.stage)
    base = args.base or str(stage.get("base") or "main")
    paths = staged_paths() if args.stage == "pre_commit" else branch_paths(base)
    checks = select_checks(stage, paths)
    print(f"farplane git gate: {args.stage} ({len(paths)} paths, {len(checks)} checks)", flush=True)
    if paths:
        print("paths:", flush=True)
        for path in paths[:30]:
            print(f"  {path}", flush=True)
        if len(paths) > 30:
            print(f"  ... {len(paths) - 30} more", flush=True)

    failures: list[CommandResult] = []
    warnings: list[CommandResult] = []
    for check_name in checks:
        result = run_check(
            config,
            stage,
            check_name,
            base=base,
            paths=paths,
            dry_run=args.dry_run,
        )
        if result.returncode != 0 and result.mode == "block":
            failures.append(result)
        elif result.returncode != 0:
            warnings.append(result)

    if warnings:
        print("warning checks failed: " + ", ".join(item.name for item in warnings), flush=True)
    if failures:
        print("blocking checks failed: " + ", ".join(item.name for item in failures), flush=True)
        return 1
    print(f"farplane git gate OK ({args.stage})", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
