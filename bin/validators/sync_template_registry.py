#!/usr/bin/env python3
"""Generate the Farplane template registry from template metadata."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
import tomllib
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = ROOT / "rules" / "template-registry.toml"
DEFAULT_REGISTRY = ROOT / "docs" / "templates" / "registry.jsonl"
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")


class TemplateRegistryError(Exception):
    pass


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "":
        return ""
    if value.startswith("[") and value.endswith("]"):
        try:
            return ast.literal_eval(value)
        except (SyntaxError, ValueError) as exc:
            raise TemplateRegistryError(f"invalid inline list: {value}") from exc
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        try:
            return ast.literal_eval(value)
        except (SyntaxError, ValueError):
            return value[1:-1]
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    return value


def parse_metadata_block(raw: str) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    current_key: str | None = None
    current_subkey: str | None = None

    for raw_line in raw.splitlines():
        if not raw_line.strip():
            continue
        if not raw_line.startswith(" "):
            current_subkey = None
            if ":" not in raw_line:
                continue
            key, raw_value = raw_line.split(":", 1)
            key = key.strip()
            value = raw_value.strip()
            metadata[key] = {} if value == "" else parse_scalar(value)
            current_key = key
            continue

        if current_key is None:
            continue

        stripped = raw_line.strip()
        current_value = metadata.get(current_key)
        if stripped.startswith("- "):
            item = parse_scalar(stripped[2:].strip())
            if current_subkey is not None and isinstance(current_value, dict):
                current_value.setdefault(current_subkey, []).append(item)
            else:
                if not isinstance(current_value, list):
                    current_value = []
                    metadata[current_key] = current_value
                current_value.append(item)
            continue

        if ":" in stripped:
            subkey, raw_value = stripped.split(":", 1)
            subkey = subkey.strip()
            value = raw_value.strip()
            if not isinstance(current_value, dict):
                current_value = {}
                metadata[current_key] = current_value
            current_value[subkey] = [] if value == "" else parse_scalar(value)
            current_subkey = subkey

    return metadata


def extract_frontmatter(text: str) -> dict[str, Any] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        raise TemplateRegistryError("unterminated YAML front matter")
    return parse_metadata_block(text[4:end])


def extract_html_comment_metadata(text: str) -> dict[str, Any] | None:
    if not text.startswith("<!--"):
        return None
    end = text.find("-->")
    if end == -1:
        raise TemplateRegistryError("unterminated HTML comment metadata")
    raw = text[4:end].strip("\n")
    return parse_metadata_block(raw)


def extract_json_metadata(text: str) -> dict[str, Any] | None:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict):
        return None
    raw_meta = payload.get("_template_metadata") or payload.get("template_metadata")
    if isinstance(raw_meta, dict):
        return raw_meta
    return None


def extract_toml_metadata(text: str) -> dict[str, Any] | None:
    try:
        payload = tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return None
    raw_meta = payload.get("_template_metadata") or payload.get("template_metadata")
    if isinstance(raw_meta, dict):
        return raw_meta
    return None


def extract_metadata(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    try:
        metadata = (
            extract_frontmatter(text)
            or extract_json_metadata(text)
            or extract_toml_metadata(text)
            or extract_html_comment_metadata(text)
        )
    except TemplateRegistryError as exc:
        raise TemplateRegistryError(f"{path}: {exc}") from exc
    if metadata is None:
        raise TemplateRegistryError(
            f"{path}: missing template metadata with template_id, template_version, and feature_refs"
        )
    return metadata


def normalize_string_list(value: Any, field: str, path: Path) -> list[str]:
    if isinstance(value, str) and value:
        return [value]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    raise TemplateRegistryError(f"{path}: {field} must be a non-empty string list")


def load_config(path: Path) -> list[str]:
    if not path.is_file():
        raise TemplateRegistryError(f"missing template registry config: {path}")
    payload = tomllib.loads(path.read_text(encoding="utf-8"))
    raw = payload.get("template_registry", payload)
    paths = raw.get("paths") if isinstance(raw, dict) else None
    if not isinstance(paths, list) or not all(isinstance(item, str) for item in paths):
        raise TemplateRegistryError(f"{path}: template_registry.paths must be a list of strings")
    return [item.replace("\\", "/").lstrip("./") for item in paths]


def load_feature_ids(root: Path) -> set[str]:
    path = root / "docs" / "features" / "registry.jsonl"
    ids: set[str] = set()
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise TemplateRegistryError(f"{path}:{line_number}: invalid JSON") from exc
        feature_id = row.get("id")
        if isinstance(feature_id, str):
            ids.add(feature_id)
    return ids


def build_registry(root: Path = ROOT, config_path: Path | None = None) -> list[dict[str, Any]]:
    config = config_path or root / "rules" / "template-registry.toml"
    feature_ids = load_feature_ids(root)
    rows: list[dict[str, Any]] = []
    seen_ids: dict[str, str] = {}

    for relative_path in load_config(config):
        path = root / relative_path
        if not path.is_file():
            raise TemplateRegistryError(f"{relative_path}: tracked template does not exist")
        metadata = extract_metadata(path)
        template_id = metadata.get("template_id") or metadata.get("template_name")
        template_version = metadata.get("template_version") or metadata.get("version")
        feature_refs = normalize_string_list(metadata.get("feature_refs"), "feature_refs", path)

        if not isinstance(template_id, str) or not template_id:
            raise TemplateRegistryError(f"{relative_path}: missing template_id")
        if template_id in seen_ids:
            raise TemplateRegistryError(
                f"{relative_path}: duplicate template_id {template_id!r}; already used by {seen_ids[template_id]}"
            )
        seen_ids[template_id] = relative_path

        if not isinstance(template_version, str) or not template_version:
            raise TemplateRegistryError(f"{relative_path}: missing template_version")
        if not VERSION_RE.match(template_version):
            raise TemplateRegistryError(
                f"{relative_path}: template_version {template_version!r} is not semver-like x.y.z"
            )

        missing_refs = [ref for ref in feature_refs if ref not in feature_ids]
        if missing_refs:
            raise TemplateRegistryError(
                f"{relative_path}: unknown feature_refs: {', '.join(missing_refs)}"
            )

        row: dict[str, Any] = {
            "template_id": template_id,
            "template_version": template_version,
            "path": relative_path,
            "feature_refs": feature_refs,
        }
        kind = metadata.get("kind")
        if isinstance(kind, str) and kind:
            row["kind"] = kind
        consumer_scope = metadata.get("consumer_scope")
        if isinstance(consumer_scope, str) and consumer_scope:
            row["consumer_scope"] = consumer_scope
        applies_to = metadata.get("applies_to")
        if applies_to not in (None, "", []):
            row["applies_to"] = normalize_string_list(applies_to, "applies_to", path)
        rows.append(row)

    return sorted(rows, key=lambda row: row["template_id"])


def render_jsonl(rows: list[dict[str, Any]]) -> str:
    return "".join(
        json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
        for row in rows
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate and validate docs/templates/registry.jsonl."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="Write the generated registry.")
    mode.add_argument("--check", action="store_true", help="Fail if the registry is stale.")
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root.")
    parser.add_argument("--config", type=Path, default=None, help="Template registry config.")
    parser.add_argument("--out", type=Path, default=None, help="Registry output path.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    config = args.config.resolve() if args.config else root / "rules" / "template-registry.toml"
    out = args.out.resolve() if args.out else root / "docs" / "templates" / "registry.jsonl"

    try:
        rendered = render_jsonl(build_registry(root, config))
        if args.write:
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(rendered, encoding="utf-8")
            print(f"wrote {out.relative_to(root)}")
            return 0
        existing = out.read_text(encoding="utf-8") if out.is_file() else ""
        if existing != rendered:
            print(
                f"{out.relative_to(root)} is stale; run `python3 bin/validators/sync_template_registry.py --write`",
                file=sys.stderr,
            )
            return 1
        print("template registry OK")
        return 0
    except TemplateRegistryError as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
