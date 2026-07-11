---
skill: pulse-update
date: 2026-07-10
change_type: behavior
owner: skill-maintenance
status: accepted
review_route: reviewer
before_ref: skills/pulse-update/SKILL.md@586-lines-product-scoped
after_ref: skills/pulse-update/SKILL.md@229-lines-project-work-pulse
reasoning_basis: reviewer
proof_artifacts:
  - tickets/TASK-0318/artifacts/review/plan-review.md
  - tickets/TASK-0318/artifacts/qa/work-pulse-proof.md
eval_required: yes
---

# Pulse Update Skill Audit

## Change

- Before: a 586-line product-scoped manager reconciled product loops, product
  rewards, product-local worker budgets/review caps, planning, review chasing,
  and board admission.
- After: a 229-line project Work Pulse reconciles one board, dispatches generic
  executable tickets, calls a pure planner only on empty-board refill, releases
  workers at human review, and writes visible receipts.
- Why: prove the `do ticket else plan` kernel before specialization.
- Tradeoff accepted: detailed review messaging and ticket quality remain in
  owner skills; Interval planning semantics remain until Workstream 2.

## First-Principles Reasoning

- Objective: one project-level executor/manager loop with visible state.
- Placement logic: `pulse-update` owns board side effects; planner, Goal
  compilation, domain capability work, and review-message detail remain separate.
- Expected behavior delta: product origin no longer affects admission or refill.
- Proof needed: controlled board fixtures, two skill evals, automation
  inventory, registry validation, and reviewer TAS-A.

## First-Load Review

```text
first_load_review:
  line_count_before: 586
  line_count_after: 229
  kept_in_skill:
    - reconciliation, eligibility, mode choice, planner call, materialization, dispatch, review release, report/receipt gates
  moved_to_reference:
    - none; existing owner skills retain ticket planning, Goal compilation, and review-message contracts
  deleted_as_duplicate_or_rationale:
    - product controller input contract and invocation receipts
    - product-local worker budgets and review caps
    - product-backed reward admission
    - product strategy and product progress selection
    - duplicated ticket-quality fields already owned by the planner
    - long review-chase mechanics already owned by worker-artifact-review-request
  extra_sections_kept_with_reason:
    - Automation Preset: normal invocation parameters are required on first load
    - Worker Handoff Contract: the shared executor boundary is a core Work Pulse gate
    - Execution Modes: compact state-machine vocabulary is required for repeatability
  remaining_sections_over_budget: none
  proof_surface_fit: deterministic classifier tests plus behavior evals and reviewer
  task_case_quality: four distinct high-value Pulse boundaries selected for focused run from six stored cases
  anti_cheat_case_design: queries use natural project heartbeat scenarios
  qa_preflight_loaded: no target checklist; skill-maintenance checklist applied
  qa_finish_independence: completion reviewer required
  qa_gotcha_deduplication: concise gotchas only
  project_specific_context_isolation: pass
  low_value_prose_scan: product rationale and duplicated workflow prose deleted
  verdict: pass pending completion reviewer
```

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Signature, numbered todo, handoff, modes, gates, and refs are in `SKILL.md`. |
| `reference_load_precision` | pass | Each linked skill has one explicit call condition. |
| `missing_context_rate` | pass | Admission, refill, review, side-effect, proof, and writeback gates remain first load. |
| `noisy_context_rate` | pass | Product/controller/strategy/reward detail removed. |
| `duplicated_instruction_count` | pass | Ticket quality and review-message detail point to their owners. |
| `prompt_size_tokens` | pass | 229 lines, down from 586. |
| `task_success_rate` | pass | Review-state repair passed 3/3 and Interval-boundary check passed 1/1 at TAS-A. |
| `review_tas_rate` | pass | Completion reviewer passed all seven families at TAS-A. |
| `maintenance_locality` | pass | Pulse owns state transitions; linked skills own specialized contracts. |
| `composition_clarity` | pass | Inputs, writes, gates, modes, and handoff are explicit. |

## Proof Artifacts

- Skill-local evals: `skills/pulse-update/eval_task.json`
- Deterministic tests: `skills/pulse-update/scripts/test_list_pulse_board.py`
- Behavior eval: `.farplane/evals/runs/20260710-135010-task-0318-work-pulse-review-state-gpt55` (3/3 TAS-A)
- Interval-boundary eval: `.farplane/evals/runs/20260710-135432-task-0318-work-pulse-interval-boundary-gpt55` (1/1 TAS-A)
- Live automation: `tickets/TASK-0318/artifacts/qa/live-automation-migration.md`
- Reviewer receipt: `tickets/TASK-0318/artifacts/review/completion-review.md`
- Validator: `check_skills.py --write` passed before final rerun
- Evidence gaps: none for Workstream 1

## Followups

- Workstream 2 removes Interval planning/ticket-delta semantics.
- Workstream 3 removes retained product files and manifest readers.
