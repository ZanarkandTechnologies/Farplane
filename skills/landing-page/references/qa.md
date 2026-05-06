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
- the page has large enough scroll range for the claimed choreography,
- at least one of debug scrub, media scrub, or pinned style scrub passes,
- checkpoint screenshots at `0`, `25`, `50`, `75`, and `95` percent map to
  distinct intended narrative states,
- reduced-motion still renders a coherent page without scroll-scrub dependency.

Fail if the page only changes because normal sections scroll into view while
the hero/stage itself has no debug, media, frame, pinned, or GSAP/ScrollTrigger
signal.
