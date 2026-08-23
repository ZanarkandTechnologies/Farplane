#!/usr/bin/env python3
"""Apply the field-preserving Farplane framework 2.0.16 migration."""

from __future__ import annotations

import argparse
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any

import yaml

FRAMEWORK_VERSION = "2.0.16"
METRICS_TEMPLATE_VERSION = "0.4.0"
HARNESS_TEMPLATE_VERSION = "0.5.3"
BINDINGS_TEMPLATE_VERSION = "0.5.0"
MIGRATION_DATE = "2026-08-19"
LEGACY_TYPE_MAP = {
    "daily": "flow",
    "daily_count": "flow",
    "point": "stock",
}
REMOVED_METRIC_FIELDS = {
    "aggregation",
    "cumulative",
    "formula",
    "windows",
    "cadence",
    "alignment",
    "timezone",
    "compare",
    "value_type",
}


def _atomic_write(path: Path, content: str) -> None:
    mode = path.stat().st_mode
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        handle.write(content)
        temporary = Path(handle.name)
    os.chmod(temporary, mode)
    os.replace(temporary, path)


def _migrate_manifest(path: Path) -> tuple[str, list[str]]:
    source = json.loads(path.read_text(encoding="utf-8"))
    template = json.loads(
        (Path(__file__).parents[1] / "references" / "MANIFEST_TEMPLATE.json").read_text(
            encoding="utf-8"
        )
    )
    if not isinstance(source, dict):
        raise ValueError("farplane/manifest.json must contain an object")
    changes: list[str] = []
    if source.get("spec_version") != FRAMEWORK_VERSION:
        source["spec_version"] = FRAMEWORK_VERSION
        changes.append(f"manifest.spec_version -> {FRAMEWORK_VERSION}")
    template_uses = source.setdefault("template_uses", {})
    if not isinstance(template_uses, dict):
        raise ValueError("manifest.template_uses must contain an object")
    if template_uses.get("farplane-framework") != FRAMEWORK_VERSION:
        template_uses["farplane-framework"] = FRAMEWORK_VERSION
        changes.append(f"manifest.template_uses.farplane-framework -> {FRAMEWORK_VERSION}")
    for key in ("_template_metadata", "standard", "optional"):
        if source.get(key) != template[key]:
            source[key] = template[key]
            changes.append(f"manifest.{key} -> {FRAMEWORK_VERSION} standard")
    return json.dumps(source, indent=2, ensure_ascii=False) + "\n", changes


