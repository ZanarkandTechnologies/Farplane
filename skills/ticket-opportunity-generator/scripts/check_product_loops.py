#!/usr/bin/env python3
"""Validate Farplane product-loop contracts."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def frontmatter_value(text: str, key: str) -> str | None:
    match = re.search(rf"^{re.escape(key)}:\s*(.+?)\s*$", text, re.MULTILINE)
    if not match:
        return None
    return match.group(1).strip().strip('"').strip("'")


def read_json(path: Path) -> dict:
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    return loaded if isinstance(loaded, dict) else {}


def relative_to_root(path: str) -> str:
    return path.strip().strip("`")


def is_git_ignored(root: Path, rel_path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "-q", rel_path],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode == 0


def validate(root: Path) -> list[str]:
    issues: list[str] = []
    products_payload = read_json(root / "farplane/products.json")
    products_list = products_payload.get("products") if isinstance(products_payload.get("products"), list) else []
    lanes_list = products_payload.get("lanes") if isinstance(products_payload.get("lanes"), list) else []
    products = {
        str(product.get("id") or ""): product
        for product in products_list
        if isinstance(product, dict) and str(product.get("id") or "")
    }
    lanes = {
        str(lane.get("id") or "")
        for lane in lanes_list
        if isinstance(lane, dict) and str(lane.get("id") or "")
    }
    if not products:
        issues.append("farplane/products.json must contain products[] rows")
    for product, row in products.items():
        refs = row.get("refs") if isinstance(row.get("refs"), dict) else {}
        product_rel = relative_to_root(refs.get("product", ""))
        skill_rel = relative_to_root(refs.get("skill", ""))
        progress_rel = relative_to_root(refs.get("progress", ""))
        expected_product = f"farplane/products/{product}/product.md"
        expected_skill = f"farplane/products/{product}/skill.md"
        expected_progress = f"farplane/products/{product}/progress.md"
        if product_rel and product_rel != expected_product:
            issues.append(f"{product}: Product config must be {expected_product}")
        if skill_rel != expected_skill:
            issues.append(f"{product}: Skill must be {expected_skill}")
        if progress_rel != expected_progress:
            issues.append(f"{product}: Runtime progress must be {expected_progress}")
        base = root / "farplane/products" / product
        product_config = root / expected_product
        skill = root / skill_rel
        if not product_config.exists():
            issues.append(f"missing product config: {product_config}")
        if not skill.exists():
            issues.append(f"missing product skill: {skill}")
        product_text = read(product_config)
        skill_text = read(skill)
        if product_text:
            if frontmatter_value(product_text, "kind") != "product-loop":
                issues.append(f"{product_config}: kind must be product-loop")
            if frontmatter_value(product_text, "id") != product:
                issues.append(f"{product_config}: id must be {product}")
        lane = frontmatter_value(product_text, "lane")
        if lane not in lanes:
            issues.append(f"{product_config}: lane must match a Work Lanes row")
        owner_skill = frontmatter_value(product_text, "owner_skill")
        if not owner_skill:
            issues.append(f"{product_config}: missing owner_skill")
        elif frontmatter_value(skill_text, "name") != owner_skill:
            issues.append(f"{product_config}: owner_skill must match {skill} frontmatter name")
        for required in (
            "Current Strategy",
            "Loop Contract",
            "worker_budget:",
            "max_tickets_in_review:",
            "runtime_progress:",
            "Product Loop",
            "Progress Entry Shape",
        ):
            if required not in product_text:
                issues.append(f"{product_config}: missing {required}")
        if "progress.template.md" in product_text:
            issues.append(f"{product_config}: must not point to progress.template.md")
        if not is_git_ignored(root, progress_rel):
            issues.append(f"{progress_rel} must be git-ignored")
        template = base / "progress.template.md"
        if template.exists():
            issues.append(f"unexpected product progress template: {template}")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    issues = validate(root)
    if issues:
        for issue in issues:
            print(f"ERROR: {issue}", file=sys.stderr)
        return 1
    print("product loop contracts OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
