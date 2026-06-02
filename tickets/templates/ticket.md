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

## Plan
- `Change:` what is changing
- `Why:` why this ticket exists now
- `First-principles basis:` objective, user/system need, assumptions, root
  cause, constraints, first viable slice, proof/falsification, tradeoff
  accepted, and non-goals when material
- `Before -> After:`
- `Touch:` files expected to change
- `Inspect:` nearby files/docs checked to ground the plan
- `Signature delta:` added/changed seams in `file / symbol(input): output` form
- `Type Sketch:` compact named structs/types for the data crossing boundaries
  or changing shape; include only the fields that matter
- `Typed flow example:` one golden-path dry run showing a representative
  payload/object evolving through the main stages when typed data flow matters
- `Execution steps:` ordered implementation steps with concrete verbs
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

## Proof Contract
<!-- Modular boundary: tickets carry proof handles and TAS gates; review and autoresearch skills carry execution logic. -->
- Required for material, agentically hard, ticketed build, or review-sensitive
  work. For trivial or judgment-only changes, keep it compact and write
  `Metrics: none mechanical` instead of inventing fake numbers.
- `Metrics:`
  - `Primary metric:` numeric or boolean result to track, or `none mechanical`
  - `Direction:` `higher`, `lower`, `pass/fail`, or `none`
  - `Verify:` command, fixture, script, manual check, or `none`
  - `Guard:` correctness command or `none`
  - `Min acceptable result:` threshold, TAS gate, or `none`
  - `Autoresearch warranted:` `yes` when repeated metric experiments should run, otherwise `no`
  - `Autoresearch session:` path to `autoresearch.md` when present, otherwise `none`
- `Review Rubrics:`
  - caller-declared rubric families and TAS gates, for example
    `evidence-quality: TAS-A`
  - hard gates, especially `evidence-quality` and `integration-readiness` when
    relevant
  - for material review, fill the reviewer handoff rather than leaving rubric
    routing for the reviewer to infer
- `Reviewer Handoff:`
  - `task_path:` this ticket path
  - `review_focus:` planning, implementation, skill-change, prompt-change,
    eval-change, docs, evidence, demo, video, or completion
  - `changed_files:` expected file or diff scope
  - `evidence:` proof artifacts, command outputs, QA reports, screenshots,
    traces, or logs
  - `rubric_families:` caller-owned rubric routing; see
    `skills/review/references/reviewer-handoff.md`
  - `required_tas:` required family gates, especially hard gates
  - `hard_gates:` task-specific constraints that force revise/block
  - `expected_output:` review artifact path when durable proof is required
- `Required Evidence:`
  - artifacts, command outputs, QA reports, review JSON, screenshots, traces, or logs needed before completion

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

## Autonomy Readiness
- Optional for trivial/manual tickets. Required when the ticket may run under
  `$ralph`, unattended loops, external services, hard-to-QA UI/motion/canvas,
  async jobs, deploy/spend/destructive boundaries, or long-running work.
- `Human inputs/assets:`
- `Credentials / external access:`
- `Compute/runtime needs:`
- `Tooling gaps:`
- `QA risks:`
- `Human gates:`
- `Agent decision boundaries:`

## Execution Profile Hints
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

## Evidence Checklist
- Optional for non-UI work. Keep it short and concrete for UI-bearing or
  agentically hard tickets.
- [ ] Screenshot:
- [ ] Screenshot:
- [ ] Snapshot:
- [ ] QA report linked:

## Refs
- Optional durable links only: specs, docs, issues, websites, or comparable
  examples
- This is the canonical place for linked docs. Do not mirror them in
  frontmatter.
- Do not store raw `session_id` values in ticket frontmatter.

## Evidence
- Store screenshots, logs, exported review JSON, and clips under
  `tickets/TASK-XXXX/artifacts/` and link them here.
  For build/documenting completion paths, also link the visible completion
  receipt artifact here when Stop hook requested one.
- Keep detailed proof here. `last_verification` in frontmatter should stay a
  one-line current verdict, not a second evidence section.
- `Artifacts:`
- `Commands:`
- `Result summary:`

## Blockers
- none
