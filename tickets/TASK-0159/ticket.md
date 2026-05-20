---
ticket_id: TASK-0159
title: copy SRC-0008 into frontend-craft composed scroll animation
phase: planning
status: review
owner: unassigned
claimed_by:
priority: high
depends_on:
  - TASK-0158
blocked_by: []
ready: false
approval_required: true
requires_qa: true
requires_demo: true
created_at: 2026-05-21T00:00:00+08:00
updated_at: 2026-05-21T01:30:00+08:00
next_action: approve the replanned frontend-craft composed-scroll method todos, then add the method and run the bounded SRC-0008 reimplementation attempt
last_verification: 2026-05-21 - replanned against TASK-0158 video reconstruction brief and source-todo comparison
---

# TASK-0159: copy SRC-0008 into frontend-craft composed scroll animation

## Summary
Copy the specific skill demonstrated in `SRC-0008` into `frontend-craft`: a
method for generating several image assets, isolating/cutting them into layers,
composing them into a rich browser scene, driving scroll or timed transitions,
and verifying against source frames. This ticket also runs a bounded
reimplementation attempt so we can judge whether the copied skill actually
works.

## Scope
- In:
  - `frontend-craft:composed-scroll-animation` method routing
  - a dedicated composed-scroll reference for 6-12 layer asset planning,
    background removal/cutouts, layer composition, timeline drivers,
    instrumentation, fallback, and source-frame QA
  - updates to frontend-craft asset/motion references without duplicating
    image-generation or GSAP docs
  - a bounded `SRC-0008` reimplementation attempt using the transcript/frames
    produced by `TASK-0158`
  - gap report comparing the attempt to the source video frames
- Out:
  - general media ingest/video understanding; that is `TASK-0158`
  - broad landing-page rewrite unrelated to this method
  - unbounded paid asset generation
  - claiming one-prompt generation is required or sufficient

## Plan
- `Change:` add `frontend-craft:composed-scroll-animation` and test it by
  reimplementing the portal-style animation process from `SRC-0008`.
- `Why:` the video is one example input to `harness-scout`, but the copied skill
  itself is frontend-specific: generate multiple assets, isolate layers, stitch
  them into a composed animation, and prove the result against source frames.
- `Before -> After:`
  - Before: `frontend-craft` can route generated assets and complex motion, but
    it lacks a named method for source-video-derived layered image composition.
  - After: `frontend-craft` has a method that turns a reconstruction brief into
    a layer manifest, generated/cutout asset plan, scroll/timed timeline,
    instrumentation contract, QA plan, and reimplementation gap report.
- `Touch:`
  - `skills/frontend-craft/SKILL.md`
  - `skills/frontend-craft/todos.md` if method routing needs checklist support
  - `skills/frontend-craft/references/composed-scroll-animation.md`
  - `skills/frontend-craft/references/asset-generation.md`
  - `skills/frontend-craft/references/motion-routing.md`
  - `skills/landing-page/references/qa.md` only if source-frame comparison
    should be referenced from scroll QA
  - `experiments/harness-scout/runs/2026-05-20-instagram-claude-portal-video/`
  - `docs/features/registry.jsonl`
  - `docs/skills/registry.jsonl` through sync if skill metadata changes
  - `docs/HISTORY.md` after implementation
  - `tickets/TASK-0159/ticket.md`
- `Inspect:`
  - `skills/frontend-craft/SKILL.md`
  - `skills/frontend-craft/references/asset-generation.md`
  - `skills/frontend-craft/references/motion-routing.md`
  - `skills/landing-page/todos.md`
  - `skills/landing-page/references/qa.md`
  - `skills/image-generation/SKILL.md`
  - `skills/image-generation/references/tools/background-removal.md`
  - `experiments/harness-scout/runs/2026-05-20-instagram-claude-portal-video/`
- `Signature delta:`
  - `skills/frontend-craft/SKILL.md / frontend-craft:composed-scroll-animation(brief): FrontendAnimationBuildPlan`
  - `skills/frontend-craft/references/composed-scroll-animation.md / plan_layers(brief): LayeredAssetManifest`
  - `skills/frontend-craft/references/composed-scroll-animation.md / plan_qa(source_frames, implementation): SourceFrameQaPlan`
