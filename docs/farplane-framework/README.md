---
title: Farplane Framework
status: active
owner: harness
created_at: 2026-06-15
updated_at: 2026-06-24
framework_template_version: "0.2.0"
source_of_truth:
  - docs/farplane-framework/lifecycle.md
  - docs/farplane-framework/graph-contract.md
  - docs/farplane-framework/hooks-and-runtime.md
  - farplane/README.md
  - farplane/manifest.json
  - farplane/harness.md
  - farplane/goals.md
  - farplane/automations.md
  - farplane/bindings.md
  - farplane/evals.md
  - farplane/pm.json
  - docs/specs/steer-pulse-automation.md
  - docs/specs/program-notation.md
  - skills/deep-init-project/SKILL.md
  - skills/harness-creator/SKILL.md
---

# Farplane Framework

Farplane's project framework is the standard shape for an agent-run project:
tracked config, visible tickets, durable docs, reusable skills, proof surfaces,
and recurring Codex automation loops.

```text
project = files + tickets + skills + goals + bindings + Pulse/Interval + runtime reports
```

## Start Here

Use [Lifecycle](lifecycle.md) as the friendly end-to-end surface. It explains
how a project moves from initialization into Horizon, Goal Advisor, ticketed
Goal execution, Pulse/Interval automations, hooks, drains, and memory compression.

Use [Graph Contract](graph-contract.md) when the lifecycle needs to be consumed
by tools or the Farplane UI. It defines the node, edge, confidence, and finite
state projection model used by the generated lifecycle graph.

Use [Hooks and Runtime](hooks-and-runtime.md) when you need the concrete hook
and runtime-state boundaries. Hooks observe and gate; skills and tickets own
judgment-heavy work.

## Project Tree

```text
PROJECT_ROOT/
  AGENTS.md
  README.md
  PROJECT_RULES.md
  ARCHITECTURE.md

  farplane/
    README.md
    manifest.json
    harness.md
    goals.md
    automations.md
    bindings.md
    evals.md
    pm.json

  tickets/
    README.md
    TASK-0001/
      ticket.md
      program.md
      progress.md
      artifacts/
    archive/
    templates/

  docs/
    MEMORY.md
    HISTORY.md
    LESSONS.md
    TROUBLES.md
    specs/
    fundamentals/

  qa/
  skills/

  .farplane/
    state/run-ledger.json
    automation/
    reports/
    evals/runs/
    logs/
```

Use `farplane/` for tracked config. Use `.farplane/` for generated state,
reports, eval runs, and logs.

## Template Version

This standard uses:

```text
framework_template_version: "0.2.0"
```

When the framework shape changes, bump the manifest `spec_version`, dogfood the
current Farplane files, update deep-init and harness-creator templates, and run
the project-file validator.

## Setup Lifecycle

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
   + farplane/pm.json?
   + .farplane/ ignored runtime root
```

`harness-creator` fills or refines the operating program: mission, values,
goals, KPIs, feedback loops, missing skills, current milestone, and automation
setup. It should produce Pulse/Interval-ready project harness output rather than a
separate automation manifest.

## Automation Model

Farplane projects use explicit recurring automation loops:

```text
pulse_update(...)  # fast idle/action loop
interval_update(...)  # scheduled report-then-plan loop
```

Pulse is the actor loop. It wakes frequently, reconciles outcomes, selects one
bounded action, optionally hands off work, and records decision/reward state.

Daily Interval and Weekly Interval are planning loops. Their live Codex prompts
are reviewed in `farplane/automations.md`; Codex automation records own their
cadence. They call `interval-update`, write date-stamped reports, check drift,
and produce Pulse guidance or Goal Advisor handoffs.

The full contract lives in [Pulse and Interval Automation](../specs/steer-pulse-automation.md).

## Automation Authoring

Use `automation-advisor` when creating or revising live Codex automations. The
advisor owns prompt templates and config guidance; it is not a compiler.

```text
automation_advisor(intent, project_refs, current_automation?)
  -> prompt_delta + proof_checklist
```

Live Codex automations should load their owning skills:

- `skills/pulse-update/SKILL.md`
- `skills/interval-update/SKILL.md`

## Reports

Reports are date-stamped records:

```text
.farplane/reports/pulse/<YYYY-MM-DDTHHMMSSZ>.md
.farplane/reports/interval/<interval_id>/<YYYY-MM-DDTHHMMSSZ>.md
```

State files may store `last_report` pointers. Do not make `latest.md` the
canonical report contract for new framework surfaces.

## File Specs

See [Project Files](project-files.md) for file-by-file responsibilities.

For the end-to-end bootstrap and automation activation story, see
[Deep Init Critical Path](deep-init-critical-path.md).
