---
title: Farplane Framework
status: active
owner: harness
created_at: 2026-06-15
updated_at: 2026-07-11
framework_template_version: "0.3.0"
source_of_truth:
  - docs/farplane-framework/v1.md
  - docs/farplane-framework/lifecycle.md
  - docs/farplane-framework/ticket-execution-loop.md
  - docs/farplane-framework/pulse-and-interval-loop.md
  - docs/farplane-framework/graph-contract.md
  - docs/farplane-framework/harness-maintenance.md
  - docs/farplane-framework/hooks-and-runtime.md
  - docs/farplane-framework/reporting.md
  - docs/systems/README.md
  - docs/systems/registry.jsonl
  - docs/features/registry.jsonl
  - farplane/README.md
  - farplane/manifest.json
  - farplane/harness.md
  - farplane/goals.yaml
  - farplane/metrics.yaml
  - farplane/automations.toml
  - farplane/bindings.yaml
  - farplane/hooks.json
  - farplane/pm.json
  - docs/features/FEAT-0065-pulse-and-interval-automation.md
  - docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md
  - skills/init-advisor/SKILL.md
  - skills/harness-creator/SKILL.md
---

# Farplane Framework

Farplane's project framework is the local structure that lets every cloned
harness carry the same minimum operating standard: tracked config, visible
tickets, durable docs, reusable skills, proof surfaces, versioned templates,
and recurring Codex automation loops.

```text
project = program files + tickets + skills + one Work Pulse + scheduled report/ticket sources
```

This framework is the bridge between the two main product surfaces:

- **Farplane Core** defines and validates the project shape.
- **Farplane UI** reads the generated payloads and manifests so operators can
  view global harness state and project/company state without each panel
  re-inventing framework semantics.

## Start Here

Use [Lifecycle](lifecycle.md) as the friendly end-to-end overview. It explains
how a project moves from initialization into Horizon, Goal Advisor, ticketed
Goal execution, metric snapshots, budget/runway review, Pulse/Interval
automations, hooks, drains, and memory compression.

Use [Ticket Execution Loop](ticket-execution-loop.md) when the question is how
human shaping, ticket fields, `impl-plan`, `goal-advisor`, autonomous Goal
execution, QA/proof, reviewer gates, and closeout work together.

Use [Pulse And Interval Loop](pulse-and-interval-loop.md) when the question is
how the one Work Pulse, Daily/Weekly BAU reports, Feed Scout, Dogfood
self-improvement, ticket Reward check-ins, and their bounded ticket sources
coordinate higher-level work.

Use [Farplane Framework V1](v1.md) for the canonical operating model and its
derivation from `program + progress`: one Work Pulse, ticket-backed check-ins,
capability skills, and immediate or delayed self-improvement. The structural
migration is complete; current work is operational proof and evidence-driven
refinement.

Use [Graph Contract](graph-contract.md) when the lifecycle needs to be consumed
by tools or the Farplane UI. It defines the node, edge, confidence, and finite
state projection model used by the generated lifecycle graph.

Use [Harness Maintenance Features](harness-maintenance.md) when you need to
remember which maintenance systems exist: system and feature registries,
template registries, skill OS checks, template rollout, project adoption, graph
projections, evals, doc tracking, and CLI/UI payloads.

Use the Farplane UI product model in
[`../Farplane-UI/docs/features/FP02-harness-product-model.md`](../../../Farplane-UI/docs/features/FP02-harness-product-model.md)
when deciding whether a surface belongs in a global harness entrypoint or a
project/company panel.

Use [Hooks and Runtime](hooks-and-runtime.md) when you need the concrete hook
and runtime-state boundaries. Hooks observe and gate; skills and tickets own
judgment-heavy work.

Use [Reporting](reporting.md) when UI or report producers need the current
Core-owned Markdown frontmatter and `.farplane/reports/index.json` registry
contract.

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
    goals.yaml
    metrics.yaml
    automations.toml
    bindings.yaml
    hooks.json
    pm.json

  .agents/
    skills/
      README.md
      <capability>/SKILL.md

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
    features/
    fundamentals/

  qa/
  skills/

  .farplane/
    automation/
      decisions.jsonl
      spawned-threads.jsonl
    reports/
    metrics/daily/
    evals/runs/
    logs/
