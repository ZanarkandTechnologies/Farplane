---
skill: optimize-with-human
date: 2026-06-27
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/optimize-with-human/SKILL.md
after_ref: skills/optimize-with-human/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/optimize-with-human/qa_checklist.md
  - skills/optimize-with-human/eval_task.json
eval_required: yes
---

# Skill Audit

## Change

- Before: `optimize-with-human` allowed planning feedback on compact concept
  cards without stating the minimum detail needed for non-trivial artifacts.
- After: it requires proposal-level planning detail for non-trivial artifacts
  and treats hook-only requests as valid only for hook-sized work.
- Why: A short Telegram question is useful only when the underlying proposal is
  rich enough to judge.
- Tradeoff accepted: Feedback requests must carry more context, but they remain
  decision-shaped.

## First-Principles Reasoning

- Objective: Prevent human-feedback loops from optimizing against underspecified
  artifacts.
- Placement logic: `optimize-with-human` owns feedback request quality and exit
  gates; Taste Loop owns the planning artifact template.
- Expected behavior delta: Workers should not pause for feedback until the
  planning artifact has enough detail for a real verdict.
- Proof needed: QA checklist guardrail plus eval reference update.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` lists minimum TasteProposal fields and hook-only exception. |
| `reference_load_precision` | pass | No new references are required by this change. |
| `missing_context_rate` | pass | Feedback sufficiency gate is first-load and checklist-backed. |
| `noisy_context_rate` | pass | No long examples were added to first-load. |
| `duplicated_instruction_count` | pass | `SKILL.md` owns behavior; checklist owns QA verdict wording. |
| `prompt_size_tokens` | pass | Skill remains under the rough 250-line budget. |
| `task_success_rate` | unknown | No post-change optimization worker has been observed yet. |
| `review_tas_rate` | unknown | No independent reviewer receipt was requested for this focused update. |
| `maintenance_locality` | pass | Future feedback sufficiency edits belong in this skill/checklist. |
| `composition_clarity` | pass | Taste Loop and Telegram responsibilities remain distinct. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/optimize-with-human/eval_task.json`.
- Structure evals, when needed: `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Reviewer receipt: skipped; focused same-scope hardening.
- Validator: `check_skills.py --write`.
- Eval required: yes, reference points updated; scored eval not run in this turn.
- Evidence gaps: Next human-feedback worker should be inspected for proposal
  sufficiency before Telegram send.

## Before Behavior

- Planning feedback could ask Kenji to choose from titles and hooks.

## After Behavior

- Planning feedback must expose enough proposal detail to support a meaningful
  keep/revise/reject decision.

## Followups

- If future workers still send shallow summaries, harden the caller prompt or
  add an agent-behavior test around `optimize-with-human`.
