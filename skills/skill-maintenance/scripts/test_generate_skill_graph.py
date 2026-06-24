#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_skill_graph


class GenerateSkillGraphTests(unittest.TestCase):
    def test_workflow_refs_become_ordered_workflow_chain_edges(self) -> None:
        rows = [
            {
                "name": "weekly-workflow",
                "tier": 3,
                "source": "local",
                "group": "harness",
                "path": "skills/weekly-workflow/SKILL.md",
                "description": "Run a weekly workflow.",
                "has_checklist": True,
                "skill_links": [],
                "workflow": True,
                "workflow_refs": ["horizon-advisor", "goal-advisor"],
            },
            {
                "name": "horizon-advisor",
                "tier": 3,
                "source": "local",
                "group": "harness",
                "path": "skills/horizon-advisor/SKILL.md",
                "description": "Shape goals.",
                "has_checklist": True,
                "skill_links": [],
            },
            {
                "name": "goal-advisor",
                "tier": 3,
                "source": "local",
                "group": "harness",
                "path": "skills/goal-advisor/SKILL.md",
                "description": "Compile goals.",
                "has_checklist": True,
                "skill_links": [],
            },
        ]

        graph = generate_skill_graph.build_graph(rows)
        edges = [
            edge
            for edge in graph["edges"]
            if edge["source"] == "weekly-workflow" and edge["type"] == "workflow-chain"
        ]
        edges = sorted(edges, key=lambda edge: edge["order"])

        self.assertEqual(
            [(edge["target"], edge["label"], edge["order"], edge["workflow_source"]) for edge in edges],
            [
                ("horizon-advisor", "workflow.todo.1", 1, "todo_list"),
                ("goal-advisor", "workflow.todo.2", 2, "todo_list"),
            ],
        )
        node = next(node for node in graph["nodes"] if node["id"] == "weekly-workflow")
        self.assertTrue(node["workflow"])
        self.assertEqual(node["workflow_refs"], ["horizon-advisor", "goal-advisor"])


if __name__ == "__main__":
    unittest.main()
