---
title: Project Files
status: draft
owner: harness
created_at: 2026-06-15
updated_at: 2026-06-17
framework_template_version: "0.1.0"
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

Use this rule:

```text
farplane/   = tracked project framework config
.farplane/  = ignored local runtime state, cache, reports, and logs
docs/       = tracked human-readable project memory and durable narrative
tickets/    = visible work queue
skills/     = tracked reusable project or repo skills
.codex/     = installed user/runtime Codex state outside the repo
```

The dot matters.
Do not put canonical project config in `.farplane/` unless the project has
changed `.gitignore` on purpose.

## Why This Shape

Farplane project files exist so an agent can understand the project from durable
filesystem state instead of transcript memory.

- `AGENTS.md` is the always-loaded operating policy. Keep it short and
  navigational so every loop gets the current repo rules without swallowing the
  whole project history.
- `PROJECT_RULES.md` owns stack-specific runtime commands, QA commands,
  services, ports, environment assumptions, and local conventions. This keeps
  executable project facts out of chat and out of generic skills.
- `ARCHITECTURE.md` gives software projects one top-level map for modules,
  data, boundaries, and runtime shape.
- `farplane/manifest.json` records which Farplane project spec this repo
  instantiated and which standard files should be tracked or ignored.
- `farplane/*.md` files carry tracked project config: harness identity, goals,
  automations, bindings, eval policy, and optional PM thread grouping.
- `.farplane/` carries ignored local runtime state such as reports, logs, eval
  runs, and continuation ledgers. It is useful to agents, but it is not the
  canonical project contract.
- `docs/` carries durable human-readable memory: specs, history, lessons,
  troubles, taste, and other long-lived narrative.
- `tickets/` carries executable work state. Tickets are the shared task memory,
  proof target, and handoff surface for implementation.
- `qa/` carries reusable proof shortcuts, deep links, seed/reset paths, and
  cookbook entries so user-visible checks are not rediscovered from scratch.
- Optional `.githooks/` and repo-local `scripts/` make quality gates visible
  without silently mutating local git config.

Skills such as `deep-init-project` should create or update this shape, not
explain it at length. The rationale belongs here so the project spec can evolve
without bloating first-load skill instructions.

## Tracked Framework Config

Recommended folder:

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

Create the files when they have real content.
Deep init creates the standard set by default; use `harness_depth=none` only
for substrate-only migrations.
Do not expand a tiny project beyond the template until it has real content.

Validate the convention with:

```bash
python3 bin/validators/check_farplane_project_files.py
```

### `farplane/manifest.json`

The versioned Farplane project spec manifest for this project instance.

Use JSON because the primary job is simple validation: for this framework
version, which paths are standard, and should they be pushed or ignored?

```json
{
  "schema": "farplane_project",
  "spec_version": "1.1.0",
  "standard": {
    "tracked": ["AGENTS.md", "PROJECT_RULES.md", "farplane/manifest.json"],
    "ignored": [".farplane/state/run-ledger.json"]
  },
  "optional": {
    "tracked": ["farplane/pm.json"],
    "ignored": [".farplane/reviews/"]
  }
}
```

Keep this file concise. It is not a changelog. When the framework shape changes,
bump `spec_version`, archive the old manifest snapshot in the framework docs or
release notes, and make the current manifest describe only the current standard.
Put semantics, examples, and migration guidance in this doc or
`farplane/README.md`.

### `farplane/harness.md`

The project constitution and operating model:

- mission
- values and non-tradeoffs
- modes such as business, lab, channel, academy, product, or internal ops
- feedback loops
- systems and skill bindings by name
- project-level operating principles

Use this for stable project identity and why the harness exists.

### `farplane/goals.md`

The goal portfolio:

- north star
- current milestone
- KPIs
- strategy axes
- holds and stop conditions
- Goal Advisor handoffs

Use this for values -> goals -> KPIs -> current milestone.
Do not make ticket microtasks the default goal structure.

### `farplane/automations.md`

The automation manifest:

- schedules
- live automation IDs
- grouped jobs
- ticket source policy
- Notion use policy
- report paths
- run ledger path
- side-effect gates

Use this because it can compile into live Codex automation TOML prompts.
This file should be isolated from the broader harness so the scheduler layer
can read the automation program without inheriting every strategic note.

### `farplane/bindings.md`

The non-secret project binding manifest.

Skills define reusable capabilities such as `posthog_metrics`,
`notion_task_source`, `github_repo_context`, or `telegram_notify`.
`farplane/bindings.md` gives those skills the project-specific coordinates
they need:

- Notion project/page/database aliases
- GitHub repo mapping
- analytics project identifiers and dashboard links
- deploy/project links such as Vercel project URLs
- auth/provider tenant aliases such as WorkOS org or app labels
- notification channel labels
- safe data-source names

Use bindings for IDs, URLs, labels, aliases, and lookup handles that are safe
to track.
Do not store API keys, access tokens, passwords, raw private credentials, or
anything that grants account access.
Those belong in the user's secure runtime environment.

When a binding is missing, create a ticket to add the binding or build the
skill that can fetch it.
Do not turn a missing binding into a vague markdown blocker.

### `farplane/evals.md`

Project-level eval and QA policy:

- end-to-end eval scenarios
- smoke checks
- acceptance examples
- regression cases
- proof paths
- review rubrics or links to rubrics

Use `.farplane/evals/runs/` for generated eval outputs.
Keep the eval definitions tracked in `farplane/evals.md`.

### `farplane/pm.json`

Optional project PM thread manifest for Farplane UI.

Shape:

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

Use `threads.chats` for ordinary Codex chat thread IDs and
`threads.automations` for Codex automation thread IDs. Farplane UI folds the
listed IDs into one visual project PM without merging transcripts.

Missing file means legacy UI behavior. Empty arrays are valid while the project
has no PM thread IDs to group.

## Local Runtime State

Recommended ignored folder:

```text
.farplane/
  state/
    run-ledger.json
  reports/
    <job>/latest.md
    <job>/runs/YYYY-MM-DD.md
  evals/
    runs/
  logs/
```

Use `.farplane/` for generated state that helps agents continue work but should
not become the canonical project contract.

## Durable Project Memory

Keep these in `docs/`, not `.farplane/`:

```text
docs/MEMORY.md
docs/HISTORY.md
docs/TROUBLES.md
docs/LESSONS.md
```

They are project memory, not runtime cache.
They should be reviewable and portable with the project.

## Tickets

Keep tickets in `tickets/`.

Tickets are the visible work queue and should remain outside `.farplane/`.
The ticket drainer reads local tickets first, then optional external sources
only when `farplane/automations.md` enables them.

## Skills And Agents

Use repo-owned `skills/` for reusable project skills that should travel with
the repo.
Use installed `~/.codex/skills/` only as the user's runtime installation
surface.

Use `AGENTS.md` for Codex operating policy loaded every loop.
Do not bury durable project strategy or recurring automation config inside
`AGENTS.md`.

## Recommended Minimal Project

For a small project, start with:

```text
AGENTS.md
README.md
docs/MEMORY.md
docs/HISTORY.md
docs/TROUBLES.md
docs/LESSONS.md
tickets/
farplane/README.md
farplane/harness.md
farplane/goals.md
farplane/automations.md
farplane/bindings.md
farplane/evals.md
farplane/pm.json
.farplane/state/run-ledger.json
```
