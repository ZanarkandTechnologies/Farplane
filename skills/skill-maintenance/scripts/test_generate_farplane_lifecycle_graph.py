#!/usr/bin/env python3
"""Tests for the Farplane lifecycle graph generator."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import farplane_lifecycle_graph as lifecycle_graph
from graph_projection import project_graph
from graph_projection_config import ProjectionConfig, get_projection_config, list_projection_configs


class LifecycleGraphTests(unittest.TestCase):
    def test_extracts_multiline_skill_signature(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            skill_dir = repo / "skills" / "sample-skill"
            skill_dir.mkdir(parents=True)
            skill = skill_dir / "SKILL.md"
            skill.write_text(
                """---
name: sample-skill
description: "Sample"
tier: 3
group: harness
source: local
---

# Sample Skill

## Skill Signature

```text
sample_skill(input) -> output

state:
  reads(farplane/goals.md?,
        tickets/TASK-*/ticket.md,
        docs/MEMORY.md?)
  writes(.farplane/reports/pulse/<YYYY-MM-DDTHHMMSSZ>.md,
         farplane/pm.json when worker threads are spawned)

gates:
  context_loaded; proof_recorded

routes:
  goal-advisor | review
```
"""
            )
            contract = lifecycle_graph.parse_skill_contract(skill, repo)

        self.assertEqual(contract.name, "sample-skill")
        self.assertIn("farplane/goals.md?", contract.reads)
        self.assertIn("tickets/TASK-*/ticket.md", contract.reads)
        self.assertIn(".farplane/reports/pulse/<YYYY-MM-DDTHHMMSSZ>.md", contract.writes)
        self.assertIn("farplane/pm.json when worker threads are spawned", contract.writes)
        self.assertEqual(contract.routes, ["goal-advisor", "review"])
        self.assertEqual(contract.gates, ["context_loaded", "proof_recorded"])

    def test_trims_multiline_gates(self) -> None:
        signature = """```text
state: reads(foo)
gates:
  first_gate; second_gate;
  third_gate
routes:
  caller-owned
```"""
        self.assertEqual(
            lifecycle_graph.extract_gates(signature),
            ["first_gate", "second_gate", "third_gate"],
        )

    def test_non_skill_routes_are_abstract_route_nodes(self) -> None:
        repo = Path(__file__).resolve().parents[3]
        direct = lifecycle_graph.route_target_node("direct-answer", repo)
        method = lifecycle_graph.route_target_node("research:gap", repo)
        self.assertEqual(direct["id"], "route:direct-answer")
        self.assertEqual(direct["kind"], "route")
        self.assertEqual(method["id"], "skill:research")
        self.assertEqual(method["kind"], "skill")

    def test_known_file_refs_ignore_prose_suffixes(self) -> None:
        node_id, kind, label, _tags = lifecycle_graph.canonical_ref("farplane/automations.md prompt updates")
        self.assertEqual(node_id, "file:farplane/automations.md")
        self.assertEqual(kind, "file")
        self.assertEqual(label, "Reviewed automation prompts")

    def test_ticket_refs_are_flattened(self) -> None:
        node_id, kind, _label, _tags = lifecycle_graph.canonical_ref("tickets/TASK-XXXX/artifacts/qa/<run>/report.md")
        self.assertEqual(node_id, "ticket:tickets/TASK-*/artifacts/")
        self.assertEqual(kind, "ticket")
        node_id, kind, _label, tags = lifecycle_graph.canonical_ref("tickets/progress/PM reports")
        self.assertEqual(node_id, "state:tickets/progress/pm-reports")
        self.assertEqual(kind, "state")
        self.assertIn("abstract-state", tags)

    def test_build_graph_contains_required_lifecycle_edges(self) -> None:
        repo = Path(__file__).resolve().parents[3]
        graph = lifecycle_graph.build_graph(repo)
        errors = lifecycle_graph.validate_graph(graph)
        self.assertEqual(errors, [])
        nodes = {node["id"] for node in graph["nodes"]}
        edges = {(edge["source"], edge["target"], edge["type"]) for edge in graph["edges"]}

        self.assertIn("skill:deep-init-project", nodes)
        self.assertIn("skill:horizon-advisor", nodes)
        self.assertIn("skill:goal-advisor", nodes)
        self.assertIn("hook:Stop", nodes)
        self.assertIn(("skill:goal-advisor", "ticket:tickets/TASK-*/program.md", "writes"), edges)
        self.assertIn(("automation:pulse", "skill:pulse-update", "triggers"), edges)
        self.assertIn(("automation:daily-interval", "skill:interval-update", "triggers"), edges)
        self.assertIn(("automation:weekly-interval", "skill:interval-update", "triggers"), edges)

    def test_core_graph_excludes_noisy_detail_nodes(self) -> None:
        repo = Path(__file__).resolve().parents[3]
        graph = lifecycle_graph.build_graph(repo)
        kinds = {node["kind"] for node in graph["nodes"]}
        self.assertNotIn("gate", kinds)
        self.assertNotIn("fsa_state", kinds)
        self.assertFalse(any("abstract-state" in node.get("tags", []) for node in graph["nodes"]))
        self.assertEqual(len(graph["fsa_projections"]), 4)

    def test_full_graph_can_include_noisy_detail_nodes(self) -> None:
        repo = Path(__file__).resolve().parents[3]
        graph = lifecycle_graph.build_graph(
            repo,
            include_gates=True,
            include_abstract_state=True,
            include_fsa_nodes=True,
        )
        kinds = {node["kind"] for node in graph["nodes"]}
        self.assertIn("gate", kinds)
        self.assertIn("fsa_state", kinds)
        self.assertTrue(any("abstract-state" in node.get("tags", []) for node in graph["nodes"]))

    def test_fsa_projection_shape(self) -> None:
        projections = lifecycle_graph.build_fsa_projections()
        by_id = {projection["id"]: projection for projection in projections}
        self.assertEqual(
            set(by_id),
            {
                "project_initialization",
                "automation_activation",
                "ticket_goal_execution",
                "memory_drain_upkeep",
            },
        )
        ticket = by_id["ticket_goal_execution"]
        self.assertEqual(ticket["start"], "fsa:ticket_goal_execution:ticket-selected")
        self.assertTrue(ticket["terminal"])
        self.assertEqual(len(ticket["transitions"]), len(ticket["states"]) - 1)

    def test_named_projection_configs_include_graph_surfaces(self) -> None:
        configs = {config.name: config for config in list_projection_configs()}
        self.assertEqual(
            set(configs),
            {
                "skill-registry",
                "harness-reference",
                "farplane-lifecycle-core",
                "farplane-lifecycle-full",
            },
        )
        self.assertEqual(get_projection_config("skill-registry").output_schema, "skill_graph")
        self.assertEqual(get_projection_config("harness-reference").output_schema, "harness_graph")
        self.assertEqual(get_projection_config("farplane-lifecycle-core").output_schema, "lifecycle_graph")
        full = get_projection_config("farplane-lifecycle-full")
        self.assertIn("gates", full.optional_nodes)
        self.assertIn("ticket_ids", full.flatteners)

    def test_generic_projection_filters_nodes_and_edges(self) -> None:
        graph = {
            "schema_version": "1.0.0",
            "generated_at": "ignored",
            "source": {},
            "counts": {},
            "nodes": [
                {"id": "skill:a", "kind": "skill", "label": "a", "tags": ["skill"]},
                {"id": "file:x", "kind": "file", "label": "x", "tags": ["file"]},
                {"id": "state:y", "kind": "state", "label": "y", "tags": ["abstract-state"]},
            ],
            "edges": [
                {"source": "skill:a", "target": "file:x", "type": "reads", "confidence": "parsed"},
                {"source": "skill:a", "target": "state:y", "type": "writes", "confidence": "parsed"},
            ],
        }
        config = ProjectionConfig(
            name="files-only",
            description="test",
            output_schema="test",
            default_out="unused.json",
            include_node_kinds=frozenset({"skill", "file"}),
            include_edge_types=frozenset({"reads"}),
        )
        projected = project_graph(graph, config, annotate=True)
        self.assertEqual({node["id"] for node in projected["nodes"]}, {"skill:a", "file:x"})
        self.assertEqual(
            [(edge["source"], edge["target"], edge["type"]) for edge in projected["edges"]],
            [("skill:a", "file:x", "reads")],
        )
        self.assertEqual(projected["source"]["projection"], "files-only")

    def test_temp_artifacts_match_fresh_generation(self) -> None:
        repo = Path(__file__).resolve().parents[3]
        graph = lifecycle_graph.build_graph(repo)
        with tempfile.TemporaryDirectory() as tmp:
            json_path = Path(tmp) / "farplane-lifecycle-graph.json"
            js_path = Path(tmp) / "farplane-lifecycle-graph.js"
            lifecycle_graph.write_json(json_path, graph)
            lifecycle_graph.write_js(js_path, "FARPLANE_LIFECYCLE_GRAPH", graph)
            existing_json = json.loads(json_path.read_text())
            existing_js = lifecycle_graph.load_js_value(js_path)
            self.assertEqual(
                lifecycle_graph.normalized_for_compare(existing_json),
                lifecycle_graph.normalized_for_compare(graph),
            )
            self.assertEqual(
                lifecycle_graph.normalized_for_compare(existing_js),
                lifecycle_graph.normalized_for_compare(graph),
            )


if __name__ == "__main__":
    unittest.main()
