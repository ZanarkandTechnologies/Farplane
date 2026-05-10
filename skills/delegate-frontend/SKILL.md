---
name: delegate-frontend
version: 0.1.0
description: Delegate bounded frontend planning, asset, implementation, or review phases to the configured Pi/Kimi frontend CLI profile while preserving Codexter ownership and auditability.
allowed-tools: Bash, Read, Glob, Grep
---

# Delegate Frontend

Use this when frontend work should be handed to the external Pi/Kimi frontend
agent instead of being implemented directly in the Codex lane.

## Job

Run a bounded external-CLI phase with the mounted frontend skills, collect the
handoff, and let Codexter integrate or reject the result.

## Default Profile

- Adapter: `pi`
- Model: `openrouter/moonshotai/kimi-k2.6`
- Profile root: `.harness/external-cli/profiles/frontend-pi-kimi`
- Run root: `.harness/external-cli/runs`

## Phase Types

- `spec`: produce or refine `LANDING_SPEC.md`; no implementation.
- `assets`: generate, collect, render, or manifest assets; no page build.
- `implementation`: edit the target frontend from an approved spec.
- `repair`: fix a named visual, motion, asset, or QA failure.
- `visual-review`: run same-thread review/visual-QA and produce findings.

## Required Inputs

- phase name
- run id
- owned output paths
- first-write path
- target page/spec path
- design brief path or explicit reason no durable design brief is needed
- stack facts: framework/router, Tailwind version, package availability,
  shadcn config, registry/theme plan
- acceptance criteria
- handoff path under `.harness/external-cli/runs/<run-id>/handoff.md`

## Command Pattern

Write the prompt to `.harness/external-cli/runs/<run-id>/prompt.md`, then run:

```bash
pi \
  --session-dir .harness/external-cli/runs/<run-id>/sessions \
  --model openrouter/moonshotai/kimi-k2.6 \
  --thinking low \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/frontend-craft \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/functional-ui \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/visual-design \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/landing-page \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/best-of-worlds \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/brainstorm \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/frontend-design \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/image-generation \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/video-generation \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/product-photography \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/agent-browser \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/visual-qa \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/review \
  --skill .harness/external-cli/profiles/frontend-pi-kimi/skills/web-design-guidelines \
  -p @.harness/external-cli/runs/<run-id>/prompt.md
```

Add other mounted skills only when the phase needs them.

## Rules

- Do not delegate vague "make it better" work. Convert it into a phase,
  owned files, and acceptance criteria first.
- Delegate prompts must include the design brief path, stack facts, registry or
  theme plan, and expected component-state proof when the phase touches reusable
  UI. If any item is unavailable, the prompt must say why.
- First external write must touch the named first-write path before broad
  reading or implementation.
- For premium landing pages, delegate only after the landing spec has research
  synthesis, best-of-worlds decisions, unique take, asset evidence, motion, and
  QA gates.
- For `spec` or `spec-research` phases, forbid reading `qa/**`, prior session
  JSONL, screenshots, videos, frame folders, and large generated assets unless
  the prompt explicitly requests visual review. Finish the owned planning
  artifact and handoff before optional artifact dives.
- For product, device, hardware, or equipment landing pages, mount and use the
  `product-photography` skill during the asset phase when available. Require
  realistic product shots/renders and assembly, disassembly, exploded-view, or
  feature-detail media instead of generic infographics.
- For premium product pages, require explicit product-clarity/accessibility QA:
  the hero and primary demo must keep the product inspectable, section text
  contrast must be readable, focus/skip-link affordances must exist, all images
  need alt text plus width/height attributes, and the handoff must report a
  `product_clarity_score`.
- For product teardown or exploded-view media, require a disassembly score:
  object continuity across states, component specificity, clean separation,
  product clarity, studio lighting, and no baked readable text or alphanumeric
  quality labels in generated pixels.
- For premium landing-page visual carriers, do not ask the delegated agent to
  create custom SVG illustrations, SVG diagrams, or SVG overlay art. Require
  generated/real raster media, or real WebGL/Three.js when a procedural visual
  is warranted.
- For cinematic hero scroll scrub, require a long authored media plan instead
  of a short decorative loop: 8-15+ seconds of seekable video or a 96+ frame
  sequence, at least five named beats, and a synchronized effect layer using
  GSAP, WebGL, Three.js, or HTML beat panels. The handoff must include debug
  evidence for media time, active beat, and effect-layer state.
- When the phase requests generated video, the delegated run must actually use
  the mounted `video-generation` skill and a video app/model. `Seedream` or
  other image-generation output plus local `ffmpeg` assembly is a frame
  sequence, not generated video. The handoff and manifest must record
  `skillsActuallyUsed` including `video-generation` plus `videoModel`,
  `videoProvider`, `sourceVideo`, or equivalent video provenance; otherwise
  Codexter must reject the handoff or downgrade the result to prototype.
- Require the handoff to list changed files, skills loaded, skills actually
  used, commands/results, risks, and next recommendation.
- Require implementation and repair handoffs to report stack facts observed,
  package or registry commands run, theme/preset changes, reusable component
  state coverage, and QA evidence for responsive, reduced-motion, focus,
  contrast, and overflow checks when UI changed.
- Codexter owns final verification and integration. Pi/Kimi does not claim final
  completion.

## Outcome Contract

After a delegate run, Codexter should have:

- `prompt.md`
- `command.json`
- `session_files.json` when available
- `handoff.md`
- the owned output files
- clear keep/repair/reject decision
- stack facts and design-brief traceability
