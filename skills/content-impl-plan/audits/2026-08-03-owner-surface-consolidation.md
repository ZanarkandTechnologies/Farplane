---
skill: content-impl-plan
date: 2026-08-03
change_type: maintenance
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: git:HEAD:skills/content-impl-plan
after_ref: skills/content-impl-plan
reasoning_basis: eval
proof_artifacts:
  - .farplane/evals/runs/20260802-200244-task0427-owner-final/summary.json
  - tickets/TASK-0427/artifacts/skill-surface-consolidation.md
  - tickets/TASK-0427/artifacts/skill-consolidation-review.md
eval_required: yes
---

# Content Impl Plan Owner-Surface Consolidation Audit

## Change

- Before: 19 top-level QA checks and 19 broad eval rows exceeded the enrolled
  five-item surface budget; owner routing was scattered through the long skill.
- After: five production-phase QA gates retain the runtime guardrails, five
  focused evals diagnose the TASK-0427 owner boundaries, and one first-load
  owner table plus `AdvisorAction` record makes the sibling contract executable.
- Why: remove a mechanical close blocker while improving owner-route recall,
  not merely reducing counts.
- Tradeoff accepted: broad story/style scenarios remain QA guardrails rather
  than independent runnable eval rows. Their prior IDs and dispositions are
  recorded in the ticket artifact and remain recoverable from git history.

## First-Principles Reasoning

- Objective: preserve production behavior while making the minimum high-value
  behavioral sample diagnostic and keeping each output under one owner.
- Placement logic: every-invocation ownership lives in `SKILL.md`; runtime
  prevention lives in QA; variable routing behavior lives in five evals.
- Expected behavior delta: fewer omitted owner outputs and no duplicated Asset,
  Editing, or Remotion responsibility; no intended story/asset guard is removed.
- Proof needed: surface validator pass, query lint pass, one clean five-case A
  run, and independent skill/eval review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | owner table and five-field action record are in `SKILL.md` |
| `reference_load_precision` | pass | no default-path ownership moved behind a reference |
| `missing_context_rate` | pass | five final owner evals score A |
| `noisy_context_rate` | pass | 19 QA units consolidated into five phase gates |
| `duplicated_instruction_count` | pass | one owner table is canonical; todo/gotchas reinforce only execution failures |
| `prompt_size_tokens` | pass | surface budget validator passes at five QA and five eval units |
| `task_success_rate` | pass | final run is 5/5 A |
| `review_tas_rate` | pass | independent consolidation review is TAS-A |
| `maintenance_locality` | pass | changes remain in the owning skill and its ticket evidence |
| `composition_clarity` | pass | each applicable action exposes owner, inputs, output, gate, and next handoff |

## Proof Artifacts

- Skill-local evals: `.farplane/evals/runs/20260802-200244-task0427-owner-final/summary.json`.
- Structure evals: `python3 skills/skill-maintenance/scripts/check_skills.py --write` passes.
- Reviewer receipt: `tickets/TASK-0427/artifacts/skill-consolidation-review.md` (TAS-A).
- Validator: canonical TASK-0427 complete-phase rerun after review.
- Eval required: yes; the final focused suite ran rather than relying on JSON.
- Evidence gaps: removed broad scenarios are QA-protected but not independently
  sampled in the five-row suite; this intentional tradeoff is recorded in the
  ticket and accepted by the independent reviewer.

## Before Behavior

- The repository rejected the skill at 19 QA checks and 19 eval rows.
- A count-driven five-row matrix prototype scored 0/5 because multi-scenario
  prompts caused summaries instead of executable records.
- A first focused pass scored 3/5 A and exposed two exact first-load omissions.

## After Behavior

- The owner contract is visible before the long production procedure.
- The full final suite scores 5/5 A for missing media, editing direction,
  deterministic rendering, full sibling sequencing, and mixed asset/edit work.
- Skill-system validation passes the surface budget and method-reference schema.

## Followups

- Promote a broad story/style scenario back into the five-row suite only when a
  real regression proves it has higher value than one of the current owner cases.
