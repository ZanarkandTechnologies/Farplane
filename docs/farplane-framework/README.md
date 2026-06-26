---
title: Farplane Framework
status: active
owner: harness
created_at: 2026-06-15
updated_at: 2026-06-26
framework_template_version: "0.2.0"
source_of_truth:
  - docs/farplane-framework/lifecycle.md
  - docs/farplane-framework/graph-contract.md
  - docs/farplane-framework/harness-maintenance.md
  - docs/farplane-framework/hooks-and-runtime.md
  - docs/systems/README.md
  - docs/systems/registry.jsonl
  - docs/features/registry.jsonl
  - farplane/README.md
  - farplane/manifest.json
  - farplane/harness.md
  - farplane/goals.md
  - farplane/products.md
  - farplane/automations.md
  - farplane/bindings.md
  - farplane/hooks.json
  - farplane/pm.json
  - docs/specs/steer-pulse-automation.md
  - docs/specs/program-notation.md
  - skills/init-advisor/SKILL.md
  - skills/harness-creator/SKILL.md
---

# Farplane Framework

Farplane's project framework is the local structure that lets every cloned
harness carry the same minimum operating standard: tracked config, visible
tickets, durable docs, reusable skills, proof surfaces, versioned templates,
and recurring Codex automation loops.

```text
project = files + tickets + skills + goals + bindings + Pulse/Interval + runtime reports
```

This framework is the bridge between the two main product surfaces:

- **Farplane Core** defines and validates the project shape.
- **Farplane UI** reads the generated payloads and manifests so operators can
  view global harness state and project/company state without each panel
  re-inventing framework semantics.

## Start Here

Use [Lifecycle](lifecycle.md) as the friendly end-to-end surface. It explains
how a project moves from initialization into Horizon, Goal Advisor, ticketed
Goal execution, Pulse/Interval automations, hooks, drains, and memory compression.

Use [Graph Contract](graph-contract.md) when the lifecycle needs to be consumed
by tools or the Farplane UI. It defines the node, edge, confidence, and finite
state projection model used by the generated lifecycle graph.

Use [Harness Maintenance Features](harness-maintenance.md) when you need to
remember which maintenance systems exist: system and capability registries,
template registries, skill OS checks, template rollout, project adoption, graph
projections, evals, doc tracking, and CLI/UI payloads.

Use the Farplane UI product model in
[`../Farplane-UI/docs/specs/FP02-harness-product-model.md`](../../../Farplane-UI/docs/specs/FP02-harness-product-model.md)
when deciding whether a surface belongs in a global harness entrypoint or a
project/company panel.

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
    products.md
    automations.md
    bindings.md
    hooks.json
    skills/
      README.md
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

`farplane/manifest.json` carries the small UI card identity:
`project.name`, `project.description`, and `project.archetype`. The richer
description of what the project is lives in Markdown:
`farplane/harness.md` owns the static human charter,
`farplane/products.md` owns the product catalog and work lanes, and
`farplane/goals.md` owns current strategy.
Project-specific product workflows live under `.agents/skills/`; promote them
to root `skills/` only after repeated evidence shows cross-project reuse.

## Template Version

This standard uses:

```text
framework_template_version: "0.2.0"
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
   + farplane/goals.md
   + farplane/products.md
   + farplane/automations.md
   + farplane/bindings.md
   + farplane/hooks.json
   + .agents/skills/README.md
   + farplane/pm.json?
   + .farplane/ ignored runtime root
```

In `full` init mode, `init-advisor` calls `harness-creator` after the
substrate exists. `harness-creator` fills or refines the split project files:
static charter in `harness.md`, product rows and work lanes in `products.md`,
strategy and KPIs in `goals.md`, automation prompt text in `automations.md`,
and safe coordinates in `bindings.md`. It owns the smaller advisor calls such
as research, `horizon-advisor`, `harness-advisor`, `skill-creator`, and
`goal-advisor` when those are needed. Canonical `harness.md` files use YAML
front matter plus Markdown sections, not a fenced custom program DSL.

## Automation Model

Farplane projects use explicit recurring automation loops:

```text
pulse_update(...)  # fast ticket executor loop
interval_update(...)  # scheduled report-then-plan loop
```

Pulse is the executor loop. It wakes frequently, reads the static harness
charter and dynamic product/strategy context, reconciles outcomes, executes
ready tickets up to policy cap, requests planning when no executable work
exists, and records decision/reward state.

Daily Interval and Weekly Interval are planning loops. Their live Codex prompts
are reviewed in `farplane/automations.md`; Codex automation records own their
cadence. They call `interval-update`, write date-stamped reports, check drift,
and produce Pulse guidance or Goal Advisor handoffs. They may propose static
charter deltas in reports, but must not silently apply them.

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
[Init Advisor Critical Path](init-advisor-critical-path.md).
