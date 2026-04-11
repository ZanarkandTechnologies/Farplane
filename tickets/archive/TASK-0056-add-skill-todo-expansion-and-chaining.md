---
ticket_id: TASK-0056
title: add skill todo expansion and chaining
phase: complete
status: done
owner: codex
priority: medium
depends_on: []
blocked_by: []
ready: false
approval_required: false
created_at: 2026-04-10T18:38:58Z
updated_at: 2026-04-11T02:06:45Z
next_action: none; ticket archived after the first-pass `todos.md` sidecars, durable docs writeback, and scoped closeout commit prep
last_verification: python3 tickets/scripts/check_ticket_metadata.py; git diff --check; manual inspection of the archived ticket plus the candidate `skills/*/todos.md` sidecars and touched README/AGENTS writeback
linked_docs:
  - AGENTS.md
  - ARCHITECTURE.md
  - README.md
  - docs/HISTORY.md
  - docs/MEMORY.md
  - tickets/templates/ticket.md
  - skills/review/SKILL.md
  - skills/review/todos.md
  - skills/impl/SKILL.md
  - skills/impl/todos.md
  - skills/impl-plan/SKILL.md
  - skills/impl-plan/todos.md
---

# TASK-0056: add skill todo expansion and chaining

## Summary
Experiment with a `todos.md` sidecar contract for skills so complex skills can expose anti-forgetting behavior scaffolds as plain natural-language checkbox templates, and parent skills can reference other skills through Markdown links inside those templates.

## Scope
- In:
  - a canonical `todos.md` convention for skills
  - plain natural-language checkbox templates inside `todos.md`
  - Markdown skill links inside todo items instead of a custom expansion syntax in the first pass
  - guidance for how agents should read and use skill todos as behavioral reminders without inventing a second durable state system
  - one high-fidelity `review` example and one parent-skill chaining example
- Out:
  - persisted workflow runtime state
  - a new ticket state machine or second checklist engine
  - hard enforcement that every skill must have todos in the first pass
  - automatic execution without agent judgment, replanning, or skipping
  - recursive "call the whole same skill again" loops from inside todo groups

## User Story
- `Actor:` Codexter operator or agent using multi-step skills
- `Need:` skills to expose clearer anti-forgetting steps than prose workflow alone
- `Outcome:` agents complete intended skill flows more consistently, especially for review, evidence, QA, and orchestration behaviors that are currently easy to skip

## User Pain / JTBD
- `Current pain:` skills describe workflows, but the instructions are often narrative rather than operational, so agents can miss, compress, or inconsistently order parts of the intended flow and especially forget important behaviors such as delegating review passes or qualifying evidence
- `Why now:` the user wants to test whether explicit skill todo expansion can act as anti-forgetting scaffolding for high-value skills without building a hidden workflow engine

## Non-Goals
- `Do not solve:` a durable workflow runner, persisted completion tracking for skill steps, a replacement for Codex's own internal todo system, or strict deterministic skill execution

## High-Fidelity Example
- `Example flow/artifact:` `skills/impl/todos.md` contains plain checklist items such as `Use the [Review](../review/SKILL.md) skill instead of improvising a vague review pass` and `Use the [Visual QA](../visual-qa/SKILL.md) skill` so the agent can follow natural-language todo prompts and linked skill references without needing a rigid custom parser syntax in the first pass

## What Good Looks Like
- `Quality bar:` skill todos are simple enough to author and maintain, strong enough to reduce repeat "forgot the important behavior" misses, and clearly scoped so they improve agent follow-through without reintroducing hidden orchestration state

## Proof Target
- `Reviewer-visible proof:` a reader can tell where skill todos live, how natural-language todo templates reference other skills, how an agent is supposed to use them, and why the first pass does not create a second runtime workflow system

## Plan

### Pitch
- `Req:` make complex skills easier for agents to follow step by step and reduce repeated behavior misses such as skipped review delegation or weak evidence qualification
- `Bet:` a lightweight `todos.md` sidecar with natural-language checklist templates and Markdown skill links will improve skill completion more than adding more prose to `SKILL.md` or jumping straight to a workflow engine
- `Win:` agents get a stronger scaffold for complex skill flows while tickets and runtime state stay cleanly separated

### Recommendation
- `Best:` define a per-skill `todos.md` sidecar as plain natural-language checklist text with Markdown links to related skills
- `Why:` this keeps reusable anti-forgetting scaffolding close to the skill, preserves `SKILL.md` for narrative contract and handoff rules, and avoids over-designing a custom mini-language before the authoring pattern itself proves useful
- `Tradeoff accepted:` agents still retain judgment to skip, reorder, or replan steps, so this improves consistency rather than guaranteeing strict deterministic execution

