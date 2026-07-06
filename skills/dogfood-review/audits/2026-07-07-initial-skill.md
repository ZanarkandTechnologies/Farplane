---
skill: dogfood-review
date: 2026-07-07
change_type: structure
owner: skill-creator
status: pass
review_route: self_check
before_ref: none
after_ref: skills/dogfood-review/SKILL.md
reasoning_basis: advise
proof_artifacts:
  - skills/dogfood-review/eval_task.json
  - skills/dogfood-review/qa_checklist.md
eval_required: yes
---

# Skill Audit

## Change

- Before: Tracked feature dogfooding had no reusable owner; Daily Interval could
  summarize reports but did not own bulk feature trial judgment.
- After: `dogfood-review` owns registry `track` prompts, evidence gathering,
  grouped ticket-batch judgment, and dated dogfood reports.
- Why: The operator needs frequent callable review of dogfooded behavior such
  as high-volume Pulse ticket spawning without visiting every worker thread.
- Tradeoff accepted: Adds one Tier 3 skill surface instead of expanding
  `interval-update` or letting Pulse grade itself.

## First-Principles Reasoning

- Objective: turn compact registry prompts into evidence-backed review reports.
- Placement logic: feature/system registries opt into tracking; this skill owns
  review logic; interval-update only schedules and links the result.
- Expected behavior delta: tracked rows now produce grouped continue/adjust/cap
  decisions and report paths under `.farplane/reports/dogfood-review/`.
- Proof needed: skill validator, registry validator, and eval row shape.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` includes trigger, signature, gates, todos, template, and output. |
| `reference_load_precision` | pass | Only the report template and owner docs are linked with load conditions. |
| `missing_context_rate` | pass | Required registry/report/ticket reads and write path are first-load. |
| `noisy_context_rate` | pass | Detailed report body lives in `templates/dogfood-report.md`. |
| `duplicated_instruction_count` | pass | Registry stores prompt only; skill owns logic. |
| `prompt_size_tokens` | pass | Skill is below structure-review line pressure. |
| `task_success_rate` | unknown | Needs future eval execution. |
| `review_tas_rate` | unknown | No reviewer lane run for initial creation. |
| `maintenance_locality` | pass | Skill package owns runtime logic; registry docs own `track`. |
| `composition_clarity` | pass | Signature names reads, writes, gates, routes, and fails. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/dogfood-review/eval_task.json`.
- Structure evals, when needed: not run yet.
- Reviewer receipt: not run; self-check used for initial narrow skill creation.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Eval required: yes, future behavior proof should run through `eval`.
- Evidence gaps: no live dogfood report has been generated yet.

## Before Behavior

- Daily Interval could reflect on Pulse outputs but had no reusable tracked
  feature review owner.

## After Behavior

- Daily Interval can call `dogfood-review` for registry rows with non-empty
  `track` text and link the resulting report.

## Followups

- Run a live dogfood review after the next daily interval or manual invocation.
