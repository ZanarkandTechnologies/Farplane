---
title: Farplane Framework
status: draft
owner: harness
created_at: 2026-06-15
updated_at: 2026-06-17
framework_template_version: "0.1.0"
source_of_truth:
  - farplane/README.md
  - farplane/manifest.json
  - farplane/harness.md
  - farplane/goals.md
  - farplane/automations.md
  - farplane/bindings.md
  - farplane/evals.md
  - farplane/pm.json
  - docs/specs/program-notation.md
  - skills/deep-init-project/SKILL.md
  - skills/harness-creator/SKILL.md
---

# Farplane Framework

Farplane's project framework is the standard shape for an agent-run project:
tracked config, visible tickets, durable docs, reusable skills, and recurring
PM-style automations.

The point is simple:

```text
project = files + tickets + skills + goals + bindings + automations + PM threads + runtime reports
```

## Project Tree

Every initialized project should be legible from the filesystem.
Small projects may leave optional files as drafts, but the structure should be
predictable.

```text
PROJECT_ROOT/
  AGENTS.md                    # operating policy loaded by Codex in this repo
  README.md                    # human entry point: what the project is and how to use it
  PROJECT_RULES.md             # project-specific run commands, stack rules, and gates
  ARCHITECTURE.md              # top-level system map when the project has software shape

  farplane/                    # tracked project framework config
    README.md                  # local index for the framework files
    manifest.json              # versioned Farplane project spec manifest
    harness.md                 # mission, values, modes, operating principles, systems
    goals.md                   # north star, current milestone, KPIs, strategy axes
    automations.md             # recurring jobs, schedules, grouped cadences, report paths
    bindings.md                # non-secret project IDs, URLs, labels, aliases
    evals.md                   # project evals, smoke checks, proof and review policy
    pm.json                    # optional UI manifest for chat and automation thread IDs

  tickets/                     # local visible work queue
    README.md                  # ticket state machine and ticket-as-program rules
    TASK-0001/
      ticket.md                # compact task contract
      program.md               # optional Goal Packet loop config
      progress.md              # optional append-only execution log
      artifacts/               # proof, review, QA, screenshots, generated reports
    archive/                   # closed tickets
    templates/                 # ticket templates

  docs/                        # tracked durable knowledge and narrative
    MEMORY.md                  # durable invariants and constraints
    HISTORY.md                 # meaningful project timeline
    LESSONS.md                 # distilled reusable prevention lessons
    TROUBLES.md                # raw repeated misses, blockers, corrections
    specs/                     # concrete system contracts and specs
    fundamentals/              # cross-surface theory and doctrine

  skills/                      # repo-owned reusable workflows when local skills exist

  .farplane/                   # ignored runtime state
    state/run-ledger.json      # job freshness, running/blocked/failed state
    reports/<job>/latest.md    # cached report for a recurring job
    reports/<job>/runs/        # timestamped report history
    evals/runs/                # generated eval outputs
    logs/                      # local runtime logs
```

Use `farplane/` for tracked config.
Use `.farplane/` for generated state.
The dot is the boundary between project contract and runtime cache.

See [Project Files](project-files.md) for the file-by-file spec and rationale
behind each surface.

## Template Version

This draft standard uses:

```text
framework_template_version: "0.1.0"
```

Every tracked `farplane/*.md` file should declare that version in front matter.
When the framework shape changes, bump the version and update the dogfooded
Farplane files, deep-init templates, harness-creator templates, and validators
together.

## Setup Lifecycle

One public skill creates the project shape.
Farplane is not a mode; it is the framework default.

```text
deep_init_project(project_root?, project_idea?, repo_shape?, profile?, harness_depth?)
  -> AGENTS.md
   + PROJECT_RULES.md
   + ARCHITECTURE.md
   + docs/*
   + tickets/*
   + qa/*
   + farplane/README.md
   + farplane/manifest.json
   + farplane/harness.md
   + farplane/goals.md
   + farplane/automations.md
   + farplane/bindings.md
   + farplane/evals.md
   + farplane/pm.json
   + .farplane/ ignored runtime root
```

