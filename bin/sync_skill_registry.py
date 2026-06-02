#!/usr/bin/env python3
"""Generate the Farplane skill registry from skill frontmatter."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path
from typing import Any


SKILL_LINK_RE = re.compile(r"\]\((?:\.\./)?([^/\)\s]+)/SKILL\.md(?:#([^)]+))?\)")
LOCAL_METHOD_RE = re.compile(r"\]\(SKILL\.md#([^)]+)\)")
CHECKLIST_BEGIN = "<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->"
CHECKLIST_END = "<!-- END FARPLANE_IMPORTANT_CHECKLIST -->"
CHECKLIST_RE = re.compile(
    rf"^{re.escape(CHECKLIST_BEGIN)}\n"
    r"## Important Checklist\n\n"
    r"(?:Source: `[^\n]+`\n\n)?"
    rf"(.*?)\n^{re.escape(CHECKLIST_END)}",
    re.MULTILINE | re.DOTALL,
)
ALLOWED_COMMON_CHAIN_KEYS = {"after"}
TIER1_PRIMITIVES = {"advise", "reference-grounding", "review"}
ALLOWED_SOURCES = {"local", "external"}


class RegistryError(Exception):
    pass


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "":
        return ""
    if value.startswith("[") and value.endswith("]"):
        try:
            return ast.literal_eval(value)
        except (SyntaxError, ValueError) as exc:
            raise RegistryError(f"invalid inline list: {value}") from exc
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
        raise RegistryError(f"{path}: missing frontmatter")
    end = text.find("\n---", 4)
    if end == -1:
        raise RegistryError(f"{path}: unterminated frontmatter")

    metadata: dict[str, Any] = {}
    duplicates: set[str] = set()
    current_key: str | None = None
    current_subkey: str | None = None

    for raw_line in text[4:end].splitlines():
        if not raw_line.strip():
            continue
        if not raw_line.startswith(" "):
            current_subkey = None
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

    if duplicates:
        duplicate_list = ", ".join(sorted(duplicates))
        raise RegistryError(f"{path}: duplicate frontmatter keys: {duplicate_list}")
    return metadata


def normalize_string_list(value: Any, field: str, path: Path) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    raise RegistryError(f"{path}: {field} must be a string or list of strings")


def normalize_allowed_tools(value: Any, path: Path) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return value
    raise RegistryError(f"{path}: allowed-tools must be a comma string or list")


def collect_skill_links_from_paths(paths: list[Path], skill_name: str) -> list[str]:
    links: set[str] = set()
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text()
        for match in SKILL_LINK_RE.finditer(text):
            target, anchor = match.groups()
            if target in {".", skill_name}:
                continue
            links.add(f"{target}#{anchor}" if anchor else target)
        for match in LOCAL_METHOD_RE.finditer(text):
            links.add(f"{skill_name}#{match.group(1)}")
    return sorted(links)


def collect_skill_links_from_text(text: str, skill_name: str) -> list[str]:
    links: set[str] = set()
    for match in SKILL_LINK_RE.finditer(text):
        target, anchor = match.groups()
        if target in {".", skill_name}:
            continue
        links.add(f"{target}#{anchor}" if anchor else target)
    for match in LOCAL_METHOD_RE.finditer(text):
        links.add(f"{skill_name}#{match.group(1)}")
    return sorted(links)


def extract_direct_checklist(skill_path: Path) -> str:
    text = skill_path.read_text()
    match = CHECKLIST_RE.search(text)
    return match.group(1).strip() if match else ""


def checklist_source_text(skill_dir: Path) -> str:
    direct_checklist = extract_direct_checklist(skill_dir / "SKILL.md")
    if direct_checklist:
        return direct_checklist
    todos_path = skill_dir / "todos.md"
    if todos_path.exists():
        text = todos_path.read_text().strip()
        if text.startswith("# Todos\n"):
            return text.split("\n", 1)[1].strip()
        return text
    return ""


def collect_checklist_links(skill_dir: Path, skill_name: str) -> list[str]:
    return collect_skill_links_from_text(checklist_source_text(skill_dir), skill_name)


def collect_skill_links(skill_dir: Path, skill_name: str) -> list[str]:
    return collect_skill_links_from_paths(
        [skill_dir / "SKILL.md", skill_dir / "todos.md"],
        skill_name,
    )


def skill_ref_name(ref: str) -> str:
    return ref.split("#", 1)[0].split(":", 1)[0]


def normalize_common_chains(value: Any, path: Path, tier: int) -> dict[str, list[str]]:
    if value in (None, ""):
        return {}
    if tier != 3:
        raise RegistryError(f"{path}: common_chains is only allowed on tier 3 skills")
    if not isinstance(value, dict):
        raise RegistryError(f"{path}: common_chains must be a mapping")

    unknown = set(value) - ALLOWED_COMMON_CHAIN_KEYS
    if unknown:
        names = ", ".join(sorted(unknown))
        raise RegistryError(f"{path}: unsupported common_chains keys: {names}")

    normalized: dict[str, list[str]] = {}
    for key in sorted(value):
        normalized[key] = normalize_string_list(value[key], f"common_chains.{key}", path)
    return normalized


def validate_skill_ref(ref: str, skill_names: set[str], methods_by_skill: dict[str, set[str]]) -> None:
    if ref.endswith(":*"):
        skill_name = ref[:-2]
        if skill_name not in skill_names:
            raise RegistryError(f"unknown skill reference: {ref}")
        return

    if ":" in ref:
        skill_name, _method = ref.split(":", 1)
        if skill_name not in skill_names:
            raise RegistryError(f"unknown skill reference: {ref}")
        if ref not in methods_by_skill.get(skill_name, set()):
            raise RegistryError(f"method reference is not declared in frontmatter: {ref}")
        return

    if ref not in skill_names:
        raise RegistryError(f"unknown skill reference: {ref}")


def validate_common_chain_refs(rows: list[dict[str, Any]]) -> None:
    skill_names = {row["name"] for row in rows}
    methods_by_skill = {row["name"]: set(row.get("methods", [])) for row in rows}
    for row in rows:
        for ref in row.get("common_chains", {}).get("after", []):
            validate_skill_ref(ref, skill_names, methods_by_skill)


def validate_todos_hierarchy(repo_root: Path, rows: list[dict[str, Any]]) -> None:
    tier_by_name = {row["name"]: row["tier"] for row in rows}
    for row in rows:
        if row["tier"] != 3 or not row["has_checklist"]:
            continue

        skill_dir = repo_root / "skills" / row["name"]
        checklist_links = collect_checklist_links(skill_dir, row["name"])
        direct_tier1_links = [
            link
            for link in checklist_links
            if tier_by_name.get(skill_ref_name(link)) == 1
            or skill_ref_name(link) in TIER1_PRIMITIVES
        ]
        if direct_tier1_links:
            refs = ", ".join(sorted(direct_tier1_links))
            source_path = skill_dir / "SKILL.md"
            raise RegistryError(
                f"{source_path}: tier 3 checklist must link tier 2 surfaces instead of "
                f"direct tier 1 primitives: {refs}"
            )


def build_registry(repo_root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    skill_paths = sorted((repo_root / "skills").glob("*/SKILL.md"))

    for skill_path in skill_paths:
        skill_dir = skill_path.parent
        metadata = parse_frontmatter(skill_path)
        name = metadata.get("name")
        if name != skill_dir.name:
            raise RegistryError(f"{skill_path}: name must match directory {skill_dir.name!r}")

        tier = metadata.get("tier")
        if tier not in (1, 2, 3):
            raise RegistryError(f"{skill_path}: tier must be 1, 2, or 3")
        source = metadata.get("source")
        if source not in ALLOWED_SOURCES:
            allowed = ", ".join(sorted(ALLOWED_SOURCES))
            raise RegistryError(f"{skill_path}: source must be one of: {allowed}")
        group = metadata.get("group")
        if tier == 3 and not isinstance(group, str):
            raise RegistryError(f"{skill_path}: tier 3 skills must set group")
        if tier != 3 and group not in (None, ""):
            raise RegistryError(f"{skill_path}: group is only allowed on tier 3 skills")

        has_todos = (skill_dir / "todos.md").exists()
        has_checklist = bool(checklist_source_text(skill_dir))
        row: dict[str, Any] = {
            "name": name,
            "tier": tier,
            "source": source,
            "path": str(skill_path.relative_to(repo_root)),
            "description": metadata.get("description", ""),
            "has_checklist": has_checklist,
            "has_todos": has_todos,
            "skill_links": collect_skill_links(skill_dir, name),
        }
        if tier == 3:
            row["group"] = group

        methods = normalize_string_list(metadata.get("methods"), "methods", skill_path)
        if methods:
            row["methods"] = methods

        common_chains = normalize_common_chains(metadata.get("common_chains"), skill_path, tier)
        if common_chains:
            row["common_chains"] = common_chains

        version = metadata.get("version")
        if version not in (None, ""):
            row["version"] = str(version)

        allowed_tools = normalize_allowed_tools(metadata.get("allowed-tools"), skill_path)
        if allowed_tools:
            row["allowed_tools"] = allowed_tools

        upstream_url = metadata.get("upstream_url")
        if upstream_url not in (None, ""):
            row["upstream_url"] = str(upstream_url)

        rows.append(row)

    validate_common_chain_refs(rows)
    validate_todos_hierarchy(repo_root, rows)
    return rows


def render_jsonl(rows: list[dict[str, Any]]) -> str:
    return "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows)


def write_registry(repo_root: Path, content: str) -> None:
    target = repo_root / "docs" / "skills" / "registry.jsonl"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)


def check_registry(repo_root: Path, content: str) -> int:
    target = repo_root / "docs" / "skills" / "registry.jsonl"
    if not target.exists():
        print(f"{target} is missing; run with --write", file=sys.stderr)
        return 1
    existing = target.read_text()
    if existing != content:
        print(f"{target} is stale; run with --write", file=sys.stderr)
        return 1
    print(f"skill registry OK ({len(content.splitlines())} skill rows)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="write docs/skills/registry.jsonl")
    parser.add_argument("--check", action="store_true", help="verify registry is up to date")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    try:
        rows = build_registry(repo_root)
        content = render_jsonl(rows)
    except RegistryError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.write:
        write_registry(repo_root, content)
        print(f"wrote docs/skills/registry.jsonl ({len(content.splitlines())} skill rows)")
        return 0
    return check_registry(repo_root, content)


if __name__ == "__main__":
    raise SystemExit(main())
