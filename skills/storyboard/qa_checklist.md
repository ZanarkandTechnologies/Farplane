---
title: Storyboard QA Checklist
owner: storyboard
status: active
kind: qa-checklist
applies_to:
  - storyboard
  - content-video-plans
---

# Storyboard QA Checklist

Read this checklist before drafting a storyboard plan, then apply it
again before claiming the handoff is production-ready.

```text
storyboard_check(creative_ticket, production_handoff?)
  -> pass | violation | deferral
```

## Checklist

- [ ] `viewer_contract`: ICP, viewer promise, core idea, proof or reason to
  believe, platform, duration, style, CTA, and constraints are bound or
  explicitly assumed.
- [ ] `narrative_shape`: The plan names hook, tension, turn, proof moment,
  payoff, and final action; every beat advances that shape.
- [ ] `storyboard_alignment`: Script lines, storyboard panels, shot
  list, motion notes, captions/supers, audio notes, and asset needs describe
  one executable production path. Narrative video storyboards name recurring
  character/object continuity or explicit rationale, viewer question -> answer,
  generation topology, start/end frame pairs for continuous AI-video chains,
  and transition notes for deliberate scene breaks. Each deliberate-break clip
  has one normally 4-5 second scene packet with a clean grid, matching annotated
  grid, stable IDs, keyed action/camera/end-state notes, provider strategy,
  audio obligations, and `reuse_locked` approved assets.
  Character-bearing packets bind the canonical identity path/hash, and any
  provider fallback that changes visible identity invalidates approval until
  the revised character card and affected grids receive fresh human review.
  The canonical card remains unchanged, the fallback is a versioned sibling,
  and unaffected approved scenes remain locked.
- [ ] `production_route`: The handoff names the next owner, such as `remotion`,
  `video-production`, `ai-video-advisor`, `remotion-render`, or
  `social-content`, with required inputs and blocker conditions.
- [ ] `proof_observable`: Done/proof names the review, still-frame, render,
  storyboard, script, or asset evidence needed before claiming production
  readiness. For deliberate breaks, the human sees the overview strip plus all
  existing, dimension-verified clean/annotated grid image files and notes before
  generation, alongside the recurring-character card and an explicit feedback
  request; text-only panels remain draft-only, and unchanged approved assets
  are reused rather than silently regenerated.

## Reviewer Prompt

```text
Review the storyboard artifact against
skills/storyboard/qa_checklist.md. Return pass, violation, or deferral
for failed checks. Focus on whether the plan is executable by the named
production skill without hidden chat context.
```
