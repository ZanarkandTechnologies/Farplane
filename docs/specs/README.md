# Specs

Canonical harness and product specs live here once ideas move past exploration.

Top-level companion docs:

- [`ARCHITECTURE.md`](/Users/kenjipcx/coding-harness/Farplane/ARCHITECTURE.md) - top-level system map and canonical surface guide
- [`README.md`](/Users/kenjipcx/coding-harness/Farplane/README.md) - product/setup story and public entrypoints

Documentation ownership:

- `README.md` is the public documentation router.
- `ARCHITECTURE.md` owns the whole-system diagram and surface ownership map.
- this file indexes canonical specs and the doc-gardening loop.
- `tickets/README.md` owns ticket metadata, lifecycle, and invocation policy.

Active feature and contract specs:

- `adaptive-backoff.md` - repeated wait, retry, polling, and long-running job
  cadence policy without hidden daemons or queues
- `agent-testability-surfaces.md` - post-system-design control accelerators,
  state probes, coordination views, and proof-surface planning
- `case-based-memory-context-graph.md` - designed context graph over history,
  memory, troubles, lessons, sources, features, tickets, and skills
- `context-and-handoff-policy.md` - visible progress, reset/resume handoff,
  documenting, and archive rules for ticketed work
- `diagram-first-conventions.md` - Mermaid-first approval-surface and
  delta-diagram standard
- `doc-governance.md` - structural versus narrative doc-audit policy
- `first-principles-planning.md` - planning/spec basis for objective, need,
  assumptions, root cause, constraints, proof, tradeoffs, and non-goals
- `filesystem-lifecycle.md` - lifecycle and drain rules for ledgers, tickets,
  registries, experiments, specs, and research
- `harness-algebra.md` - canonical function model for skills, evals, hooks,
  memory drains, tickets, artifacts, composition, and optimization
- `harness-engineering-doctrine.md` - routing doctrine for where harness
  changes belong before editing the repo
- `harness-techniques.md` - current-state feature and technique inventory
- `invocation-and-adapters.md` - explicit Farplane invocation, board adapter,
  compute selection, local execution, and future external-runner contract
- `meta-harness-automation.md` - feature registry, skill registry,
  skill-maintenance, source ingestion, evals, failure capture, review, and
  durable-memory map
- `orchestrator-subagent-loop.md` - single-ticket `$impl` worker-lane and
  reviewer/QA/evidence-check orchestration model
- `review-gates.md` - ticket proof contract, QA, reviewer, and Stop-hook review
  gates
- `runtime-surface.md` - current public runtime/control surfaces and retired
  runtime boundaries
- `skill-self-healing.md` - skill failure detection and repair-ticket handoff
  pipeline
- `spec-authoring-contract.md` - PRD/spec/ticket layer split, spec depth
  decisions, service-runtime template, and conformance matrix
- `spec-first-execution-loop.md` - spec -> ticket -> plan -> build -> QA ->
  review execution model

Skill-owned contracts should live with their skills, not as separate specs.
Examples: autoresearch belongs to `skills/autoresearch-plan`,
`skills/autoresearch-exec`, and `skills/self-improve`; best-of-worlds belongs
to `skills/best-of-worlds`; skill registry/tier rollout belongs to
`docs/skills/README.md` and `skills/skill-maintenance`.

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
