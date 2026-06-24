#!/usr/bin/env python3
"""Shared graph primitives for Farplane generated graph surfaces."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def utc_timestamp() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


@dataclass(frozen=True)
class GraphNode:
    id: str
    label: str
    kind: str = ""
    path: str = ""
    tags: tuple[str, ...] = ()
    attributes: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def as_dict(self, include_empty_kind: bool = False) -> dict[str, Any]:
        node: dict[str, Any] = {"id": self.id, "label": self.label}
        if self.kind or include_empty_kind:
            node["kind"] = self.kind
        if self.path:
            node["path"] = self.path
        if self.tags:
            node["tags"] = sorted(set(self.tags))
        node.update(self.attributes)
        if self.metadata:
            node["metadata"] = self.metadata
        return node


@dataclass(frozen=True)
class GraphEdge:
    source: str
    target: str
    type: str
    label: str = ""
    evidence_ref: str = ""
    confidence: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        edge: dict[str, Any] = {
            "source": self.source,
            "target": self.target,
            "type": self.type,
        }
        if self.label:
            edge["label"] = self.label
        if self.evidence_ref:
            edge["evidence_ref"] = self.evidence_ref
        if self.confidence:
            edge["confidence"] = self.confidence
        edge.update(self.metadata)
        return edge


@dataclass(frozen=True)
class GraphBundle:
    nodes: list[dict[str, Any]]
    edges: list[dict[str, Any]]
    schema_version: str = "1.0.0"
    generated_at: str = field(default_factory=utc_timestamp)
    counts: dict[str, Any] = field(default_factory=dict)
    extras: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        graph: dict[str, Any] = {
            "schema_version": self.schema_version,
            "generated_at": self.generated_at,
            "counts": self.counts,
            "nodes": self.nodes,
            "edges": self.edges,
        }
        graph.update(self.extras)
        return graph


def counter(values: list[str]) -> dict[str, int]:
    return dict(sorted(Counter(values).items()))


def edge_counts(edges: list[dict[str, Any]]) -> dict[str, int]:
    return counter([str(edge.get("type", "unknown")) for edge in edges])


def node_kind_counts(nodes: list[dict[str, Any]]) -> dict[str, int]:
    return counter([str(node.get("kind", "unknown")) for node in nodes])


def stable_node_key(node: dict[str, Any]) -> tuple[str, str]:
    return (str(node.get("kind", "")), str(node.get("label", node.get("id", ""))))


def stable_edge_key(edge: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        str(edge.get("source", "")),
        str(edge.get("target", "")),
        str(edge.get("type", "")),
        str(edge.get("label", edge.get("evidence_ref", edge.get("from_file", "")))),
    )


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def write_js(path: Path, global_name: str, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"window.{global_name} = " + json.dumps(value, indent=2, sort_keys=True) + ";\n")


def load_js_value(path: Path, global_name: str) -> dict[str, Any]:
    text = path.read_text()
    prefix = f"window.{global_name} = "
    if not text.startswith(prefix) or not text.endswith(";\n"):
        raise ValueError(f"{path} is not a {global_name} wrapper")
    return json.loads(text[len(prefix) : -2])


def normalized_for_compare(value: dict[str, Any]) -> dict[str, Any]:
    copy = json.loads(json.dumps(value))
    copy["generated_at"] = "<ignored>"
    return copy


def validate_edge_endpoints(graph: dict[str, Any]) -> list[str]:
    nodes = {node["id"] for node in graph.get("nodes", [])}
    errors: list[str] = []
    for edge in graph.get("edges", []):
        if edge.get("source") not in nodes:
            errors.append(f"missing source node for edge {edge}")
        if edge.get("target") not in nodes:
            errors.append(f"missing target node for edge {edge}")
    return errors
