---
skill: impl-plan
date: 2026-06-23
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/impl-plan/SKILL.md@missing-docs-closeout-route
after_ref: skills/impl-plan/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/impl-plan/SKILL.md
  - skills/impl-plan/references/template.md
  - skills/impl-plan/prompts/plan.md
  - skills/impl-plan/qa_checklist.md
eval_required: no
---

# Skill Audit

## Change

- Before: material `impl-plan` output named proof and Goal Packet preview, but
  did not explicitly name the documentation/closeout owner.
- After: material plans include a `Documentation / Closeout` route: default to
  `close-ticket` for final writeback and durable docs changed; call
  `documentation` only for substantive durable doc writing or revision.
- Why: docs can be silently skipped if closeout is omitted, while calling
  `documentation` for routine writeback adds needless ceremony.
- Tradeoff accepted: one compact plan block instead of making documentation a
  mandatory Goal completion step.

## First-Principles Reasoning

- Objective: make documentation ownership visible before approval.
- Placement logic: `impl-plan` names the route; `close-ticket` owns final
  writeback; `documentation` owns substantive durable doc-writing quality.
- Expected behavior delta: plans now show whether docs are not required,
  closeout-only, or a real documentation task.
- Proof needed: checklist entry, prompt/template update, validator, live
  installed copy.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` Todo List requires naming the documentation/closeout route. |
| `reference_load_precision` | pass | `references/template.md` owns the detailed `Documentation / Closeout` block. |
| `missing_context_rate` | pass | Output contract says whether `close-ticket` alone is enough or `documentation` is required. |
| `noisy_context_rate` | pass | Detailed doc closeout fields stay in the template reference. |
| `duplicated_instruction_count` | pass | `impl-plan` names the route; `close-ticket` and `documentation` keep their owner responsibilities. |
| `prompt_size_tokens` | pass | Added compact first-load route without expanding into documentation rules. |
| `task_success_rate` | unknown | No live plan generated after the change. |
| `review_tas_rate` | unknown | No reviewer receipt for this targeted contract edit. |
| `maintenance_locality` | pass | Future changes are local to `impl-plan` routing or owner skills. |
| `composition_clarity` | pass | Plan output distinguishes closeout writeback from substantive documentation. |

## Proof Artifacts

- Skill-local evals, when needed: not changed.
- Structure evals, when needed: checklist self-review.
- Reviewer receipt: skipped; targeted behavior contract edit.
- Validator: `python3 scripts/check_skills.py --write` from
  `skills/skill-maintenance`.
- Eval required: no.
- Evidence gaps: no live plan output demonstrates the new block yet.

## Before Behavior

- A plan could approve implementation without naming docs closeout.

## After Behavior

- The end of the plan names `close-ticket` and, when warranted,
  `documentation` before approval.

## Followups

- Consider migrating `documentation` itself to template `0.3.0` and a root
  `qa_checklist.md`.
