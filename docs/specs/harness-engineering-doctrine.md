# Harness Engineering Doctrine

Date: 2026-04-24

## Goal

Give Codexter one canonical way to decide where a harness change belongs before
editing the repo.

This doctrine is Codexter-first. It is not a generic agent-harness manifesto.
Its job is to route a proposed change to the smallest owning surface:

- root policy
- canonical spec
- skill
- subagent
- hook
- ticket contract
- validator
- tool surface

## Core Model

Use these equations as the compact model:

- `harness = instructions + artifacts + tools + review loop`
- `subagent = model + prompt + tool policy + owned output`
- `skill = reusable workflow + references + optional scripts/templates`
- `specialist behavior = subagent + invoked skill`
- `hook = control point that can inspect artifacts and route the next action`
- `ticket = durable task memory + proof target + progress surface`

Two consequences matter most:

1. improve the review loop and proof surfaces before broadening generation
2. prefer the smallest lever that fixes the real failure

For harness-routing decisions, interpret those equations this way:

- the main value of a subagent is context isolation plus clear ownership
- the main value of a skill is procedural consistency
- the main value of a hook is deterministic control-boundary judgment
- the main value of a ticket is visible work state plus proof targeting

## Default Tuning Order

When more than one surface could change, evaluate them in this order:

1. review loop and proof requirements
2. ticket and work-package contract
3. skill packaging
4. subagent boundary
5. hook logic
6. tool or MCP capability
7. root policy

Do not jump to root-prompt rewrites when a narrower surface can carry the
correction.

## Always-Ask Questions

Ask these questions before changing the harness:

1. What exact failure are we trying to prevent or reward?
2. Which current surface owns that failure today?
3. What is the smallest lever that can fix it?
4. Is this a global invariant, a local contract, a repeatable workflow, a role
   boundary, a deterministic routing problem, or a missing capability?
5. Does the problem come from weak judgment, weak proof, missing procedure,
   context overload, ownership blur, or missing observability?
6. Does this need independent judgment, or only a more consistent procedure?
7. Should the answer live in policy, a spec, a skill, a subagent, a hook, a
   ticket contract, a validator, or a tool surface?
8. What ticket size lets us prove this change without hiding it inside a giant
   batch?
9. What is the smallest eval that can prove or kill the idea?
10. If it works, what durable writeback is required?

## Required Placement Analysis

For harness-engineering work, do not jump from "problem noticed" to "edit this
surface." Compare the most likely placement candidates explicitly:

1. repo-local `AGENTS.md`
2. `templates/global/AGENTS.md` when the rule belongs in the shipped global contract
3. `skills/*`
4. `agents/*.toml`
5. hooks / `bin/*`

For each one, state:

- what problem it would solve well
- why it is or is not the right primary surface for this specific change
- whether it should change now, later, or not at all

The expected result is:

- one primary owning surface
- any secondary surfaces that must stay in sync
- a short why-not for the rejected alternatives

Default interpretation:

- repo-local `AGENTS.md` = Codexter-specific priorities, boundaries, and routing
- `templates/global/AGENTS.md` = shipped cross-repo default operating contract
- `skills/*` = repeatable workflow and procedural consistency
- `agents/*.toml` = independent responsibility and context isolation
- hooks / `bin/*` = deterministic control-boundary checks and routing

## Routing Rules

### Root `AGENTS.md`

Use when:

- the rule is repo-wide and durable
- multiple workflows need the same priority or boundary
- the main need is routing agents toward the right deeper source of truth

Do not use when:

- the content is a long procedure
- the rule is local to one workflow or one module
- the real need is a stronger spec, skill, or validator

Keep root `AGENTS.md` map-like.

### `docs/specs/*`

Use when:

- the repo needs a canonical behavior, contract, equation, or routing doctrine
- several skills or agents should consume the same rule
- the change explains how surfaces relate, not just how one workflow runs

Do not use when:

- the content is still exploratory research
- the rule is ticket-local or one-off

### `skills/*`

Use when:

- a workflow is repeated often enough to deserve a playbook
- agents know the idea but execute it inconsistently
- the fix is procedural consistency, not role separation

Do not use when:

- the real problem is self-approval, overloaded context, or ambiguous ownership
- the workflow is too local or too unstable to standardize

### `agents/*.toml`

Use when:

- a responsibility boundary should be independent
- a lane needs isolated context and one owned output
- implementor, QA, reviewer, or evidence skeptic should not be the same role

Do not create a new subagent just because the current role needs a better
checklist.

Default routing lens:

- `subagent` alone solves context isolation and ownership
- `subagent + skill` solves context isolation plus procedural consistency

Reach for a skill before a new subagent when the role is correct but the steps
are inconsistent. Reach for a new subagent before a skill when the problem is
self-agreement, muddy ownership, or context rot.

### Hooks and `bin/*`

Use when:

- the logic should run at a control boundary
- the decision is deterministic and artifact-driven
- the system needs routing, sanity checks, or threshold enforcement

Do not use hooks for broad planning, exploratory judgment, or hidden autonomy.

A good hook decides things like:

- continue, block, or complete
- stale or mismatched ticket selection
- evidence threshold pass or fail
- control-skill activation and safe re-entry

### Ticket contracts

Use `tickets/README.md`, the template, and execution specs when the change is
about:

- work-package size
- proof targets
- acceptance criteria
- verification shape
- progress and handoff visibility

Default ticket size remains:

- the largest coherent capability an agent can build and prove in one strong
  pass

Split only on:

- a real blocker
- a reusable proof surface or foundation
- a risky migration boundary
- an external dependency boundary
- a real runtime or service boundary

Do not split work into crumbs just to make the board look neat.

### Validators

Use mechanical checks only after a repeated high-signal failure proves the rule
is worth the noise.

Good validator targets are:

- required canonical links
- ticket metadata invariants
- naming and file-presence contracts
- objective boundary rules

Do not create validators for narrative nuance or taste.

### Tool and MCP surfaces

Use when:

- the agent cannot reach ground truth
- QA or review lacks inspectable evidence
- a workflow needs a capability the current tool surface does not expose

Do not add tools just because they exist. Wire them into a skill or clear
workflow before expecting consistent use.

## Ticket-Size Questions

Before splitting or combining work, ask:

1. Is this one operator-visible capability or several?
2. Can one pass build it and prove it credibly?
3. Does the proof surface stay coherent if this is split?
4. Is the proposed split driven by a real runtime, migration, or dependency
   boundary?
5. Would this split help review, QA, or rollback, or only make the board look
   cleaner?

If the split does not improve proof, safety, or ownership, keep the ticket
whole.

## Small-Eval Loop

For any harness change:

1. name the failure mode
2. choose one primary owning surface
3. state the smallest patch that changes system behavior
4. run the smallest eval that can prove or kill it
5. write the result back into the canonical doc, ticket, and durable logs that
   actually own the lesson

Default writeback order:

- ticket or active work artifact first
- canonical spec or skill second
- `docs/HISTORY.md` always for shipped changes
- `docs/MEMORY.md` only for durable invariants
- `docs/TROUBLES.md` only for repeated misses or corrections

## Anti-Goals

- do not solve every failure with more global prompt text
- do not create a new subagent when a skill would do
- do not create a new skill when the real need is independent judgment
- do not move exploratory reasoning into hooks
- do not split tickets below the proof boundary
- do not add validators before the failure pattern is clear
