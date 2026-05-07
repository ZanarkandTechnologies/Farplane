# Landing Page QA

## Screenshots

Capture:

- desktop first viewport,
- mobile first viewport,
- important section states,
- final CTA,
- scroll checkpoints for scrolltelling pages.

## Checks

- Product/place/object is visible in the first viewport when relevant.
- H1 and CTA fit on mobile.
- Text does not overlap media or controls.
- Assets load from workspace/project paths.
- Reduced-motion mode is usable.
- Canvas/WebGL scenes are nonblank and framed correctly.
- Every main narrative section has the thing users came to see: a heading,
  enough section copy, and the expected visual carrier rendered inside the
  section pane, not merely somewhere else on the page.
- Support sections are allowed to use ambient video, canvas, SVG, image, or
  HTML-in-canvas style data overlays, but blank bordered panels fail even when
  the hero scroll scrub passes.
- Proof metrics must not expose placeholder values such as `0M+`, `0×`, or
  `0%` at the moment a user sees the proof section.

## Scroll Checkpoints

For animation-heavy pages, use representative progress points:

- 0%
- 20-25%
- 50%
- 75%
- 95-100%

Add narrative-specific checkpoints when phases have named start/peak/end values.

## Section Quality Gate

For premium cinematic or Terminal-style landings, run a section-level QA pass in
addition to scroll-scrub mechanics:

```bash
NODE_PATH=/path/to/node_modules node skills/landing-page/scripts/section_quality_qa.cjs \
  --url <file-or-url> \
  --out <qa-dir>
```

The section-quality gate checks:

- expected section coverage: hero, problem, solution, capabilities, proof, CTA,
- text and heading presence for every main section,
- visible rich visual carriers for problem, solution, capabilities, and CTA,
- individual visual panes such as `.mission__visual`, `.cta__stage`, and
  `.rupture__canvas-wrap`,
- runtime page errors and browser console warnings,
- visible placeholder proof metrics.

Use this gate to catch the failure where a page earns a high hero/scroll score
but the lower sections still look empty, generic, or under-designed.

## Designer Judgment Gate

After mechanical checks pass, score the page with
`references/designer-judgment.md`. This is the final premium-quality pass for
the next 5% of improvement. It judges narrative clarity, section
intentionality, visual authorship, motion direction, proof credibility, and
taste consistency.

Real-life analogs this gate intentionally borrows from:

- conversion/key-event tracking for business outcomes,
- scroll-depth and heatmap review for section usefulness,
- expert heuristic review for usability and trust,
- guideline-weighted benchmark review for severity,
- accessibility/performance checks as hard hygiene gates.

For Codexter QA, the metric is not meant to replace real user analytics. It is
the same-session proxy that prevents agents from calling a page "premium"
before a skeptical designer would agree.