def _migrate_metrics(path: Path) -> tuple[str, list[str]]:
    text = path.read_text(encoding="utf-8")
    changes: list[str] = []
    previous_text = text
    text, count = re.subn(
        r'(?m)^framework_template_version:\s*["\']?[^\s"\']+["\']?\s*$',
        f'framework_template_version: "{METRICS_TEMPLATE_VERSION}"',
        text,
    )
    if count != 1:
        raise ValueError("metrics.yaml must define framework_template_version exactly once")
    if text != previous_text:
        changes.append(f"metrics.framework_template_version -> {METRICS_TEMPLATE_VERSION}")
    previous_text = text
    text, count = re.subn(
        r"(?m)^updated_at:\s*\S+\s*$", f"updated_at: {MIGRATION_DATE}", text
    )
    if count != 1:
        raise ValueError("metrics.yaml must define updated_at exactly once")
    if text != previous_text:
        changes.append(f"metrics.updated_at -> {MIGRATION_DATE}")

    migrated_kinds: list[str] = []

    def replace_kind(match: re.Match[str]) -> str:
        indent, legacy = match.groups()
        metric_type = LEGACY_TYPE_MAP.get(legacy)
        if metric_type is None:
            raise ValueError(f"unsupported legacy metric kind: {legacy}")
        migrated_kinds.append(f"{legacy}->{metric_type}")
        return f"{indent}type: {metric_type}"

    text = re.sub(
        r"(?m)^(\s{4,})kind:\s*(daily_count|daily|point)\s*$",
        replace_kind,
        text,
    )
    if migrated_kinds:
        changes.append(f"metrics.kind -> type ({len(migrated_kinds)} definitions)")

    legacy_fields = sorted(
        {
            match.group(1)
            for match in re.finditer(r"(?m)^\s{4,}([a-z_]+):", text)
            if match.group(1) in REMOVED_METRIC_FIELDS
        }
    )
    if legacy_fields:
        raise ValueError(
            "metrics.yaml still contains removed projection fields: "
            + ", ".join(legacy_fields)
            + "; replace them with a refresh prompt or typed observation before retrying"
        )
    remaining_kinds = re.findall(r"(?m)^\s{4,}kind:\s*(\S+)", text)
    if remaining_kinds:
        raise ValueError(
            "metrics.yaml contains unsupported legacy metric kinds: "
            + ", ".join(sorted(set(remaining_kinds)))
        )
    source = yaml.safe_load(text)
    if not isinstance(source, dict) or not isinstance(source.get("metrics"), dict):
        raise ValueError("metrics.yaml must contain a metrics object")
    missing_refresh = [
        metric_id
        for metric_id, metric in source["metrics"].items()
        if isinstance(metric, dict) and "refresh" not in metric and "refresh_ref" not in metric
    ]
    duplicate_refresh = [
        metric_id
        for metric_id, metric in source["metrics"].items()
        if isinstance(metric, dict) and "refresh" in metric and "refresh_ref" in metric
    ]
    if duplicate_refresh:
        raise ValueError(
            "metrics define both refresh and refresh_ref: " + ", ".join(duplicate_refresh)
        )
    if missing_refresh:
        refreshers = source.setdefault("refreshers", {})
        if not isinstance(refreshers, dict):
            raise ValueError("metrics.refreshers must contain an object")
        refresher = refreshers.setdefault(
            "local_project_metrics",
            {
                "refresh": (
                    "Read the metric definition and project-local evidence for the requested "
                    "date; write one raw observation per metric with provenance and explicit "
                    "source gaps. Never infer a healthy zero from missing evidence."
                ),
                "provides": [],
            },
        )
        if not isinstance(refresher, dict):
            raise ValueError("metrics.refreshers.local_project_metrics must contain an object")
        provides = refresher.setdefault("provides", [])
        if not isinstance(provides, list):
            raise ValueError(
                "metrics.refreshers.local_project_metrics.provides must contain a list"
            )
        for metric_id in missing_refresh:
            source["metrics"][metric_id]["refresh_ref"] = "local_project_metrics"
            if metric_id not in provides:
                provides.append(metric_id)
        text = yaml.safe_dump(source, sort_keys=False, allow_unicode=True, width=100)
        changes.append(
            f"metrics missing acquisition prompts -> local_project_metrics ({len(missing_refresh)} definitions)"
        )
    return text, changes


def _migrate_harness(path: Path) -> tuple[str, list[str]]:
    original = path.read_text(encoding="utf-8")
    source = yaml.safe_load(original)
    if not isinstance(source, dict):
        raise ValueError("farplane/harness.yaml must contain an object")
    changes: list[str] = []
    structural_change = False
    version_changed = str(source.get("framework_template_version")) != HARNESS_TEMPLATE_VERSION
    date_changed = str(source.get("updated_at")) != MIGRATION_DATE
    if version_changed:
        source["framework_template_version"] = HARNESS_TEMPLATE_VERSION
        changes.append(f"harness.framework_template_version -> {HARNESS_TEMPLATE_VERSION}")
    if source.get("updated_at") != MIGRATION_DATE:
        source["updated_at"] = MIGRATION_DATE
        changes.append(f"harness.updated_at -> {MIGRATION_DATE}")
    identity = source.get("identity")
    if isinstance(identity, dict) and "product_bets" in identity:
        identity.pop("product_bets")
        structural_change = True
        changes.append("harness.identity.product_bets removed")
    if "goals" in source:
        source.pop("goals")
        structural_change = True
        changes.append("harness.goals removed")
    products = source.pop("products", None)
    if isinstance(products, dict):
        structural_change = True
        areas = source.setdefault("areas", {})
        planning = source.setdefault("planning", {"skill_refs": []})
        identity = source.setdefault("identity", {})
        if not isinstance(areas, dict) or not isinstance(planning, dict):
            raise ValueError("harness areas and planning must contain objects")
        if not isinstance(identity, dict):
            raise ValueError("harness identity must contain an object")
        problems = identity.setdefault("problems", [])
        if not isinstance(problems, list):
            raise ValueError("harness identity.problems must contain a list")
        planning_refs = planning.setdefault("skill_refs", [])
        if not isinstance(planning_refs, list):
            raise ValueError("harness planning.skill_refs must contain a list")
        for area_id, product in products.items():
            if not isinstance(product, dict):
                continue
            description = str(product.get("description") or "").strip()
            output = str(product.get("output") or "").strip()
            if output:
                description = f"{description}\n\nExpected output: {output}".strip()
            skill_refs = list(product.get("skill_refs") or [])
            areas.setdefault(
                area_id,
                {
                    "description": description,
                    "icp": {
                        "label": "Project operators",
                        "description": str(product.get("description") or "").strip(),
                        "jobs_to_be_done": [output] if output else [],
                        "pain_points": [],
                        "evidence_bar": output or description,
                    },
                    "skill_refs": skill_refs,
                    "metric_refs": list(product.get("metric_refs") or []),
                },
            )
            problems.append(
                {
                    "id": area_id,
                    "statement": str(product.get("description") or "").strip(),
                    "metric_refs": [
                        ref.get("metric_id")
                        for ref in product.get("metric_refs") or []
                        if isinstance(ref, dict) and ref.get("metric_id")
                    ],
                }
            )
            for skill_ref in skill_refs:
                if skill_ref not in planning_refs:
                    planning_refs.append(skill_ref)
        changes.append(f"harness.products -> areas ({len(products)} entries)")
    if not changes:
        return original, []
    if not structural_change:
        text = original
        if version_changed:
            text = re.sub(
                r'(?m)^framework_template_version:\s*["\']?[^\s"\']+["\']?\s*$',
                f'framework_template_version: "{HARNESS_TEMPLATE_VERSION}"',
                text,
            )
        if date_changed:
            text = re.sub(
                r"(?m)^updated_at:\s*\S+\s*$", f"updated_at: {MIGRATION_DATE}", text
            )
        return text, changes
    return yaml.safe_dump(source, sort_keys=False, allow_unicode=True, width=100), changes


