---
skill: ticket-opportunity-generator
date: 2026-07-05
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: local untracked skill before TASK-0294 implementation
after_ref: skills/ticket-opportunity-generator/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/ticket-opportunity-generator/eval_task.json
  - python3 skills/skill-maintenance/scripts/check_skills.py --write
eval_required: yes
---

# Skill Audit

## Change

- Before: Specific local tickets could pass if they had metadata and a concrete
  artifact, even when the claim was boring, self-referential, or review/admin
  shaped.
- After: Ticket generation requires trend or leverage premises when useful,
  product-lane scan, big claim, audience/operator tension, surprise factor,
  baseline/contrast, dedupe status, artifact level, and product-backed reward.
- Why: Pulse workers were spending cycles on valid-looking artifacts that did
  not create proof, content, or product value Kenji wanted to review.
- Tradeoff accepted: `SKILL.md` remains long because the normal path needs
  first-load gates for ticket quality, reward admission, and artifact levels.

## First-Principles Reasoning

- Objective: Make empty-board planning produce bold executable bets, not
  planner tickets or paperwork.
- Placement logic: The manager-side idea compiler owns premise quality before
  Pulse writes tickets or spawns workers.
- Expected behavior delta: Mid-but-valid tickets are rejected or strengthened;
  Feed Scout and leverage signals become ticket premises; every spec names a
  reviewable product artifact.
- Proof needed: JSON eval syntax, skill registry validation, and reviewer
  judgment against TASK-0294.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Signature, gates, todos, schemas, and examples are in `SKILL.md`. |
| `reference_load_precision` | pass | No conditional references were added. |
| `missing_context_rate` | pass | Required reward, artifact, dedupe, and baseline gates are first-load. |
| `noisy_context_rate` | unknown | File is over 400 lines; reviewer should judge whether examples should move. |
| `duplicated_instruction_count` | pass | Repeated gates are used in signature, todo, and render schema for enforcement. |
| `prompt_size_tokens` | unknown | 607 lines after edit; first-load bloat is the main residual risk. |
| `task_success_rate` | unknown | Behavioral evals added but not run by an automated judge in this pass. |
| `review_tas_rate` | unknown | Pending completion review. |
| `maintenance_locality` | pass | Behavior lives in the generator skill and its eval file. |
| `composition_clarity` | pass | Inputs, outputs, routes, fails, and ticket spec fields are explicit. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/ticket-opportunity-generator/eval_task.json`.
- Structure evals, when needed: `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Reviewer receipt: pending.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write` passed.
- Eval required: yes; cases added for boring-valid, Feed Scout, leverage, and artifact-level failures.
- Evidence gaps: No live Pulse run is part of this ticket.

## Before Behavior

- A ticket like "prepare evidence-fidelity feedback capture note" could look
  valid if it was local, specific, and safe.

## After Behavior

- That ticket is rejected unless it becomes a stronger proof/content artifact
  with claim, contrast, artifact level, dedupe status, and product reward.

## Followups

- Consider moving long examples to a reference if reviewer flags first-load
  size as the highest risk.
