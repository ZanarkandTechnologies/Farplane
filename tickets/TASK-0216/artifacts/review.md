---
ticket_id: TASK-0216
title: "Review: Shared GraphIR and Configurable Projections"
status: active
owner: reviewer
created_at: 2026-06-24T11:00:33+0800
updated_at: 2026-06-24T11:00:33+0800
refs:
  - ../ticket.md
  - ../progress.md
---

# Review

## First Pass

- `overall_tas:` TAS-C
- `verdict:` block
- `hard_gate_failures:` integration-readiness, evidence-quality

Findings:

1. `High:` the first implementation did not actually route generators through
   shared GraphIR; `GraphNode`, `GraphEdge`, `GraphBundle`, and
   `project_graph()` were mostly unused outside tests.
2. `Medium:` lifecycle wrapper `--check` silently passed when requested output
   files were missing.
3. `Medium:` docs overstated the first implementation.

## Fix Response

- Skill generator now builds registry nodes and edges through shared
  `GraphNode` and `GraphEdge`, then returns a `GraphBundle`.
- Harness generator now normalizes final node/edge output through shared
  `GraphNode` and `GraphEdge`, uses shared count helpers, then returns a
  `GraphBundle`.
- Lifecycle generator now uses shared `GraphNode`, `GraphEdge`, `GraphBundle`,
  node-kind counts, edge counts, JSON/JS helpers, and normalized comparison.
- Dispatcher now applies `project_graph()` for each named profile.
- Lifecycle `--check` now fails when requested JSON/JS outputs are missing.
- Docs describe the implemented profile system and shared GraphIR path.

## Proof After Fixes

- `python3 -m py_compile ...graph scripts...`: pass.
- `PYTHONPATH=skills/skill-maintenance/scripts python3 -m unittest skills/skill-maintenance/scripts/test_generate_farplane_lifecycle_graph.py`: pass.
- Wrapper-vs-dispatcher normalized JSON comparison: pass for skill graph,
  skill docs, harness graph, and lifecycle core.
- Temp generation for all four profiles: pass.
- `python3 bin/validators/check_doc_refs.py`: pass.
- `python3 tickets/scripts/check_ticket_metadata.py`: pass.
- `git diff --check`: pass.

## Residual Risk

The worktree contains unrelated active changes, including generated graph file
drift. `harness-reference --check` currently reports stale on-disk
`harness-graph.json/js`. This ticket did not regenerate or stage those dirty
generated files to avoid mixing unrelated active work into the GraphIR commit.

## Second Pass

- `overall_tas:` TAS-A
- `verdict:` pass
- `blocking_findings:` none
- `hard_gate_failures:` none

Resolved findings:

1. Shared GraphIR usage is now real: skill, harness, and lifecycle builders
   construct output through `GraphNode`, `GraphEdge`, and `GraphBundle`, and
   the dispatcher applies `project_graph()` for each profile.
2. Lifecycle missing-output `--check` now exits `1`.
3. Docs accurately describe the Python profile/config model without claiming a
   new runtime or skill-graph child projection.

Reviewer caveat: default lifecycle JSON includes one concrete ticket path only
as an `evidence_ref`; node IDs remain flattened to `tickets/TASK-*`, so the
flattening requirement is satisfied.
