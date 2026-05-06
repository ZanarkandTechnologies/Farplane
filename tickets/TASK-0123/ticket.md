---
ticket_id: TASK-0123
title: add board adapter conformance scaffolding
phase: planning
status: review
owner: codex
claimed_by:
priority: medium
depends_on:
  - TASK-0120
blocked_by: []
ready: false
approval_required: true
requires_qa: false
requires_demo: false
created_at: 2026-05-06T17:18:41Z
updated_at: 2026-05-06T17:18:41Z
next_action: review the adapter conformance scaffolding plan
last_verification: planned on 2026-05-06 to keep future board adapters easy to add
---

# TASK-0123: add board adapter conformance scaffolding

## Summary
Add lightweight conformance scaffolding for future Linear, Notion, GitHub, or
custom board adapters without implementing those adapters now. The goal is to
make every future adapter prove it can normalize one work item, preserve
readiness/invocation semantics, and write evidence traceably.

## Scope
- In:
  - Add a board-adapter conformance reference or fixture suite.
  - Define required adapter behaviors in code-adjacent terms:
    `list_candidates`, `read_work_item`, `write_evidence`, and normalization.
  - Keep filesystem adapter as the only live implementation.
  - Add sample raw payload fixtures for future shared-board adapters if useful.
  - Ensure conformance language says adapters store/read work; they do not
    decide when work starts.
- Out:
  - No Linear adapter.
  - No Notion adapter.
  - No external writeback implementation.
  - No webhooks or polling.

## Plan
- `Change:` Add adapter conformance docs/tests that future adapters must reuse.
- `Why:` Symphony gave us useful adapter-shaped thinking. We should preserve
  the extension seam without building unused integrations.
- `Before -> After:`
  - Before: `FileTicketAdapter` works, and specs describe a future adapter
    contract, but future adapters do not have a concrete checklist or fixture
    shape.
  - After: future adapters have a small conformance target that protects
    `WorkItem`, readiness, compute target, and evidence semantics.
- `Touch:`
  - `docs/specs/board-adapter-conformance.md`
  - `docs/specs/README.md`
  - `docs/specs/board-compute-orchestration.md`
  - `bin/codexter_boards.py` only for docstrings or exported fixture helpers
    if needed.
  - `bin/test_codexter_boards.py`
  - `tickets/README.md`
- `Inspect:`
  - `bin/codexter_boards.py`
  - `bin/test_codexter_boards.py`
  - `bin/codexter_invocation.py`
  - `docs/specs/symphony-compatible-codexter-runner.md`
  - `tickets/scripts/check_ticket_metadata.py`
- `Signature delta:`
  - optional `bin/test_codexter_boards.py / assert_work_item_contract(item): None`
  - optional `docs/specs/board-adapter-conformance.md / Adapter Checklist`
  - no `LinearAdapter` or `NotionAdapter` class in this ticket.
- `Type Sketch:`
  - `AdapterConformanceCase`:
    - `raw`: source-specific payload or ticket markdown
    - `expectedWorkItem`: normalized id, title, readiness, blockers, deps,
      compute target, path/url
    - `writeExpectation`: manual, unsupported, or traceable write result
  - `WorkItem`: existing canonical normalized shape.
- `Typed flow example:`
  1. A future Notion adapter receives one page payload.
  2. Conformance fixture expects `identifier`, `title`, `ready`,
     `approvalRequired`, `dependsOn`, and `computeTarget`.
  3. Adapter returns `WorkItem`.
  4. Codexter invocation uses the same `ComputeSelector` and skill routing as
     filesystem tickets.
  5. Evidence writeback returns a traceable result or explicit manual block.
- `Execution steps:`
  1. Add conformance doc with required behaviors and non-goals.
  2. Extract a small reusable assertion helper in board tests only if it reduces
     duplication.
  3. Add one filesystem conformance test that documents the adapter baseline.
  4. Link conformance doc from specs index and board-compute spec.
  5. Run board/invocation tests, metadata, doc parity, and harness invariants.
- `Recommendation:` Add conformance scaffolding after the mental-model reset,
  before any real shared-board adapter ticket.
- `Options considered:`
  - Implement Linear/Notion now: too early and likely to overfit.
  - Keep contract prose only: low effort, but weak future regression protection.
  - Add conformance scaffolding: recommended; small, durable, and adapter-ready.
- `Blast radius:` future adapter tickets, board adapter tests, specs index.
- `Risks:`
  - Over-specifying future adapters before seeing real payloads. Containment:
    keep conformance focused on normalized output and non-goals.
  - Adding test abstraction too early. Containment: extract helpers only if
    they simplify current filesystem tests.

## Gap Analysis
- `Current state:` filesystem adapter exists and future adapters are described
  in specs.
- `Production expectation:` a pluggable adapter interface needs conformance
  tests or fixtures before multiple implementations exist.
- `Missing gaps:` no adapter checklist, no future fixture shape, no explicit
  writeback semantics beyond filesystem manual mode.
- `Comparable implementations:` Symphony's normalized issue model, Codexter's
  `WorkItem`, existing filesystem adapter tests.
- `Recommendation:` ship the conformance scaffold, not an adapter.

## Acceptance Criteria
- [ ] A board-adapter conformance doc or fixture exists.
- [ ] Filesystem adapter is covered by the conformance shape.
- [ ] Future adapters are told to normalize into `WorkItem` and preserve
  explicit invocation semantics.
- [ ] No external adapter, webhook, polling, or writeback implementation ships.

## Verification
- `Tests:`
  - `python3 -m unittest bin/test_codexter_boards.py`
  - `python3 -m unittest bin/test_codexter_invocation.py`
  - `python3 tickets/scripts/check_ticket_metadata.py`
  - `python3 bin/check_doc_parity.py`
  - `python3 bin/check_harness_invariants.py`
- `Manual checks:`
  - Review conformance doc against `docs/specs/board-compute-orchestration.md`
    and `tickets/README.md`.
- `Evidence required:`
  - Review artifact confirming no real external adapter was introduced.

## Autonomy Readiness
- `Human inputs/assets:` approval of conformance-first adapter strategy.
- `Credentials / external access:` none.
- `Compute/runtime needs:` local tests only.
- `Tooling gaps:` none.
- `QA risks:` adapter conformance could become abstract fluff; keep it tied to
  filesystem tests.
- `Human gates:` approval required.
- `Agent decision boundaries:` may write docs/tests; may not add live external
  adapters or network calls.

## Refs
- [BoardAdapter helper](/Users/kenjipcx/coding-harness/Codexter/bin/codexter_boards.py)
- [board-compute orchestration](/Users/kenjipcx/coding-harness/Codexter/docs/specs/board-compute-orchestration.md)
- [tickets README](/Users/kenjipcx/coding-harness/Codexter/tickets/README.md)

## Evidence
- `Artifacts:`
  - [next-batch plan review](/Users/kenjipcx/coding-harness/Codexter/tickets/TASK-0120/artifacts/review/2026-05-06-next-batch-plan-review.json)
- `Commands:`
  - `python3 tickets/scripts/check_ticket_metadata.py`
  - `git diff --check -- tickets/TASK-0120/ticket.md tickets/TASK-0121/ticket.md tickets/TASK-0122/ticket.md tickets/TASK-0123/ticket.md`
  - `python3 skills/ralph/scripts/select_next_ticket.py --root . --json`
- `Result summary:`
  - Planning ticket created and approval-gated; depends on the terminology reset in `TASK-0120`.

## Blockers
- awaiting approval
