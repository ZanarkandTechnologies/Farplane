---
name: batch-work
description: Work across several similar tickets or skill updates in one bounded pass when the operator wants progress without one-ticket-at-a-time confirmation. Use for low-to-medium-risk batches with shared rules, clear validation, and reversible edits; avoid for fragile migrations or ambiguous architecture.
tier: 2
source: local
---

# Batch Work

Use this when the operator explicitly wants a bulk pass instead of a fragile
one-ticket-at-a-time loop.

## Job

1. Identify the shared rule across the batch.
2. Pick a bounded set of targets.
3. Classify which targets are safe to batch and which must stay single-lane.
4. Apply the same pattern across the safe targets.
5. Run one batch-level validation suite.
6. Report completed targets, skipped targets, blockers, and the next batch.

## Use When

- The user says to work in batch, bulk, or across several tickets/skills.
- The targets share a simple invariant or checklist pattern.
- The user will be away and wants meaningful progress without repeated
  confirmation.
- Work is reversible and has a deterministic validation command.

## Do Not Use When

- The work is destructive, publish/deploy/spend-bearing, or irreversible.
- Each target needs a different architecture decision.
- A migration could corrupt data or break production.
- The validation story is unknown.

## Workflow

1. Read the project files, tickets, docs, and skill surfaces that define the
   batch rule.
2. Use [reference-grounding](../reference-grounding/SKILL.md) to verify the
   local baseline and avoid inventing missing context.
3. Use [advise](../advise/SKILL.md) when deciding whether to batch, split, or
   defer targets.
4. Make a small target table:
   - `do now`
   - `skip/defer`
   - `needs single-ticket pass`
5. Edit only the `do now` targets and keep each target's local pattern intact.
6. Run the batch proof command and any target-specific checks.
7. Use [review](../review/SKILL.md) before claiming the batch is ready.

## Decision Branches

- **Same pattern, low risk:** batch up to the natural validation boundary.
- **Same family, mixed risk:** batch the low-risk targets and defer fragile
  targets.
- **Different patterns:** split into smaller batches.
- **Unclear proof:** stop before edits and define validation first.

## Outcome Contract

Return or write:

- batch rule
- target table
- changed targets
- skipped targets and why
- validation commands and results
- remaining follow-up ticket or next batch
