# Impl Plan Template

## Human

### Decision

- `Req:`
- `Best:`
- `Why:`
- `Tradeoff accepted:`
- `Not chosen:`

### Diagram

- `Required:` yes for material or cross-module work; optional for trivial
  localized fixes
- `Legend:` keep | change | add | remove

```mermaid
flowchart LR
  %% Tier 1: top-level delta map
  %% Put short signatures in nodes when the interface or ownership boundary matters.
```

- `Tier 2:` optional zoom-in or numbered data flow only when Tier 1 is not
  enough

### Signature Sketch

- `Format:` `module / symbol(input): output`
- `Use:` 3-7 seams that prove codebase understanding
- `Avoid:` full type dumps

### B -> A

- `Before:`
- `After:`
- `Outcome:`

### Proof

- `P1:`
- `P2:`
- `Risk:`
- `Rollback:`

### Ask

- `Ready:` yes / no
- `Next:`
- `If split:`

## Agent

### Delta

- `Touch:`
- `Keep:`
- `Change:`
- `Delete/Avoid:`

### Execution Plan

```mermaid
flowchart LR
  %% Prefer a numbered critical-path data-flow diagram for material work.
```

```pseudo
inspect current path
name the real seams
apply minimal delta
verify proof points
update ticket move
```

### Risk / Rollback

- `Primary risk:`
- `Containment:`
- `Rollback:`

### User Story

- `Actor:`
- `Need:`
- `Outcome:`

### User Pain / JTBD

- `Current pain:`
- `Why now:`

### Non-Goals

- `Do not solve:`

### High-Fidelity Example

- `Example flow/artifact:`

### What Good Looks Like

- `Quality bar:`

### Proof Target

- `Reviewer-visible proof:`

### Plan Review

- `Refs:` prd/spec/ticket/memory/troubles/code
- `Checks:` scope / proof / guardrails / diagram / signatures / rollback
- `Fixes:` none / short note

### Options Appendix

- `Option 1:`
- `Pros:`
- `Cons:`
- `Why not chosen:`
- `Option 2:`
- `Pros:`
- `Cons:`
- `Why not chosen:`
- `Option 3:`
- `Pros:`
- `Cons:`
- `Why not chosen:`

### Delegation

- `Need:` `Not needed` / skill / subagent
- `Why:`
- `Artifact:`

### Ticket Move

- `Now:`
- `On approval:`
- `Follow-ups:`
- `Blocked in building?:`

## Optional Appendix

- use only for risky, novel, or cross-cutting details

## Applicability Rule

- `Human` comes first.
- `Diagram` plus `Signature Sketch` are required for material feature work,
  workflow/tooling changes, ambiguous implementation work, and any ticket where
  trust depends on seeing changed components or interfaces.
- Narrative sections may be short or omitted for trivial, narrowly localized
  fixes where the code context already anchors the expected behavior.
