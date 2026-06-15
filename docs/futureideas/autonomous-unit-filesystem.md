---
title: Autonomous Unit Filesystem
status: future-idea
owner: harness
created_at: 2026-06-15
source_of_truth:
  - docs/farplane-framework/README.md
  - farplane/goals.md
  - skills/goal-advisor/SKILL.md
  - tickets/templates/goal-loop/program.md
  - tickets/templates/goal-loop/progress.md
---

# Autonomous Unit Filesystem

This is a future idea, not the current Farplane requirement.

The interesting pattern is that a tiny autonomous research loop, a Goal Packet,
a project, and a parent project all seem to use the same filesystem shape at
different scales.

```text
autonomous_unit =
  constitution?
  + program
  + progress
  + memory
  + artifacts
  + children?
  + bindings?
  + automations?
```

## Minimal Loop

The smallest useful loop looks like:

```text
unit/
  program.md      # what the loop is trying to do and how it should run
  progress.md     # what happened so far
  memory.md       # durable lessons or state extracted from the run
  artifacts/      # evidence produced by the run
```

This is close to the basic autonomous auto-research filesystem.

## Goal Packet Projection

Goal Advisor uses a ticket-scoped projection:

```text
tickets/TASK-XXXX/
  ticket.md       # task contract and proof target
  program.md      # loop config: metric, budget, heartbeat, drift, stop policy
  progress.md     # compact append-only observed execution state
  artifacts/      # proof, review, QA, generated outputs
```

Mapping:

```text
constitution  = ticket.md constraints and gates
program       = program.md
progress      = progress.md
memory        = durable notes promoted back into ticket/docs/skills
artifacts     = artifacts/
children      = child tickets only when a real boundary exists
```

## Project Projection

Farplane project structure is the same pattern expanded for a wider project:

```text
project/
  farplane/harness.md        # constitution: mission, values, principles
  farplane/goals.md          # program: strategy, KPIs, current milestone
  farplane/automations.md    # loop runner config: cadences and grouped jobs
  farplane/bindings.md       # project-specific external coordinates
  farplane/evals.md          # proof policy

  .farplane/reports/         # recurring progress reports and run cache
  docs/HISTORY.md            # durable promoted progress
  docs/MEMORY.md             # durable project memory
  docs/LESSONS.md            # generalized learning
  docs/TROUBLES.md           # raw repeated misses and correction pain
  tickets/                   # child executable loops
```

Mapping:

```text
constitution  = farplane/harness.md
program       = farplane/goals.md
progress      = .farplane/reports/* + docs/HISTORY.md
memory        = docs/MEMORY.md + docs/LESSONS.md + docs/TROUBLES.md
artifacts     = tickets/*/artifacts + .farplane/reports/*
children      = tickets/ + subprojects
bindings      = farplane/bindings.md
automations   = farplane/automations.md
```

## Recursive Pattern

A project can contain tickets, and a parent project can contain child projects.
Each layer is an autonomous unit with a different projection:

```text
parent_project/
  farplane/goals.md
  child_project/
    farplane/goals.md
    tickets/TASK-0001/
      program.md
      progress.md
```

The same conceptual slots repeat:

```text
what should happen     -> program
what happened          -> progress
what should persist    -> memory
what proves it         -> artifacts
what can run below it  -> children
```

## Current Decision

Do not force all scales to use identical filenames right now.

The specialized Farplane names are useful:

- `program.md` and `progress.md` are precise for executable Goal Packets.
- `farplane/goals.md` is clearer for project-level strategy.
- `farplane/harness.md` is clearer for values and operating principles.
- `farplane/automations.md` is clearer for scheduled loop configuration.
- `docs/HISTORY.md` is clearer for durable project-level progress.

The current framework should keep working names and only use this abstraction
as a mental model.

## Future Opportunity

If Farplane later needs parent/child project rollups, a generic interface could
help:

```text
read_autonomous_unit(path)
  -> constitution
   + program
   + progress
   + memory
   + artifacts
   + children
   + bindings
   + automations
```

That could let a root PM summarize subprojects, roll up memory, and compare
progress without caring whether a child is a ticket, a project, or a research
loop.

This is cream-of-the-crop architecture, not required for the current framework.
