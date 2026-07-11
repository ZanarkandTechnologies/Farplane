#!/usr/bin/env python3
"""Build the manifest-backed Farplane framework core graph projection.

Ownership: skill-maintenance graph generation.
Inputs: farplane/manifest.json farplane_graph.framework_core plus the
harness-reference graph extracted from local file links.
Outputs: a GraphIR-compatible projection where key framework docs, directly
referenced framework docs/files, and directly mentioned skills are explicit.
Side effects: none unless called through the projection writer.
"""

from __future__ import annotations

import fnmatch
import json
import re
from collections import Counter
from pathlib import Path, PurePosixPath
from typing import Any

import farplane_lifecycle_catalog
import generate_harness_graph
import generate_skill_graph
from graph_ir import GraphBundle, edge_counts, node_kind_counts, validate_edge_endpoints


DEFAULT_INCLUDE = [
    "docs/farplane-framework/README.md",
    "docs/farplane-framework/lifecycle.md",
    "docs/farplane-framework/init-advisor-critical-path.md",
    "docs/farplane-framework/project-files.md",
    "docs/farplane-framework/graph-contract.md",
    "docs/farplane-framework/hooks-and-runtime.md",
    "docs/farplane-framework/harness-maintenance.md",
]

DEFAULT_EXCLUDE = [
    "tickets/archive/**",
    ".farplane/reports/**",
    ".farplane/logs/**",
    ".farplane/**",
]

KNOWN_LINKED_KINDS = {
    "doc",
    "file",
    "root-doc",
    "skill",
    "skill-doc",
    "spec",
}

DIRECT_FILE_PREFIXES = (
    "docs/farplane-framework/",
    "docs/features/",
    "farplane/",
)

SKIP_DIRECT_PREFIXES = (
    "skills/skill-maintenance/graph/",
)

WORKFLOWS = [
    {
        "id": "workflow:lifecycle",
        "label": "Farplane lifecycle",
        "description": "Top-level lifecycle spine from init through metric objectives, proof, autonomy loops, and improvement.",
        "doc": "docs/farplane-framework/lifecycle.md",
        "skills": [],
    },
    {
        "id": "workflow:bootstrap",
        "label": "Bootstrap",
        "description": "Create the project substrate and first usable harness state.",
        "doc": "docs/farplane-framework/init-advisor-critical-path.md",
        "skills": ["init-advisor", "harness-creator", "deep-interview", "prd", "spec-to-ticket"],
    },
    {
        "id": "workflow:strategy",
        "label": "Strategy",
        "description": "Shape measurable objectives, guards, proposal trajectories, and executable frontier choices.",
        "doc": "docs/farplane-framework/lifecycle.md",
        "skills": ["metric-advisor", "leverage-advisor", "harness-advisor", "goal-advisor"],
    },
    {
        "id": "workflow:goal-execution",
        "label": "Goal execution",
        "description": "Compile a goal into a ticket-backed program, execute it, and produce proof.",
        "doc": "docs/farplane-framework/lifecycle.md",
        "skills": ["goal-advisor", "impl-plan", "qa", "demo", "review"],
    },
    {
        "id": "workflow:autonomy-loops",
        "label": "Autonomy loops",
        "description": "Run Pulse and interval loops for bounded action and planning cadence.",
        "doc": "docs/farplane-framework/hooks-and-runtime.md",
        "skills": ["automation-advisor", "pulse-update", "interval-update"],
    },
    {
        "id": "workflow:proof",
        "label": "Proof",
        "description": "Select and run proof paths for claims, tickets, skills, and workflows.",
        "doc": "docs/farplane-framework/lifecycle.md",
        "skills": ["proof-advisor", "eval", "qa", "review"],
    },
    {
        "id": "workflow:improvement",
        "label": "Improvement",
        "description": "Drain outcomes into memory, lessons, skill maintenance, and future evals.",
        "doc": "docs/farplane-framework/lifecycle.md",
        "skills": ["update-memory", "skill-maintenance", "skill-creator", "optimize-harness", "eval"],
    },
]


def read_manifest(repo_root: Path) -> dict[str, Any]:
    path = repo_root / "farplane" / "manifest.json"
    return json.loads(path.read_text())


def framework_core_config(manifest: dict[str, Any]) -> dict[str, list[str]]:
    raw = manifest.get("farplane_graph", {})
    core = raw.get("framework_core", {}) if isinstance(raw, dict) else {}
    include = core.get("include") if isinstance(core, dict) else None
    exclude = core.get("exclude") if isinstance(core, dict) else None
    return {
        "include": [str(item) for item in include] if isinstance(include, list) else list(DEFAULT_INCLUDE),
        "exclude": [str(item) for item in exclude] if isinstance(exclude, list) else list(DEFAULT_EXCLUDE),
    }


