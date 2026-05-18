---
name: agent-testability-plan
version: 0.1.0
description: "Post-system-design planning skill that turns a System Design Brief into an Agent Testability Brief covering control accelerators, state probes, coordination views, tooling, and proof surfaces before ticketization or per-ticket build planning."
tier: 3
group: coding
source: local
argument-hint: "<system design brief, spec path, or active ticket>"
allowed-tools: Read, Glob, Grep
---

# Agent Testability Plan

Use this after `deep-system-design` and before `spec-to-ticket` or
`impl-plan`.

## Purpose

This skill answers one question:

What does the agent need in order to operate, debug, and verify the designed
system effectively?

It turns a `System Design Brief` into a reusable `Agent Testability Brief`
covering:

- `Control Accelerators`
- `State Probes`
- `Coordination Views`
- `Tooling / Infra`
- `Proof Surfaces`
- `Autonomy Readiness`

## Use When

- a `System Design Brief` already exists, but future tickets would still have
  to guess how the agent should reach hard states, inspect hidden state, or
  understand multi-part execution
- the user asks what utilities, instrumentation, shortcuts, HUDs, dashboards,
  or helper scripts the agent should create for itself
- the system includes canvas/game/simulation behavior, hidden runtime state, or
  multi-job / multi-service coordination
- `spec-to-ticket` or `impl-plan` would otherwise have to invent testability
  doctrine ad hoc

## Do Not Use When

- architecture is still vague; use `deep-system-design`
- the request is already a concrete file/symbol implementation task
- the work is only a per-ticket execution plan with no broader agent-UX or
  testability question
- you are being asked to build the actual helper/runtime surface right now

## First-Load Contract

### Trigger Conditions

- a reusable `System Design Brief` is available on a visible spec/ticket
  surface
- the system will be hard for an agent to reach, inspect, or coordinate without
  extra surfaces
- future tickets should inherit testability expectations instead of discovering
  them after QA friction

### Workflow

1. Read the `System Design Brief`, active ticket/spec, and the smallest nearby
   code/docs needed to understand the system class.
2. Map agent friction across:
   - state reachability
   - hidden-state visibility
   - multi-part coordination visibility
   - proof/evidence difficulty
3. Derive the smallest useful surfaces in six buckets:
   - `Control Accelerators`
   - `State Probes`
   - `Coordination Views`
   - `Tooling / Infra`
   - `Proof Surfaces`
4. Add `Autonomy Readiness`: inputs/assets, permissions, credentials, compute,
   missing tools, hard-to-QA surfaces, and human gates that must be known before
   unattended execution.
5. Set explicit `Non-Goals` and `Decision Boundaries`, especially the existing
   no-autonomous publish/deploy/spend boundary.
6. Write a visible `Agent Testability Brief` to:
   - `docs/specs/<slug>-agent-testability.md` when the brief is spec-level and reusable
   - otherwise the active ticket when the guidance is ticket-local
7. Add consumer guidance for `spec-to-ticket`, `impl-plan`, and `$ralph` so later planning
   surfaces know how to use the brief.
8. Read [references/review.md](references/review.md) and tighten the output
   before handoff. When an active ticket exists, point the workflow at the
   shared `review` skill for the final plan/spec challenge pass.

### Core Decision Branches

- **Canvas / game / simulation**
  - bias toward `Control Accelerators` and `State Probes`
  - examples: pause/step, seeded scenarios, camera presets, debug HUDs,
    overlays, position timelines
- **Distributed jobs / cloud / worker trees**
  - bias toward `Coordination Views` plus correlated evidence surfaces
  - examples: job dashboards, run trees, failure summaries, correlated logs
- **Conventional CRUD / form / route-driven apps**
  - bias toward the cheapest useful hooks only
  - examples: deep links, fixture loaders, seed/reset commands, DOM/state
    mirrors, simple sanity scripts
- **Already testable systems**
  - the brief may say existing surfaces are sufficient; do not invent ceremony

### Top 3 Gotchas

1. Do not reinvent the system design. This skill consumes the `System Design
   Brief`; it does not replace it.
2. Do not jump straight to stack-specific implementations when a reusable
   surface category is enough.
3. Do not turn the brief into a runtime execution layer. This skill plans
   surfaces; later tickets build them.

### Outcome Contract

The output must include:

1. `System Input`
2. `Friction Map`
3. `Control Accelerators`
4. `State Probes`
5. `Coordination Views`
6. `Tooling / Infra`
7. `Proof Surfaces`
8. `Autonomy Readiness`
9. `Non-Goals`
10. `Decision Boundaries`
11. `Consumer Guidance`
12. `Follow-Up Candidates` when the brief exposes implementation-sized deltas

## Core Question Families

Ask and answer these directly in the brief:

1. **Reachability**
   - which important states are too slow or flaky for an agent to reach by
     replaying the whole app manually?
2. **Hidden State**
   - which runtime facts are currently invisible and need direct probes, HUDs,
     overlays, logs, mirrors, or snapshots?
3. **Coordination**
   - where do multiple jobs, workers, services, or nested runs need one
     summary/dashboard surface?
4. **Proof**
   - what deterministic proof surfaces should later tickets and QA require?
5. **Boundaries**
   - what should stay out of scope, and what autonomy limits still apply?
6. **Autonomy Readiness**
   - what must be provided or approved before an agent can run the work
     unattended without blocking mid-implementation?

## Output Shape

Keep the brief compact and directly reusable.

```markdown
# Agent Testability Brief: <system>

## System Input
- source brief:
- system class:

## Friction Map
- reachability:
- hidden state:
- coordination:
- proof risk:

## Control Accelerators
- ...

## State Probes
- ...

## Coordination Views
- ...

## Tooling / Infra
- ...

## Proof Surfaces
- ...

## Autonomy Readiness
- human inputs/assets:
- permissions/credentials:
- external services:
- compute/runtime needs:
- tooling gaps:
- QA risks:
- human gates:
- agent decision boundaries:

## Non-Goals
- ...

## Decision Boundaries
- ...

## Consumer Guidance
- spec-to-ticket:
- impl-plan:
- ralph:
- qa/debugging:

## Follow-Up Candidates
- ...
```

## Handoff Rules

- `spec-to-ticket` should preserve the brief in ticket `Agent Contract`,
  `Test hook`, `Stabilize`, `Inspect`, and `Expected artifacts` fields when
  relevant.
- `impl-plan` should preserve the brief in proof and testability planning
  rather than re-deriving it from scratch.
- `$ralph` should stop before selecting risky tickets whose readiness fields do
  not name required inputs, permissions, compute, QA surfaces, and human gates.
- `qa-tester`, `visual-qa`, and `runtime-debugging` should treat the resulting
  surfaces as expected proof/testability aids, not last-minute inventions.

## References

- [references/review.md](references/review.md)
- [docs/specs/agent-testability-surfaces.md](/Users/kenjipcx/coding-harness/Codexter/docs/specs/agent-testability-surfaces.md)
- [skills/deep-system-design/SKILL.md](/Users/kenjipcx/coding-harness/Codexter/skills/deep-system-design/SKILL.md)
- [skills/spec-to-ticket/SKILL.md](/Users/kenjipcx/coding-harness/Codexter/skills/spec-to-ticket/SKILL.md)
- [skills/impl-plan/SKILL.md](/Users/kenjipcx/coding-harness/Codexter/skills/impl-plan/SKILL.md)
