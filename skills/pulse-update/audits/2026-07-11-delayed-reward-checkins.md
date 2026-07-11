---
skill: pulse-update
date: 2026-07-11
change_type: behavior
owner: skill-maintenance
status: implemented
review_route: reviewer
reasoning_basis: TASK-0319
eval_required: yes
---

# Pulse Delayed-Reward Audit

## Change

- Before: Work Pulse classified ordinary ticket frontmatter but did not derive
  matured delayed-reward work.
- After: the board classifier projects due, future, and invalid
  `Reward.kpi_rewards[]` rows; a due row makes the original non-terminal ticket
  executable without another ticket or readiness mutation.
- Boundary: claims, blockers, approval, dependencies, review state, and
  terminal state still exclude dispatch. One handoff carries every matured row
  while future and completed rows stay dormant.

## Proof

- `python3 skills/pulse-update/scripts/test_list_pulse_board.py`
- `python3 -m py_compile skills/pulse-update/scripts/list_pulse_board.py skills/pulse-update/scripts/test_list_pulse_board.py`
- Eval cases: `pulse_resumes_due_reward_on_original_ticket` and
  `pulse_handles_multiple_due_reward_rows_together`
