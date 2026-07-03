---
title: Remotion Proof Video Storyboard Example
owner: storyboard
status: active
kind: skill-example
created_at: 2026-07-03
---

# Remotion Proof Video Example

## Input

```text
idea: Farplane turns agent work into visible proof.
icp: skeptical AI operators who have been burned by vague agent claims.
platform: vertical short video
duration: 20 seconds
style: crisp motion-graphics proof demo
cta: read the proof packet
production_route: remotion
```

## Summary

Create a 20 second vertical motion-graphics video for skeptical AI operators.
The video contrasts vague agent completion claims with Farplane's visible
artifact, check, review, and proof loop.

## Scope

- In: one 20 second vertical proof explainer, motion-graphics style.
- Out: final render, posting, paid media, account actions.
- Platform: short-form vertical, adaptable to X, Instagram Reels, TikTok, and
  YouTube Shorts.
- Duration: 20 seconds.
- Style: clean UI cards, fast evidence cuts, restrained motion.
- CTA: read the proof packet.

## Delta

- Before: "agents did work" is a claim.
- After: viewer sees a simple proof trail: task, artifact, check, review,
  evidence.
- Why now: autonomous marketing needs proof-first creative that can be rendered
  deterministically with Remotion.

## Program

Narrative Signatures:

- Hook: "Agent work is only real when you can inspect the proof."
- Tension: completion claims are easy to fake or misunderstand.
- Turn: Farplane makes the work visible as artifacts and checks.
- Proof moment: the screen shows task, artifact path, validation, and review.
- Payoff: the viewer understands the trust loop in one glance.
- Final action: "Read the proof packet."

Beat Sheet:

1. 0-3s: Open with a vague green "Done" badge that glitches into a question.
2. 3-7s: Replace the badge with a task card and artifact path.
3. 7-12s: Show checks lighting up: validation, QA, reviewer.
4. 12-17s: Pull back into a proof packet with evidence links.
5. 17-20s: End card with CTA.

Script:

- Scene 1: "Done is not proof."
- Scene 2: "Farplane makes the work inspectable."
- Scene 3: "Artifact. Check. Review. Evidence."
- Scene 4: "Trust the trail, not the claim."
- Scene 5: "Read the proof packet."

Storyboard:

| Scene | Time | Visual | Copy/VO | Motion | Assets | Proof |
| --- | ---: | --- | --- | --- | --- | --- |
| 1 | 0-3s | Large "Done" badge on dark UI card | Done is not proof. | Badge flickers, question mark appears | none | one-frame still at 2s |
| 2 | 3-7s | Task card expands into artifact path | Farplane makes the work inspectable. | Card unfolds into path and file icon | task label, path text | text legibility still |
| 3 | 7-12s | Three check chips: validation, QA, reviewer | Artifact. Check. Review. Evidence. | Chips light up left to right | check icons | animation timing check |
| 4 | 12-17s | Proof packet page with linked evidence rows | Trust the trail, not the claim. | Camera pulls back to packet view | evidence row labels | layout still |
| 5 | 17-20s | CTA card | Read the proof packet. | CTA settles, subtle pulse | CTA text | final frame still |

## Map

- Production route: `remotion`
- Asset route: deterministic UI cards and icons in React; no generated bitmap
  assets required for the first render.
- Distribution route: `social-content` after render for caption and post copy.

## Done / Proof

- done_when:
  - Remotion composition dimensions, fps, duration, scenes, copy, assets, and
    proof frames are named.
  - A later Remotion run can produce at least one still-frame proof before MP4.
- evidence:
  - storyboard table
  - source copy inventory
  - still frames at 2s, 9s, and 19s after implementation
- residual_risk:
  - final motion taste and pacing require visual QA after implementation.

## State

review

## Links

- source proof: user-provided Farplane proof packet or local ticket artifact
- production: Remotion project path after implementation
- outputs: still frames and MP4 after render

## Notes

- Rejected angles: "AI agents are magic" because it weakens the proof-first
  trust claim.
- Taste notes: restrained, inspectable, not hype-driven.
- Blockers: actual ticket/proof packet path must be supplied before factual
  labels replace illustrative placeholders.
