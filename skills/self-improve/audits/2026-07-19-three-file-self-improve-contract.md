---
skill: self-improve
date: 2026-07-19
change_type: simplification
owner: self-improve
status: superseded
superseded_by: TASK-0397-goal-program-template
review_route: user-corrected
reasoning_basis: operator clarified the intended skill-local lifecycle
eval_required: yes
---

# Three-File Self-Improve Contract

> Historical record. TASK-0397 superseded target-local lifecycle ownership with
> the ordinary ticket Goal Packet and reusable harden-then-refine program
> template. Nothing below is active runtime policy.

## Before

The active skill mixed skill optimization with campaign history, tickets, Goal
Packets, Reward rows, delayed check-ins, Pulse, and Dogfood coordination.

## After

One target skill owns:

```text
evals/evals.json
self-improve/program.md
self-improve/progress.md
```

Generated `.farplane/evals/runs/<job-id>` artifacts are evidence only. Native
Goal may continue the loop but does not introduce another state model.

## Proof

- `python3 skills/eval/tests/test_run_evals.py`
- `python3 skills/self-improve/scripts/test_init_skill_memory.py`
- `python3 skills/skill-maintenance/scripts/check_skills.py --write`
- focused Farplane UI Eval OS tests and build
