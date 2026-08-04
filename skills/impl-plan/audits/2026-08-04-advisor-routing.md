---
skill: impl-plan
date: 2026-08-04
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: git:HEAD:skills/impl-plan/SKILL.md
after_ref: working-tree:skills/impl-plan/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/impl-plan/evals/evals.json
  - tickets/TASK-9015/artifacts/qa/validation.md
  - tickets/TASK-9015/artifacts/review/completion-review.md
eval_required: yes
---

# Impl Plan Advisor Routing Audit

## Change

- Before: The planner grounded material code changes but did not require a
  repository capability inventory or conditional UI, landing, offer, visual,
  asset, and official-documentation inputs.
- After: The planner inventories internal leverage, records bounded
  call-or-skip decisions, integrates advisor outputs into one Change Plan, and
  runs an explicit lean-plan gate before Goal compilation.
- Why: One implementation planner can cover product, frontend, landing, and
  backend work when domain judgment arrives as bounded inputs rather than child
  plans.
- Tradeoff accepted: Material plans gain a small routing ledger; settled local
  work may skip every irrelevant advisor with compact evidence.

## First-Principles Reasoning

- Objective: Produce the smallest executable software Change Plan using the
  strongest capabilities already present in the repository and skill system.
- Placement logic: Repository inspection and route selection belong in the
  planning compiler because they determine the implementation units; advisor
  craft remains in the existing owner skills.
- Expected behavior delta: UI and landing plans stop relying on planner
  intuition, while localized backend work avoids unnecessary workflow calls.
- Proof needed: Representative UI, landing, and backend eval cases; structure,
  tier, registry, JSON, and diff checks; reviewer inspection of recursion and
  minimality boundaries.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Signature, phase boundary, and Todo 3-8 expose inventory, routing, integration, and lean gates. |
| `reference_load_precision` | pass | Template and QA remain deferred until drafting/checking; advisor skills load only when their condition is open. |
| `missing_context_rate` | pass | Three selected live cases supplied only the bounded rule or advisor packets needed for the tested decision and reached A after fixture repair. |
| `noisy_context_rate` | pass | Lean backend and app UI cases skipped irrelevant advisor/research branches without adding ceremony. |
| `duplicated_instruction_count` | pass | One routing table owns advisor decisions; prompt and template consume rather than redefine it. |
| `prompt_size_tokens` | unknown | No before/candidate token measurement was run. |
| `task_success_rate` | pass | Lean backend and app UI live receipts both reached A with pass rate 1.0. |
| `review_tas_rate` | pass | TASK-9015 completion review passed TAS-A with no hard-gate failures. |
| `maintenance_locality` | pass | Changes remain inside impl-plan, the narrowed landing-page owner, generated registry, and ticket evidence. |
| `composition_clarity` | pass | Advisors return bounded inputs; impl-plan owns the single Change Plan; goal-advisor owns execution compilation. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/impl-plan/evals/evals.json`.
- Structure evals, when needed: quick validation, todo-tier, surface-budget,
  eval-query, registry, JSON, and diff checks in the ticket QA receipt.
- Reviewer receipt: `tickets/TASK-9015/artifacts/review/completion-review.md`.
- Validator: `tickets/TASK-9015/artifacts/qa/validation.md`.
- Eval required: yes; behavior changed.
- Evidence gaps: The full five-case impl-plan suite was not run; the selected
  lean backend and app UI cases cover this change's critical branches.

## Before Behavior

- A UI plan could be structurally complete without a settled workflow or
  visual system.
- A landing plan did not mechanically integrate offer, assets, or current API
  documentation.
- Internal components, assets, and knowledge sources were not an explicit
  reuse-first planning input.

## After Behavior

- Each applicable advisor route records its condition, decision, expected
  output, evidence, and exact Change Plan integration.
- Settled routes can be skipped without ceremony.
- One lean Change Plan remains the only implementation-planning artifact.

## Followups

- Keep all five impl-plan rows as the broader regression surface for the next
  semantic change.
