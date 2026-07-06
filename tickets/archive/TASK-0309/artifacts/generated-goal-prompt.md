---
kind: generated-goal-prompt
ticket_id: TASK-0309
created_at: 2026-07-07T01:25:33+08:00
---

# Generated Goal Prompt

Files:

- `tickets/TASK-0309/ticket.md`
- `tickets/TASK-0309/program.md`
- `tickets/TASK-0309/progress.md`
- `farplane/products.md`
- `farplane/automations.toml`
- `skills/pulse-update/SKILL.md`
- `skills/pulse-update/eval_task.json`
- `skills/ticket-opportunity-generator/SKILL.md`
- `skills/ticket-opportunity-generator/eval_task.json`
- `skills/ticket-opportunity-generator/scripts/check_product_loops.py`
- `docs/farplane-framework/pulse-and-interval-loop.md`
- `.gitignore`

Task:

Implement TASK-0309. Move product-local skill/program/progress state into
`farplane/products/<id>/`, update Pulse/generator/product index/docs/validator
and evals to use product-owned paths, and replace the global Pulse desired
state with product-scoped Pulse automation records that pass only
`project_root` and `product`.

Logging:

Append compact observations to `tickets/TASK-0309/progress.md`.

Metric:

Mechanical validators, targeted evals, and reviewer evidence. Do not count
this complete without the checks required by `ticket.md`.

After each turn:

Compare current state to `ticket.md`, write progress, and continue unless
complete or strictly blocked.
