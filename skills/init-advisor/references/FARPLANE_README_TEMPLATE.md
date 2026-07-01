---
kind: farplane-config-index
status: draft
created_at: TODO
updated_at: TODO
framework_template_version: "0.2.0"
---

# Farplane Config

Tracked project framework config lives here.

`manifest.json` owns the compact UI identity card. Richer project meaning lives
in Markdown: `harness.md` is the static human charter, `products.md` is the
product catalog and work-lane table, `goals.md` is current strategy, and
`ops-memory.md` is active operating memory.

```text
farplane/
  README.md        # this index
  manifest.json    # versioned Farplane project spec for this project
  harness.md       # static human charter
  goals.md         # north star, KPIs, current milestone, holds
  products.md      # products and work lanes this team creates
  ops-memory.md    # active focus, projects, runway, and frontier
  automations.md   # exact Codex automation prompt blocks for Pulse and Intervals
  bindings.md      # non-secret project IDs, URLs, labels, aliases
  hooks.json       # declarative Farplane-native hook configuration
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
  automation/
  reports/
  evals/runs/
  logs/
```

Keep canonical project config in `farplane/`. Use `.farplane/` only for local
runtime state, generated evidence, reports, logs, and continuation ledgers.
