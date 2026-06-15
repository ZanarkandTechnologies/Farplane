---
skill: eval
date: 2026-06-13
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/eval/SKILL.md
after_ref: skills/eval/SKILL.md
reasoning_basis: eval
proof_artifacts:
  - tickets/TASK-0200/ticket.md
  - tickets/TASK-0200/program.md
  - tickets/TASK-0200/progress.md
  - tickets/TASK-0200/artifacts/eval-drain/skills-eval-eval_task.report.json
  - tickets/TASK-0200/artifacts/eval-drain/skills-learning-drain-eval_task.report.json
  - tickets/TASK-0200/artifacts/eval-drain/skills-goal-advisor-eval_task.report.json
eval_required: yes
---

# Skill Audit

## Change

- Before: The eval skill could create, run, and repair evals, but had no weekly
  drain for consolidating skill-local eval growth.
- After: The eval skill owns `eval:consolidate`, a thin automation prompt, a
  content-hash discovery script, and a per-file `consolidate_eval` lane
  contract.
- Why: Lesson/trouble-derived evals should land immediately, but redundant
  evals need a later cleanup pass so suites remain strong and runnable.
- Tradeoff accepted: Consolidation requires judgment and review, but avoids
  letting proof cost grow without hiding fresh regressions in a temporary queue.

## First-Principles Reasoning

- Objective: Preserve immediate regression coverage while reducing eval-suite
  noise after coverage exists.
- Placement logic: The eval skill owns task quality, eval discovery, and run
  artifacts; automation should only invoke the skill.
- Expected behavior delta: Weekly eval drain fetches changed eval files, spawns
  bounded per-file consolidation lanes, and applies only coverage-preserving
  simplifications.
- Proof needed: JSON/script tests, skill-system validation, and reviewer
  judgment for eval-quality and skill-contract.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` names `eval:consolidate`, the discovery command, and the per-file lane requirement. |
| `reference_load_precision` | pass | Consolidation detail lives in `references/eval-consolidation.md` and is loaded only for drain mode. |
| `missing_context_rate` | pass | Three bounded reports were produced from ticket, eval file, consolidation guide, and rubric context. |
| `noisy_context_rate` | pass | First-load text stays short; detailed automation/subagent prompt lives in references. |
| `duplicated_instruction_count` | pass | Automation prompt points to the skill-owned guide instead of duplicating full logic. |
| `prompt_size_tokens` | unknown | Not measured. |
| `task_success_rate` | pass | Eval runner tests and discovery tests passed; the new eval row parses. |
| `review_tas_rate` | pass | Final reviewer rerun returned TAS-A across eval-quality, skill-contract, evidence-quality, and integration-readiness. |
| `maintenance_locality` | pass | Changes stay inside `skills/eval` plus TASK-0200. |
| `composition_clarity` | pass | Reports show per-file consolidation can recommend no-op without flattening distinct failure modes. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/eval/eval_task.json`
- Structure evals, when needed: none
- Reviewer receipt: initial TAS-B revise at
  `tickets/TASK-0200/artifacts/review/final-review.md`; final TAS-A pass at
  `tickets/TASK-0200/artifacts/review/final-review-rerun.md`.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  passed; ticket metadata check remains blocked by unrelated TASK-0197 metadata.
- Eval required: yes
- Evidence gaps: none known; ticket metadata validator remains blocked by
  unrelated TASK-0197 metadata.

## Before Behavior

- Eval growth had no owner-local drain.
- A weekly automation could be tempted to own consolidation logic directly.
- The lifecycle could accidentally delay fresh evals until cleanup.

## After Behavior

- `eval:consolidate` owns the drain.
- Automation fetches changed eval files and dispatches per-file consolidation
  lanes.
- Fresh regression evals still land immediately in `eval_task.json`.

## Followups

- Run the new discovery script against the repo.
- Add reviewer receipt after implementation proof.
