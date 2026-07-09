---
kind: farplane-config-index
status: draft
created_at: TODO
updated_at: TODO
framework_template_version: "0.2.0"
---

# Farplane Config

Tracked project framework config lives here.

`manifest.json` owns the compact UI identity card. Richer project meaning
lives in files: `harness.md` is the static human charter,
`products/<product>/product.md` files are canonical product-loop definitions,
generated `products.json` is the machine/UI product index, and `goals.yaml` is
current cross-product strategy.

```text
farplane/
  README.md        # this index
  manifest.json    # versioned Farplane project spec for this project
  harness.md       # static human charter
  goals.yaml       # north star, KPIs, current milestone, holds
  products/
    core/product.md # canonical starter product-loop definition
    core/skill.md   # project-local product workflow
  products.json    # generated machine/UI product index
  automations.toml # full Codex automation configs for Pulse and Intervals
  bindings.yaml      # non-secret project IDs, URLs, labels, aliases
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
