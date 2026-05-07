# Spec-First Cinematic Industrial Gate

Use this reference for Terminal Industries-style logistics, infrastructure,
industrial AI, mission-control, or premium cinematic landing pages.

## Why This Gate Exists

Terminal-style pages fail when the agent treats the site as ordinary HTML/CSS
polish. The reference quality comes from a first-viewport physical operation,
real or generated media, careful crop direction, restrained enterprise copy,
and visual QA against screenshots. A broad "plan and build everything" prompt
often produces mismatched HTML/CSS/JS, missing assets, and no final review.

## Phase Contract

1. `spec`: produce or update `SPEC.md`; do not build yet unless a spec already
   exists and the current prompt explicitly asks for a later phase.
2. `assets`: generate or create only the assets named by the spec, then verify
   every referenced URL/file returns 200.
3. `implementation`: build in bounded file slices. Prefer `index/html shell`,
   `styles/assets`, `motion/js`, then `integration repair` over one giant pass.
4. `visual-review`: render screenshots, compare against the gold reference, run
   mobile and reduced-motion checks, then write the improvement hypothesis.

## Required Spec Contents

- `Offer`, `Audience`, and `Carrier object / world`.
- `Recipe route`: recipe, taste-profile, and effect-stack IDs.
- Section map with first-viewport, proof, and final CTA.
- Asset generation plan with:
  - desktop hero media or frame sequence,
  - mobile hero media or frame sequence,
  - poster frame,
  - reduced-motion still,
  - support loops or section stills,
  - `assets/asset-manifest.json`,
  - source prompts for generated media,
  - a rule that readable text, logos, CTAs, and product copy stay in HTML/CSS
    overlays, not generated pixels.
- Motion plan with scroll checkpoints and reduced-motion behavior.
- Scroll-scrub instrumentation contract:
  - mark the scrubbed stage with `data-scroll-scrub-root`,
  - expose `window.__scrollScrubDebug` with `progress`, `phase`, `frame` or
    `mediaTime`, `active`, `reducedMotion`, and `ready`,
  - document how each checkpoint maps to narrative state,
  - keep the debug object available in production builds unless the ticket
    explicitly scopes a removal pass.
- File map and implementation slices.
- Visual QA plan with desktop, mobile, full-page, asset-load, and no-overlap
  checks.
- Gold-reference comparison checklist if a reference URL or screenshots exist.

## Terminal Gold Checklist

Pass only when the first viewport has all of these:

- A physical-world object or operation dominates the screen.
- The media reads as photographic, rendered, or intentionally art-directed,
  not generic SVG filler.
- The nav and CTA are enterprise-serious and immediately usable.
- The main product/category signal appears early without hiding the object.
- Mobile has its own deliberate crop, not a shrunken desktop composition.
- There is a hint of the next section without a dead blank band.

## External Builder Rules

- Do not attach large gold screenshots to implementation passes after the spec
  has summarized them. Attach screenshots to visual-review passes.
- Every builder prompt must name exactly one phase and the files it may touch.
- External CLI implementation prompts should be run with `--expect-output` for
  the owned files so `first_write.json` proves the builder produced an artifact
  before self-review.
- Ask builders to run concrete checks before handoff: `ls`, syntax checks, asset
  existence checks, and screenshots when a browser is available.
- For scroll-scrub implementations, ask builders to run:
  `NODE_PATH=$CODEX_NODE_MODULES $CODEX_NODE skills/landing-page/scripts/scroll_scrub_qa.cjs --url <page> --out <qa-dir>`
  or the local equivalent with the bundled Codex Node runtime.
- For Terminal/Terminus-level final builds, require generated/rendered media or
  frame/video assets in `assets/asset-manifest.json`. `code-native-canvas` is
  acceptable only for a mechanics prototype and should fail final visual parity.
- A timed-out run with partial files is a failure, even when the page appears to
  render. Record it and split the next prompt smaller.

## Comparison Output

After a visual-review phase, write:

- `gold reference`: screenshots or URL used.
- `observed output`: screenshots and files reviewed.
- `Terminal gap`: first viewport, media quality, physical operation, crop,
  typography, motion, proof, mobile, and asset pipeline.
- `scroll-scrub proof`: link the `scroll-scrub-qa.json`, five checkpoint
  screenshots, and whether debug/media/style/pinned checks passed.
- `skill improvement hypothesis`: the smallest rule or eval that would have
  prevented the miss.
