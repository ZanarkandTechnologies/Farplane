---
id: TASK-0214
kind: goal-program
status: approved
created_at: 2026-06-24
updated_at: 2026-06-24
---

# TASK-0214 Program

## Goal

Flatten the active Farplane automation model from Pulse + Steer scheduler into
Pulse + Daily Interval + Weekly Interval while preserving the reusable
report-before-plan interval workflow.

## Trigger

User explicitly requested `impl-plan`, `goal-advisor`, and native Goal
execution for this migration.

## Files

- `tickets/TASK-0214/ticket.md`
- `tickets/TASK-0214/program.md`
- `tickets/TASK-0214/progress.md`
- `farplane/automations.md`
- `farplane/steer.config.toml`
- `skills/steer-update/SKILL.md`
- `skills/steer-update/references/interval-update.md`
- `skills/pulse-update/SKILL.md`
- `skills/automation-advisor/SKILL.md`
- `skills/deep-init-project/references/AUTOMATION_TEMPLATE.md`
- `skills/deep-init-project/references/STEER_CONFIG_TEMPLATE.toml`
- `docs/specs/steer-pulse-automation.md`
- `docs/farplane-framework/lifecycle.md`
- `docs/farplane-framework/deep-init-critical-path.md`
- `docs/MEMORY.md`
- `docs/LESSONS.md`

## Budget

- Time: current execution turn.
- Compute: local shell and validators.
- Subagents: none required unless a validator/review blocker appears.
- Spend/deploy/publish/destructive actions: forbidden.

## Metric / Proof Provider

`mechanical`: validator success, generated registry consistency, and targeted
text searches proving the active story no longer depends on Steer as a hidden
scheduler.

## Drift Policy

Inline drift check each pass:

```text
compare(ticket.md + program.md, current diff)
  -> continue if Pulse/Daily/Weekly model is being implemented
  -> revise if edits recreate Steer scheduler or add hidden compiler/runtime
  -> block if live automation mutation becomes necessary but unsafe
```

## Proof Route

Self-run mechanical checks are acceptable. No UI/user-visible proof required.
Material judgment claims should be limited to explicit local evidence.

## Final Evidence

Final response must name changed surfaces, verification commands, and any
remaining risks. No screenshot required.

## Native Goal Prompt

```text
/goal Run the following files as one Goal Packet.
Files:
- tickets/TASK-0214/ticket.md
- tickets/TASK-0214/program.md
- tickets/TASK-0214/progress.md
- farplane/automations.md
- farplane/steer.config.toml
- skills/steer-update/SKILL.md
- skills/steer-update/references/interval-update.md
- skills/pulse-update/SKILL.md
- skills/automation-advisor/SKILL.md
- skills/deep-init-project/references/AUTOMATION_TEMPLATE.md
- skills/deep-init-project/references/STEER_CONFIG_TEMPLATE.toml
- docs/specs/steer-pulse-automation.md
- docs/farplane-framework/lifecycle.md
- docs/farplane-framework/deep-init-critical-path.md
- docs/MEMORY.md
- docs/LESSONS.md

Task: Complete TASK-0214. Preserve the ticket scope and replace the active
Steer-scheduler automation model with Pulse + Daily Interval + Weekly Interval.
Keep interval planning as a direct report-before-plan workflow. Do not mutate
live Codex automation records, push, deploy, publish, spend, or perform
destructive cleanup.

Logging: Before ending each turn, append a compact structured entry to
tickets/TASK-0214/progress.md with changed files, verification, drift verdict,
and next action or completion status.

Metric: Satisfy the Done / Proof checks in ticket.md and this program. Use
mechanical validators and targeted text search; do not self-certify claims that
the files do not support.

After each turn: Compare progress against ticket.md and program.md. Continue
within this execution window if useful. Stop complete only when active docs and
skills reflect the flat model, generated registries are synced, and validators
pass; otherwise stop blocked with the exact missing input or failing command.

Approval: approved by explicit operator request to run after impl-plan and
goal-advisor.
```

## Approval

Approved for current-turn execution.
