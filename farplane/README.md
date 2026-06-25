---
kind: farplane-config-index
status: draft
created_at: 2026-06-15
updated_at: 2026-06-15
framework_template_version: "0.1.0"
---

# Farplane Config

Tracked project framework config lives here.

This folder is the project-local declaration that Farplane UI should be able to
summarize as one autonomous company inside the broader harness cockpit.

`manifest.json` owns the compact UI identity card. Richer project meaning lives
in Markdown: `harness.md` is the static human charter, `products.md` is the
dynamic product portfolio, and `goals.md` is current strategy.

```text
farplane/
  README.md        # this index
  manifest.json    # versioned Farplane project spec for this project
  harness.md       # static human charter and compact charter-level loop
  goals.md         # north star, KPIs, current milestone, holds
  products.md      # dynamic primary and supporting products this team creates
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

See [docs/farplane-framework/project-files.md](../docs/farplane-framework/project-files.md).
