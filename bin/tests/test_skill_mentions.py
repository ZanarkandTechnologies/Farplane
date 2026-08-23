from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME_DIR = ROOT / "bin" / "runtime"
if str(RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(RUNTIME_DIR))

from skill_registry import extract_skill_mentions, load_skill_registry
from user_turn import extract_control_surfaces


class SkillMentionTests(unittest.TestCase):
    def test_control_surfaces_and_registered_mentions_are_unique(self) -> None:
        text = "First $impl-plan TASK-0160, then $qa and $close-ticket. Please do not double count $qa."

        self.assertEqual(extract_control_surfaces(text), ["impl-plan", "qa", "close-ticket"])
        self.assertEqual(extract_skill_mentions(text), ["impl-plan", "qa", "close-ticket"])

    def test_control_surfaces_accept_linked_syntax_but_stay_narrow(self) -> None:
        text = (
            "Run [$brainstorm](/tmp/brainstorm/SKILL.md), $QA, and "
            "[$unslop](/tmp/unslop/SKILL.md), not /tmp/$qa or foo.$demo."
        )

        self.assertEqual(extract_control_surfaces(text), ["brainstorm", "qa"])

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
                json.dumps({"name": "lean-check", "source": "local"}) + "\n",
                encoding="utf-8",
            )
            registry = load_skill_registry(project_root)
            mentions = extract_skill_mentions(
                "$LEAN-CHECK [$lean-check](/skills/lean-check/SKILL.md) "
                "$lean-check-extra x$lean-check /tmp/$lean-check foo.$lean-check "
                "[$lean-check](/skills/lean-check/README.md) $unknown",
                registry=registry,
            )

        self.assertEqual(mentions, ["lean-check"])

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
