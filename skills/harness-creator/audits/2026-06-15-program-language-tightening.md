---
kind: skill-audit
skill: harness-creator
status: complete
created_at: 2026-06-15
---

# Harness Creator Program Language Tightening

## Decision

`harness-creator` now treats the Harness Program as the compact source of
truth for project/business operating design.

The active language changes are:

- `values { ... }` is a first-class block with `mission`,
  `operating_principles`, `priorities`, and `non_tradeoffs`.
- `priorities` replaces `goal_weights` in signatures and notation.
- `milestone` replaces `frontier` for the selected executable branch.
- `hourly_task_update` and `update_system_gaps` replace drain-style function
  names.
- Human access, setup, approval, and data blockers are represented as
  `ticket { type: unblock }` nodes.
- External systems stay expressible as `skill` capabilities with `requires`
  inputs; no new top-level external-IO abstraction was added.

## Rationale

The skill should produce one compact program-like artifact that can explain how
an agentic project or small business runs. Values need to be durable operating
constraints, not just weights beside goals. Human blockers need to become
tickets so the project remains executable instead of accumulating Markdown
notes.

## Proof Targets

- Active examples use `values { ... }`.
- Shared notation spec uses `priorities`, `milestone`, and update-function
  vocabulary.
- Harness template proposes unblock tickets rather than sidecar blocker lists.
