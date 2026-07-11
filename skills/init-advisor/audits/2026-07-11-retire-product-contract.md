---
skill: init-advisor
date: 2026-07-11
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/init-advisor/SKILL.md@pre-TASK-0321
after_ref: skills/init-advisor/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - tickets/TASK-0321/ticket.md
eval_required: yes
---

# Init Advisor Product-Contract Retirement Audit

## Change

- Before: initialization promised product definitions, a generated product
  index, and product-local workflow files.
- After: initialization creates the charter, goals, ticket/proof substrate,
  automation config, and a project-local capability-skill home.
- Why: recurring workflow categories must not become planners or runtime
  controllers.
- Tradeoff accepted: initialization no longer supplies a structured category
  catalog; consumers use goals, capability refs, skills, and tickets.

## First-Principles Reasoning

- Objective: create the smallest usable project substrate.
- Placement logic: init owns scaffold shape; skills own recurring workflows.
- Expected behavior delta: a clean bootstrap has no product-controller files.
- Proof needed: eval JSON, template sweep, clean-bootstrap and project-file
  validation owned by TASK-0321.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Signature and todo still describe substrate, readiness, and handoff. |
| `reference_load_precision` | pass | Deleted template refs were removed; remaining refs keep load conditions. |
| `missing_context_rate` | pass | Charter, goals, capability, ticket, and automation owners are explicit. |
| `noisy_context_rate` | pass | Retired file inventory removed. |
| `duplicated_instruction_count` | pass | Automation detail remains in its template. |
| `prompt_size_tokens` | unknown | No token benchmark run; line count fell from 261 to 254. |
| `task_success_rate` | unknown | Clean-bootstrap QA belongs to the parent ticket. |
| `review_tas_rate` | unknown | Parent reviewer pending. |
| `maintenance_locality` | pass | Changes stay in init-owned prompt, refs, eval, and checklist. |
| `composition_clarity` | pass | Harness Creator owns full-mode meaning; Init owns substrate. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/init-advisor/eval_task.json`
- Structure evals, when needed: scoped old-reference sweep
- Reviewer receipt: pending TASK-0321 reviewer
- Validator: `check_skills.py` and clean-bootstrap checks
- Eval required: yes; changed reference points preserve the retired-file guard
- Evidence gaps: real clean bootstrap and independent reviewer remain parent-owned

## Before Behavior

- Generated and required product definition/index files.

## After Behavior

- Produces a product-independent substrate and capability-workflow handoff.

## Followups

- TASK-0322 must finish the metrics/manifest side of the clean scaffold.
