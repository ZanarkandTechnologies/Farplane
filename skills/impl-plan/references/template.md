# Impl Plan Template

## Summary
2-3 sentences on the recommended before/after change, why it matters now, and
the decisive path.

## Scope

- `In:`
- `Out:`

## Delta

- `Before:`
- `After:`
- `Why now:`
- `First-principles basis:` objective, need, assumptions, root cause,
  constraints, first viable slice, proof/falsification, tradeoff, and non-goals
  when material

## Change Plan

Use change units as the merged implementation program and file map. Group by
coherent fix, not by artifact type. Each unit should carry the local
before/after, read/write files, operation, local type or signature impact,
routes, and QA expectations so builders do not cross-map separate sections.
For material plans, start with compact architecture signatures so reviewers can
scan the top-level code shape before reading change-unit detail:

```text
architecture_signatures:
  module_level:
    - path_or_module / owner_seam(input): output
  main_flow:
    - function_or_handler(input): output
  data_flow:
    - source.field -> boundary.field -> result.field
  builder_freeform_boundary:
    - Implementation below this level is builder-owned unless it changes
      ownership, public contracts, data flow, proof, or reviewability.
```

For tiny localized fixes, use:

```text
architecture_signatures: not_applicable - localized same-surface fix because <reason>
```

Repeat one heading and fenced block per coherent change:

### Change 1: short label

```text
fixes:
  - plain-language problem or delta this change resolves
before:
  -
after:
  -
read:
  - path:
    reason:
write:
  - path:
    change:
operation:
  -
signature_or_type_impact:
  -
routes:
  docs: doc-advisor | no_docs
  qa: tests | qa-tester | visual-qa | agent-qa-test | none
  review: reviewer | inline | none
qa:
  -
failure_modes:
  -
```

Include `Recommendation:` only when it changes the build path. Include
`Options considered:` only when there is a real material fork.
Use `signature_or_type_impact` for local deltas inside the change unit; do not
duplicate the full `architecture_signatures` map in every unit.

Optional visual system map only when topology, ownership boundaries, or typed
flow are easier to understand as a diagram:

```mermaid
flowchart LR
  %% Optional. Omit for localized tickets.
```

## Done

```text
done_when:
  -
```

## QA Strategy

```text
qa_strategy:
  proof_weight: smoke | tests | qa | visual_qa | review | agent_qa | demo
  checks:
    -
  manual:
    -
  delegated_lanes:
    -
  review:
    - rubric: none
      required_tas: none
  evidence:
    -
  goal_advisor_inputs:
    proof_route:
    final_evidence:
    final_checkpoint:
  residual_risk:
    -
```

## Docs Strategy

```text
docs_strategy:
  outcome: update_docs | no_docs
  doc_targets:
    -
  no_docs_reason:
  validation:
    -
```

Use `doc-advisor` to decide whether durable docs change. Use `update_docs` when
README, feature/system specs, runbooks, templates, public guidance, or other
durable docs need edits. Use `no_docs` only with a concrete reason, such as
internal-only implementation, generated-only output, test fixture changes, or
proof that no public/canonical/workflow-facing surface changed.

## Links

- `program:`
- `progress:`
- `artifacts:`
- `review:`
- `refs:`

## Notes

- `Blast radius:`
- `Risks / rollback:`
- `Follow-ups:`
- `Citations:` inline or compact references only when they ground a claim or decision
- `Blockers:` omit when none

## Gap Analysis

- `Required:` only for missing, partial, parity-driven, or product-shaping
  feature work
- `Current state:`
- `Production expectation:`
- `Missing gaps:`
- `Comparable implementations:`
- `Recommendation:`

## Run Hints

Use only when the ticket is intended for `$ralph`, unattended work, external
services, hard-to-QA UI/motion/simulation, or deploy/spend/destructive
boundaries. Otherwise keep readiness in the spec or ticket and reflect only the
testability or human gate in `QA Strategy`.
