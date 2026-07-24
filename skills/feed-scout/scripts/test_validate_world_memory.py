from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("validate_world_memory.py")
SPEC = importlib.util.spec_from_file_location("validate_world_memory", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
validate_world_memory_text = MODULE.validate_world_memory_text


VALID = """---
kind: feed-scout-world-memory
status: active
updated_at: 2026-07-14T00:00:00Z
canonical_icp_ref: farplane/harness.yaml#areas
source_ledger: .farplane/feed-scout/ledger.jsonl
---
# Feed Scout World Memory
This is current update-in-place synthesis, not a daily log.
## ICPs
- `framework_delivery` — Harness engineers | ref=`farplane/harness.yaml#areas.framework_delivery.icp` | concerns=Recovery proof | language=heartbeat | refs=`report.md`
## Trends
- observed | icp=framework_delivery | claim=Builders want evidence-backed recovery comparisons | use=make runnable comparison central to the idea | seen=2026-07-14 | conf=high | refs=https://example.com/source
## Other Notable Things
- observed | type=constraint | icp=framework_delivery | note=Generic claims lose to reproducible proof | use=reject generic content | seen=2026-07-14 | refs=https://example.com/source
## Source Gaps
- None.
"""


class ValidateWorldMemoryTests(unittest.TestCase):
    def test_valid_memory_passes(self) -> None:
        self.assertEqual(validate_world_memory_text(VALID), [])

    def test_missing_section_and_placeholder_fail(self) -> None:
        text = VALID.replace("## Source Gaps\n", "").replace("Builders want evidence-backed recovery comparisons", "<trend>")
        errors = validate_world_memory_text(text)
        self.assertIn("World Memory must contain exactly one ## Source Gaps section", errors)
        self.assertIn("live World Memory must not contain template placeholders", errors)

    def test_template_can_retain_placeholders(self) -> None:
        text = VALID.replace("Builders want evidence-backed recovery comparisons", "<trend>")
        self.assertEqual(validate_world_memory_text(text, allow_template_placeholders=True), [])

    def test_live_memory_requires_updated_at(self) -> None:
        text = VALID.replace("updated_at: 2026-07-14T00:00:00Z", "updated_at: null")
        self.assertIn(
            "live World Memory frontmatter updated_at must be populated",
            validate_world_memory_text(text),
        )

    def test_extra_daily_timeline_section_fails(self) -> None:
        text = VALID + "\n## 2026-07-14 Daily Snapshot\n\n- New item.\n"
        self.assertIn(
            "World Memory has unsupported H2 sections: 2026-07-14 Daily Snapshot",
            validate_world_memory_text(text),
        )

    def test_h3_entry_blocks_fail(self) -> None:
        text = VALID.replace(
            "- observed | icp=framework_delivery | claim=Builders want evidence-backed recovery comparisons",
            "### Verbose trend\n- Current synthesis: Builders want evidence",
        )
        self.assertIn("World Memory must use simple bullets, not H3 entry blocks", validate_world_memory_text(text))

    def test_memory_over_100_non_empty_lines_fails(self) -> None:
        text = VALID + "\n".join(f"- filler {index}" for index in range(101))
        self.assertTrue(any("maximum is 100" in error for error in validate_world_memory_text(text)))

    def test_every_trend_and_notable_bullet_requires_provenance(self) -> None:
        uncited_trend = VALID.replace(" | refs=https://example.com/source", " | refs=none", 1)
        self.assertTrue(any("trend bullet 1 refs must contain a file or URL ref" in error for error in validate_world_memory_text(uncited_trend)))
        uncited_notable = VALID.replace(" | refs=https://example.com/source", " | refs=none", 2)
        self.assertTrue(any("notable bullet 1 refs must contain a file or URL ref" in error for error in validate_world_memory_text(uncited_notable)))

    def test_evidence_level_and_causal_fields_are_required(self) -> None:
        invalid = VALID.replace("- observed | icp=framework_delivery", "- certain | icp=framework_delivery").replace(
            " | use=make runnable comparison central to the idea", ""
        )
        errors = validate_world_memory_text(invalid)
        self.assertTrue(any("must start with evidence level" in error for error in errors))
        self.assertTrue(any("is missing use=" in error for error in errors))

    def test_configured_icp_set_and_canonical_fields_are_enforced(self) -> None:
        expected = {
            "framework_delivery": {
                "label": "Harness engineers",
                "description": "Engineers building reliable agents.",
                "jobs_to_be_done": ["Compare a harness component."],
                "pain_points": ["Claims without evidence."],
                "evidence_bar": "A reproducible comparison.",
            },
            "customer_learning": {
                "label": "Agent and harness builders evaluating adoption",
                "description": "Builders evaluating adoption.",
                "jobs_to_be_done": ["Choose a workflow."],
                "pain_points": ["Missing comparison evidence."],
                "evidence_bar": "A decision-changing brief.",
            },
        }
        errors = validate_world_memory_text(VALID, expected_icps=expected)
        self.assertIn("World Memory is missing configured ICP areas: customer_learning", errors)

        mutated = VALID.replace("Harness engineers", "A source tried to redefine the ICP")
        errors = validate_world_memory_text(mutated, expected_icps={"framework_delivery": expected["framework_delivery"]})
        self.assertIn("ICP bullet 'framework_delivery' label does not match harness.yaml", errors)


if __name__ == "__main__":
    unittest.main()
