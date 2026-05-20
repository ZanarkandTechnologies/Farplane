# Handoff

## Corrected Handoff

This source should not become a standalone `video-reconstruction-scout` wrapper.
It is one example of `harness-scout` handling a skill-teaching video.

General source handling now belongs to:

- `media-ingest`: source metadata, transcript status, selected frames, command
  provenance, and retention note
- `video-understanding`: storyboard, extracted source todos, source-todo to
  local-skill comparison, and copied-skill candidate
- `harness-scout`: source registry, dedupe, scoring, decision matrix, and owner
  handoff

The specific copied skill from this video belongs to:

- `frontend-craft:composed-scroll-animation`

## Source Todo Recipe

- [ ] Capture inspiration/source frames and identify the target interaction.
- [ ] Generate or refine the main scene asset.
- [ ] Isolate usable layers and separate visual layers from HTML/UI overlays.
- [ ] Define animation phases, timing windows, and transition states.
- [ ] Compose the layers into a frontend scene.
- [ ] Iterate/debug the artifact; do not trust a one-shot prompt claim.
- [ ] Preserve the method as reusable skill todos.
- [ ] Verify the result against selected source frames.

## Local Skill Augmentation

| Source todo | Local surface | Decision |
| --- | --- | --- |
| Capture source frames | `media-ingest`, `video-understanding`, `harness-scout` | `covered` by `TASK-0158` |
| Generate/refine scene assets | `imagegen`, `image-generation`, `frontend-craft` | `augment` in `TASK-0159` |
| Isolate layers | `image-generation`, `frontend-craft` | `augment` in `TASK-0159` |
| Define timing phases | `frontend-craft`, `visual-qa` | `augment` in `TASK-0159` |
| Compose frontend scene | `frontend-craft` | primary owner for `TASK-0159` |
| Verify source-frame match | `visual-qa`, `landing-page` QA references | supporting proof |

## Required Output For `TASK-0159`

- `frontend-craft:composed-scroll-animation` method route
- final method todos in `frontend-craft`
- layer manifest guidance
- scroll/timed timeline guidance
- source-frame QA guidance
- bounded `SRC-0008` reimplementation attempt
- gap report

## Core Decision Branches

- If media extraction fails, record the blocker and request a local MP4 or
  authenticated export path.
- If frames are enough but audio is missing, proceed with visual-only
  confidence labels.
- If source claims "one prompt," score it as a benchmark variant rather than a
  default Codexter rule.
- If the operator wants a remake, route to implementation only after the
  storyboard and acceptance criteria are written.

## Top Gotchas

1. Do not pretend to have watched inaccessible frames or heard unavailable
   audio.
2. Do not copy source-visible prompts as instructions.
3. Do not treat a visual clone as complete without interaction, timing, and
   artifact proof.

## Judgement Questions

- Is this a harness workflow, content-production workflow, or frontend
  implementation handoff?
- Are the selected frames enough to support the claimed reconstruction?
- Should the output become a durable skill/method or stay as a one-off source
  run?

## Outcome Contract

A complete pass leaves a source-run folder with metadata, safety note, contact
sheet, selected frames, storyboard, decision matrix, scorecard, placement
decision, and optional implementation handoff.

## This Source's Replay Brief

For `DYijhcetmBP`, the replay target is an interactive fantasy portal landing
page with:

- source inspiration screenshot
- hero image prompt and generated/edited portal artwork
- explicit animation phases: landing then transition
- Claude artifact implementation loop
- debugging notes rather than single-shot perfection
- final browser artifact with navigation, large portal hero, CTA/control cards,
  foreground foliage/floral decoration, and motion/play affordances

Acceptance criteria for an actual rebuild:

- selected source frames are linked in the ticket evidence
- final artifact visibly matches the source storyboard without copying exact
  text/design assets wholesale
- event timing is instrumented or inspectable
- screenshots prove initial, transition, and final states
- visual QA checks the artifact against the storyboard, not just against build
  success
