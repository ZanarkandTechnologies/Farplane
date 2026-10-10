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
from graph_projection_config import GENERATED_GRAPH_ROOT, list_projection_configs


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
    def test_generated_skill_docs_do_not_embed_optional_ensemble_personas(self) -> None:
        repo_root = Path(__file__).resolve().parents[3]
        docs = generate_skill_graph.build_docs(
            [{"name": "advise", "path": str(repo_root / "skills" / "advise" / "SKILL.md")}]
        )
        advise = docs["skills"]["advise"]

        self.assertNotIn("ensemble", advise["frontmatter"])
        self.assertNotIn("operator-value", advise["frontmatter_raw"])

    def test_projection_defaults_use_ignored_runtime_graph_root(self) -> None:
        for config in list_projection_configs():
            self.assertTrue(config.default_out.startswith(f"{GENERATED_GRAPH_ROOT}/"))
            if config.default_js_out:
                self.assertTrue(config.default_js_out.startswith(f"{GENERATED_GRAPH_ROOT}/"))
            if config.docs_out:
                self.assertTrue(config.docs_out.startswith(f"{GENERATED_GRAPH_ROOT}/"))
            if config.docs_js_out:
                self.assertTrue(config.docs_js_out.startswith(f"{GENERATED_GRAPH_ROOT}/"))

    def test_todo_skill_refs_become_ordered_todo_chain_edges(self) -> None:
        rows = [
            {
                "name": "weekly-workflow",
                "source": "local",
                "department": "harness",
                "path": "skills/weekly-workflow/SKILL.md",
                "description": "Run a weekly workflow.",
                "has_checklist": True,
                "skill_links": [],
                "todo_skill_refs": ["horizon-advisor", "goal-advisor"],
            },
            {
                "name": "horizon-advisor",
                "source": "local",
                "department": "harness",
                "path": "skills/horizon-advisor/SKILL.md",
                "description": "Shape goals.",
                "has_checklist": True,
                "skill_links": [],
            },
            {
                "name": "goal-advisor",
                "source": "local",
                "department": "harness",
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

    def test_projects_capability_metadata(self) -> None:
        rows = [
            {
                "name": "meta-ads",
                "source": "local",
                "department": "marketing",
                "capability": {"kind": "integration", "consumes": ["ad-draft"]},
                "path": "skills/meta-ads/SKILL.md",
                "description": "Operate Meta ads.",
                "has_checklist": True,
                "skill_links": [],
            },
            {
                "name": "advise",
                "source": "local",
                "path": "skills/advise/SKILL.md",
                "description": "Give advice.",
                "has_checklist": True,
                "skill_links": [],
            },
        ]

        graph = generate_skill_graph.build_graph(rows)
        node = next(node for node in graph["nodes"] if node["id"] == "meta-ads")

        self.assertEqual(node["capability"], {"kind": "integration", "consumes": ["ad-draft"]})
        self.assertEqual(graph["counts"]["capabilities"], {"core": 1, "integration": 1})

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
                "source": "local",
                "department": "harness",
                "path": "skills/hot-caller/SKILL.md",
                "description": "Calls target skill.",
                "has_checklist": True,
                "eval": "evals/evals.json",
                "skill_links": ["target-skill"],
                "todo_skill_refs": ["target-skill"],
            },
            {
                "name": "target-skill",
                "source": "local",
                "department": "harness",
                "path": "skills/target-skill/SKILL.md",
                "description": "Receives refs.",
                "has_checklist": False,
                "eval": "evals/evals.json",
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
        self.assertEqual(signals["maintenance_recommendation"], "keep")

    def test_unique_orchestrator_without_heat_is_kept(self) -> None:
        rows = [
            {
                "name": "desk-primary",
                "specialist": "reporter",
                "source": "local",
                "department": "harness",
                "path": "skills/desk-primary/SKILL.md",
                "description": "Primitive skill.",
                "has_checklist": True,
                "skill_links": [],
            },
            {
                "name": "orchestrator",
                "source": "local",
                "department": "harness",
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

        self.assertEqual(recommendations["desk-primary"], "keep")
        self.assertEqual(recommendations["orchestrator"], "keep")


class CapabilityProjectionTests(unittest.TestCase):
    SPECIALISTS = {
        "social-manager": {
            "label": "Social Manager",
            "department": "marketing",
            "deliverable": "an approval-ready social post",
            "primary": "x-thread",
            "skills": ("x-thread", "x-account", "social-content"),
        },
        "content-producer": {
            "label": "Content Producer",
            "department": "marketing",
            "deliverable": "a content production ticket",
            "primary": "content-impl-plan",
            "skills": ("content-impl-plan",),
        },
    }

    def rows(self) -> list[dict]:
        return [
            {"name": "content-impl-plan", "department": "marketing", "_desk": "content-producer",
             "description": "Plan content.", "capability": {"kind": "artifact", "produces": ["content-brief"], "consumes": []}},
            {"name": "x-thread", "department": "marketing", "_desk": "social-manager",
             "description": "Create a review-ready X thread.",
             "capability": {"kind": "artifact", "consumes": ["content-brief"], "produces": ["x-thread-draft"]}},
            {"name": "x-account", "department": "marketing", "_desk": "social-manager",
             "description": "Operate X account boundaries.",
             "capability": {"kind": "integration", "consumes": ["x-thread-draft"]}},
            {"name": "social-content", "department": "marketing", "_desk": "social-manager",
             "description": "Plan social content."},
            {"name": "storyboard", "department": "marketing", "description": "Plan a storyboard."},
        ]

    def test_groups_skill_variants_into_specialist_desks(self) -> None:
        graph = generate_skill_graph.build_capability_graph(
            self.rows(), department_labels={"marketing": "Marketing"}, specialists=self.SPECIALISTS
        )
        nodes = {node["id"]: node for node in graph["nodes"]}
        desk = nodes["specialist:social-manager"]
        self.assertEqual(graph["schema_version"], "3.0.0")
        self.assertEqual(desk["kind"], "workstation")
        self.assertEqual(desk["label"], "Social Manager")
        self.assertEqual(desk["skill_id"], "x-thread")
        self.assertEqual(desk["skill_ids"], ["social-content", "x-account", "x-thread"])
        self.assertEqual(desk["capability"], {"consumes": ["content-brief"], "produces": ["x-thread-draft"]})
        self.assertEqual(nodes["skill:x-account"]["kind"], "facility")
        self.assertEqual(nodes["skill:x-account"]["specialist_id"], "social-manager")
        self.assertNotIn("skill:storyboard", nodes)
        self.assertEqual(graph["counts"]["node_kinds"], {"department": 1, "facility": 1, "workstation": 2})
        self.assertEqual(
            {(edge["source"], edge["target"], edge["type"]) for edge in graph["edges"]},
            {
                ("department:marketing", "specialist:content-producer", "member-of"),
                ("department:marketing", "specialist:social-manager", "member-of"),
                ("specialist:social-manager", "skill:x-account", "member-of"),
                ("specialist:content-producer", "specialist:social-manager", "artifact-flow"),
                ("specialist:social-manager", "skill:x-account", "artifact-flow"),
            },
        )

    def test_rejects_department_drift_and_unknown_members(self) -> None:
        rows = self.rows()
        rows[1]["department"] = "sales"
        with self.assertRaisesRegex(ValueError, "differs from specialist 'social-manager'"):
            generate_skill_graph.build_capability_graph(
                rows, department_labels={"marketing": "Marketing", "sales": "Sales"}, specialists=self.SPECIALISTS
            )
        specialists = {**self.SPECIALISTS, "ghost": {**self.SPECIALISTS["content-producer"], "primary": "missing", "skills": ("missing",)}}
        with self.assertRaisesRegex(ValueError, "specialist 'ghost' lists unknown skill 'missing'"):
            generate_skill_graph.build_capability_graph(
                self.rows(), department_labels={"marketing": "Marketing"}, specialists=specialists
            )

    def test_checked_in_specialists_project_every_desk(self) -> None:
        repo_root = Path(__file__).resolve().parents[3]
        departments = generate_skill_graph.load_skill_departments(repo_root)
        specialists = generate_skill_graph.load_skill_specialists(repo_root, departments)
        rows = generate_skill_graph.load_registry(repo_root / "docs/skills/registry.jsonl")
        graph = generate_skill_graph.build_capability_graph(
            rows, department_labels=departments, specialists=specialists
        )
        desks = {node["specialist_id"] for node in graph["nodes"] if node.get("kind") == "workstation"}
        self.assertEqual(desks, set(specialists))
        self.assertEqual(
            {node["department_id"] for node in graph["nodes"] if node.get("kind") == "department"},
            set(departments),
        )
        self.assertIn(
            ("specialist:social-manager", "skill:x-account", "artifact-flow"),
            {(edge["source"], edge["target"], edge["type"]) for edge in graph["edges"]},
        )


if __name__ == "__main__":
    unittest.main()
