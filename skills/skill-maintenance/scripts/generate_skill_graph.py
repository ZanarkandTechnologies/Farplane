#!/usr/bin/env python3
"""Generate graph and document data for the Farplane skill registry."""

from __future__ import annotations

import argparse
import json
import os
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from graph_ir import GraphBundle, GraphEdge, GraphNode, edge_counts, utc_timestamp, write_js, write_json
from graph_projection_config import get_projection_config

SKILL_HEAT_EVENT_TYPES = {
    "control_surface_detected",
    "hook_result",
    "learning_review_launched",
    "skill_requested",
}
DEFAULT_SKILL_HEAT_WINDOW_DAYS = 30
DEFAULT_SKILL_HEAT_RECENT_DAYS = 7
DEFAULT_SKILL_HEAT_TOP_N = 25


def configured_positive_int(env_name: str, default: int) -> int:
    raw = os.environ.get(env_name, "").strip()
    if not raw:
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return value if value > 0 else default


def configured_skill_heat_event_types() -> set[str]:
    raw = os.environ.get("FARPLANE_SKILL_HEAT_EVENT_TYPES", "").strip()
    if not raw:
        return set(SKILL_HEAT_EVENT_TYPES)
    configured = {item.strip() for item in raw.replace("\n", ",").split(",") if item.strip()}
    return configured or set(SKILL_HEAT_EVENT_TYPES)


def skill_heat_config_from_env() -> dict[str, Any]:
    window_days = configured_positive_int("FARPLANE_SKILL_HEAT_WINDOW_DAYS", DEFAULT_SKILL_HEAT_WINDOW_DAYS)
    recent_days = configured_positive_int("FARPLANE_SKILL_HEAT_RECENT_DAYS", DEFAULT_SKILL_HEAT_RECENT_DAYS)
    if recent_days > window_days:
        recent_days = window_days
    return {
        "window_days": window_days,
        "recent_days": recent_days,
        "default_top_n": configured_positive_int("FARPLANE_SKILL_HEAT_TOP_N", DEFAULT_SKILL_HEAT_TOP_N),
        "event_types": sorted(configured_skill_heat_event_types()),
    }


def load_registry(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def find_repo_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "docs" / "skills" / "registry.jsonl").exists() and (candidate / "skills").exists():
            return candidate
    return Path.cwd()


def skill_ref_name(ref: str) -> str:
    base = ref.split("#", 1)[0]
    return base.split(":", 1)[0]


def parse_event_timestamp(value: object) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def event_invocation_key(event: dict[str, Any]) -> tuple[str, ...]:
    skill_name = str(event.get("skill_name") or "")
    session_id = str(event.get("session_id") or "")
    turn_id = str(event.get("turn_id") or "")
    ticket_id = str(event.get("ticket_id") or "")
    event_id = str(event.get("event_id") or "")
    anchor = turn_id or ticket_id or event_id
    return (skill_name, session_id, anchor)


