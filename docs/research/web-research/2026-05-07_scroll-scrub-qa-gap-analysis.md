# Scroll-Scrub QA Gap Analysis

Date: 2026-05-07

## Capability + User

Capability: make the `landing-page` and Pi/Kimi frontend delegation workflow
consistently produce Terminal Industries-style cinematic industrial landing
pages with verifiable scroll-scrub behavior.

User: Codexter operator delegating premium frontend work to an external CLI
agent and needing proof that the result is not merely static SaaS layout plus
fade-up animations.

## Parity Baseline

Reference: https://terminal-industries.com/

Observed parity signals from the live site and bundle research:

- Nuxt app shell with Lenis smooth scrolling.
- GSAP/ScrollTrigger choreography.
- Canvas/video-sequence style media driven by progress.
- Separate desktop/mobile media assets.
- Oversized editorial hero, physical yard/logistics operation, proof modules,
  named quote, logos, and high-intent CTAs.

Measured with `skills/landing-page/scripts/scroll_scrub_qa.cjs`:

- `scroll-qa-terminal-gold`: `PASS`
- `hasMediaScrub: true`
- `hasStyleScrub: true`
- `videoTimeSpan: 0.827`
- checkpoint screenshots show large visual deltas across scroll positions.

## Current State

Prior generated output:

- `.harness/warehouse-cv-terminal-style/index.html`
- `.harness/warehouse-cv-terminal-style/app.js`
- `.harness/warehouse-cv-terminal-style/styles.css`

Measured with the same harness:

- `scroll-qa-warehouse-prior`: `FAIL`
- `hasDebugInstrumentation: false`
- `hasDebugScrub: false`
- `hasMediaScrub: false`
- `hasPinnedSurface: false`
- `hasGsapOrScrollTrigger: false`

The prior page has some moving/revealed content, but it does not prove a
scroll-scrubbed media stage. Its `app.js` is primarily IntersectionObserver
reveal, nav state, menu, smooth anchors, and form feedback.

## Runtime Debugging

### Symptom

A delegated build can look more polished than plain HTML while still failing
the actual Terminal-style requirement: scroll should drive a pinned media,
timeline, video, canvas, or frame-sequence state.

### Repro Path

1. Run the scroll QA harness on the reference site.
2. Run the same harness on the generated site.
3. Compare debug, media, style, pinned, and checkpoint screenshot signals.

### Hypotheses

1. The prompt says "scroll" but does not require measurable runtime state.
   Prediction: output uses IntersectionObserver or CSS transitions, and the QA
   result lacks debug/media/pinned signals.
2. The skill recipe describes frame sequences but does not require a browser
   proof artifact.
   Prediction: output may claim cinematic scroll without any `ScrollTrigger`,
   media time, frame index, or checkpoint evidence.
3. The builder avoids generated media complexity by substituting SVG/card
   visuals.
   Prediction: screenshots change only because page sections scroll into view,
   not because one anchored scene progresses.

### Root Cause

The existing landing recipe and external Pi prompt were too qualitative. They
encouraged Terminal-style outputs, but did not make scroll-scrub instrumentation
and browser QA a hard acceptance gate.

## Gap Analysis

### Production Expectation

A credible Terminal-style cinematic landing page must include:

- one dominant physical operation/world in the first viewport,
- one scroll-linked major section with pinned or anchored media/timeline state,
- explicit desktop/mobile choreography,
- debug surface for scroll progress, phase, frame/media time, readiness, and
  reduced-motion,
- proof modules beyond abstract claims,
- browser evidence at 0%, 25%, 50%, 75%, and 95% scroll checkpoints.

### Missing Gaps

- No reusable harness existed to distinguish real scroll scrub from normal
  scrolling.
- The spec gate did not require `window.__scrollScrubDebug`.
- Pi profile instructions did not explicitly reject IntersectionObserver-only
  output as "not scroll-scrub."
- The recipe QA expectation did not name a machine-checkable scroll-scrub gate.
- Prior output lacked pinned/GSAP/media/frame instrumentation.

## Advice Decision

Decision: how to make the skill/sub-agent reliably better at this class.

Options:

1. Prompt-only improvement.
   - Pros: fastest, minimal code.
   - Cons: easy for the agent to ignore or satisfy rhetorically.
2. Hard QA gate plus debug contract.
   - Pros: measurable, repeatable, catches fake scroll implementations.
   - Cons: adds one required instrumentation surface to every cinematic build.
3. Full generated-video pipeline only.
   - Pros: closest to Terminal media quality.
   - Cons: expensive, slower, and still needs debug/QA to prove scroll linkage.

Recommendation: use option 2 now. Require the debug contract and QA harness for
every Terminal-style scroll build, then add generated video/frame assets as a
separate asset-quality upgrade once the motion contract is reliable.

## Implemented Skill Fix

- Added `skills/landing-page/scripts/scroll_scrub_qa.cjs`.
- Updated `landing-page` QA and cinematic spec gate to require
  `data-scroll-scrub-root` and `window.__scrollScrubDebug`.
- Updated recipe/effect-stack records to require scroll QA proof.
- Updated Pi/Kimi profile instructions to reject IntersectionObserver-only
  output for scroll-scrub claims.
- Added delegate CLI `--prompt-file` support for precise phase prompts.
- Added delegate CLI `--expect-output` plus `first_write.json` so live
  implementation/repair runs prove the external agent created or modified an
  owned artifact before broad self-review.

## Next QA Loop

1. Ask Pi/Kimi to build a fresh `.harness/warehouse-cv-scrollscrub-pi` page with
   the stricter recipe.
2. Run `scroll_scrub_qa.cjs` against that output.
3. If it fails, inspect `app.js`, generated prompt, and handoff logs.
4. Patch the smallest missing rule or prompt instruction.
5. Repeat until the page passes scroll-scrub instrumentation and visual
   checkpoints.
