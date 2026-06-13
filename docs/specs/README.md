# Specs

Canonical harness and product specs live here once ideas move past exploration
and become buildable behavior contracts.

Top-level companion docs:

- [`ARCHITECTURE.md`](/Users/kenjipcx/coding-harness/Farplane/ARCHITECTURE.md) - top-level system map and canonical surface guide
- [`README.md`](/Users/kenjipcx/coding-harness/Farplane/README.md) - product/setup story and public entrypoints
- [`docs/fundamentals/README.md`](../fundamentals/README.md) - harness
  theory, doctrine, and cross-surface best practices

Documentation ownership:

- `README.md` is the public documentation router.
- `ARCHITECTURE.md` owns the whole-system diagram and surface ownership map.
- this file indexes canonical specs and the doc-gardening loop.
- `docs/fundamentals/README.md` indexes conceptual foundations that are not
  themselves runtime/spec contracts.
- `tickets/README.md` owns ticket metadata, lifecycle, and invocation policy.

Canonical inventory specs:

- `harness-techniques.md` - current-state feature and technique inventory.
- `filesystem-lifecycle.md` - lifecycle and drain rules for ledgers, tickets,
  registries, experiments, specs, and research.
- `doc-governance.md` - structural versus narrative doc-audit policy.

Execution and proof specs:

- `spec-first-execution-loop.md` - spec -> ticket -> plan -> build -> QA ->
  review execution model.
- `review-gates.md` - ticket Done / Proof contract, QA, reviewer, and Stop-hook review
  gates.
- `agent-testability-surfaces.md` - post-system-design control accelerators,
  state probes, coordination views, and proof-surface planning.
- `adaptive-backoff.md` - repeated wait, retry, polling, and long-running job
  cadence policy without hidden daemons or queues.
- `goal-loop-contract.md` - Goal Packet model for native Codex Goals backed by
  tickets, `program.md`, `progress.md`, drift review, human feedback, heartbeat
  triggers, and rollout patterns.

Planning and authoring specs:

- `first-principles-planning.md` - planning/spec basis for objective, need,
  assumptions, root cause, constraints, proof, tradeoffs, and non-goals.
- `spec-authoring-contract.md` - PRD/spec/ticket layer split, spec depth
  decisions, service-runtime template, and conformance matrix.
- `context-and-handoff-policy.md` - visible progress, reset/resume handoff,
  documenting, and archive rules for ticketed work.

Invocation and runtime specs:

- `invocation-and-adapters.md` - explicit Farplane invocation, board adapter,
  compute selection, local execution, runtime surface boundaries, and future
  external-runner contract.

Product feature specs:

- `inspiration-vault.md` - skill-backed inspiration capture, LocalPinterest
  storage, Farplane UI browsing/graph/recall surface, and creative grounding
  contract.

Meta-harness specs:

- `self-improvement-contracts.md` - canonical signatures for gap analysis,
  harness advising, eval capture, skill maintenance, self-improve,
  skill self-healing, and optimize-harness workflows.

Archived or superseded specs:

- `../archive/specs/meta-harness-automation.md` - folded into
  `harness-techniques.md` and `self-improvement-contracts.md`.
- `../archive/specs/skill-self-healing.md` - folded into
  `self-improvement-contracts.md` and `docs/skills/README.md`.
- `../archive/specs/runtime-surface.md` - folded into
  `invocation-and-adapters.md`.
- `../archive/specs/orchestrator-subagent-loop.md` - folded into
  `spec-first-execution-loop.md`.
- `../archive/specs/case-based-memory-context-graph.md` - folded into
  `../fundamentals/harness-algebra.md`.

Generated audit:

- `../doc-audit/generated/doc-reference-report.md` - generated docs backlink
  and cleanup preview from
  `skills/skill-maintenance/scripts/generate_harness_graph.py`.

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
- reusable contracts that later tickets and skills should consume

Use `docs/fundamentals/` for reusable theory, doctrine, and best-practice
contracts such as harness algebra, harness placement doctrine, and prompt
engineering.

Keep exploratory source comparison notes and one-off research in ticket or
experiment artifacts. Historical research retained only for context belongs in
`docs/archive/research/`.

## Doc Gardening Loop

Run this loop when the public harness story changes:

1. Run `python3 tickets/scripts/check_ticket_metadata.py`.
2. Run `python3 bin/validators/check_harness_invariants.py`.
3. Run `python3 bin/validators/check_doc_parity.py`.
4. Run `python3 bin/validators/check_doc_refs.py`.
5. Re-read `ARCHITECTURE.md`, `README.md`, `docs/specs/README.md`, `docs/specs/harness-techniques.md`, and `tickets/README.md` against the active ticket plus `docs/MEMORY.md` / `docs/HISTORY.md`.
6. Use the `codex exec` narrative audit in `doc-governance.md` when the public story, implemented/proposed status, or canonical links changed.
7. Patch only the canonical surfaces that drifted; keep README and
   ARCHITECTURE synchronized when the whole-system map, shipped capability
   list, or roadmap cap changes.
8. Re-run `python3 tickets/scripts/check_ticket_metadata.py`, `python3 bin/validators/check_harness_invariants.py`, `python3 bin/validators/check_doc_parity.py`, and `python3 bin/validators/check_doc_refs.py`.
