"""Parse and validate the small frontmatter contract shared by skill tooling."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any


METHOD_CLASSES = {"artifact", "integration", "internal"}


class SkillFrontmatterError(ValueError):
    """Raised when a skill's structured frontmatter is malformed."""


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "":
        return ""
    if value.startswith("[") and value.endswith("]"):
        try:
            return ast.literal_eval(value)
        except (SyntaxError, ValueError) as exc:
            raise SkillFrontmatterError(f"invalid inline list: {value}") from exc
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        try:
            return ast.literal_eval(value)
        except (SyntaxError, ValueError):
            return value[1:-1]
    if value.isdigit():
        return int(value)
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    return value


def parse_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text()
    if not text.startswith("---\n"):
        raise SkillFrontmatterError(f"{path}: missing frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        raise SkillFrontmatterError(f"{path}: unterminated frontmatter")

    metadata: dict[str, Any] = {}
    duplicates: set[str] = set()
    current_key: str | None = None
    current_subkey: str | None = None
    current_list_item: dict[str, Any] | None = None

    for raw_line in text[4:end].splitlines():
        if not raw_line.strip():
            continue
        if not raw_line.startswith(" "):
            current_subkey = None
            current_list_item = None
            if ":" not in raw_line:
                continue
            key, raw_value = raw_line.split(":", 1)
            key = key.strip()
            if key in metadata:
                duplicates.add(key)
            value = raw_value.strip()
            metadata[key] = {} if value == "" else parse_scalar(value)
            current_key = key
            continue

        if current_key is None:
            continue

        stripped = raw_line.strip()
        current_value = metadata.get(current_key)
        indentation = len(raw_line) - len(raw_line.lstrip(" "))
        if indentation == 2 and stripped.startswith("- "):
            item_value = stripped[2:].strip()
            item_key, separator, raw_item_value = item_value.partition(": ")
            if separator:
                item: Any = {item_key.strip(): parse_scalar(raw_item_value)}
                current_list_item = item
            else:
                item = parse_scalar(item_value)
                current_list_item = None
            if current_subkey is not None and isinstance(current_value, dict):
                current_value.setdefault(current_subkey, []).append(item)
            else:
                if not isinstance(current_value, list):
                    current_value = []
                    metadata[current_key] = current_value
                current_value.append(item)
            continue

        if indentation >= 4 and current_list_item is not None and ":" in stripped:
            subkey, raw_value = stripped.split(":", 1)
            current_list_item[subkey.strip()] = parse_scalar(raw_value.strip())
            continue

        if indentation == 2 and ":" in stripped:
            current_list_item = None
            subkey, raw_value = stripped.split(":", 1)
            subkey = subkey.strip()
            value = raw_value.strip()
            if not isinstance(current_value, dict):
                current_value = {}
                metadata[current_key] = current_value
            current_value[subkey] = [] if value == "" else parse_scalar(value)
            current_subkey = subkey

    if duplicates:
        duplicate_list = ", ".join(sorted(duplicates))
        raise SkillFrontmatterError(f"{path}: duplicate frontmatter keys: {duplicate_list}")
    return metadata


def normalize_method_contracts(value: Any, skill_name: str, path: Path) -> list[dict[str, str]]:
    if value in (None, ""):
        return []
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise SkillFrontmatterError(
            f"{path}: methods must be a list of mappings with id, class, and output"
        )

    contracts: list[dict[str, str]] = []
    seen_ids: set[str] = set()
    for item in value:
        unknown = set(item) - {"id", "class", "output"}
        if unknown:
            names = ", ".join(sorted(unknown))
            raise SkillFrontmatterError(f"{path}: methods entry has unsupported field(s): {names}")
        method_id = item.get("id")
        method_class = item.get("class")
        output = item.get("output")
        if not isinstance(method_id, str) or not method_id.startswith(f"{skill_name}:"):
            raise SkillFrontmatterError(f"{path}: method id must start with {skill_name}:")
        if method_id in seen_ids:
            raise SkillFrontmatterError(f"{path}: duplicate method id {method_id}")
        if method_class not in METHOD_CLASSES:
            allowed = ", ".join(sorted(METHOD_CLASSES))
            raise SkillFrontmatterError(
                f"{path}: method {method_id} class must be one of: {allowed}"
            )
        if not isinstance(output, str) or not output.strip():
            raise SkillFrontmatterError(f"{path}: method {method_id} output must be a non-empty string")
        seen_ids.add(method_id)
        contracts.append({"id": method_id, "class": method_class, "output": output})
    return contracts
