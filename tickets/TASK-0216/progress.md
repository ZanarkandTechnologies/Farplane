---
ticket_id: TASK-0216
title: "Progress: Shared GraphIR and Configurable Projections"
status: draft
owner: codex
created_at: 2026-06-24T11:00:33+0800
updated_at: 2026-06-24T11:00:33+0800
refs:
  - ticket.md
  - program.md
---

# Progress

## 2026-06-24T11:00:33+0800 - Impl Plan

- Created implementation plan for a shared GraphIR plus named graph projection
  configs.
- Grounded against existing graph scripts:
  - `generate_skill_graph.py`
  - `generate_harness_graph.py`
  - `farplane_lifecycle_graph.py`
  - `docs/farplane-framework/graph-contract.md`
  - `skills/skill-maintenance/graph/README.md`
- Decision: build skill, harness, and lifecycle graphs as sibling projections
  from one GraphIR rather than making lifecycle a child projection of the
  current skill graph.
- State: awaiting approval before implementation.

## Evidence Log

- `python3 -m py_compile ...graph scripts...`: pass.
- `PYTHONPATH=skills/skill-maintenance/scripts python3 -m unittest skills/skill-maintenance/scripts/test_generate_farplane_lifecycle_graph.py`: pass, 12 tests.
- `generate_graph_projection.py --projection <profile>` temp generation:
  - `skill-registry`: 97 nodes, 313 edges, 97 skill docs.
  - `harness-reference`: 873 nodes, 3587 edges.
  - `farplane-lifecycle-core`: 90 nodes, 171 edges, 4 FSA projections.
  - `farplane-lifecycle-full`: 284 nodes, 343 edges, 4 FSA projections.
- Wrapper-vs-dispatcher normalized JSON comparison:
  - `skill-graph.json`: OK.
  - `skill-docs.json`: OK.
  - `harness-graph.json`: OK.
  - `lifecycle.json`: OK.
- `generate_farplane_lifecycle_graph.py --out <missing> --js-out <missing> --check`: pass as negative test; exits `1`.
- `python3 bin/validators/check_doc_refs.py`: pass, 1159 refs checked.
- `python3 tickets/scripts/check_ticket_metadata.py`: pass, 19 ticket files checked.
- `git diff --check`: pass.
- On-disk generated artifact freshness:
  - `skill-registry --check`: pass, 97 nodes / 313 edges.
  - `farplane-lifecycle-core --check`: pass, 90 nodes / 171 edges.
  - `harness-reference --check`: fails because existing
    `harness-graph.json/js` are stale in the current dirty worktree; not
    regenerated in this ticket to avoid sweeping unrelated active changes into
    the GraphIR commit.

## 2026-06-24T11:00:33+0800 - Review And Fixes

- Reviewer first pass returned `TAS-C` because the first implementation used
  shared emit/timestamp helpers and a dispatcher, but not enough real GraphIR.
- Fixes applied:
  - Skill, harness, and lifecycle builders now emit through shared
    `GraphNode`, `GraphEdge`, and `GraphBundle` primitives.
  - The dispatcher applies `project_graph()` for every named profile.
  - Lifecycle `--check` now fails when requested JSON/JS outputs are missing.
  - Docs remain accurate: named profiles are Python configs and existing graph
    paths remain compatibility outputs.
- Second reviewer pass: `TAS-A`, no blocking findings, rerun not required.

## 2026-06-24T11:00:33+0800 - Closeout

- Ticket moved to `phase: complete`, `status: done`.
- Commit prep uses scoped staging because the working tree has unrelated active
  interval/automation changes. The staged GraphIR commit preserves the current
  committed lifecycle wording while leaving the working-tree interval changes
  untouched.
