---
title: "Init Advisor Critical Path"
status: active
owner: farplane-framework
created_at: 2026-06-23
updated_at: 2026-06-25
framework_template_version: "0.2.0"
tags:
  - farplane
  - init-advisor
  - project-setup
  - automations
refs:
  - skills/init-advisor/SKILL.md
  - skills/init-advisor/scripts/bootstrap.sh
  - skills/harness-creator/SKILL.md
  - skills/horizon-advisor/SKILL.md
  - skills/goal-advisor/SKILL.md
  - skills/automation-advisor/SKILL.md
  - docs/specs/steer-pulse-automation.md
  - docs/farplane-framework/README.md
  - docs/farplane-framework/project-files.md
---

# Init Advisor Critical Path

This document is the full story for setting up a new Farplane project. It is
the reader-facing explanation of what `init-advisor` does, what it does
not do, and how the project becomes an autonomous Pulse/Interval project.

```text
init_advisor(...)
  -> project substrate
   + project operating docs
   + project identity and team archetype
   + static human charter
   + ticket system
   + QA/proof surfaces
   + product catalog
   + automation prompt source
   + PM UI thread grouping manifest
   + starter planning ticket
   + harness-creator operating-model handoff_or_result?
   + optional automation-advisor activation handoff
```

Bootstrap creates the filesystem substrate. `harness-creator` owns the
project-specific operating-model pass after substrate setup: static charter,
product catalog, goals/KPIs, feedback loops, missing systems, automation or
binding deltas, and first executable frontier. It may call `horizon-advisor`,
`harness-advisor`, `skill-creator`, `goal-advisor`, or research skills as
smaller internal advisor moves. Live Codex automation activation remains a
separate step owned by `automation-advisor`.

Every material init stage should be expressible as a function signature. Missing
required params become natural question gates: infer from local files and
operator context first, use real-world-equivalent research for grounding, then
ask the smallest blocking question instead of inventing the missing value.

## Critical Path

### 1. Bind the Init Target

Owner: `init-advisor`

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

Signature:

```text
bind_init_target(project_root?, project_idea?, repo_shape?, init_mode?, force?)
  -> target_root
   + project_identity?
   + setup_mode
   + missing_param_question?
```

Guardrails:

- Read existing repo files before writing.
- Preserve existing files unless `force` or explicit overwrite intent is
  present.
- Stop for credentials, billing, cloud project creation, destructive actions,
  or materially branching product decisions.

### 2. Create the Project Substrate

Owner: `init-advisor`

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
- In `full` mode, route product, goals, feedback-loop, and missing-system
  setup through `harness-creator` after the substrate exists.
- Do not convert the whole backlog into tickets.
- Do not claim the project is initialized only because files exist.

### 3. Create Farplane Framework Config

Owner: `init-advisor`

Tracked config:

```text
farplane/README.md
farplane/manifest.json
farplane/harness.md
farplane/goals.md
farplane/products.md
farplane/automations.md
farplane/bindings.md
farplane/hooks.json
farplane/skills/README.md
farplane/pm.json
```

Ignored runtime state:

```text
.farplane/README.md
.farplane/state/run-ledger.json
.farplane/reports/
.farplane/evals/runs/
.farplane/logs/
```

Key contracts:

- `farplane/manifest.json` records the project spec version and standard
  tracked/ignored files, plus a compact UI-facing project identity:
  `project.name`, `project.description`, and `project.archetype`.
- `farplane/harness.md` is the static human charter: mission, human thesis,
  operating principles, non-tradeoffs, static leverage commitments, allocation
  guardrails, agent authority, and change rule. It uses YAML front matter plus
  Markdown sections, not a fenced custom program DSL.
- `farplane/goals.md` is compact dynamic strategy context: north star, value
  function, KPI axes, current bets, milestone, and holds.
- `farplane/products.md` is the project product catalog: team identity,
  product rows, work-lane weights, and constraints. It informs interval
  planning; Pulse executes ready tickets after planners create them.
- `farplane/automations.md` is the human-reviewable source for the exact Pulse,
  Daily Interval, and Weekly Interval prompts copied into Codex automations.
- `farplane/hooks.json` is declarative project hook config. Hook algorithms,
  eval runners, and post-action procedures belong in skills, runtime hooks,
  validators, or ticket programs.
- `farplane/skills/README.md` is the local product-skill home. Project-specific
  production workflows live under `farplane/skills/<product-skill>/SKILL.md`
  until repeated evidence justifies promotion to reusable root `skills/`.
- Codex automation records own cadence. Farplane does not create a tracked
  scheduler config or ignored scheduler state by default.
- `farplane/pm.json` is UI glue that groups PM-visible chat and automation
  thread IDs under one persistent employee agent.

Guardrails:

- Do not recreate `farplane/automations.json` or a hidden automation compiler.
- Do not reintroduce `farplane/steer.config.toml` or
  `.farplane/state/steer-scheduler.json` without a new ticket proving the
  explicit Codex automation model cannot hold the work.