def _migrate_bindings(path: Path) -> tuple[str, list[str]]:
    original = path.read_text(encoding="utf-8")
    source = yaml.safe_load(original)
    if not isinstance(source, dict):
        raise ValueError("farplane/bindings.yaml must contain an object")
    changes: list[str] = []
    structural_change = False
    defaults = {
        "status": "active",
        "created_at": MIGRATION_DATE,
        "updated_at": MIGRATION_DATE,
        "framework_template_version": BINDINGS_TEMPLATE_VERSION,
        "owner": "project-pm-automation",
    }
    for key, value in defaults.items():
        if str(source.get(key)) != value and (
            key in {"updated_at", "framework_template_version"} or key not in source
        ):
            source[key] = value
            changes.append(f"bindings.{key} -> {value}")
    if "metric_bindings" in source:
        source.pop("metric_bindings")
        structural_change = True
        changes.append("bindings.metric_bindings removed")
    integrations = source.get("integrations")
    if isinstance(integrations, dict):
        kanban = integrations.get("kanban")
        if isinstance(kanban, dict) and "filesystem_ticket_policy" not in kanban:
            kanban["filesystem_ticket_policy"] = "include"
            structural_change = True
            changes.append("bindings.integrations.kanban.filesystem_ticket_policy -> include")
    feed_scout = source.get("feed_scout")
    if isinstance(feed_scout, dict):
        legacy_scout_brief = feed_scout.get("world_memory")
        current_scout_brief = feed_scout.get("scout_brief")
        if legacy_scout_brief is not None:
            migrated_scout_brief = (
                legacy_scout_brief.replace("world-memory.md", "scout-brief.md")
                if isinstance(legacy_scout_brief, str)
                else legacy_scout_brief
            )
            if current_scout_brief is not None and current_scout_brief != migrated_scout_brief:
                raise ValueError(
                    "bindings.feed_scout contains conflicting world_memory and scout_brief values"
                )
            feed_scout.pop("world_memory")
            feed_scout["scout_brief"] = migrated_scout_brief
            structural_change = True
            changes.append("bindings.feed_scout.world_memory -> scout_brief")
        elif isinstance(current_scout_brief, str) and "world-memory.md" in current_scout_brief:
            feed_scout["scout_brief"] = current_scout_brief.replace(
                "world-memory.md", "scout-brief.md"
            )
            structural_change = True
            changes.append("bindings.feed_scout.scout_brief path -> scout-brief.md")
    if not changes:
        return original, []
    if not structural_change and all(
        key in original
        for key in ("status:", "created_at:", "updated_at:", "framework_template_version:", "owner:")
    ):
        text = original
        text = re.sub(r"(?m)^updated_at:\s*\S+\s*$", f"updated_at: {MIGRATION_DATE}", text)
        text = re.sub(
            r'(?m)^framework_template_version:\s*["\']?[^\s"\']+["\']?\s*$',
            f'framework_template_version: "{BINDINGS_TEMPLATE_VERSION}"',
            text,
        )
        return text, changes
    return yaml.safe_dump(source, sort_keys=False, allow_unicode=True, width=100), changes


