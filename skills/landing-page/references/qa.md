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
- Three.js scenes have visible lighting/materials, sane mobile framing, lazy-load/off-screen behavior, and a static fallback.

## Scroll Checkpoints

For animation-heavy pages, use representative progress points:

- 0%
- 20-25%
- 50%
- 75%
- 95-100%

Add narrative-specific checkpoints when phases have named start/peak/end values.

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
