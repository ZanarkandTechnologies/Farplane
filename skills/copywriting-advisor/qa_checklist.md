---
title: Copywriting Advisor QA Checklist
owner: copywriting-advisor
status: active
kind: qa-checklist
applies_to:
  - copywriting-advisor
---

# Copywriting Advisor QA Checklist

Use this checklist before drafting and again before claiming copy quality,
message quality, or readiness for review.

```text
copywriting_check(copy_packet, target_stage?)
  -> pass | revise | blocked
```

## Preflight

- [ ] Inputs are bound or labeled as assumptions: one reader, demographic
  group, product, page goal, offer, proof, CTA, output stage, source/swipe/Tasty
  Pack availability, and final-public human review gate.

## Copy Checks

- [ ] Default page copy is under 100 non-empty lines, with hero copy under 20
  words, one primary promise, one intended action, and one job per section.
- [ ] The story spine has tension, turn, proof, and action, with source atoms
  or `source_mode: hypothesis` visible; confident copy is backed by
  voice-of-customer, Tasty Pack, swipe moves, proof, product truth, or supplied
  brief material, and the selected persuasion path fits the reader stage:
  AIDA, PAS, 4Cs, FAB, ACC, or SLAP.
- [ ] The copy strategy would not transfer unchanged to a generic writing
  skill: it names awareness stage, dominant desire, market sophistication,
  dominant objection, message angle, proof strategy, lead posture, swipe move,
  concrete before/after situation, and message-layer verdict.
- [ ] Claims, word bank, cut list, line count, weakest claim, next owner, and
  blockers are visible; the weakest conversion factor is named as motivation,
  value, friction, anxiety, or incentive; unearned hype such as "seamless",
  "revolutionary", "unlock", "supercharge", or "game-changing" is removed
  unless proof earns it.

## Reviewer Prompt

```text
Review the copy packet against skills/copywriting-advisor/qa_checklist.md.
Return pass, revise, or blocked. Focus on one-message clarity, emotional force,
specificity, proof fit, line budget, and public-copy approval safety.
```
