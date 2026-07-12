---
skill: lead-scout
date: 2026-07-12
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/lead-scout/SKILL.md
after_ref: skills/lead-scout/SKILL.md
reasoning_basis: advise
proof_artifacts:
  - skills/lead-scout/qa_checklist.md
  - skills/lead-scout/examples/public-founder-scout/example.md
eval_required: yes
---

# Skill Audit

## Change

- Before: CRM writeback mixed report paths, owner, next action, and status.
- After: CRM writeback is limited to entity identity, description, links, and
  status; candidate packets remain skill-owned reports.
- Why: CRM is a relationship ledger, not a workflow artifact index.
- Tradeoff accepted: next actions are found in reports rather than directly on
  the entity record.

## First-Principles Reasoning

- Objective: keep prospect qualification useful without expanding CRM schema.
- Placement logic: `lead-scout` owns candidate packets; CRM owns entity state.
- Expected behavior delta: callers receive `crm_entity_delta`, not an index or
  report-path writeback.
- Proof needed: checklist/example consistency, skill validation, and review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Signature and writeback step name the new boundary. |
| `reference_load_precision` | pass | Existing example demonstrates the entity delta. |
| `missing_context_rate` | unknown | No post-change invocation corpus exists yet. |
| `noisy_context_rate` | unknown | No post-change invocation corpus exists yet. |
| `duplicated_instruction_count` | pass | Old report/index writeback wording was replaced. |
| `prompt_size_tokens` | unknown | Token comparison is not required for this behavior migration. |
| `task_success_rate` | unknown | Runtime eval has not yet been sampled. |
| `review_tas_rate` | pass | Independent rerun returned TAS-A with no blockers. |
| `maintenance_locality` | pass | Candidate reports stay with `lead-scout`; entities stay in CRM. |
| `composition_clarity` | pass | The example shows the `customer-research` entity handoff. |

## Proof Artifacts

- Skill-local evals, when needed: the safety eval now enforces the exact
  five-field CRM boundary and rejects workflow/report fields.
- Structure evals, when needed: `check_skills.py --write`.
- Reviewer receipt: TAS-A; skill-contract, eval-quality, and integration-readiness passed.
- Validator: skill checker and bootstrap fixture.
- Eval required: yes; the changed CRM writeback boundary is covered statically.
- Evidence gaps: no live post-change lead-scout invocation yet.

## Before Behavior

- CRM writeback included workflow and report-reference fields.

## After Behavior

- CRM writeback changes only the five-field entity record; reports carry
  workflow detail and entity references.

## Followups

- None unless a real caller needs an additional CRM field.
