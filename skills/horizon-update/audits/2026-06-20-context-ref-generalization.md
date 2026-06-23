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
  - skills/weekly-pm-plan/eval_task.json
eval_required: yes
---

# Skill Audit

## Change

- Before: `weekly-pm-plan` described weekly Farplane strategy from fixed repo
  surfaces but did not make the reusable context parameter contract explicit.
- After: `weekly-pm-plan` accepts `context_refs`, writes a bounded context
  bundle, labels missing refs as source gaps, and routes Kenji-specific weekly
  strategy through `weekly-strategy-analysis`.
- Why: the same weekly planning shape should work for project PM automation,
  personal strategy automation, and future deep-init projects without copying
  personal Notion or life paths into the generic skill.
- Tradeoff accepted: the generic skill now depends more on callers supplying
  clear refs, in exchange for less hard-coded context discovery.

## First-Principles Reasoning

- Objective: keep weekly strategy reusable across projects while preserving the
  high-evidence shape already proven by the personal weekly automation.
- Placement logic: the behavior belongs in `weekly-pm-plan`; the personal
  wrapper keeps private/source-specific collection rules.
- Expected behavior delta: weekly planners bind context files/tools as params,
  normalize them into a bundle, and then synthesize strategy.
- Proof needed: eval guardrail plus skill registry validation.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `weekly-pm-plan` now names signature, context params, todo path, routes, and output. |
| `reference_load_precision` | pass | Personal Notion/Codex details stay in `weekly-strategy-analysis`; generic skill only links it as a specialization. |
| `missing_context_rate` | unknown | Requires live automation runs to measure. |
| `noisy_context_rate` | unknown | Requires live automation runs to measure. |
| `duplicated_instruction_count` | pass | The generic skill captures the contract; the specialized skill keeps source-specific procedure. |
| `prompt_size_tokens` | unknown | Not measured. |
| `task_success_rate` | unknown | Requires eval or live run outcomes beyond static checks. |
| `review_tas_rate` | unknown | No reviewer lane was run for this small behavior delta. |
| `maintenance_locality` | pass | Edits are owner-local plus manifest/template call-site refs. |
| `composition_clarity` | pass | `weekly-strategy-analysis` is marked as a wrapper over `weekly-pm-plan`. |

## Proof Artifacts

- Skill-local evals, when needed: `weekly_pm_plan_context_refs_01`.
- Structure evals, when needed: `check_skills.py --write` passed.
- Reviewer receipt: skipped; localized contract change.
- Validator: `python3 skills/eval/tests/test_run_evals.py` and
  `git diff --check` passed.
- Eval required: yes.
- Evidence gaps: no live weekly automation run has exercised the new params yet.

## Before Behavior

- Weekly PM strategy read a fixed Farplane-like set of files and reports.
- The relationship to the existing personal weekly strategy automation was
  implicit.

## After Behavior

- Weekly PM strategy receives `WeeklyPMContext` refs and produces a context
  bundle before synthesis.
- Personal weekly strategy is explicitly a wrapper that pre-fills private and
  Kenji-specific refs.

## Followups

- Recompile live weekly PM automation prompts from the manifest when ready.
- Run one weekly PM dry run to validate the context bundle shape on real inputs.
