#!/usr/bin/env python3
"""Build a minimal CRM JSONL index from customer research report frontmatter."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_frontmatter(markdown: str) -> dict[str, object]:
    match = FRONTMATTER_RE.match(markdown)
    if not match:
        return {}

    data: dict[str, object] = {}
    current_list_key: str | None = None
    for raw_line in match.group(1).splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        if line.startswith("  - ") and current_list_key:
            value = line[4:].strip().strip('"')
            data.setdefault(current_list_key, [])
            if isinstance(data[current_list_key], list):
                data[current_list_key].append(value)
            continue
        if ":" not in line:
            current_list_key = None
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value == "":
            data[key] = []
            current_list_key = key
        else:
            data[key] = value.strip('"')
            current_list_key = None
    return data


def build_index(crm_root: Path) -> list[dict[str, object]]:
    reports_dir = crm_root / "reports"
    rows: list[dict[str, object]] = []
    for report_path in sorted(reports_dir.glob("*.md")):
        frontmatter = parse_frontmatter(report_path.read_text(encoding="utf-8"))
        if not frontmatter:
            continue
        rows.append(
            {
                "skill": frontmatter.get("skill", ""),
                "name": frontmatter.get("name", ""),
                "links": frontmatter.get("links", []),
                "industry": frontmatter.get("industry", ""),
                "relevance": frontmatter.get("relevance", ""),
                "created_at": frontmatter.get("created_at", ""),
                "report_path": str(report_path),
            }
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build .farplane/crm/index.jsonl from report frontmatter."
    )
    parser.add_argument(
        "crm_root",
        help="Path to a CRM root containing reports/, such as .farplane/crm",
    )
    args = parser.parse_args()

    crm_root = Path(args.crm_root).expanduser().resolve()
    reports_dir = crm_root / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    rows = build_index(crm_root)
    index_path = crm_root / "index.jsonl"
    index_path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )
    print(f"Wrote {len(rows)} rows to {index_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
