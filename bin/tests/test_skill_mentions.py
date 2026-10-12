from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for RUNTIME_DIR in (ROOT / "bin" / "core",):
    if str(RUNTIME_DIR) not in sys.path:
        sys.path.insert(0, str(RUNTIME_DIR))

from skill_registry import extract_skill_mentions, load_skill_registry
from user_turn import extract_control_surfaces


class SkillMentionTests(unittest.TestCase):
    def test_control_surfaces_and_registered_mentions_are_unique(self) -> None:
        text = "First $impl-plan TASK-0160, then $qa, $frame and $demo. Please do not double count $qa."

        self.assertEqual(extract_control_surfaces(text), ["impl-plan", "qa", "frame", "demo"])
        self.assertEqual(extract_skill_mentions(text), ["impl-plan", "qa", "frame"])

    def test_control_surfaces_accept_linked_syntax_but_stay_narrow(self) -> None:
        text = (
            "Run [$frame](/tmp/frame/SKILL.md), $QA, and "
            "[$unslop](/tmp/unslop/SKILL.md), not /tmp/$qa or foo.$demo."
        )

        self.assertEqual(extract_control_surfaces(text), ["frame", "qa"])

    def test_registered_names_are_recognized(self) -> None:
        registry = load_skill_registry(ROOT)
        names = [str(record["name"]) for record in registry.records.values()]
        prompt = " ".join(f"[${name}](/skills/{name}/SKILL.md)" for name in names)

        self.assertEqual(registry.status, "loaded")
        self.assertEqual(extract_skill_mentions(prompt, registry=registry), names)

    def test_mentions_are_case_insensitive_deduped_and_exact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            registry_path = project_root / "docs" / "skills" / "registry.jsonl"
            registry_path.parent.mkdir(parents=True)
            registry_path.write_text(
                json.dumps({"name": "code-health", "source": "local"}) + "\n",
                encoding="utf-8",
            )
            registry = load_skill_registry(project_root)
            mentions = extract_skill_mentions(
                "$CODE-HEALTH [$code-health](/skills/code-health/SKILL.md) "
                "$code-health-extra x$code-health /tmp/$code-health foo.$code-health "
                "[$code-health](/skills/code-health/README.md) $unknown",
                registry=registry,
            )

        self.assertEqual(mentions, ["code-health"])

    def test_invalid_or_missing_registry_rejects_mentions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp)
            missing = load_skill_registry(project_root)
            self.assertEqual(missing.status, "missing")
            self.assertEqual(extract_skill_mentions("$qa", registry=missing), [])

            registry_path = project_root / "docs" / "skills" / "registry.jsonl"
            registry_path.parent.mkdir(parents=True)
            registry_path.write_text("{not-json}\n", encoding="utf-8")
            invalid = load_skill_registry(project_root)

        self.assertEqual(invalid.status, "invalid")
        self.assertEqual(extract_skill_mentions("$qa", registry=invalid), [])
