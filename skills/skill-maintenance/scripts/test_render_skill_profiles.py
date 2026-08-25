from __future__ import annotations

import importlib.util
import re
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
MODULE_PATH = Path(__file__).with_name("render_skill_profiles.py")
SPEC = importlib.util.spec_from_file_location("render_skill_profiles", MODULE_PATH)
assert SPEC and SPEC.loader
renderer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(renderer)


def enabled_skills(path: Path) -> set[str]:
    return {
        skill
        for skill, enabled in re.findall(r'name = "([^"]+)"\nenabled = (true|false)', path.read_text())
        if enabled == "true"
    }


class RenderSkillProfilesTests(unittest.TestCase):
    def test_default_profile_enables_and_exposes_every_registered_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir)
            result = renderer.render_profiles(ROOT, output)

            self.assertEqual(result["profile_count"], 12)
            self.assertEqual(result["managed_skill_count"], 65)
            all_skills = enabled_skills(output / "base.config.toml")
            self.assertEqual(all_skills, renderer.registry_skill_names(ROOT))
            self.assertIn("intelligest", all_skills)
            hidden_from_default_prompt = sorted(
                skill_name
                for skill_name in all_skills
                if (metadata_path := ROOT / "skills" / skill_name / "agents" / "openai.yaml").is_file()
                and re.search(
                    r"(?m)^\s*allow_implicit_invocation:\s*false\s*$",
                    metadata_path.read_text(encoding="utf-8"),
                )
            )
            self.assertEqual(hidden_from_default_prompt, [])
            self.assertEqual(
                len(re.findall(r'^\[\[skills\.config\]\]$', (output / "base.config.toml").read_text(), re.MULTILINE)),
                len(all_skills),
            )
            self.assertIn("intelligest", result["profiles"]["deep-researcher"])
            self.assertIn("content-impl-plan", result["profiles"]["content-specialist"])

            for profile_name, expected_skills in result["profiles"].items():
                profile_path = output / "profiles" / f"{profile_name}.config.toml"
                self.assertTrue(profile_path.is_file())
                content = profile_path.read_text()
                self.assertTrue(content.startswith(renderer.PROFILE_MARKER_BEGIN))
                self.assertTrue(content.rstrip().endswith(renderer.PROFILE_MARKER_END))
                self.assertEqual(enabled_skills(profile_path), set(expected_skills))
                self.assertEqual(
                    len(re.findall(r'^\[\[skills\.config\]\]$', content, re.MULTILINE)),
                    result["managed_skill_count"],
                )

    def test_unknown_manifest_skill_blocks_render_before_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / "docs/skills").mkdir(parents=True)
            (root / "rules").mkdir()
            (root / "docs/skills/registry.jsonl").write_text('{"name":"known"}\n')
            (root / "rules/skill-profiles.toml").write_text('[profiles]\nexample = ["missing"]\n')

            with self.assertRaisesRegex(renderer.ProfileRenderError, "missing_from_registry"):
                renderer.render_profiles(root, root / "rendered")


if __name__ == "__main__":
    unittest.main()
