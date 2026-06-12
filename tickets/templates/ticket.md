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
---

# TASK-XXXX: title

<!-- Optional frontmatter field when needed: compute_target: local_shared | local_worktree | symphony | codex_cloud -->

## Summary
2-3 sentences on what changes, why it matters now, and the decisive path being
recommended.

## Scope
- In:
- Out:

## Delta
- `Before:`
- `After:`
- `Why now:`
- `First-principles basis:`
  - `objective:`
  - `need:`
  - `assumptions:`
  - `root_cause:`
  - `constraints:`
  - `first_viable_slice:`
  - `proof_or_falsification:`
  - `tradeoff:`
  - `non_goals:`

## Program
Use this compact task program for the normal build plan. Move it to
`program.md` when the work is a native Goal, heartbeat, rollout,
skill-improvement loop, or long multi-turn task.

```text
signature:
  task(input, state?) -> artifact + evidence + state_delta

vars:
  target =
  owner =
  docs = []

program:
  ground(vars)
    -> current_state

  change(current_state)
    -> artifact_delta

  verify(done_when, proof)
    -> evidence
```

## Map
- `Touch:`
- `Inspect:`
- `Signature delta:` added/changed seams in `file / symbol(input): output` form
- `Type Sketch:` compact named structs/types for the data crossing boundaries
  or changing shape; include only the fields that matter
- `Typed flow example:` one golden-path dry run showing a representative
  payload/object evolving through the main stages when typed data flow matters
- `Diagram:` optional for narrow localized fixes. Use one compact Mermaid delta
  map for material, cross-module, or ambiguous work when it improves skim value.

```mermaid
flowchart LR
  %% Keep this compact. Prefer one top-level delta map when it adds clarity.
```

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

## Done / Proof
Collapse done conditions, tests, review gates, and required evidence here.
Move bulky command output, screenshots, review reports, and logs to
`artifacts/`, then link them from `State` or `Links`.

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

## Run Hints
- Optional for trivial/manual tickets. Add when `$work`, `$ralph`, `batch-work`,
  remote kanban, Codex Cloud, Symphony, or another unattended runner may use
  this ticket.
- These hints are advisory context, not runtime authority. Explicit invocation
  still starts work.
- `Likely size:` `tiny` | `normal` | `large` | `epic`
- `Goal recommendation:` `none` | `recommend` | `required`
- `Compute hint:` `local_shared` | `local_worktree` | `codex_cloud` |
  `symphony` | `none`
- `Planning hint:` `none` | `light` | `impl_plan` | `reslice`
- `Proof weight:` `smoke` | `tests` | `qa` | `visual_qa` | `review` |
  `demo`
- `Batchability:` `batchable` | `single-ticket` | `unknown`
- `Batch reason:` shared module/workflow/setup/proof surface, or no-batch
  reason
- `Human inputs/assets:`
- `Credentials / external access:`
- `Compute/runtime needs:`
- `Tooling gaps:`
- `QA risks:`
- `Human gates:`
- `Agent decision boundaries:`

## Goal Packet
- Required when `Goal recommendation` is `required`, and recommended for any
  material native Goal, heartbeat, rollout, skill-improvement loop, or
  human-feedback loop.
- `Goal packet:` `none` | `required` | `active`
- `Program:` `tickets/TASK-XXXX/program.md` or `none`
- `Progress:` `tickets/TASK-XXXX/progress.md` or `none`
- `Generated Goal prompt:` paste or link the current native `/goal` prompt
- `Metric provider:` `mechanical` | `review` | `agent_qa` |
  `human_feedback` | `market` | `hybrid` | `none`
- `Feedback preset:` `optimize-with-human` | `none`
- `Drift reviewer:` `goal-drift-reviewer` | `reviewer` | `inline` | `none`
- `Heartbeat:` cadence or `none`
- `Stop condition:` complete, blocked, pause, or escalation condition
- `Refs:` `docs/specs/goal-loop-contract.md`,
  `tickets/templates/goal-loop/program.md`,
  `tickets/templates/goal-loop/progress.md`

## State
- `next_action:`
- `blocked:`
- `latest_verification:`
- `result:`

## Links
- `program:` `tickets/TASK-XXXX/program.md` or `none`
- `progress:` `tickets/TASK-XXXX/progress.md` or `none`
- `artifacts:`
- `review:`
- `refs:`

## Notes
- Keep sparse: blast radius, risks, rollback, citations, blockers, or follow-up
  boundaries only.
