---
title: Copywriting Advisor Source Mining Hardening
owner: copywriting-advisor
status: active
kind: skill-audit
created_at: 2026-07-09
ticket_id: TASK-0317
---

# Copywriting Advisor Source Mining Hardening

## Trigger

Operator feedback: the first implementation was too generic and needed real
step-by-step source mining, swipe-file use, and Tasty Pack integration.

## Behavior Delta

- Before: `SKILL.md` told agents to build a message spine but did not explain
  what to mine or how to use swipes/Tasty Packs.
- After: `SKILL.md` requires source atoms or hypothesis mode, links a
  source-mining workflow, and makes swipe/Tasty Pack material part of the
  default input contract.

## Source Grounding

- Copyhackers voice-of-customer and review-mining workflows.
- CXL voice-of-customer guidance.
- VWO landing-page copywriting workflow.
- Swipe-file guidance from Swipe Files / SwipeFile-style public references.
- Farplane `ingest-content` and `content-impl-plan` Tasty Pack contracts.

## Checklist Verdicts

- `first_load_sufficiency`: pass - normal path now includes source mining
  before message mapping.
- `reference_load_precision`: pass - source workflow loads only when source,
  swipe, Tasty Pack, review, competitor, or quality-sensitive copy work exists.
- `surface_budget`: pass target - QA remains five checklist items.
- `proof_surface_fit`: pass - eval and QA now test for source mining rather
  than generic copy principles only.

## Proof Plan

Run `python3 skills/skill-maintenance/scripts/check_skills.py --write`,
`python3 -m json.tool skills/copywriting-advisor/eval_task.json`, and scoped
`git diff --check`.
