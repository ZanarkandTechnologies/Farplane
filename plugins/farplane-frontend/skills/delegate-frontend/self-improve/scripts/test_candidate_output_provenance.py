from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from typing import Any

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import artifact_summary
import phase_prompt_compiler

SELF_IMPROVE_ROOT = ROOT.parent
PROJECT_ROOT = SELF_IMPROVE_ROOT.parents[2]


def load_candidate_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    path = SELF_IMPROVE_ROOT / "results" / "candidate_outputs.jsonl"
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def load_test_cases() -> dict[str, dict[str, Any]]:
    cases: dict[str, dict[str, Any]] = {}
    path = SELF_IMPROVE_ROOT / "evals" / "test_cases.jsonl"
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        case = json.loads(line)
        cases[str(case["id"])] = case
    return cases


def marker_slug(value: str) -> str:
    return "".join(char if char.isalnum() else "_" for char in value).strip("_").lower()


def expected_output_marker(source: dict[str, Any]) -> str:
    tool = source.get("tool")
    if tool == "artifact_summary.py" and source.get("run_dir"):
        return f"produced_from_artifact_summary_{marker_slug(Path(source['run_dir']).name)}"
    if tool == "phase_prompt_compiler.py":
        return f"produced_from_phase_prompt_compiler_{marker_slug(str(source.get('phase', 'phase')))}"
    return ""


def semantic_phase(summary: dict[str, Any]) -> dict[str, Any]:
    phase = summary.get("phase_completion", {})
    handoff_path = str(phase.get("handoff_path", ""))
    return {
        "status": phase.get("status"),
        "owned_outputs": phase.get("owned_outputs"),
        "first_write_status": phase.get("first_write_status"),
        "exit_code": phase.get("exit_code"),
        "handoff_status": phase.get("handoff_status"),
        "handoff_present": bool(handoff_path),
        "handoff_placeholder_markers": phase.get("handoff_placeholder_markers", []),
        "handoff_contract": phase.get("handoff_contract", {}),
    }


def semantic_summary(summary: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "id": summary.get("id"),
        "startup": summary.get("startup"),
        "phase_completion": semantic_phase(summary),
    }
    if "first_write" in summary:
        first_write = summary["first_write"]
        result["first_write"] = {
            "status": first_write.get("status"),
            "expected_outputs": first_write.get("expected_outputs"),
            "observed_output": first_write.get("observed_output"),
            "failure_reason": first_write.get("failure_reason"),
        }
    if "spec" in summary:
        result["spec"] = summary["spec"]
    if "asset_manifest" in summary:
        manifest = dict(summary["asset_manifest"])
        manifest["assets"] = [
            {
                key: asset.get(key)
                for key in ("path", "kind", "role", "width", "height", "source_prompt")
                if key in asset
            }
            for asset in manifest.get("assets", [])
            if isinstance(asset, dict)
        ]
        result["asset_manifest"] = manifest
    return result


class CandidateOutputProvenanceTests(unittest.TestCase):
    def test_artifact_summary_rows_match_their_declared_sources(self) -> None:
        checked = 0
        cases = load_test_cases()
        for row in load_candidate_rows():
            source = row.get("summary_source", {})
            if source.get("tool") != "artifact_summary.py":
                continue
            marker = expected_output_marker(source)
            self.assertTrue(row.get("output", "").startswith(f"{marker}:"), row["id"])
            self.assertIn(marker, cases[row["id"]].get("must_contain", []), row["id"])
            source_project_root = (
                PROJECT_ROOT / source["project_root"]
                if source.get("project_root")
                else PROJECT_ROOT
            )
            args = SimpleNamespace(
                id=row["id"],
                output=row.get("output", ""),
                project_root=str(source_project_root),
                run_dir=str(PROJECT_ROOT / source["run_dir"]) if source.get("run_dir") else "",
                spec=str(PROJECT_ROOT / source["spec"]) if source.get("spec") else "",
                asset_manifest=str(PROJECT_ROOT / source["asset_manifest"]) if source.get("asset_manifest") else "",
                scroll_qa=str(PROJECT_ROOT / source["scroll_qa"]) if source.get("scroll_qa") else "",
                min_output_bytes=1,
            )
            produced = artifact_summary.build_summary(args)
            self.assertEqual(semantic_summary(row), semantic_summary(produced), row["id"])
            checked += 1
        self.assertGreaterEqual(checked, 4)

    def test_phase_prompt_compiler_rows_match_their_declared_sources(self) -> None:
        checked = 0
        cases = load_test_cases()
        for row in load_candidate_rows():
            source = row.get("summary_source", {})
            if source.get("tool") != "phase_prompt_compiler.py":
                continue
            marker = expected_output_marker(source)
            self.assertTrue(row.get("output", "").startswith(f"{marker}:"), row["id"])
            self.assertIn(marker, cases[row["id"]].get("must_contain", []), row["id"])
            prompt_args = SimpleNamespace(
                phase=source["phase"],
                brief=source.get("brief", ""),
                brief_file="",
                owned_output=source.get("owned_outputs", []),
                handoff_path="handoff.md",
                recipe_id=source["recipe_id"],
                taste_profile_id=source["taste_profile_id"],
                effect_stack_id=source["effect_stack_id"],
                acceptance=[],
                output="",
            )
            prompt = phase_prompt_compiler.compile_prompt(prompt_args)
            produced = phase_prompt_compiler.summarize_prompt(
                prompt=prompt,
                phase=source["phase"],
                owned_outputs=source.get("owned_outputs", []),
                recipe_id=source["recipe_id"],
                taste_profile_id=source["taste_profile_id"],
                effect_stack_id=source["effect_stack_id"],
            )
            self.assertEqual(row.get("compiled_prompt"), produced, row["id"])
            checked += 1
        self.assertGreaterEqual(checked, 1)


if __name__ == "__main__":
    unittest.main()