### B -> A
- `Before:` skills mostly describe workflows in prose, and chained multi-skill work depends heavily on the agent reconstructing the intended sequence and remembering critical behaviors each time
- `After:` selected skills expose plain natural-language todo templates that can remind the agent which related skills or behaviors to use next
- `Outcome:` skill flows become more followable, more composable, and harder to partially forget

### Delta
- `Touch:` skill contract guidance, one or two example skill folders, and repo docs that explain skill composition and authoring expectations
- `Keep:` tickets as the canonical durable progress surface and Codex's own internal todo mechanism as the execution checklist
- `Change:` add a visible skill-side todo template contract
- `Delete/Avoid:` avoid hidden workflow state, avoid auto-execution claims, avoid recursive full-skill self-invocation, avoid premature custom parser syntax, and avoid making every skill author maintain two bloated documents

### Core Flow
```pseudo
invoke skill or parent skill
read SKILL.md for contract and handoff rules
read todos.md when present
follow the natural-language checklist and linked skill references
dedupe or reorder only when context requires it
execute the normal ticket/spec/build flow using that scaffold
do not persist completion state outside the agent's own todo system
```

### Proof
- `P1:` `skills/review/todos.md` exists as a plain checklist that concretely encodes anti-forgetting review behaviors
- `P2:` at least one parent skill example shows natural-language references to related skills via Markdown links
- `P3:` docs explicitly state that these templates are reminders for the agent's existing internal todo behavior rather than a new persisted workflow tracker
- `Risk:` the contract becomes too rigid, too noisy, or too parser-shaped before the authoring pattern proves useful
- `Rollback:` keep the first slice optional, narrow, and example-driven; if it adds ceremony without improving completion, remove the sidecars and keep the main skill contracts

### Plan Review
- `Refs:` `tickets/TASK-0056-add-skill-todo-expansion-and-chaining.md`, `ARCHITECTURE.md`, `README.md`, `docs/MEMORY.md`, `docs/TROUBLES.md`, `skills/review/SKILL.md`, `skills/impl/SKILL.md`, `skills/impl-plan/references/examples.md`, `skills/impl-plan/references/review.md`
- `Scope:` pass; first build slice stays at contract + example sidecars instead of full-skill rollout
- `Proof:` pass; examples and acceptance checks are observable in-repo
- `Guardrails:` pass; no new durable runtime state and no second checklist engine
- `Recommendation:` pass; plain natural-language sidecars beat both inline overload and workflow-engine overreach
- `Fixes:` narrowed the first implementation target to anti-forgetting behavior scaffolds, removed the named-group mini-language from the examples, and replaced abstract examples with concrete `review` and parent-skill templates

### Options Appendix
- `Option 1:` keep todo steps inline inside each `SKILL.md`
- `Pros:` one file per skill and lower file-count overhead
- `Cons:` mixes narrative contract and anti-forgetting scaffold together, and makes named-group expansion or maintenance noisier
- `Why not chosen:` too muddy for the first experiment and likely to bloat core skill prose
- `Option 2:` add a `todos.md` sidecar per skill as plain natural-language checkbox template text with Markdown links to related skills
- `Pros:` clear separation of concerns, easier authorship, easier chaining, and strong fit for anti-forgetting behavior reminders
- `Cons:` creates another authoring surface and leaves execution semantics intentionally loose
- `Why not chosen:` recommended
- `Option 3:` build a richer workflow engine, custom parser syntax, or persisted skill-step state
- `Pros:` strongest execution control and reporting
- `Cons:` over-scoped, conflicts with current visible-surface boundaries, and risks reintroducing hidden orchestration
- `Why not chosen:` too heavy for the experiment and explicitly out of scope for v1

### Delegation
- `Need:` Not needed
- `Why:` planning slice only
- `Artifact:` n/a

### Ask
- `Ready: yes`
- `Next:` approve the experiment, then define the `todos.md` contract, natural-language checklist style, and one parent-skill chaining example

### Ticket Move
- `Now:` `status: done`, `phase: complete`
- `On approval:` implemented within this ticket
- `Follow-ups:` consider parser behavior, parent-todo semantics, or a dedicated closeout skill only after the plain-template shape proves valuable in real use
- `Blocked in building?:` no

## Acceptance Criteria
- [x] AC-1: Codexter has a documented `todos.md` sidecar convention for skills
- [x] AC-2: the first-pass contract defines plain natural-language checkbox templates with Markdown links to related skills
- [x] AC-3: the guidance explicitly states that expanded steps feed the agent's existing internal todo list rather than a new persisted workflow state surface
- [x] AC-4: `review` has a high-fidelity `todos.md` example that captures anti-forgetting behaviors such as reading the active ticket, selecting rubrics, qualifying evidence, and writing the `Review Packet`
- [x] AC-5: at least one parent-skill chaining example demonstrates the intended before/after behavior and boundaries