- `Type Sketch:`
  - `LayeredAssetManifest`: `layers`, `generation_prompts`,
    `cutout_steps`, `composition_order`, `fallbacks`, `provenance`
  - `ComposedScrollAnimationSpec`: `story_beats`, `layers`,
    `timeline_driver`, `scroll_or_timed_phases`, `debug_contract`,
    `source_frame_targets`
  - `ReimplementationGapReport`: `source_frames`, `attempt_artifacts`,
    `matched_behaviors`, `misses`, `next_repairs`
- `Typed flow example:`
  - `SRC-0008` handoff says the creator builds a portal interaction from a
    generated hero image, event timing, Claude artifact iteration, and final
    interactive state.
  - The method converts that into a background portal layer, foreground foliage
    and flower layers, HTML text/control overlays, a scroll/timed transition,
    reduced-motion still, and source-frame QA targets.
  - The bounded reimplementation attempt produces an artifact bundle and gap
    report instead of claiming a perfect clone.
- `Execution steps:`
  1. Add method routing to `frontend-craft`.
  2. Write the composed-scroll reference with asset layers, cutouts,
     composition, motion driver, debug hooks, fallback, and QA requirements.
  3. Update existing asset/motion references to point to the new method.
  4. Use the `SRC-0008` reconstruction from `TASK-0158` to draft an asset layer
     manifest and implementation brief.
  5. Run a bounded reimplementation attempt as artifact proof. Prefer a small
     local HTML/React prototype or documented build brief if a full app target
     is not available.
  6. Capture screenshots or source-frame comparison notes.
  7. Write a gap report judging whether the copied method works.
  8. Run registry/ticket checks and review.
- `Recommendation:` keep the copied skill under `frontend-craft`; use
  `landing-page` and `visual-qa` as supporting proof surfaces, not primary
  owners.
- `Options considered:`
  1. Put the method in `landing-page`: rejected because the source pattern can
     apply to non-landing interactive components.
  2. Put the method in `frontend-craft`: chosen because it orchestrates assets,
     motion, implementation, and QA.
  3. Put the method in `video-production`: rejected because the output is a
     frontend scene, not a produced video.
- `Blast radius:`
  - frontend-craft routing
  - asset generation references
  - scroll/visual QA expectations
  - generated asset provenance expectations
- `Risks:`
  - over-copying visual style instead of copying the method
  - skipping real asset isolation and only writing CSS decoration
  - accepting visual resemblance without interaction/timing proof
  - running paid generation without explicit approval

## Acceptance Criteria
- [ ] `frontend-craft` exposes `frontend-craft:composed-scroll-animation`.
- [ ] Dedicated reference covers layered asset generation, background removal,
      composition order, motion timeline, instrumentation, fallback, and QA.
- [ ] The method todos explicitly preserve the source-video recipe and map each
      step to existing support skills where possible.
- [ ] `SRC-0008` reimplementation attempt exists with asset/layer manifest.
- [ ] Attempt includes screenshots or source-frame comparison notes.
- [ ] Gap report judges what worked, what failed, and next repairs.
- [ ] Registry and ticket checks pass.

## Final Skill Todos
These are the todos that should land in the `frontend-craft` method/reference
for `frontend-craft:composed-scroll-animation`.

- [ ] Read the
  [SRC-0008 reconstruction brief](../../experiments/harness-scout/runs/2026-05-20-instagram-claude-portal-video/video-reconstruction-brief.md)
  and corrected
  [handoff](../../experiments/harness-scout/runs/2026-05-20-instagram-claude-portal-video/handoff.md).
- [ ] Restate the source-video recipe as implementation steps without copying
  the source prompt or creator branding.
- [ ] Define the target artifact and layer manifest: 6-12 image/UI layers,
  z-order, timing/scroll states, responsive constraints, and fallback.
- [ ] Route asset generation, background removal, cutouts, and provenance
  through `imagegen` / `image-generation`.
- [ ] Compose the frontend scene with generated imagery and HTML/UI overlays as
  inspectable separate layers.
- [ ] Add debug/proof hooks for phase, scroll progress, active layer states,
  and reduced-motion fallback.
- [ ] Verify against selected source frames with screenshots, visual QA notes,
  and a gap report.

