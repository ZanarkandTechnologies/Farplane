---
target: video-production/retro-low-poly-consequence
mode: prompt_profile
ticket: tickets/TASK-0378/ticket.md
---

# Self-Improve Program: Retro Low-Poly Consequence

## Objective

Improve the complete video workflow until a finished 45–50 second proof video
scores at least 80 percent in every declared facet, at least 80 percent overall,
passes all hard gates, and receives TAS-A completion review.

## Current Contract

- Trigger: a Retro Low-Poly Consequence explainer requests generation or a
  measured style-profile improvement.
- Outcome: full video with creator-neutral visuals, original audio storytelling,
  captions, exact runtime, receipts, and evidence.
- Validation: `evals/rubric.json`, `evals/score_facets.py`, executable boundary
  regressions, delegated visual/factual/audio QA, and hash-bound final reviewer
  verdict.

## Baseline

- Complete deterministic fallback video: v2 exists at 47.000 seconds. Delegated
  visual QA improved from v1 `23/30` to v2 `27/30`; every visual-owned facet
  reaches at least `4/5`.
- Baseline reference-layer proxy: `6/10`.
- Candidate 1 reference-layer proxy: `8/10`; its engine-budget clauses now have
  measured Seedance support from the promoted reference-conditioned repair.
- Audio result: sound storytelling `5/5`; voice performance `3/5` because tone
  and emotional-curve assertions still require genuine listening.
- Final visual result: the 47-second Seedance-first v4 exists at 720x1280 with
  provider, spend, media, visual, and rights receipts. Full-motion visual QA is
  `30/30`; factual clarity, sound, captions, and technical delivery are `5/5`.
- Remaining failed facet: voice performance is `3/5` because genuine listening
  has not established dry/matter-of-fact tone or controlled escalation. The
  deterministic pre-review score is `48/50` but remains `accepted: false`.

## Eval Metric

- Primary: every facet `>= 0.80`, overall `>= 0.80`, all hard gates true.
- Provider: hybrid two-phase deterministic scorer plus delegated
  visual/factual/audio review.
- Minimum meaningful delta: at least one failed assertion repaired without
  lowering another facet below threshold.
- Simplicity guard: one bounded prompt hypothesis per round; no adjective
  stacking, source copying, weakened assertion, or average-only promotion.

## Search Space

1. Original character/environment reference-bible rendering constraints.
2. Seedance geometry, texture, lighting, motion, camera, and end-state wording.
3. Script/shot causal clarity and exact edit timing.
4. Original voice direction, mechanism-bound SFX, silence, and mix automation.
5. Caption chunking, safe zones, and final Remotion assembly.

## Durable Evals

- `evals/test_cases.jsonl`
- `evals/rubric.json`
- `evals/score_facets.py`
- `evals/test_score_facets.py`
- `tickets/TASK-0378/artifacts/full-video-metric-card.md`
- `tickets/TASK-0378/artifacts/physics-grounding.md`

## Experiment Log

| Date | Run | Hypothesis | Result | Keep? | Lesson |
| --- | --- | --- | --- | --- | --- |
| 2026-07-15 | reference-candidate-1 | engine-budget constraints suppress polished/PBR drift | reference proxy 6/10 → 8/10; Seedance blocked | carry, not promote | broad “low-poly” language is insufficient; actual mesh/texture/lighting constraints help |
| 2026-07-15 | full-animatic-v1-to-v2 | replace label-dependent flat foregrounds with faceted/atlas action and exact timeline audio | visual-owned 23/30 → 27/30; technical 4/5; sound 5/5 | keep for deterministic fallback only | mechanisms must read with labels hidden; a low-poly plate alone cannot carry the style; pad the final mix with deliberate room tone rather than trusting AAC container duration |
| 2026-07-15 | seedance-reference-take-1 | short source motion/style conditioning plus original bibles will preserve the grammar without copying identity/content | rights TAS-A; visual 5/6; style/continuity/edit/text/copy guards pass; split reads as controlled stance | keep topology, repair action | runtime style conditioning is viable, but generic “slide apart” does not force world-relative displacement |
| 2026-07-15 | seedance-reference-repair-1 | fixed landmarks, minimum displacement, lower body collapse, and a held pose will make the mechanism legible without changing style | visual 6/6; rights TAS-A; glide/split flips fail → pass; USD 2.9798 cumulative | promote | prompt contact motion against tile seams/rail posts/stop lines; preserve the successful reference/bible setup and change one failure only |
| 2026-07-16 | multi-scene-block-to-single-mechanism-v4 | one physical mechanism per 4–6 second Seedance clip plus bounded optical/time edits and light path markers will preserve the model-native look while making causes readable | first batch 3/11 causal actions; v4 full visual QA 30/30; factual/sound/captions/technical 5/5; rights TAS-A; USD 19.46598 cumulative | promote visual workflow | do not compress several mechanisms into one provider call; Seedance owns characters/world motion, while Remotion may crop, time, caption, mix, and add sparse post-owned path evidence |

## Accepted Learnings

- Probe and reference scores are gates, never completion evidence.
- “Low-poly” must be operationalized through visible engine-budget constraints.
- Audio is one master storytelling spine; per-clip Seedance audio stays off.
- No facet may be averaged below the operator's 80 percent threshold.
- Major mechanism shots must remain inferable when captions and explanatory
  labels are hidden; force arrows may clarify an already visible action but
  cannot substitute for it.
- Faceted/atlas foreground treatment, hard light, and a mundane textured plate
  can clear the reusable visual grammar while still honestly missing fully 3D
  mesh depth.
- Probe both encoded stream duration and decoded PCM duration. Add an original
  low-level room-tone bed and sample-exact padding when the final hold must
  remain audible through the exact timeline end.
- An explicitly approved source excerpt can condition motion/editing/style when
  it is muted, caption-cropped, runtime-only, excluded from the final edit, and
  paired with original bibles plus independent visual/rights review.
- Contact actions need fixed world landmarks, minimum visible displacement,
  world-relative rather than in-place motion, and a held causal end state.
- Seedance owns primary animation. Remotion owns edit, captions, audio, and
  light VFX; it cannot substitute for a missing model-native shot batch.

## Rejected Ideas

- Treating an 8/10 still-reference proxy as proof of generated-video relevance.
- Using unapproved source media, source voice, creator identity, exact wardrobe,
  source footage in the final edit, or source-conditioned output without an
  independent no-copy review.

## Next Hypothesis

The visual workflow is promoted from the hash-bound v4 result. Preserve its
single-mechanism clip topology, accepted-trim review, source-exclusion boundary,
and Seedance-primary/Remotion-light-VFX ownership split. The remaining failed
facet and next pre-review blocker is genuine listening of the master voice:
tone and escalation cannot be promoted from mechanical audio analysis or a
non-listening reviewer. If listening clears the voice facet, immutable
pre-review and the independent TAS-A completion review still must run.
