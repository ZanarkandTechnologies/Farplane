---
kind: goal-program
ticket_id: TASK-0309
status: active
created_at: 2026-07-07T01:25:33+08:00
template_id: goal-loop-program
template_version: "0.1.0"
---

# TASK-0309 Goal Program

## Loop

- `shape:` active_goal
- `owner:` codex
- `objective:` implement TASK-0309 exactly as approved in `ticket.md`
- `metric_provider:` hybrid mechanical + eval + review
- `proof_route:` file moves and contract updates, product-loop validator,
  TOML parse, skill registry checks, targeted evals, reviewer lane
- `human_gates:` no live automation activation, no external account mutation,
  no phone call, no publish, no deploy, no spend

## Files

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
- `docs/review/rubrics/ticket-opportunity-quality.md`
- `.gitignore`

## Stop Policy

Stop complete only after:

1. Product-owned loop files exist under `farplane/products/<id>/`.
2. Active references no longer instruct new product loops under
   `.agents/skills/farplane-*/product-loop`.
3. Product-scoped Pulse automation records exist with only `project_root` and
   `product` params.
4. Validators and targeted evals pass.
5. Reviewer evidence is recorded or a blocker is written.

Stop blocked only when the same blocker repeats across three goal turns and no
safe local progress remains.