## Working Notes
- The user's sharper target behavior is anti-forgetting scaffolding: the skill should remind the agent of behaviors it keeps forgetting, not just serialize every thought into a checklist.
- Success case to preserve: before, agents miss or inconsistently order parts of skill workflows and forget key review/evidence behaviors; after, invoking a skill or parent skill can use plain `todos.md` templates as a stable internal todo scaffold that improves completion consistency.
- Decision boundary: the agent may still decide to skip, reorder, or replan expanded todos when context demands it.
- Recursion guardrail: todo groups may reference other skill todo groups, but v1 should avoid a todo step that recursively re-invokes the whole same skill contract.
- The user prefers this to behave more like a lightweight templating language than a strict custom parser grammar; natural-language checkbox text with Markdown links is the current preferred direction.
- First-cohort candidates after `review`: `impl`, `runtime-debugging`, `visual-qa`, `spec-to-ticket`, `impl-plan`.
- Approved for build on 2026-04-10; the current sub-slice is example sidecars only so the user can review the proposed todo-group shape before any parser or skill-contract rewrites land.

## Inspiration
- Source: user design discussion on 2026-04-10 about adding skill todos and chainable skill todo expansion.
- Relevant takeaway: the strongest first experiment is a sidecar `todos.md` contract that helps an agent build a better internal checklist without turning Codexter into a persisted workflow engine.

## Implementation Notes
- Touched areas:
  - skill authoring contract docs
  - `skills/review/`
  - one parent skill example, likely `skills/impl/`
  - maybe README/spec guidance for skill composition
  - example sidecars now added under `skills/review/`, `skills/impl/`, `skills/runtime-debugging/`, `skills/impl-plan/`, `skills/visual-qa/`, and `skills/spec-to-ticket/`
- Reused patterns:
  - visible artifact boundaries
  - optional conventions before hard enforcement
  - ticket-first planning
- Guardrails:
  - no runtime-owned completion state
  - no hidden auto-chaining claims
  - no recursive full-skill self-invocation in v1
  - keep the contract readable enough for humans and agents

## Optional Appendix

### Example Template

```md
# Todos

- [ ] Read the active ticket first
- [ ] Use the [Review](../review/SKILL.md) skill to review the changed surface
- [ ] If UI evidence is involved, use the [Visual QA](../visual-qa/SKILL.md) skill
- [ ] Pitch the result to the user and revise as needed
```

### Example `review/todos.md`

```md
# Todos

- [ ] read the active ticket first
- [ ] open the rubric index
- [ ] choose the matching rubric families
- [ ] decide whether evidence or UI judgment needs another skill
- [ ] inspect changed files and the minimum neighboring surfaces
- [ ] rank findings by severity and confidence
- [ ] write the Review Packet
- [ ] return verdict and next action
- [ ] collect the proof artifacts the ticket claims exist
- [ ] check traceability from claim to artifact
- [ ] check freshness and inspectability
- [ ] reject weak or missing proof
- [ ] summarize the evidence-quality verdict
```

### Example Parent-Skill Expansion

```md
When `impl` reaches the review/evidence phase for a selected ticket, its `todos.md`
can simply say:

- [ ] Use the [Review](../review/SKILL.md) skill instead of improvising a vague review pass.
- [ ] Use the [Visual QA](../visual-qa/SKILL.md) skill when UI evidence needs judgment.
- [ ] Return to this todo list after those linked skills have been used.
```

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [x] QA / manual verification
- Validation details:
  - added example `todos.md` sidecars for the first-cohort candidate skills
  - converted those example sidecars to plain natural-language checkbox templates after user feedback
  - added `AGENTS.md` and `README.md` for `skills/visual-qa/` and `skills/spec-to-ticket/` because those touched modules lacked them
  - updated touched skill READMEs to expose the new `todos.md` surface where applicable
  - verified `python3 tickets/scripts/check_ticket_metadata.py`
  - verified `git diff --check`
  - archived the ticket after durable docs writeback and closeout review

## Review Packet
- `reviewed_at:` 2026-04-10 18:48 +0100
- `rubrics_used:` implementation-plan,spec-contract
- `overall_score:` 4.6
- `overall_threshold:` 4.0
- `overall_verdict:` pass
- `rerun_required:` false
- `evidence_quality:` pass
- `integration_readiness:` pass
- `traceability:` pass
- `freshness:` pass
- `hard_gate_failures:` []
- `blocking_findings:` []
- `next_action:` archive complete; no further work in this ticket

## Blockers
- none

## Handoff
- Current state: first-pass `todos.md` sidecars landed as plain natural-language checkbox templates, durable docs recorded the anti-parser boundary, and the ticket is archived.
- Resume from: the archived ticket, the candidate sidecars under `skills/*/todos.md`, `docs/MEMORY.md`, and `docs/HISTORY.md` if follow-up work reopens parser behavior or closeout-skill chaining

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter. Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then move the ticket into `tickets/archive/` or set `status: done` briefly if you intentionally keep a short-lived visible completion state first.
