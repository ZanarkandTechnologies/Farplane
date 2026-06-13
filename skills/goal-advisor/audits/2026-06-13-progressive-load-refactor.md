---
skill: goal-advisor
date: 2026-06-13
change_type: structure
owner: skill-maintenance
status: pass
review_route: deliberative_advice
before_ref: skills/goal-advisor/SKILL.md
after_ref: skills/goal-advisor/SKILL.md; skills/goal-advisor/references/prompt-templates.md; skills/goal-advisor/references/goal-shapes.md; skills/goal-advisor/references/goal-algebra.md; docs/skills/best-practices.md
reasoning_basis: deliberative_advice
proof_artifacts: []
eval_required: no
---

# Progressive Load Refactor Audit

## Change

- Before: `goal-advisor/SKILL.md` loaded architecture, shape detail, algebra,
  prompt templates, and rare-path recipes together on first load.
- After: `SKILL.md` carries the execution compiler contract, checklist, gates,
  output contract, and reference routing; prompt templates, shape detail, and
  algebra load only after the branch is selected.
- Why: Loading every important detail early increases context rot and can force
  compaction before active task state is stable.
- Tradeoff accepted: Prompt templates are one extra reference read when emitting
  a prompt, in exchange for a smaller normal first-load surface.

## First-Principles Reasoning

- Objective: Preserve Goal Advisor correctness while reducing first-load token
  cost and compaction risk.
- Placement logic: A rule stays first-load only when deferring it is riskier
  than loading it early: `defer_loading_risk > context_rot_risk +
  compaction_loss_risk`.
- Expected behavior delta: Architecture-only uses no longer preload full prompt
  templates; prompt-emission branches explicitly load the template reference.
- Proof needed: line count reduction, link/registry validation, and JSON parse
  for the existing eval task.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` still includes trigger, signature, state surfaces, gates, todo path, output contract, and gotchas. |
| `reference_load_precision` | pass | `SKILL.md` names the exact read condition for prompt templates, goal shapes, algebra, portfolio, and examples. |
| `missing_context_rate` | pass | Every prompt-emission todo explicitly loads `references/prompt-templates.md` first. |
| `noisy_context_rate` | pass | Long templates and algebra were moved out of first load. |
| `duplicated_instruction_count` | pass | First load keeps summaries; references own full bodies. |
| `prompt_size_tokens` | pass | `SKILL.md` reduced from about 500 lines to 250 lines. |
| `task_success_rate` | unknown | Needs a live Goal Advisor use after refactor or a focused eval run. |
| `review_tas_rate` | unknown | No independent reviewer receipt in this pass. |
| `maintenance_locality` | pass | Shared progressive-load rule is in `docs/skills/best-practices.md`; skill-specific templates remain under `goal-advisor/references`. |
| `composition_clarity` | pass | Signature and output contract remain first-load; composition detail is in `goal-algebra.md`. |

## Proof Artifacts

- Validator:
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write` passed.
  - `git diff --check` passed.
  - `python3 -m json.tool skills/goal-advisor/eval_task.json >/dev/null` passed.
- Reviewer receipt:
  - Initial reviewer pass found that `skill-maintenance/SKILL.md` violated its
    own structure checklist through duplicated workflow prose and 338-line
    first-load bloat.
  - Cleanup removed the duplicate workflow section and compressed repeated
    outcome/gotcha prose.
  - Reviewer rerun passed `noisy_context_rate`, `duplicated_instruction_count`,
    and `prompt_size_tokens`; `skill-maintenance/SKILL.md` is now 247 lines.
- Eval required: no new behavior eval required for this structure-only split.
- Evidence gaps: first live native Goal prompt should confirm the reference
  routing feels natural.

## Before Behavior

Every Goal Advisor invocation loaded full prompt templates and deeper algebra,
even when the user only needed an architecture recommendation or branch choice.

## After Behavior

Goal Advisor first load decides the branch and names the exact reference to
load next. Prompt templates are loaded only for prompt emission, shape detail
only for complex shape decisions, and algebra only for composition or migration
questions.

## Followups

- Consider splitting `references/goal-portfolio.md` if portfolio work becomes
  common enough that its 400+ line reference causes branch-local bloat.
