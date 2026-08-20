---
skill: automation-advisor
date: 2026-08-20
change_type: behavior
owner: automation-advisor
status: superseded
superseded_by: 2026-08-20-weekly-draft-automation-boundary.md
review_route: reviewer
before_ref: installed-skill-baseline
after_ref: working-tree
reasoning_basis: operator_direction
proof_artifacts:
  - /Users/kenjipcx/.farplane/evals/runs/20260819T213205Z-automation-interval-parent-candidate-vs-installed-final/summary.json
  - skills/automation-advisor/audits/2026-08-20-interval-live-sync-receipt.json
eval_required: yes
---

# Interval Parent Automation Prompt Audit

> Superseded on 2026-08-20 by
> `2026-08-20-weekly-draft-automation-boundary.md`. The active prompts stage
> all Daily knowledge candidates and reserve canonical promotion for Weekly.

## Change

The existing Daily and Weekly cron records still call one `$interval-update`
parent. Their prompts now bind reporting and knowledge phases to the same
window, separate safe local knowledge writes from external side-effect gates,
require the dated report and sibling receipt, and preserve the one Work Pulse
heartbeat and no-ticket-execution boundary.

No new automation, scheduler, prompt compiler, runtime ledger, or persistent
thread was added.

## Eval Comparison

The candidate passed at 0.975 while the installed baseline failed at 0.675.
The case fixture contained one Pulse heartbeat and existing Daily and Weekly
cron records, proving update-in-place rather than creation of a parallel job.

## Deterministic And Live Proof

- `farplane/automations.toml` parses and project-file conventions pass.
- The Codex app updated `farplane-daily-interval` and
  `farplane-weekly-interval` in place. Normalized live prompts match desired
  TOML prompts; both remain `PAUSED` with their existing Daily and Monday
  Weekly schedules, model, reasoning, target, and execution environment.
- Exactly one Farplane Work Pulse heartbeat remains; no new automation exists.

Independent reviewer verdict: `TAS-A`, pass, with no blocking issue or hard
gate failure. The durable live-sync receipt closes the reviewer's nonblocking
evidence caveat about preserved live status.