def node_path(node: dict[str, Any]) -> str:
    path = str(node.get("path") or "")
    if path:
        return path.rstrip("/")
    node_id = str(node.get("id", ""))
    if node_id.startswith("file:"):
        return node_id.removeprefix("file:").rstrip("/")
    if node_id.startswith("dir:"):
        return node_id.removeprefix("dir:").rstrip("/")
    if node_id.startswith("skill:"):
        return f"skills/{node_id.removeprefix('skill:')}/SKILL.md"
    return node_id


def pattern_matches(path: str, pattern: str) -> bool:
    normalized = path.strip("/")
    normalized_pattern = pattern.strip("/")
    if PurePosixPath(normalized).match(normalized_pattern):
        return True
    if fnmatch.fnmatchcase(normalized, normalized_pattern):
        return True
    if "/**/" in normalized_pattern:
        direct_pattern = normalized_pattern.replace("/**/", "/")
        return PurePosixPath(normalized).match(direct_pattern) or fnmatch.fnmatchcase(normalized, direct_pattern)
    return False


def matches_any(path: str, patterns: list[str]) -> bool:
    return any(pattern_matches(path, pattern) for pattern in patterns)


def is_included_source(node: dict[str, Any], include: list[str], exclude: list[str]) -> bool:
    path = node_path(node)
    return matches_any(path, include) and not matches_any(path, exclude)


def is_excluded(node: dict[str, Any], exclude: list[str]) -> bool:
    return matches_any(node_path(node), exclude)


def edge_key(edge: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        str(edge.get("source")),
        str(edge.get("target")),
        str(edge.get("type", "")),
        str(edge.get("from_file", edge.get("raw_ref", ""))),
    )


def skill_ids(repo_root: Path) -> list[str]:
    skills_root = repo_root / "skills"
    if not skills_root.exists():
        return []
    return sorted(
        path.parent.name
        for path in skills_root.glob("*/SKILL.md")
        if path.parent.name
    )


def skill_heat(repo_root: Path, names: set[str]) -> dict[str, dict[str, Any]]:
    registry = repo_root / "docs" / "skills" / "registry.jsonl"
    if not registry.exists() or not names:
        return {}
    config = generate_skill_graph.skill_heat_config_from_env()
    return generate_skill_graph.load_skill_heat(repo_root, names, config=config)


def read_source_text(repo_root: Path, node: dict[str, Any]) -> str:
    path = repo_root / node_path(node)
    if not path.is_file():
        return ""
    try:
        return path.read_text(errors="ignore")
    except UnicodeDecodeError:
        return ""


def mentioned_skill_ids(text: str, ids: list[str]) -> list[str]:
    matches: list[str] = []
    for skill_id in ids:
        if re.search(rf"(?<![\w-]){re.escape(skill_id)}(?![\w-])", text):
            matches.append(skill_id)
    return matches


def direct_target_allowed(target: dict[str, Any], source_ids: set[str], excluded_ids: set[str]) -> bool:
    target_id = str(target.get("id"))
    if target_id in excluded_ids:
        return False
    if target_id in source_ids:
        return True
    path = node_path(target)
    if any(path.startswith(prefix) for prefix in SKIP_DIRECT_PREFIXES):
        return False
    if str(target.get("kind")) == "skill":
        return True
    return any(path.startswith(prefix) for prefix in DIRECT_FILE_PREFIXES)


def workflow_nodes() -> dict[str, dict[str, Any]]:
    nodes: dict[str, dict[str, Any]] = {}
    for index, workflow in enumerate(WORKFLOWS):
        nodes[workflow["id"]] = {
            "id": workflow["id"],
            "label": workflow["label"],
            "kind": "workflow",
            "path": workflow["doc"],
            "description": workflow["description"],
            "framework_role": "workflow",
            "source_match": False,
            "source_path": workflow["doc"],
            "workflow_order": index,
            "workflow_skills": workflow["skills"],
            "tags": ["framework-core", "framework-role:workflow", "workflow"],
        }
    return nodes