## Verification
- `Tests:`
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  - `python3 bin/sync_skill_registry.py --check`
  - `python3 bin/check_skill_todo_tiers.py --allow-peer-tier3`
  - `python3 tickets/scripts/check_ticket_metadata.py`
- `Manual checks:`
  - Read `frontend-craft` route and confirm this ask selects the new method.
  - Inspect the reimplementation bundle and gap report.
  - Confirm no raw media/transcripts/secrets were committed.
- `Evidence required:`
  - method reference
  - `SRC-0008` reimplementation bundle
  - source-frame comparison or screenshots
  - gap report
  - review artifact

## Proof Contract
- `Metrics:`
  - `Primary metric:` `src_0008_reimplementation_attempt_completed`
  - `Direction:` `pass/fail`
  - `Verify:` artifact bundle and gap report exist; validation commands pass
  - `Guard:` no paid generation without approval; no raw media/secrets
  - `Min acceptable result:` method docs exist, attempt exists, gap report
    exists, checks pass
  - `Autoresearch warranted:` no
  - `Autoresearch session:` none
- `Review Rubrics:`
  - `user-intent-satisfaction >= 4.0`
  - `evidence-quality >= 4.0`
  - `integration-readiness >= 4.0`
  - `ui-quality >= 3.5` if a runnable prototype is produced
- `Required Evidence:`
  - screenshots/source-frame comparison
  - gap report
  - command outputs
  - review artifact

## Agent Contract
- `Open:` if a prototype is produced, use its local file or dev-server URL
- `Test hook:` source-frame comparison plus visual QA notes; scroll-scrub QA
  when scroll-driven implementation is runnable
- `Stabilize:` keep prototype bounded; record generated assets and prompts
- `Inspect:` initial, transition, and final states from the source frames
- `Key screens/states:` source inspiration, asset generation, transition phase,
  final interactive artifact
- `QA cookbook:` `skills/landing-page/references/qa.md` when scroll-scrub proof
  applies
- `Taste refs:` `skills/frontend-craft/references/composed-scroll-animation.md`
- `Expected artifacts:` layer manifest, prototype/build brief, screenshots,
  gap report, review
- `Delegate with:` this ticket and the `SRC-0008` reconstruction handoff

## Autonomy Readiness
- `Human inputs/assets:` `SRC-0008` transcript/frames from `TASK-0158`
- `Credentials / external access:` none required for local prototype; paid
  generation needs explicit approval
- `Compute/runtime needs:` browser QA only if runnable prototype exists
- `Tooling gaps:` if image generation or background removal tools are not
  available, document fallback and use placeholders only as failed/partial
  evidence
- `QA risks:` visual clone may miss timing, responsiveness, or interaction
- `Human gates:` paid generation and external publishing
- `Agent decision boundaries:` copy method, not exact creator branding or
  source assets

## Evidence Checklist
- [ ] Layer manifest:
- [ ] Prototype/build brief:
- [ ] Screenshot/source-frame comparison:
- [ ] Gap report:
- [x] Review report:
  `tickets/TASK-0159/artifacts/review/2026-05-21-replan-review.md`

## Refs
- `tickets/TASK-0158/ticket.md`
- `experiments/harness-scout/runs/2026-05-20-instagram-claude-portal-video/`
- `experiments/harness-scout/runs/2026-05-20-instagram-claude-portal-video/video-reconstruction-brief.md`
- `skills/frontend-craft/SKILL.md`
- `skills/image-generation/SKILL.md`
- `skills/landing-page/references/qa.md`

## Evidence
- `Artifacts:`
  - `tickets/TASK-0159/artifacts/review/2026-05-21-impl-plan-review.md`
  - `tickets/TASK-0159/artifacts/review/2026-05-21-replan-review.md`
  - `tickets/TASK-0158/artifacts/review/2026-05-21-checklist-refactor-review.md`
- `Commands:`
  - `python3 tickets/scripts/check_ticket_metadata.py`
- `Result summary:`
  - split from general video-to-skill pipeline; planning review passed; implementation evidence pending
  - replanned final method todos against the `TASK-0158`
    video-reconstruction brief

## Blockers
- none for planning; implementation depends on the `TASK-0158` reconstruction
  handoff now linked in Refs
