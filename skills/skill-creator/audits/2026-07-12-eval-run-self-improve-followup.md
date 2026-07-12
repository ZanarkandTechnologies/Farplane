---
skill: skill-creator
date: 2026-07-12
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/skill-creator/SKILL.md
after_ref: skills/skill-creator/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/skill-creator/evals/evals.json
eval_required: yes
---

# Skill Audit

## Change

- Before: New behavior-sensitive skills needed a behavior proof artifact, but
  the contract did not explicitly require evals to be created and run before
  completion or route artifact-skill optimization to a follow-up self-improve
  packet.
- After: New behavior-sensitive skills must enable evals, create representative
  cases, run them, and record pass/fail/deferred-proof results before readiness.
  Artifact-creation skills must create a self-improve ticket or Goal Packet
  seeded from the baseline eval result when ongoing optimization is warranted,
  or record `no_self_improve_reason`.
- Why: Skill creation should produce a usable baseline and leave iterative
  quality improvement in the self-improve route instead of hiding it in the
  creation ticket or chat.
- Tradeoff accepted: This adds one more first-load proof obligation, but it is
  directly tied to new-skill readiness and avoids a separate baseline gate.

## First-Principles Reasoning

- Objective: Make new skill completion mean the skill was actually exercised by
  evals, and make artifact-skill optimization resumable through self-improve.
- Placement logic: `SKILL.md` owns every-invocation creation gates and output
  contracts; `evals/evals.json` owns the regression case that protects the new
  lifecycle expectation.
- Expected behavior delta: Agents creating behavior-sensitive skills should not
  stop at scaffolding or unrun eval files; they should run the evals and record
  the result, then create or explicitly decline the self-improve follow-up for
  artifact skills.
- Proof needed: Skill registry validation plus a skill-creator eval row that
  asserts evals-created/evals-ran/self-improve-follow-up behavior.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` signature, todo, and output contract name the new proof path. |
| `reference_load_precision` | pass | No new references were added. |
| `missing_context_rate` | pass | The eval-run and self-improve follow-up requirements stay in first load. |
| `noisy_context_rate` | pass | The added text is short and only applies to new behavior-sensitive or artifact-creation skills. |
| `duplicated_instruction_count` | pass | Output contract summarizes todo obligations without adding a second workflow. |
| `prompt_size_tokens` | pass | The skill remains under the line-budget concern threshold. |
| `task_success_rate` | unknown | Requires future skill-creator eval execution. |
| `review_tas_rate` | unknown | No independent reviewer was run for this compact policy update. |
| `maintenance_locality` | pass | Creation readiness is in `SKILL.md`; regression coverage is in `evals/evals.json`. |
| `composition_clarity` | pass | Routes now include `self-improve` and `goal-advisor` for the follow-up packet. |

## Proof Artifacts

- Skill-local evals, when needed:
  `skills/skill-creator/evals/evals.json`
- Structure evals, when needed: not run separately; covered by skill validation.
- Reviewer receipt: self-check only for a compact same-skill contract update.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
- Eval required: yes, regression row added.
- Evidence gaps: The new eval row was added; live eval execution depends on the
  project eval runner availability.

## Before Behavior

- A new skill could be declared ready with an eval artifact or alternate proof,
  without clearly requiring eval creation and execution.
- Artifact-creation skills had no explicit handoff to self-improve after
  baseline readiness.

## After Behavior

- New behavior-sensitive skill readiness requires enabled evals, representative
  cases, recorded eval execution, and pass/fail/deferred-proof status.
- Artifact-creation skills route ongoing quality optimization to a self-improve
  ticket or Goal Packet, unless the creator records `no_self_improve_reason`.

## Followups

- Run the new skill-creator eval row through the project eval harness when the
  next skill-system eval sweep is active.
