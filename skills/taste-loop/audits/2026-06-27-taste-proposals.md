---
skill: taste-loop
date: 2026-06-27
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/taste-loop/SKILL.md
after_ref: skills/taste-loop/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/taste-loop/templates/taste-proposal.md
  - skills/taste-loop/eval_task.json
  - farplane/automations.md
eval_required: yes
---

# Skill Audit

## Change

- Before: Taste Loop treated thin concept cards as sufficient first-stage
  planning artifacts for product workflows.
- After: Taste Loop defaults to `TasteProposal` planning artifacts with
  audience, taste insight, artifact shape, core angle, execution beats, win
  reasons, cringe risks, references or taste pack, feedback question, and next
  step.
- Why: Kenji cannot give high-signal taste feedback when proposals contain only
  titles, hooks, and shallow angles.
- Tradeoff accepted: Planning artifacts become denser, but they should still be
  capped at one best bet or three compact proposals for comparison.

## First-Principles Reasoning

- Objective: Improve the human feedback loop by making planning proposals
  detailed enough to judge before execution.
- Placement logic: Taste Loop owns worker selection and planning artifact shape,
  while `optimize-with-human` owns feedback request sufficiency.
- Expected behavior delta: Future workers generate proposal-level planning
  artifacts instead of hook-only choices for non-trivial workflows.
- Proof needed: Skill-system validator, eval reference update, automation prompt
  source update, and live automation prompt sync.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` and heartbeat prompt define `TasteProposal` and worker requirements. |
| `reference_load_precision` | pass | `templates/taste-proposal.md` is linked as the proposal/digest shape. |
| `missing_context_rate` | pass | Worker prompt requirements are first-load, not hidden only in the template. |
| `noisy_context_rate` | pass | Detailed reusable shape is in a template; first-load keeps the required fields. |
| `duplicated_instruction_count` | pass | `SKILL.md` names the hard gate; template owns reusable formatting. |
| `prompt_size_tokens` | pass | Existing long skill remains below hard failure threshold for this repo. |
| `task_success_rate` | unknown | No post-change Taste Loop worker has generated a proposal yet. |
| `review_tas_rate` | unknown | No independent reviewer receipt was requested for this focused update. |
| `maintenance_locality` | pass | Future planning artifact shape changes belong in Taste Loop template plus skill gates. |
| `composition_clarity` | pass | `optimize-with-human` now owns the matching feedback sufficiency gate. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/taste-loop/eval_task.json`.
- Structure evals, when needed: `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Reviewer receipt: skipped; direct operator failure with focused owner-local
  hardening.
- Validator: `check_skills.py --write`.
- Eval required: yes, reference points updated; scored eval not run in this turn.
- Evidence gaps: Next Taste Loop run should be inspected for actual
  `TasteProposal` quality.

## Before Behavior

- A worker could send three choices that were mostly title, hook, and angle.

## After Behavior

- A worker should send one to three proposal-level planning artifacts and a
  phone-readable digest before asking Kenji to choose.

## Followups

- Capture the next Taste Loop worker output as evidence that the proposal
  template materially improves feedback quality.
