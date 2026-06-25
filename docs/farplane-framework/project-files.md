---
title: Project Files
status: active
owner: harness
created_at: 2026-06-15
updated_at: 2026-06-26
framework_template_version: "0.2.0"
source_of_truth:
  - docs/farplane-framework/README.md
  - farplane/manifest.json
  - farplane/harness.md
  - farplane/goals.md
  - farplane/automations.md
  - farplane/products.md
  - farplane/bindings.md
  - farplane/hooks.json
  - farplane/skills/README.md
  - farplane/pm.json
  - .gitignore
---

# Project Files

Farplane projects separate tracked control files from local runtime state.

```text
farplane/        = tracked project framework config
farplane/skills/ = project-local product skills
.farplane/       = ignored local runtime state, reports, eval runs, and logs
docs/            = tracked human-readable project memory and durable narrative
tickets/         = visible work queue and proof surface
skills/          = tracked reusable cross-project or repo skills
```

## Project File Minimality Rule

Project files are declarative state. They may contain identity, goals, product
rows, thresholds, constraints, refs, and human-approved boundaries.

Project files must not contain algorithms, ordered workflow steps, fallback
procedures, review procedures, learning procedures, or repeated agent
instructions. Extract that behavior into skills, hooks, validators, or ticket
programs where it can be tested.

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
  hooks.json
  skills/
    README.md
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
products, goals, and automation prompts live in the project files below.

### `farplane/harness.md`

Static human charter: mission, human thesis, operating principles,
non-tradeoffs, static leverage commitments, allocation guardrails, agent
authority, and change rule.

This file is the one owner for the durable human thesis. Products and goals may
evolve from evidence, but agents must not silently rewrite `harness.md`.
Interval reports may propose harness deltas; applying them requires explicit
human approval.

Use YAML front matter plus Markdown sections and stable tables. Do not put a
fenced `harness-program` DSL block in canonical project harness files. Product
pipelines belong in `products.md`, current strategy belongs in `goals.md`, and
automation prompts belong in `automations.md`.

### `farplane/goals.md`

Project strategy context: north star, value function, KPI axes, current bets,
current milestone, and holds. This file may evolve through evidence-backed
goals deltas, but it must stay inside the static charter in
`farplane/harness.md`. Horizon and Goal Advisor procedures live in their skills,
not in this file.

### `farplane/products.md`

Project product catalog: team identity, product rows, work-lane weights, and
constraints. Products are not chores. Interval planners consume this data;
the planning/refill procedure lives in `interval-update`.

Use Markdown with YAML front matter and the standard headings `Team`,
`Products`, `Work Lanes`, and `Constraints`.

### `farplane/automations.md`

Human-reviewable Codex automation prompt source. It stores the exact Pulse,
Daily Interval, and Weekly Interval prompt blocks copied into the Codex app
automation records.

Skills stay generic and parameterized. Prompts here should configure cadence,
project root, thread IDs, and project-specific extensions only. Generic loop
behavior belongs in `pulse-update` and `interval-update`.

### `farplane/bindings.md`

Non-secret project coordinates: URLs, handles, safe IDs, labels, aliases,
database names, dashboard links, and notification channel labels. Do not store
secrets or credentials here.

### `farplane/hooks.json`

Declarative Farplane-native hook configuration. It may contain thresholds,
enabled flags, and hook-specific refs. Hook algorithms and post-action behavior
belong in hook scripts or skills.

### `farplane/skills/`

Project-local product skills. Use this for monetizable or company-specific
workflows derived from `farplane/products.md`, such as
`farplane/skills/<product-skill>/SKILL.md`.

These local skills are referenced by tickets, interval reports, or automation
prompts by path. Promote a local product skill to root `skills/` only after
repeated runs show that it is reusable across projects.

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
`farplane/project.md`, product-catalog headings, hooks JSON shape, bindings
front matter, and obvious secret leakage.
