#!/usr/bin/env python3
"""Generate graph and document data for the Farplane skill registry."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from graph_ir import GraphBundle, GraphEdge, GraphNode, edge_counts, utc_timestamp, write_js, write_json
from graph_projection_config import get_projection_config


def load_registry(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def skill_ref_name(ref: str) -> str:
    base = ref.split("#", 1)[0]
    return base.split(":", 1)[0]


def build_graph(rows: list[dict[str, Any]]) -> dict[str, Any]:
    skill_names = {row["name"] for row in rows}
    nodes = [
        GraphNode(
            id=row["name"],
            label=row["name"],
            attributes={
                "tier": row.get("tier"),
                "source": row.get("source", "local"),
                "group": row.get("group", ""),
                "methods": row.get("methods", []),
                "has_checklist": bool(row.get("has_checklist")),
                "eval": row.get("eval", ""),
                "qa_checklist": row.get("qa_checklist", ""),
                "skill_ui": row.get("skill_ui", ""),
                "path": row.get("path", ""),
                "description": row.get("description", ""),
            },
        ).as_dict()
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
            GraphEdge(
                source=source,
                target=target,
                type=edge_type,
                label=label,
                metadata={"target_ref": target_ref},
            ).as_dict()
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
        "edge_types": edge_counts(edges),
    }
    for node in nodes:
        tier = str(node.get("tier", "unknown"))
        counts["tiers"][tier] = counts["tiers"].get(tier, 0) + 1
        source = str(node.get("source", "unknown"))
        counts["sources"][source] = counts["sources"].get(source, 0) + 1

    return GraphBundle(nodes=nodes, edges=edges, generated_at=utc_timestamp(), counts=counts).as_dict()


def parse_frontmatter(markdown: str) -> tuple[dict[str, Any], str, str]:
    if not markdown.startswith("---\n"):
        return {}, "", markdown
    end = markdown.find("\n---\n", 4)
    if end == -1:
        return {}, "", markdown
    raw = markdown[4:end]
    body = markdown[end + 5 :].lstrip("\n")
    return parse_simple_yaml(raw), raw, body


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value in {"true", "false"}:
        return value == "true"
    if value.startswith("[") and value.endswith("]"):
        try:
            return json.loads(value.replace("'", '"'))
        except json.JSONDecodeError:
            inner = value[1:-1].strip()
            return [part.strip().strip("\"'") for part in inner.split(",") if part.strip()]
    if value.startswith(("\"", "'")) and value.endswith(("\"", "'")):
        return value[1:-1]
    try:
        return int(value)
    except ValueError:
        return value


def parse_simple_yaml(raw: str) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    current_map: str | None = None
    current_list: str | None = None

    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  ") and current_map:
            key, _, value = line.strip().partition(":")
            if key and value:
                if not isinstance(parsed.get(current_map), dict):
                    parsed[current_map] = {}
                parsed.setdefault(current_map, {})[key] = parse_scalar(value)
            continue
        if line.startswith("  - ") and current_list:
            if not isinstance(parsed.get(current_list), list):
                parsed[current_list] = []
            parsed.setdefault(current_list, []).append(parse_scalar(line.strip()[2:]))
            continue

        current_map = None
        current_list = None
        key, _, value = line.partition(":")
        key = key.strip()
        if not key:
            continue
        if value.strip():
            parsed[key] = parse_scalar(value)
        else:
            current_map = key
            current_list = key
            parsed[key] = {}
    return parsed


def build_docs(rows: list[dict[str, Any]]) -> dict[str, Any]:
    docs: dict[str, Any] = {
        "schema_version": "1.0.0",
        "generated_at": utc_timestamp(),
        "skills": {},
    }
    for row in rows:
        path = Path(row.get("path", ""))
        if not path.exists():
            continue
        markdown = path.read_text()
        frontmatter, frontmatter_raw, body = parse_frontmatter(markdown)
        docs["skills"][row["name"]] = {
            "name": row["name"],
            "path": str(path),
            "frontmatter": frontmatter,
            "frontmatter_raw": frontmatter_raw,
            "body": body,
        }
    docs["counts"] = {"skills": len(docs["skills"])}
    return docs


def write_graph(graph: dict[str, Any], output_path: Path, js_path: Path | None) -> None:
    write_json(output_path, graph)
    if js_path is not None:
        write_js(js_path, "SKILL_GRAPH", graph)


def write_docs(docs: dict[str, Any], output_path: Path, js_path: Path | None) -> None:
    write_json(output_path, docs)
    if js_path is not None:
        write_js(js_path, "SKILL_DOCS", docs)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", default="docs/skills/registry.jsonl")
    parser.add_argument("--out", default="skills/skill-maintenance/graph/skill-graph.json")
    parser.add_argument("--js-out", default="skills/skill-maintenance/graph/skill-graph.js")
    parser.add_argument("--docs-out", default="skills/skill-maintenance/graph/skill-docs.json")
    parser.add_argument("--docs-js-out", default="skills/skill-maintenance/graph/skill-docs.js")
    parser.add_argument("--projection", default="skill-registry", help="projection profile name")
    args = parser.parse_args()

    config = get_projection_config(args.projection)
    if config.output_schema != "skill_graph":
        raise SystemExit(f"{args.projection} is not a skill graph projection")

    rows = load_registry(Path(args.registry))
    graph = build_graph(rows)
    docs = build_docs(rows)
    write_graph(graph, Path(args.out), Path(args.js_out) if args.js_out else None)
    write_docs(docs, Path(args.docs_out), Path(args.docs_js_out) if args.docs_js_out else None)
    print(
        "wrote "
        f"{args.out} ({graph['counts']['nodes']} nodes, "
        f"{graph['counts']['edges']} edges) and "
        f"{args.docs_out} ({docs['counts']['skills']} skill docs)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
