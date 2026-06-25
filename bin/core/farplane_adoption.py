#!/usr/bin/env python3
"""Resolve Farplane project adoption pins across local project manifests."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from bin.validators.template_usage import TemplateUsageError, normalize_template_uses


DEFAULT_FARPLANE_HOME = Path.home() / ".farplane"
DEFAULT_STATE_PATHS = (
    DEFAULT_FARPLANE_HOME / "state" / "projects.json",
    DEFAULT_FARPLANE_HOME / "projects.json",
    DEFAULT_FARPLANE_HOME / "farplane-cli.json",
)


class AdoptionError(ValueError):
    """Raised when adoption inputs cannot be resolved safely."""


@dataclass(frozen=True)
class RegistryTemplate:
    template_id: str
    version: str
    path: str
    feature_refs: tuple[str, ...]


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise AdoptionError(f"missing_json:{path}") from exc
    except json.JSONDecodeError as exc:
        raise AdoptionError(f"invalid_json:{path}:{exc}") from exc


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        return rows
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise AdoptionError(f"invalid_jsonl:{path}:{line_no}:{exc}") from exc
        if isinstance(row, dict):
            rows.append(row)
    return rows


def normalize_root(path: str | Path, base: Path | None = None) -> Path:
    candidate = Path(path).expanduser()
    if not candidate.is_absolute() and base is not None:
        candidate = base / candidate
    return candidate.resolve()


def candidate_project_root(value: Any, base: Path | None = None) -> Path | None:
    if isinstance(value, str):
        return normalize_root(value, base)
    if not isinstance(value, dict):
        return None
    for key in ("root", "path", "projectRoot", "project_root", "directory", "projectDirectory"):
        raw = value.get(key)
        if isinstance(raw, str) and raw.strip():
            return normalize_root(raw, base)
    return None


def roots_from_payload(payload: Any, base: Path | None = None) -> list[Path]:
    if isinstance(payload, list):
        return [root for item in payload if (root := candidate_project_root(item, base)) is not None]
    if not isinstance(payload, dict):
        return []
    for key in ("projectRoots", "project_roots", "roots", "projects", "workspaces"):
        value = payload.get(key)
        roots = roots_from_payload(value, base)
        if roots:
            return roots
    return []


def roots_from_file(path: Path) -> list[Path]:
    payload = read_json(path)
    return roots_from_payload(payload, path.parent)


def discover_state_roots(paths: tuple[Path, ...] = DEFAULT_STATE_PATHS) -> tuple[list[Path], list[str]]:
    for path in paths:
        if not path.exists():
            continue
        roots = roots_from_file(path)
        if roots:
            return roots, [str(path)]
    return [], []


def unique_paths(paths: list[Path]) -> list[Path]:
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in paths:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        unique.append(resolved)
    return unique


def load_feature_registry(path: Path) -> dict[str, dict[str, Any]]:
    rows = read_jsonl(path)
    return {str(row["id"]): row for row in rows if isinstance(row.get("id"), str)}


def load_template_registry(path: Path) -> dict[str, RegistryTemplate]:
    templates: dict[str, RegistryTemplate] = {}
    for row in read_jsonl(path):
        template_id = row.get("template_id")
        if not isinstance(template_id, str):
            continue
        feature_refs = tuple(
            str(item)
            for item in row.get("feature_refs", [])
            if isinstance(item, str) and item.strip()
        )
        templates[template_id] = RegistryTemplate(
            template_id=template_id,
            version=str(row.get("template_version") or ""),
            path=str(row.get("path") or ""),
            feature_refs=feature_refs,
        )
    return templates


def compare_version(pinned: str, expected: str) -> str:
    if not pinned:
        return "missing"
    if not expected:
        return "unknown"
    if pinned == expected:
        return "ok"
    return "drift"


def local_skill_names(project_root: Path) -> list[str]:
    skills_dir = project_root / "skills"
    if not skills_dir.is_dir():
        return []
    names: list[str] = []
    for child in sorted(skills_dir.iterdir()):
        if child.is_dir() and (child / "SKILL.md").is_file():
            names.append(child.name)
    return names


def explicit_feature_pins(manifest: dict[str, Any]) -> dict[str, str]:
    raw = manifest.get("feature_pins") or manifest.get("featurePins") or {}
    if not isinstance(raw, dict):
        return {}
    pins: dict[str, str] = {}
    for key, value in raw.items():
        if isinstance(key, str) and key.strip():
            pins[key] = str(value)
    return pins


def template_uses(manifest: dict[str, Any]) -> dict[str, str]:
    try:
        return normalize_template_uses(manifest, "<manifest>", include_legacy=False)
    except TemplateUsageError as exc:
        raise AdoptionError(str(exc)) from exc


def resolve_project(
    project_root: Path,
    *,
    global_manifest: dict[str, Any],
    features: dict[str, dict[str, Any]],
    templates: dict[str, RegistryTemplate],
) -> dict[str, Any]:
    manifest_path = project_root / "farplane" / "manifest.json"
    issues: list[str] = []
    if not manifest_path.exists():
        return {
            "root": str(project_root),
            "manifestPath": str(manifest_path),
            "manifestExists": False,
            "ok": False,
            "issues": ["manifest_missing"],
            "localSkills": [],
            "templateUses": {},
            "featurePins": {},
            "impliedFeaturePins": {},
            "drift": [],
        }
    manifest_value = read_json(manifest_path)
    if not isinstance(manifest_value, dict):
        raise AdoptionError(f"invalid_manifest_shape:{manifest_path}:expected_object")

    project_templates = template_uses(manifest_value)
    global_templates = template_uses(global_manifest)
    explicit_features = explicit_feature_pins(manifest_value)
    implied_features: dict[str, list[str]] = {}
    drift: list[dict[str, str]] = []

    spec_status = compare_version(
        str(manifest_value.get("spec_version") or ""),
        str(global_manifest.get("spec_version") or ""),
    )
    if spec_status != "ok":
        drift.append(
            {
                "type": "spec_version",
                "status": spec_status,
                "pinned": str(manifest_value.get("spec_version") or ""),
                "expected": str(global_manifest.get("spec_version") or ""),
            }
        )

    for template_id, expected_version in sorted(global_templates.items()):
        pinned = project_templates.get(template_id, "")
        status = compare_version(pinned, expected_version)
        if status != "ok":
            drift.append(
                {
                    "type": "template",
                    "template_id": template_id,
                    "status": status,
                    "pinned": pinned,
                    "expected": expected_version,
                }
            )

    for template_id, pinned in sorted(project_templates.items()):
        template = templates.get(template_id)
        if template is None:
            issues.append(f"unknown_template:{template_id}")
            drift.append({"type": "template", "template_id": template_id, "status": "unknown", "pinned": pinned, "expected": ""})
            continue
        for feature_id in template.feature_refs:
            implied_features.setdefault(feature_id, []).append(template_id)

    for feature_id in explicit_features:
        if feature_id not in features:
            issues.append(f"unknown_feature:{feature_id}")
            drift.append({"type": "feature", "feature_id": feature_id, "status": "unknown"})

    skills = local_skill_names(project_root)
    return {
        "root": str(project_root),
        "manifestPath": str(manifest_path),
        "manifestExists": True,
        "ok": not issues and not drift,
        "projectId": str(manifest_value.get("project_id") or project_root.name),
        "schema": manifest_value.get("schema"),
        "specVersion": str(manifest_value.get("spec_version") or ""),
        "expectedSpecVersion": str(global_manifest.get("spec_version") or ""),
        "templateUses": project_templates,
        "featurePins": explicit_features,
        "impliedFeaturePins": {key: sorted(value) for key, value in sorted(implied_features.items())},
        "localSkills": skills,
        "usesLocalSkills": bool(skills),
        "skillSourcePolicy": "local-if-present" if skills else "global",
        "issues": issues,
        "drift": drift,
    }


def adoption_graph(projects: list[dict[str, Any]], features: dict[str, dict[str, Any]]) -> dict[str, Any]:
    graph: dict[str, Any] = {}
    for feature_id, row in sorted(features.items()):
        explicit: list[str] = []
        implied: list[str] = []
        for project in projects:
            project_id = str(project.get("projectId") or project.get("root"))
            if feature_id in project.get("featurePins", {}):
                explicit.append(project_id)
            if feature_id in project.get("impliedFeaturePins", {}):
                implied.append(project_id)
        total = sorted(set(explicit) | set(implied))
        if not total:
            continue
        graph[feature_id] = {
            "id": feature_id,
            "name": row.get("name", feature_id),
            "status": row.get("status", ""),
            "explicitProjects": sorted(explicit),
            "impliedProjects": sorted(implied),
            "projectCount": len(total),
        }
    return graph


def resolve_adoption_stats(
    *,
    standard_root: Path,
    project_roots: list[Path],
    feature_registry: Path | None = None,
    template_registry: Path | None = None,
) -> dict[str, Any]:
    standard_root = standard_root.resolve()
    global_manifest_path = standard_root / "farplane" / "manifest.json"
    global_manifest = read_json(global_manifest_path)
    if not isinstance(global_manifest, dict):
        raise AdoptionError(f"invalid_manifest_shape:{global_manifest_path}:expected_object")
    feature_path = feature_registry or standard_root / "docs" / "features" / "registry.jsonl"
    template_path = template_registry or standard_root / "docs" / "templates" / "registry.jsonl"
    features = load_feature_registry(feature_path)
    templates = load_template_registry(template_path)
    roots = unique_paths(project_roots)
    projects = [
        resolve_project(root, global_manifest=global_manifest, features=features, templates=templates)
        for root in roots
    ]
    drift_count = sum(len(project.get("drift", [])) for project in projects)
    local_skill_projects = [project for project in projects if project.get("usesLocalSkills")]
    return {
        "schema": "farplane_adoption_stats",
        "schemaVersion": "0.1.0",
        "standardRoot": str(standard_root),
        "globalManifestPath": str(global_manifest_path),
        "globalSpecVersion": str(global_manifest.get("spec_version") or ""),
        "globalTemplateUses": template_uses(global_manifest),
        "featureRegistryPath": str(feature_path),
        "templateRegistryPath": str(template_path),
        "counts": {
            "projects": len(projects),
            "manifests": sum(1 for project in projects if project.get("manifestExists")),
            "projectsWithLocalSkills": len(local_skill_projects),
            "driftItems": drift_count,
        },
        "projects": projects,
        "features": adoption_graph(projects, features),
    }


def resolve_project_roots(args: argparse.Namespace) -> tuple[list[Path], list[str]]:
    roots: list[Path] = []
    sources: list[str] = []
    for raw in args.project_root or []:
        roots.append(normalize_root(raw))
        sources.append("arg")
    if args.roots_file:
        roots.extend(roots_from_file(Path(args.roots_file).expanduser()))
        sources.append(str(Path(args.roots_file).expanduser()))
    if not roots and not args.no_state:
        state_roots, state_sources = discover_state_roots()
        roots.extend(state_roots)
        sources.extend(state_sources)
    if not roots and args.include_standard:
        roots.append(Path(args.standard_root).expanduser().resolve())
        sources.append("standard_root")
    return unique_paths(roots), sources


def print_summary(payload: dict[str, Any]) -> None:
    counts = payload["counts"]
    print(
        "farplane adoption: "
        f"{counts['manifests']}/{counts['projects']} manifests, "
        f"{counts['projectsWithLocalSkills']} with local skills, "
        f"{counts['driftItems']} drift items"
    )
    for project in payload["projects"]:
        marker = "ok" if project.get("ok") else "drift"
        local = "local-skills" if project.get("usesLocalSkills") else "global-skills"
        print(f"- {marker}: {project.get('projectId', project['root'])} ({local})")
        for drift in project.get("drift", [])[:5]:
            label = drift.get("template_id") or drift.get("feature_id") or drift.get("type")
            print(f"  - {drift.get('type')}:{label} {drift.get('status')}")
        for issue in project.get("issues", [])[:5]:
            print(f"  - issue:{issue}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command")
    scan = sub.add_parser("scan", help="Resolve adoption stats for project manifests.")
    scan.add_argument("--standard-root", default=str(Path(__file__).resolve().parents[1]))
    scan.add_argument("--project-root", action="append", help="Project root to scan. May be repeated.")
    scan.add_argument("--roots-file", help="JSON file containing project roots.")
    scan.add_argument("--no-state", action="store_true", help="Do not read ~/.farplane global state project roots.")
    scan.add_argument("--include-standard", action="store_true", help="Scan the standard root when no project roots are found.")
    scan.add_argument("--feature-registry", help="Feature registry JSONL path.")
    scan.add_argument("--template-registry", help="Template registry JSONL path.")
    scan.add_argument("--json", action="store_true")
    scan.set_defaults(func=run_scan)
    return parser


def run_scan(args: argparse.Namespace) -> int:
    roots, sources = resolve_project_roots(args)
    if not roots:
        raise AdoptionError("no_project_roots: pass --project-root, --roots-file, or create ~/.farplane/state/projects.json")
    payload = resolve_adoption_stats(
        standard_root=Path(args.standard_root).expanduser().resolve(),
        project_roots=roots,
        feature_registry=Path(args.feature_registry).expanduser().resolve() if args.feature_registry else None,
        template_registry=Path(args.template_registry).expanduser().resolve() if args.template_registry else None,
    )
    payload["rootSources"] = sources
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print_summary(payload)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 0
    try:
        return int(args.func(args))
    except AdoptionError as exc:
        print(f"farplane adoption: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
