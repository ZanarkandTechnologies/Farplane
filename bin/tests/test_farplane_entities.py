from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = ROOT / "bin" / "core"
CLI = ROOT / "bin" / "farplane.py"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from farplane_entities import (
    body_claims,
    build_crm_projection,
    build_entity_index,
    build_entity_registry,
    build_view_projections,
    build_graph_projection,
    project_identity,
)


def write_entity(path: Path, frontmatter: str, body: str = "# Notes\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\n{frontmatter.strip()}\n---\n\n{body}", encoding="utf-8")


def write_views(root: Path, content: str) -> None:
    path = root / ".farplane/views.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class FarplaneEntityTests(unittest.TestCase):
    def test_compiles_named_views_into_all_projections_and_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(
                root / ".farplane/entities/acme.md",
                "id: acme\nkind: company\nname: Acme\nfunnel:\n  stage: researching",
            )
            write_entity(
                root / ".farplane/entities/supplier.md",
                "id: supplier\nkind: company\nname: Supplier",
            )
            write_views(
                root,
                "views:\n"
                "  supply-chain:\n"
                "    name: Supply Chain\n"
                "    entity_ids:\n"
                "      - supplier\n"
                "      - acme\n",
            )
            index = build_entity_registry(root)
            graph = build_graph_projection(index, root)
            crm = build_crm_projection(index, root)

        expected = [
            {
                "id": "supply-chain",
                "name": "Supply Chain",
                "entity_ids": ["supplier", "acme"],
            }
        ]
        self.assertEqual(index["views"], expected)
        self.assertEqual(graph["views"], expected)
        self.assertNotIn("views", crm)
        self.assertEqual(
            {index["source_fingerprint"], graph["source_fingerprint"], crm["source_fingerprint"]},
            {index["source_fingerprint"]},
        )

    def test_absent_view_config_compiles_as_no_views(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(root / ".farplane/entities/acme.md", "id: acme\nkind: company\nname: Acme")
            index = build_entity_registry(root)

        self.assertEqual(index["views"], [])
        self.assertNotIn("views_by_id", index)
        self.assertEqual(index["issues"], [])

    def test_view_changes_invalidate_projection_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(root / ".farplane/entities/acme.md", "id: acme\nkind: company\nname: Acme")
            write_entity(root / ".farplane/entities/other.md", "id: other\nkind: company\nname: Other")
            write_views(root, "views:\n  focus:\n    name: Focus\n    entity_ids: [acme]\n")
            first = build_entity_registry(root)
            write_views(root, "views:\n  focus:\n    name: Focus\n    entity_ids: [other]\n")
            second = build_entity_registry(root)

        self.assertNotEqual(first["source_fingerprint"], second["source_fingerprint"])

    def test_reports_invalid_duplicate_and_unresolved_view_membership(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(root / ".farplane/entities/acme.md", "id: acme\nkind: company\nname: Acme")
            write_views(
                root,
                "views:\n"
                "  focus:\n"
                "    name: Focus\n"
                "    entity_ids: [acme, acme, missing]\n"
                "  empty:\n"
                "    name: Empty\n"
                "    entity_ids: []\n",
            )
            index = build_entity_registry(root)
            result = subprocess.run(
                [sys.executable, str(CLI), "wiki", "rebuild", "--project-root", str(root), "--no-write"],
                capture_output=True,
                text=True,
                check=False,
            )

        reasons = {issue["reason"] for issue in index["issues"]}
        self.assertIn("invalid_view:focus:duplicate_entity_id:acme", reasons)
        self.assertIn("invalid_view:focus:unresolved_entity_id:missing", reasons)
        self.assertIn("invalid_view:empty:empty_entity_ids", reasons)
        self.assertEqual(index["views"], [])
        self.assertEqual(result.returncode, 1)
        self.assertIn("invalid_view:focus:duplicate_entity_id:acme", result.stderr)

    def test_rejects_duplicate_yaml_view_keys_before_they_collapse(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(root / ".farplane/entities/acme.md", "id: acme\nkind: company\nname: Acme")
            write_views(
                root,
                "views:\n"
                "  focus:\n"
                "    name: First\n"
                "    entity_ids: [acme]\n"
                "  focus:\n"
                "    name: Second\n"
                "    entity_ids: [acme]\n",
            )
            index = build_entity_registry(root)
            result = subprocess.run(
                [sys.executable, str(CLI), "wiki", "rebuild", "--project-root", str(root), "--no-write"],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(index["views"], [])
        self.assertEqual(index["issues"], [{"path": ".farplane/views.yaml", "reason": "invalid_views_yaml:duplicate_key"}])
        self.assertEqual(result.returncode, 1)

    def test_reports_malformed_view_shapes_and_non_string_ids(self) -> None:
        cases = (
            ("[]\n", "views_config_not_object"),
            ("views: []\n", "views_not_object"),
            ("views:\n  1:\n    name: Numeric\n    entity_ids: [acme]\n", "invalid_view_id:1"),
            ("views:\n  focus:\n    entity_ids: [acme]\n", "invalid_view:focus:missing_name"),
            (
                "views:\n  focus:\n    name: Focus\n    entity_ids: acme\n",
                "invalid_view:focus:entity_ids_not_list",
            ),
            (
                "views:\n  focus:\n    name: Focus\n    entity_ids: [1]\n",
                "invalid_view:focus:invalid_entity_id:1",
            ),
        )
        for config, expected_reason in cases:
            with self.subTest(expected_reason=expected_reason), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                write_entity(root / ".farplane/entities/acme.md", "id: acme\nkind: company\nname: Acme")
                write_views(root, config)
                index = build_entity_registry(root)

            self.assertIn(expected_reason, {issue["reason"] for issue in index["issues"]})
            self.assertEqual(index["views"], [])

    def test_internal_registry_preserves_markdown_for_projection_compilation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(root / ".farplane/entities/acme.md", "id: acme\nkind: company\nname: Acme")
            write_entity(
                root / ".farplane/entities/jane.md",
                "id: jane\nkind: person\nname: Jane\ncompany_ref: acme\nstatus: researching",
                "# Jane\n\nPrefers concrete demos.\n",
            )
            registry = build_entity_registry(root)

        self.assertEqual(registry["counts"], {"included": 2, "excluded": 0, "issues": 0})
        self.assertIn("Prefers concrete demos", registry["by_id"]["jane"]["body"])
        self.assertEqual(registry["by_id"]["jane"]["frontmatter"]["company_ref"], "acme")

    def test_index_contains_only_bounded_search_and_routing_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(
                root / ".farplane/entities/acme.md",
                "id: acme\nkind: company\nname: Acme",
            )
            write_entity(
                root / ".farplane/entities/jane.md",
                "id: jane\n"
                "kind: person\n"
                "name: Jane Doe\n"
                "aliases: [J. Doe, Jane]\n"
                "location: Kuala Lumpur, Malaysia\n"
                "company_ref: acme\n"
                "entity_refs: [acme]\n"
                "status: researching\n"
                "metadata:\n  private_note: do not duplicate\n"
                "funnel:\n  stage: researched",
                "# Jane\n\nFull canonical prose remains in this file. [^q-20260802-01]\n\n"
                "[^q-20260802-01]: Who is Jane?\n",
            )
            registry = build_entity_registry(root)
            index = build_entity_index(registry)

        self.assertEqual(
            set(index),
            {"schema_version", "source_fingerprint", "entities"},
        )
        self.assertEqual(index["schema_version"], 5)
        jane = next(entry for entry in index["entities"] if entry["id"] == "jane")
        self.assertEqual(
            jane,
            {
                "id": "jane",
                "kind": "person",
                "name": "Jane Doe",
                "path": ".farplane/entities/jane.md",
                "aliases": ["J. Doe", "Jane"],
                "location": "Kuala Lumpur, Malaysia",
                "company_ref": "acme",
                "entity_refs": ["acme"],
                "question_refs": ["q-20260802-01"],
            },
        )
        serialized = json.dumps(index)
        self.assertNotIn("Full canonical prose", serialized)
        self.assertNotIn("private_note", serialized)
        self.assertNotIn("funnel", serialized)
        self.assertNotIn("frontmatter", serialized)
        self.assertNotIn("body", serialized)

    def test_reports_invalid_mismatched_and_unresolved_entities(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entity_root = root / ".farplane/entities"
            write_entity(entity_root / "jane.md", "id: jane\nkind: person\nname: Jane\ncompany_ref: missing")
            write_entity(entity_root / "wrong-name.md", "id: other\nkind: person\nname: Other")
            write_entity(entity_root / "bad.md", "id: Bad ID\nkind: person\nname: Bad")
            write_entity(entity_root / "missing.md", "kind: person\nname: Missing")
            (entity_root / "no-frontmatter.md").write_text("# Nope\n", encoding="utf-8")
            registry = build_entity_registry(root)

        reasons = {issue["reason"] for issue in registry["issues"]}
        self.assertIn("filename_id_mismatch:wrong-name:other", reasons)
        self.assertIn("invalid_id", reasons)
        self.assertIn("missing_required:id", reasons)
        self.assertIn("missing_frontmatter", reasons)
        self.assertIn("unresolved_ref:company_ref:missing", reasons)
        self.assertEqual(registry["counts"], {"included": 1, "excluded": 4, "issues": 5})

    def test_registry_is_deterministic_for_identical_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(root / ".farplane/entities/jane.md", "id: jane\nkind: person\nname: Jane")
            first = build_entity_registry(root)
            second = build_entity_registry(root)

        self.assertEqual(first, second)

    def test_cli_writes_lookup_index_and_graph_projections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(root / ".farplane/entities/design-partner.md", "id: design-partner\nkind: opportunity\nname: Design Partner")
            write_views(
                root,
                "views:\n  pipeline:\n    name: Pipeline\n    entity_ids: [design-partner]\n",
            )
            result = subprocess.run(
                [sys.executable, str(CLI), "wiki", "rebuild", "--project-root", str(root), "--json"],
                capture_output=True,
                text=True,
                check=False,
            )
            written = json.loads((root / ".farplane/entities/index.json").read_text(encoding="utf-8"))
            graph = json.loads((root / ".farplane/entities/graph.json").read_text(encoding="utf-8"))
            crm = json.loads((root / ".farplane/entities/crm.json").read_text(encoding="utf-8"))
            payload = json.loads(result.stdout)

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(written["schema_version"], 5)
        self.assertEqual(graph["schema_version"], 4)
        self.assertEqual(crm["schema_version"], 4)
        self.assertEqual(written["entities"][0]["id"], "design-partner")
        self.assertEqual(graph["nodes"][0]["key"], f"{project_identity(root)['id']}:design-partner")
        self.assertEqual(crm["entities"], [])
        self.assertEqual(graph["views"][0]["entity_ids"], ["design-partner"])
        self.assertEqual(payload["diagnostics"]["counts"], {"included": 1, "excluded": 0, "issues": 0})
        self.assertEqual(payload["diagnostics"]["issues"], [])
        self.assertEqual(payload["diagnostics"]["view_issue_count"], 0)
        self.assertNotIn("views", written)
        self.assertNotIn("by_id", written)
        self.assertNotIn("counts", written)
        self.assertNotIn("issues", written)
        self.assertNotIn("counts", graph)
        self.assertNotIn("issues", graph)
        self.assertNotIn("frontmatter", graph["nodes"][0])
        self.assertNotIn("metadata", graph["nodes"][0])
        self.assertNotIn("by_id", crm)
        self.assertNotIn("views", crm)
        self.assertNotIn("counts", crm)
        self.assertNotIn("issues", crm)
        self.assertNotIn("body", written["entities"][0])
        self.assertNotIn("frontmatter", written["entities"][0])
        self.assertEqual(
            {written["source_fingerprint"], graph["source_fingerprint"], crm["source_fingerprint"]},
            {written["source_fingerprint"]},
        )

    def test_cli_removes_stale_typed_view_projection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(
                root / ".farplane/entities/acme.md",
                "id: acme\nkind: company\nname: Acme",
            )
            write_views(
                root,
                "views:\n  old-view:\n    name: Old View\n    entity_ids: [acme]\n",
            )
            first = subprocess.run(
                [sys.executable, str(CLI), "wiki", "rebuild", "--project-root", str(root)],
                capture_output=True,
                text=True,
                check=False,
            )
            stale_path = root / ".farplane/views/old-view.json"
            self.assertEqual(first.returncode, 0, first.stderr + first.stdout)
            self.assertTrue(stale_path.exists())

            write_views(root, "views: {}\n")
            second = subprocess.run(
                [sys.executable, str(CLI), "wiki", "rebuild", "--project-root", str(root)],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(second.returncode, 0, second.stderr + second.stdout)
            self.assertFalse(stale_path.exists())

    def test_crm_projection_contains_only_entities_with_funnel_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(
                root / ".farplane/entities/prospect.md",
                "id: prospect\nkind: company\nname: Prospect\nfunnel:\n  stage: researched\n  status: active",
            )
            write_entity(root / ".farplane/entities/indicator.md", "id: indicator\nkind: market-indicator\nname: Indicator")
            index = build_entity_registry(root)
            crm = build_crm_projection(index, root)

        self.assertEqual(index["issues"], [])
        self.assertEqual(set(crm), {"schema_version", "source_fingerprint", "project", "entities"})
        self.assertEqual(len(crm["entities"]), 1)
        self.assertEqual(crm["entities"][0]["funnel"]["stage"], "researched")
        self.assertNotIn("frontmatter", crm["entities"][0])

    def test_reports_non_object_funnel_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(
                root / ".farplane/entities/prospect.md",
                "id: prospect\nkind: company\nname: Prospect\nfunnel: researching",
            )
            index = build_entity_registry(root)
            crm = build_crm_projection(index, root)

        self.assertEqual(index["issues"][0]["reason"], "invalid_funnel:not_object")
        self.assertEqual(crm["entities"], [])

    def test_rejects_nested_entity_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(root / ".farplane/entities/companies/acme.md", "id: acme\nkind: company\nname: Acme")
            index = build_entity_registry(root)

        self.assertEqual(index["counts"], {"included": 0, "excluded": 1, "issues": 1})
        self.assertEqual(index["issues"][0]["reason"], "nested_entity_path")

    def test_builds_project_qualified_nodes_and_sentence_backed_edges(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir(parents=True)
            (root / "farplane/manifest.json").write_text(
                json.dumps({"project": {"id": "supply-lab", "name": "Supply Lab"}}),
                encoding="utf-8",
            )
            write_entity(
                root / ".farplane/entities/acme.md",
                "id: acme\nkind: company\nname: Acme Motors\nlocation: Detroit, USA\nlatitude: 42.3314\nlongitude: -83.0458",
            )
            write_entity(
                root / ".farplane/entities/castings.md",
                "id: castings\nkind: company\nname: Penang Castings\naliases:\n  - PC Manufacturing\nlocation: Penang, Malaysia",
                "# Penang Castings\n\n## Relationships\n\n- Supplies aluminum housings to [Acme Motors](entity:acme) from its Penang facility. "
                "The relationship is under review. Source: "
                "[contract](https://example.com/contract).\n",
            )
            registry = build_entity_registry(root)
            first = build_graph_projection(registry, root)
            second = build_graph_projection(registry, root)

        self.assertEqual(first, second)
        self.assertEqual(
            first["project"],
            {"project_id": "supply-lab", "name": "Supply Lab", "identity_source": "manifest"},
        )
        self.assertEqual(first["source_fingerprint"], registry["source_fingerprint"])
        self.assertNotIn("counts", first)
        self.assertNotIn("issues", first)
        self.assertEqual(first["nodes"][0]["key"], "supply-lab:acme")
        self.assertNotIn("frontmatter", first["nodes"][0])
        self.assertNotIn("metadata", first["nodes"][0])
        self.assertNotIn("latitude", first["nodes"][1])
        edge = first["edges"][0]
        self.assertTrue(edge["key"].startswith("supply-lab:association:"))
        self.assertFalse(edge["directed"])
        self.assertEqual(edge["source_key"], "supply-lab:castings")
        self.assertEqual(edge["target_key"], "supply-lab:acme")
        self.assertEqual(edge["section"], "Relationships")
        self.assertEqual(
            edge["context"],
            "Supplies aluminum housings to [Acme Motors](entity:acme) from its Penang facility.",
        )
        self.assertEqual(
            edge["display_context"],
            "Supplies aluminum housings to Acme Motors from its Penang facility.",
        )
        self.assertEqual(edge["source_urls"], ["https://example.com/contract"])
        self.assertNotIn("body", first["nodes"][0])

    def test_compiles_tagged_timeline_bullets_without_creating_nodes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir(parents=True)
            (root / "farplane/manifest.json").write_text(
                json.dumps({"project": {"id": "ai-market", "name": "AI Market"}}),
                encoding="utf-8",
            )
            write_entity(
                root / ".farplane/entities/nvidia.md",
                "id: nvidia\nkind: company\nname: NVIDIA",
                "# NVIDIA\n\n## Timeline\n\n"
                "- 2026-03-11 [type:investment] [factor:capital] [factor:chips] "
                "[signal:bubble-risk-up] [metric:stake] [value:9.3] [unit:percent] "
                "NVIDIA reported a stake in [Nebius](entity:nebius). "
                "Source: [SEC filing](https://example.com/sec).\n"
                "- 2026-01-01 [type:capacity] [factor:power] "
                "[signal:feasibility-up] NVIDIA expanded AI capacity.\n\n"
                "## Notes\n\n- 2025-01-01 [type:ignored] This is not timeline data.\n",
            )
            write_entity(
                root / ".farplane/entities/nebius.md",
                "id: nebius\nkind: company\nname: Nebius",
            )
            registry = build_entity_registry(root)
            graph = build_graph_projection(registry, root)

        self.assertEqual(len(graph["nodes"]), 2)
        self.assertEqual(len(graph["timeline"]), 2)
        latest = graph["timeline"][0]
        self.assertEqual(latest["date"], "2026-03-11")
        self.assertEqual(latest["source_entity_id"], "nvidia")
        self.assertEqual(latest["entity_ids"], ["nebius", "nvidia"])
        self.assertEqual(latest["entity_keys"], ["ai-market:nebius", "ai-market:nvidia"])
        self.assertEqual(latest["tags"]["factor"], ["capital", "chips"])
        self.assertEqual(latest["tags"]["value"], ["9.3"])
        self.assertNotIn("[type:", latest["display_context"])
        self.assertIn("NVIDIA reported a stake in Nebius", latest["display_context"])
        self.assertIn("Source: SEC filing", latest["display_context"])

    def test_timeline_item_stops_before_trailing_document_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(
                root / ".farplane/entities/acme.md",
                "id: acme\nkind: company\nname: Acme",
                "# Acme\n\n## Timeline\n\n"
                "- 2026-01-02 [type:milestone]\n"
                "  Acme demonstrated a prototype. [^q-proof]\n\n"
                "A separate paragraph must not join the event.\n\n"
                "[^q-proof]: What evidence supports the prototype?\n\n"
                "```text\n[type:incorrect] fenced content\n```\n",
            )
            registry = build_entity_registry(root)
            graph = build_graph_projection(registry, root)

        self.assertEqual(len(graph["timeline"]), 1)
        entry = graph["timeline"][0]
        self.assertEqual(entry["tags"], {"type": ["milestone"]})
        self.assertEqual(entry["question_refs"], ["q-proof"])
        self.assertNotIn("separate paragraph", entry["context"])
        self.assertNotIn("fenced content", entry["context"])

    def test_compiles_view_sections_and_inline_tags_into_typed_view(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(
                root / ".farplane/entities/acme.md",
                "id: acme\nkind: company\nname: Acme",
                "# Acme\n\n## View: AI Market\n\n"
                "### Latest Status\n\n"
                "_As of 2026-01-03_\n\n"
                "[role:financier] Acme is funding grid capacity.\n\n"
                "### Timeline\n\n"
                "- 2026-01-02 [relation:investment] [status:announced] "
                "[confidence:primary] [signal:feasibility-up] "
                "[ownership:9.3 percent] [capital-supply:2 USD-billion] "
                "Acme committed capital to [GridCo](entity:gridco). "
                "Source: [filing](https://example.com/filing).\n",
            )
            write_entity(
                root / ".farplane/entities/gridco.md",
                "id: gridco\nkind: company\nname: GridCo",
            )
            write_views(
                root,
                "views:\n"
                "  ai-market:\n"
                "    name: AI Market\n"
                "    entity_ids: [acme, gridco]\n"
                "    resources:\n"
                "      capital:\n"
                "        name: Capital\n"
                "        measure: flow\n"
                "        base_unit: USD-billion\n"
                "        units:\n"
                "          USD-billion: 1\n"
                "          USD-million: 0.001\n"
                "    problems:\n"
                "      financing:\n"
                "        name: Financing\n"
                "        resources: [capital]\n"
                "    resource_tags:\n"
                "      capital-supply:\n"
                "        resource: capital\n"
                "        direction: supply\n"
                "        entity: source\n"
                "        transfer: source-to-linked\n"
                "    metric_tags:\n"
                "      ownership:\n"
                "        unit: percent\n"
                "    status_weights:\n"
                "      announced: 0.5\n"
                "    confidence_weights:\n"
                "      primary: 0.8\n",
            )
            registry = build_entity_registry(root)
            graph = build_graph_projection(registry, root)
            projection = build_view_projections(registry, graph)["ai-market"]

        self.assertEqual(registry["issues"], [])
        self.assertEqual(registry["view_statuses"][0]["as_of"], "2026-01-03")
        self.assertEqual(registry["view_statuses"][0]["tags"]["role"], ["financier"])
        self.assertEqual(graph["timeline"][0]["view_name"], "AI Market")
        self.assertEqual(projection["counts"], {
            "entities": 2,
            "edges": 1,
            "events": 1,
            "observations": 1,
            "resource_flows": 1,
            "issues": 0,
        })
        self.assertEqual(projection["schema_version"], 4)
        observation = projection["observations"][0]
        self.assertEqual(observation["normalized_value"], 2.0)
        self.assertEqual(observation["weighted_value"], 0.8)
        self.assertEqual(projection["resource_summaries"][0]["supply"], 0.8)
        self.assertEqual(projection["events"][0]["metrics"][0]["key"], "ownership")
        self.assertEqual(projection["entities"][0]["view_status"]["as_of"], "2026-01-03")
        relationship = projection["relationships"][0]
        self.assertFalse(relationship["directed"])
        self.assertEqual(relationship["relation_types"], ["investment"])
        self.assertEqual(relationship["resource_ids"], ["capital"])
        self.assertEqual(relationship["event_count"], 1)
        flow = projection["resource_flows"][0]
        self.assertEqual(flow["from_entity_id"], "acme")
        self.assertEqual(flow["to_entity_id"], "gridco")
        self.assertEqual(flow["value"], 2.0)
        self.assertEqual(flow["unit"], "USD-billion")
        self.assertEqual(flow["source_urls"], ["https://example.com/filing"])
        self.assertEqual(relationship["resource_flows"], [flow])
        self.assertEqual(relationship["timeline"][0]["resource_flows"], [flow])
        self.assertEqual(relationship["timeline"][0]["date"], "2026-01-02")
        self.assertEqual(
            relationship["timeline"][0]["source_urls"],
            ["https://example.com/filing"],
        )

    def test_resource_observation_without_transfer_stays_a_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(
                root / ".farplane/entities/acme.md",
                "id: acme\nkind: company\nname: Acme",
                "# Acme\n\n## View: AI Market\n\n### Timeline\n\n"
                "- 2026-01-02 [power-demand:5 GW] Acme needs power from "
                "[GridCo](entity:gridco).\n",
            )
            write_entity(
                root / ".farplane/entities/gridco.md",
                "id: gridco\nkind: company\nname: GridCo",
            )
            write_views(
                root,
                "views:\n"
                "  ai-market:\n"
                "    name: AI Market\n"
                "    entity_ids: [acme, gridco]\n"
                "    resources:\n"
                "      power:\n"
                "        name: Power\n"
                "        base_unit: GW\n"
                "        units: {GW: 1}\n"
                "    resource_tags:\n"
                "      power-demand:\n"
                "        resource: power\n"
                "        direction: demand\n"
                "        entity: source\n",
            )
            registry = build_entity_registry(root)
            graph = build_graph_projection(registry, root)
            projection = build_view_projections(registry, graph)["ai-market"]

        self.assertEqual(projection["counts"]["observations"], 1)
        self.assertEqual(projection["counts"]["resource_flows"], 0)
        self.assertEqual(projection["resource_flows"], [])
        self.assertEqual(projection["relationships"][0]["resource_ids"], ["power"])
        self.assertEqual(projection["relationships"][0]["resource_flows"], [])

    def test_resource_transfer_supports_linked_to_source_direction(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(
                root / ".farplane/entities/acme.md",
                "id: acme\nkind: company\nname: Acme",
                "# Acme\n\n## View: AI Market\n\n### Timeline\n\n"
                "- 2026-01-02 [capital-received:2 USD-billion] Acme received capital from "
                "[GridCo](entity:gridco).\n",
            )
            write_entity(
                root / ".farplane/entities/gridco.md",
                "id: gridco\nkind: company\nname: GridCo",
            )
            write_views(
                root,
                "views:\n"
                "  ai-market:\n"
                "    name: AI Market\n"
                "    entity_ids: [acme, gridco]\n"
                "    resources:\n"
                "      capital:\n"
                "        name: Capital\n"
                "        base_unit: USD-billion\n"
                "        units: {USD-billion: 1}\n"
                "    resource_tags:\n"
                "      capital-received:\n"
                "        resource: capital\n"
                "        direction: demand\n"
                "        entity: source\n"
                "        transfer: linked-to-source\n",
            )
            registry = build_entity_registry(root)
            graph = build_graph_projection(registry, root)
            projection = build_view_projections(registry, graph)["ai-market"]

        flow = projection["resource_flows"][0]
        self.assertEqual(flow["from_entity_id"], "gridco")
        self.assertEqual(flow["to_entity_id"], "acme")

    def test_typed_view_reports_invalid_resource_observation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(
                root / ".farplane/entities/acme.md",
                "id: acme\nkind: company\nname: Acme",
                "# Acme\n\n## View: AI Market\n\n### Timeline\n\n"
                "- 2026-01-02 [status:announced] [confidence:primary] "
                "[power-demand:5 bananas] Acme announced capacity.\n",
            )
            write_views(
                root,
                "views:\n"
                "  ai-market:\n"
                "    name: AI Market\n"
                "    entity_ids: [acme]\n"
                "    resources:\n"
                "      power:\n"
                "        name: Power\n"
                "        base_unit: GW\n"
                "        units: {GW: 1}\n"
                "    resource_tags:\n"
                "      power-demand:\n"
                "        resource: power\n"
                "        direction: demand\n"
                "        entity: source\n"
                "    status_weights: {announced: 0.5}\n"
                "    confidence_weights: {primary: 1}\n",
            )
            registry = build_entity_registry(root)
            graph = build_graph_projection(registry, root)
            projection = build_view_projections(registry, graph)["ai-market"]

        self.assertEqual(projection["counts"]["observations"], 0)
        self.assertEqual(projection["counts"]["issues"], 1)
        self.assertIn(
            "invalid_resource_unit:power-demand:bananas",
            projection["issues"][0]["reason"],
        )

    def test_relationship_bundles_both_authored_directions_newest_first(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(
                root / ".farplane/entities/acme.md",
                "id: acme\nkind: company\nname: Acme",
                "# Acme\n\n## View: AI Market\n\n### Timeline\n\n"
                "- 2026-01-02 [relation:investment] Acme invested in "
                "[GridCo](entity:gridco). Source: [filing](https://example.com/acme).\n",
            )
            write_entity(
                root / ".farplane/entities/gridco.md",
                "id: gridco\nkind: company\nname: GridCo",
                "# GridCo\n\n## View: AI Market\n\n### Timeline\n\n"
                "- 2026-02-03 [relation:contract] GridCo signed a contract with "
                "[Acme](entity:acme). Source: [award](https://example.com/gridco).\n",
            )
            write_views(
                root,
                "views:\n"
                "  ai-market:\n"
                "    name: AI Market\n"
                "    entity_ids: [acme, gridco]\n",
            )
            registry = build_entity_registry(root)
            graph = build_graph_projection(registry, root)
            projection = build_view_projections(registry, graph)["ai-market"]

        self.assertEqual(projection["counts"]["edges"], 1)
        relationship = projection["relationships"][0]
        self.assertFalse(relationship["directed"])
        self.assertEqual(relationship["source_entity_id"], "acme")
        self.assertEqual(relationship["target_entity_id"], "gridco")
        self.assertEqual(relationship["event_count"], 2)
        self.assertEqual(
            [evidence["date"] for evidence in relationship["timeline"]],
            ["2026-02-03", "2026-01-02"],
        )
        self.assertEqual(relationship["latest_date"], "2026-02-03")
        self.assertEqual(relationship["relation_types"], ["contract", "investment"])

    def test_reports_retired_farplane_metadata_fence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(
                root / ".farplane/entities/acme.md",
                "id: acme\nkind: company\nname: Acme",
                "# Acme\n\n## View: AI Market\n\n### Timeline\n\n"
                "- 2026-01-02 Acme announced capacity.\n\n"
                "  ```farplane\n"
                "  view: ai-market\n"
                "  ```\n",
            )
            write_views(
                root,
                "views:\n"
                "  ai-market:\n"
                "    name: AI Market\n"
                "    entity_ids: [acme]\n"
                "    resources:\n"
                "      power:\n"
                "        name: Power\n"
                "        base_unit: GW\n"
                "        units: {GW: 1}\n",
            )
            registry = build_entity_registry(root)
        self.assertEqual(registry["counts"]["issues"], 1)
        self.assertEqual(
            registry["issues"][0]["reason"],
            "retired_farplane_metadata_fence",
        )

    def test_reports_invalid_coordinates_and_entity_links_without_dropping_nodes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entity_root = root / ".farplane/entities"
            write_entity(
                entity_root / "acme.md",
                "id: acme\nkind: company\nname: Acme\nlatitude: 91\nlongitude: 20",
                "# Acme\n\nLinks to [Missing](entity:missing), [Bad](entity:Bad-ID), and [itself](entity:acme).\n",
            )
            registry = build_entity_registry(root)
            graph = build_graph_projection(registry, root)

        reasons = [issue["reason"] for issue in registry["issues"]]
        self.assertEqual(
            reasons,
            ["latitude_out_of_range", "unresolved_entity_link:missing", "invalid_entity_link:Bad-ID", "self_entity_link:acme"],
        )
        self.assertEqual(len(graph["nodes"]), 1)
        self.assertEqual(graph["edges"], [])
        self.assertNotIn("issues", graph)

    def test_reports_unpaired_and_non_numeric_coordinates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entity_root = root / ".farplane/entities"
            write_entity(entity_root / "one.md", "id: one\nkind: company\nname: One\nlatitude: 1")
            write_entity(
                entity_root / "two.md",
                "id: two\nkind: company\nname: Two\nlatitude: north\nlongitude: east",
            )
            write_entity(
                entity_root / "three.md",
                "id: three\nkind: company\nname: Three\nlatitude: .nan\nlongitude: 10",
            )
            registry = build_entity_registry(root)

        self.assertEqual(
            [issue["reason"] for issue in registry["issues"]],
            ["coordinates_unpaired", "coordinates_not_finite", "coordinates_not_numeric"],
        )

    def test_no_write_does_not_replace_either_projection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(root / ".farplane/entities/acme.md", "id: acme\nkind: company\nname: Acme")
            result = subprocess.run(
                [sys.executable, str(CLI), "wiki", "rebuild", "--project-root", str(root), "--no-write"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertFalse((root / ".farplane/entities/index.json").exists())
            self.assertFalse((root / ".farplane/entities/graph.json").exists())
            self.assertFalse((root / ".farplane/entities/crm.json").exists())

    def test_ignores_entity_links_inside_inline_and_fenced_code(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(
                root / ".farplane/entities/acme.md",
                "id: acme\nkind: company\nname: Acme",
                "# Notes\n\n`[Inline](entity:target)`\n\n```markdown\n[Fenced](entity:target)\n```\n",
            )
            write_entity(
                root / ".farplane/entities/target.md",
                "id: target\nkind: company\nname: Target",
            )
            registry = build_entity_registry(root)
            graph = build_graph_projection(registry, root)

        self.assertEqual(graph["edges"], [])
        self.assertEqual(registry["issues"], [])

    def test_compiles_question_backed_claims_nodes_and_edges(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir()
            (root / "farplane/manifest.json").write_text(
                json.dumps({"project": {"id": "supply-lab", "name": "Supply Lab"}}),
                encoding="utf-8",
            )
            question_definition = (
                "[^q-20260720-01]: Which suppliers could support Acme's Malaysian expansion?"
                " | session=019f7e88-6864-7f23-8dbb-5e058009e911"
            )
            write_entity(
                root / ".farplane/entities/acme.md",
                "id: acme\nkind: company\nname: Acme Motors",
                "# Acme Motors\n\n## Notes\n\nMalaysia expansion is under evaluation. [^q-20260720-01]\n\n"
                "## Question index\n\n" + question_definition + "\n",
            )
            write_entity(
                root / ".farplane/entities/castings.md",
                "id: castings\nkind: company\nname: Penang Castings",
                "# Penang Castings\n\n## Relationships\n\n"
                "- Supplies aluminum housings to [Acme Motors](entity:acme). [^q-20260720-01]\n\n"
                "## Question index\n\n" + question_definition + "\n",
            )
            registry = build_entity_registry(root)
            graph = build_graph_projection(registry, root)

        self.assertNotIn("schema_version", registry)
        self.assertEqual(registry["issues"], [])
        self.assertEqual(len(registry["questions"]), 1)
        self.assertEqual(len(registry["claims"]), 2)
        self.assertEqual(registry["questions"][0]["id"], "q-20260720-01")
        self.assertEqual(
            registry["questions"][0]["session_ids"],
            ["019f7e88-6864-7f23-8dbb-5e058009e911"],
        )
        self.assertEqual(registry["by_id"]["acme"]["question_refs"], ["q-20260720-01"])
        self.assertEqual(graph["edges"][0]["question_refs"], ["q-20260720-01"])
        self.assertEqual(graph["questions"][0]["entity_ids"], ["acme", "castings"])
        self.assertEqual(len(graph["questions"][0]["claim_keys"]), 2)
        self.assertEqual(len(graph["questions"][0]["edge_keys"]), 1)
        self.assertNotIn("question", {node["kind"] for node in graph["nodes"]})

    def test_reports_unresolved_and_conflicting_question_refs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entity_root = root / ".farplane/entities"
            write_entity(
                entity_root / "one.md",
                "id: one\nkind: company\nname: One",
                "# One\n\nKnown fact. [^q-shared]\n\n"
                "## Question index\n\n[^q-shared]: What is the shared fact? | session=session-one\n",
            )
            write_entity(
                entity_root / "two.md",
                "id: two\nkind: company\nname: Two",
                "# Two\n\nDifferent fact. [^q-shared]\n\n"
                "## Question index\n\n[^q-shared]: A conflicting question? | session=session-one\n",
            )
            write_entity(
                entity_root / "three.md",
                "id: three\nkind: company\nname: Three",
                "# Three\n\nLocally unresolved fact. [^q-shared] [^q-missing]\n",
            )
            registry = build_entity_registry(root)

        reasons = [issue["reason"] for issue in registry["issues"]]
        self.assertIn("conflicting_question_definition:q-shared", reasons)
        self.assertIn("unresolved_question_ref:q-shared", reasons)
        self.assertIn("unresolved_question_ref:q-missing", reasons)

    def test_question_provenance_does_not_change_semantic_keys(self) -> None:
        def compile_with_session(root: Path, session_id: str) -> dict[str, Any]:
            (root / "farplane").mkdir(parents=True)
            (root / "farplane/manifest.json").write_text(
                json.dumps({"project": {"id": "stable-project", "name": "Stable Project"}}),
                encoding="utf-8",
            )
            write_entity(
                root / ".farplane/entities/acme.md",
                "id: acme\nkind: company\nname: Acme",
            )
            write_entity(
                root / ".farplane/entities/supplier.md",
                "id: supplier\nkind: company\nname: Supplier",
                "# Supplier\n\n## Relationships\n\n"
                "- Supplies [Acme](entity:acme). [^q-stable]\n\n"
                f"## Question index\n\n[^q-stable]: Who supplies Acme? | session={session_id}\n",
            )
            return build_graph_projection(build_entity_registry(root), root)

        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            first = compile_with_session(base / "first", "session-one")
            second = compile_with_session(base / "second", "session-two")

        self.assertEqual(first["edges"][0]["key"], second["edges"][0]["key"])
        self.assertEqual(first["claims"][0]["key"], second["claims"][0]["key"])
        self.assertNotEqual(first["source_fingerprint"], second["source_fingerprint"])

    def test_semantic_claim_and_edge_keys_ignore_storage_path(self) -> None:
        record = {
            "id": "supplier",
            "path": ".farplane/entities/supplier.md",
            "body": "Supplies [Acme](entity:acme). [^q-stable]\n\n[^q-stable]: Who supplies Acme?\n",
        }
        moved_record = {**record, "path": ".farplane/elsewhere/supplier.md"}
        self.assertEqual(body_claims(record)[0]["key"], body_claims(moved_record)[0]["key"])

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "farplane").mkdir(parents=True)
            (root / "farplane/manifest.json").write_text(
                json.dumps({"project": {"id": "stable-project", "name": "Stable Project"}}),
                encoding="utf-8",
            )
            write_entity(root / ".farplane/entities/acme.md", "id: acme\nkind: company\nname: Acme")
            write_entity(
                root / ".farplane/entities/supplier.md",
                "id: supplier\nkind: company\nname: Supplier",
                record["body"],
            )
            index = build_entity_registry(root)
            first = build_graph_projection(index, root)
            moved_index = copy.deepcopy(index)
            moved_index["by_id"]["supplier"]["path"] = ".farplane/elsewhere/supplier.md"
            second = build_graph_projection(moved_index, root)

        self.assertEqual(first["edges"][0]["key"], second["edges"][0]["key"])

    def test_session_provenance_is_optional_and_not_question_identity(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entity_root = root / ".farplane/entities"
            question = "Which suppliers support Acme?"
            write_entity(
                entity_root / "one.md",
                "id: one\nkind: company\nname: One",
                f"# One\n\nFirst fact. [^q-shared]\n\n[^q-shared]: {question}\n",
            )
            write_entity(
                entity_root / "two.md",
                "id: two\nkind: company\nname: Two",
                f"# Two\n\nSecond fact. [^q-shared]\n\n[^q-shared]: {question} | session=session-two\n",
            )
            write_entity(
                entity_root / "three.md",
                "id: three\nkind: company\nname: Three",
                f"# Three\n\nThird fact. [^q-shared]\n\n[^q-shared]: {question} | session=session-three\n",
            )
            registry = build_entity_registry(root)

        self.assertEqual(registry["issues"], [])
        self.assertEqual(registry["questions"][0]["question"], question)
        self.assertEqual(registry["questions"][0]["session_ids"], ["session-three", "session-two"])
        self.assertEqual(registry["questions"][0]["entity_ids"], ["one", "three", "two"])

    def test_question_syntax_inside_code_or_definitions_does_not_create_claims_or_edges(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(
                root / ".farplane/entities/acme.md",
                "id: acme\nkind: company\nname: Acme",
                "# Acme\n\n`Example [^q-code] and [Target](entity:target)`\n\n"
                "[^q-code]: Does [Target](entity:target) matter?\n",
            )
            write_entity(
                root / ".farplane/entities/target.md",
                "id: target\nkind: company\nname: Target",
            )
            registry = build_entity_registry(root)
            graph = build_graph_projection(registry, root)

        self.assertEqual(registry["claims"], [])
        self.assertEqual(registry["questions"][0]["session_ids"], [])
        self.assertEqual(graph["edges"], [])

    def test_same_named_local_projects_receive_distinct_fallback_ids(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = root / "one" / "same-name"
            second = root / "two" / "same-name"
            first.mkdir(parents=True)
            second.mkdir(parents=True)
            first_identity = project_identity(first)
            second_identity = project_identity(second)

        self.assertNotEqual(first_identity["id"], second_identity["id"])
        self.assertEqual(first_identity["source"], "local_path_fallback")


if __name__ == "__main__":
    unittest.main()
