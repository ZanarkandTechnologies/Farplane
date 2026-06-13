---
skill: reference-grounding
date: 2026-06-12
change_type: behavior
owner: skill-maintenance
status: pass
review_route: deliberative_advice
before_ref: skills/reference-grounding/SKILL.md@pre-change
after_ref: skills/reference-grounding/SKILL.md
reasoning_basis: deliberative_advice
proof_artifacts:
  - skills/skill-maintenance/scripts/check_skills.py --write
eval_required: yes
---

# Skill Audit

## Change

- Before: `reference-grounding` allowed local files to satisfy implementation
  grounding even when the real decision depended on current external practice.
- After: implementation choices must classify the source need and use current
  official docs, maintained examples, or peer implementations unless the task is
  tiny, local-only, or already freshly grounded.
- Why: feature implementation quality depends on recent blocks, docs, and
  examples that may not exist in model memory or local files.
- Tradeoff accepted: more search latency for implementation tasks in exchange
  for fewer stale or self-invented designs.

## First-Principles Reasoning

- Objective: make implementation work external-current by default while keeping
  compact grounding cheaper than full research.
- Placement logic: `reference-grounding` owns the Tier 1 evidence gate;
  `research` owns broader current-source passes; the global template owns the
  cross-repo default.
- Expected behavior delta: agents should check current docs/examples before
  choosing an implementation approach and route larger source sets to
  `research:*`.
- Proof needed: skill-system validation plus a follow-up behavior eval that
  prompts for feature implementation and checks for current external evidence.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Source classification and implementation default are in `SKILL.md`. |
| `reference_load_precision` | pass | Long research remains in `research:*`; no new reference required. |
| `missing_context_rate` | pass | The missing current-source trigger is now explicit. |
| `noisy_context_rate` | pass | The rule is short and scoped to implementation/current-source decisions. |
| `duplicated_instruction_count` | pass | Global template states the default; skill owns the operational gate. |
| `prompt_size_tokens` | pass | First-load increase is small. |
| `task_success_rate` | unknown | Needs behavior eval artifacts. |
| `review_tas_rate` | unknown | No reviewer receipt yet. |
| `maintenance_locality` | pass | Tier 1 gate, Tier 2 research, and global default have distinct jobs. |
| `composition_clarity` | pass | Source need and escalation routes are named. |

## Proof Artifacts

- Skill-local evals, when needed: follow-up recommended.
- Structure evals, when needed: not required for this patch.
- Reviewer receipt: not collected in this direct patch.
- Validator: `skills/skill-maintenance/scripts/check_skills.py --write`.
- Eval required: yes, to prove behavior in live agent runs.
- Evidence gaps: no live agent behavior eval has been run yet.

## Before Behavior

- A feature implementation request could ground only in local files and then
  proceed from model memory.

## After Behavior

- A feature implementation request should inspect local fit, then check current
  official docs, maintained examples, or peer implementations before selecting
  the approach.

## Followups

- Add a focused behavior eval for "implement a feature using best current
  practice" prompts.
