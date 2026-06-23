---
title: Project Files
status: active
owner: harness
created_at: 2026-06-15
updated_at: 2026-06-23
framework_template_version: "0.2.0"
source_of_truth:
  - docs/farplane-framework/README.md
  - farplane/manifest.json
  - farplane/automations.md
  - farplane/steer.config.json
  - farplane/bindings.md
  - farplane/pm.json
  - .gitignore
---

# Project Files

Farplane projects separate tracked control files from local runtime state.

```text
farplane/   = tracked project framework config
.farplane/  = ignored local runtime state, reports, eval runs, and logs
docs/       = tracked human-readable project memory and durable narrative
tickets/    = visible work queue and proof surface
skills/     = tracked reusable project or repo skills
```

## Tracked Framework Config

```text
farplane/
  manifest.json
  README.md
  harness.md
  goals.md
  automations.md
  steer.config.json
  bindings.md
  evals.md
  pm.json
```

### `farplane/manifest.json`

Versioned project spec manifest. It records which files are standard tracked
project config and which ignored runtime paths should exist locally.

Use `template_uses.farplane-framework` in this JSON file so Farplane can count
which projects are current, stale, or missing for the framework template.

### `farplane/harness.md`

Project constitution and operating model: mission, values, non-tradeoffs,
systems, modes, feedback loops, and skill bindings.

### `farplane/goals.md`

Project strategy context: north star, current milestone, KPIs, strategy axes,
holds, stop conditions, and Goal Advisor handoffs.

### `farplane/automations.md`

Human-reviewable Codex automation prompt source. It stores the exact Pulse and
Steer prompt blocks copied into the Codex app automation records.

Skills stay generic and parameterized. Project-specific cadence, paths,
policies, thread IDs, and schedule choices live in the prompts here. This file
is not generated runtime state and does not store `last_run_at`, `next_due_at`,
or automation execution logs.

### `farplane/steer.config.json`

Human-owned Steer job config:

- config version and timezone
- scheduler state ref
- scheduled planning jobs
- job cadence strings
- job prompts

Use `template_uses.farplane-steer-config` so project rollout reporting can tell
which projects have adopted the current Steer config template.

Keep this file easy to edit. If a job should not run, remove it from the list.
Do not duplicate workflow inputs, outputs, drift checks, report paths, or gates
that the job prompt or skill already owns. Mutable fields such as
`last_run_at`, `next_due_at`, and `last_report` belong in
`.farplane/state/steer-scheduler.json`.

### `farplane/bindings.md`

Non-secret project coordinates: URLs, handles, safe IDs, labels, aliases,
database names, dashboard links, and notification channel labels. Do not store
secrets or credentials here.

### `farplane/evals.md`

Project-level proof and eval policy: smoke checks, acceptance examples,
regression cases, review rubrics, and evidence routes.

### `farplane/pm.json`

Optional UI glue for grouping multiple Codex threads under one persistent
employee/PM agent in the Farplane UI. It is not loop state, scheduler state, or
an automation registry.

```json
{
  "version": 1,
  "name": "Project PM",
  "role": "founder_operator",
  "threads": {
    "chats": [],
    "automations": []
  }
}
```

Use `threads.chats` for persistent chat or worker threads that should render
under the same employee agent. Use `threads.automations` for automation-owned
threads that should also render under that employee. Threads not listed here
may appear as ephemeral agents in the UI.

## Ignored Runtime State

```text
.farplane/
  README.md
  state/run-ledger.json
  state/steer-scheduler.json
  reports/
  evals/runs/
  logs/
```

### `.farplane/state/steer-scheduler.json`

Mutable Steer scheduler cache:

- config version used to generate state
- per-job `last_run_at`
- per-job `next_due_at`
- per-job `last_report`
- per-job `last_status`

Steer reads this file first after loading config. The normal hot path is simple
timestamp comparison against cached `next_due_at` values.

### `.farplane/reports/`

Generated reports. New framework reports should be date-stamped:

```text
.farplane/reports/pulse/<YYYY-MM-DDTHHMMSSZ>.md
.farplane/reports/steer/<job>/<YYYY-MM-DDTHHMMSSZ>.md
```

State files store newest-report pointers when needed.

## Validation

Run:

```bash
python3 bin/validators/check_farplane_project_files.py
```

The validator checks the current manifest shape, retired file names, Steer
config JSON, bindings front matter, and obvious secret leakage.
