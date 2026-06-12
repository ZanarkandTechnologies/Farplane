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

## Map

Use one Mermaid delta map when the work is material, cross-module, or easier to
understand visually. Put changed signatures and typed flow in the map when that
keeps the plan clearer.

- `Touch:`
- `Inspect:`
- `Legend:` keep | change | add | remove

```mermaid
flowchart LR
  %% Prefer one compact visual before/after map.
  %% Put inline signatures in nodes or edges when seams matter.
  %% Number typed-flow edges when payload/state movement matters.
```

Optional fallback detail when the map would become crowded:

- `Signature delta:` `module / symbol(input): output`
- `Type sketch:` `TypeName { field: Type }`
- `Typed flow:` one representative object or payload path

## Program

```text
signature:
  task(input, state?) -> artifact + evidence + state_delta

vars:
  target =
  owner =

program:
  ground(vars) -> current_state
  change(current_state) -> artifact_delta
  verify(done_when, proof) -> evidence
```

Include `Recommendation:` only when it changes the build path. Include
`Options considered:` only when there is a real material fork.

## Done / Proof

```text
done_when:
  -

proof:
  checks:
    -
  manual:
    -
  review:
    - rubric: none
      required_tas: none
  evidence:
    -
```

## State

- `next_action:`
- `blocked:`
- `latest_verification:`

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
testability or human gate in `Done / Proof`.
