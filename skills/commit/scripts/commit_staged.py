#!/usr/bin/env python3
"""Create one local commit from an already staged Git boundary."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def git(repo_root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=check,
    )


def emit(payload: dict[str, str]) -> None:
    print(json.dumps(payload, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--message", required=True)
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    message = args.message.strip()
    if not message:
        emit({"status": "error", "detail": "commit message must not be empty"})
        return 2

    try:
        inside = git(repo_root, "rev-parse", "--is-inside-work-tree")
    except (OSError, subprocess.CalledProcessError):
        emit({"status": "error", "detail": "repo-root is not a Git work tree"})
        return 2
    if inside.stdout.strip() != "true":
        emit({"status": "error", "detail": "repo-root is not a Git work tree"})
        return 2

    staged = git(repo_root, "diff", "--cached", "--quiet", check=False)
    if staged.returncode == 0:
        emit({"status": "no_staged_changes"})
        return 0
    if staged.returncode != 1:
        emit({"status": "error", "detail": staged.stderr.strip() or "cannot inspect staged diff"})
        return 1

    result = git(repo_root, "commit", "-m", message, check=False)
    if result.returncode:
        emit({"status": "error", "detail": result.stderr.strip() or result.stdout.strip()})
        return result.returncode

    commit = git(repo_root, "rev-parse", "HEAD").stdout.strip()
    emit({"status": "committed", "commit": commit, "subject": message})
    return 0


if __name__ == "__main__":
    sys.exit(main())
