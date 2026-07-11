---
title: Code Audit Ticket Output
owner: code-audit
status: active
kind: reference
---

# Ticket Output

Use this reference before creating or proposing audit follow-up tickets. Tickets
should be small enough to execute and prove, but large enough to fix a coherent
problem.

## Ticket Spec

```text
audit_ticket_spec(finding)
  -> title + scope + route + proof + residual_risk
```

Required fields:

- `title`: short action phrase naming the component and improvement.
- `finding`: what is wrong or risky, with evidence refs.
- `scope_in`: files, modules, docs, tests, or configs included.
- `scope_out`: tempting cleanup, rewrites, or adjacent issues intentionally
  deferred.
- `owner_skill`: `impl-plan`, `refactoring`, `hardening`,
  `runtime-debugging`, `testing`, `doc-advisor`, or another concrete owner.
- `done_when`: behavior, structure, proof, and review conditions.
- `proof`: commands, tests, evals, QA, review gates, or evidence artifacts.
- `residual_risk`: what remains uncertain after this ticket.
- `next_action`: the first executable step for the owner skill.

## Ticket Creation Rules

- Create a ticket only when the finding has enough evidence and a concrete
  owner route.
- Group findings when they share one component, one proof route, and one
  owner skill.
- Split findings when they cross independent runtime boundaries, proof
  surfaces, or risk classes.
- Keep broad audit waves as audit artifacts, not as implementation tickets.
- Use low-confidence ideas as `Evidence gap` rows until a cheap check can
  confirm them.

## Compact Output

```text
Ticket:
  id_or_status: created | proposed
  title:
  owner_skill:
  scope_in:
  scope_out:
  done_when:
  proof:
  evidence:
  residual_risk:
  next_action:
```
