---
skill: goal-advisor
date: 2026-06-13
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/work/SKILL.md; skills/ralph/SKILL.md; skills/batch-work/SKILL.md; skills/goal-advisor/SKILL.md
after_ref: skills/goal-advisor/SKILL.md; docs/specs/goal-loop-contract.md; tickets/templates/goal-loop/program.md
reasoning_basis: deliberative_advice
proof_artifacts:
  - tickets/TASK-0196/ticket.md
eval_required: no
---

# Execution Compiler Consolidation Audit

## Change

- Before: `goal-advisor`, `$work`, `$ralph`, and `batch-work` all owned overlapping parts of admission, board selection, batching, and continuation.
- After: `goal-advisor` is the canonical execution compiler. It emits native Goal, heartbeat, batch, rollout, feedback, or direct-route prompts over an inline `Files:` list. `$impl` remains the coding-ticket leaf executor.
- Why: Native Goals and heartbeat patterns now make continuation a time-window and budget decision, not a reason to keep several public execution routers.
- Tradeoff accepted: Purging the old skill packages removes duplicate surfaces immediately, but old habits or external notes may need migration to `goal-advisor`.

## First-Principles Reasoning

- Objective: Make material Farplane execution simpler without losing ticket proof, board-drain safety, or batch-work constraints.
- Placement logic: Goal shape, file selection, budget, trigger mode, and proof policy are one decision; putting them in `goal-advisor` avoids inconsistent routers.
- Expected behavior delta: Operators call `goal-advisor` for request, ticket, batch, board, epic, or metric-loop compilation, then run the selected native Goal, heartbeat, or `$impl` leaf route.
- Proof needed: Skill registry validation, stale-reference sweep, prompt-template consistency, and JSON parse of the skill eval task.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `skills/goal-advisor/SKILL.md` contains the execution compiler contract, route table, batch guidance, and prompt templates. |
| `reference_load_precision` | pass | Inline `Files:` is standard; references are reserved for optional examples and complex patterns. |
| `missing_context_rate` | pass | Goal prompt template now requires all relevant files to be listed before execution. |
| `noisy_context_rate` | pass | Purged three overlapping public skill packages from active skills. |
| `duplicated_instruction_count` | pass | Board drain and batch policy now live in Goal Advisor and the Goal loop contract. |
| `prompt_size_tokens` | pass | File lists avoid flattening multiple tickets into one large prompt. |
| `task_success_rate` | unknown | Needs production use on the next material batch or board-drain Goal. |
| `review_tas_rate` | unknown | No independent reviewer lane was run in this pass. |
| `maintenance_locality` | pass | Canonical behavior is in `goal-advisor`, `goal-loop-contract`, and templates. |
| `composition_clarity` | pass | Public route is now `PRD/spec/ticket -> goal-advisor -> native Goal/heartbeat/batch/direct -> impl when coding leaf`. |

## Proof Artifacts

- Skill-local evals, when needed: `python3 -m json.tool skills/goal-advisor/eval_task.json >/dev/null` passed.
- Structure evals, when needed: `python3 skills/skill-maintenance/scripts/check_skills.py --write` passed.
- Reviewer receipt: none; this pass used self-check plus validator proof.
- Validator: `git diff --check` passed.
- Eval required: no new automated behavior eval required for this doc/skill consolidation.
- Evidence gaps: first live batch or board-drain Goal should be watched for prompt size, proof logging, and stale external habit issues.

## Before Behavior

An operator could reasonably route material execution through `$work`,
`$ralph`, `batch-work`, `$impl`, or `goal-advisor`, creating duplicate admission
and batching decisions before native Goal mode was even selected.

## After Behavior

An operator routes material execution through `goal-advisor`, which compiles the
listed files, trigger mode, budget, metric, proof policy, and downstream route.
Native Goal mode owns uninterrupted leaf execution windows; heartbeat owns
pause/resume, board drain, and long-duration monitoring; `$impl` owns selected
coding-ticket leaves.

## Followups

- Use the new prompt on one real batch Goal with multiple ticket file triples.
- Use the heartbeat board-drain pattern on one low-risk board slice before
adding any automation around it.
