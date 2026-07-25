---
title: "Generated graph runtime migration"
status: accepted
owner: skill-maintenance
created_at: 2026-07-25
updated_at: 2026-07-25
tags:
  - generated-artifacts
  - graph
  - git-hygiene
refs:
  - skills/skill-maintenance/graph/README.md
  - skills/skill-maintenance/scripts/graph_projection_config.py
  - .farplane/generated/graphs/
---

# Generated Graph Runtime Migration

## Decision

Keep the authored viewer shell under `skills/skill-maintenance/graph/`, but
write all regenerable JSON and JavaScript graph payloads to ignored
`.farplane/generated/graphs/`.

## Delta

- Before: twelve generated graph files were tracked beside the viewer and every
  refresh produced thousands of noisy Git lines.
- After: one shared projection root owns generated payloads; generators,
  runtime readers, tests, docs, and the viewer resolve that root.
- Example: `skill-graph.json` now regenerates at
  `.farplane/generated/graphs/skill-graph.json`, while
  `skills/skill-maintenance/graph/index.html` remains tracked.

## Proof

- All six prior JSON payloads were regenerated at the new root before tracked
  snapshots were removed.
- Projection stale checks passed for skill registry, harness reference,
  framework core, and lifecycle core.
- Generator and runtime-reader unit tests passed.
- `check_skills.py --write`, document-reference validation, runtime rollout
  scan, harness-health compilation, and `git diff --check` passed.
- The viewer's two JavaScript asset paths resolve to files at the runtime root.

## Boundary

Historical audits retain the graph paths that existed when their evidence was
captured. The generated docs-reference report remains tracked because it is a
review artifact, not viewer runtime data.
