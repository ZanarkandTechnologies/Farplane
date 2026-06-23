---
title: Ticket Reflection And Proof Surface Council Context
status: draft
owner: codex
created_at: 2026-06-22
decision_type: deliberative-advice
---

# Ticket Reflection And Proof Surface Council Context

## Decision

Should Farplane add ticket-local `decisions.md`, store reflection/decisions in
`progress.md`, put them in `program.md`, or avoid new files and keep one log?
Should proof move into each ticket directory by default?

## Why This Matters

The operator wants Farplane to be leaner and less glue-heavy. A ticket already
acts like a mini isolated workspace. Native Goals need a place to log observed
progress and reflect on decisions, but too many sidecar files can make the
system feel heavier than the work.

## Prior Discussion Summary

Current concerns:

- `FarplaneRunEnvelope`, `WorkItem`, `ComputeDecision`, and similar objects
  feel like overlapping glue around things a ticket or goal already knows.
- Proof should probably live inside each ticket rather than in global result
  locations.
- Decision packets might be stored in ticket frontmatter, `decisions.md`,
  `progress.md`, or `program.md`.
- Native Goals should log reflection somewhere.
- The operator prefers the minimum number of surfaces that still preserve
  memory, decisions, proof, and resumability.

## Current Behavior

Current repo contracts say:

- Active work lives at `tickets/TASK-*/ticket.md`.
- Ticket directories may include optional `program.md`, optional `progress.md`,
  and `artifacts/`.
- `ticket.md` owns objective, scope, acceptance criteria, proof scoreboard,
  blockers, current next action, and links.
- `program.md` owns loop configuration for material native Goal work.
- `progress.md` owns append-only observed execution: timestamp, trigger,
  intent, actions, changed files, evidence, metric/feedback sample, drift
  verdict, next action, blocker/stop reason.
- Ticket-scoped `artifacts/` already exists and is used for review, QA, proof,
  images, evals, prompts, and reports.
- The current docs warn not to put long chronological logs or bulky evidence in
  `ticket.md`.

Observed ticket examples show many active tickets with:

- `program.md`
- `progress.md`
- `artifacts/review`
- `artifacts/qa`
- `artifacts/proof.md`
- ticket-scoped eval/proof folders

No `decisions.md` appears in the current active ticket scan.

## Expected Behavior

The chosen policy should:

- keep ticket workspaces easy to inspect;
- keep Native Goal reflection reconstructable;
- avoid duplicated state between `ticket.md`, `program.md`, `progress.md`, and
  artifacts;
- make proof easy to find;
- avoid frontmatter bloat;
- preserve enough structure for future UI rendering;
- avoid creating empty boilerplate files for every ticket.

## Options Under Consideration

### Option A: One Ticket Log

Use `progress.md` for progress, reflection, decision entries, evidence links,
and completion notes. Do not add `decisions.md` by default.

### Option B: Split Decisions From Progress

Use `progress.md` as chronological log and add `decisions.md` only when a
ticket has material branching decisions or council notes.

### Option C: Put Decisions In `program.md`

Use `program.md` for run config plus decision/reflection notes because it is
already part of the Goal Packet.

### Option D: Put Decisions In Frontmatter

Store decision records or refs in ticket frontmatter for machine parsing.

## Evidence Refs

- `tickets/README.md`
- `docs/specs/goal-loop-contract.md`
- active ticket scan showing many `program.md`, `progress.md`, and
  `artifacts/` directories, but no `decisions.md`

## Relevant Files

- `tickets/README.md`
- `docs/specs/goal-loop-contract.md`
- `tickets/templates/goal-loop/program.md`
- `tickets/templates/goal-loop/progress.md`

## Constraints / Non-Goals

- Do not implement the policy during this council pass.
- Do not invent mandatory boilerplate files for every ticket unless the benefit
  clearly outweighs overhead.
- Do not put raw transcript in tracked logs.
- Do not make `program.md` a second ticket or second progress log.
- Do not put bulky decision text in frontmatter.
- Keep proof ticket-local where practical.

## Lane Briefs

### Operator Value

Judge what makes tickets easiest to understand, resume, and trust.

### Engineering Risk

Judge file sprawl, validators, migration, merge conflicts, archival, and UI
projection risk.

### Evidence Skeptic

Judge what current repo behavior actually supports and what is still only
intuition.

### Systems Fit

Judge ownership boundaries among `ticket.md`, `program.md`, `progress.md`,
`artifacts/`, and optional `decisions.md`.

### Native Goal Fit

Judge what Native Goal needs for reflection, drift checks, after-turn logging,
and completion proof.

## Output Shape

Each lane should return:

- `Perspective`
- `Recommendation`
- `Strongest reason`
- `Biggest risk`
- `Strongest opposing point`
- `Evidence that would change my mind`
- `Concrete policy constraints`

Chair synthesis should compare exactly three final options and recommend one.

## Proof / Next Owner

Likely next owner is a ticket/spec cleanup that updates `tickets/README.md`,
`docs/specs/goal-loop-contract.md`, and templates to clarify:

- proof belongs under `tickets/TASK-XXXX/artifacts/` by default;
- `progress.md` is the default reflection/log surface;
- `decisions.md` is optional and only for material branching decisions;
- frontmatter carries refs/status only.
