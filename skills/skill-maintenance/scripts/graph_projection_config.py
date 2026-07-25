#!/usr/bin/env python3
"""Named projection profiles for Farplane graph generation."""

from __future__ import annotations

from dataclasses import dataclass, field


GENERATED_GRAPH_ROOT = ".farplane/generated/graphs"


def generated_graph_path(filename: str) -> str:
    return f"{GENERATED_GRAPH_ROOT}/{filename}"


@dataclass(frozen=True)
class ProjectionConfig:
    name: str
    description: str
    output_schema: str
    default_out: str
    default_js_out: str = ""
    js_global: str = ""
    docs_out: str = ""
    docs_js_out: str = ""
    docs_js_global: str = ""
    report_out: str = ""
    include_node_kinds: frozenset[str] = frozenset()
    exclude_node_kinds: frozenset[str] = frozenset()
    include_edge_types: frozenset[str] = frozenset()
    exclude_edge_types: frozenset[str] = frozenset()
    include_tags: frozenset[str] = frozenset()
    exclude_tags: frozenset[str] = frozenset()
    include_confidence: frozenset[str] = frozenset()
    exclude_confidence: frozenset[str] = frozenset()
    flatteners: tuple[str, ...] = ()
    optional_nodes: frozenset[str] = frozenset()
    metadata: dict[str, str] = field(default_factory=dict)


PROJECTION_CONFIGS: dict[str, ProjectionConfig] = {
    "skill-registry": ProjectionConfig(
        name="skill-registry",
        description="Skill registry graph and rendered skill docs.",
        output_schema="skill_graph",
        default_out=generated_graph_path("skill-graph.json"),
        default_js_out=generated_graph_path("skill-graph.js"),
        js_global="SKILL_GRAPH",
        docs_out=generated_graph_path("skill-docs.json"),
        docs_js_out=generated_graph_path("skill-docs.js"),
        docs_js_global="SKILL_DOCS",
        flatteners=("method_routes",),
    ),
    "harness-reference": ProjectionConfig(
        name="harness-reference",
        description="Repo-wide local-reference graph plus docs audit report.",
        output_schema="harness_graph",
        default_out=generated_graph_path("harness-graph.json"),
        default_js_out=generated_graph_path("harness-graph.js"),
        js_global="HARNESS_GRAPH",
        report_out="docs/doc-audit/generated/doc-reference-report.md",
    ),
    "farplane-framework-core": ProjectionConfig(
        name="farplane-framework-core",
        description="Manifest-backed Farplane framework core graph.",
        output_schema="framework_core_graph",
        default_out=generated_graph_path("farplane-framework-core-graph.json"),
        default_js_out=generated_graph_path("farplane-framework-core-graph.js"),
        js_global="FARPLANE_FRAMEWORK_CORE_GRAPH",
    ),
    "farplane-lifecycle-core": ProjectionConfig(
        name="farplane-lifecycle-core",
        description="Compact Farplane lifecycle graph for UI and agent context.",
        output_schema="lifecycle_graph",
        default_out=generated_graph_path("farplane-lifecycle-graph.json"),
        default_js_out=generated_graph_path("farplane-lifecycle-graph.js"),
        js_global="FARPLANE_LIFECYCLE_GRAPH",
        flatteners=("ticket_ids", "timestamped_reports", "method_routes"),
    ),
    "farplane-lifecycle-full": ProjectionConfig(
        name="farplane-lifecycle-full",
        description="Audit lifecycle graph with gates, abstract state, and FSA state nodes.",
        output_schema="lifecycle_graph",
        default_out=generated_graph_path("farplane-lifecycle-graph.json"),
        default_js_out=generated_graph_path("farplane-lifecycle-graph.js"),
        js_global="FARPLANE_LIFECYCLE_GRAPH",
        flatteners=("ticket_ids", "timestamped_reports", "method_routes"),
        optional_nodes=frozenset({"gates", "abstract_state", "fsa_state_nodes"}),
    ),
}


def get_projection_config(name: str) -> ProjectionConfig:
    try:
        return PROJECTION_CONFIGS[name]
    except KeyError as error:
        known = ", ".join(sorted(PROJECTION_CONFIGS))
        raise ValueError(f"unknown projection {name!r}; expected one of: {known}") from error


def list_projection_configs() -> list[ProjectionConfig]:
    return [PROJECTION_CONFIGS[name] for name in sorted(PROJECTION_CONFIGS)]
