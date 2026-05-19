#!/usr/bin/env python3
"""Generate graph data for the Codexter skill registry."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def load_registry(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def skill_ref_name(ref: str) -> str:
    base = ref.split("#", 1)[0]
    return base.split(":", 1)[0]


def build_graph(rows: list[dict[str, Any]]) -> dict[str, Any]:
    skill_names = {row["name"] for row in rows}
    nodes = [
        {
            "id": row["name"],
            "label": row["name"],
            "tier": row.get("tier"),
            "source": row.get("source", "local"),
            "group": row.get("group", ""),
            "methods": row.get("methods", []),
            "has_todos": bool(row.get("has_todos")),
            "path": row.get("path", ""),
            "description": row.get("description", ""),
        }
        for row in rows
    ]

    edges: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str, str]] = set()

    def add_edge(source: str, target_ref: str, edge_type: str, label: str) -> None:
        target = skill_ref_name(target_ref)
        if target not in skill_names or source == target:
            return
        key = (source, target, edge_type, label)
        if key in seen:
            return
        seen.add(key)
        edges.append(
            {
                "source": source,
                "target": target,
                "target_ref": target_ref,
                "type": edge_type,
                "label": label,
            }
        )

    for row in rows:
        source = row["name"]
        for link in row.get("skill_links", []):
            label = link if "#" in link or ":" in link else "markdown-ref"
            add_edge(source, link, "markdown-ref", label)
        for target_ref in row.get("common_chains", {}).get("after", []):
            add_edge(source, target_ref, "common-chain", "common_chains.after")

    nodes.sort(key=lambda node: (int(node.get("tier") or 9), node["label"]))
    edges.sort(key=lambda edge: (edge["source"], edge["target"], edge["type"], edge["label"]))

    counts = {
        "nodes": len(nodes),
        "edges": len(edges),
        "tiers": {},
        "sources": {},
        "edge_types": {},
    }
    for node in nodes:
        tier = str(node.get("tier", "unknown"))
        counts["tiers"][tier] = counts["tiers"].get(tier, 0) + 1
        source = str(node.get("source", "unknown"))
        counts["sources"][source] = counts["sources"].get(source, 0) + 1
    for edge in edges:
        edge_type = edge["type"]
        counts["edge_types"][edge_type] = counts["edge_types"].get(edge_type, 0) + 1

    return {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "counts": counts,
        "nodes": nodes,
        "edges": edges,
    }


def write_graph(graph: dict[str, Any], output_path: Path, js_path: Path | None) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(graph, indent=2, sort_keys=True) + "\n")
    if js_path is not None:
        js_path.write_text(
            "window.SKILL_GRAPH = "
            + json.dumps(graph, indent=2, sort_keys=True)
            + ";\n"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", default="docs/skills/registry.jsonl")
    parser.add_argument("--out", default="docs/skills/graph/skill-graph.json")
    parser.add_argument("--js-out", default="docs/skills/graph/skill-graph.js")
    args = parser.parse_args()

    graph = build_graph(load_registry(Path(args.registry)))
    write_graph(graph, Path(args.out), Path(args.js_out) if args.js_out else None)
    print(
        "wrote "
        f"{args.out} ({graph['counts']['nodes']} nodes, "
        f"{graph['counts']['edges']} edges)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
