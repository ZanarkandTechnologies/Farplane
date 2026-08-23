"""Duplicate-safe parsing and changed-path discovery for static lint."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

import yaml
from yaml.resolver import BaseResolver


IGNORED_PARTS = frozenset({".git", ".farplane", "node_modules", "__pycache__", "artifacts", "build", "dist", "generated"})


class LintSourceError(ValueError):
    """Static source selection or parsing failed."""


class DuplicateKeyError(ValueError):
    """A JSON/YAML mapping would silently overwrite a previous key."""


class MarkdownFrontmatterError(ValueError):
    """A leading Markdown YAML-frontmatter block is missing or malformed."""


class UniqueYamlLoader(yaml.SafeLoader):
    """Safe YAML loader which rejects ambiguous duplicate mapping keys."""


def _construct_unique_mapping(
    loader: UniqueYamlLoader,
    node: yaml.nodes.MappingNode,
    deep: bool = False,
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise DuplicateKeyError("mapping keys must be scalar values") from exc
        if duplicate:
            raise DuplicateKeyError(str(key))
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueYamlLoader.add_constructor(BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping)


FRONTMATTER_RE = re.compile(
    r"\A---[ \t]*\r?\n(?P<yaml>.*?)\r?\n---[ \t]*(?:\r?\n|\Z)",
    re.DOTALL,
)


def _json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    mapping: dict[str, Any] = {}
    for key, value in pairs:
        if key in mapping:
            raise DuplicateKeyError(key)
        mapping[key] = value
    return mapping


def normalize_path(path: str) -> str:
    value = path.replace("\\", "/")
    while value.startswith("./"):
        value = value[2:]
    return value


def changed_paths(root: Path, *, base: str | None = None) -> tuple[str, ...]:
    """Return the explicit staged, working, untracked, and optional base paths."""

    commands = [
        ["git", "diff", "--name-only", "--cached", "--diff-filter=ACMR"],
        ["git", "diff", "--name-only", "--diff-filter=ACMR"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ]
    if base:
        commands.append(["git", "diff", "--name-only", "--diff-filter=ACMR", f"{base}...HEAD"])
    paths: set[str] = set()
    for command in commands:
        result = subprocess.run(command, cwd=root, text=True, capture_output=True, check=False)
        if result.returncode:
            raise LintSourceError(result.stderr.strip() or f"cannot read changed paths: {' '.join(command)}")
        paths.update(normalize_path(line) for line in result.stdout.splitlines() if line.strip())
    return tuple(sorted(paths))


def tracked_source_paths(root: Path, *, changed: bool = False, base: str | None = None) -> tuple[Path, ...]:
    """Return source JSON/YAML paths while excluding dependencies and artifacts."""

    if changed:
        candidates = changed_paths(root, base=base)
    else:
        result = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode:
            raise LintSourceError(result.stderr.strip() or "cannot read source paths")
        candidates = tuple(normalize_path(line) for line in result.stdout.splitlines() if line.strip())
    return tuple(
        sorted(
            Path(path)
            for path in candidates
            if Path(path).suffix in {".json", ".yaml", ".yml"}
            and not (set(Path(path).parts) & IGNORED_PARTS)
            and (root / path).is_file()
        )
    )


def parse_source_file(path: Path) -> None:
    """Parse one JSON/YAML source file with duplicate-key protection."""

    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        json.loads(text, object_pairs_hook=_json_object)
    else:
        yaml.load(text, Loader=UniqueYamlLoader)


def parse_markdown_frontmatter_document(
    text: str,
    path: Path,
    *,
    required: bool = False,
) -> tuple[dict[str, Any] | None, str, str]:
    """Read one leading YAML mapping with duplicate-key protection."""

    match = FRONTMATTER_RE.match(text)
    if match is None:
        if text.startswith("---"):
            raise MarkdownFrontmatterError(f"{path}: unterminated frontmatter")
        if required:
            raise MarkdownFrontmatterError(f"{path}: missing frontmatter")
        return None, "", text
    raw = match.group("yaml")
    try:
        metadata = yaml.load(raw, Loader=UniqueYamlLoader)
    except DuplicateKeyError as exc:
        raise MarkdownFrontmatterError(f"{path}: duplicate frontmatter keys: {exc}") from exc
    except yaml.YAMLError as exc:
        raise MarkdownFrontmatterError(f"{path}: invalid YAML frontmatter: {exc}") from exc
    if metadata is None:
        metadata = {}
    if not isinstance(metadata, dict):
        raise MarkdownFrontmatterError(f"{path}: frontmatter must be a mapping")
    if not all(isinstance(key, str) for key in metadata):
        raise MarkdownFrontmatterError(f"{path}: frontmatter keys must be strings")
    return metadata, raw, text[match.end() :].lstrip("\r\n")


def parse_markdown_frontmatter(path: Path, *, required: bool = False) -> dict[str, Any] | None:
    """Read just the leading frontmatter mapping from a Markdown source file."""

    metadata, _raw, _body = parse_markdown_frontmatter_document(
        path.read_text(encoding="utf-8"),
        path,
        required=required,
    )
    return metadata


def lint_source_syntax(root: Path, *, changed: bool = False, base: str | None = None) -> list[str]:
    """Return deterministic JSON/YAML parse diagnostics for selected sources."""

    errors: list[str] = []
    for relative_path in tracked_source_paths(root, changed=changed, base=base):
        try:
            parse_source_file(root / relative_path)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, yaml.YAMLError, DuplicateKeyError) as exc:
            errors.append(f"{relative_path}: {exc}")
    return errors