def add_workflow_edges(
    edges: dict[tuple[str, str, str, str], dict[str, Any]],
    node_ids: set[str],
) -> set[str]:
    linked_ids: set[str] = set()
    root = "workflow:lifecycle"
    lifecycle_doc = "file:docs/farplane-framework/lifecycle.md"
    for index, workflow in enumerate(WORKFLOWS):
        workflow_id = str(workflow["id"])
        if workflow_id not in node_ids:
            continue
        if workflow_id != root and root in node_ids:
            edge = {
                "source": root,
                "target": workflow_id,
                "type": "workflow-stage",
                "label": f"stage.{index}",
                "from_file": "docs/farplane-framework/lifecycle.md",
                "raw_ref": workflow_id,
                "confidence": "curated",
                "order": index,
            }
            edges[edge_key(edge)] = edge
        doc_id = f"file:{workflow['doc']}"
        if doc_id in node_ids:
            edge = {
                "source": doc_id,
                "target": workflow_id,
                "type": "defines-workflow",
                "label": workflow["label"],
                "from_file": str(workflow["doc"]),
                "raw_ref": workflow_id,
                "confidence": "curated",
            }
            edges[edge_key(edge)] = edge
        if lifecycle_doc in node_ids and workflow_id != root:
            edge = {
                "source": lifecycle_doc,
                "target": workflow_id,
                "type": "lifecycle-workflow",
                "label": workflow["label"],
                "from_file": "docs/farplane-framework/lifecycle.md",
                "raw_ref": workflow_id,
                "confidence": "curated",
            }
            edges[edge_key(edge)] = edge

        previous_skill = ""
        for order, skill_id in enumerate(workflow["skills"], start=1):
            target = f"skill:{skill_id}"
            if target not in node_ids:
                continue
            linked_ids.add(target)
            edge = {
                "source": workflow_id,
                "target": target,
                "type": "workflow-skill",
                "label": f"{order}. {skill_id}",
                "from_file": str(workflow["doc"]),
                "raw_ref": skill_id,
                "confidence": "curated",
                "order": order,
            }
            edges[edge_key(edge)] = edge
            if previous_skill and previous_skill in node_ids:
                next_edge = {
                    "source": previous_skill,
                    "target": target,
                    "type": "workflow-next",
                    "label": f"next.{order - 1}",
                    "from_file": str(workflow["doc"]),
                    "raw_ref": workflow_id,
                    "confidence": "curated",
                    "order": order - 1,
                }
                edges[edge_key(next_edge)] = next_edge
            previous_skill = target
    return linked_ids


def add_curated_skill_edges(
    edges: dict[tuple[str, str, str, str], dict[str, Any]],
    node_ids: set[str],
) -> None:
    for source, target, edge_type, evidence_ref in farplane_lifecycle_catalog.CURATED_EDGES:
        if source not in node_ids or target not in node_ids:
            continue
        edge = {
            "source": source,
            "target": target,
            "type": edge_type,
            "label": edge_type,
            "from_file": evidence_ref,
            "raw_ref": target,
            "confidence": "curated",
        }
        edges[edge_key(edge)] = edge


def expand_direct_framework_refs(
    repo_root: Path,
    graph: dict[str, Any],
    all_nodes: dict[str, dict[str, Any]],
    source_ids: set[str],
    excluded_ids: set[str],
) -> tuple[set[str], list[dict[str, Any]], set[str]]:
    """Keep source docs plus direct framework refs and directly mentioned skills."""
    kept_ids = set(source_ids)
    kept_edges: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    linked_ids: set[str] = set()

    for edge in graph.get("edges", []):
        source = str(edge.get("source"))
        target = str(edge.get("target"))
        if source not in source_ids:
            continue
        if source in excluded_ids or target in excluded_ids:
            continue
        target_node = all_nodes.get(target)
        if not target_node or not direct_target_allowed(target_node, source_ids, excluded_ids):
            continue
        kept_ids.add(target)
        linked_ids.add(target)
        kept_edges[edge_key(edge)] = edge

    ids = skill_ids(repo_root)
    for source_id in sorted(source_ids):
        source_node = all_nodes.get(source_id)
        if not source_node:
            continue
        text = read_source_text(repo_root, source_node)
        for skill_id in mentioned_skill_ids(text, ids):
            target = f"skill:{skill_id}"
            if target not in all_nodes or target in excluded_ids:
                continue
            if target in linked_ids:
                continue
            kept_ids.add(target)
            linked_ids.add(target)
            edge = {
                "source": source_id,
                "target": target,
                "type": "mentions-skill",
                "from_file": node_path(source_node),
                "raw_ref": skill_id,
                "confidence": "parsed",
            }
            kept_edges[edge_key(edge)] = edge

    for workflow in WORKFLOWS:
        kept_ids.add(str(workflow["id"]))
        doc_id = f"file:{workflow['doc']}"
        if doc_id in all_nodes and doc_id not in excluded_ids:
            kept_ids.add(doc_id)
            linked_ids.add(doc_id)
        for skill_id in workflow["skills"]:
            target = f"skill:{skill_id}"
            if target in all_nodes and target not in excluded_ids:
                kept_ids.add(target)
                linked_ids.add(target)

    return kept_ids, list(kept_edges.values()), linked_ids


def graph_role(node: dict[str, Any], source_ids: set[str], linked_ids: set[str], edges: list[dict[str, Any]]) -> str:
    node_id = str(node.get("id"))
    if str(node.get("kind")) == "workflow":
        return "workflow"
    if node_id in source_ids:
        has_edge = any(edge.get("source") == node_id or edge.get("target") == node_id for edge in edges)
        return "source" if has_edge else "isolated"
    if node_id in linked_ids:
        return "linked" if str(node.get("kind", "")) in KNOWN_LINKED_KINDS else "other"
    return "other"


