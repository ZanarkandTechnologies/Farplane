---
date: 2026-06-12
change: initial-goal-advisor
skill: goal-advisor
---

# Initial Goal Advisor Audit

## Reason

Farplane needed a higher-order entrypoint for deciding how to use native Codex
Goals with tickets, `program.md`, `progress.md`, drift checks, human feedback,
heartbeats, and rollout patterns.

## Before

Goal prompt crafting was separate from the larger decision of whether to use
active Goal, heartbeat, feedback loop, rollout, or direct work.

## After

`goal-advisor` owns Goal architecture selection and native `/goal` prompt
compilation from the same Goal Packet.

## Proof

- `docs/specs/goal-loop-contract.md` defines the canonical model.
- `skills/goal-advisor/SKILL.md` follows the template `0.2.0` structure.
- `skills/goal-advisor/eval_task.json` adds two focused behavior cases.
