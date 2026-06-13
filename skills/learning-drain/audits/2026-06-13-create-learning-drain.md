---
skill: learning-drain
date: 2026-06-13
change_type: create
owner: skill-creator
status: pass
review_route: advise
before_ref: docs/TROUBLES.md and docs/LESSONS.md weekly automation idea
after_ref: skills/learning-drain/SKILL.md
reasoning_basis: operator request plus local skill-system standards
proof_artifacts:
  - skills/learning-drain/SKILL.md
  - skills/learning-drain/eval_task.json
  - skills/learning-drain/references/automation-prompt.md
  - skills/learning-drain/references/processed-state.md
eval_required: yes
---

# Skill Audit

## Change

- Before: The weekly drain existed as an automation idea that would read
  `docs/TROUBLES.md` and `docs/LESSONS.md` and call `optimize-harness`.
- After: `learning-drain` owns the reusable drain behavior, eval cases, cap,
  pairing rules, processed-state contract, and automation prompt wrapper.
- Why: Automation should be a scheduler pointer. The reusable behavior needs a
  skill package so it can be tested, invoked manually, and reused across
  projects.
- Tradeoff accepted: The skill is workflow-only for now; it defines the drain
  contract and eval surface before adding a deterministic script runner.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` includes trigger, signature, drain policy, todo path, output, and gotchas. |
| `reference_load_precision` | pass | Automation prompt and processed-state details live in references. |
| `missing_context_rate` | pass | First-load path names docs, state paths, caps, and routes. |
| `noisy_context_rate` | pass | Long JSONL details are in a reference and short output shape stays first-load. |
| `duplicated_instruction_count` | pass | Automation prompt explicitly points back to the skill. |
| `prompt_size_tokens` | pass | Skill body remains focused and references carry optional detail. |
| `task_success_rate` | unknown | Eval tasks added but not run in this pass. |
| `review_tas_rate` | unknown | No reviewer receipt in this pass. |
| `maintenance_locality` | pass | Drain behavior has one owning package. |
| `composition_clarity` | pass | Routes to optimize-harness, eval, skill-maintenance, gap-analysis, and summary. |

## Proof

- Run `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Run or review `skills/learning-drain/eval_task.json` before claiming
  behavioral readiness.

## Followups

- Add a deterministic helper script if manual drains become frequent enough to
  need machine execution instead of skill-guided execution.
- Update the live weekly automation to call this skill with `mode=automation`
  and `cap=5`.
