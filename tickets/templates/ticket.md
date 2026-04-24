---
ticket_id: TASK-XXXX
title: short title
phase: planning
status: review
owner: unassigned
claimed_by:
priority: medium
depends_on: []
blocked_by: []
ready: false
approval_required: true
requires_qa: true
requires_demo: false
created_at: 2026-04-03T00:00:00Z
updated_at: 2026-04-03T00:00:00Z
next_action: define the one current step and keep it in this field
last_verification: none
linked_docs: []
---

# TASK-XXXX: title

## Summary
2-3 sentences on what changes and why it matters now.

## Scope
- In:
- Out:

## Plan
- `Change:` what is changing
- `Why:` why this ticket exists now
- `Before -> After:`
- `Touch:` files expected to change
- `Inspect:` nearby files/docs checked to ground the plan
- `Signature delta:` added/changed seams in `file / symbol(input): output` form
- `Type Sketch:` compact named structs/types for the data crossing boundaries
  or changing shape; include only the fields that matter
- `Typed flow example:` one golden-path dry run showing a representative
  payload/object evolving through the main stages when typed data flow matters
- `Recommendation:` chosen path when a material decision exists
- `Options considered:` 3 viable options only when the user did not already
  provide a take on a material choice
- `Blast radius:` callers, systems, or workflows most likely to feel the change
- `Risks:` main breakage modes or edge cases

## Gap Analysis
- Required for missing, partial, parity-driven, or product-shaping feature work.
  Optional for tightly scoped bug fixes, internal refactors, or obvious
  one-surface changes.
- `Current state:` what exists today and where it stops
- `Production expectation:` what a credible production app usually includes for
  this feature
- `Missing gaps:` behaviors, UX states, edge cases, permissions, data flows,
  observability, or operational surfaces still absent
- `Comparable implementations:` products, repos, docs, or standards inspected
- `Recommendation:` what this ticket should land now vs defer into follow-ups

## Diagram
- Optional for narrow localized fixes. Use it for material, cross-module, or
  ambiguous work when the flow, ownership, or typed data path is not obvious
  from the file map and signatures.
```mermaid
flowchart LR
  %% Keep this compact. Prefer one top-level delta map when it adds clarity.
```

## Acceptance Criteria
- [ ] AC-1

## Verification
- `Tests:` what should pass
- `Manual checks:` any direct checks that matter
- `Evidence required:` strongest artifacts needed to show the work is done
- `Artifacts path:` `tickets/artifacts/TASK-XXXX/`

## Agent Contract
- Optional for non-UI work. Add when the ticket changes UI, canvas rendering,
  user-visible flows, browser interaction, or any flow that is hard for agents
  to reach or inspect reliably.
- `Open:` launch path or command, plus stable route/deeplink if available
- `Test hook:` cheapest deterministic proof surface, or `none needed`
- `Stabilize:` reset/seed path plus shortcuts/debug controls if determinism matters
- `Inspect:` selectors, overlays, DOM mirrors, HUDs, or logs the agent should rely on
- `Key screens/states:` important surfaces QA must reach and compare
- `QA cookbook:` matching `qa/cookbook/<workflow>.md` path when the repo keeps
  reusable QA workflows, otherwise `none yet`
- `Taste refs:` relevant visual doctrine and any local exception
- `Expected artifacts:` screenshots, snapshots, traces, reports, or clips
- `Delegate with:` ticket path/section, recommended assignee, expected artifact

## Evidence Checklist
- Optional for non-UI work. Keep it short and concrete for UI-bearing or
  agentically hard tickets.
- [ ] Screenshot:
- [ ] Screenshot:
- [ ] Snapshot:
- [ ] QA report linked:

## Refs
- Optional links only: specs, docs, issues, websites, or comparable examples
- Do not store raw `session_id` values in ticket frontmatter.

## Evidence
- Store screenshots, logs, exported review JSON, and clips under
  `tickets/artifacts/TASK-XXXX/` and link them here.
- `Artifacts:`
- `Commands:`
- `Result summary:`

## Blockers
- none
