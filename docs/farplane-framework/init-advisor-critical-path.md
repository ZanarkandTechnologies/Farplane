---
title: "Init Advisor Critical Path"
status: active
owner: farplane-framework
created_at: 2026-06-23
updated_at: 2026-07-11
framework_template_version: "0.3.0"
tags:
  - farplane
  - init-advisor
  - project-setup
  - automations
refs:
  - skills/init-advisor/SKILL.md
  - skills/init-advisor/scripts/bootstrap.sh
  - skills/harness-creator/SKILL.md
  - skills/metric-advisor/SKILL.md
  - skills/goal-advisor/SKILL.md
  - skills/automation-advisor/SKILL.md
  - docs/features/FEAT-0071-project-work-pulse.md
  - docs/farplane-framework/README.md
  - docs/farplane-framework/project-files.md
---

# Init Advisor Critical Path

This is the reader-facing path for creating or migrating a Farplane project.
Initialization creates the substrate; it does not pretend that file creation is
the same as grounded goals or useful autonomous work.

```text
init_advisor(project_root, idea, init_mode, human_intake)
  -> project substrate
   + static charter
   + goals contract
   + capability-skill home
   + one-board ticket and proof surfaces
   + desired automation config
   + operating-model or activation handoff
```

## 1. Bind The Target

Resolve the project root, greenfield/brownfield state, project identity, stack
profile, `init_mode := substrate | full`, human-intake policy, and overwrite
authority. Inspect existing files before writing and preserve them unless
explicit overwrite intent exists.

Stop for credentials, spend, deploys, destructive actions, or genuinely
branching project decisions. Missing human-owned meaning becomes one compact
question or a readiness gap, not invented content.

## 2. Create The Substrate

Create or preserve:

```text
AGENTS.md
PROJECT_RULES.md
README.md
ARCHITECTURE.md
docs/bootstrap-brief.md
docs/prd.md
docs/features/README.md
docs/{HISTORY,MEMORY,TASTE}.md
qa/
tickets/README.md
tickets/templates/
tickets/TASK-0001/ticket.md
```

The result has local policy, durable memory, a visible ticket workflow, QA
entrypoints, and a starter planning handoff. PRD authoring remains downstream
unless explicitly requested.

## 3. Create Framework Config

Tracked project config:

```text
farplane/README.md
farplane/manifest.json
farplane/harness.yaml
farplane/metrics.yaml
farplane/automations.toml
farplane/bindings.yaml
farplane/pm.json
.agents/skills/README.md
```

Ignored runtime state:

```text
.farplane/reports/
.farplane/metrics/
.farplane/project/ui/
.farplane/automation/
.farplane/state/
.farplane/evals/runs/
.farplane/logs/
```

Key ownership:

- `manifest.json`: versioned paths and compact project identity;
- `harness.yaml`: typed human charter, configured planning skill allowlist,
  passive area/ICP context, authority, capability refs, and selected metric refs;
- `metrics.yaml`: provider-independent metric definitions with direction,
  freshness, and optional guard rules;
- `.agents/skills/`: project-local recurring capability workflows;
- `automations.toml`: one Work Pulse heartbeat plus separate scheduled sources;
- `bindings.yaml`: non-secret connector/provider coordinates;
- tickets: executable commitments and all QA/review evidence;
- `.farplane/**`: generated/local observations and reports, not strategy.

Do not scaffold a product catalog, per-category strategy files, per-category
worker policy, or a generated controller index. A recurring output should map
to a callable capability skill; the metric objective explains its measurable contribution and a
ticket owns the current execution.

## 4. Run Readiness Audit

Audit the bootstrap brief, charter, metric selection, bindings, capability ownership,
automation desired state, local skill home, PM grouping config, project rules,
ticket templates, and QA surfaces.

Human-facing results:

```text
Ready
Filesystem ready, operating model still missing
Runtime setup missing
Automation setup missing
```

`project_initialized` requires a grounded operating model, current goals, an
owned route for required recurring outputs, and enough ticket/proof context to
start useful work. Placeholder files are not readiness proof.

## 5. Shape The Operating Model

In `full` mode, `harness-creator` owns the project-specific pass:

```text
harness_creator(idea, values, priorities, current_files, capabilities)
  -> harness delta
   + goals delta
   + capability reuse map
   + local capability stubs or refinement tickets
   + feedback and missing-system tickets
   + initial metric objectives
   + goal_advisor handoff?
```

It checks existing reusable and project-local skills before creating a new
workflow. `metric-advisor` handles material objective/guard depth. `goal-advisor`
compiles a selected material ticket only after the ticket contract is concrete.

## 6. Prepare Automation

The desired project topology has exactly one execution heartbeat:

```text
Work Pulse            heartbeat
Feed Scout            cron/manual
Daily BAU Report      cron/manual
Weekly BAU Report     cron/manual
Dogfood Improvement   cron/manual
Maintenance           cron/manual
```

Bootstrap writes `farplane/automations.toml`; `automation-advisor` owns live
Codex automation activation. Runtime IDs remain in the Codex automation store,
while `pm.json` contains only UI-visible grouping refs.

Scheduled sources may write reports and bounded tickets of their own class.
They do not execute tickets, run due check-ins, or create additional worker
controllers. Work Pulse owns the shared board path.

## 7. Verify

Run the project-file validator, focused scaffold checks, YAML/TOML/JSON parses,
and an old-reference sweep. A clean bootstrap must not create retired project
files or require them to validate.

When live activation was requested, compare desired and live automation state:
one heartbeat, expected cron/manual jobs, correct project target, and no
duplicate executor.

Report the initialized stack, human-gated omissions, current readiness, starter
ticket, and exact next owner. Do not claim full initialization while a required
charter, goal, capability, proof, or runtime input is still a placeholder.
