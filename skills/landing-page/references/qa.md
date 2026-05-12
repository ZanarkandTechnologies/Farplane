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
- Premium/cinematic pages pass asset-evidence lint; a section-quality pass does
  not prove generated or real media exists.
- Reduced-motion mode is usable.
- Canvas/WebGL scenes are nonblank and framed correctly.
- Scroll-scrub/pinned sections prove the pinned panel stays in the viewport at
  every checkpoint. Do not accept a test that only proves progress, labels, or
  video time advanced.
- Every main narrative section has the thing users came to see: a heading,
  enough section copy, and the expected visual carrier rendered inside the
  section pane, not merely somewhere else on the page.
- Support sections are allowed to use ambient video, canvas, SVG, image, or
  HTML-in-canvas style data overlays, but blank bordered panels fail even when
  the hero scroll scrub passes.
- Proof metrics must not expose placeholder values such as `0M+`, `0×`, or
  `0%` at the moment a user sees the proof section.
- Three.js scenes have visible lighting/materials, sane mobile framing, lazy-load/off-screen behavior, and a static fallback.

## Scroll Checkpoints

For animation-heavy pages, use representative progress points:

- 0%
- 20-25%
- 50%
- 75%
- 95-100%

Add narrative-specific checkpoints when phases have named start/peak/end values.

For pinned scroll sections, capture runtime fields for:

- requested progress,
- actual media time or frame source,
- active named beat,
- pinned panel viewport intersection,
- primary visual viewport intersection,
- screenshot/hash of the visual region.

If the page uses CSS sticky, verify no ancestor uses `overflow: hidden` or
`overflow-x: hidden` in a way that creates a scroll container and disables
sticky behavior. Prefer `overflow-x: clip` when the only goal is horizontal
clipping.

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

## Asset Evidence Gate

For premium, cinematic, Terminal-style, or generated-media pages, run:

```bash
python3 skills/landing-page/scripts/asset_evidence_lint.py <site-dir>
```

This gate checks `assets/asset-manifest.json` for at least one generated or real
filesystem-backed primary media asset with provenance and fallback evidence.
Canvas, SVG, WebGL, Three.js, and HTML/CSS visuals may support the page, but
they fail this gate when they are the only assets.

Use this gate to catch the failure where a page looks nonblank and scrolls, but
no image/video asset was actually generated or collected.

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
## Scroll-Scrub Instrumentation

For Terminal-style, cinematic-frame-sequence, GSAP ScrollTrigger, video-scrub,
or pinned-scroll pages, static screenshots are not enough. The implementation
must expose enough runtime state for QA to prove scroll actually drives media or
timeline state.

Required page hooks:

- `data-scroll-scrub-root` on the pinned/scrubbed stage,
- `window.__scrollScrubDebug.progress` from `0` to `1`,
- `window.__scrollScrubDebug.phase` for the active narrative beat,
- `window.__scrollScrubDebug.frame` or `mediaTime` for the current frame/media
  position,
- `window.__scrollScrubDebug.active`,
- `window.__scrollScrubDebug.ready`,
- `window.__scrollScrubDebug.reducedMotion`.

Run the bundled QA harness:

```bash
NODE_PATH=/Users/kenjipcx/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules \
/Users/kenjipcx/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node \
skills/landing-page/scripts/scroll_scrub_qa.cjs \
  --url <page-url-or-html-file> \
  --out <artifact-dir> \
  --label <short-label>
```

Acceptance signals:

- `verdict` is `PASS`,
- `hasRequiredDebugContract` is `true` for pages that expose a
  `data-scroll-scrub-root` stage,
- the page has large enough scroll range for the claimed choreography,
- at least one of debug scrub, media scrub, or pinned style scrub passes,
- checkpoint screenshots at `0`, `25`, `50`, `75`, and `95` percent map to
  distinct intended narrative states,
- Terminal/Terminus-level visual parity has large enough checkpoint screenshot
  deltas to feel cinematic; tiny HUD-only changes do not count,
- reduced-motion still renders a coherent page without scroll-scrub dependency.

Terminal/Terminus final-readiness signals:

- `terminalVerdict` is `PASS` and `score.terminalFinalReady` is `true`,
- `hasTerminalMediaPipeline` is `true`: media time changes with scroll, support
  videos exist, and mission/proof sections include support-video DOM,
- `hasDominantHeroMedia` is `true`: the first viewport has a large real media,
  frame, image, or marked hero-object surface with low blank-band geometry,
- `hasInitialHeroOfferVisible` is `true`: the primary hero headline or offer is
  visible before the visitor scrolls, not revealed only after scrub starts,
- `hasDistributedScrubDeltas` is `true`: checkpoint screenshot changes are
  large and distributed across the narrative, not only one HUD transition,
- `maxCheckpointChangedRatio`, `meaningfulCheckpointDeltaCount`,
  `strongCheckpointDeltaCount`, and `midScrollDeltaCount` are reported in the
  handoff,
- mobile runs preserve `hasMobileHeroPhraseSeparation` for multi-phrase hero
  headlines.

Use the basic `verdict` only for mechanics prototypes. A Terminal-style final
build can have `verdict: PASS` and still fail `terminalVerdict` when it lacks
real media, distributed visual change, or section-level support media.

Fail if the page only changes because normal sections scroll into view while
the hero/stage itself has no debug, media, frame, pinned, or GSAP/ScrollTrigger
signal.

## Terminal Review Score

For self-improvement experiments and delegated frontend runs, score the full
artifact with the domain review runner after scroll-scrub QA:

```bash
python3 skills/landing-page/scripts/terminal_landing_score.py \
  --site-dir <site-dir> \
  --desktop-qa <desktop-scroll-scrub-qa.json> \
  --mobile-qa <mobile-scroll-scrub-qa.json> \
  --delegate-run-dir <optional-external-cli-run-dir> \
  --out <score.json>
```

Use `references/terminal-scroll-review.md` for the dimension definitions. A
score of `80` or higher is the mechanical pass target for Terminal/Terminus
self-improvement loops, pending human visual review against the gold reference.
