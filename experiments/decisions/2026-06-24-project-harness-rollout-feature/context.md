---
title: "Council Context: Project Harness Rollout Feature"
status: draft
owner: codex
created_at: 2026-06-24T00:00:00+0800
updated_at: 2026-06-24T00:00:00+0800
tags:
  - farplane
  - deliberative-advice
  - harness
  - skills
refs:
  - docs/farplane-framework/graph-contract.md
  - skills/skill-maintenance/graph/README.md
  - tickets/TASK-0216/ticket.md
---

# Council Context: Project Harness Rollout Feature

## Decision

What Farplane feature should own project-level harness development, local skill
experimentation, harness performance tracking, and rollout across many
projects?

## Why This Matters

As Farplane grows, skills and standards will mature in multiple places:

- Farplane core standards and reusable global skills.
- Team-local workflow skills, such as an AI agency's client delivery playbooks.
- Project-local harness configs, tickets, docs, memory, runtime reports, and
  experiments.

Without structure, local skills will either never promote, or every project
will copy too much Farplane machinery and drift.

## Prior Discussion Summary

- Every Farplane project can have a mini harness, but should not copy the whole
  Farplane repo.
- Farplane core should own reusable graph/schema/projection machinery.
- Projects and teams should own local skills, docs, goals, tickets, reports,
  and optional custom projections.
- Farplane Office could load a project's Farplane files and render a project
  harness graph or team-local skill graph.
- The new GraphIR projection work added named profiles for skill, harness, and
  lifecycle graphs while keeping generated artifacts stable.

## Current Behavior

- Farplane itself has graph generation under `skills/skill-maintenance/scripts/`.
- The graph contract describes sibling projections over GraphIR.
- There is no explicit feature for:
  - project-local skill lifecycle,
  - rollout/version testing across projects,
  - harness performance metrics,
  - promotion from local skill to team skill to global skill,
  - project/team graph overlays in Farplane Office.

## Expected Behavior

Farplane should make it easy to:

- initialize a project with a small local harness;
- add local or team skills without copying global Farplane internals;
- graph project-local and team-local skill behavior;
- test harness config and skill versions across projects;
- track rollout performance and proof;
- promote proven local skills into global Farplane only when warranted.

## Options Under Consideration

1. One global Farplane manifest and global harness graph only.
2. Fully self-contained per-project harness with copied skill-maintenance and
   standards.
3. Standard manifest plus per-project/team overlays: local skills, local docs,
   local projections, version pins, metrics, and promotion flow.

## Known Evidence

- `docs/farplane-framework/graph-contract.md` defines graph projections as
  UI-consumable and agent-consumable harness maps, not a runtime.
- `skills/skill-maintenance/graph/README.md` documents the shared GraphIR and
  named projection dispatcher.
- `tickets/TASK-0216/ticket.md` captured the design decision that lifecycle,
  skill, and harness graphs should be sibling projections rather than one being
  a child of another.

## Relevant Files

- `docs/farplane-framework/graph-contract.md`
- `skills/skill-maintenance/graph/README.md`
- `tickets/TASK-0216/ticket.md`
- Future owner candidates:
  - `docs/specs/*`
  - `farplane/manifest.json`
  - `skills/skill-maintenance/**`
  - `skills/deep-init-project/**`
  - Farplane Office UI

## Constraints And Non-Goals

- Do not require every project to vendor/copy all of Farplane's global skill
  maintenance machinery.
- Do not create a hidden daemon or control plane just to track rollout.
- Do not let project-local standards silently override global standards without
  visibility.
- Do not force tiny projects into heavy harness ceremony.
- Keep the model compatible with many project types: software, agency, content,
  research, internal ops.

## Lane Briefs

- `Operator value`: focus on the user's leverage, agency workflows, local skill
  experimentation, and what should feel good in Farplane Office.
- `Engineering risk`: focus on versioning, config drift, schema boundaries,
  promotion mechanics, and keeping the implementation small.
- `Evidence skeptic`: challenge whether this is proven enough, what metrics are
  missing, and what would falsify the feature.
- `Systems fit`: decide which Farplane surface should own this: manifest,
  GraphIR, skill-maintenance, deep-init, Office UI, tickets/specs, or some
  combination.

## Output Shape

Each lane should return:

- recommendation
- strongest opposing point
- evidence that would change its mind
- concrete implementation constraints

## Critique And Ranking Plan

The chair should compare exactly three final feature shapes, preserve dissent,
and recommend one with a concrete next owner and proof surface.

## Proof Or Next Owner

Likely next owner is a new ticket/spec for a "Project Harness Overlay" feature,
possibly routed through `impl-plan` after this advice.