def load_skill_heat(
    repo_root: Path,
    skill_names: set[str],
    now: datetime | None = None,
    config: dict[str, Any] | None = None,
) -> dict[str, dict[str, Any]]:
    event_dir = repo_root / ".farplane" / "events"
    heat_config = config or skill_heat_config_from_env()
    window_days = int(heat_config.get("window_days") or DEFAULT_SKILL_HEAT_WINDOW_DAYS)
    recent_days = int(heat_config.get("recent_days") or DEFAULT_SKILL_HEAT_RECENT_DAYS)
    counted_event_types = set(heat_config.get("event_types") or SKILL_HEAT_EVENT_TYPES)
    heat: dict[str, dict[str, Any]] = {
        name: {
            "invocation_count_all": 0,
            "invocation_count_recent": 0,
            "invocation_count_window": 0,
            "observed_event_count_all": 0,
            "distinct_threads_window": 0,
            "distinct_tickets_window": 0,
            "last_invoked_at": "",
            "window_days": window_days,
            "recent_days": recent_days,
        }
        for name in skill_names
    }
    if not event_dir.exists():
        return heat

    records: list[tuple[datetime, dict[str, Any]]] = []
    for path in sorted(event_dir.glob("*.jsonl")):
        if not path.is_file() or path.name == "failed-sync.jsonl":
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not isinstance(event, dict):
                continue
            skill_name = str(event.get("skill_name") or "")
            event_type = str(event.get("event_type") or "")
            if skill_name not in skill_names or event_type not in counted_event_types:
                continue
            timestamp = parse_event_timestamp(event.get("timestamp"))
            if timestamp is None:
                continue
            records.append((timestamp, event))

    clock = now.astimezone(UTC) if now else datetime.now(UTC)
    recent_window = clock - timedelta(days=recent_days)
    main_window = clock - timedelta(days=window_days)
    seen_all: set[tuple[str, ...]] = set()
    seen_recent: set[tuple[str, ...]] = set()
    seen_window: set[tuple[str, ...]] = set()
    threads_window: dict[str, set[str]] = defaultdict(set)
    tickets_window: dict[str, set[str]] = defaultdict(set)

    for timestamp, event in records:
        skill_name = str(event.get("skill_name") or "")
        item = heat[skill_name]
        item["observed_event_count_all"] += 1
        if not item["last_invoked_at"] or timestamp.isoformat() > str(item["last_invoked_at"]):
            item["last_invoked_at"] = timestamp.isoformat().replace("+00:00", "Z")

        key = event_invocation_key(event)
        if key not in seen_all:
            seen_all.add(key)
            item["invocation_count_all"] += 1
        if timestamp >= recent_window and key not in seen_recent:
            seen_recent.add(key)
            item["invocation_count_recent"] += 1
        if timestamp >= main_window and key not in seen_window:
            seen_window.add(key)
            item["invocation_count_window"] += 1
            session_id = str(event.get("session_id") or "")
            ticket_id = str(event.get("ticket_id") or "")
            if session_id:
                threads_window[skill_name].add(session_id)
            if ticket_id:
                tickets_window[skill_name].add(ticket_id)

    for skill_name, item in heat.items():
        item["distinct_threads_window"] = len(threads_window.get(skill_name, set()))
        item["distinct_tickets_window"] = len(tickets_window.get(skill_name, set()))
        # Compatibility aliases for existing readers while the graph UI migrates.
        item["invocation_count_7d"] = item["invocation_count_recent"]
        item["invocation_count_30d"] = item["invocation_count_window"]
        item["distinct_threads_30d"] = item["distinct_threads_window"]
        item["distinct_tickets_30d"] = item["distinct_tickets_window"]
        item["heat_score"] = (
            item["invocation_count_window"]
            + item["distinct_threads_window"]
            + item["distinct_tickets_window"]
        )
    return heat


def build_graph(
    rows: list[dict[str, Any]],
    skill_heat: dict[str, dict[str, Any]] | None = None,
    skill_heat_config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    skill_names = {row["name"] for row in rows}
    nodes = [
        GraphNode(
            id=row["name"],
            label=row["name"],
            attributes={
                "tier": row.get("tier"),
                "source": row.get("source", "local"),
                "group": row.get("group", ""),
                "todo_skill_refs": row.get("todo_skill_refs", []),
                "methods": row.get("methods", []),
                "has_checklist": bool(row.get("has_checklist")),
                "eval": row.get("eval", ""),
                "qa_checklist": row.get("qa_checklist", ""),
                "skill_ui": row.get("skill_ui", ""),
                "path": row.get("path", ""),
                "description": row.get("description", ""),
                "heat": (skill_heat or {}).get(row["name"], {}),
            },
        ).as_dict()
        for row in rows
    ]

    edges: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str, str]] = set()

    def add_edge(
        source: str,
        target_ref: str,
        edge_type: str,
        label: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
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
                metadata={"target_ref": target_ref, **(metadata or {})},
            ).as_dict()
        )

    for row in rows:
        source = row["name"]
        for link in row.get("skill_links", []):
            label = link if "#" in link or ":" in link else "markdown-ref"
            add_edge(source, link, "markdown-ref", label)
        for target_ref in row.get("common_chains", {}).get("after", []):
            add_edge(source, target_ref, "common-chain", "common_chains.after")
        for order, target_ref in enumerate(row.get("todo_skill_refs", []), start=1):
            add_edge(
                source,
                target_ref,
                "todo-chain",
                f"todo.{order}",
                {"order": order, "chain_source": "todo_list"},
            )

    nodes.sort(key=lambda node: (int(node.get("tier") or 9), node["label"]))
    edges.sort(key=lambda edge: (edge["source"], edge["target"], edge["type"], edge["label"]))

    counts = {
        "nodes": len(nodes),
        "edges": len(edges),
        "tiers": {},
        "sources": {},
        "edge_types": edge_counts(edges),
        "skill_heat_config": skill_heat_config or skill_heat_config_from_env(),
        "skill_heat_event_types": (skill_heat_config or skill_heat_config_from_env()).get("event_types"),
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

    registry_path = Path(args.registry)
    rows = load_registry(registry_path)
    repo_root = find_repo_root(registry_path.resolve())
    skill_heat_config = skill_heat_config_from_env()
    skill_heat = load_skill_heat(repo_root, {row["name"] for row in rows}, config=skill_heat_config)
    graph = build_graph(rows, skill_heat=skill_heat, skill_heat_config=skill_heat_config)
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
