---
kind: farplane-config-index
status: active
created_at: 2026-06-15
updated_at: 2026-06-26
framework_template_version: "0.1.0"
---

# Farplane Config

Tracked project framework config lives here.

This folder is the project-local declaration that Farplane UI should be able to
summarize as one autonomous company inside the broader harness cockpit.

`manifest.json` owns the compact UI identity card. Richer project meaning lives
in Markdown: `harness.md` is the static human charter, `products.md` is the
product catalog and work-lane table, and `goals.md` is current strategy.

```text
farplane/
  README.md        # this index
  manifest.json    # versioned Farplane project spec for this project
  harness.md       # static human charter
  goals.md         # north star, KPIs, current milestone, holds
  products.md      # products and work lanes this team creates
  automations.toml # full Codex automation configs for Pulse, Intervals, and optional consolidation/Taste Loop
  bindings.yaml    # non-secret project IDs, URLs, labels, aliases, metric recipes
  hooks.json       # declarative Farplane-native hook configuration
  ops-memory.md    # flexible current operating notes and reminders
  pm.json          # optional UI thread manifest for one visual project PM

.agents/
  skills/          # project-local product skills
    README.md
```

Runtime state lives under `.farplane/` and is intentionally ignored by git.

```text
.farplane/
  README.md
  state/run-ledger.json
  state/ticket-thread-associations.jsonl
  automation/
  content/ledger.jsonl
  metrics/daily/
  metrics/observations/
  project/ui/latest.json
  reports/
  evals/runs/
  logs/
```

Farplane Core is installed once and invoked through the global `farplane` CLI.
Other projects do not copy metric scripts; they pass a project root:

```bash
farplane metrics primitives --project-root /path/to/project --date <YYYY-MM-DD> --json
farplane project snapshot --project-root /path/to/project --date <YYYY-MM-DD> --json
```

Primitive metrics are Core-owned reducers over tickets, `bindings.yaml`, local
Codex stores, and ignored Farplane runtime state. Farplane UI should render the
generated project snapshot and deep-link back to the source files; canonical
writes still belong to the tracked project files and ignored runtime ledgers.

See [docs/farplane-framework/project-files.md](../docs/farplane-framework/project-files.md).

## Official Automation Presets

- `Pulse`: drains ready tickets and records execution/reward state.
- `Daily/Weekly Interval`: reviews recent state and plans the next window.
- `Monthly Registry Consolidation`: optional report-only pass over registry
  truth, duplicate rows, owner drift, and generated-output freshness.
- `Active-Hours Taste Loop`: optional human-feedback heartbeat that runs only
  during configured active hours, ranks candidate skills with the official
  Skill Signals, and emits a feedback card or Goal Advisor
  handoff without activating hidden workers or editing target skills directly.
