---
skill: weekly-pm-plan
date: 2026-06-20
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/weekly-pm-plan/SKILL.md
after_ref: skills/weekly-pm-plan/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/weekly-pm-plan/templates/report.md
  - skills/weekly-pm-plan/templates/context-bundle.md
  - skills/weekly-pm-plan/eval_task.json
  - tickets/TASK-0204/progress.md
eval_required: yes
---

# Skill Audit

## Change

- Before: `weekly-pm-plan` accepted context refs and wrote weekly reports, but
  it did not own concrete report/context templates or an explicit promotion
  boundary before mutating `farplane/goals.md`.
- After: `weekly-pm-plan` owns `templates/report.md`,
  `templates/context-bundle.md`, and a `goals_delta` promotion policy with
  `auto_apply`, `approval_required`, and `rejected_source_gap`.
- Why: weekly planning needs an auditable evidence record while keeping
  `goals.md` as canonical portfolio state rather than a weekly diary.
- Tradeoff accepted: one promotion boundary adds a small extra step in exchange
  for lower strategy-drift risk.

## First-Principles Reasoning

- Objective: make weekly strategy updates useful for daily/heartbeat execution
  without silently rewriting long-horizon strategy.
- Placement logic: the workflow belongs in `weekly-pm-plan`; project-specific
  cadence and paths stay in `farplane/automations.md`.
- Expected behavior delta: weekly PM writes a context bundle and weekly report,
  then promotes only eligible goals deltas.
- Proof needed: templates exist, eval guardrails cover promotion policy, and
  skill/registry/eval checks pass.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` now names templates, promotion policy, gates, fails, checklist, and outputs. |
| `reference_load_precision` | pass | Detailed report/context shape lives in `templates/` and is linked from the skill. |
| `missing_context_rate` | unknown | Requires a live weekly run to measure. |
| `noisy_context_rate` | unknown | Requires a live weekly run to measure. |
| `duplicated_instruction_count` | pass | Manifest points to template refs and presets rather than copying the runbook. |
| `prompt_size_tokens` | unknown | Not measured. |
| `task_success_rate` | unknown | Static eval/unit tests pass; no live automation run yet. |
| `review_tas_rate` | unknown | No reviewer lane was required for this scoped change. |
| `maintenance_locality` | pass | Changes are local to `weekly-pm-plan` plus call-site refs. |
| `composition_clarity` | pass | `weekly-strategy-analysis` remains the personal wrapper; generic policy stays in `weekly-pm-plan`. |

## Proof Artifacts

- Skill-local evals: `weekly_pm_plan_goals_delta_promotion_01` and
  `weekly_pm_plan_quarterly_yearly_rollup_01`.
- Structure evals: `python3 skills/skill-maintenance/scripts/check_skills.py --write` passed.
- Validator: `python3 -m json.tool skills/weekly-pm-plan/eval_task.json`,
  `python3 skills/eval/tests/test_run_evals.py`, and `git diff --check`
  passed.
- Eval required: yes.
- Evidence gaps: no live weekly PM report has been generated from the new
  templates yet.

## Before Behavior

- Weekly PM could synthesize strategy, but report shape and `goals.md` mutation
  promotion were implicit.

## After Behavior

- Weekly PM must write the report before `goals.md` mutation and must classify
  every goals delta as auto-applied, approval-required, or rejected due to a
  source gap.

## Followups

- Run one weekly PM dry run after live automations are recompiled.
- Add a live automation compiler/checker only under a separate ticket.
