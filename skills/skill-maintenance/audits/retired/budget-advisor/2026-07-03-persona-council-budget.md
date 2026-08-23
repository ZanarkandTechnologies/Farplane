---
title: "Budget Advisor Persona Council Simplification"
status: complete
owner: budget-advisor
created_at: 2026-07-03T01:20:00+08:00
ticket_id: TASK-0270
refs:
  - tickets/TASK-0270/ticket.md
  - tickets/TASK-0270/artifacts/review-receipt.md
  - skills/budget-advisor/SKILL.md
---

# Budget Advisor Persona Council Simplification

## Change

Replaced Budget Advisor's public budget model with a simpler contract:

- `base`: the caller skill's normal reviewed path
- `plus`: a small persona council, normally three complete prompts
- `max`: a bounded five-persona council plus synthesis

Budget no longer buys recursive review loops or large same-action fanout. Child
skills use their own base reviewed path unless the caller explicitly allocates
child budget through `delegate_budget`.

## Files Updated

- `skills/budget-advisor/SKILL.md`
- `skills/budget-advisor/references/budget-modes.md`
- `skills/budget-advisor/references/ensemble-lanes.md`
- `skills/budget-advisor/references/advise-example.md`
- `skills/budget-advisor/eval_task.json`
- `skills/deliberative-advice/SKILL.md`
- `skills/runtime-debugging/SKILL.md`
- `skills/runtime-debugging/references/budget-personas.md`
- `skills/hardening/SKILL.md`
- `skills/hardening/references/budget-personas.md`
- `skills/refactoring/SKILL.md`
- `skills/refactoring/references/budget-personas.md`
- `docs/skills/README.md`
- `docs/fundamentals/harness-algebra.md`

## Guardrails Preserved

- Budget Advisor still returns instructions and does not execute subagents.
- Caller skills preserve their own output contracts.
- Complete persona prompts are required for persona councils.
- The base reviewed path stays mandatory for material skill work.
- Removed references are not retained as supported routes.

## Proof

Validation and final review evidence live in:

- `tickets/TASK-0270/progress.md`
- `tickets/TASK-0270/artifacts/`
