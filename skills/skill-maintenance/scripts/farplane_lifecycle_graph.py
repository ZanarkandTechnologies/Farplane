#!/usr/bin/env python3
"""Build the Farplane lifecycle graph from skills, hooks, and framework files."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from farplane_lifecycle_catalog import CURATED_EDGES, CURATED_FILES, FSA_SPECS, TARGET_SKILLS
from graph_ir import GraphBundle, GraphEdge, GraphNode, edge_counts, load_js_value as load_graph_js_value
from graph_ir import node_kind_counts, normalized_for_compare, utc_timestamp, write_js, write_json
from graph_projection_config import get_projection_config


JS_PREFIX = "window.FARPLANE_LIFECYCLE_GRAPH = "


@dataclass
class SkillContract:
    name: str
    path: str
    description: str
    tier: int | None
    group: str
    source: str
    reads: list[str]
    writes: list[str]
    routes: list[str]
    gates: list[str]


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
            return [part.strip().strip("\"'") for part in value[1:-1].split(",") if part.strip()]
    if value.startswith(("\"", "'")) and value.endswith(("\"", "'")):
        return value[1:-1]
    try:
        return int(value)
    except ValueError:
        return value


def parse_simple_yaml(raw: str) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    current_list: str | None = None
    current_map: str | None = None
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  - ") and current_list:
            if not isinstance(parsed.get(current_list), list):
                parsed[current_list] = []
            parsed[current_list].append(parse_scalar(line.strip()[2:]))
            continue
        if line.startswith("  ") and current_map:
            key, _, value = line.strip().partition(":")
            if key and value:
                if not isinstance(parsed.get(current_map), dict):
                    parsed[current_map] = {}
                parsed[current_map][key] = parse_scalar(value)
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        if not key:
            continue
        current_list = None
        current_map = None
        if value.strip():
            parsed[key] = parse_scalar(value)
        else:
            parsed[key] = {}
            current_list = key
            current_map = key
    return parsed


def parse_frontmatter(markdown: str) -> tuple[dict[str, Any], str]:
    if not markdown.startswith("---\n"):
        return {}, markdown
    end = markdown.find("\n---\n", 4)
    if end == -1:
        return {}, markdown
    raw = markdown[4:end]
    return parse_simple_yaml(raw), markdown[end + 5 :]


def section_after(markdown: str, heading: str) -> str:
    marker = f"## {heading}"
    start = markdown.find(marker)
    if start == -1:
        return ""
    rest = markdown[start + len(marker) :]
    next_heading = re.search(r"\n##\s+", rest)
    if next_heading:
        return rest[: next_heading.start()]
    return rest


def normalize_label(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip(" ;")


def split_items(raw: str) -> list[str]:
    cleaned = re.sub(r"\s+", " ", raw.replace("\n", " ")).strip()
    cleaned = cleaned.strip(" ;")
    if not cleaned:
        return []
    parts = [normalize_label(part) for part in cleaned.split(",")]
    return [part for part in parts if part and part not in {"and"}]


def extract_call_values(signature: str, name: str) -> list[str]:
    values: list[str] = []
    for match in re.finditer(rf"\b{name}\s*\((.*?)\)", signature, flags=re.DOTALL):
        values.extend(split_items(match.group(1)))
    if values:
        return values
    simple = re.search(rf"\b{name}\s+([^\n]+)", signature)
    if simple:
        return split_items(simple.group(1))
    return []


def extract_label_block(signature: str, label: str) -> str:
    pattern = rf"\b{label}:\s*(.*?)(?=\n\w[\w_-]*:|\n```|\Z)"
    match = re.search(pattern, signature, flags=re.DOTALL)
    return match.group(1).strip() if match else ""


def extract_routes(signature: str) -> list[str]:
    block = extract_label_block(signature, "routes")
    if not block:
        return []
    block = block.replace("|", ",")
    return [normalize_label(part) for part in re.split(r",|\n", block) if normalize_label(part)]


def extract_gates(signature: str) -> list[str]:
    block = extract_label_block(signature, "gates")
    if not block:
        return []
    block = block.replace(";", ",")
    return [normalize_label(part) for part in block.split(",") if normalize_label(part)]


def parse_skill_contract(path: Path, repo_root: Path) -> SkillContract:
    markdown = path.read_text()
    frontmatter, body = parse_frontmatter(markdown)
    name = str(frontmatter.get("name") or path.parent.name)
    signature = section_after(body, "Skill Signature")
    return SkillContract(
        name=name,
        path=path.relative_to(repo_root).as_posix(),
        description=str(frontmatter.get("description", "")),
        tier=frontmatter.get("tier") if isinstance(frontmatter.get("tier"), int) else None,
        group=str(frontmatter.get("group", "")),
        source=str(frontmatter.get("source", "local")),
        reads=extract_call_values(signature, "reads"),
        writes=extract_call_values(signature, "writes"),
        routes=extract_routes(signature),
        gates=extract_gates(signature),
    )


def slug(value: str) -> str:
    value = value.strip().strip("`'\"")
    value = value.replace("?", "")
    value = re.sub(r"\s+when\s+.*$", "", value)
    value = re.sub(r"\s+only\s+.*$", "", value)
    value = value.replace("**", "*")
    return re.sub(r"[^A-Za-z0-9_.*/<>-]+", "-", value).strip("-").lower() or "unknown"


def canonical_ref(value: str) -> tuple[str, str, str, list[str]]:
    raw = value.strip().strip("`'\"")
    raw = raw.removesuffix("?")
    pathish = raw
    pathish = re.sub(r"\s+when\s+.*$", "", pathish)
    pathish = re.sub(r"\s+only\s+.*$", "", pathish)
    pathish = pathish.strip()
    for known_path in sorted(CURATED_FILES, key=len, reverse=True):
        if pathish == known_path or pathish.startswith(f"{known_path} "):
            pathish = known_path
            break
    pathish = pathish.replace("<YYYY-MM-DDTHHMMSSZ>", "<timestamp>")
    pathish = pathish.replace("<YYYY-MM-DDTHHMMSSZ>.md", "<timestamp>.md")
    pathish = pathish.replace("<YYYY-MM-DDTHHMMSSZ>", "<timestamp>")
    if pathish.startswith(".farplane/reports/pulse/"):
        pathish = ".farplane/reports/pulse/<timestamp>.md"
    if pathish.startswith(".farplane/reports/interval/"):
        pathish = ".farplane/reports/interval/<interval_id>/<timestamp>.md"
    if pathish.startswith("tickets/TASK-"):
        if "artifacts" in pathish:
            pathish = "tickets/TASK-*/artifacts/"
        elif pathish.endswith("ticket.md"):
            pathish = "tickets/TASK-*/ticket.md"
        elif pathish.endswith("program.md"):
            pathish = "tickets/TASK-*/program.md"
        elif pathish.endswith("progress.md"):
            pathish = "tickets/TASK-*/progress.md"
    if pathish == "tickets/" or pathish == "tickets":
        pathish = "tickets/TASK-*/ticket.md"
    if pathish.startswith("tickets/progress"):
        return f"state:{slug(raw)}", "state", raw, ["abstract-state"]
    if pathish.startswith(("farplane/", ".farplane/", "docs/", "tickets/", "skills/", "qa/")) or pathish in {
        "AGENTS.md",
        "README.md",
        "ARCHITECTURE.md",
        "PROJECT_RULES.md",
        "hooks.json",
    }:
        kind, label, tags = CURATED_FILES.get(pathish, ("file", pathish, ["parsed"]))
        if pathish.startswith(".farplane/"):
            kind = "report" if "/reports/" in pathish else "state"
        if pathish.startswith("tickets/"):
            kind = "ticket"
        if pathish.startswith("docs/"):
            kind = "doc"
        return f"{kind}:{pathish}", kind, label, list(tags)
    return f"state:{slug(raw)}", "state", raw, ["abstract-state"]


def make_node(node_id: str, kind: str, label: str, path: str | None = None, tags: list[str] | None = None, **metadata: Any) -> dict[str, Any]:
    return GraphNode(
        id=node_id,
        label=label,
        kind=kind,
        path=path or "",
        tags=tuple(tags or ()),
        metadata=metadata,
    ).as_dict()


def add_node(nodes: dict[str, dict[str, Any]], node: dict[str, Any]) -> None:
    existing = nodes.get(node["id"])
    if not existing:
        nodes[node["id"]] = node
        return
    existing["tags"] = sorted(set(existing.get("tags", [])) | set(node.get("tags", [])))
    for key in ("path", "metadata"):
        if key in node and key not in existing:
            existing[key] = node[key]


def add_edge(edges: list[dict[str, Any]], seen: set[tuple[str, str, str, str]], source: str, target: str, edge_type: str, evidence_ref: str, confidence: str, label: str | None = None) -> None:
    key = (source, target, edge_type, evidence_ref)
    if key in seen:
        return
    seen.add(key)
    edges.append(
        GraphEdge(
            source=source,
            target=target,
            type=edge_type,
            label=label or "",
            evidence_ref=evidence_ref,
            confidence=confidence,
        ).as_dict()
    )


def add_ref_node(nodes: dict[str, dict[str, Any]], value: str, include_abstract_state: bool = False) -> str | None:
    node_id, kind, label, tags = canonical_ref(value)
    if kind == "state" and "abstract-state" in tags and not include_abstract_state:
        return None
    path = node_id.split(":", 1)[1] if kind in {"file", "state", "report", "ticket", "doc"} else None
    add_node(nodes, make_node(node_id, kind, label, path=path, tags=tags))
    return node_id


def route_target_node(route: str, repo_root: Path) -> dict[str, Any]:
    route = normalize_label(route)
    base = route.split(":", 1)[0].strip()
    skill_path = repo_root / "skills" / base / "SKILL.md"
    if base and skill_path.exists():
        return make_node(f"skill:{base}", "skill", base, path=f"skills/{base}/SKILL.md", tags=["skill", "route-target"])
    return make_node(f"route:{slug(route)}", "route", route, tags=["route", "abstract-route"])


def parse_hooks(repo_root: Path, nodes: dict[str, dict[str, Any]], edges: list[dict[str, Any]], seen: set[tuple[str, str, str, str]]) -> None:
    hooks_path = repo_root / "hooks.json"
    if not hooks_path.exists():
        return
    data = json.loads(hooks_path.read_text())
    hooks_node = add_ref_node(nodes, "hooks.json")
    if hooks_node is None:
        return
    for event, blocks in data.get("hooks", {}).items():
        event_id = f"hook:{event}"
        add_node(nodes, make_node(event_id, "hook", event, path="hooks.json", tags=["hook"]))
        add_edge(edges, seen, hooks_node, event_id, "contains", "hooks.json", "explicit")
        for block in blocks:
            for hook in block.get("hooks", []):
                command = hook.get("command", "")
                command_id = f"command:{slug(command)[:80]}"
                add_node(
                    nodes,
                    make_node(
                        command_id,
                        "command",
                        command,
                        path="hooks.json",
                        tags=["command", "hook"],
                        timeout=hook.get("timeout"),
                        statusMessage=hook.get("statusMessage", ""),
                    ),
                )
                add_edge(edges, seen, event_id, command_id, "triggers", "hooks.json", "explicit", hook.get("statusMessage"))


def add_curated_framework(nodes: dict[str, dict[str, Any]], edges: list[dict[str, Any]], seen: set[tuple[str, str, str, str]]) -> None:
    for path, (kind, label, tags) in CURATED_FILES.items():
        add_node(nodes, make_node(f"{kind}:{path}", kind, label, path=path, tags=tags))

    for source, target, edge_type, evidence in CURATED_EDGES:
        if source.startswith("runtime:"):
            add_node(nodes, make_node(source, "runtime", source.split(":", 1)[1], tags=["runtime", "goal"]))
        if source.startswith("automation:"):
            add_node(nodes, make_node(source, "automation", source.split(":", 1)[1], tags=["automation"]))
        if target.startswith("runtime:"):
            add_node(nodes, make_node(target, "runtime", target.split(":", 1)[1], tags=["runtime", "goal"]))
        if target.startswith("automation:"):
            add_node(nodes, make_node(target, "automation", target.split(":", 1)[1], tags=["automation"]))
        add_edge(edges, seen, source, target, edge_type, evidence, "curated")


def build_fsa_projection(projection_id: str, label: str, state_labels: list[str], terminal: list[str]) -> dict[str, Any]:
    states = []
    transitions = []
    for index, state_label in enumerate(state_labels):
        state_id = f"fsa:{projection_id}:{slug(state_label)}"
        states.append(state_id)
        if index:
            previous = states[index - 1]
            transitions.append(
                {
                    "source": previous,
                    "target": state_id,
                    "type": "transition",
                    "label": f"{state_labels[index - 1]} -> {state_label}",
                    "evidence_ref": "docs/farplane-framework/graph-contract.md",
                    "confidence": "curated",
                }
            )
    return {
        "id": projection_id,
        "label": label,
        "start": states[0],
        "terminal": [f"fsa:{projection_id}:{slug(item)}" for item in terminal],
        "states": states,
        "transitions": transitions,
    }


def add_fsa_nodes(nodes: dict[str, dict[str, Any]], projections: list[dict[str, Any]]) -> None:
    for projection in projections:
        for state_id in projection["states"]:
            label = state_id.rsplit(":", 1)[1].replace("-", " ")
            add_node(nodes, make_node(state_id, "fsa_state", label, tags=["fsa", projection["id"]]))


def build_fsa_projections() -> list[dict[str, Any]]:
    return [
        build_fsa_projection(projection_id, label, states, terminal)
        for projection_id, label, states, terminal in FSA_SPECS
    ]


def build_graph(
    repo_root: Path,
    include_gates: bool = False,
    include_abstract_state: bool = False,
    include_fsa_nodes: bool = False,
) -> dict[str, Any]:
    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str, str]] = set()
    parsed_skills: list[SkillContract] = []
    missing_skills: list[str] = []

    for skill_name in TARGET_SKILLS:
        path = repo_root / "skills" / skill_name / "SKILL.md"
        if not path.exists():
            missing_skills.append(skill_name)
            continue
        contract = parse_skill_contract(path, repo_root)
        parsed_skills.append(contract)
        skill_id = f"skill:{contract.name}"
        add_node(
            nodes,
            make_node(
                skill_id,
                "skill",
                contract.name,
                path=contract.path,
                tags=["skill", contract.group] if contract.group else ["skill"],
                description=contract.description,
                tier=contract.tier,
                source=contract.source,
            ),
        )
        for value in contract.reads:
            target = add_ref_node(nodes, value, include_abstract_state)
            if target is not None:
                add_edge(edges, seen, skill_id, target, "reads", contract.path, "parsed", value)
        for value in contract.writes:
            target = add_ref_node(nodes, value, include_abstract_state)
            if target is not None:
                add_edge(edges, seen, skill_id, target, "writes", contract.path, "parsed", value)
        for route in contract.routes:
            route = normalize_label(route)
            if not route:
                continue
            target = route_target_node(route, repo_root)
            target_id = target["id"]
            add_node(nodes, target)
            add_edge(edges, seen, skill_id, target_id, "routes_to", contract.path, "parsed", route)
        if include_gates:
            for gate in contract.gates:
                gate_id = f"gate:{slug(gate)}"
                add_node(nodes, make_node(gate_id, "gate", gate, tags=["gate"]))
                add_edge(edges, seen, skill_id, gate_id, "guards", contract.path, "parsed", gate)

    add_curated_framework(nodes, edges, seen)
    parse_hooks(repo_root, nodes, edges, seen)
    fsa_projections = build_fsa_projections()
    if include_fsa_nodes:
        add_fsa_nodes(nodes, fsa_projections)

    confidence_counts = Counter(edge["confidence"] for edge in edges)
    counts = {
        "nodes": len(nodes),
        "edges": len(edges),
        "fsa_projections": len(fsa_projections),
        "node_kinds": node_kind_counts(list(nodes.values())),
        "edge_types": edge_counts(edges),
        "edge_confidence": dict(sorted(confidence_counts.items())),
        "parsed_skills": len(parsed_skills),
    }
    return GraphBundle(
        nodes=sorted(nodes.values(), key=lambda node: (node["kind"], node["id"])),
        edges=sorted(edges, key=lambda edge: (edge["source"], edge["target"], edge["type"], edge["evidence_ref"])),
        generated_at=utc_timestamp(),
        counts=counts,
        extras={
            "source": {
            "generator": "skills/skill-maintenance/scripts/generate_farplane_lifecycle_graph.py",
            "target_skills": TARGET_SKILLS,
            "missing_skills": missing_skills,
            "mode": "full" if include_gates or include_abstract_state or include_fsa_nodes else "core",
            "included_optional_nodes": {
                "gates": include_gates,
                "abstract_state": include_abstract_state,
                "fsa_state_nodes": include_fsa_nodes,
            },
            },
            "fsa_projections": fsa_projections,
        },
    ).as_dict()


def load_js_value(path: Path, global_name: str = "FARPLANE_LIFECYCLE_GRAPH") -> dict[str, Any]:
    return load_graph_js_value(path, global_name)


def validate_graph(graph: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    nodes = {node["id"] for node in graph.get("nodes", [])}
    for edge in graph.get("edges", []):
        if edge["source"] not in nodes:
            errors.append(f"missing source node for edge {edge}")
        if edge["target"] not in nodes:
            errors.append(f"missing target node for edge {edge}")
        if edge.get("confidence") == "explicit" and not edge.get("evidence_ref"):
            errors.append(f"explicit edge lacks evidence_ref: {edge}")
    required_nodes = [
        "skill:init-advisor",
        "skill:metric-advisor",
        "skill:goal-advisor",
        "skill:proof-advisor",
        "skill:pulse-update",
        "skill:interval-update",
        "skill:update-memory",
        "skill:skill-maintenance",
        "skill:eval",
        "skill:knowledge-tidier",
        "file:farplane/metrics.yaml",
        "file:farplane/pm.json",
        "hook:UserPromptSubmit",
        "hook:Stop",
    ]
    for node in required_nodes:
        if node not in nodes:
            errors.append(f"missing required node {node}")
    projection_ids = {projection["id"] for projection in graph.get("fsa_projections", [])}
    for projection_id in {
        "project_initialization",
        "automation_activation",
        "ticket_goal_execution",
        "memory_drain_upkeep",
    }:
        if projection_id not in projection_ids:
            errors.append(f"missing FSA projection {projection_id}")
    return errors


def main() -> int:
    config = get_projection_config("farplane-lifecycle-core")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out", default=config.default_out)
    parser.add_argument("--js-out", default=config.default_js_out)
    parser.add_argument("--check", action="store_true", help="validate generated graph shape and on-disk artifact")
    parser.add_argument("--full", action="store_true", help="include gates, abstract state, and FSA state nodes")
    parser.add_argument("--include-gates", action="store_true", help="include skill gate nodes and guard edges")
    parser.add_argument("--include-abstract-state", action="store_true", help="include abstract prose-derived state nodes")
    parser.add_argument("--include-fsa-nodes", action="store_true", help="include FSA state nodes in the top-level node list")
    parser.add_argument("--projection", default="farplane-lifecycle-core", help="projection profile name")
    args = parser.parse_args()

    config = get_projection_config(args.projection)
    if config.output_schema != "lifecycle_graph":
        raise SystemExit(f"{args.projection} is not a lifecycle graph projection")
    profile_gates = "gates" in config.optional_nodes
    profile_abstract = "abstract_state" in config.optional_nodes
    profile_fsa = "fsa_state_nodes" in config.optional_nodes
    repo_root = Path(args.repo_root).resolve()
    graph = build_graph(
        repo_root,
        include_gates=args.full or args.include_gates or profile_gates,
        include_abstract_state=args.full or args.include_abstract_state or profile_abstract,
        include_fsa_nodes=args.full or args.include_fsa_nodes or profile_fsa,
    )
    errors = validate_graph(graph)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    out_path = repo_root / args.out
    js_path = repo_root / args.js_out if args.js_out else None
    if args.check:
        if not out_path.exists():
            print(f"{args.out} does not exist", file=sys.stderr)
            return 1
        existing = json.loads(out_path.read_text())
        if normalized_for_compare(existing) != normalized_for_compare(graph):
            print(f"{args.out} is stale; rerun generator", file=sys.stderr)
            return 1
        if js_path:
            if not js_path.exists():
                print(f"{args.js_out} does not exist", file=sys.stderr)
                return 1
            existing_js = load_js_value(js_path)
            if normalized_for_compare(existing_js) != normalized_for_compare(graph):
                print(f"{args.js_out} is stale; rerun generator", file=sys.stderr)
                return 1
        print(
            "farplane lifecycle graph OK "
            f"({graph['counts']['nodes']} nodes, {graph['counts']['edges']} edges, "
            f"{graph['counts']['fsa_projections']} FSA projections)"
        )
        return 0

    write_json(out_path, graph)
    if js_path:
        write_js(js_path, "FARPLANE_LIFECYCLE_GRAPH", graph)
    print(
        "wrote "
        f"{args.out} ({graph['counts']['nodes']} nodes, {graph['counts']['edges']} edges, "
        f"{graph['counts']['fsa_projections']} FSA projections)"
    )
    return 0