Use `deep-init-project` when a repo lacks the standard project substrate or
when an existing repo should join the AI office.

`harness_depth` controls how much operating harness is initialized:

```text
none      # substrate-only migration
light     # minimal farplane/*.md files
standard  # default project harness
full      # richer business/product/content operating program
```

```text
project_harness_creator(project_idea, values?, priorities?, mode_presets?, context?, constraints?, budget?)
  -> farplane/harness.md
   + farplane/goals.md
   + farplane/evals.md?
   + farplane/automations.md delta
   + farplane/bindings.md delta
   + unblock tickets
   + Goal Advisor handoff
```

Use `harness-creator` when the project needs a program: mission, values, goals,
KPIs, feedback loops, missing skills, current milestone, and recurring
automations. In normal setup, `deep-init-project` calls it as the internal
operating-program phase when `harness_depth != none`.

Lifecycle:

```text
1. deep_init_project(..., harness_depth=standard)
   -> creates the substrate and initial Farplane config

2. harness_creator_phase(...)
   -> fills or refines the operating program and proposed tickets

3. compile_automations(farplane/automations.md)
   -> one ticket-drainer automation
   -> one weekly PM automation
   -> optional extra cadences only when they need their own schedule

4. weekly_pm_update(...)
   -> refreshes reports, strategy, memory/docs, skills, goals, and tickets

5. daily_ticket_drainer(...)
   -> advances one high-value ticket
```

Live Codex automation prompts may read `farplane/automations.md`, but they
should still carry a compiled program and exact todo list.
The manifest configures the prompt; it does not replace the prompt.

## Automation Model

Each recurring job is a function with inputs, outputs, freshness, reports, and
gates.
Jobs that share a cadence are grouped into one live automation so the PM thread
has one context.

```text
automation(schedule, grouped_jobs, ledger, gates)
  -> run_or_reuse_each_job
   + reports
   + state_delta
```

`farplane/automations.md` owns:

- project identity and mission
- ticket sources
- binding references
- side-effect gates
- schedules
- grouped recurring jobs
- report paths
- run-ledger path

`.farplane/state/run-ledger.json` records whether a job is fresh, running,
blocked, failed, or stale.
If a daily feed scout already ran and the weekly PM needs the same report, the
weekly PM reuses the fresh report instead of doing duplicate work.

## Scrum Cadence

The default operating model is intentionally close to Scrum:

```text
weekly_pm_update(...)  # plan, inspect, update strategy, shape tickets
daily_ticket_drainer(...)  # execute one ready ticket
```

The PM heartbeat owns planning and system upkeep.
The ticket drainer owns leaf execution.
Do not mix these by default.

### Weekly PM Update

```text
weekly_pm_update(project, config, bindings, ledger, grouped_jobs)
  -> weekly_pm_report
   + strategy_delta
   + goal_delta
   + ticket_board_delta
   + memory_docs_delta
   + skill_improvement_delta
   + blockers
```

Default grouped jobs:

```text
update_external_context(feed-scout, max_age=24h)
update_memory(update-memory, max_age=7d, covers=memory+docs)
skill_hardening(skill-maintenance.harden_skill, max_age=7d)
skill_refinement(skill-maintenance.refine_skill, max_age=7d)
registry_drift(skill-maintenance, max_age=7d)
update_strategy(update-strategy, max_age=7d)
```

The weekly PM may create or update local tickets.
It should not execute leaf tickets unless the project explicitly chooses a
combined cadence.

### Ticket Drainer

```text
daily_ticket_drainer(project, ticket_sources, bindings, gates, ranking_policy, limit=1)
  -> selected_ticket | no_op_report
   + impl_plan_result?
   + goal_advisor_execution?
   + evidence_or_blocker
```

Order:

1. Fetch local tickets first.
2. If no local ticket is proceedable, fetch Notion only when enabled in
   `farplane/automations.md` and configured in `farplane/bindings.md`.
3. Filter for tickets that are ready, unblocked, direct, autonomous, and safe.
4. Rank by priority, compounding ROI, project value, autonomy, and likelihood
   of reaching Done or Review.
