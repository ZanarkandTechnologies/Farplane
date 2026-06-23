---
title: "Deep Init Critical Path"
status: active
owner: farplane-framework
created_at: 2026-06-23
updated_at: 2026-06-23
framework_template_version: "0.2.0"
tags:
  - farplane
  - deep-init
  - project-setup
  - automations
refs:
  - skills/deep-init-project/SKILL.md
  - skills/deep-init-project/scripts/bootstrap.sh
  - skills/horizon-advisor/SKILL.md
  - skills/goal-advisor/SKILL.md
  - skills/automation-advisor/SKILL.md
  - docs/specs/steer-pulse-automation.md
  - docs/farplane-framework/README.md
  - docs/farplane-framework/project-files.md
---

# Deep Init Critical Path

This document is the full story for setting up a new Farplane project. It is
the reader-facing explanation of what `deep-init-project` does, what it does
not do, and how the project becomes an autonomous Steer/Pulse project.

```text
deep_init_project(...)
  -> project substrate
   + project operating docs
   + ticket system
   + QA/proof surfaces
   + steer config and scheduler state
   + PM UI thread grouping manifest
   + starter planning ticket
   + horizon-advisor goal-shaping handoff
   + goal-advisor execution handoff?
   + optional automation-advisor activation handoff
```

Bootstrap creates the filesystem substrate. Project strategy is shaped through
`horizon-advisor`, execution frontiers are compiled through `goal-advisor`, and
live Codex automation activation is a separate step owned by
`automation-advisor`.

## Critical Path

### 1. Bind the Init Target

Owner: `deep-init-project`

Inputs:

- project root
- greenfield or brownfield state
- whether code/app scaffolding is requested
- `init_mode`: `substrate` or `full`
- overwrite policy

Output:

- selected target root
- selected project profile
- selected stack profile or no-code-scaffold decision
- first missing human-owned decision, only when it blocks setup

Guardrails:

- Read existing repo files before writing.
- Preserve existing files unless `force` or explicit overwrite intent is
  present.
- Stop for credentials, billing, cloud project creation, destructive actions,
  or materially branching product decisions.

### 2. Create the Project Substrate

Owner: `deep-init-project`

Files created or preserved:

```text
AGENTS.md
PROJECT_RULES.md
ARCHITECTURE.md
README.md
docs/bootstrap-brief.md
docs/prd.md
docs/specs/README.md
docs/HISTORY.md
docs/MEMORY.md
docs/TASTE.md
docs/TROUBLES.md
docs/LESSONS.md
qa/README.md
qa/AGENTS.md
qa/cookbook/*
tickets/README.md
tickets/templates/ticket.md
tickets/TASK-0001/ticket.md
```

What this means:

- The repo has one local operating policy.
- The repo has a visible ticket workflow.
- The repo has durable memory and learning ledgers.
- The repo has QA/proof entrypoints.
- The first project discovery handoff exists as `TASK-0001`.

Guardrails:

- Do not run product discovery inside bootstrap unless explicitly requested.
- Do not convert the whole backlog into tickets.
- Do not claim the project is initialized only because files exist.

### 3. Create Farplane Framework Config

Owner: `deep-init-project`

Tracked config:

```text
farplane/README.md
farplane/manifest.json
farplane/harness.md
farplane/goals.md
farplane/automations.md
farplane/steer.config.toml
farplane/bindings.md
farplane/evals.md
farplane/pm.json
```

Ignored runtime state:

```text
.farplane/README.md
.farplane/state/run-ledger.json
.farplane/state/steer-scheduler.json
.farplane/reports/
.farplane/evals/runs/
.farplane/logs/
```

Key contracts:

- `farplane/manifest.json` records the project spec version and standard
  tracked/ignored files.
- `farplane/goals.md` is project strategy context.
- `farplane/automations.md` is the human-reviewable source for the exact Pulse
  and Steer prompts copied into Codex automations.
- `farplane/steer.config.toml` is an optional compact schedule helper for Steer
  jobs when a project wants machine-readable job rows.
- `.farplane/state/steer-scheduler.json` stores mutable `next_due_at`,
  `last_run_at`, `last_report`, and job status.
- `farplane/pm.json` is UI glue that groups PM-visible chat and automation
  thread IDs under one persistent employee agent.

Guardrails:

- Do not recreate `farplane/automations.json` or a hidden automation compiler.
- Do not put `last_run_at`, `next_due_at`, or automation IDs in
  `steer.config.toml`.
- Do not duplicate workflow inputs, outputs, drift checks, report paths, or
  gates in `steer.config.toml`; put those in the job prompt or owning skill.

### 4. Run Readiness Audit

Owner: `deep-init-project`

Audit:

