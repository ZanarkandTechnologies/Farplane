from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from bin.core.eval_contract import (
    EvalContractError,
    lint_agent_skills_eval_suite,
    load_agent_skills_eval_suite,
    suite_json_schema,
)
from bin.validators.check_eval_contract import check_generated_schema, discover_eval_manifests, lint_eval_manifests


class EvalContractTests(unittest.TestCase):
    def write_suite(self, root: Path, payload: dict) -> Path:
        path = root / "skills" / "sample-skill" / "evals" / "evals.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def valid_payload(self) -> dict:
        return {
            "skill_name": "sample-skill",
            "evals": [
                {
                    "id": "case-1",
                    "prompt": "Do the real task.",
                    "expected_output": "A grounded result.",
                    "files": ["evals/files/input.txt"],
                    "assertions": ["Names the result."],
                    "metadata": {
                        "farplane": {
                            "title": "Visible case title",
                            "workspace_fixture": "evals/files/workspace",
                            "extensions": {"acme.preview": {"enabled": True}},
                        }
                    },
                }
            ],
        }

    def test_typed_suite_accepts_consumer_fields_and_extension_map(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = self.write_suite(root, self.valid_payload())

            suite = lint_agent_skills_eval_suite(path, root=root)

        self.assertEqual(suite.skill_name, "sample-skill")
        self.assertEqual(suite.evals[0].metadata.farplane.extensions["acme.preview"], {"enabled": True})

    def test_closed_root_case_and_metadata_reject_typos(self) -> None:
        payload = self.valid_payload()
        payload["format"] = "farplane.eval.agent-skill/v1"
        payload["evals"][0]["expectations"] = ["legacy alias"]
        payload["evals"][0]["metadata"]["farplane"]["titel"] = "typo"

        with tempfile.TemporaryDirectory() as temp:
            path = self.write_suite(Path(temp), payload)
            with self.assertRaisesRegex(EvalContractError, "Extra inputs are not permitted"):
                load_agent_skills_eval_suite(path)

    def test_retired_metadata_fields_are_rejected(self) -> None:
        retired_fields = {
            "anti_patterns": ["Do not invent facts."],
            "behavior_requirements": {"required_successful_command_regexes": ["python3"]},
            "benchmark_value": "high",
            "difficulty": "hard",
            "expected_behavior": "Names the result.",
            "failure_modes": ["Generic answer"],
            "hardcase": True,
            "sanitization_notes": "Sanitized",
        }
        for field, value in retired_fields.items():
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temp:
                payload = self.valid_payload()
                payload["evals"][0]["metadata"]["farplane"][field] = value
                path = self.write_suite(Path(temp), payload)
                with self.assertRaisesRegex(EvalContractError, "Extra inputs are not permitted"):
                    load_agent_skills_eval_suite(path)

    def test_required_core_strings_are_inline_constrained_and_ids_are_strings(self) -> None:
        payload = self.valid_payload()
        payload["evals"][0]["id"] = 1

        with tempfile.TemporaryDirectory() as temp:
            path = self.write_suite(Path(temp), payload)
            with self.assertRaisesRegex(EvalContractError, "id: Input should be a valid string"):
                load_agent_skills_eval_suite(path)

        payload = self.valid_payload()
        payload["evals"][0]["prompt"] = " "
        with tempfile.TemporaryDirectory() as temp:
            path = self.write_suite(Path(temp), payload)
            with self.assertRaisesRegex(EvalContractError, "prompt: String should have at least 1 character"):
                load_agent_skills_eval_suite(path)

    def test_empty_optional_context_is_valid_for_legacy_context_disable_semantics(self) -> None:
        payload = self.valid_payload()
        payload["evals"][0]["metadata"]["farplane"]["context"] = ""

        with tempfile.TemporaryDirectory() as temp:
            path = self.write_suite(Path(temp), payload)
            suite = load_agent_skills_eval_suite(path)

        self.assertEqual(suite.evals[0].metadata.farplane.context, "")

    def test_rejects_path_escape_and_duplicate_ids(self) -> None:
        payload = self.valid_payload()
        payload["evals"].append({
            "id": "case-1",
            "prompt": "Other task",
            "expected_output": "Other result",
            "files": ["../escape.txt"],
        })

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = self.write_suite(root, payload)
            with self.assertRaisesRegex(EvalContractError, "file paths must stay relative"):
                lint_agent_skills_eval_suite(path, root=root)

    def test_retired_feature_id_is_rejected(self) -> None:
        payload = self.valid_payload()
        payload["evals"][0]["metadata"]["farplane"]["feature_id"] = "unbound"

        with tempfile.TemporaryDirectory() as temp:
            path = self.write_suite(Path(temp), payload)
            with self.assertRaisesRegex(EvalContractError, "Extra inputs are not permitted"):
                load_agent_skills_eval_suite(path)

    def test_checked_in_json_schema_matches_the_pydantic_source_of_truth(self) -> None:
        root = Path(__file__).resolve().parents[2]
        schema_path = root / "bin" / "core" / "eval_suite.schema.json"

        self.assertEqual(json.loads(schema_path.read_text(encoding="utf-8")), suite_json_schema())
        self.assertIsNone(check_generated_schema(root))

    def test_production_discovery_excludes_nested_fixtures_and_linked_external_skills(self) -> None:
        root = Path(__file__).resolve().parents[2]
        manifests = discover_eval_manifests(root)

        owned = [path for path in root.glob("skills/*/evals/evals.json") if not path.parent.parent.is_symlink()]
        self.assertEqual(len(manifests), len(owned))
        self.assertTrue(all(path.match("skills/*/evals/evals.json") for path in manifests))
        self.assertEqual(lint_eval_manifests(root, manifests), [])


if __name__ == "__main__":
    unittest.main()
