"""Roles, goals, problems and resources on Wiki entity pages (farplane_entity_items)."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = ROOT / "bin" / "core"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))
TESTS_DIR = Path(__file__).resolve().parent
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from farplane_entities import build_crm_projection, build_entity_index, build_entity_registry, build_graph_projection
from test_farplane_entities import write_entity


class EntityItemTests(unittest.TestCase):
    def test_people_carry_roles_problems_and_resources_that_link_by_help(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(
                root / ".farplane/entities/hank.md",
                "id: hank\nkind: person\nname: Hank\nroles:\n  - client\n"
                "problems:\n  - id: leads\n    text: Needs commercial leads\n    since: 2026-09-23\n    ongoing: true\n",
            )
            write_entity(
                root / ".farplane/entities/kenji.md",
                "id: kenji\nkind: person\nname: Kenji\n"
                "resources:\n  - id: workflows\n    text: Agent-built workflows\n"
                "    helps:\n      - problem: hank#leads\n        impact: high\n",
            )
            registry = build_entity_registry(root)
            index = build_entity_index(registry)
            graph = build_graph_projection(registry, root)
            crm = build_crm_projection(registry, root)

        self.assertEqual(registry["issues"], [])
        hank = next(entry for entry in index["entities"] if entry["id"] == "hank")
        self.assertEqual(hank["roles"], ["client"])
        self.assertEqual(hank["problems"], [{
            "id": "leads", "text": "Needs commercial leads", "status": "open", "since": "2026-09-23", "ongoing": True,
        }])
        problem = next(node for node in graph["nodes"] if node["entity_id"] == "hank#leads")
        self.assertEqual((problem["kind"], problem["owner_entity_id"]), ("problem", "hank"))
        helps = [edge for edge in graph["edges"] if edge["kind"] == "helps"]
        self.assertEqual([(e["source_entity_id"], e["target_entity_id"], e["impact"], e["status"]) for e in helps],
                         [("kenji#workflows", "hank#leads", "high", "suggested")])
        self.assertEqual({e["target_entity_id"] for e in graph["edges"] if e["kind"] == "owns"}, {"hank#leads", "kenji#workflows"})
        self.assertEqual([entry["entity_id"] for entry in crm["entities"]], ["hank"])

    def test_reports_unresolved_helps_and_malformed_owner_items(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(
                root / ".farplane/entities/kenji.md",
                "id: kenji\nkind: person\nname: Kenji\nroles: client\n"
                "problems:\n  - id: a\n    text: A\n    status: stuck\n  - id: a\n    text: Again\n"
                "resources:\n  - id: r\n    text: R\n    helps:\n      - problem: nobody#x\n        impact: huge\n",
            )
            registry = build_entity_registry(root)

        reasons = sorted(issue["reason"] for issue in registry["issues"])
        self.assertEqual(reasons, [
            "duplicate_problems_id:a",
            "invalid_help_impact:r:nobody#x",
            "invalid_problem_status:a:stuck",
            "invalid_roles",
            "unresolved_ref:helps:nobody#x",
        ])

    def test_goals_carry_setups_and_validate_their_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(root / ".farplane/entities/kenji.md", "id: kenji\nkind: person\nname: Kenji")
            write_entity(
                root / ".farplane/entities/acme.md",
                "id: acme\nkind: company\nname: Acme\n"
                "goals:\n  - id: revenue\n    title: Recurring revenue\n    unit: USD/mo\n    target: 10000\n    deadline: 2026-12-31\n"
                "    setups:\n      - id: pilot\n        title: Pilot\n        owner: kenji\n        for: nobody\n        project: GlobexAI\n"
                "        steps:\n          - text: Kickoff\n            status: done\n          - text: Ship\n            status: later\n",
            )
            registry = build_entity_registry(root)
            index = build_entity_index(registry)

        reasons = sorted(issue["reason"] for issue in registry["issues"])
        self.assertEqual(reasons, ["invalid_step_status:revenue:pilot:later", "unresolved_ref:setup_for:nobody"])
        goal = next(entry for entry in index["entities"] if entry["id"] == "acme")["goals"][0]
        self.assertEqual((goal["title"], goal["target"], goal["deadline"]), ("Recurring revenue", 10000, "2026-12-31"))
        self.assertEqual([step["status"] for step in goal["setups"][0]["steps"]], ["done", "later"])
        self.assertEqual(goal["setups"][0]["project"], "GlobexAI")


if __name__ == "__main__":
    unittest.main()