- `docs/bootstrap-brief.md`
- `farplane/harness.md`
- `farplane/goals.md`
- `farplane/steer.config.toml`
- `farplane/bindings.md`
- `farplane/pm.json`
- `PROJECT_RULES.md`
- QA surfaces

Results:

```text
substrate_complete
needs_goal_intake
needs_runtime_setup
needs_automation_setup
project_initialized
```

Rules:

- `substrate_complete` means the filesystem base exists.
- `project_initialized` requires grounded goals and enough runtime/proof
  context to start useful work.
- `needs_goal_intake` means `farplane/goals.md` is missing, placeholder, stale,
  or not grounded in the operator's current intent.
- `needs_automation_setup` means the project has not yet activated live
  Steer/Pulse automations.

Guardrails:

- In `substrate` mode, report missing goal/setup questions as next handoff.
- In `full` mode, ask the first missing project-goals question before claiming
  initialization.
- Do not use `goal-advisor` until the current milestone is concrete enough for
  a ticket-backed Goal Packet.

### 5. Shape Project Goals

Owner: `horizon-advisor`

Use this phase when `farplane/goals.md` is missing, placeholder, stale, or not
grounded in the operator's current intent.

Inputs:

- operator intent
- `farplane/harness.md`
- existing `farplane/goals.md`
- tickets and project evidence
- memory, lessons, and troubles when relevant

Output:

```text
horizon_advice(...)
  -> goals_delta
   + value_function
   + kpi_tree
   + project_goal_map
   + current_milestone
   + goal_advisor_handoff?
```

What this means:

- The project has a North Star or learning objective.
- The project has a value function and anti-metrics.
- The project has a current milestone small enough to become executable.
- Strategy lives in `farplane/goals.md`, not chat.

Guardrails:

- Do not turn every goal into a ticket.
- Do not invent fake metrics.
- Do not compile native Goal prompts here; hand selected frontiers to
  `goal-advisor`.

### 6. Compile the First Executable Frontier

Owner: `goal-advisor`

Use this phase once `horizon-advisor` has made the current milestone concrete
enough to execute.

Output:

```text
goal_advisor(files=[farplane/goals.md, ticket.md?, program.md?, progress.md?], ...)
  -> ticket.md
   + program.md
   + progress.md
   + native_goal_prompt?
   + heartbeat_prompt?
   + next_action
```

What this means:

- The first frontier is turned into a ticket-backed Goal Packet or a direct
  route.
- Execution state has durable files.
- The future Pulse/Steer loops have a real project direction to follow.

Guardrails:

- Do not run material Goal work without files.
- Do not use Goal mode as a substitute for missing project strategy.
- Do not self-certify QA/review for material work.

### 7. Optional Code Scaffold

Owner: `deep-init-project`

Possible stack profiles:

- Convex + Next.js + Clerk
- plain Next.js + shadcn
- Convex in an existing app
- React-only
- no code scaffold

Outputs:

- app scaffold when requested
- canonical app-only run path in `PROJECT_RULES.md`
- canonical QA/evidence run path in `PROJECT_RULES.md` and `qa/`
- required services, ports, and environment assumptions

Guardrails:

- Stop for interactive setup, credentials, cloud setup, billing, deploys, or
  destructive actions.
- Use current official docs when stack commands may be stale.
- Do not confuse code scaffold completion with project initialization.

### 8. Starter Planning Handoff

Owner: `deep-init-project`

Default next path:

```text
brainstorm -> deep-interview -> horizon-advisor -> goal-advisor
prd -> spec-to-ticket -> impl-plan -> goal-advisor
```

Artifacts:

- `tickets/TASK-0001/ticket.md` for the initial PRD or discovery handoff
- `docs/prd.md` as a draft placeholder unless PRD work is requested now

Guardrails:

- Do not write a full PRD during init unless explicitly requested.
- Do not run a native Goal before a ticket-backed Goal Packet exists.

### 9. Live Automation Activation

Owner: `automation-advisor`

Activation is not automatic during bootstrap. It happens only when the operator
asks to activate live automations.

```text
automation_advisor(activate=true, project_refs)
  -> pulse_thread_id
   + steer_thread_id
   + pulse_automation_id
   + steer_automation_id
   + farplane/pm.json thread-grouping delta
```

Activation steps:

1. Inspect existing Codex automations and project threads.
2. Reuse or update matching Pulse/Steer loops instead of creating duplicates.
3. Create or reuse a dedicated `Project Pulse` thread.
4. Create or reuse a dedicated `Project Steer` thread.
5. Attach Pulse automation to the Pulse thread at the fast idle cadence.
6. Attach Steer automation to the Steer thread or project workspace at the
   minimum planning cadence.
