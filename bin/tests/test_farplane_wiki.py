from __future__ import annotations

import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
CORE_DIR = ROOT / "bin" / "core"
CLI = ROOT / "bin" / "farplane.py"
if str(CORE_DIR) not in sys.path:
    sys.path.insert(0, str(CORE_DIR))

from farplane_entities import build_entity_registry, build_graph_projection
from farplane_wiki import WIKI_DATABASE_PATH, doctor, rebuild, search, sync
from farplane_wiki_store import os as wiki_store_os


def write_entity(
    root: Path,
    entity_id: str,
    name: str,
    *,
    aliases: list[str] | None = None,
    body: str = "",
    kind: str = "company",
) -> Path:
    alias_yaml = ""
    if aliases:
        alias_yaml = "\naliases:\n" + "\n".join(f"  - {alias}" for alias in aliases)
    path = root / ".farplane/entities" / f"{entity_id}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"---\nid: {entity_id}\nkind: {kind}\nname: {name}{alias_yaml}\n---\n\n"
        f"# {name}\n\n{body}\n",
        encoding="utf-8",
    )
    return path


def database_rows(root: Path, query: str) -> list[tuple[object, ...]]:
    connection = sqlite3.connect(root / WIKI_DATABASE_PATH)
    try:
        return connection.execute(query).fetchall()
    finally:
        connection.close()


