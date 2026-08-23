#!/usr/bin/env python3
"""Generate the Farplane skill registry from skill frontmatter."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bin.core.skill_departments import DepartmentTaxonomyError, load_skill_departments
from bin.core.skill_contract import (
    FrontmatterError,
    normalize_capability_contract as parse_capability_contract,
    normalize_method_contracts as parse_method_contracts,
    normalize_skill_frontmatter,
    parse_skill_frontmatter,
)
from bin.validators.template_usage import TemplateUsageError, normalize_template_uses


SKILL_LINK_RE = re.compile(r"\]\((?:\.\./)?([^/\)\s]+)/SKILL\.md(?:#([^)]+))?\)")
LOCAL_METHOD_RE = re.compile(r"\]\(SKILL\.md#([^)]+)\)")
CHECKLIST_BEGIN = "<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->"
CHECKLIST_END = "<!-- END FARPLANE_IMPORTANT_CHECKLIST -->"
CHECKLIST_RE = re.compile(
    rf"^{re.escape(CHECKLIST_BEGIN)}\n"
    r"## Todo List\n\n"
    r"(?:Source: `[^\n]+`\n\n)?"
    rf"(.*?)\n^{re.escape(CHECKLIST_END)}",
    re.MULTILINE | re.DOTALL,
)
ALLOWED_COMMON_CHAIN_KEYS = {"after"}
TIER1_PRIMITIVES = {"advise", "reference-grounding", "prototyping"}
PROTOCOL_WRAPPERS = {"review"}
ALLOWED_SOURCES = {"local", "external"}
DESCRIPTION_MAX_CHARS = 220
SURFACE_FIELDS = {"eval", "qa_checklist", "skill_ui"}
RETIRED_FRONTMATTER_FIELDS = {"workflow"}

try:
    SKILL_DEPARTMENTS = load_skill_departments(ROOT)
except DepartmentTaxonomyError as exc:
    raise RuntimeError(str(exc)) from exc


class RegistryError(Exception):
    pass


def normalize_method_contracts(value: Any, skill_name: str, path: Path) -> list[dict[str, str]]:
    try:
        return parse_method_contracts(value, skill_name, path)
    except FrontmatterError as exc:
        raise RegistryError(str(exc)) from exc


def normalize_capability_contract(
    value: Any,
    path: Path,
) -> dict[str, Any] | None:
    try:
        return parse_capability_contract(value, path)
    except FrontmatterError as exc:
        raise RegistryError(str(exc)) from exc


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


def normalize_surface_field(value: Any, field: str, path: Path) -> str | dict[str, Any]:
    if value in (None, ""):
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        if "path" in value and not isinstance(value["path"], str):
            raise RegistryError(f"{path}: {field}.path must be a string")
        if "status" in value and not isinstance(value["status"], str):
            raise RegistryError(f"{path}: {field}.status must be a string")
        return value
    raise RegistryError(f"{path}: {field} must be a string path or mapping")


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


def collect_ordered_skill_refs_from_text(
    text: str,
    skill_name: str,
    skill_names: set[str],
) -> list[str]:
    """Collect first-seen skill references from todo text in human order."""

    candidates: list[tuple[int, str]] = []
    for match in SKILL_LINK_RE.finditer(text):
        target, _anchor = match.groups()
        target = skill_ref_name(target)
        if target in skill_names and target != skill_name:
            candidates.append((match.start(), target))

    for target in skill_names:
        if target == skill_name:
            continue
        explicit_patterns = [
            rf"(?<![A-Za-z0-9_-])\${re.escape(target)}(?![A-Za-z0-9_-])",
            rf"`{re.escape(target)}(?:[#:][^`]*)?`",
            rf"`(?:skills/|\.\./)?{re.escape(target)}/SKILL\.md(?:#[^`]*)?`",
        ]
        for pattern in explicit_patterns:
            for match in re.finditer(pattern, text):
                candidates.append((match.start(), target))

    ordered: list[str] = []
    seen: set[str] = set()
    for _position, target in sorted(candidates, key=lambda item: (item[0], item[1])):
        if target in seen:
            continue
        seen.add(target)
        ordered.append(target)
    return ordered


def extract_direct_checklist(skill_path: Path) -> str:
    text = skill_path.read_text()
    match = CHECKLIST_RE.search(text)
    return match.group(1).strip() if match else ""


def checklist_source_text(skill_dir: Path) -> str:
    direct_checklist = extract_direct_checklist(skill_dir / "SKILL.md")
    return direct_checklist


def collect_checklist_links(skill_dir: Path, skill_name: str) -> list[str]:
    return collect_skill_links_from_text(checklist_source_text(skill_dir), skill_name)


def collect_todo_skill_refs(skill_dir: Path, skill_name: str, skill_names: set[str]) -> list[str]:
    return collect_ordered_skill_refs_from_text(checklist_source_text(skill_dir), skill_name, skill_names)


def collect_skill_links(skill_dir: Path, skill_name: str) -> list[str]:
    return collect_skill_links_from_paths(
        [skill_dir / "SKILL.md"],
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
    methods_by_skill = {
        row["name"]: {str(method["id"]) for method in row.get("methods", [])}
        for row in rows
    }
    for row in rows:
        for ref in row.get("common_chains", {}).get("after", []):
            validate_skill_ref(ref, skill_names, methods_by_skill)


def attach_todo_skill_refs(repo_root: Path, rows: list[dict[str, Any]]) -> None:
    skill_names = {row["name"] for row in rows}
    for row in rows:
        skill_dir = repo_root / "skills" / row["name"]
        refs = collect_todo_skill_refs(skill_dir, row["name"], skill_names)
        if refs:
            row["todo_skill_refs"] = refs


def validate_shortcut_composition_leaves(
    repo_root: Path,
    rows: list[dict[str, Any]],
) -> None:
    """Keep explicit-only shortcuts out of composition edges in both directions."""

    shortcut_names = {
        row["name"]
        for row in rows
        if isinstance(row.get("capability"), dict)
        and row["capability"].get("kind") == "shortcut"
    }
    if not shortcut_names:
        return
    for row in rows:
        composition_refs = {
            "todo_skill_refs": [
                skill_ref_name(ref) for ref in row.get("todo_skill_refs", [])
            ],
            "skill_links": [skill_ref_name(ref) for ref in row.get("skill_links", [])],
            "common_chains": [
                skill_ref_name(ref)
                for ref in row.get("common_chains", {}).get("after", [])
            ],
        }
        targeted = {
            field: sorted(set(refs) & shortcut_names)
            for field, refs in composition_refs.items()
            if set(refs) & shortcut_names
        }
        if targeted:
            details = "; ".join(
                f"{field}={','.join(refs)}" for field, refs in targeted.items()
            )
            source_path = repo_root / row["path"]
            raise RegistryError(
                f"{source_path}: composition must not target explicit-only shortcut "
                f"skill(s) ({details})"
            )

    for row in rows:
        capability = row.get("capability")
        if not isinstance(capability, dict) or capability.get("kind") != "shortcut":
            continue
        composition_refs = {
            "todo_skill_refs": [
                skill_ref_name(ref) for ref in row.get("todo_skill_refs", [])
            ],
            "skill_links": [skill_ref_name(ref) for ref in row.get("skill_links", [])],
            "common_chains": [
                skill_ref_name(ref)
                for ref in row.get("common_chains", {}).get("after", [])
            ],
        }
        populated = {
            field: sorted(set(refs))
            for field, refs in composition_refs.items()
            if refs
        }
        if populated:
            details = "; ".join(
                f"{field}={','.join(refs)}" for field, refs in populated.items()
            )
            source_path = repo_root / row["path"]
            raise RegistryError(
                f"{source_path}: explicit-only shortcut must be a composition leaf; "
                f"remove outbound composition refs ({details})"
            )


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
            if skill_ref_name(link) not in PROTOCOL_WRAPPERS
            and (
                tier_by_name.get(skill_ref_name(link)) == 1
                or skill_ref_name(link) in TIER1_PRIMITIVES
            )
        ]
        if direct_tier1_links:
            refs = ", ".join(sorted(direct_tier1_links))
            source_path = skill_dir / "SKILL.md"
            raise RegistryError(
                f"{source_path}: tier 3 todo list must link tier 2 surfaces instead of "
                f"direct tier 1 primitives: {refs}"
            )


def build_registry(repo_root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    skill_paths = sorted((repo_root / "skills").glob("*/SKILL.md"))

    for skill_path in skill_paths:
        skill_dir = skill_path.parent
        try:
            metadata = parse_skill_frontmatter(skill_path)
            metadata = normalize_skill_frontmatter(metadata, skill_path)
        except FrontmatterError as exc:
            raise RegistryError(str(exc)) from exc
        retired_fields = RETIRED_FRONTMATTER_FIELDS.intersection(metadata)
        if retired_fields:
            names = ", ".join(sorted(retired_fields))
            raise RegistryError(
                f"{skill_path}: retired frontmatter field(s): {names}; "
                "skill graph importance is derived from observed skill heat"
            )

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
        description = metadata.get("description", "")
        if not isinstance(description, str) or not description.strip():
            raise RegistryError(f"{skill_path}: description must be a non-empty string")
        if len(description) > DESCRIPTION_MAX_CHARS:
            raise RegistryError(
                f"{skill_path}: description is {len(description)} chars; "
                f"keep it at or below {DESCRIPTION_MAX_CHARS} chars"
            )
        group = metadata.get("group")
        if tier == 3 and (
            not isinstance(group, str) or group.strip() not in SKILL_DEPARTMENTS
        ):
            allowed = ", ".join(SKILL_DEPARTMENTS)
            raise RegistryError(
                f"{skill_path}: tier 3 group must be one of the canonical departments: {allowed}"
            )
        if tier != 3 and group not in (None, ""):
            raise RegistryError(f"{skill_path}: group is only allowed on tier 3 skills")
        if metadata.get("feature_refs") not in (None, "", []):
            raise RegistryError(
                f"{skill_path}: feature_refs moved to versioned skill template metadata; "
                "use eval, qa_checklist, or skill_ui for skill-local surfaces"
            )
        canonical_eval = skill_dir / "evals" / "evals.json"
        if canonical_eval.exists() and metadata.get("eval") != "evals/evals.json":
            raise RegistryError(
                f"{skill_path}: {canonical_eval.relative_to(repo_root)} exists but frontmatter must declare "
                "eval: evals/evals.json"
            )

        has_checklist = bool(checklist_source_text(skill_dir))
        row: dict[str, Any] = {
            "name": name,
            "tier": tier,
            "source": source,
            "path": str(skill_path.relative_to(repo_root)),
            "description": description,
            "has_checklist": has_checklist,
            "skill_links": collect_skill_links(skill_dir, name),
        }
        if tier == 3:
            row["group"] = group
        methods = normalize_method_contracts(metadata.get("methods"), name, skill_path)
        if methods:
            row["methods"] = methods

        capability = normalize_capability_contract(
            metadata.get("capability"),
            skill_path,
        )
        if capability:
            row["capability"] = capability

        common_chains = normalize_common_chains(metadata.get("common_chains"), skill_path, tier)
        if common_chains:
            row["common_chains"] = common_chains

        version = metadata.get("version")
        if version not in (None, ""):
            row["version"] = str(version)

        try:
            template_uses = normalize_template_uses(metadata, skill_path)
        except TemplateUsageError as exc:
            raise RegistryError(str(exc)) from exc
        if template_uses:
            row["template_uses"] = template_uses
            if "skill-template" in template_uses:
                row["skill_template_version"] = template_uses["skill-template"]

        allowed_tools = normalize_allowed_tools(metadata.get("allowed-tools"), skill_path)
        if allowed_tools:
            row["allowed_tools"] = allowed_tools

        for field in sorted(SURFACE_FIELDS):
            normalized_surface = normalize_surface_field(metadata.get(field), field, skill_path)
            if normalized_surface:
                row[field] = normalized_surface

        upstream_url = metadata.get("upstream_url")
        if upstream_url not in (None, ""):
            row["upstream_url"] = str(upstream_url)

        rows.append(row)

    attach_todo_skill_refs(repo_root, rows)
    validate_shortcut_composition_leaves(repo_root, rows)
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

    repo_root = Path(__file__).resolve().parents[2]
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
