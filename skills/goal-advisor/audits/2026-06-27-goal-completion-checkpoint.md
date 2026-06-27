---
skill: goal-advisor
date: 2026-06-27
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/goal-advisor/SKILL.md; skills/goal-advisor/references/prompt-templates.md; skills/goal-advisor/qa_checklist.md
after_ref: skills/goal-advisor/SKILL.md; skills/goal-advisor/references/prompt-templates.md; skills/goal-advisor/qa_checklist.md; skills/goal-advisor/eval_task.json
reasoning_basis: first_principles
proof_artifacts: []
eval_required: yes
---

# Goal Advisor Completion Checkpoint Audit

## Change

- Before: Goal prompts required delegated proof and critical-path evidence, but
  the final QA evidence review and completion review checkpoint could still be
  assumed to happen through legacy Stop-hook behavior.
- After: Goal prompts must make the final checkpoint part of the listed ticket
  and Goal program: run or request QA evidence review and completion review,
  write links back to `ticket.md`, `progress.md`, and `artifacts/`, then block
  or revise if the checkpoint is missing.
- Why: Native Goal owns continuation now; ticket-local proof must be enough to
  prevent premature done claims without relying on Stop-hook reentry.
- Tradeoff accepted: Slightly stronger Goal prompt obligations in exchange for
  avoiding hidden orchestration.

## First-Principles Reasoning

- Objective: Make material Goal-backed implementation prove the ticket before
  completion.
- Placement logic: `goal-advisor` compiles native Goal prompts, so it is the
  right surface for final checkpoint language.
- Expected behavior delta: Generated Goal prompts stop only after evidence,
  review receipts, residual risk, and ticket/progress writeback are present.
- Proof needed: Skill validator plus eval coverage for final checkpoint
  reference points.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Checklist and Goal Contract now name final checkpoint. |
| `reference_load_precision` | pass | Prompt wording lives in `references/prompt-templates.md`. |
| `missing_context_rate` | pass | Goal prompts require file lists and writeback. |
| `noisy_context_rate` | pass | No full Stop-hook procedure copied into the skill. |
| `duplicated_instruction_count` | pass | Ticket/program templates own flexible body details. |
| `prompt_size_tokens` | pass | Added compact checkpoint lines only. |
| `task_success_rate` | unknown | Needs future live Goal run evidence. |
| `review_tas_rate` | unknown | Needs reviewer sample after next material Goal. |
| `maintenance_locality` | pass | Change stays in goal-advisor plus ticket templates. |
| `composition_clarity` | pass | QA/review lanes remain delegated proof surfaces. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/goal-advisor/eval_task.json`
- Structure evals, when needed: pending validator run
- Reviewer receipt: none
- Validator: pending
- Eval required: yes
- Evidence gaps: no live Goal sample yet

## Before Behavior

- Material Goal prompts could delegate proof but still leave final missing-proof
  detection to Stop-hook folklore.

## After Behavior

- Material Goal prompts require QA evidence review and completion review before
  `stop_complete`, with durable ticket/progress/artifact writeback.

## Followups

- Capture the next material Goal run as proof that the final checkpoint is
  followed without Stop-hook orchestration.
