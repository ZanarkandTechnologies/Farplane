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
  - farplane/harness.md
  - farplane/goals.md
  - farplane/automations.md
  - farplane/products.md
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
  products.md
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

The manifest also carries a small UI-facing project identity block:
`project.name`, `project.description`, and `project.archetype`. Keep it short.
Do not turn the manifest into the product strategy document; detailed mission,
products, goals, and operating loops live in the Markdown project files below.

### `farplane/harness.md`

Static human charter: mission, human thesis, operating principles,
non-tradeoffs, static leverage commitments, agent authority, change rule, and
one compact charter-level operating loop.

This file is the one owner for the durable human thesis. Products and goals may
evolve from evidence, but agents must not silently rewrite `harness.md`.
Interval reports may propose harness deltas; applying them requires explicit
human approval.

Use YAML front matter plus Markdown sections and stable tables. Do not put a
fenced `harness-program` DSL block in canonical project harness files. Product
pipelines belong in `products.md`, current strategy belongs in `goals.md`, and
automation prompts belong in `automations.md`.

### `farplane/goals.md`

Project strategy context: north star, current milestone, KPIs, strategy axes,
holds, stop conditions, and Goal Advisor handoffs. This file may evolve through
evidence-backed goals deltas, but it must stay inside the static charter in
`farplane/harness.md`.

### `farplane/products.md`

Project product catalog: the team archetype, operating flywheel, primary and
supporting value outputs, and autonomous project types this team can create.
Products are not chores. Pulse uses this file as context for product-shaped
refill tickets when the board is empty or stale; routine metadata repair,
blocker clarification, QA/eval collection, report writing, and ticket cleanup
stay in Pulse's default action arms.

Use Markdown with YAML front matter and the standard headings `Team Archetype`,
`Operating Flywheel`, `Primary Products`, `Supporting Products`, `Autonomous
Project Types`, `Product Selection Notes`, and `Pulse Refill Guidance`. UI code
can render or project the stable table structure later, but operators should
not have to author raw JSON for product strategy.

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

The validator checks the current manifest shape, retired file names, required
`harness.md` static-charter headings, absence of fenced harness-program DSL in
canonical harness files, duplicate active charter files such as
`farplane/project.md`, product-catalog headings, bindings front matter, and
obvious secret leakage.