def _migrate_scout_brief(project_root: Path) -> tuple[Path | None, str, list[str]]:
    legacy_path = project_root / ".farplane" / "feed-scout" / "world-memory.md"
    current_path = project_root / ".farplane" / "feed-scout" / "scout-brief.md"
    if legacy_path.is_file() and current_path.exists():
        raise ValueError(
            "both retired and current Scout Brief paths exist; reconcile them before migration"
        )
    source_path = legacy_path if legacy_path.is_file() else current_path
    if not source_path.is_file():
        return None, "", []
    original = source_path.read_text(encoding="utf-8")
    migrated = original.replace(
        "kind: feed-scout-world-memory", "kind: feed-scout-brief"
    ).replace("# Feed Scout World Memory", "# Feed Scout Brief")
    changes: list[str] = []
    if source_path == legacy_path:
        changes.append(".farplane/feed-scout/world-memory.md -> scout-brief.md")
    if migrated != original:
        changes.append("Scout Brief kind and title migrated")
    return current_path, migrated, changes


def migrate_project(project_root: Path, *, force: bool) -> dict[str, Any]:
    root = project_root.resolve()
    manifest_path = root / "farplane" / "manifest.json"
    metrics_path = root / "farplane" / "metrics.yaml"
    harness_path = root / "farplane" / "harness.yaml"
    bindings_path = root / "farplane" / "bindings.yaml"
    for path in (manifest_path, metrics_path):
        if not path.is_file():
            raise FileNotFoundError(f"required project file is missing: {path}")

    manifest_text, manifest_changes = _migrate_manifest(manifest_path)
    metrics_text, metrics_changes = _migrate_metrics(metrics_path)
    harness_text, harness_changes = (
        _migrate_harness(harness_path) if harness_path.is_file() else ("", [])
    )
    bindings_text, bindings_changes = (
        _migrate_bindings(bindings_path) if bindings_path.is_file() else ("", [])
    )
    scout_brief_path, scout_brief_text, scout_brief_changes = _migrate_scout_brief(root)
    changes = (
        manifest_changes
        + metrics_changes
        + harness_changes
        + bindings_changes
        + scout_brief_changes
    )
    if force:
        _atomic_write(manifest_path, manifest_text)
        _atomic_write(metrics_path, metrics_text)
        if harness_path.is_file():
            _atomic_write(harness_path, harness_text)
        if bindings_path.is_file():
            _atomic_write(bindings_path, bindings_text)
        if scout_brief_path is not None and scout_brief_changes:
            scout_brief_path.parent.mkdir(parents=True, exist_ok=True)
            legacy_scout_brief_path = root / ".farplane" / "feed-scout" / "world-memory.md"
            source_mode_path = (
                legacy_scout_brief_path
                if legacy_scout_brief_path.is_file()
                else scout_brief_path
            )
            mode = source_mode_path.stat().st_mode
            with tempfile.NamedTemporaryFile(
                "w", encoding="utf-8", dir=scout_brief_path.parent, delete=False
            ) as handle:
                handle.write(scout_brief_text)
                temporary = Path(handle.name)
            os.chmod(temporary, mode)
            os.replace(temporary, scout_brief_path)
            if legacy_scout_brief_path != scout_brief_path:
                legacy_scout_brief_path.unlink(missing_ok=True)
    return {
        "ok": True,
        "project_root": str(root),
        "mode": "applied" if force else "dry_run",
        "framework_version": FRAMEWORK_VERSION,
        "metrics_template_version": METRICS_TEMPLATE_VERSION,
        "changes": changes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Migrate one Farplane project to framework 2.0.16 without replacing human-authored files."
    )
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--force",
        action="store_true",
        help="Apply the migration. Without this flag the command is a dry run.",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        result = migrate_project(args.project_root, force=args.force)
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as error:
        if args.json:
            print(json.dumps({"ok": False, "error": str(error)}, indent=2))
        else:
            print(f"error: {error}")
        return 1
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"{result['mode']}: {result['project_root']}")
        for change in result["changes"]:
            print(f"- {change}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
