---
title: Copywriting Advisor Initial Skill Audit
owner: copywriting-advisor
status: active
kind: skill-audit
created_at: 2026-07-09
ticket_id: TASK-0317
---

# Copywriting Advisor Initial Skill Audit

## Scope

Created the initial `copywriting-advisor` package for concise emotional page
copy from audience, product, page goal, proof, and offer inputs.

## Source Grounding

- Google Search Central: people-first, useful, trustworthy content.
- Nielsen Norman Group: concise, scannable, objective web writing.
- Stripe Atlas and VWO: one reader / one offer / one action landing-page copy
  discipline.

## Checklist Verdicts

- `first_load_sufficiency`: pass - `SKILL.md` includes trigger, signature,
  todo path, routes, gates, and outputs.
- `reference_load_precision`: pass - only root QA and neighboring skills are
  referenced with read/use conditions.
- `prompt_size_tokens`: pass - first load is compact and examples live outside
  `SKILL.md`.
- `proof_surface_fit`: pass - behavior-sensitive quality is guarded by
  `qa_checklist.md`, one example, and one eval smoke case.
- `human_gate`: pass - public final copy requires human review.

## Proof Plan

Run `python3 skills/skill-maintenance/scripts/check_skills.py --write` and
`python3 -m json.tool skills/copywriting-advisor/eval_task.json`.
