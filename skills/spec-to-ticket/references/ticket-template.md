# Ticket Template Reference

Use the canonical template at `tickets/templates/ticket.md` when creating
filesystem tickets. This reference summarizes the expected body shape for
`spec-to-ticket`.

## Body Shape

````markdown
# TASK-XXXX: title

## Summary
2-3 sentences on what changes and why now.

## Scope
- In:
- Out:

## Delta
- `Before:`
- `After:`
- `Why now:`
- `First-principles basis:`

## Program
```text
signature:
  task(input, state?) -> artifact + evidence + state_delta

vars:
  target =

program:
  ground(vars) -> current_state
  change(current_state) -> artifact_delta
  verify(done_when, proof) -> evidence
```

## Map
- `Touch:`
- `Inspect:`
- `Signature delta:`
- `Type Sketch:`
- `Typed flow example:`

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
- Sparse blast radius, risk, rollback, citations, blockers, or follow-up
  boundaries only.
````

## Optional Sections

- `Gap Analysis` for missing, partial, parity-driven, or product-shaping work.
- `Agent Contract` for UI-bearing, browser-driven, canvas/game, or otherwise
  agentically hard work.
- `Run Hints` for `$work`, `$ralph`, batch, external compute, or unattended
  execution.
- `Goal Packet` when native Goal mode, heartbeat, rollout, skill improvement,
  or human-feedback optimization is required.

## Planning Checklist

- Each ticket file is independently implementable.
- Dependencies are explicit and acyclic.
- `Scope` prevents overbuild and underbuild.
- `Delta` makes before/after behavior and first principles obvious.
- `Program` names variables, operations, and outputs in readable pseudocode.
- `Map` carries touched files, inspected files, callable seams, typed examples,
  and a compact diagram when useful.
- `Done / Proof` collapses done conditions, checks, review gates, and evidence
  obligations without duplicating old acceptance/verification/proof sections.
- UI-bearing tickets define how agents open, inspect, verify, and delegate from
  the ticket artifact.
- Tickets use `none mechanical` when a metric would be fake.