- Do not duplicate workflow inputs, outputs, drift checks, report paths, or
  gates in automation prompts when the called skill already owns them.
- Write automation prompts in signature-style operational language:
  `Call`, `Reads`, `Writes`, `Runs`, and `Gates`. Do not expose raw empty
  internal config objects when a plain read/write contract is clearer.

### 4. Run Readiness Audit

Owner: `init-advisor`

Audit:

- `docs/bootstrap-brief.md`
- `farplane/harness.md`
- `farplane/goals.md`
- `farplane/products.md`
- `farplane/bindings.md`
- `farplane/skills/README.md`
- `farplane/pm.json`
- `PROJECT_RULES.md`
- QA surfaces

Results:

```text
substrate_complete
needs_operating_model_intake
needs_runtime_setup
needs_automation_setup
project_initialized
```

Rules:

- `substrate_complete` means the filesystem base exists.
- `project_initialized` requires a grounded operating model, current goals, and
  enough runtime/proof context to start useful work.
- `needs_operating_model_intake` means `farplane/harness.md`,
  `farplane/products.md`, `farplane/goals.md`, feedback loops, or current
  milestone state are missing, placeholder, stale, or not grounded in the
  operator's current intent.
- missing human thesis, static leverage commitments, agent authority, or change
  rule in `farplane/harness.md` means the project is not ready for autonomous
  activation.
- `needs_automation_setup` means the project has not yet activated live
  Pulse and Interval automations.

Guardrails:

- In `substrate` mode, report missing operating-model/setup questions as the
  next handoff.
- In `full` mode, call `harness-creator` after substrate setup and ask only the
  first missing operating-model parameter before claiming initialization.
- Do not use `goal-advisor` directly from `init-advisor`; `harness-creator` owns the
  execution handoff and should call `goal-advisor` only after the current
  milestone is concrete enough for a ticket-backed Goal Packet.

### 5. Shape The Operating Model

Owner: `harness-creator`

Use this phase in `full` mode, or when the readiness audit finds that
`farplane/harness.md`, `farplane/products.md`, `farplane/goals.md`, feedback
loops, missing-system tickets, automation/binding deltas, or the current
milestone are missing, placeholder, stale, or not grounded.

Inputs:

- operator intent
- real-world-equivalent research for the requested team type
- `farplane/manifest.json` project identity
- `farplane/harness.md`
- existing `farplane/products.md`
- existing `farplane/goals.md`
- current tickets, docs, skills, and safe bindings

Output:

```text
harness_creator(project_idea, values?, priorities?, mode_presets?,
                context?, constraints?, budget?)
  -> farplane/harness.md delta?
   + farplane/products.md delta?
   + farplane/goals.md delta?
   + farplane/automations.md delta?
   + farplane/bindings.md delta?
   + missing-system or unblock tickets?
   + current_milestone
   + goal_advisor_handoff?
   + first_missing_question?
```

What this means:

- The project can answer "what does this team do?" in one sentence.
- The project can answer "what human thesis must not drift?" in one sentence.
- Products are value outputs, not chores.
- Work lanes explain how interval planners should distribute planned work
  without rediscovering the product catalog.
- The manifest has a short UI card; `products.md` has the richer operating
  model.
- The goals file has a value function, KPI axes, current bets, and
  handoff-ready milestone when enough operator intent exists.
- Human access, missing metrics, missing skills, or unavailable integrations
  become explicit tickets or bindings instead of hidden assumptions.

Guardrails:

- Always ground team archetype, product lifecycle, and the first feedback loop
  against real-world equivalents before finalizing `harness.md`, `products.md`,
  or `goals.md`. Keep the
  research compact unless the project is high-risk, unfamiliar, or
  market-facing enough to need a separate `research:*` artifact.
- Do not stuff the full team story into `manifest.json`.
- Do not make operators author raw JSON for product strategy.
- Do not let product changes silently rewrite the human thesis or static
  leverage commitments.
- Do not create marketing/content work unless it is tied to a product,
  accepted experiment, user question, or adoption gap.
- Let `harness-creator` decide which sub-advisor owns a smaller move:
  `horizon-advisor` for strategy/KPI depth, `harness-advisor` for Farplane
  surface placement, `skill-creator` for reusable missing primitives, and
  `goal-advisor` for executable frontier compilation.

### 6. Compile The First Executable Frontier

Owner: `harness-creator` using `goal-advisor`

Use this phase once `harness-creator` has selected a current milestone concrete
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
- The future Pulse and Interval loops have a real project direction to follow.

Guardrails:

- Do not run material Goal work without files.
- Do not use Goal mode as a substitute for missing project strategy.
- Do not self-certify QA/review for material work.

### 7. Optional Code Scaffold

Owner: `init-advisor`

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

Owner: `init-advisor`

Default next path:

