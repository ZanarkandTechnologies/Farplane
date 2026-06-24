#!/usr/bin/env python3
"""Projection helpers for Farplane graph dictionaries."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from graph_ir import load_js_value, normalized_for_compare, write_js, write_json
from graph_projection_config import ProjectionConfig


def _passes_includes(value: str, includes: frozenset[str]) -> bool:
    return not includes or value in includes


def _passes_excludes(value: str, excludes: frozenset[str]) -> bool:
    return value not in excludes


def project_graph(graph: dict[str, Any], config: ProjectionConfig, annotate: bool = False) -> dict[str, Any]:
    """Apply generic kind/type/tag/confidence filters to a graph dictionary."""
    projected = dict(graph)
    nodes = []
    for node in graph.get("nodes", []):
        kind = str(node.get("kind", ""))
        tags = set(node.get("tags", []))
        if not _passes_includes(kind, config.include_node_kinds):
            continue
        if not _passes_excludes(kind, config.exclude_node_kinds):
            continue
        if config.include_tags and not tags.intersection(config.include_tags):
            continue
        if config.exclude_tags and tags.intersection(config.exclude_tags):
            continue
        nodes.append(node)

    node_ids = {node["id"] for node in nodes}
    edges = []
    for edge in graph.get("edges", []):
        edge_type = str(edge.get("type", ""))
        confidence = str(edge.get("confidence", ""))
        if edge.get("source") not in node_ids or edge.get("target") not in node_ids:
            continue
        if not _passes_includes(edge_type, config.include_edge_types):
            continue
        if not _passes_excludes(edge_type, config.exclude_edge_types):
            continue
        if not _passes_includes(confidence, config.include_confidence):
            continue
        if not _passes_excludes(confidence, config.exclude_confidence):
            continue
        edges.append(edge)

    projected["nodes"] = nodes
    projected["edges"] = edges
    if annotate:
        projected.setdefault("source", {})
    if annotate and isinstance(projected["source"], dict):
        projected["source"]["projection"] = config.name
        projected["source"]["projection_schema"] = config.output_schema
        projected["source"]["flatteners"] = list(config.flatteners)
    return projected


def write_graph_projection(graph: dict[str, Any], out_path: Path, js_path: Path | None, config: ProjectionConfig) -> None:
    write_json(out_path, graph)
    if js_path is not None:
        write_js(js_path, config.js_global, graph)


def check_graph_projection(graph: dict[str, Any], out_path: Path, js_path: Path | None, config: ProjectionConfig) -> list[str]:
    errors: list[str] = []
    if out_path.exists():
        existing = __import__("json").loads(out_path.read_text())
        if normalized_for_compare(existing) != normalized_for_compare(graph):
            errors.append(f"{out_path} is stale; rerun generator")
    if js_path and js_path.exists():
        existing_js = load_js_value(js_path, config.js_global)
        if normalized_for_compare(existing_js) != normalized_for_compare(graph):
            errors.append(f"{js_path} is stale; rerun generator")
    return errors
