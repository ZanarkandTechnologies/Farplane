#!/usr/bin/env python3
"""Create one isolated local commit while preserving the caller's real index."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def git(repo: Path, *args: str, env: dict[str, str] | None = None,
        check: bool = True, text: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", *args], cwd=repo, env=env, text=text,
        capture_output=True, check=check,
    )


def emit(payload: dict) -> None:
    print(json.dumps(payload, sort_keys=True))


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--message", required=True)
    parser.add_argument("--path", action="append", default=[])
    parser.add_argument("--cached-patch", type=Path)
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    message = args.message.strip()
    if not message or (not args.path and not args.cached_patch):
        emit({"status": "error", "detail": "message and an explicit path or cached patch are required"})
        return 2

    try:
        if git(repo, "rev-parse", "--is-inside-work-tree").stdout.strip() != "true":
            raise ValueError
    except (OSError, ValueError, subprocess.CalledProcessError):
        emit({"status": "error", "detail": "repo-root is not a Git work tree"})
        return 2

    paths = list(dict.fromkeys(args.path))
    for path in paths:
        candidate = repo / path
        try:
            candidate.resolve().relative_to(repo)
        except ValueError:
            emit({"status": "error", "detail": f"path leaves repository: {path}"})
            return 2
        if (path in {".", ".."} or Path(path).is_absolute()
                or path.startswith(":") or any(char in path for char in "*?[")
                or candidate.is_dir()):
            emit({"status": "error", "detail": f"path must be explicit and repo-relative: {path}"})
            return 2
    if args.cached_patch and not args.cached_patch.is_file():
        emit({"status": "error", "detail": "cached patch does not exist"})
        return 2

    head_before = git(repo, "rev-parse", "HEAD").stdout.strip()
    real_index = Path(git(repo, "rev-parse", "--git-path", "index").stdout.strip())
    if not real_index.is_absolute():
        real_index = repo / real_index
    index_before = real_index.read_bytes() if real_index.exists() else b""

    fd, temp_name = tempfile.mkstemp(prefix="farplane-commit-index-")
    os.close(fd)
    Path(temp_name).unlink()
    env = os.environ.copy()
    env["GIT_INDEX_FILE"] = temp_name
    committed_paths: list[str] = []
    restore_name = ""
    try:
        git(repo, "read-tree", "HEAD", env=env)
        if paths:
            add = git(repo, "add", "--", *paths, env=env, check=False)
            if add.returncode:
                emit({"status": "error", "detail": add.stderr.strip() or "cannot stage requested paths"})
                return 1
        if args.cached_patch:
            patch = subprocess.run(
                ["git", "apply", "--cached", "--whitespace=nowarn", str(args.cached_patch.resolve())],
                cwd=repo, env=env, text=True, capture_output=True,
            )
            if patch.returncode:
                emit({"status": "error", "detail": patch.stderr.strip() or "cannot apply cached patch"})
                return 1

        diff_check = git(repo, "diff", "--cached", "--quiet", env=env, check=False)
        if diff_check.returncode == 0:
            emit({"status": "no_changes"})
            return 0
        if diff_check.returncode != 1:
            emit({"status": "error", "detail": "cannot inspect isolated index"})
            return 1
        committed_paths = [p for p in git(repo, "diff", "--cached", "--name-only", "-z", env=env).stdout.split("\0") if p]

        # Preserve existing staged changes except whole paths explicitly owned by
        # this commit. Cached-patch paths stay in the preservation set because
        # they may contain unrelated staged hunks in the same file.
        preserve_args = ["diff", "--cached", "--binary", "--"]
        preserve_args.extend(f":(exclude){path}" for path in paths)
        preserve_patch = git(repo, *preserve_args, text=False).stdout
        prospective_tree = git(repo, "write-tree", env=env).stdout.strip()
        restore_fd, restore_name = tempfile.mkstemp(
            prefix="farplane-restored-index-", dir=real_index.parent
        )
        os.close(restore_fd)
        Path(restore_name).unlink()
        restore_env = os.environ.copy()
        restore_env["GIT_INDEX_FILE"] = restore_name
        git(repo, "read-tree", prospective_tree, env=restore_env)
        if preserve_patch:
            preflight = subprocess.run(
                ["git", "apply", "--cached", "--3way", "--whitespace=nowarn", "-"],
                cwd=repo, env=restore_env, input=preserve_patch, capture_output=True,
            )
            if preflight.returncode:
                emit({"status": "boundary_blocker", "detail": "existing staged work cannot be restored over the requested commit"})
                return 1

        result = git(repo, "commit", "-m", message, env=env, check=False)
        if result.returncode:
            emit({"status": "error", "detail": result.stderr.strip() or result.stdout.strip()})
            return result.returncode
        commit = git(repo, "rev-parse", "HEAD").stdout.strip()
        if commit == head_before:
            emit({"status": "error", "detail": "HEAD did not advance"})
            return 1

        shutil.copyfile(restore_name, real_index)
        index_after = real_index.read_bytes() if real_index.exists() else b""
        emit({
            "status": "committed", "commit": commit, "subject": message,
            "paths": committed_paths,
            "original_index_sha256": digest(index_before),
            "result_index_sha256": digest(index_after),
        })
        return 0
    finally:
        Path(temp_name).unlink(missing_ok=True)
        if restore_name:
            Path(restore_name).unlink(missing_ok=True)


if __name__ == "__main__":
    sys.exit(main())
