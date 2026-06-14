#!/usr/bin/env python3
"""
Pre-commit guard for Farplane template metadata and version bumps.

The staged-file mode checks only template-like files touched in the index. A
template edit must carry template metadata and, when the file already existed in
HEAD, must bump the template version. The hook does not choose major/minor/patch;
that remains a human decision.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from fnmatch import fnmatchcase
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = ROOT / "rules" / "template-version-watch.toml"
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
METADATA_KEY_RE = re.compile(
    r"(?im)^\s*(?:[#/;*-]+\s*)?(?:<!--\s*)?(template_id|template_name|template_version|version)\s*:\s*[\"']?([^\"'\n>-]+)"
)


@dataclass(frozen=True)
class TemplateMetadata:
    template_id: str | None
    version: str | None
    source: str


@dataclass(frozen=True)
class WatchConfig:
    paths: frozenset[str]
    globs: tuple[str, ...]
    exclude_globs: tuple[str, ...]
    source: Path


def run_git(args: list[str], root: Path, *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def normalize_path(path: str) -> str:
    return path.replace("\\", "/").lstrip("./")


def load_watch_config(path: Path) -> WatchConfig:
    if not path.is_file():
        raise SystemExit(
            f"missing template watch config: {path}. Add explicit paths/globs before "
            "enabling the template version hook."
        )
    payload = tomllib.loads(path.read_text(encoding="utf-8"))
    raw = payload.get("template_version_watch", payload)
    if not isinstance(raw, dict):
        raise SystemExit(f"{path}: expected a TOML table of template watch settings")

    paths = raw.get("paths", [])
    globs = raw.get("globs", [])
    exclude_globs = raw.get("exclude_globs", [])
    for key, value in {
        "paths": paths,
        "globs": globs,
        "exclude_globs": exclude_globs,
    }.items():
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            raise SystemExit(f"{path}: `{key}` must be a list of strings")
    return WatchConfig(
        paths=frozenset(normalize_path(item) for item in paths),
        globs=tuple(normalize_path(item) for item in globs),
        exclude_globs=tuple(normalize_path(item) for item in exclude_globs),
        source=path,
    )


def is_watched_path(path: str, config: WatchConfig) -> bool:
    normalized = normalize_path(path)
    if any(fnmatchcase(normalized, pattern) for pattern in config.exclude_globs):
        return False
    return normalized in config.paths or any(
        fnmatchcase(normalized, pattern) for pattern in config.globs
    )


def staged_paths(root: Path) -> list[str]:
    proc = run_git(
        ["diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        root,
    )
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def all_template_paths(root: Path, config: WatchConfig) -> list[str]:
    proc = run_git(["ls-files"], root)
    return sorted(path for path in proc.stdout.splitlines() if is_watched_path(path, config))


def read_staged_blob(root: Path, path: str) -> str:
    proc = run_git(["show", f":{path}"], root)
    return proc.stdout


def read_head_blob(root: Path, path: str) -> str | None:
    proc = run_git(["show", f"HEAD:{path}"], root, check=False)
    if proc.returncode != 0:
        return None
    return proc.stdout


def read_worktree(root: Path, path: str) -> str:
    return (root / path).read_text(encoding="utf-8")


def parse_simple_yaml(raw: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if key in {"template_id", "template_name", "template_version", "version"}:
            values[key] = value
    return values


def frontmatter_metadata(text: str) -> TemplateMetadata | None:
    if not text.startswith("---\n"):
        return None
    try:
        raw = text.split("---\n", 2)[1]
    except IndexError:
        return None
    values = parse_simple_yaml(raw)
    if not values:
        return None
    return TemplateMetadata(
        template_id=values.get("template_id") or values.get("template_name"),
        version=values.get("template_version") or values.get("version"),
        source="YAML front matter",
    )


def json_metadata(text: str) -> TemplateMetadata | None:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None
    raw_meta = payload.get("_template_metadata") or payload.get("template_metadata")
    if not isinstance(raw_meta, dict):
        return None
    template_id = raw_meta.get("template_id") or raw_meta.get("template_name")
    version = raw_meta.get("template_version") or raw_meta.get("version")
    return TemplateMetadata(
        template_id=str(template_id) if template_id is not None else None,
        version=str(version) if version is not None else None,
        source="JSON template metadata",
    )


def comment_metadata(text: str) -> TemplateMetadata | None:
    head = "\n".join(text.splitlines()[:40])
    values: dict[str, str] = {}
    for key, value in METADATA_KEY_RE.findall(head):
        values[key] = value.strip()
    if not values:
        return None
    return TemplateMetadata(
        template_id=values.get("template_id") or values.get("template_name"),
        version=values.get("template_version") or values.get("version"),
        source="comment metadata",
    )


def extract_metadata(text: str) -> TemplateMetadata | None:
    return frontmatter_metadata(text) or json_metadata(text) or comment_metadata(text)


def validate_metadata(path: str, metadata: TemplateMetadata | None) -> list[str]:
    errors: list[str] = []
    if metadata is None:
        errors.append(
            f"{path}: missing template metadata. Add YAML front matter for Markdown/text templates, "
            "JSON `_template_metadata`, or a top-of-file comment metadata block with "
            "`template_id` and `template_version`."
        )
        return errors
    if not metadata.template_id:
        errors.append(f"{path}: template metadata is missing `template_id`.")
    if not metadata.version:
        errors.append(f"{path}: template metadata is missing `template_version`.")
    elif not VERSION_RE.match(metadata.version):
        errors.append(
            f"{path}: template_version {metadata.version!r} is not semver-like `x.y.z`."
        )
    return errors


def validate_staged(root: Path, config: WatchConfig) -> list[str]:
    errors: list[str] = []
    paths = [path for path in staged_paths(root) if is_watched_path(path, config)]
    for path in paths:
        staged_text = read_staged_blob(root, path)
        staged_metadata = extract_metadata(staged_text)
        errors.extend(validate_metadata(path, staged_metadata))
        head_text = read_head_blob(root, path)
        if head_text is None or staged_metadata is None:
            continue
        head_metadata = extract_metadata(head_text)
        if head_text != staged_text and head_metadata is not None:
            if head_metadata.version == staged_metadata.version:
                errors.append(
                    f"{path}: template content changed but template_version stayed "
                    f"{staged_metadata.version!r}. Bump the version before committing; "
                    "major/minor/patch is a human decision."
                )
    return errors


def validate_all(root: Path, config: WatchConfig) -> list[str]:
    errors: list[str] = []
    for path in all_template_paths(root, config):
        try:
            text = read_worktree(root, path)
        except UnicodeDecodeError:
            continue
        errors.extend(validate_metadata(path, extract_metadata(text)))
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate Farplane template metadata and staged template version bumps."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--staged",
        action="store_true",
        help="Validate staged template files and require version bumps on edits.",
    )
    mode.add_argument(
        "--all",
        action="store_true",
        help="Validate metadata on all tracked template-like files.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="Repository root to validate (defaults to the current repo).",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Template watch config. Defaults to rules/template-version-watch.toml.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    config_path = args.config.resolve() if args.config else root / "rules" / "template-version-watch.toml"
    config = load_watch_config(config_path)
    errors = validate_all(root, config) if args.all else validate_staged(root, config)
    if errors:
        for error in errors:
            print(error)
        return 1
    mode = "all tracked templates" if args.all else "staged templates"
    print(f"template metadata OK ({mode})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