5. Select one ticket.
6. Rename the current Codex automation thread to
   `[Farplane] <ticket-id> <ticket name>` when the thread-title tool is
   available.
7. Run `impl-plan` when planning is missing or stale.
8. Use `goal-advisor` to create or activate the execution goal.
9. Execute as far as possible.
10. Write the ticket report and ledger row.

The ticket drainer must not run feed scout, memory updates, strategy updates,
registry drift, or skill maintenance.

## Context And Docs Update

```text
update_memory(project_root?, readme?, docs?, memory?, history?, lessons?, troubles?, recent_progress?)
  -> memory_delta
   + readme_delta
   + docs_delta
   + docs_consolidation_plan?
   + history_candidates
   + lesson_or_trouble_promotions
   + stale_context_notes
```

This is one job, not two.
It updates project memory and documentation together because docs do not need
the urgent harden-then-refine split that skills need.

Inputs:

- `README.md`
- relevant `docs/**/*.md`
- `docs/MEMORY.md`
- `docs/HISTORY.md`
- `docs/LESSONS.md`
- `docs/TROUBLES.md`
- recent tickets, PM reports, and progress artifacts

Outputs:

- `.farplane/reports/memory/latest.md`
- patch-sized README/doc/memory deltas
- docs consolidation ticket when the merge/split/archive decision is too large
- `skill-maintenance(mode: harden_skill)` handoff for eval/gotcha-worthy
  lessons or troubles

Substantial prose cleanup routes through `documentation`.
Strategy routes through `update-strategy`.
Skill evals and gotchas route through `skill-maintenance`.

## Skill Maintenance

Skills need two passes because bad behavior should be blocked quickly before
older guardrails are compacted.

```text
skill_maintenance.harden_skill(skill, lessons, troubles)
  -> new_evals
   + gotchas
   + regression_cases
   + improvement_tickets
   + hardening_report
```

Inputs:

- `docs/LESSONS.md`
- `docs/TROUBLES.md`
- touched `skills/*/SKILL.md`
- existing evals, gotchas, audits, and registry rows

Outputs:

- `.farplane/reports/skill-maintenance/harden-latest.md`
- new evals or gotchas where repeated misses must be prevented
- skill patches or tickets when the behavior change is material

```text
skill_maintenance.refine_skill(skill, evals, gotchas, usage_results)
  -> skill_delta
   + consolidated_evals
   + consolidated_gotchas
   + review_notes
   + refinement_report
```

Inputs:

- skill evals
- skill gotchas
- hardening report
- usage or validation results

Outputs:

- `.farplane/reports/skill-maintenance/refine-latest.md`
- shorter skill wording
- consolidated evals/gotchas
- review notes or tickets when compaction is unsafe

## External Context

```text
update_external_context(feeds, sources, tracked_entities, freshness=24h)
  -> external_context_report
   + source_items
   + scout_decisions
   + proposal_tickets?
```

This is the feed-scout pattern.
It grounds planning in new external signals before the weekly PM updates
strategy.

Reports live under:

```text
.farplane/reports/external-context/latest.md
.farplane/reports/external-context/runs/YYYY-MM-DD.md
```

## Goals And Strategy

Goals are values translated into measurable loops.

```text
values -> goals -> KPIs -> strategy axes -> current milestone -> tickets
```

`farplane/goals.md` owns:

- north star
- operating priorities
- KPIs
- strategy axes
- current milestone
- holds and stop conditions
- Goal Advisor handoffs

The weekly strategy update reads the current goals and all fresh reports:

```text
update_strategy(goal_portfolio, tickets, progress, metrics_or_feedback, reports)
  -> strategy_delta
   + system_gaps
   + experiments
   + ticket_deltas
   + goal_advisor_handoffs
```

It should update strategy and tickets based on evidence.
If a metric is missing, it should create an instrumentation or access ticket
instead of pretending the metric exists.

## Real Example

Faceless AI engineering channel:

