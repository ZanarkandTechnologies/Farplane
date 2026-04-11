# Impl Plan Template

## Pitch

- `Req:`
- `Bet:`
- `Win:`

## Recommendation

- `Best:`
- `Why:`
- `Tradeoff accepted:`

## Diagram Summary

- `Required:` yes for material or cross-module work; optional for trivial localized fixes
- `Legend:` keep | change | add | remove

```mermaid
flowchart LR
  %% Tier 1: top-level delta map
  %% Put short signatures in nodes when the interface or ownership boundary matters.
```

- `Tier 2:` optional zoom-in only when the top-level map is not enough

## B -> A

- `Before:`
- `After:`
- `Outcome:`

## Delta

- `Touch:`
- `Keep:`
- `Change:`
- `Delete/Avoid:`

## Core Flow

```mermaid
flowchart LR
  %% Prefer a numbered critical-path data-flow diagram for material work.
```

```pseudo
input/request
-> inspect current path
-> decide split or single-commit
-> apply minimal delta
-> persist/render/return
-> verify proof points
```

## Proof

- `P1:`
- `P2:`
- `Risk:`
- `Rollback:`

## User Story

- `Actor:`
- `Need:`
- `Outcome:`

## User Pain / JTBD

- `Current pain:`
- `Why now:`

## Non-Goals

- `Do not solve:`

## High-Fidelity Example

- `Example flow/artifact:`

## What Good Looks Like

- `Quality bar:`

## Proof Target

- `Reviewer-visible proof:`

## Plan Review

- `Refs:` prd/spec/ticket/memory/troubles/code
- `Scope:` pass / fix
- `Proof:` pass / fix
- `Guardrails:` pass / fix
- `Recommendation:` pass / fix
- `Fixes:` none / short note

## Options Appendix

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

## Delegation

- `Need:` `Not needed` / skill / subagent
- `Why:`
- `Artifact:`

## Ask

- `Ready:` yes / no
- `Next:`
- `If split:`

## Optional Appendix

- use only for risky, novel, or cross-cutting details

## Applicability Rule

- Required for material feature work, workflow/tooling changes, ambiguous
  implementation work, and any ticket where desired behavior would otherwise be
  inferred.
- May be short or omitted for trivial, narrowly localized fixes where the code
  context already anchors the expected behavior.
