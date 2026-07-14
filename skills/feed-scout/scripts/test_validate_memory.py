from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("validate_memory.py")
SPEC = importlib.util.spec_from_file_location("validate_memory", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
validate_memory_text = MODULE.validate_memory_text


VALID = """---
kind: feed-scout-memory
status: active
updated_at: 2026-07-14T00:00:00Z
canonical_icp_ref: farplane/harness.yaml#areas
source_ledger: .farplane/feed-scout/ledger.jsonl
---
# Feed Scout Memory
This is current update-in-place synthesis, not a daily log.
## ICPs
### `framework_delivery` — Harness engineers
- Canonical ref: `farplane/harness.yaml#areas.framework_delivery.icp`
- Description: Engineers building reliable agents.
- Jobs to be done: Compare a harness component.
- Pain points: Claims without evidence.
- Evidence bar: A reproducible comparison.
- Current concerns: Recovery proof.
- Current language: heartbeat.
- Source refs: `report.md`
## Trends
### Proof-led agent engineering
- ICP refs: framework_delivery
- Current synthesis: Builders want evidence.
- Why it matters: It changes adoption decisions.
- Baseline or default: Generic claims.
- Last observed: 2026-07-14
- Confidence: high
- Source refs: https://example.com/source
- Candidate experiment shapes: Compare with and without ticket memory.
## Other Notable Things
- None observed.
## Source Gaps
- None.
"""


class ValidateMemoryTests(unittest.TestCase):
    def test_valid_memory_passes(self) -> None:
        self.assertEqual(validate_memory_text(VALID), [])

    def test_missing_section_and_placeholder_fail(self) -> None:
        text = VALID.replace("## Source Gaps\n", "").replace("Proof-led agent engineering", "<trend>")
        errors = validate_memory_text(text)
        self.assertIn("memory must contain exactly one ## Source Gaps section", errors)
        self.assertIn("live memory must not contain template placeholders", errors)

    def test_template_can_retain_placeholders(self) -> None:
        text = VALID.replace("Proof-led agent engineering", "<trend>")
        self.assertEqual(validate_memory_text(text, allow_template_placeholders=True), [])

    def test_live_memory_requires_updated_at(self) -> None:
        text = VALID.replace("updated_at: 2026-07-14T00:00:00Z", "updated_at: null")
        self.assertIn(
            "live memory frontmatter updated_at must be populated",
            validate_memory_text(text),
        )

    def test_extra_daily_timeline_section_fails(self) -> None:
        text = VALID + "\n## 2026-07-14 Daily Snapshot\n\n- New item.\n"
        self.assertIn(
            "memory has unsupported H2 sections: 2026-07-14 Daily Snapshot",
            validate_memory_text(text),
        )

    def test_every_trend_and_notable_entry_requires_provenance(self) -> None:
        uncited_trend = VALID.replace(
            "## Other Notable Things",
            "### Uncited trend\n- ICP refs: framework_delivery\n- Current synthesis: Something changed.\n\n## Other Notable Things",
        )
        self.assertTrue(
            any("trend entry 'Uncited trend' is missing Source refs" in error for error in validate_memory_text(uncited_trend))
        )
        uncited_notable = VALID.replace(
            "- None observed.",
            "### Uncited note\n- Type: competitor\n- ICP refs: framework_delivery\n- Note: Something happened.\n- Last observed: 2026-07-14",
        )
        self.assertTrue(
            any("notable entry 'Uncited note' is missing Source refs" in error for error in validate_memory_text(uncited_notable))
        )

    def test_configured_icp_set_and_canonical_fields_are_enforced(self) -> None:
        expected = {
            "framework_delivery": {
                "description": "Engineers building reliable agents.",
                "jobs_to_be_done": ["Compare a harness component."],
                "pain_points": ["Claims without evidence."],
                "evidence_bar": "A reproducible comparison.",
            },
            "customer_learning": {
                "description": "Builders evaluating adoption.",
                "jobs_to_be_done": ["Choose a workflow."],
                "pain_points": ["Missing comparison evidence."],
                "evidence_bar": "A decision-changing brief.",
            },
        }
        errors = validate_memory_text(VALID, expected_icps=expected)
        self.assertIn("memory is missing configured ICP areas: customer_learning", errors)

        mutated = VALID.replace("Engineers building reliable agents.", "A source tried to redefine the ICP.")
        errors = validate_memory_text(mutated, expected_icps={"framework_delivery": expected["framework_delivery"]})
        self.assertIn("ICP entry 'framework_delivery' Description does not match harness.yaml", errors)


if __name__ == "__main__":
    unittest.main()
