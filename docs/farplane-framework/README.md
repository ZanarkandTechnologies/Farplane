---
title: Farplane Framework
status: active
owner: harness
created_at: 2026-06-15
updated_at: 2026-06-23
framework_template_version: "0.2.0"
source_of_truth:
  - farplane/README.md
  - farplane/manifest.json
  - farplane/harness.md
  - farplane/goals.md
  - farplane/automations.md
  - farplane/steer.config.toml
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
and two recurring Codex automation loops.

```text
project = files + tickets + skills + goals + bindings + Steer/Pulse + runtime reports
```

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
    steer.config.toml
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
    state/steer-scheduler.json
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
   + farplane/steer.config.toml
   + farplane/bindings.md
   + farplane/evals.md
   + farplane/pm.json?
   + .farplane/ ignored runtime root
```

`harness-creator` fills or refines the operating program: mission, values,
goals, KPIs, feedback loops, missing skills, current milestone, and automation
setup. It should produce Steer/Pulse-ready project harness output rather than a
separate automation manifest.

## Automation Model

Farplane projects use two recurring automation loops:

```text
pulse_update(...)  # fast idle/action loop
steer_update(...)  # scheduled planning loop
```

Pulse is the actor loop. It wakes frequently, reconciles outcomes, selects one
bounded action, optionally hands off work, and records decision/reward state.

Steer is the planning loop. Its live Codex prompt is reviewed in
`farplane/automations.md`. When the project uses the optional helper config,
it reads `farplane/steer.config.toml`, checks cached `next_due_at` values in
`.farplane/state/steer-scheduler.json`, runs due jobs, writes date-stamped
reports, and advances scheduler state.

The full contract lives in [Steer and Pulse Automation](../specs/steer-pulse-automation.md).

## Automation Authoring

Use `automation-advisor` when creating or revising live Codex automations. The
advisor owns prompt templates and config guidance; it is not a compiler.

```text
automation_advisor(intent, project_refs, current_automation?, steer_config?)
  -> prompt_delta + config_delta? + proof_checklist
```

Live Codex automations should load their owning skills:

- `skills/pulse-update/SKILL.md`
- `skills/steer-update/SKILL.md`

## Reports

Reports are date-stamped records:

```text
.farplane/reports/pulse/<YYYY-MM-DDTHHMMSSZ>.md
.farplane/reports/steer/<job>/<YYYY-MM-DDTHHMMSSZ>.md
```

State files may store `last_report` pointers. Do not make `latest.md` the
canonical report contract for new framework surfaces.

## File Specs

See [Project Files](project-files.md) for file-by-file responsibilities.

For the end-to-end bootstrap and automation activation story, see
[Deep Init Critical Path](deep-init-critical-path.md).
