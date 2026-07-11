---
skill: self-improve
date: 2026-07-11
change_type: behavior
owner: skill-maintenance
status: implemented
review_route: reviewer
reasoning_basis: TASK-0319
eval_required: yes
---

# Self Improve Feedback-Timing Audit

## Change

- Before: the skill assumed an in-window measured candidate search.
- After: it classifies `immediate` versus `delayed` before execution. Immediate
  results finish in the current Goal; delayed results reuse the original
  ticket's exact Reward rows and existing Metric Provider, Heartbeat, Stop,
  Rollout, and progress sections.
- Boundary: no future check-in is manufactured for immediate feedback, and no
  second ticket or experiment metadata is created for delayed feedback.
- Refinement: duplicated field-level routing moved to
  `references/workflows.md`; first-load `SKILL.md` shrank from 388 lines to a
  compact route selector under the 250-line review threshold.

## Proof

- Eval cases: `self_improve_immediate_reward_01` and
  `self_improve_delayed_reward_01`
- JSON parse: `jq empty skills/self-improve/eval_task.json`
