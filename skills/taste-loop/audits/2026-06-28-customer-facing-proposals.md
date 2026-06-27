---
skill: taste-loop
date: 2026-06-28
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: tickets/TASK-0240/artifacts/telegram-message-TL-EXP-002.txt
after_ref: skills/taste-loop/templates/taste-proposal.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/taste-loop/SKILL.md
  - skills/taste-loop/templates/taste-proposal.md
  - skills/taste-loop/templates/heartbeat-prompt.md
  - skills/taste-loop/eval_task.json
eval_required: yes
---

# Skill Audit

## Change

- Before: Taste Loop required detailed TasteProposal fields, but the
  phone-facing digest could still read like an internal option sheet.
- After: TasteProposal now requires a customer-facing opening: task context,
  bigger problem, proposed solution, why the idea should feel desirable, and
  the exact taste decision being requested.
- Why: Kenji's feedback is highest-signal when he can feel the marketing idea
  as a customer before judging whether the worker should execute it.
- Tradeoff accepted: The first-load skill text gained only compact guardrails;
  the fuller pitch format lives in the TasteProposal template and eval.

## First-Principles Reasoning

- Objective: Convert human taste into useful artifact decisions, not internal
  plan grading.
- Placement logic: Taste Loop owns the proposal artifact shape; Telegram owns
  delivery/readability; optimize-with-human owns the feedback turn gate.
- Expected behavior delta: Future Taste Loop workers sell the idea first, then
  ask for a decision.
- Proof needed: Skill validation plus the next TASK-0240 worker iteration.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` fails internal option sheets and requires customer-facing framing. |
| `reference_load_precision` | pass | `SKILL.md` and heartbeat prompt point workers to `templates/taste-proposal.md`. |
| `missing_context_rate` | pass | The template now names task context, bigger problem, solution, and decision. |
| `noisy_context_rate` | pass | The larger Telegram shape stays in the template instead of expanding first-load prose. |
| `duplicated_instruction_count` | pass | `SKILL.md` has gates; template has output shape; eval has regression points. |
| `prompt_size_tokens` | unknown | `SKILL.md` remains long from prior accumulated contracts; this change does not materially expand it. |
| `task_success_rate` | unknown | Needs a post-change worker output to prove behavior in the wild. |
| `review_tas_rate` | unknown | No independent reviewer was run for this narrow behavior delta. |
| `maintenance_locality` | pass | Future pitch-format edits belong in `templates/taste-proposal.md`. |
| `composition_clarity` | pass | Taste Loop, Telegram, and optimize-with-human responsibilities remain separated. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/taste-loop/eval_task.json`
- Structure evals, when needed: `skills/skill-maintenance/scripts/check_skills.py --write`
- Reviewer receipt: not run; scoped template/eval hardening only.
- Validator: pending command run in this turn.
- Eval required: yes, covered by updated reference points.
- Evidence gaps: next TASK-0240 Telegram iteration should be inspected for the
  customer-facing pitch layer.

## Before Behavior

- A worker could send `Bet`, `Audience`, `Story`, and `Risk` without explaining
  the original task, the customer problem, or why Kenji should care.

## After Behavior

- A worker must open with context, problem, solution, desirability, and a clear
  taste decision before showing options.

## Followups

- Feed Kenji's TASK-0240 correction back into the active worker and inspect the
  next TL-EXP iteration.
