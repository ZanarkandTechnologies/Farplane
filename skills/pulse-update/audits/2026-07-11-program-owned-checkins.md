---
skill: pulse-update
date: 2026-07-11
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/pulse-update/SKILL.md; skills/pulse-update/eval_task.json
after_ref: skills/pulse-update/SKILL.md; skills/pulse-update/eval_task.json
reasoning_basis: first_principles
proof_artifacts: []
eval_required: yes
---

# Pulse Program-Owned Check-In Audit

## Change

- Before: Pulse handed due rows plus generic Metric, Heartbeat, Stop, and
  Rollout sections, which left room for the dispatcher to restate policy.
- After: Pulse hands the original ticket/program/progress, matured indexes,
  time, and evidence refs; the worker executes `program.md` first.
- Why: due-row scheduling and experiment decisions need different owners.
- Tradeoff accepted: malformed legacy packets stop for Goal Advisor repair
  instead of receiving an inferred check-in policy.

## First-Principles Reasoning

- Objective: keep one check-in scorer without turning Pulse into a planner.
- Placement logic: Pulse owns eligibility and dispatch only.
- Expected behavior delta: retries preserve future/completed rows and reuse the
  original packet's program.
- Proof needed: eval references, existing board projection tests, and composed
  delayed-check-in QA.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Todo and handoff schema name all runtime inputs. |
| `reference_load_precision` | pass | No new Pulse reference needed. |
| `missing_context_rate` | pass | Missing/non-executable program has an explicit repair route. |
| `noisy_context_rate` | pass | No experiment-specific algorithm added to Pulse. |
| `duplicated_instruction_count` | pass | Decision policy was removed from the dispatcher contract. |
| `prompt_size_tokens` | unknown | First load grew from 259 to 270 lines; execution-mode and receipt detail remain the largest future compaction candidates. |
| `task_success_rate` | unknown | Requires a live worker check-in. |
| `review_tas_rate` | unknown | Pending TASK-0320 reviewer. |
| `maintenance_locality` | pass | Pulse owns dispatch; Goal Program owns check-in instructions. |
| `composition_clarity` | pass | Handoff fields expose ticket, program, progress, indexes, evidence, and instruction. |

## Proof Artifacts

- Skill-local evals: updated delayed-reward cases
- Structure evals: skill validator
- Reviewer receipt: pending TASK-0320 completion review
- Validator: pending focused validation
- Eval required: yes
- Evidence gaps: no live check-in handoff receipt yet

## Before Behavior

- Pulse could implicitly tell the worker how to interpret generic policy.

## After Behavior

- Pulse derives due rows and dispatches; the original program exclusively owns
  evidence, scoring, decisions, writeback, and source-gap rules.

## Followups

- Compact the wider Pulse first-load receipt/execution documentation in a
  separate behavior-preserving refinement.