```text
values:
  mission: teach practical AI and harness engineering from real work
  priorities: [impact.high, loyal_users.high, trust.high, money.medium]

goal:
  north_star: create trusted AI engineering education that compounds into an academy

KPI axes:
  acquire: qualified viewers from titles/hooks/search
  activate: first useful concept learned per video
  retain: returning viewers, saves, comments, newsletter joins
  revenue: academy demand, consult leads, paid cohort interest
  efficiency: idea-to-published-video cycle time

feedback skills:
  youtube_retention_metrics(status: needs_access)
  operator_usefulness_labels(status: ready)
  comment_objection_miner(status: missing)

weekly PM:
  update_external_context -> inspect creators, methods, trend gaps
  update_memory -> consolidate lessons from published tests into README/docs
  update_strategy -> choose next content bet and tickets

ticket drainer:
  pick one ready ticket, such as "draft first episode outline"
  run impl-plan
  use goal-advisor to execute until done, blocked, or review-ready
```

The first milestone should be evidence-producing:

```text
current_milestone:
  publish or internally review one pilot episode package
  metric: human review + first retention proxy
  stop_when: pilot proves useful, exposes a missing skill, or needs operator approval
```

## Bindings

Bindings connect generic skills to this project.

```text
skill(capability) + binding(project_coordinates) + secret(runtime_env)
  -> usable project tool
```

`farplane/bindings.md` stores safe coordinates:

- GitHub repo names and remotes
- Notion project/page/database aliases
- PostHog project IDs and dashboard URLs
- Vercel project URLs
- WorkOS tenant labels
- notification channel labels

Do not store credentials there.
If a binding is missing, create an unblock ticket or a skill to fetch it.

## File Roles

### `farplane/harness.md`

The project constitution: mission, values, operating principles, modes,
systems, feedback loops, and capability map.

### `farplane/goals.md`

The strategy object: north star, priorities, KPIs, current milestone, and Goal
Advisor handoffs.

### `farplane/automations.md`

The recurring job manifest: schedules, grouped jobs, ticket source policy,
report paths, ledger path, and side-effect gates.

### `farplane/bindings.md`

The non-secret binding manifest: project IDs, URLs, labels, aliases, and safe
lookup handles that skills need.

### `farplane/evals.md`

The project proof policy: smoke checks, end-to-end evals, review gates, and
acceptance examples.

### `farplane/pm.json`

The optional project PM thread manifest. Farplane UI reads it to fold listed
chat and automation Codex thread IDs into one visual project PM without
merging transcripts. Missing file means legacy behavior.

### `farplane/manifest.json`

The versioned Farplane project spec manifest for this project instance. Use it
to answer which spec version the repo instantiated and which paths are standard
tracked or ignored files. Keep this file JSON and small; archive old manifest
snapshots when the spec bumps, and keep semantics, examples, and migration
guidance in Markdown docs.

### `tickets/`

The visible work queue.
Tickets are the unit the drainer can pick, plan, execute, review, and close.

### `.farplane/`

The ignored runtime cache for reports, logs, eval runs, and job freshness.

## Validation

Run these after changing the framework standard:

```bash
python3 bin/validators/check_farplane_project_files.py
python3 bin/validators/check_harness_invariants.py
python3 bin/validators/check_doc_refs.py
python3 skills/skill-maintenance/scripts/check_skills.py --write
```

The project-file validator enforces:

- `farplane/automations.md` has `farplane/bindings.md`
- tracked `farplane/*.md` files declare `framework_template_version`
- `farplane/manifest.json` declares `schema: farplane_project`,
  `spec_version`, and standard/optional tracked or ignored paths
- retired integration-manifest names are not used
- `farplane/bindings.md` declares `kind: project-bindings`
- `farplane/pm.json`, when present, matches the version 1 manifest shape
- obvious credential values are not stored in bindings

## Related Docs

- [project-files.md](project-files.md): compact file reference.
- [../specs/program-notation.md](../specs/program-notation.md): shared program
  vocabulary for skills, tickets, harness programs, and automations.
- [../../farplane/automations.md](../../farplane/automations.md): current
  Farplane automation manifest.
- [../../farplane/bindings.md](../../farplane/bindings.md): current Farplane
  binding manifest.