def annotate_node(
    node: dict[str, Any],
    role: str,
    source_ids: set[str],
    config: dict[str, list[str]],
    heat: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    annotated = dict(node)
    tags = set(str(tag) for tag in annotated.get("tags", []))
    tags.add("framework-core")
    tags.add(f"framework-role:{role}")
    annotated["tags"] = sorted(tags)
    annotated["framework_role"] = role
    annotated["source_match"] = str(node.get("id")) in source_ids
    annotated["source_path"] = node_path(node)
    if role == "other":
        annotated["kind"] = "other"
    if str(node.get("kind")) == "skill":
        skill_id = str(node.get("id", "")).removeprefix("skill:")
        if skill_id in heat:
            annotated["heat"] = heat[skill_id]
    if str(node.get("id")) in source_ids:
        matched = [pattern for pattern in config["include"] if pattern_matches(node_path(node), pattern)]
        annotated["matched_patterns"] = matched
    return annotated


def annotate_edge(edge: dict[str, Any]) -> dict[str, Any]:
    annotated = dict(edge)
    annotated["projection"] = "farplane-framework-core"
    return annotated


def build_graph(repo_root: Path) -> dict[str, Any]:
    manifest = read_manifest(repo_root)
    config = framework_core_config(manifest)
    harness_graph = generate_harness_graph.build_graph(repo_root)
    all_nodes = {str(node["id"]): node for node in harness_graph.get("nodes", [])}
    all_nodes.update(workflow_nodes())
    excluded_ids = {
        node_id
        for node_id, node in all_nodes.items()
        if is_excluded(node, config["exclude"])
    }
    source_ids = {
        node_id
        for node_id, node in all_nodes.items()
        if (
            node_id not in excluded_ids
            and str(node.get("kind")) != "workflow"
            and is_included_source(node, config["include"], config["exclude"])
        )
    }
    projected_ids, projected_edges, linked_ids = expand_direct_framework_refs(
        repo_root,
        harness_graph,
        all_nodes,
        source_ids,
        excluded_ids,
    )
    projected_edge_map = {edge_key(edge): edge for edge in projected_edges}
    workflow_linked_ids = add_workflow_edges(projected_edge_map, projected_ids)
    linked_ids.update(workflow_linked_ids)
    add_curated_skill_edges(projected_edge_map, projected_ids)
    projected_edges = list(projected_edge_map.values())
    heat = skill_heat(
        repo_root,
        {
            str(node_id).removeprefix("skill:")
            for node_id in projected_ids
            if str(node_id).startswith("skill:")
        },
    )
    projected_nodes = []
    for node_id in sorted(projected_ids):
        node = all_nodes[node_id]
        role = graph_role(node, source_ids, linked_ids, projected_edges)
        projected_nodes.append(annotate_node(node, role, source_ids, config, heat))
    annotated_edges = [annotate_edge(edge) for edge in projected_edges]
    role_counts = Counter(str(node.get("framework_role", "other")) for node in projected_nodes)
    counts = {
        "nodes": len(projected_nodes),
        "edges": len(annotated_edges),
        "source_nodes": len(source_ids),
        "linked_nodes": len(linked_ids),
        "workflow_nodes": role_counts.get("workflow", 0),
        "isolated_nodes": role_counts.get("isolated", 0),
        "other_nodes": role_counts.get("other", 0),
        "node_kinds": node_kind_counts(projected_nodes),
        "edge_types": edge_counts(annotated_edges),
        "framework_roles": dict(sorted(role_counts.items())),
    }
    return GraphBundle(
        nodes=sorted(projected_nodes, key=lambda node: (str(node.get("framework_role", "")), str(node.get("kind", "")), str(node.get("label", "")))),
        edges=sorted(annotated_edges, key=lambda edge: (str(edge.get("source", "")), str(edge.get("target", "")), str(edge.get("type", "")), str(edge.get("from_file", "")))),
        generated_at=str(harness_graph.get("generated_at", "")),
        counts=counts,
        extras={
            "projection": "farplane-framework-core",
            "source": {
                "manifest": "farplane/manifest.json",
                "include": config["include"],
                "exclude": config["exclude"],
                "expansion": "framework-doc-direct-refs",
            },
        },
    ).as_dict()


def validate_graph(graph: dict[str, Any]) -> list[str]:
    errors = validate_edge_endpoints(graph)
    if not graph.get("nodes"):
        errors.append("framework core graph has no nodes")
    if not graph.get("counts", {}).get("source_nodes"):
        errors.append("framework core graph has no manifest-matched source nodes")
    return errors