7. Append PM-visible thread IDs to `farplane/pm.json` so the UI renders them
   under the same persistent employee.

`farplane/pm.json` groups threads for the UI:

```json
{
  "version": 1,
  "name": "Project PM",
  "role": "founder_operator",
  "threads": {
    "chats": ["..."],
    "automations": ["..."]
  }
}
```

Guardrails:

- Create exactly two live loops: Pulse and Steer.
- Do not create separate daily, weekly, quarterly, yearly, strategy-review, or
  ticket-drainer threads; daily and weekly are Steer interval jobs.
- Do not activate autonomous loops when goals are placeholder or stale.
- If Codex thread/automation tools are unavailable, write prepared prompts and
  report `needs_automation_setup`.
- Do not store automation runtime state in `farplane/pm.json`; it is only UI
  grouping glue for thread IDs.
- When Pulse or Steer creates persistent ticket/worker threads that should
  appear under the same employee, append those chat thread IDs to
  `threads.chats`.

## File Plan

| Surface | Created By | Updated By | Purpose |
| --- | --- | --- | --- |
| `AGENTS.md` | `deep-init-project` | operator / project policy work | local operating policy |
| `PROJECT_RULES.md` | `deep-init-project` | runtime/setup work | commands, services, QA paths |
| `ARCHITECTURE.md` | `deep-init-project` | architecture/docs work | system map |
| `docs/bootstrap-brief.md` | `deep-init-project` | deep interview / setup | setup decisions and readiness |
| `farplane/manifest.json` | `deep-init-project` | framework migrations | expected tracked/ignored paths |
| `farplane/harness.md` | `deep-init-project` / `harness-creator` | harness planning | mission, values, systems |
| `farplane/goals.md` | `deep-init-project` / `horizon-advisor` | strategy work | goals, KPIs, milestone |
| `farplane/automations.md` | `deep-init-project` / `automation-advisor` | operator / `automation-advisor` | reviewed Pulse and Steer prompt source |
| `farplane/steer.config.toml` | `deep-init-project` | operator / `automation-advisor` | Steer job prompts and cadence |
| `.farplane/state/steer-scheduler.json` | `deep-init-project` / Steer | Steer runtime | next due and last run state |
| `farplane/pm.json` | `deep-init-project` | `automation-advisor` / PM-visible threads | UI grouping for persistent chat and automation threads |
| `tickets/TASK-0001/ticket.md` | `deep-init-project` | planning flow | starter PRD/discovery handoff |
| `qa/` | `deep-init-project` | QA work | reusable proof paths |

## End States

### Substrate Complete

The repo has the files, tickets, QA surface, and Farplane config skeleton. It
may still need goals, runtime commands, and automation activation.

### Project Initialized

The repo has grounded goals, usable runtime/proof paths, a starter ticket, and
clear next planning or execution handoff. For autonomous projects, this usually
means `horizon-advisor` has shaped goals and `goal-advisor` has compiled the
first executable frontier.

### Automation Activated

The repo has exactly two live recurring automation loops, Pulse and Steer.
Pulse handles frequent bounded action. Steer handles scheduled planning jobs
from `farplane/steer.config.toml`. PM-visible threads are grouped in
`farplane/pm.json`.

## Common Failure Modes

- `file_scaffold_only:` Files exist, but goals and runtime commands are still
  placeholders. Report `substrate_complete`, not `project_initialized`.
- `automation_surprise:` Bootstrap creates live automations without operator
  intent. Do not do this; route activation through `automation-advisor`.
- `loop_duplication:` Daily/weekly/quarterly jobs become separate threads.
  Keep them as Steer jobs.
- `config_bloat:` `steer.config.toml` starts duplicating skill runbooks. Keep it
  to job `id`, `cadence`, and `prompt`.
- `state_mixup:` runtime timestamps or automation IDs enter tracked Steer
  config. Store schedule runtime in `.farplane/state/steer-scheduler.json`;
  keep `farplane/pm.json` for UI thread grouping only.
- `goal_drift:` autonomous loops activate against placeholder goals. Run
  `horizon-advisor` first, then `goal-advisor` once the frontier is executable.
- `pm_ui_split:` Pulse, Steer, or ticket-worker threads are not listed in
  `farplane/pm.json`, so the UI renders them as ephemeral agents. Append
  persistent PM-owned thread IDs to the appropriate `threads.*` list.

## Verification

Run after changing this setup story:

```bash
python3 bin/validators/check_farplane_project_files.py
python3 bin/validators/check_doc_refs.py
python3 skills/skill-maintenance/scripts/check_skills.py --write
```

Run `python3 tickets/scripts/check_ticket_metadata.py` when ticket metadata is
in scope. Existing unrelated ticket metadata failures should be reported rather
than hidden.
