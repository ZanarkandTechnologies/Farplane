---
title: Project Files
status: active
owner: harness
created_at: 2026-06-15
updated_at: 2026-06-24
framework_template_version: "0.2.0"
source_of_truth:
  - docs/farplane-framework/README.md
  - farplane/manifest.json
  - farplane/automations.md
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

Human-reviewable Codex automation prompt source. It stores the exact Pulse,
Daily Interval, and Weekly Interval prompt blocks copied into the Codex app
automation records.

Skills stay generic and parameterized. Project-specific cadence, paths,
policies, thread IDs, and schedule choices live in the prompts here. This file
is not generated runtime state and does not store `last_run_at`, `next_due_at`,
or automation execution logs.

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
  automation/
  reports/
  evals/runs/
  logs/
```

### `.farplane/automation/`

Mutable Pulse automation state:

- bandit and action-arm scores
- Pulse decision rows
- reward observations
- spawned worker thread rows
- normalized action outcomes

### `.farplane/reports/`

Generated reports. New framework reports should be date-stamped:

```text
.farplane/reports/pulse/<YYYY-MM-DDTHHMMSSZ>.md
.farplane/reports/interval/<interval_id>/<YYYY-MM-DDTHHMMSSZ>.md
```

Consumers find newest interval reports by timestamp sorting or explicit links
from later reports. There is no tracked scheduler config just to store
`last_report`.

## Validation

Run:

```bash
python3 bin/validators/check_farplane_project_files.py
```

The validator checks the current manifest shape, retired file names, bindings
front matter, and obvious secret leakage.
