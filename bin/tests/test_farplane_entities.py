from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = ROOT / "bin" / "core"
CLI = ROOT / "bin" / "farplane.py"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from farplane_entities import body_claims, build_crm_projection, build_entity_index, build_world_projection, project_identity


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
            index = build_entity_index(root)
            world = build_world_projection(index, root)
            crm = build_crm_projection(index, root)

        expected = [
            {
                "id": "supply-chain",
                "name": "Supply Chain",
                "entity_ids": ["supplier", "acme"],
            }
        ]
        self.assertEqual(index["views"], expected)
        self.assertEqual(world["views"], expected)
        self.assertEqual(crm["views"], expected)
        self.assertEqual(index["views_by_id"]["supply-chain"], expected[0])
        self.assertEqual(
            {index["source_fingerprint"], world["source_fingerprint"], crm["source_fingerprint"]},
            {index["source_fingerprint"]},
        )

    def test_absent_view_config_compiles_as_no_views(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(root / ".farplane/entities/acme.md", "id: acme\nkind: company\nname: Acme")
            index = build_entity_index(root)

        self.assertEqual(index["views"], [])
        self.assertEqual(index["views_by_id"], {})
        self.assertEqual(index["issues"], [])

    def test_view_changes_invalidate_projection_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(root / ".farplane/entities/acme.md", "id: acme\nkind: company\nname: Acme")
            write_entity(root / ".farplane/entities/other.md", "id: other\nkind: company\nname: Other")
            write_views(root, "views:\n  focus:\n    name: Focus\n    entity_ids: [acme]\n")
            first = build_entity_index(root)
            write_views(root, "views:\n  focus:\n    name: Focus\n    entity_ids: [other]\n")
            second = build_entity_index(root)

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
            index = build_entity_index(root)
            result = subprocess.run(
                [sys.executable, str(CLI), "entities", "compile", "--project-root", str(root), "--no-write"],
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
            index = build_entity_index(root)
            result = subprocess.run(
                [sys.executable, str(CLI), "entities", "compile", "--project-root", str(root), "--no-write"],
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
                index = build_entity_index(root)

            self.assertIn(expected_reason, {issue["reason"] for issue in index["issues"]})
            self.assertEqual(index["views"], [])

    def test_compiles_markdown_entities_and_body(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(root / ".farplane/entities/acme.md", "id: acme\nkind: company\nname: Acme")
            write_entity(
                root / ".farplane/entities/jane.md",
                "id: jane\nkind: person\nname: Jane\ncompany_ref: acme\nstatus: researching",
                "# Jane\n\nPrefers concrete demos.\n",
            )
            registry = build_entity_index(root)

        self.assertEqual(registry["counts"], {"included": 2, "excluded": 0, "issues": 0})
        self.assertIn("Prefers concrete demos", registry["by_id"]["jane"]["body"])
        self.assertEqual(registry["by_id"]["jane"]["frontmatter"]["company_ref"], "acme")

    def test_reports_invalid_mismatched_and_unresolved_entities(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entity_root = root / ".farplane/entities"
            write_entity(entity_root / "jane.md", "id: jane\nkind: person\nname: Jane\ncompany_ref: missing")
            write_entity(entity_root / "wrong-name.md", "id: other\nkind: person\nname: Other")
            write_entity(entity_root / "bad.md", "id: Bad ID\nkind: person\nname: Bad")
            write_entity(entity_root / "missing.md", "kind: person\nname: Missing")
            (entity_root / "no-frontmatter.md").write_text("# Nope\n", encoding="utf-8")
            registry = build_entity_index(root)

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
            first = build_entity_index(root)
            second = build_entity_index(root)

        self.assertEqual(first, second)

    def test_cli_writes_registry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(root / ".farplane/entities/design-partner.md", "id: design-partner\nkind: opportunity\nname: Design Partner")
            write_views(
                root,
                "views:\n  pipeline:\n    name: Pipeline\n    entity_ids: [design-partner]\n",
            )
            result = subprocess.run(
                [sys.executable, str(CLI), "entities", "compile", "--project-root", str(root), "--json"],
                capture_output=True,
                text=True,
                check=False,
            )
            written = json.loads((root / ".farplane/entities/index.json").read_text(encoding="utf-8"))
            world = json.loads((root / ".farplane/entities/world.json").read_text(encoding="utf-8"))
            crm = json.loads((root / ".farplane/entities/crm.json").read_text(encoding="utf-8"))

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(written["schema_version"], 3)
        self.assertEqual(world["schema_version"], 3)
        self.assertEqual(crm["schema_version"], 3)
        self.assertEqual(written["entities"][0]["id"], "design-partner")
        self.assertEqual(world["nodes"][0]["key"], f"{project_identity(root)['id']}:design-partner")
        self.assertEqual(crm["entities"], [])
        self.assertEqual(written["views"], world["views"])
        self.assertEqual(world["views"], crm["views"])
        self.assertEqual(world["views"][0]["entity_ids"], ["design-partner"])
        self.assertEqual(
            {written["source_fingerprint"], world["source_fingerprint"], crm["source_fingerprint"]},
            {written["source_fingerprint"]},
        )

    def test_crm_projection_contains_only_entities_with_funnel_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(
                root / ".farplane/entities/prospect.md",
                "id: prospect\nkind: company\nname: Prospect\nfunnel:\n  stage: researched\n  status: active",
            )
            write_entity(root / ".farplane/entities/indicator.md", "id: indicator\nkind: market-indicator\nname: Indicator")
            index = build_entity_index(root)
            crm = build_crm_projection(index, root)

        self.assertEqual(index["issues"], [])
        self.assertEqual(crm["counts"], {"entities": 1, "issues": 0})
        self.assertEqual(list(crm["by_id"]), ["prospect"])
        self.assertEqual(crm["by_id"]["prospect"]["funnel"]["stage"], "researched")

    def test_reports_non_object_funnel_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(
                root / ".farplane/entities/prospect.md",
                "id: prospect\nkind: company\nname: Prospect\nfunnel: researching",
            )
            index = build_entity_index(root)
            crm = build_crm_projection(index, root)

        self.assertEqual(index["issues"][0]["reason"], "invalid_funnel:not_object")
        self.assertEqual(crm["entities"], [])

    def test_rejects_nested_entity_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(root / ".farplane/entities/companies/acme.md", "id: acme\nkind: company\nname: Acme")
            index = build_entity_index(root)

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
                "# Penang Castings\n\n## Relationships\n\n- Supplies aluminum housings to [Acme Motors](entity:acme) from its Penang facility. The relationship is under review.\n",
            )
            registry = build_entity_index(root)
            first = build_world_projection(registry, root)
            second = build_world_projection(registry, root)

        self.assertEqual(first, second)
        self.assertEqual(
            first["project"],
            {"project_id": "supply-lab", "name": "Supply Lab", "identity_source": "manifest"},
        )
        self.assertEqual(first["source_fingerprint"], registry["source_fingerprint"])
        self.assertEqual(first["counts"], {"nodes": 2, "located_nodes": 1, "edges": 1, "issues": 0})
        self.assertEqual(first["nodes"][0]["key"], "supply-lab:acme")
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
        self.assertNotIn("body", first["nodes"][0])

    def test_reports_invalid_coordinates_and_entity_links_without_dropping_nodes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            entity_root = root / ".farplane/entities"
            write_entity(
                entity_root / "acme.md",
                "id: acme\nkind: company\nname: Acme\nlatitude: 91\nlongitude: 20",
                "# Acme\n\nLinks to [Missing](entity:missing), [Bad](entity:Bad-ID), and [itself](entity:acme).\n",
            )
            registry = build_entity_index(root)
            world = build_world_projection(registry, root)

        reasons = [issue["reason"] for issue in registry["issues"]]
        self.assertEqual(
            reasons,
            ["latitude_out_of_range", "unresolved_entity_link:missing", "invalid_entity_link:Bad-ID", "self_entity_link:acme"],
        )
        self.assertEqual(world["counts"], {"nodes": 1, "located_nodes": 0, "edges": 0, "issues": 4})

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
            registry = build_entity_index(root)

        self.assertEqual(
            [issue["reason"] for issue in registry["issues"]],
            ["coordinates_unpaired", "coordinates_not_finite", "coordinates_not_numeric"],
        )

    def test_no_write_does_not_replace_either_projection(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(root / ".farplane/entities/acme.md", "id: acme\nkind: company\nname: Acme")
            result = subprocess.run(
                [sys.executable, str(CLI), "entities", "compile", "--project-root", str(root), "--no-write"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertFalse((root / ".farplane/entities/index.json").exists())
            self.assertFalse((root / ".farplane/entities/world.json").exists())
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
            registry = build_entity_index(root)
            world = build_world_projection(registry, root)

        self.assertEqual(world["edges"], [])
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
            registry = build_entity_index(root)
            world = build_world_projection(registry, root)

        self.assertEqual(registry["schema_version"], 3)
        self.assertEqual(registry["issues"], [])
        self.assertEqual(len(registry["questions"]), 1)
        self.assertEqual(len(registry["claims"]), 2)
        self.assertEqual(registry["questions"][0]["id"], "q-20260720-01")
        self.assertEqual(
            registry["questions"][0]["session_ids"],
            ["019f7e88-6864-7f23-8dbb-5e058009e911"],
        )
        self.assertEqual(registry["by_id"]["acme"]["question_refs"], ["q-20260720-01"])
        self.assertEqual(world["edges"][0]["question_refs"], ["q-20260720-01"])
        self.assertEqual(world["questions"][0]["entity_ids"], ["acme", "castings"])
        self.assertEqual(len(world["questions"][0]["claim_keys"]), 2)
        self.assertEqual(len(world["questions"][0]["edge_keys"]), 1)
        self.assertNotIn("question", {node["kind"] for node in world["nodes"]})

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
            registry = build_entity_index(root)

        reasons = [issue["reason"] for issue in registry["issues"]]
        self.assertIn("conflicting_question_definition:q-shared", reasons)
        self.assertIn("unresolved_question_ref:q-shared", reasons)
        self.assertIn("unresolved_question_ref:q-missing", reasons)

    def test_question_provenance_does_not_change_semantic_keys(self) -> None:
        def compile_with_session(root: Path, session_id: str) -> dict[str, object]:
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
            return build_world_projection(build_entity_index(root), root)

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
            index = build_entity_index(root)
            first = build_world_projection(index, root)
            moved_index = copy.deepcopy(index)
            moved_index["by_id"]["supplier"]["path"] = ".farplane/elsewhere/supplier.md"
            second = build_world_projection(moved_index, root)

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
            registry = build_entity_index(root)

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
            registry = build_entity_index(root)
            world = build_world_projection(registry, root)

        self.assertEqual(registry["claims"], [])
        self.assertEqual(registry["questions"][0]["session_ids"], [])
        self.assertEqual(world["edges"], [])

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
