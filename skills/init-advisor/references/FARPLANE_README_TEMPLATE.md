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
lives in files: `harness.md` is the static human charter and capability map,
while `goals.yaml` owns current value direction, goals, KPI IDs, milestone, and
holds. Reusable and project-local skills own recurring workflows.

```text
farplane/
  README.md        # this index
  manifest.json    # versioned Farplane project spec for this project
  harness.md       # static human charter
  goals.yaml       # north star, KPIs, current milestone, holds
  metrics.yaml     # provider-independent metric definitions
  automations.toml # one Work Pulse heartbeat plus separate scheduled jobs
  bindings.yaml      # non-secret project IDs, URLs, labels, aliases
  hooks.json       # declarative Farplane-native hook configuration
  pm.json          # optional UI thread manifest for one visual project PM

.agents/
  skills/          # project-local capability skills
    README.md
```

Runtime state lives under `.farplane/` and is intentionally ignored by git.

```text
.farplane/
  README.md
  automation/
  metrics/daily/
  reports/
  evals/runs/
  logs/
```

Keep canonical project config in `farplane/`. Use `.farplane/` only for
owner-named local state, generated reports, metric observations, evals, logs,
and continuation ledgers. Store QA and review evidence under the owning ticket;
do not add generic runtime, evidence, or review buckets.
