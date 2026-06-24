---
kind: farplane-config-index
status: draft
created_at: TODO
updated_at: TODO
framework_template_version: "0.2.0"
---

# Farplane Config

Tracked project framework config lives here.

```text
farplane/
  README.md        # this index
  manifest.json    # versioned Farplane project spec for this project
  harness.md       # mission, values, modes, systems, feedback loops
  goals.md         # north star, KPIs, current milestone, holds
  automations.md   # exact Codex automation prompt blocks for Pulse and Intervals
  bindings.md      # non-secret project IDs, URLs, labels, aliases
  evals.md         # project-level proof and eval policy
  pm.json          # optional UI thread manifest for one visual project PM
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
