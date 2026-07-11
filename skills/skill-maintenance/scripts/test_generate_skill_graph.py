#!/usr/bin/env python3
from __future__ import annotations

import sys
import json
import os
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate_skill_graph


class EnvPatch:
    def __init__(self, **values: str) -> None:
        self.values = values
        self.previous: dict[str, str | None] = {}

    def __enter__(self) -> None:
        for key, value in self.values.items():
            self.previous[key] = os.environ.get(key)
            os.environ[key] = value

    def __exit__(self, *_args: object) -> None:
        for key, value in self.previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


class GenerateSkillGraphTests(unittest.TestCase):
    def test_todo_skill_refs_become_ordered_todo_chain_edges(self) -> None:
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
                "todo_skill_refs": ["horizon-advisor", "goal-advisor"],
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
            if edge["source"] == "weekly-workflow" and edge["type"] == "todo-chain"
        ]
        edges = sorted(edges, key=lambda edge: edge["order"])

        self.assertEqual(
            [(edge["target"], edge["label"], edge["order"], edge["chain_source"]) for edge in edges],
            [
                ("horizon-advisor", "todo.1", 1, "todo_list"),
                ("goal-advisor", "todo.2", 2, "todo_list"),
            ],
        )
        node = next(node for node in graph["nodes"] if node["id"] == "weekly-workflow")
        self.assertEqual(node["todo_skill_refs"], ["horizon-advisor", "goal-advisor"])

    def test_skill_heat_counts_distinct_invocations_from_events(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            event_dir = repo / ".farplane" / "events"
            event_dir.mkdir(parents=True)
            (event_dir / "2026-06-24.jsonl").write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "event_id": "evt-1",
                                "event_type": "skill_requested",
                                "skill_name": "goal-advisor",
                                "session_id": "sess-1",
                                "turn_id": "turn-1",
                                "timestamp": "2026-06-24T00:00:00Z",
                            }
                        ),
                        json.dumps(
                            {
                                "event_id": "evt-2",
                                "event_type": "control_surface_detected",
                                "skill_name": "goal-advisor",
                                "session_id": "sess-1",
                                "turn_id": "turn-1",
                                "timestamp": "2026-06-24T00:00:01Z",
                            }
                        ),
                        json.dumps(
                            {
                                "event_id": "evt-3",
                                "event_type": "skill_requested",
                                "skill_name": "impl-plan",
                                "session_id": "sess-2",
                                "ticket_id": "TASK-1",
                                "timestamp": "2026-06-20T00:00:00Z",
                            }
                        ),
                        json.dumps(
                            {
                                "event_id": "evt-4",
                                "event_type": "turn_start",
                                "skill_name": "impl-plan",
                                "session_id": "sess-2",
                                "ticket_id": "TASK-1",
                                "timestamp": "2026-06-20T00:00:01Z",
                            }
                        ),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            heat = generate_skill_graph.load_skill_heat(
                repo,
                {"goal-advisor", "impl-plan"},
                now=datetime(2026, 6, 24, tzinfo=UTC),
            )

        self.assertEqual(heat["goal-advisor"]["observed_event_count_all"], 2)
        self.assertEqual(heat["goal-advisor"]["invocation_count_window"], 1)
        self.assertEqual(heat["goal-advisor"]["distinct_threads_window"], 1)
        self.assertEqual(heat["impl-plan"]["observed_event_count_all"], 1)
        self.assertEqual(heat["impl-plan"]["invocation_count_window"], 1)
        self.assertEqual(heat["impl-plan"]["distinct_tickets_window"], 1)

    def test_skill_heat_config_reads_env_vars(self) -> None:
        with EnvPatch(
            FARPLANE_SKILL_HEAT_WINDOW_DAYS="14",
            FARPLANE_SKILL_HEAT_RECENT_DAYS="3",
            FARPLANE_SKILL_HEAT_TOP_N="12",
            FARPLANE_SKILL_HEAT_EVENT_TYPES="skill_requested,hook_result",
        ):
            config = generate_skill_graph.skill_heat_config_from_env()

        self.assertEqual(config["window_days"], 14)
        self.assertEqual(config["recent_days"], 3)
        self.assertEqual(config["default_top_n"], 12)
        self.assertEqual(config["event_types"], ["hook_result", "skill_requested"])

    def test_recent_window_is_capped_to_main_window(self) -> None:
        with EnvPatch(
            FARPLANE_SKILL_HEAT_WINDOW_DAYS="5",
            FARPLANE_SKILL_HEAT_RECENT_DAYS="20",
        ):
            config = generate_skill_graph.skill_heat_config_from_env()

        self.assertEqual(config["window_days"], 5)
        self.assertEqual(config["recent_days"], 5)

    def test_skill_signals_include_deduped_composition_heat(self) -> None:
        rows = [
            {
                "name": "hot-caller",
                "tier": 2,
                "source": "local",
                "group": "harness",
                "path": "skills/hot-caller/SKILL.md",
                "description": "Calls target skill.",
                "has_checklist": True,
                "eval": "evals/evals.json",
                "qa_checklist": "qa_checklist.md",
                "skill_links": ["target-skill"],
                "todo_skill_refs": ["target-skill"],
            },
            {
                "name": "target-skill",
                "tier": 3,
                "source": "local",
                "group": "harness",
                "path": "skills/target-skill/SKILL.md",
                "description": "Receives refs.",
                "has_checklist": False,
                "skill_links": [],
            },
        ]
        skill_heat = {
            "hot-caller": {
                "invocation_count_window": 4,
                "invocation_count_recent": 1,
                "distinct_threads_window": 2,
                "distinct_tickets_window": 1,
                "last_invoked_at": "2026-06-24T00:00:00Z",
            },
            "target-skill": {
                "invocation_count_window": 0,
                "invocation_count_recent": 0,
                "distinct_threads_window": 0,
                "distinct_tickets_window": 0,
                "last_invoked_at": "",
            },
        }

        graph = generate_skill_graph.build_graph(rows, skill_heat=skill_heat)
        target = next(node for node in graph["nodes"] if node["id"] == "target-skill")
        signals = target["signals"]

        self.assertEqual(signals["direct_heat"]["invocation_count_window"], 0)
        self.assertEqual(signals["composition_heat"]["incoming_ref_count"], 1)
        self.assertEqual(signals["composition_heat"]["hot_referrer_count"], 1)
        self.assertEqual(signals["composition_heat"]["window_referrer_invocations"], 4)
        self.assertEqual(signals["composition_heat"]["top_referrers"][0]["skill"], "hot-caller")
        self.assertEqual(signals["maintenance_recommendation"], "refine")

    def test_unique_orchestrator_without_heat_is_kept(self) -> None:
        rows = [
            {
                "name": "tier-one-primitive",
                "tier": 1,
                "source": "local",
                "group": "harness",
                "path": "skills/tier-one-primitive/SKILL.md",
                "description": "Primitive skill.",
                "has_checklist": True,
                "skill_links": [],
            },
            {
                "name": "orchestrator",
                "tier": 3,
                "source": "local",
                "group": "harness",
                "path": "skills/orchestrator/SKILL.md",
                "description": "Coordinates several skills.",
                "has_checklist": True,
                "skill_links": ["a", "b", "c"],
            },
        ]

        graph = generate_skill_graph.build_graph(rows)
        recommendations = {
            node["id"]: node["signals"]["maintenance_recommendation"]
            for node in graph["nodes"]
        }

        self.assertEqual(recommendations["tier-one-primitive"], "keep")
        self.assertEqual(recommendations["orchestrator"], "keep")


if __name__ == "__main__":
    unittest.main()
