#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import re
import shlex
import shutil
import subprocess
import sys

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SKIP_ENV_VAR = "CODEXTER_SKIP_CODERABBIT"

# MEM-0039: keep CodeRabbit as an explicit PR/pre-push gate, not a Stop-hook default.
STAGE_DEFAULTS = {
    "manual": {"review_type": "all", "needs_base": False, "output": "plain"},
    "pre-commit": {"review_type": "uncommitted", "needs_base": False, "output": "plain"},
    "pre-push": {"review_type": "committed", "needs_base": True, "output": "plain"},
    "pr": {"review_type": "committed", "needs_base": True, "output": "plain"},
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run CodeRabbit with Codexter stage-aware defaults."
    )
    parser.add_argument(
        "--stage",
        choices=tuple(STAGE_DEFAULTS),
        default="manual",
        help="Review stage to optimize for.",
    )
    parser.add_argument(
        "--base",
        help="Base branch for committed/PR review. Auto-detected when omitted.",
    )
    parser.add_argument(
        "--type",
        dest="review_type",
        choices=("all", "committed", "uncommitted"),
        help="Override the default review type for the selected stage.",
    )
    parser.add_argument(
        "--output",
        choices=("plain", "agent", "interactive", "prompt-only"),
        help="Override the default output mode for the selected stage.",
    )
    parser.add_argument(
        "--config",
        action="append",
        default=[],
        help="Additional CodeRabbit config/instruction files to pass with --config.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the resolved command without executing it.",
    )
    parser.add_argument(
        "--no-auth-check",
        action="store_true",
        help="Skip the auth status check before running the review.",
    )
    return parser.parse_args()


def run_command(
    args: list[str], *, capture_output: bool = True
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=REPO_ROOT,
        capture_output=capture_output,
        text=True,
        check=False,
    )


def decode_output(value: str | bytes | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def strip_ansi(value: str) -> str:
    return re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", value)


def require_tool(name: str) -> None:
    if shutil.which(name):
        return
    raise SystemExit(
        f"{name} is not installed or not on PATH. Install/setup it before running this helper."
    )


def ensure_git_repo() -> None:
    result = run_command(["git", "rev-parse", "--show-toplevel"])
    if result.returncode != 0:
        raise SystemExit("This helper must run inside a git repository.")


def detect_base_branch() -> str:
    remote_head = run_command(["git", "symbolic-ref", "refs/remotes/origin/HEAD"])
    if remote_head.returncode == 0:
        value = remote_head.stdout.strip()
        if value:
            return value.rsplit("/", 1)[-1]

    for candidate in ("main", "master", "develop", "trunk"):
        exists = run_command(["git", "show-ref", "--verify", f"refs/heads/{candidate}"])
        if exists.returncode == 0:
            return candidate

    return "main"


def ensure_authenticated() -> None:
    try:
        fallback = subprocess.run(
            ["coderabbit", "auth", "status"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=3,
        )
    except subprocess.TimeoutExpired as exc:
        probe_output = strip_ansi(decode_output(exc.stdout) + decode_output(exc.stderr))
        if "Authentication: Not logged in" in probe_output:
            raise SystemExit(
                "CodeRabbit is not authenticated. Run `coderabbit auth login --agent` for agent workflows "
                "or `coderabbit auth login` for manual workflows first."
            )
        if "Authentication:" in probe_output and "Not logged in" not in probe_output:
            return
        raise SystemExit(
            "CodeRabbit auth status did not exit cleanly within 3 seconds. "
            "If you know auth is valid, rerun with `--no-auth-check`."
        )
    else:
        probe_output = strip_ansi(fallback.stdout + fallback.stderr)
        if "Authentication: Not logged in" in probe_output:
            raise SystemExit(
                "CodeRabbit is not authenticated. Run `coderabbit auth login --agent` for agent workflows "
                "or `coderabbit auth login` for manual workflows first."
            )
        if "Authentication:" in probe_output and "Not logged in" not in probe_output:
            return

    raise SystemExit(
        "CodeRabbit auth status returned an unexpected response. "
        "If auth is known-good, rerun with `--no-auth-check`."
    )


def build_command(args: argparse.Namespace) -> list[str]:
    defaults = STAGE_DEFAULTS[args.stage]
    review_type = args.review_type or defaults["review_type"]
    output = args.output or defaults["output"]

    command = ["coderabbit", "review"]

    if output == "plain":
        command.append("--plain")
    elif output == "agent":
        command.append("--agent")
    elif output == "interactive":
        command.append("--interactive")
    elif output == "prompt-only":
        command.append("--prompt-only")

    command.extend(["--type", review_type])

    if defaults["needs_base"] or args.base:
        command.extend(["--base", args.base or detect_base_branch()])

    for config_path in args.config:
        command.extend(["--config", config_path])

    return command


def maybe_skip(stage: str) -> None:
    if stage in {"pre-commit", "pre-push", "pr"} and os.environ.get(SKIP_ENV_VAR, "").lower() in {
        "1",
        "true",
        "yes",
    }:
        print(f"Skipping CodeRabbit because {SKIP_ENV_VAR} is set.")
        raise SystemExit(0)


def main() -> int:
    args = parse_args()
    maybe_skip(args.stage)
    require_tool("git")
    require_tool("coderabbit")
    ensure_git_repo()

    command = build_command(args)
    if args.dry_run:
        print(shlex.join(command))
        return 0

    if not args.no_auth_check:
        ensure_authenticated()

    result = run_command(command, capture_output=False)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
