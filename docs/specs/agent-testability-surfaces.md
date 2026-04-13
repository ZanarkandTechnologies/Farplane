# Agent Testability Surfaces

Date: 2026-04-13

## Goal

Define the post-system-design planning surface that decides what an agent will
need in order to build, debug, and verify a system effectively before later
ticketization or per-ticket planning begins.

This is not the runtime implementation layer.
It is the doctrine and artifact shape that later tickets should consume.

## Pipeline Position

- input: `System Design Brief` from `deep-system-design`
- planning step: `agent-testability-plan`
- output: visible `Agent Testability Brief`
- downstream consumers:
  - `spec-to-ticket`
  - `impl-plan`
  - `qa-tester`
  - `visual-qa`
  - `runtime-debugging`

Use this step when the agent would otherwise struggle to:

- reach the right state quickly
- inspect hidden runtime state directly
- understand many moving parts in one place

## Core Buckets

### 1. Control Accelerators

Surfaces that help the agent reach or replay the important state faster.

Examples:

- deep links
- scenario loaders
- seed/reset commands
- pause/resume/step
- camera presets
- stable shortcuts

### 2. State Probes

Surfaces that make hidden runtime state directly inspectable.

Examples:

- debug HUDs
- overlays
- DOM/state mirrors
- object IDs and counters
- event timelines
- sampled logs or snapshots

### 3. Coordination Views

Surfaces that summarize multi-part execution in one place.

Examples:

- job dashboards
- worker trees
- retry/failure summaries
- correlated log/status views
- nested run or pipeline summaries

## Agent Testability Brief Contract

The resulting brief should include:

1. `System Input`
2. `Friction Map`
3. `Control Accelerators`
4. `State Probes`
5. `Coordination Views`
6. `Tooling / Infra`
7. `Proof Surfaces`
8. `Non-Goals`
9. `Decision Boundaries`
10. `Consumer Guidance`
11. `Follow-Up Candidates`

## Consumer Rules

### `spec-to-ticket`

- turn the brief into concrete `Agent Contract`, `Test hook`, `Stabilize`,
  `Inspect`, and `Expected artifacts` fields when relevant
- make missing testability work explicit in tickets instead of leaving QA to
  improvise later

### `impl-plan`

- preserve the brief in the proof path and execution plan
- do not reinvent testability doctrine when the brief already exists

### QA and Debugging

- treat the brief as expected instrumentation/testability guidance
- do not wait until the end of QA to discover every missing shortcut, HUD, or
  coordination surface from scratch

## Non-Goals

- not a hosted observability platform
- not a generic permission expansion mechanism
- not a vendor- or domain-specific adapter library
- not a replacement for `deep-system-design`, `spec-to-ticket`, or `impl-plan`

## Current Bet

The first useful win is planning discipline:

- ask what the agent needs
- write it down visibly
- feed that into future tickets and plans

Concrete helper implementations, dashboards, and instrumentation libraries
belong in later build tickets once the doctrine proves useful.
