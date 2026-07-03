---
title: Script Storyboard QA Checklist
owner: script-storyboard
status: active
kind: qa-checklist
applies_to:
  - script-storyboard
  - content-video-plans
---

# Script Storyboard QA Checklist

Read this checklist before drafting a script-storyboard plan, then apply it
again before claiming the handoff is production-ready.

```text
script_storyboard_check(creative_ticket, production_handoff?)
  -> pass | violation | deferral
```

## Checklist

- [ ] `viewer_contract`: ICP, viewer promise, core idea, proof or reason to
  believe, platform, duration, style, CTA, and constraints are bound or
  explicitly assumed.
- [ ] `narrative_shape`: The plan names hook, tension, turn, proof moment,
  payoff, and final action; every beat advances that shape.
- [ ] `script_storyboard_alignment`: Script lines, storyboard panels, shot
  list, motion notes, captions/supers, audio notes, and asset needs describe
  one executable production path.
- [ ] `production_route`: The handoff names the next owner, such as `remotion`,
  `video-production`, `video-generation`, `remotion-render`, or
  `social-content`, with required inputs and blocker conditions.
- [ ] `proof_observable`: Done/proof names the review, still-frame, render,
  storyboard, script, or asset evidence needed before claiming production
  readiness.

## Reviewer Prompt

```text
Review the script-storyboard artifact against
skills/script-storyboard/qa_checklist.md. Return pass, violation, or deferral
for failed checks. Focus on whether the plan is executable by the named
production skill without hidden chat context.
```
