#!/usr/bin/env python3
"""Render and validate the generated Farplane product index."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


PRODUCT_ROOT = Path("farplane/products")
PRODUCTS_JSON = Path("farplane/products.json")
PRODUCT_FILE = "product.md"
PROJECT_TEAM = {
    "Archetype": "autonomous_ai_harness_lab",
    "Core product": "evidence-backed harness improvements",
    "Secondary product": "trust distribution from proven work",
}
REQUIRED_PRODUCT_FIELDS = {
    "kind",
    "id",
    "label",
    "lane",
    "lane_purpose",
    "default_weight",
    "audience",
    "output",
    "reward",
    "owner_skill",
    "skill_ref",
    "progress_ref",
    "kpis",
}


class ProductIndexError(Exception):
    pass


def split_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ProductIndexError(f"{path}: missing YAML front matter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ProductIndexError(f"{path}: unterminated YAML front matter")
    try:
        loaded = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as exc:
        raise ProductIndexError(f"{path}: invalid YAML front matter: {exc}") from exc
    if not isinstance(loaded, dict):
        raise ProductIndexError(f"{path}: front matter must be an object")
    return loaded, parts[2]


def read_yaml(path: Path) -> dict[str, Any]:
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except FileNotFoundError:
        return {}
    if not isinstance(loaded, dict):
        return {}
    return loaded


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def string_list(value: Any) -> list[str]:
    return [str(item).strip() for item in as_list(value) if str(item).strip()]


def product_kpis(product: dict[str, Any]) -> list[str]:
    kpis = product.get("kpis")
    if not isinstance(kpis, dict):
        return []
    values: list[str] = []
    for key in ("primary", "supporting", "guardrail"):
        values.extend(string_list(kpis.get(key)))
    return sorted(set(values))


def product_goals(product: dict[str, Any]) -> list[dict[str, Any]]:
    goals = product.get("goals")
    if not isinstance(goals, list):
        return []
    return [goal for goal in goals if isinstance(goal, dict)]


def product_workflows(product: dict[str, Any]) -> list[dict[str, Any]]:
    workflows = product.get("artifact_workflows")
    if not isinstance(workflows, list):
        return []
    return [workflow for workflow in workflows if isinstance(workflow, dict)]


def goal_axes(goals_payload: dict[str, Any]) -> list[dict[str, Any]]:
    goals = goals_payload.get("goals")
    if not isinstance(goals, dict):
        return []
    rows: list[dict[str, Any]] = []
    for axis_id, axis_payload in goals.items():
        if not isinstance(axis_payload, dict):
            continue
        question = str(axis_payload.get("question") or "").strip()
        for smart_goal in axis_payload.get("smart_goals") or []:
            if not isinstance(smart_goal, dict):
                continue
            goal_id = str(smart_goal.get("id") or "").strip()
            if not goal_id:
                continue
            kpi_ids = [
                str(kpi.get("id") or "").strip()
                for kpi in smart_goal.get("kpis") or []
                if isinstance(kpi, dict) and str(kpi.get("id") or "").strip()
            ]
            rows.append(
                {
                    "axis_id": str(axis_id),
                    "question": question,
                    "goal_id": goal_id,
                    "scope": str(smart_goal.get("scope") or "").strip(),
                    "target": str(smart_goal.get("target") or "").strip(),
                    "product_refs": string_list(smart_goal.get("product_refs")),
                    "kpis": kpi_ids,
                    "interpretation": str(smart_goal.get("interpretation") or "").strip(),
                }
            )
    return rows


def product_goal_matches(product: dict[str, Any], goal_kpis: list[str]) -> list[dict[str, Any]]:
    goal_kpi_set = set(goal_kpis)
    matches: list[dict[str, Any]] = []
    for goal in product_goals(product):
        product_goal_kpis = string_list(goal.get("kpis"))
        shared_kpis = sorted(goal_kpi_set & set(product_goal_kpis))
        if shared_kpis:
            next_goal = dict(goal)
            next_goal["_shared_kpis"] = shared_kpis
            matches.append(next_goal)
    return matches


def goal_product_matrix(products: list[dict[str, Any]], goals_payload: dict[str, Any]) -> list[dict[str, Any]]:
    product_by_id = {str(product.get("id") or "").strip(): product for product in products}
    rows: list[dict[str, Any]] = []
    for smart_goal in goal_axes(goals_payload):
        for product_ref in smart_goal["product_refs"]:
            product = product_by_id.get(product_ref)
            if product is None:
                rows.append(
                    {
                        **smart_goal,
                        "product_id": product_ref,
                        "product_label": "",
                        "product_goal_ids": [],
                        "shared_kpis": [],
                        "status": "missing_product",
                    }
                )
                continue
            matches = product_goal_matches(product, smart_goal["kpis"])
            shared_kpis = sorted(set(smart_goal["kpis"]) & set(product_kpis(product)))
            shared_product_goal_kpis = sorted({kpi for match in matches for kpi in match.get("_shared_kpis", [])})
            rows.append(
                {
                    **smart_goal,
                    "product_id": product_ref,
                    "product_label": product.get("label"),
                    "product_goal_ids": [str(match.get("id") or "").strip() for match in matches if match.get("id")],
                    "shared_kpis": shared_kpis,
                    "shared_product_goal_kpis": shared_product_goal_kpis,
                    "status": "aligned" if shared_kpis else "no_shared_product_kpi",
                }
            )
    return rows


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def load_products(root: Path) -> tuple[list[dict[str, Any]], list[str]]:
    issues: list[str] = []
    product_dir = root / PRODUCT_ROOT
    products: list[dict[str, Any]] = []
    if not product_dir.exists():
        return products, [f"{PRODUCT_ROOT.as_posix()} is missing"]
    for path in sorted(product_dir.glob(f"*/{PRODUCT_FILE}")):
        try:
            frontmatter, _body = split_frontmatter(path)
        except ProductIndexError as exc:
            issues.append(str(exc))
            continue
        frontmatter["_path"] = rel(path, root)
        frontmatter["_dir_id"] = path.parent.name
        products.append(frontmatter)
    if not products:
        issues.append(f"{PRODUCT_ROOT.as_posix()}/*/{PRODUCT_FILE} did not match any product files")
    return products, issues


def validate_products(root: Path, products: list[dict[str, Any]]) -> list[str]:
    issues: list[str] = []
    bindings = read_yaml(root / "farplane" / "bindings.yaml")
    metrics = bindings.get("metrics") if isinstance(bindings.get("metrics"), dict) else {}
    allowed_gates = set(string_list(bindings.get("human_gates")))
    seen_ids: set[str] = set()
    for product in products:
        path = product.get("_path", "<unknown>")
        missing = sorted(field for field in REQUIRED_PRODUCT_FIELDS if field not in product)
        if missing:
            issues.append(f"{path}: missing required frontmatter fields: {', '.join(missing)}")
        product_id = str(product.get("id") or "").strip()
        if not product_id:
            issues.append(f"{path}: id is required")
            continue
        if product_id in seen_ids:
            issues.append(f"{path}: duplicate product id {product_id}")
        seen_ids.add(product_id)
        if product.get("kind") != "product-loop":
            issues.append(f"{path}: kind must be product-loop")
        if product_id != product.get("_dir_id"):
            issues.append(f"{path}: id must match directory name {product.get('_dir_id')}")
        expected_refs = {
            "skill_ref": f"farplane/products/{product_id}/skill.md",
            "progress_ref": f"farplane/products/{product_id}/progress.md",
        }
        for field, expected in expected_refs.items():
            actual = str(product.get(field) or "").strip()
            if actual != expected:
                issues.append(f"{path}: {field} must be {expected}")
            elif field == "skill_ref" and not (root / actual).exists():
                issues.append(f"{path}: {field} target is missing: {actual}")
        kpis = product.get("kpis")
        if not isinstance(kpis, dict):
            issues.append(f"{path}: kpis must be a mapping")
        else:
            for key in ("primary", "supporting", "guardrail"):
                for kpi in string_list(kpis.get(key)):
                    if kpi not in metrics:
                        issues.append(f"{path}: kpis.{key} references missing bindings metric: {kpi}")
        for goal in product_goals(product):
            for kpi in string_list(goal.get("kpis")):
                if kpi not in metrics:
                    issues.append(f"{path}: goals.{goal.get('id', '?')}.kpis references missing bindings metric: {kpi}")
        if allowed_gates:
            unknown_gates = sorted(set(string_list(product.get("human_gates"))) - allowed_gates)
            if unknown_gates:
                issues.append(f"{path}: human_gates not declared in bindings.yaml: {', '.join(unknown_gates)}")
        if not product_workflows(product):
            issues.append(f"{path}: artifact_workflows must contain at least one workflow")
    return issues


def sorted_products(products: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(products, key=lambda product: (int(product.get("sort_order") or 999), str(product.get("id") or "")))


def generated_updated_at(products: list[dict[str, Any]]) -> str:
    updated_at = max((str(product.get("updated_at") or "") for product in products), default="").strip()
    return updated_at or "2026-07-08"


def kpi_group(product: dict[str, Any], key: str) -> list[str]:
    kpis = product.get("kpis")
    if not isinstance(kpis, dict):
        return []
    return string_list(kpis.get(key))


def product_record(product: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": product.get("id"),
        "label": product.get("label"),
        "status": product.get("status"),
        "sort_order": product.get("sort_order"),
        "lane": product.get("lane"),
        "lane_purpose": product.get("lane_purpose"),
        "default_weight": product.get("default_weight"),
        "audience": product.get("audience"),
        "output": product.get("output"),
        "reward": product.get("reward"),
        "owner_skill": product.get("owner_skill"),
        "refs": {
            "product": product.get("_path"),
            "skill": product.get("skill_ref"),
            "progress": product.get("progress_ref"),
        },
        "worker_policy": {
            "worker_budget_min": product.get("worker_budget_min"),
            "max_tickets_in_review": product.get("max_tickets_in_review"),
            "review_channel": product.get("review_channel"),
            "human_gates": string_list(product.get("human_gates")),
        },
        "kpis": {
            "primary": kpi_group(product, "primary"),
            "supporting": kpi_group(product, "supporting"),
            "guardrail": kpi_group(product, "guardrail"),
            "all": product_kpis(product),
        },
        "goals": product_goals(product),
        "artifact_workflows": product_workflows(product),
        "supporting_skills": string_list(product.get("supporting_skills")),
        "notes": product.get("notes"),
    }


def render_json_payload(products: list[dict[str, Any]], goals_payload: dict[str, Any] | None = None) -> str:
    ordered = sorted_products(products)
    goals_payload = goals_payload or {}
    lanes: dict[str, dict[str, Any]] = {}
    workflows: list[dict[str, Any]] = []
    for product in ordered:
        product_id = str(product.get("id") or "").strip()
        lane = str(product.get("lane") or "").strip()
        if lane and lane not in lanes:
            lanes[lane] = {
                "id": lane,
                "default_weight": product.get("default_weight"),
                "purpose": product.get("lane_purpose"),
            }
        for workflow in product_workflows(product):
            workflow_record = dict(workflow)
            workflow_record.setdefault("lane", lane)
            workflow_record["product_id"] = product_id
            workflows.append(workflow_record)
    payload = {
        "schema_version": 1,
        "kind": "project-products-index",
        "project": "Farplane",
        "updated_at": generated_updated_at(ordered),
        "generated_by": "bin/validators/render_product_index.py",
        "source_of_truth": [
            "farplane/harness.md",
            "farplane/goals.yaml",
            "farplane/bindings.yaml",
            "farplane/products/*/product.md",
        ],
        "indexes": {
            "json": PRODUCTS_JSON.as_posix(),
        },
        "products": [product_record(product) for product in ordered],
        "lanes": list(lanes.values()),
        "artifact_workflows": workflows,
        "goal_product_matrix": goal_product_matrix(ordered, goals_payload),
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def write_or_check_file(root: Path, path: Path, rendered: str, *, write: bool, check: bool) -> list[str]:
    target = root / path
    if write:
        target.write_text(rendered, encoding="utf-8")
        return []
    if check:
        current = target.read_text(encoding="utf-8") if target.exists() else ""
        if current != rendered:
            return [f"{path.as_posix()} is stale; run python3 bin/validators/render_product_index.py --project-root . --write"]
    return []


def write_or_check(root: Path, rendered_json: str, *, write: bool, check: bool) -> list[str]:
    return write_or_check_file(root, PRODUCTS_JSON, rendered_json, write=write, check=check)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--write", action="store_true", help="Render farplane/products.json from product.md files.")
    parser.add_argument("--check", action="store_true", help="Fail when generated product registry is stale.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    products, issues = load_products(root)
    issues.extend(validate_products(root, products))
    goals_payload = read_yaml(root / "farplane" / "goals.yaml")
    rendered_json = render_json_payload(products, goals_payload) if not issues else ""
    if not issues:
        issues.extend(write_or_check(root, rendered_json, write=args.write, check=args.check))

    payload = {
        "ok": not issues,
        "product_count": len(products),
        "products": [product.get("id") for product in sorted_products(products)],
        "issues": issues,
        "indexes": [PRODUCTS_JSON.as_posix()],
    }
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif issues:
        for issue in issues:
            print(issue, file=sys.stderr)
    else:
        action = "wrote" if args.write else "validated"
        if args.check:
            action = "checked"
        print(f"{action} {PRODUCTS_JSON.as_posix()} from {len(products)} product files")
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())
