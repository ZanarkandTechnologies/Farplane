---
skill: impl-plan
date: 2026-07-11
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/impl-plan/prompts/plan.md@optional-inline-map
after_ref: skills/impl-plan/SKILL.md@required-separate-companion
reasoning_basis: first_principles
proof_artifacts:
  - tickets/archive/TASK-0319/diagrams.md
  - skills/impl-plan/eval_task.json
eval_required: yes
---

# Universal Separate Diagrams Audit

## Change

- Before: the first-load skill required a companion for material work, but the
  operator prompt still allowed an optional inline Mermaid map and tiny fixes
  could claim a not-applicable exemption.
- After: every impl-plan creates and links a separate `diagrams.md`; Mermaid is
  forbidden inside `ticket.md`, and small plans reduce diagram depth rather
  than omit the companion.
- Why: TASK-0319 proved that prompt drift and the exemption let a material plan
  pass without the promised visual surface.
- Tradeoff accepted: even tiny impl-plan tickets create one extra compact file.

## First-Principles Reasoning

- Objective: make diagram generation deterministic and independently readable.
- Placement logic: `impl-plan` owns the mandatory handoff; `diagramming` owns
  rendering; the canonical ticket remains text-only.
- Expected behavior delta: `impl_plan(ticket) -> ticket.md + diagrams.md` on
  every invocation.
- Proof needed: aligned prompt, skill, template, checklist, eval, canonical
  ticket template, and a repaired live ticket example.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Required companion is in signature, gates, todo, fails, and output. |
| `reference_load_precision` | pass | Companion template remains the named rendering reference. |
| `missing_context_rate` | pass | Prompt now names path, template, metadata, and small-ticket behavior. |
| `noisy_context_rate` | pass | Rendering details remain in the companion template. |
| `duplicated_instruction_count` | pass | Repetition is limited to the hard invariant across execution surfaces. |
| `prompt_size_tokens` | pass | The stale optional-map wording was replaced, not accumulated. |
| `task_success_rate` | unknown | Requires future invocation evidence. |
| `review_tas_rate` | pass | Final independent review returned TAS-A across implementation-plan, skill-contract, and evidence-quality. |
| `maintenance_locality` | pass | Behavior remains owned by impl-plan plus diagramming rendering. |
| `composition_clarity` | pass | Ticket contract and visual companion have separate ownership. |

## Proof Artifacts

- Skill-local evals: added tiny-fix universal-companion case.
- Structure evals: `check_skills.py --write` passes.
- Reviewer receipt: final pass / TAS-A after link, existence, structural,
  semantic-class, embedded-asset, installed-copy, and completion-time checks.
- Validator: JSON parse, skill-system validation, no inline Mermaid in TASK-0319.
- Eval required: yes; static eval contract added.
- Evidence gaps: no fresh full planner invocation yet; deterministic source and
  installed-copy behavior plus TASK-0319 validation are proven.

## Before Behavior

- A planner could follow `prompts/plan.md`, omit the optional inline map, and
  never perform the newer companion handoff.

## After Behavior

- Missing `diagrams.md`, inline Mermaid, or a not-applicable exemption fails the
  impl-plan contract.

## Followups

- Observe the next live impl-plan invocation as behavioral confirmation.