```

Use `farplane/` for tracked config. Use `.farplane/` for owner-named generated
state, reports, metric observations, eval runs, and logs; ticket QA and review
evidence stays under the owning ticket.

`farplane/manifest.json` carries the small UI card identity:
`project.name`, `project.description`, and `project.archetype`. The richer
description of what the project is lives in Markdown: `farplane/harness.md`
owns the static human charter and stable capability refs, while
`farplane/goals.yaml` owns current strategy and KPI IDs, and
`farplane/metrics.yaml` defines those metrics independently from provider
bindings. The reporting standard is a framework doc, not a project primitive;
see [Reporting](reporting.md).
Project-specific capability workflows live under `.agents/skills/`; promote them
to root `skills/` only after repeated evidence shows cross-project reuse.

## Template Version

This standard uses:

```text
framework_template_version: "0.3.0"
```

When the framework shape changes, bump the manifest `spec_version`, dogfood the
current Farplane files, update init-advisor and harness-creator templates, and
run the project-file validator.

## Setup Lifecycle

```text
init_advisor(project_root?, project_idea?, repo_shape?, stack_profile?, init_mode?, force?)
  -> AGENTS.md
   + PROJECT_RULES.md
   + ARCHITECTURE.md
   + docs/*
   + tickets/*
   + qa/*
   + farplane/README.md
   + farplane/manifest.json
   + farplane/harness.md
   + farplane/goals.yaml
   + farplane/metrics.yaml
   + farplane/automations.toml
   + farplane/bindings.yaml
   + farplane/hooks.json
   + .agents/skills/README.md
   + farplane/pm.json?
   + .farplane/ ignored runtime root
```

In `full` init mode, `init-advisor` calls `harness-creator` after the
substrate exists. `harness-creator` fills or refines the split project files:
static charter and capability refs in `harness.md`, strategy and KPI IDs in
`goals.yaml`, metric semantics in `metrics.yaml`, full automation configs in
`automations.toml`, and safe provider coordinates in `bindings.yaml`. It owns the smaller advisor calls such
as research, `horizon-advisor`, `harness-advisor`, `skill-creator`, and
`goal-advisor` when those are needed. Canonical `harness.md` files use YAML
front matter plus Markdown sections, not a fenced custom program DSL.

## Automation Model

Farplane projects use one execution heartbeat plus bounded scheduled sources:

```text
pulse_update(...)     # fast board execution and due check-ins
feed_scout(...)       # source report + bounded opportunity tickets
interval_update(...)  # BAU problem report + known maintenance tickets
dogfood_review(...)   # portfolio learning + 0..experiment_wave_size Goal Packets
```

Work Pulse is the only heartbeat. It reconciles outcomes, derives matured
Reward rows from original tickets, dispatches admitted tickets up to policy
caps, and asks the BAU planner for a bounded wave only when no executable work
exists.

Daily and Weekly Interval are cron/manual BAU reporting jobs. They write dated
Problems ledgers and may resurface only bounded maintenance already supported
by prior finalized evidence. Feed Scout and Dogfood Review run separately and
may create only their own bounded ticket class. None of these jobs execute
tickets or perform matured check-ins; Work Pulse owns that shared path.

The active contract lives in [Work Pulse And Scheduled Ticket Sources](pulse-and-interval-loop.md).

## Automation Authoring

Use `automation-advisor` when creating or revising live Codex automations. The
advisor owns prompt templates and config guidance; it is not a compiler.

```text
automation_advisor(intent, project_refs, current_automation?)
  -> config_delta + proof_checklist
```

Live Codex automations should load their owning skills:

- `skills/pulse-update/SKILL.md`
- `skills/interval-update/SKILL.md`

## Reports

Reports are date-stamped records:

```text
.farplane/reports/pulse/<YYYY-MM-DDTHHMMSSZ>.md
.farplane/reports/interval/<interval_id>/<YYYY-MM-DDTHHMMSSZ>.md
.farplane/reports/dogfood-review/<YYYY-MM-DDTHHMMSSZ>.md
.farplane/reports/index.json
```

UI-indexed report Markdown must include `ref`, `kind`, `created_at`, and
`ui_summary` frontmatter. Core builds `.farplane/reports/index.json` with
prefix-derived hierarchy from `ref`; see [Reporting](reporting.md). State files
may store `last_report` pointers. Do not make `latest.md` the canonical report
contract for new framework surfaces.

## File Specs

See [Project Files](project-files.md) for file-by-file responsibilities.

For the end-to-end bootstrap and automation activation story, see
[Init Advisor Critical Path](init-advisor-critical-path.md).
