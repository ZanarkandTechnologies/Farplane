# Terminal Scroll Landing Review

Use this domain rubric for Terminal/Terminus-inspired, premium industrial,
cinematic, generated-media, or scroll-scrubbed landing pages. It complements the
general `review` skill: general review owns the anchored verdict shape, while
this file defines landing-page-specific evidence, scoring dimensions, and
failure modes.

## Score Contract

Report both:

- `percent_score`: `0`-`100`, with `80` as the pass threshold for serious
  Terminal-style self-improvement experiments.
- `anchored_score`: `1.0`-`5.0`, mapped from the percent score for compatibility
  with the review skill.

Mapping:

- `0-39`: `1.0` failing or absent
- `40-59`: `2.0` partially relevant but not trustable
- `60-74`: `3.0` directionally correct but still ordinary
- `75-89`: `4.0` strong and defendable with minor caveats
- `90-100`: `5.0` exemplary within scope

Overall verdict:

- `pass`: `percent_score >= 80` and no hard gates fail
- `revise`: `50 <= percent_score < 80` or a non-critical hard gate fails
- `block`: unsafe, wrong target, destructive, or no runnable page

## Required Evidence

- Built page URL or `index.html`
- `SPEC.md` or landing brief
- `assets/asset-manifest.json` when final quality is claimed
- Desktop scroll-scrub QA JSON and checkpoint screenshots
- Mobile scroll-scrub QA JSON and checkpoint screenshots
- Reduced-motion proof when animation is required
- Delegated run prompt, stdout/stderr logs, handoff, `first_write.json`, and
  session-file list when the page came from an external CLI

## Dimensions

### 1. Strategy And Spec, 20 points

Judges whether the page followed the landing-page todo recipe before build.

- competitor or inspiration matrix
- chosen primary reference and reason
- user story and buyer job
- section-count decision
- low-fidelity ASCII flow
- nested `advise` decisions and rejected options
- phase-aware implementation handoff

Hard gate: A Terminal-style build that skipped spec/story planning cannot pass
above `70`, even when it has a plausible visual.

### 2. Asset Pipeline, 20 points

Judges whether the page uses real or generated/rendered media as a story carrier.

- generated/rendered hero video or frame sequence
- poster and reduced-motion still
- mobile-specific crop or variant
- support assets for non-hero sections
- local asset manifest with source prompts and safe paths
- readable text kept in HTML/CSS overlays

Hard gate: `code-native-canvas` or decorative SVG-only media is prototype
evidence and cannot pass above `65` for final Terminal parity.

### 3. Scroll-Scrub Mechanics, 25 points

Judges whether scroll actually drives media or timeline state.

- `data-scroll-scrub-root`
- `window.__scrollScrubDebug`
- progress, phase, frame or `mediaTime`, active, ready, reducedMotion
- debug/media/style scrub changes across checkpoints
- pinned or ScrollTrigger/GSAP signal when claimed
- distributed screenshot deltas across the hero narrative
- `terminalVerdict: PASS` for final readiness

Hard gate: A static page, fake scroll, or normal section scrolling cannot pass
above `60`.

### 4. Visual Craft And Enterprise Trust, 15 points

Judges whether the page feels like a serious premium industrial product, not a
generic dark SaaS mockup.

- physical-world operation dominates the first viewport
- initial hero headline or offer copy is visible before the first scroll
- product/category signal appears early
- restrained enterprise nav and CTA
- typography hierarchy and dense technical labels feel deliberate
- media crop avoids dead blank bands
- proof sections feel buyer-relevant rather than decorative

### 5. Mobile And Reduced Motion, 10 points

Judges production readiness outside the desktop hero.

- mobile first viewport is deliberately cropped
- H1 and CTA fit without overlap
- multi-phrase hero titles keep visible phrase separation
- reduced-motion path is coherent
- asset and interaction fallbacks work

### 6. Delegation Process Evidence, 10 points

Judges whether an external CLI run is observable and safe to learn from.

- prompt and command captured
- stdout/stderr logs captured
- session files captured when the adapter produces them
- `first_write.json` passes for owned implementation outputs
- handoff includes changed files, verification, risks, loaded skills, and next
  phase recommendation
- timed-out partial runs are marked as failures rather than accepted

Hard gate: A delegated build with no observable output, no first-write proof,
or a placeholder handoff cannot pass above `70` as a self-improvement fixture.

## Mechanical Runner

Use:

```bash
python3 skills/landing-page/scripts/terminal_landing_score.py \
  --site-dir <site-dir> \
  --desktop-qa <desktop-scroll-scrub-qa.json> \
  --mobile-qa <mobile-scroll-scrub-qa.json> \
  --delegate-run-dir <optional-external-cli-run-dir> \
  --out <score.json>
```

The runner is intentionally a proxy metric. It does not replace human visual
review; it makes the self-improvement loop honest enough to decide whether a
new prompt or skill change improved the observable artifact.

## Review Output

Return the normal review structure plus:

- `terminal_scroll_percent`
- `terminal_scroll_threshold`
- `terminal_scroll_dimensions`
- `terminal_scroll_hard_gates`
- `terminal_scroll_next_action`

If score is below `80`, the next action should name the smallest repairable
dimension, such as `spec recipe`, `asset manifest`, `scroll mechanics`,
`mobile`, or `delegation evidence`.
