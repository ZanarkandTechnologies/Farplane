---
kind: goal-program
ticket_id: TASK-0197
status: active
created_at: 2026-06-13T00:00:00+08:00
---

# TASK-0197 Goal Program

## Goal Mode

- `mode:` `skill_improvement`
- `trigger:` `native_goal`
- `files:` `tickets/TASK-0197/ticket.md`,
  `tickets/TASK-0197/program.md`, `tickets/TASK-0197/progress.md`,
  `experiments/decisions/2026-06-13-skill-maintenance-rewrite-council/context.md`,
  `experiments/decisions/2026-06-13-skill-maintenance-rewrite-council/synthesis.md`,
  `skills/skill-maintenance/SKILL.md`,
  `skills/skill-maintenance/eval_task.json`,
  `skills/skill-maintenance/references/skill-structure-checklist.md`
- `budget:` one focused local Goal execution window; no external spend; use a
  reviewer subagent for final material review when available.
- `time_window:` active native Goal until complete, blocked, or proof requires
  external human input.
- `portfolio_boundary:` none

## Metric Provider

- `provider:` `hybrid`
- `feedback_preset:` `none`
- `signal:` mechanical validation, fixture proof, structure checklist results,
  and reviewer TAS verdict.
- `direction:` `pass/fail`
- `minimum:` all mechanical checks pass; fixture proof recorded; structure
  checklist has no unresolved violation; reviewer returns TAS-A for
  `skill-contract`, `integration-readiness`, and `evidence-quality`, or a
  blocker is recorded.

## Feedback Policy

- `human_feedback:` `none`
- `review_question:` Does the rewritten `skill-maintenance` preserve the
  original safety behavior while improving entrypoint clarity?
- `feedback_file:` none
- `notification:` none

## After Each Turn

1. Read `ticket.md`, this `program.md`, `progress.md` tail, the council
   synthesis, and the current target skill files.
2. Continue from the largest unresolved Done / Proof gap.
3. Change one bounded surface at a time: `SKILL.md`, a skill-local reference, an
   audit, or proof artifact.
4. If `skills/skill-maintenance/eval_task.json` changes, compare changed
   `reference_points` against the relevant checklist/QA guardrail surface and
   record promoted or skipped points.
5. Preserve hard gates inline; do not move required first-load behavior into
   references just to make the skill shorter.
6. Append a structured entry to `progress.md` before ending the turn.
7. Request drift review before completion or any broad rewrite beyond this
   ticket's scope.
8. Continue, stop complete, or report blocked with attempted paths and one
   missing input.

## After Completion

- `on_goal_window_complete:` append completion progress, link proof artifacts,
  and leave follow-up tickets for script-assisted detection or broader skill
  rollout if needed.
- `on_frontier_complete:` none
- `manual_replan_allowed:` yes
- `automatic_replan:` none

## Drift Policy

- `drift_check:` `subagent_required`
- `checkpoints:` turn start, before moving detail out of first load, before
  completion
- `drift_reviewer:` `goal-drift-reviewer`
- `block_on_drift:` yes

## Heartbeat Policy

- `cadence:` none
- `heartbeat_prompt:` none
- `no_op_policy:` not applicable
- `wake_condition:` manual resume only
- `heartbeat_action:` no_op
- `selected_file_policy:` this ticket is the leaf Goal; do not create child
  tickets unless script-assisted detection or broader rollout becomes a
  separate follow-up.

## Batch / Board Policy

- `target_set:` `skills/skill-maintenance` only
- `board_source:` none
- `proceedable_filter:` ready, unblocked, no human gate, local tools available
- `proof_rows:` one row each for mechanical validation, fixture proof,
  structure checklist, and reviewer pass
- `split_when:` script-assisted detection, other skill migrations, or installed
  copy rollout becomes necessary
- `no_op_policy:` log no-op when no useful same-ticket action exists

## Stop Conditions

- `complete_when:` ticket Done / Proof conditions pass and progress links the
  audit, validation output, fixture proof, checklist result, and reviewer pass.
- `blocked_when:` semantic safety cannot be proved with available fixture/eval
  surfaces, reviewer finds unresolved TAS-blocking issues, or required tooling
  is missing.
- `pause_when:` reviewer or drift lane is pending and no safe local proof step
  remains.
- `escalate_when:` implementation would require changing other skills,
  installing live copies as source of truth, or adding new scripts beyond the
  ticket scope.

## Rollout Policy

- `target_set:` none
- `sample_proof:` rewritten `skills/skill-maintenance/SKILL.md`
- `batch_size:` none
- `promotion_rule:` consider broader skill-style rollout only after this ticket
  proves the pattern safe.
- `rollback_or_hold_rule:` hold if compact draft weakens any hard gate or fails
  reviewer/eval/fixture proof.

## Native Goal Prompt

```text
/goal Run tickets/TASK-0197/ticket.md as a native Goal-backed skill-improvement
loop for skills/skill-maintenance.

Task: Rewrite skills/skill-maintenance/SKILL.md as the council-selected Option B:
conservative behavior-delta compression. The rewritten skill must have one
primary behavior-delta signature, bind edited_skill / expected_behavior /
current_behavior / mode / evidence, use readable pseudocode branch routing, and
keep audit as a mode/output path. Preserve hard gates for source ownership,
prototype-before-bulk, registry sync, template-version truth, validator command,
audit-or-skip reason, reinstall when live behavior matters, eval-to-QA sync, and
reviewer routing for material changes. Do not add script-assisted detection or
broaden to other skills in this ticket.

Files: Read tickets/TASK-0197/ticket.md, tickets/TASK-0197/program.md,
tickets/TASK-0197/progress.md,
experiments/decisions/2026-06-13-skill-maintenance-rewrite-council/context.md,
experiments/decisions/2026-06-13-skill-maintenance-rewrite-council/synthesis.md,
skills/skill-maintenance/SKILL.md, skills/skill-maintenance/eval_task.json, and
skills/skill-maintenance/references/skill-structure-checklist.md before editing.

Logging: Before ending each turn, append a compact structured entry to
tickets/TASK-0197/progress.md with trigger, intent, actions, files/artifacts,
metric or feedback sample, drift verdict, next_action, and blockers.

Metric: Hybrid pass/fail from mechanical checks, fixture proof, structure
checklist, and reviewer verdict. Required checks are:
python3 skills/skill-maintenance/scripts/check_skills.py --write;
python3 skills/skill-maintenance/scripts/check_skills.py --template-version 0.2.0;
python3 -m json.tool skills/skill-maintenance/eval_task.json; git diff --check.
Also review existing skill-maintenance eval cases, perform sandbox fixture proof
against skills/skill-maintenance/tests/fixtures/bad-skill-repo, run the skill
structure checklist against the draft, and obtain reviewer pass for
skill-contract, integration-readiness, and evidence-quality.

After each turn: Compare progress against ticket.md and program.md, request
goal-drift-reviewer before completion or before broadening scope, then continue
from the largest unresolved acceptance/evidence/blocker gap. Stop complete only
when Done / Proof conditions and verification are recorded in progress.md, or
report blocked with attempted paths and one missing input.
```
