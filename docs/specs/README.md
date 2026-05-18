# Specs

Canonical harness and product specs live here once ideas move past exploration.

Top-level companion docs:

- [`ARCHITECTURE.md`](/Users/kenjipcx/coding-harness/Codexter/ARCHITECTURE.md) - top-level system map and canonical surface guide
- [`README.md`](/Users/kenjipcx/coding-harness/Codexter/README.md) - product/setup story and public entrypoints

Documentation ownership:

- `README.md` is the public documentation router.
- `ARCHITECTURE.md` owns the whole-system diagram and surface ownership map.
- this file indexes canonical specs and the doc-gardening loop.
- `tickets/README.md` owns ticket metadata, lifecycle, and invocation policy.

Current design docs:

- `autoresearch-skill-suite.md` - metric-driven autoresearch planning, execution, and skill self-improvement contract
- `best-of-worlds-workflow.md` - multi-source synthesis workflow for extracting, scoring, and adapting the best transferable features
- `board-adapter-conformance.md` - fixture/checklist contract future board
  adapters must satisfy before Linear, Notion, GitHub, or custom boards become
  live work-item sources
- `board-compute-orchestration.md` - board adapter, explicit ticket
  invocation, compute selection, local Codexter, Ralph, and future
  Symphony/shared-board ownership contract
- `codexter-v2-milestone.md` - completed capped Symphony-inspired milestone for
  explicit invocation triggers, adapter conformance, and external-compute
  recipes, with explicit deferrals so Codexter does not become a daemon
- `agent-testability-surfaces.md` - post-system-design doctrine for control accelerators, state probes, coordination views, and proof surfaces
- `diagram-first-conventions.md` - canonical Mermaid-first approval-surface and delta-diagram standard
- `doc-governance.md` - structural versus narrative doc-audit policy
- `context-and-handoff-policy.md`
- `harness-engineering-doctrine.md` - routing doctrine for where harness changes belong before editing the repo
- `harness-engineering-quickstart.md`
- `harness-techniques.md` - current-state feature and technique inventory
- `orchestrator-subagent-loop.md`
- `runtime-surface.md`
- `review-gates.md`
- `skill-tier-rollout-plan.md` - planning draft for mapping local skills into
  Tier 1 primitives, Tier 2 workflow interfaces/methods, and Tier 3 application
  skills before a dedicated skill registry rollout
- `spec-first-execution-loop.md`
- `spec-authoring-contract.md` - PRD/spec/ticket layer split, spec depth
  decisions, service-runtime spec template, and conformance matrix format
- `symphony-compatible-codexter-runner.md` - invocation contract that lets a
  normal Codex session run Codexter locally now and lets Symphony invoke
  Codexter-equipped Codex later

Legacy or transitional references:

- `legacy/ralph-runtime-surface.md`
- `legacy/ralph-orchestration-blueprint.md`
- `legacy/ralph-v2-direction.md`
- `legacy/ralph-flow-examples.md`
- `legacy/ralph-run-state.schema.json`
- `legacy/ralph-judge-verdict.schema.json`

Use this folder for:

- execution model specs
- artifact and schema specs
- orchestration flow docs
- `skill` / `subagent` / `hook` stories tied to buildable system behavior
- reusable planning doctrine that later tickets and skills should consume

Keep exploratory source comparison notes and one-off research in `docs/research/`.

## Doc Gardening Loop

Run this loop when the public harness story changes:

1. Run `python3 tickets/scripts/check_ticket_metadata.py`.
2. Run `python3 bin/check_harness_invariants.py`.
3. Run `python3 bin/check_doc_parity.py`.
4. Re-read `ARCHITECTURE.md`, `README.md`, `docs/specs/README.md`, `docs/specs/harness-techniques.md`, and `tickets/README.md` against the active ticket plus `docs/MEMORY.md` / `docs/HISTORY.md`.
5. Use the `codex exec` narrative audit in `doc-governance.md` when the public story, implemented/proposed status, or canonical links changed.
6. Patch only the canonical surfaces that drifted; keep README and
   ARCHITECTURE synchronized when the whole-system map, shipped capability
   list, or roadmap cap changes.
7. Re-run `python3 tickets/scripts/check_ticket_metadata.py`, `python3 bin/check_harness_invariants.py`, and `python3 bin/check_doc_parity.py`.
