#!/usr/bin/env python3
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import landing_spec_lint


VALID_SPEC = """---
status: approved
approval_source: user
landing_type: cinematic-scrolltelling
quality_target: terminal-level
---

# LANDING_SPEC

## Offer
Terminus gives warehouse camera networks a real-time computer vision command layer.

## Audience
Enterprise logistics and warehouse operations buyers evaluating AI visibility.

## Non-goals
Do not build a dashboard, pricing page, or generic SaaS gradient site.

## Decision Boundaries
The agent may choose concrete section copy, visual layout, and fallback details
as long as they preserve the approved narrative and QA gates.

## Taste References
Terminal-style industrial scrolltelling, Palantir-style density, and restrained
enterprise operations copy.

## Reference Research
Terminal uses cinematic industrial assets and pinned scroll; peer enterprise
sites use concrete product imagery, proof metrics, and governance-safe claims.

## Best-of-worlds Decisions
Adopt full-bleed asset-led hero, adapt operational proof ladders, reject generic
gradient SaaS cards, and defer customer logo proof until supplied.

## Unique Take
Make the page feel like a live operational mission brief rather than a feature
catalog or generic AI dashboard.

## Narrative Arc
World with eyes -> operational blind spots -> command layer -> mission proof ->
credible enterprise CTA.

## Low-fi ASCII Flow
Hero warehouse video -> problem pane -> platform topology -> missions -> proof -> CTA.

## Section Matrix
| Section | User job | Narrative claim | Visual carrier | Asset plan | Motion/effect | Proof/copy payload | QA assertion |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Hero | Understand category | Existing cameras become intelligence | Full-bleed warehouse video | Generated desktop/mobile video | Scroll scrub with HUD | H1 and assessment CTA | first viewport and mobile proof |
| Problem | Feel pain | Walkthroughs miss incidents | Blind-spot canvas pane | Generated still or canvas | GSAP reveal | Loss/blind coverage metrics | rich visual block |
| Solution | See mechanism | Existing cameras connect fast | SVG topology | SVG/data overlay | draw lines on scroll | install and API bullets | rich visual block |
| Capabilities | Understand use cases | Three missions cover core ops | mission video/canvas panes | support videos | reveal and scrub support media | safety/throughput/compliance copy | every pane nonblank |
| Proof | Trust claims | Outcomes are measurable | metric and logo proof band | customer-safe proof data | counter reveal after scroll | credible metrics and quote | no placeholder metrics |
| CTA | Know next step | Assessment is the enterprise action | command grid canvas | stabilized still/canvas | ambient pulses | schedule and technical overview CTAs | final CTA screenshot |

## Asset Plan
Hero video, mobile fallback, support mission videos, proof-safe metric copy, and
reduced-motion stills.

## Product Demo Plan
Use a realistic product shot as the hero anchor, then show an assembly and
disassembly sequence with exploded parts that reveal the camera module, edge
compute core, mounting hardware, and key feature callouts.

## Motion Plan
Scroll-scrub hero, section reveal, support video entrance, and reduced-motion
static fallbacks.

## Proof Plan
Use plausible demo-safe metrics and identify any synthetic values as demo copy.

## Designer Judgment Plan
Score narrative clarity, section intentionality, visual authorship, motion
direction, proof credibility, and taste consistency.

## QA Gates
Run section quality, section_quality_qa, designer judgment, mobile,
reduced-motion, reduced motion, console, and runtime checks.

## Executor Handoff
Build from this matrix and do not add sections that are not represented here.
"""


class LandingSpecLintTests(unittest.TestCase):
    def write_spec(self, text: str) -> Path:
        tmp = tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".md", delete=False)
        with tmp:
            tmp.write(text)
        return Path(tmp.name)

    def test_valid_spec_passes(self) -> None:
        result = landing_spec_lint.lint_spec(self.write_spec(VALID_SPEC))
        self.assertEqual(result["verdict"], "PASS")
        self.assertEqual(result["findings"], [])

    def test_missing_approval_and_matrix_fail(self) -> None:
        bad = VALID_SPEC.replace("status: approved", "status: draft")
        bad = "\n".join(line for line in bad.splitlines() if not line.startswith("| CTA |"))
        result = landing_spec_lint.lint_spec(self.write_spec(bad))
        self.assertEqual(result["verdict"], "FAIL")
        self.assertIn("frontmatter status must be approved", result["findings"])
        self.assertIn("Section Matrix missing main section coverage: cta", result["findings"])

    def test_placeholder_fails(self) -> None:
        result = landing_spec_lint.lint_spec(self.write_spec(VALID_SPEC + "\nTODO\n"))
        self.assertEqual(result["verdict"], "FAIL")
        self.assertTrue(any("placeholder remains" in finding for finding in result["findings"]))

    def test_premium_product_spec_requires_product_demo_plan(self) -> None:
        bad = VALID_SPEC.replace(
            "\n## Product Demo Plan\nUse a realistic product shot as the hero anchor, then show an assembly and\n"
            "disassembly sequence with exploded parts that reveal the camera module, edge\n"
            "compute core, mounting hardware, and key feature callouts.\n",
            "\n",
        )
        result = landing_spec_lint.lint_spec(self.write_spec(bad))
        self.assertEqual(result["verdict"], "FAIL")
        self.assertIn("premium product specs require section: Product Demo Plan", result["findings"])


if __name__ == "__main__":
    unittest.main()
