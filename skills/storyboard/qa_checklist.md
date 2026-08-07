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
  For short-form, latest-news, title-led, or
  retention-sensitive work, the plan generates at least ten materially
  different hook candidates spanning at least six causal lenses with no more
  than two candidates from one lens, compares at least three finalists, and
  selects one winner. The output shows the complete candidate set with
  keep/reject reasons and a source-title
  comparison table rather than collapsing the lab to a few preferred lines.
  An unfamiliar general viewer can understand the winner
  immediately without decoding unexplained legal, financial, technical, or
  infrastructure jargon. The winner normally expresses one recognizable
  actor, one concrete action, and one understandable consequence in one
  breath and at most eight display words; abstract verbs and bridge phrases
  such as `back`, `backing`, `secure`, `facilitate`, `support`, `finance`,
  `fund`, `get the money`, or `help fund` fail when a concrete everyday action
  such as `help buy`, `help pay`, `build`, `stop`, or `save` can express the
  evidence safely. A finalist containing a blocked abstract term is removed
  before scoring rather than averaged into a win; the displayed candidate set
  is also post-cleanup, with blocked drafts allowed only in rejected-line
  notes. Coined simplifications such
  as `AI factory` or `computer hub` also fail when they create a new metaphor
  to decode. When the evidence places one company on both sides of a purchase,
  the candidate pass tests the direct supplier/customer/product loop. `Help`
  is acceptable only when it directly modifies a drawable action such as
  `buy`, `build`, or `pay`, and two-actor hooks repeat names or objects instead
  of using ambiguous pronouns. When a source title exists, the comparison shows why the winner is
  stronger on comprehension, curiosity, factual accuracy, brevity, and
  first-frame visual potential; otherwise the hook remains unlocked. The
  first-three-second packet gives exact on-screen copy, voiceover, dominant
  visual action, and a compact evidence qualifier. Reported, forecast,
  alleged, or unsigned claims retain their uncertainty. An applicable hook
  decision cannot pass with an abbreviated finalist list: the complete
  candidate decisions, criterion-by-criterion source-title table, winner
  rationale, rejected-finalist reasons, and all four first-three-second fields
  are mandatory.
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
  When the selected format is a voice-led documentary/editorial reel, measured
  narration defines compact causal scene ranges. Each scene names one
  viewer-state change, a dominant spatial action,
  background/subject/foreground needs, exact frame events, restrained
  micro-motion, and audio/caption obligations. Each missing visual has a
  searchable Asset Advisor brief with subject, source classes, rights
  constraint, framing, and acceptance check; the storyboard does not prescribe
  custom-created SVG/JSX/programmatic vector animation assets as substitutes.
- [ ] `production_route`: The handoff names the next owner, such as `remotion`,
  `content-impl-plan`, `ai-video-advisor`, `remotion-render`, or
  `social-content`, with required inputs and blocker conditions. When visuals
  are missing, `asset-advisor` candidate discovery precedes generation unless
  the brief explicitly requires an original generated asset. Discovery may
  select a source, create a rights-safe inspiration packet for original
  generation, or record no usable reference and route original generation.
  Accepted static SVG source media remains allowed with provenance.
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