```text
brainstorm -> deep-interview -> harness-creator -> goal-advisor
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
   + pulse_automation_id
   + daily_interval_automation_id
   + weekly_interval_automation_id
   + farplane/pm.json thread-grouping delta
```

Activation steps:

1. Inspect existing Codex automations and project threads.
2. Reuse or update matching Pulse/Interval loops instead of creating duplicates.
3. Create or reuse a dedicated `Project Pulse` thread.
4. Attach the Pulse heartbeat automation to the Pulse thread at the fast idle
   cadence.
5. Create or update standalone Codex cron automations for Daily Interval and
   Weekly Interval at their configured cadences.
6. Append the Pulse thread ID and PM-visible automation/thread IDs to
   `farplane/pm.json` when they should render under the same persistent
   employee.

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

- Create the live loops named in `farplane/automations.md`, commonly Pulse,
  Daily Interval, and Weekly Interval.
- Do not create separate ticket-drainer or hidden scheduler threads; Pulse owns
  fast ticket selection and intervals own report-then-plan work.
- Do not activate autonomous loops when the operating model or goals are
  placeholder or stale.
- If Codex thread/automation tools are unavailable, write prepared prompts and
  report `needs_automation_setup`.
- Do not store automation runtime state in `farplane/pm.json`; it is only UI
  grouping glue for thread IDs.
- When Pulse creates persistent ticket/worker threads that should
  appear under the same employee, append those chat thread IDs to
  `threads.chats`.

## File Plan

| Surface | Created By | Updated By | Purpose |
| --- | --- | --- | --- |
| `AGENTS.md` | `init-advisor` | operator / project policy work | local operating policy |
| `PROJECT_RULES.md` | `init-advisor` | runtime/setup work | commands, services, QA paths |
| `ARCHITECTURE.md` | `init-advisor` | architecture/docs work | system map |
| `docs/bootstrap-brief.md` | `init-advisor` | deep interview / setup | setup decisions and readiness |
| `farplane/manifest.json` | `init-advisor` | framework migrations | expected tracked/ignored paths |
| `farplane/harness.md` | `init-advisor` / `harness-creator` | harness planning | static human charter: mission, thesis, non-tradeoffs, leverage commitments, authority, change rule |
| `farplane/goals.md` | `init-advisor` / `harness-creator` / `horizon-advisor` | strategy work | goals, KPIs, milestone |
| `farplane/products.md` | `init-advisor` / `harness-creator` | product planning / work-lane tuning | product rows and work lanes |
| `farplane/automations.md` | `init-advisor` / `automation-advisor` | operator / `automation-advisor` | reviewed Pulse and Interval prompt source |
| `farplane/skills/README.md` | `init-advisor` | `harness-creator` / product-skill refinement | local product-skill home |
| `farplane/pm.json` | `init-advisor` | `automation-advisor` / PM-visible threads | UI grouping for persistent chat and automation threads |
| `tickets/TASK-0001/ticket.md` | `init-advisor` | planning flow | starter PRD/discovery handoff |
| `qa/` | `init-advisor` | QA work | reusable proof paths |

## End States

### Substrate Complete

The repo has the files, tickets, QA surface, and Farplane config skeleton. It
may still need goals, runtime commands, and automation activation.

### Project Initialized

The repo has grounded split-file project state, usable runtime/proof paths, a
starter ticket, and clear next planning or execution handoff. For autonomous
projects, this usually means `harness-creator` has shaped the operating model
and either prepared or produced the first `goal-advisor` handoff.

### Automation Activated

The repo has live recurring automation loops for Pulse, Daily Interval, and
Weekly Interval. Pulse is a persistent heartbeat thread for frequent ticket
execution. Daily and Weekly Interval are standalone Codex cron automations that
write dated reports and plans. PM-visible threads are grouped in
`farplane/pm.json`; automation cadence/runtime metadata stays in the Codex app.

## Common Failure Modes

- `file_scaffold_only:` Files exist, but the operating model, goals, and
  runtime commands are still placeholders. Report `substrate_complete`, not
  `project_initialized`.
- `automation_surprise:` Bootstrap creates live automations without operator
  intent. Do not do this; route activation through `automation-advisor`.
- `loop_duplication:` ticket-drainer, scheduler, or strategy-review jobs become
  extra threads. Keep ticket execution in Pulse and report-then-plan work in
  explicit interval automations.
- `prompt_bloat:` `farplane/automations.md` starts duplicating skill runbooks.
  Keep prompts to skill calls, cadence, and true project-specific extensions.
- `state_mixup:` runtime timestamps or automation IDs enter tracked project
  config. Keep automation runtime IDs in Codex and `farplane/pm.json` for UI
  thread grouping only.
- `goal_drift:` autonomous loops activate against placeholder goals. Run
  `harness-creator` first; it can route to `horizon-advisor` and then
  `goal-advisor` once the frontier is executable.
- `pm_ui_split:` Pulse, Interval, or ticket-worker threads are not listed in
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