class FarplaneWikiTests(unittest.TestCase):
    def test_rebuild_creates_searchable_exact_alias_and_trigram_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(root, "alphabet", "Alphabet", aliases=["Alphabet Inc.", "Google"])
            write_entity(root, "openai", "OpenAI", aliases=["OpenAI Group PBC"])

            result = rebuild(root)
            exact = search(root, "Open AI")
            alias = search(root, "Google")
            typo = search(root, "Googel")

        self.assertTrue(result["ok"])
        self.assertTrue(result["written"])
        self.assertEqual(exact["candidates"][0]["id"], "openai")
        self.assertIn("exact_name", exact["candidates"][0]["match_types"])
        self.assertEqual(alias["candidates"][0]["id"], "alphabet")
        self.assertIn("exact_alias", alias["candidates"][0]["match_types"])
        self.assertEqual(typo["candidates"][0]["id"], "alphabet")
        self.assertIn("trigram", typo["candidates"][0]["match_types"])

    def test_rebuild_deduplicates_aliases_after_identity_normalization(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(root, "openai", "OpenAI", aliases=["Open AI", "OpenAI"])

            result = rebuild(root)
            aliases = database_rows(
                root, "SELECT alias, normalized_alias FROM aliases ORDER BY alias"
            )
            candidates = search(root, "Open AI")["candidates"]

        self.assertTrue(result["ok"])
        self.assertEqual(len(aliases), 1)
        self.assertEqual(aliases[0][1], "openai")
        self.assertEqual([candidate["id"] for candidate in candidates], ["openai"])

    def test_rebuild_removes_retired_projection_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(root, "alpha", "Alpha")
            retired_path = root / ".farplane/entities/world.json"
            retired_path.parent.mkdir(parents=True, exist_ok=True)
            retired_path.write_text('{"retired": true}\n', encoding="utf-8")

            result = rebuild(root)
            retired_exists = retired_path.exists()

        self.assertTrue(result["written"])
        self.assertFalse(retired_exists)
        self.assertIn(".farplane/entities/graph.json", result["projection_paths"])

    def test_sync_removes_retired_projection_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            alpha = write_entity(root, "alpha", "Alpha")
            rebuild(root)
            retired_path = root / ".farplane/entities/world.json"
            retired_path.write_text('{"retired": true}\n', encoding="utf-8")
            alpha.write_text(
                alpha.read_text(encoding="utf-8").replace("name: Alpha", "name: Alpha Labs"),
                encoding="utf-8",
            )

            result = sync(root, [str(alpha)])
            retired_exists = retired_path.exists()
            graph_exists = (root / ".farplane/entities/graph.json").exists()

        self.assertTrue(result["written"])
        self.assertFalse(retired_exists)
        self.assertTrue(graph_exists)

    def test_sync_replaces_only_changed_origin_edges_and_matches_rebuild(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            alpha = write_entity(
                root,
                "alpha",
                "Alpha",
                body="Works with [Beta](entity:beta).",
            )
            write_entity(root, "beta", "Beta")
            write_entity(
                root,
                "gamma",
                "Gamma",
                body="Also works with [Beta](entity:beta).",
            )
            rebuild(root)
            gamma_before = database_rows(
                root,
                "SELECT edge_key, payload_json FROM edge_claims "
                "WHERE origin_page_id = 'gamma'",
            )

            alpha.write_text(
                alpha.read_text(encoding="utf-8").replace(
                    "[Beta](entity:beta)", "[Gamma](entity:gamma)"
                ),
                encoding="utf-8",
            )
            result = sync(root, [str(alpha)])
            graph_after_sync = json.loads(
                (root / ".farplane/entities/graph.json").read_text(encoding="utf-8")
            )
            gamma_after = database_rows(
                root,
                "SELECT edge_key, payload_json FROM edge_claims "
                "WHERE origin_page_id = 'gamma'",
            )
            alpha_targets = database_rows(
                root,
                "SELECT target_entity_id FROM edge_claims "
                "WHERE origin_page_id = 'alpha'",
            )
            rebuild(root)
            graph_after_rebuild = json.loads(
                (root / ".farplane/entities/graph.json").read_text(encoding="utf-8")
            )

        self.assertEqual(result["changed_pages"], [".farplane/entities/alpha.md"])
        self.assertEqual(gamma_before, gamma_after)
        self.assertEqual(alpha_targets, [("gamma",)])
        self.assertEqual(graph_after_sync, graph_after_rebuild)

    def test_sync_path_limits_changes_to_the_requested_pages(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            alpha = write_entity(root, "alpha", "Alpha")
            gamma = write_entity(root, "gamma", "Gamma")
            rebuild(root)
            alpha.write_text(
                alpha.read_text(encoding="utf-8").replace("name: Alpha", "name: Alpha Labs"),
                encoding="utf-8",
            )
            gamma.write_text(
                gamma.read_text(encoding="utf-8").replace("name: Gamma", "name: Gamma Labs"),
                encoding="utf-8",
            )

            first = sync(root, [str(alpha)])
            cached_names = database_rows(
                root, "SELECT entity_id, name FROM pages ORDER BY entity_id"
            )
            with self.assertRaisesRegex(Exception, "wiki_database_stale"):
                search(root, "Alpha Labs")
            second = sync(root, [str(gamma)])

        self.assertEqual(first["changed_pages"], [".farplane/entities/alpha.md"])
        self.assertEqual(cached_names, [("alpha", "Alpha Labs"), ("gamma", "Gamma")])
        self.assertEqual(second["changed_pages"], [".farplane/entities/gamma.md"])

    def test_invalid_rebuild_is_fail_closed_for_database_and_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            alpha = write_entity(root, "alpha", "Alpha")
            rebuild(root)
            database_before = (root / WIKI_DATABASE_PATH).read_bytes()
            graph_path = root / ".farplane/entities/graph.json"
            graph_before = graph_path.read_bytes()
            alpha.write_text(
                alpha.read_text(encoding="utf-8")
                + "\nLinks [Missing](entity:missing).\n",
                encoding="utf-8",
            )

            result = rebuild(root)
            database_after = (root / WIKI_DATABASE_PATH).read_bytes()
            graph_after = graph_path.read_bytes()

        self.assertFalse(result["ok"])
        self.assertFalse(result["written"])
        self.assertEqual(database_before, database_after)
        self.assertEqual(graph_before, graph_after)
        self.assertIn(
            "unresolved_entity_link:missing",
            {issue["reason"] for issue in result["diagnostics"]["issues"]},
        )

    def test_export_failure_rolls_back_database_and_json_as_one_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            alpha = write_entity(root, "alpha", "Alpha")
            rebuild(root)
            database_path = root / WIKI_DATABASE_PATH
            graph_path = root / ".farplane/entities/graph.json"
            retired_path = root / ".farplane/entities/world.json"
            retired_path.write_text('{"retired": true}\n', encoding="utf-8")
            database_before = database_path.read_bytes()
            graph_before = graph_path.read_bytes()
            retired_before = retired_path.read_bytes()
            alpha.write_text(
                alpha.read_text(encoding="utf-8").replace("name: Alpha", "name: Alpha Labs"),
                encoding="utf-8",
            )
            original_replace = wiki_store_os.replace
            failed_once = False

            def fail_graph_promotion(source: object, destination: object) -> None:
                nonlocal failed_once
                source_path = Path(source)
                destination_path = Path(destination)
                if (
                    not failed_once
                    and destination_path == graph_path
                    and ".wiki-stage-" in source_path.as_posix()
                ):
                    failed_once = True
                    raise OSError("simulated_projection_promotion_failure")
                original_replace(source, destination)

            with mock.patch(
                "farplane_wiki_store.os.replace", side_effect=fail_graph_promotion
            ):
                with self.assertRaisesRegex(OSError, "simulated_projection_promotion_failure"):
                    sync(root, [str(alpha)])

            database_after = database_path.read_bytes()
            graph_after = graph_path.read_bytes()
            retired_after = retired_path.read_bytes()

        self.assertEqual(database_before, database_after)
        self.assertEqual(graph_before, graph_after)
        self.assertEqual(retired_before, retired_after)

    def test_rebuild_failure_restores_retired_projection_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            alpha = write_entity(root, "alpha", "Alpha")
            rebuild(root)
            database_path = root / WIKI_DATABASE_PATH
            graph_path = root / ".farplane/entities/graph.json"
            retired_path = root / ".farplane/entities/world.json"
            retired_path.write_text('{"retired": true}\n', encoding="utf-8")
            database_before = database_path.read_bytes()
            graph_before = graph_path.read_bytes()
            retired_before = retired_path.read_bytes()
            alpha.write_text(
                alpha.read_text(encoding="utf-8").replace("name: Alpha", "name: Alpha Labs"),
                encoding="utf-8",
            )
            original_replace = wiki_store_os.replace
            failed_once = False

            def fail_graph_promotion(source: object, destination: object) -> None:
                nonlocal failed_once
                source_path = Path(source)
                destination_path = Path(destination)
                if (
                    not failed_once
                    and destination_path == graph_path
                    and ".wiki-stage-" in source_path.as_posix()
                ):
                    failed_once = True
                    raise OSError("simulated_projection_promotion_failure")
                original_replace(source, destination)

            with mock.patch(
                "farplane_wiki_store.os.replace", side_effect=fail_graph_promotion
            ):
                with self.assertRaisesRegex(OSError, "simulated_projection_promotion_failure"):
                    rebuild(root)

            database_after = database_path.read_bytes()
            graph_after = graph_path.read_bytes()
            retired_after = retired_path.read_bytes()

        self.assertEqual(database_before, database_after)
        self.assertEqual(graph_before, graph_after)
        self.assertEqual(retired_before, retired_after)

    def test_sync_deletes_removed_page_and_its_search_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            removed = write_entity(root, "obsolete", "Obsolete")
            write_entity(root, "kept", "Kept")
            rebuild(root)
            removed.unlink()

            result = sync(root, [str(removed)])
            pages = database_rows(root, "SELECT entity_id FROM pages ORDER BY entity_id")
            fts = database_rows(root, "SELECT entity_id FROM entity_fts ORDER BY entity_id")

        self.assertEqual(result["removed_pages"], [".farplane/entities/obsolete.md"])
        self.assertEqual(pages, [("kept",)])
        self.assertEqual(fts, [("kept",)])

    def test_search_rejects_stale_database_until_sync(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            article = write_entity(root, "alpha", "Alpha")
            rebuild(root)
            article.write_text(
                article.read_text(encoding="utf-8").replace("name: Alpha", "name: Alpha Labs"),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(Exception, "wiki_database_stale"):
                search(root, "Alpha Labs")
            sync(root, [str(article)])
            result = search(root, "Alpha Labs")

        self.assertEqual(result["candidates"][0]["id"], "alpha")

    def test_cli_exposes_only_wiki_command_and_doctor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            wiki = subprocess.run(
                [sys.executable, str(CLI), "wiki", "doctor", "--project-root", str(root), "--json"],
                capture_output=True,
                text=True,
                check=False,
            )
            retired = subprocess.run(
                [sys.executable, str(CLI), "entities", "compile", "--project-root", str(root)],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(wiki.returncode, 0)
        self.assertTrue(json.loads(wiki.stdout)["ready"])
        self.assertNotEqual(retired.returncode, 0)
        self.assertIn("invalid choice", retired.stderr)

    def test_doctor_reports_generated_database_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_entity(root, "alpha", "Alpha")
            before = doctor(root)
            rebuild(root)
            after = doctor(root)

        self.assertTrue(before["ready"])
        self.assertFalse(before["database_exists"])
        self.assertTrue(after["database_exists"])
        self.assertEqual(after["schema_version"], "1")
        self.assertFalse(after["stale"])

    def test_cached_registry_preserves_full_projection_semantics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            article = write_entity(
                root,
                "supplier",
                "Supplier",
                body="Supplies [Buyer](entity:buyer). [^q-one]\n\n"
                "## Question index\n\n[^q-one]: Who supplies Buyer?",
            )
            write_entity(root, "buyer", "Buyer")
            rebuild(root)
            article.write_text(
                article.read_text(encoding="utf-8") + "\n\n## Notes\n\nStill active.\n",
                encoding="utf-8",
            )
            sync(root, [str(article)])
            generated = json.loads(
                (root / ".farplane/entities/graph.json").read_text(encoding="utf-8")
            )
            clean = build_graph_projection(build_entity_registry(root), root)

        self.assertEqual(generated, clean)


if __name__ == "__main__":
    unittest.main()
