# Modern Scroll-Scrub Landing Todo Recipe

Use this checklist for modern, premium, Terminal/Terminus-inspired, cinematic,
asset-heavy, or scroll-scrubbed landing pages. Treat it as the ordered recipe:
do not jump to implementation before the story, section plan, effect choices,
and asset plan exist.

## 1. Ground The Reference Set

- [ ] Identify the product, category, buyer, and promised transformation in one
  sentence.
- [ ] Collect 3-5 competitor or inspiration references, including the user's
  supplied reference when available.
- [ ] Extract from each reference:
  - [ ] section order,
  - [ ] hero media type,
  - [ ] scroll or motion behavior,
  - [ ] copy posture,
  - [ ] proof and CTA pattern,
  - [ ] asset types worth adapting.
- [ ] Use `advise` to choose one primary inspiration and one or two supporting
  references. Record why the primary wins for this product.

## 2. Choose The Page Story

- [ ] Decide the minimum section set before planning visuals. Default to:
  `Hero -> Problem -> Solution -> CTA`.
- [ ] Add optional sections only when the offer earns them:
  `Logos`, `Proof`, `Use cases`, `Comparison`, `Reviews`, `Security`,
  `Pricing`, or `Contact`.
- [ ] Write the user story in plain language:
  - [ ] who arrives,
  - [ ] what pain or ambition they bring,
  - [ ] what they must understand in the first 10 seconds,
  - [ ] what proof makes them trust the product,
  - [ ] what action the page asks for.
- [ ] Draft the low-fidelity page flow in ASCII Markdown before generating
  assets or writing code.

```text
[Hero: scroll-scrubbed generated video / frame sequence]
  beat 0: current world
  beat 1: problem becomes visible
  beat 2: product intelligence layer appears
  beat 3: outcome state and CTA

[Problem]
  job: make the cost of the old world obvious
  visual carrier: ...

[Solution]
  job: show the new operating model
  visual carrier: ...

[CTA]
  job: convert the now-convinced buyer
  visual carrier: ...
```

## 3. Run Nested Advise Per Section

For every section, answer these questions before choosing the implementation.
Use `advise` for each question, asking for exactly 3 options, a recommendation,
and the tradeoff accepted.

- [ ] What WebGL effect belongs here?
- [ ] What pretext / framing / copy idea belongs here?
- [ ] What HTML-in-canvas visualization belongs here?
- [ ] What Three.js idea belongs here?
- [ ] What Spline idea belongs here?
- [ ] What asset options belong here?

After the nested pass:

- [ ] Choose one primary visual/effect direction for the section.
- [ ] Reject the unused options explicitly so the implementation does not stack
  every cool idea at once.
- [ ] Record the section contract:
  `job`, `copy beat`, `visual carrier`, `motion`, `asset`, `fallback`, and
  `QA proof`.

## 4. Plan The Hero Scroll-Scrub Asset Pipeline

The first section is the attention capture. In this recipe, the hero is a
scroll-scrubbed visual built from generated or rendered media unless the brief
explicitly downgrades the page to a non-cinematic scope. A static decorative
image is only a prototype fallback.

- [ ] Write the hero video prompt from the story beats and product world.
- [ ] Keep readable headlines, CTAs, labels, logos, and product copy in HTML
  overlays, not baked into generated pixels.
- [ ] Generate or render source hero video relevant to the product theme using
  the repo's media workflow, such as `video-generation` or another configured
  inference.sh video skill.
- [ ] Plan any still or support assets through `image-generation`,
  `video-generation`, Remotion, real product capture, or a named project asset
  source; do not leave asset origin implicit.
- [ ] Produce desktop and mobile crops or variants.
- [ ] Produce a poster frame and reduced-motion still.
- [ ] Convert the source video into a scrub-friendly asset:
  - [ ] preferred: frame sequence with a manifest,
  - [ ] alternate: all-I-frame/keyframe-only video for media-time scrubbing.
- [ ] Verify asset files exist before implementation.

Useful commands to include in the asset plan:

```bash
ffmpeg -i hero-source.mp4 -vf "fps=30,scale=1920:-2:flags=lanczos" -q:v 75 public/frames/hero/desktop/frame_%04d.webp
ffmpeg -i hero-source.mp4 -c:v libx264 -preset slow -crf 18 -g 1 -keyint_min 1 -sc_threshold 0 -an public/video/hero-scrub-all-i.mp4
```

## 5. Build The Spec Before The Page

- [ ] Write or update `SPEC.md` before implementation for cinematic or
  Terminal-style pages.
- [ ] Include the competitor matrix, chosen inspiration, user story, ASCII page
  flow, nested `advise` decisions, section contracts, asset manifest plan,
  motion plan, fallback plan, and QA plan.
- [ ] Use `advise` one final time on the complete ASCII/spec plan to compare:
  - [ ] conservative production plan,
  - [ ] cinematic scroll plan,
  - [ ] maximal experimental plan.
- [ ] Choose the strongest plan that can be built and proved in the available
  scope.

## 6. Assemble And Instrument

- [ ] Build the page from the spec and asset manifest.
- [ ] Implement the hero scroll scrub with GSAP ScrollTrigger, a frame mapper,
  media-time scrubbing, WebGL, Three.js, or the selected effect stack.
- [ ] Expose `data-scroll-scrub-root` on the scrubbed stage.
- [ ] Expose `window.__scrollScrubDebug` with:
  `progress`, `phase`, `frame` or `mediaTime`, `active`, `ready`, and
  `reducedMotion`.
- [ ] Keep text in accessible HTML; use canvas/WebGL/video for the visual
  carrier, not the readable message.
- [ ] Include reduced-motion behavior and mobile-specific crop/framing.

## 7. Verify And Repair

- [ ] Run visual QA on desktop and mobile first viewports.
- [ ] Run scroll-scrub QA:

```bash
NODE_PATH=$CODEX_NODE_MODULES $CODEX_NODE skills/landing-page/scripts/scroll_scrub_qa.cjs --url <page-url-or-html-file> --out <qa-dir>
```

- [ ] For Terminal/Terminus-level pages, require `terminalVerdict: PASS`, not
  only basic `verdict: PASS`.
- [ ] Confirm checkpoint screenshots show meaningful visual changes in the main
  media surface, not just text or HUD movement.
- [ ] Confirm support sections have their own assets, not only the hero asset.
- [ ] Compare against the primary inspiration and write the gap:
  `media fidelity`, `first viewport`, `scroll motion`, `copy`, `proof`,
  `mobile`, and `CTA`.
- [ ] Repair the smallest failing layer, then rerun QA.

## Required Handoff

- [ ] Competitor/inspiration matrix.
- [ ] Final chosen recipe, taste profile, and effect stack when applicable.
- [ ] ASCII page flow.
- [ ] Per-section nested `advise` decisions and rejections.
- [ ] Asset manifest with generated/rendered media, frames, posters, fallbacks,
  and support assets.
- [ ] Implementation file map.
- [ ] Desktop and mobile screenshots.
- [ ] Scroll-scrub QA JSON and checkpoint screenshot directory.
- [ ] Final gap analysis against the primary inspiration.
