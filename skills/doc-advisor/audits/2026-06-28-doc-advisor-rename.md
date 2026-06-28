---
skill: doc-advisor
date: 2026-06-28
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: retired documentation-skill package
after_ref: skills/doc-advisor/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - tickets/TASK-0241/ticket.md
  - tickets/TASK-0241/artifacts/documentation-skill-reference-inventory.md
eval_required: yes
---

# Skill Audit

## Change

- Before: the reusable docs workflow used the retired documentation-skill name,
  and ticket planning used a closeout-shaped docs block with routine completion
  fields.
- After: the package is `skills/doc-advisor/`, the skill identity is
  `doc-advisor`, and planning surfaces use `Docs Strategy` with `update_docs`
  or `no_docs`.
- Why: the skill behaves like an advisor for durable docs strategy and quality,
  while ticket closeout belongs to `close-ticket`.
- Tradeoff accepted: historical prose and domain terms such as Documentation OS
  remain where they name the product/documentation domain rather than the skill.

## First-Principles Reasoning

- Objective: make the docs update obligation visible during implementation
  planning without duplicating the skill or preserving a legacy skill name.
- Placement logic: skill identity and package paths belong in `skills/`;
  planning schema belongs in `impl-plan` and ticket templates; routine final
  ticket closure stays in `close-ticket`.
- Expected behavior delta: agents call `doc-advisor` for docs strategy,
  durable-doc edits, and doc quality, and they use `Docs Strategy` instead of a
  closeout route in plans and tickets.
- Proof needed: source refs move to the new path, generated registries refresh,
  runtime no longer accepts the retired docs-closeout alias, and validators pass.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `skills/doc-advisor/SKILL.md` names strategy, branch references, gates, and output schema. |
| `reference_load_precision` | pass | Branch references remain under `skills/doc-advisor/references/`. |
| `missing_context_rate` | pass | `qa_checklist.md` now carries the no-docs reason and forbidden-field guardrails. |
| `noisy_context_rate` | pass | Closeout ceremony moved out of the docs planning schema. |
| `duplicated_instruction_count` | pass | No duplicate skill package is retained. |
| `prompt_size_tokens` | pass | Rename adds one strategy block and does not expand first-load workflow breadth. |
| `task_success_rate` | unknown | Requires future live planning samples. |
| `review_tas_rate` | unknown | Requires future reviewer receipts after plans use the new schema. |
| `maintenance_locality` | pass | Changes stay in skill, impl-plan, ticket template, runtime alias tests, and registries. |
| `composition_clarity` | pass | `doc-advisor` owns docs strategy; `close-ticket` owns final ticket closure. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/doc-advisor/eval_task.json`
- Structure evals, when needed: `skills/skill-maintenance/scripts/check_skills.py --write`
- Reviewer receipt: pending final ticket review
- Validator: pending final validation bundle
- Eval required: yes, one docs-strategy eval row added
- Evidence gaps: live behavior should be checked on the next material
  `impl-plan` output.

## Before Behavior

- Plans could ask for docs closeout fields that blurred documentation advice
  with ticket completion.
- Skill routing used a generic docs identity even though callers used it as an
  advisor.

## After Behavior

- Plans carry a compact `Docs Strategy` block with `outcome`, `doc_targets`,
  `no_docs_reason`, and `validation`.
- The skill is called `doc-advisor` and supports durable doc strategy, document
  edits, and quality finish gates.

## Followups

- Reinstall repo-owned skills when live installed skill packages should reflect
  the rename.
