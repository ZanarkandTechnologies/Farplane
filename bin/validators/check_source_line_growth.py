#!/usr/bin/env python3
"""Block new oversized source files and growth in oversized legacy files."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from fnmatch import fnmatchcase
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class SourceDelta:
    path: str
    base_lines: int | None
    current_lines: int


def git(*args: str, root: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(detail or f"git {' '.join(args)} failed")
    return result


def line_count(blob: bytes) -> int:
    if not blob:
        return 0
    return len(blob.splitlines())


def matches(path: str, globs: list[str]) -> bool:
    normalized = path.replace("\\", "/")
    return any(
        fnmatchcase(normalized, pattern)
        or ("/**/" in pattern and fnmatchcase(normalized, pattern.replace("/**/", "/")))
        for pattern in globs
    )


def read_blob(spec: str, *, root: Path = ROOT) -> bytes | None:
    result = git("show", spec, root=root, check=False)
    return result.stdout if result.returncode == 0 else None


def changed_paths(mode: str, base: str, *, root: Path = ROOT) -> tuple[list[str], str]:
    if mode == "staged":
        result = git("diff", "--cached", "--name-only", "--diff-filter=ACMR", root=root)
        return result.stdout.decode().splitlines(), "HEAD"

    merge_base = git("merge-base", base, "HEAD", root=root).stdout.decode().strip()
    result = git("diff", "--name-only", "--diff-filter=ACMR", f"{merge_base}...HEAD", root=root)
    return result.stdout.decode().splitlines(), merge_base


def source_deltas(
    mode: str,
    base: str,
    globs: list[str],
    baseline: dict[str, int] | None = None,
    baseline_path: str | None = None,
    *,
    root: Path = ROOT,
) -> list[SourceDelta]:
    paths, comparison = changed_paths(mode, base, root=root)
    use_adoption_baseline = bool(
        mode == "branch"
        and baseline
        and baseline_path
        and read_blob(f"{comparison}:{baseline_path}", root=root) is None
    )
    deltas: list[SourceDelta] = []
    for path in paths:
        if not matches(path, globs):
            continue
        current_spec = f":{path}" if mode == "staged" else f"HEAD:{path}"
        current = read_blob(current_spec, root=root)
        if current is None:
            continue
        previous = read_blob(f"{comparison}:{path}", root=root)
        previous_lines = line_count(previous) if previous is not None else None
        if use_adoption_baseline and baseline and path in baseline:
            previous_lines = baseline[path]
        deltas.append(
            SourceDelta(
                path=path,
                base_lines=previous_lines,
                current_lines=line_count(current),
            )
        )
    return deltas


def violations(deltas: list[SourceDelta], max_lines: int) -> list[str]:
    errors: list[str] = []
    for delta in deltas:
        if delta.current_lines <= max_lines:
            continue
        if delta.base_lines is None:
            errors.append(
                f"{delta.path}: new source file has {delta.current_lines} lines; max is {max_lines}"
            )
        elif delta.current_lines > delta.base_lines:
            errors.append(
                f"{delta.path}: oversized source grew from {delta.base_lines} to "
                f"{delta.current_lines} lines; reduce or hold it at its previous size"
            )
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("staged", "branch"), required=True)
    parser.add_argument("--base", default="origin/main")
    parser.add_argument("--max-lines", type=int, default=500)
    parser.add_argument("--glob", action="append", dest="globs", default=[])
    parser.add_argument("--baseline", help="TOML adoption baseline used until the base contains it")
    return parser.parse_args()


def load_baseline(path: Path | None) -> dict[str, int]:
    if path is None:
        return {}
    with path.open("rb") as handle:
        payload = tomllib.load(handle)
    files = payload.get("files", {})
    if not isinstance(files, dict) or not all(
        isinstance(key, str) and isinstance(value, int) and value > 0
        for key, value in files.items()
    ):
        raise RuntimeError(f"{path}: [files] must map paths to positive line counts")
    return dict(files)


def main() -> int:
    args = parse_args()
    if args.max_lines <= 0:
        raise SystemExit("--max-lines must be positive")
    globs = args.globs or ["bin/**/*.py"]
    try:
        baseline_path = Path(args.baseline) if args.baseline else None
        baseline = load_baseline(ROOT / baseline_path if baseline_path else None)
        deltas = source_deltas(
            args.mode,
            args.base,
            globs,
            baseline=baseline,
            baseline_path=baseline_path.as_posix() if baseline_path else None,
        )
    except (OSError, RuntimeError, tomllib.TOMLDecodeError) as exc:
        print(f"source line growth guard error: {exc}", file=sys.stderr)
        return 2
    errors = violations(deltas, args.max_lines)
    if errors:
        print("source line growth guard failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"source line growth guard OK ({len(deltas)} source files checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
