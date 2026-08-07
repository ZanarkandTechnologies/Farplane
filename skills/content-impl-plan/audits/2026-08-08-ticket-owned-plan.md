---
skill: content-impl-plan
date: 2026-08-08
change_type: structure
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: tickets/TASK-9019/ticket.md
after_ref: skills/content-impl-plan/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - docs/skills/composition.md
  - tickets/TASK-9019/artifacts/validation/complete.md
  - tickets/TASK-9019/artifacts/review/completion-review.md
eval_required: no
---

# Skill Audit: Ticket-Owned Content Plan

## Change

- Before: the action graph could be represented by a ticket, a named plan, and
  a versioned JSON program with a validator.
- After: `ticket.md` is the only plan container. Its `Change Plan` holds one
  compact content action-graph snippet; `Done` and `QA Strategy` hold proof.
- Why: one plan needs one durable source of truth and the same planner contract
  as `impl-plan`.
- Tradeoff accepted: the JSON projection and shadow field map were removed
  because no caller consumed them; detailed packets remain child-owned.

## First-Principles Reasoning

- Objective: preserve the complete artifact-birth route while deleting duplicate
  state, template, and maintenance surfaces.
- Placement logic: durable action graph and proof belong to the canonical ticket;
  the skill's compact ticket addition owns the only content-specific ticket
  shape, while child references keep their own detailed packets.
- Expected behavior delta: content planning returns one ticket and its next
  owner, never a parallel plan artifact.
- Proof needed: registry regeneration, stale-surface search, ticket validation,
  and independent review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | compact ticket addition gives the planner's required output without a shadow appendix |
| `reference_load_precision` | pass | first load contains only the compact addition; child packets remain owner-local references |
| `duplicated_instruction_count` | pass | named plan, JSON program, validator, test, and shadow field map are removed |
| `maintenance_locality` | pass | ticket template, composition doc, content skill, and system record own their respective contracts |
| `composition_clarity` | pass | action graph remains owner-separated inside `Change Plan` |
| `proof_surface_fit` | pass | complete validation and focused completion review both pass |

## Proof Artifacts

- Eval skip: owner-routing scenarios and focused eval cases are unchanged; this
  is a source-of-truth consolidation with deterministic registry/search checks.
- Validation: complete-phase pass in
  `tickets/TASK-9019/artifacts/validation/complete.md`.
- Reviewer receipt: `TAS-A` pass in
  `tickets/TASK-9019/artifacts/review/completion-review.md`.

## Followups

- None unless review finds a live consumer for a derived production-program
  projection.
