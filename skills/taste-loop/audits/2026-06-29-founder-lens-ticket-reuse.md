---
title: Taste Loop founder lens and workflow ticket reuse
owner: taste-loop
status: accepted
date: 2026-06-29
related:
  - skills/taste-loop/SKILL.md
  - skills/optimize-with-human/SKILL.md
  - farplane/automations.md
---

# Taste Loop Founder Lens And Workflow Ticket Reuse

## Trigger

Kenji observed that `optimize-with-human` workers should act less like generic
"impress me" artifact graders and more like founder loops: generate a bet,
frame the customer/problem/wedge, validate with human taste, and iterate. He
also noted that Taste Loop should not create a fresh ticket for every TL
experiment; one active workflow ticket should hold the experiment series until
the loop is actually done.

## Delta

- Added `founder_lens=true` to `optimize-with-human` as an explicit framing
  mode for product, content, offer, distribution, and market-learning artifacts.
- Updated Taste Loop to optimize for founder conviction that a bet is worth
  making, selling, or testing.
- Expanded TasteProposal framing to include customer/buyer, problem, wedge,
  offer/artifact, distribution angle, validation question, next bet if
  approved, and pivot trigger if rejected.
- Added the workflow ticket reuse rule:
  `ticket_key = product_lane + "/" + workflow_id`.
- Defined non-terminal states (`revise`, `reject`, no-reply, reminder) as
  reasons to append another timestamped hypothesis cycle to the same
  `progress.md`, not to create a fresh ticket or a fresh named TL experiment
  item.

## Proof

- `skills/taste-loop/eval_task.json` now includes founder-lens and workflow
  ticket reuse reference points.
- `farplane/automations.md` now carries `founder_lens = true` and a
  `ticket_reuse` override for the active-hours Taste Loop automation.
