---
title: "Nested PM Projects"
status: designed
owner: project-pm-automation
created_at: 2026-06-23
updated_at: 2026-06-23
tags:
  - farplane
  - nested-projects
  - pm
  - self-improvement
refs:
  - docs/farplane-framework/README.md
  - docs/farplane-framework/project-files.md
  - docs/futureideas/autonomous-unit-filesystem.md
  - docs/specs/goal-loop-contract.md
  - farplane/goals.md
---

# Nested PM Projects

Farplane allows projects to nest.
A parent project can coordinate child projects, read their PM reports, and
delegate work downward without merging transcripts or hiding state.

The model is valid for large autonomous units such as:

- `Zanarkand Technologies` as a parent portfolio.
- `Farplane` as a child project.
- `Farplane UI` as a sibling or child product project.
- A future `Skill System` child project, if skill-system improvement proves it
  needs its own goals, cadence, memory, tickets, reports, and parent rollup.

Nested projects are not the same as one PM per skill.
Most skill work should start as tickets or Goal Packets inside the owning
project and promote only when the loop has independent project gravity.

## Contract

```text
nested_pm_project(parent_project, child_project)
  -> child_farplane_config
   + child_ticket_board
   + child_pm_reports
   + parent_rollup_entry
   + delegation_boundary
```

The parent PM does not inspect every child transcript by default.
It reads child project surfaces:

- `farplane/goals.md` for child strategy and current milestone.
- `farplane/steer.config.toml` for child scheduled planning jobs.
- Date-stamped `.farplane/reports/**` records and scheduler pointers for child
  PM status.
- `tickets/` for executable child work and blockers.
- `docs/MEMORY.md`, `docs/LESSONS.md`, and `docs/TROUBLES.md` for durable
  child learning when topic-relevant.
- `farplane/pm.json` when UI thread grouping is needed.

## Promotion Rule

Start with the smallest durable surface that can prove the loop.

```text
promote_to_child_project(loop)
  iff independent_strategy(loop)
   OR independent_cadence(loop)
   OR independent_memory(loop)
   OR independent_ticket_board(loop)
   OR parent_surface_noise(loop)
   OR parent_child_rollup_needed(loop)
```

Interpretation:

- `independent_strategy`: the loop has goals, KPIs, holds, or milestones that
  are not just one parent milestone.
- `independent_cadence`: the loop needs its own Pulse/Steer cadence or
  scheduled planning actions that would clutter the parent project config.
- `independent_memory`: the loop accumulates local lessons, troubles, or
  invariants that should not all roll up into parent memory.
- `independent_ticket_board`: the loop has multiple active tickets whose state
  is easier to manage locally than as parent tasks.
- `parent_surface_noise`: parent `farplane/goals.md`, reports, or ticket board
  become harder to scan because the child loop is too large.
- `parent_child_rollup_needed`: a parent PM needs a compact status interface
  rather than reading many child tickets directly.

## Skill-System Example

Skill-system improvement is a good candidate for a staged promotion test.

Default starting shape:

```text
Farplane/
  farplane/goals.md              # names skill-system improvement as a program
  tickets/TASK-XXXX/
    ticket.md                    # Skill-System PM pilot
    program.md                   # targets, cadence, metric, stop conditions
    progress.md                  # append-only PM status
    artifacts/                   # reports, eval results, reviews
  tickets/TASK-YYYY/             # per-skill Goal Packet, e.g. skill-maintenance
  tickets/TASK-ZZZZ/             # per-skill Goal Packet, e.g. skill-creator
  tickets/TASK-AAAA/             # per-skill Goal Packet, e.g. eval
```

Promote to a child project only when the pilot shows the loop needs separate
project files:

```text
Farplane/
  projects/skill-system/
    farplane/
    tickets/
    docs/
    .farplane/
```

The exact child path is a project-framework decision.
Do not place PM state inside `skills/<skill-name>/`.
`skills/` remains the reusable skill package inventory.

## PM Count Rule

Use this escalation ladder:

```text
one_project_pm
  -> per-domain PM pilot
  -> child_project_pm
  -> temporary per-skill specialist lane
```

Do not create one permanent PM per skill by default.

Use a temporary specialist lane or per-skill Goal Packet when:

- one skill has an active experiment;
- one skill needs hardening, refinement, eval repair, or audit work;
- a reviewer or QA lane needs isolated context;
- the work can collapse back into the parent project after completion.

Use a child project PM when:

- the loop has its own roadmap;
- several tickets are active at once;
- the parent PM needs status rollups;
- recurring reports or automations are useful;
- local memory and lessons need a child-owned home.

## Lightweight PM-Loop Initialization

A future `deep-init-project` mode may create a lightweight PM loop without app
scaffolding:

```text
deep_init_project(project_root, harness_depth="pm_loop")
  -> farplane/
   + tickets/
   + docs/MEMORY.md
   + docs/LESSONS.md
   + docs/TROUBLES.md
   + .farplane/
   + no app scaffold
```

This mode should not be added only because nesting is possible.
Add it after one or more pilots prove the minimal file set, report shape, and
parent rollup contract.

## Parent Rollup

A parent PM should treat each child project as an autonomous unit with a compact
read interface:

```text
read_child_project(child_root)
  -> goals_summary
   + latest_reports
   + active_blockers
   + ticket_status
   + memory_delta
   + delegation_options
```

The parent may then:

- record a rollup in its own PM report;
- delegate a ticket to the child project;
- request child feedback;
- promote a child lesson into parent memory;
- leave the child alone when it is fresh and unblocked.

## Non-Goals

- No hidden daemon, queue, or hosted control plane.
- No one-PM-per-skill default.
- No child project without durable state and a parent rollup need.
- No canonical PM state inside `skills/<skill-name>/`.
- No duplicated strategy source when parent tickets or Goal Packets are enough.

## Proof Gates

Before creating a new child PM project, prove at least one of:

- central tickets failed to preserve or summarize state clearly;
- parent PM reports became noisy because the loop was too large;
- three or more child-loop tickets needed concurrent management;
- child-specific memory or automations would be clearer than parent-local rows;
- a parent-child rollup report would reduce coordination cost.

Before adding `deep-init-project(..., harness_depth="pm_loop")`, prove:

- the minimal PM-loop file set from a real pilot;
- the expected report and rollup shape;
- validator or doc-index updates needed for nested child discovery;
- migration behavior from parent tickets into a child project.
