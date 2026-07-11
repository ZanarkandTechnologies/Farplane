---
template_id: ticket-template
template_version: "0.1.9"
feature_refs:
  - FEAT-0007
  - FEAT-0008
ticket_id: TASK-0323
title: consolidate ticket validation behind one phase-aware API
phase: complete
status: done
owner: codex
claimed_by:
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
requires_qa: true
requires_demo: false
human_gate: none
created_at: 2026-07-11T21:00:00+08:00
updated_at: 2026-07-11T21:50:00+08:00
next_action: none
last_verification: phase-aware completion selected eight check families and passed; QA pass and reviewer TAS-A
---

# TASK-0323: consolidate ticket validation behind one phase-aware API

## Summary

Give agents one `farplane validate ticket` command that selects pure,
allowlisted Farplane-wide and skill-local checks by target phase and explicit
changed-path boundary, then writes one deterministic receipt.

## Scope

- In: shared validation models/selection/runner/receipts, consolidated
  Farplane check registry, planning and completion phases, CLI, rules, tests,
  Git-runner reuse where safe, lifecycle documentation, and modular commits.
- In: preserve skill-specific validators under their owning skills.
- Out: no arbitrary shell evaluation, worktree-wide implicit path inference,
  write/install/API/credential/repair/hardcase side effects, or reviewer/QA
  judgment inside validators.
- Out: do not overwrite concurrent TASK-0321/TASK-0322 changes; defer physical
  deletion of an actively modified legacy wrapper when isolation is unsafe.

## Delta

```text
before: agents select many validator scripts and receive fragmented output.
after: one phase-aware ticket API selects modular pure checks and writes one receipt.
tradeoff: owner-local implementations remain multiple files behind one interface.
```

## Change Plan

```text
architecture_signatures:
  - validate_ticket(ticket, target_phase, path_boundary) -> ValidationReceipt
  - select_checks(phase, paths, ticket_state) -> ordered check IDs
  - run_checks(checks, context) -> CheckResult[]
  - write_receipt(receipt, ticket/artifacts/validation) -> JSON + Markdown
builder_freeform_boundary:
  - helper extraction and formatting may change without weakening purity,
    deterministic path provenance, or owner-local skill validation.
```

### Change 1: Shared validation kernel

```text
read: bin/validators/run_git_gate.py, rules/git-review-gates.toml
write: bin/core/validation/*
operation: add typed models, selection, execution, and receipt primitives
qa: unit tests for deterministic selection, ordering, failures, and receipts
failure_modes: implicit dirty-worktree scope; mutation; nondeterministic output
```

### Change 2: Farplane checks and CLI

```text
read: bin/validators/*, tickets/scripts/check_ticket_metadata.py
write: bin/validators/farplane_checks.py, bin/farplane.py, rules/validation.toml
operation: register phase/path check families and expose farplane validate ticket
qa: planning and completion CLI integration tests
failure_modes: duplicate suites; unsafe commands; missing path provenance
```

### Change 3: Lifecycle integration and migration

```text
read: impl-plan, goal-advisor, qa, close-ticket, git gates
write: owner contracts and compatibility routing only where isolated
operation: make the one API the phase-boundary command and preserve post-close gate
qa: old-vs-new check selection and independent completion review
failure_modes: closure gate runs too early; skill validators move to wrong owner
```

## Done

- One command validates planning and completion phases.
- No new ticket metadata fields are introduced.
- Changed paths require explicit provenance and appear in receipts.
- Only allowlisted pure checks execute.
- Skill-specific validators remain skill-local.
- Tests cover missing boundary, failure aggregation, mutation bans, and receipts.
- Independent QA and reviewer gates pass.
- Work is split into modular commits without unrelated worktree changes.

## QA Strategy

```text
proof_weight: tests + CLI integration + reviewer
checks:
  - python3 -m unittest bin.tests.test_ticket_validation
  - python3 -m unittest bin.validators.test_farplane_checks
  - python3 bin/validators/check_doc_refs.py
delegated_lanes:
  - qa-tester
  - reviewer
final_checkpoint: QA evidence and reviewer TAS-A before completion
residual_risk: legacy wrapper deletion deferred where concurrent modifications overlap
```

## Docs Strategy

```text
outcome: update_docs
targets:
  - bin/README.md
  - tickets/archive/TASK-0323/artifacts/design/validation-system-consolidation.md
validation: doc reference check
```

## Links

- Audit: `tickets/archive/TASK-0323/artifacts/design/validation-system-consolidation.md`
- Visual companion: `tickets/archive/TASK-0323/diagrams.md`
- QA: `tickets/archive/TASK-0323/artifacts/qa/20260711T132041Z-ticket-validation-authority-final/result.json`
- Completion review: `tickets/archive/TASK-0323/artifacts/review/completion-review.md`
- Validation receipt: `tickets/archive/TASK-0323/artifacts/validation/complete.json`

## Notes

- Accepted plan: one public API, modular owner-local validators, no schema expansion.
- Commit 1: `bf99ef1c feat(validation): add phase-aware ticket validation`.
- Commit 2: `1fae2f45 fix(impl-plan): require separate validated diagrams`.
- Commit 3: `d74d0cda refactor(validation): route lifecycle through ticket API`.
