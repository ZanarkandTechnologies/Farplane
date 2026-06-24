from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import farplane_adoption as adoption


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n", encoding="utf-8")


def write_manifest(root: Path, spec: str = "1.3.0", template_version: str = "1.3.0", features: dict[str, str] | None = None) -> None:
    payload: dict[str, object] = {
        "schema": "farplane_project",
        "spec_version": spec,
        "template_uses": {"farplane-framework": template_version},
    }
    if features is not None:
        payload["feature_pins"] = features
    write_json(root / "farplane" / "manifest.json", payload)


class FarplaneAdoptionTests(unittest.TestCase):
    def test_resolves_project_manifest_adoption_and_local_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            standard = root / "standard"
            project = root / "project"
            write_manifest(standard, features={"FEAT-0061": "adopted"})
            write_manifest(project, features={"FEAT-0061": "adopted"})
            skill_dir = project / "skills" / "client-report"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text("---\nname: client-report\n---\n", encoding="utf-8")
            write_jsonl(
                standard / "docs" / "features" / "registry.jsonl",
                [{"id": "FEAT-0061", "name": "Adoption tracker", "status": "implemented"}],
            )
            write_jsonl(
                standard / "docs" / "templates" / "registry.jsonl",
                [
                    {
                        "template_id": "farplane-framework",
                        "template_version": "1.3.0",
                        "feature_refs": ["FEAT-0061"],
                        "path": "skills/deep-init-project/references/MANIFEST_TEMPLATE.json",
                    }
                ],
            )

            result = adoption.resolve_adoption_stats(standard_root=standard, project_roots=[project])

        self.assertEqual(result["counts"]["projects"], 1)
        self.assertEqual(result["counts"]["manifests"], 1)
        self.assertEqual(result["counts"]["projectsWithLocalSkills"], 1)
        self.assertEqual(result["projects"][0]["localSkills"], ["client-report"])
        self.assertEqual(result["projects"][0]["skillSourcePolicy"], "local-if-present")
        self.assertIn("FEAT-0061", result["features"])
        self.assertEqual(result["features"]["FEAT-0061"]["projectCount"], 1)

    def test_reports_template_and_spec_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            standard = root / "standard"
            project = root / "project"
            write_manifest(standard, spec="1.3.0", template_version="1.3.0")
            write_manifest(project, spec="1.2.0", template_version="1.2.0")
            write_jsonl(standard / "docs" / "features" / "registry.jsonl", [])
            write_jsonl(
                standard / "docs" / "templates" / "registry.jsonl",
                [{"template_id": "farplane-framework", "template_version": "1.3.0"}],
            )

            result = adoption.resolve_adoption_stats(standard_root=standard, project_roots=[project])

        drift = result["projects"][0]["drift"]
        self.assertEqual(result["counts"]["driftItems"], 2)
        self.assertEqual({item["type"] for item in drift}, {"spec_version", "template"})

    def test_roots_file_accepts_office_project_shapes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project_a = root / "project-a"
            project_b = root / "project-b"
            roots_file = root / "projects.json"
            write_json(
                roots_file,
                {
                    "projects": [
                        {"projectRoot": str(project_a)},
                        {"path": str(project_b)},
                    ]
                },
            )

            roots = adoption.roots_from_file(roots_file)

        self.assertEqual(roots, [project_a.resolve(), project_b.resolve()])

    def test_missing_manifest_is_nonfatal_project_issue(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            standard = root / "standard"
            missing_project = root / "missing-project"
            write_manifest(standard)
            write_jsonl(standard / "docs" / "features" / "registry.jsonl", [])
            write_jsonl(standard / "docs" / "templates" / "registry.jsonl", [])

            result = adoption.resolve_adoption_stats(standard_root=standard, project_roots=[missing_project])

        self.assertFalse(result["projects"][0]["manifestExists"])
        self.assertEqual(result["projects"][0]["issues"], ["manifest_missing"])


if __name__ == "__main__":
    unittest.main()
