---
title: Optimize With Human founder lens
owner: optimize-with-human
status: accepted
date: 2026-06-29
related:
  - skills/optimize-with-human/SKILL.md
  - skills/taste-loop/SKILL.md
---

# Optimize With Human Founder Lens

## Trigger

Taste Loop product workers needed a stronger operating frame than "try to
impress Kenji." For product, content, offer, and distribution work, Kenji's
feedback should approximate founder judgment about whether a bet is worth
making, selling, or testing.

## Delta

- Added optional `founder_lens=false?` to the skill signature.
- Defined `founder_lens(...) -> customer + problem + wedge + offer_or_artifact
  + distribution_angle + validation_question + next_bet_if_approved
  + pivot_trigger_if_rejected`.
- Required founder-mode progress logs and feedback requests to name what would
  change the next bet, rather than asking only whether an artifact is good.

## Proof

- `skills/optimize-with-human/eval_task.json` includes founder-lens reference
  points.
- Taste Loop now passes `founder_lens=true` for product-lane artifact loops.
