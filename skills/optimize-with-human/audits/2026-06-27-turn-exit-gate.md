---
title: "Optimize With Human Turn Exit Gate"
owner: optimize-with-human
status: complete
created_at: 2026-06-27
---

# Optimize With Human Turn Exit Gate

## Behavior Delta

Before: a worker could process Kenji's feedback, make a change, and stop
without sending the next Telegram feedback request or blocker.

After: every stop must satisfy a turn exit gate: waiting turns send Telegram or
fallback/blocker, non-terminal feedback turns send the next artifact request or
blocker, and terminal turns record the terminal reason.

## Evidence

- `skills/optimize-with-human/SKILL.md` now includes
  `turn_exit_gate_satisfied`.
- `skills/optimize-with-human/qa_checklist.md` checks reply path, phone-friendly
  artifact surfaces, Telegram send/fallback, post-feedback continuation, and
  progress logging.
- `skills/optimize-with-human/eval_task.json` includes the new exit gate and
  terminal reason reference points.

## Verdict

pass: source contract hardened. Runtime proof should come from the next worker
thread after it receives non-terminal feedback.
