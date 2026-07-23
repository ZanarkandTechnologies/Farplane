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
lives in files: `harness.yaml` is the typed charter, descriptive-product and
capability map, and active metric selection. `metrics.yaml` owns reusable
metric meaning, direction, freshness, and guard rules. Reusable and
project-local skills own recurring workflows.

```text
farplane/
  README.md        # this index
  manifest.json    # versioned Farplane project spec for this project
  harness.yaml     # typed charter, planning areas, capability refs, metric selection
  metrics.yaml     # metric definitions, direction, freshness, guard rules
  automations.toml # one Work Pulse heartbeat plus separate scheduled jobs
  bindings.yaml      # non-secret project IDs, URLs, labels, aliases
  pm.json          # optional UI thread manifest for one visual project PM

.agents/
  skills/          # project-local capability skills
    README.md
```

Runtime state lives under `.farplane/` and is intentionally ignored by git.

```text
.farplane/
  README.md
  views.yaml
  entities/
  automation/
  metrics/daily/
  reports/
  evals/runs/
  logs/
```

Keep shared canonical project config in `farplane/`. The ignored
`.farplane/entities/*.md` and `.farplane/views.yaml` files are explicit
authored local exceptions for private entity memory and named membership.
Other `.farplane/` paths hold owner-named local state, generated reports,
metric observations, evals, logs, and continuation ledgers. Store QA and review
evidence under the owning ticket; do not add generic runtime, evidence, review,
or config buckets.
