# Agent Testability Plan

## Purpose

`agent-testability-plan` turns a reusable `System Design Brief` into an
`Agent Testability Brief` that explains what an agent will need to observe,
control, coordinate, and prove the system effectively before ticketization or
per-ticket planning.

## Public Entrypoints

- `SKILL.md` - live planning contract
- `references/review.md` - brief-tightening checklist
- `AGENTS.md` - maintenance rules and boundaries

## Minimal Example

```text
$agent-testability-plan docs/specs/my-system.md
```

## How To Test

- Re-read `SKILL.md` once and confirm the boundary with
  `deep-system-design`, `spec-to-ticket`, and `impl-plan` is obvious.
- Confirm the output contract covers control accelerators, state probes,
  coordination views, tooling/infra, proof surfaces, non-goals, and decision
  boundaries.
- Confirm the skill stays planning-only and points concrete helper
  implementations to later tickets.
