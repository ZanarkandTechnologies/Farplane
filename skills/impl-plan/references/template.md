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

## Goal Packet Preview

Include this for material Goal-backed work. This preview is compiled through
`goal-advisor` and is reviewed with the plan before native Goal execution.

```text
goal_packet:
  ticket: tickets/TASK-XXXX/ticket.md
  program: tickets/TASK-XXXX/program.md
  progress: tickets/TASK-XXXX/progress.md
  files:
    -
  budget:
  metric:
  proof_route:
  drift_policy:
  final_evidence:
  native_goal_prompt: |
    /goal ...
  approval:
    status: pending | approved | revise | blocked
    rule: approve plan and Goal Packet together before run
```

If the ticket plan changes after review, rerun `goal-advisor` and replace this
preview before asking for approval again.

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

## Documentation / Closeout

```text
docs_closeout:
  close_ticket: required
  documentation_skill: not_required | required
  docs_changed:
    -
  documentation_reason: substantive durable doc writing/revision | none
  final_writeback:
    - ticket evidence and linked docs
    - durable docs changed in final pass
    - validators/checks matched to touched surfaces
```

Use `close-ticket` for final ticket writeback and durable-doc consistency.
Use `documentation` only when the ticket itself includes substantive durable doc
writing or revision that needs reader contract, grounding, and doc-quality
checks.

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
