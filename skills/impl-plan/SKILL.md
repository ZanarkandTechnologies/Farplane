---
name: impl-plan
version: 2.1.0
description: "Unified per-ticket planning skill. Default approval-first planning with a compact diagram-first summary and optional consensus mode for Architect/Critic challenge before execution."
allowed-tools: Read, Glob, Grep
---

# Impl Plan

Use this for per-ticket implementation planning after a bounded ticket or
execution slice already exists.

`impl-plan` replaces the old split between `ralplan` and `tech-impl-plan`.
There is now one public planner:

- default mode: approval-first ticket planning
- `--consensus`: Planner/Architect/Critic loop for higher-risk or more
  contentious work

Discovery still belongs to `brainstorm`, `deep-interview`, `prd`, and
`spec-to-ticket`. `impl-plan` is not the broad intake surface.

<!-- MEM-0007 decision: planning output should be approval-first and compact: pitch, before->after, delta, core flow, proof, ask. -->
<!-- decision: every plan should run a built-in quality pass before handoff so missing references, weak proof, or hidden scope drift are caught before approval. -->
<!-- MEM-0008 decision: root AGENTS should stay repo-only and terse; skill internals belong in skills, not repo contract text. -->
<!-- MEM-0030 decision: material plans default to a diagram-first approval surface with one top-level Mermaid delta map, optional zoom-in/data-flow, and inline signatures when interface shape matters. -->

## Modes

- **Default:** approval-first planning with a concise top section and richer
  implementation detail only when the ticket needs it
- **`--consensus`:** run the former `ralplan` challenge loop with
  Planner/Architect/Critic before presenting the final plan
- **`--interactive`:** consensus mode only; present the draft and final plan
  for user approval
- **`--deliberate`:** consensus mode only; add pre-mortem and expanded test
  planning for higher-risk work

## Core Prompt Wording

0a. Study `@docs/prd.md` for outcomes + constraints.
0b. Study `@docs/specs/*` for spec truth.
0c. Study the active ticket in `@tickets/*` first; if none exists, inspect `@tickets/*`.
0d. Study `@docs/MEMORY.md` for durable constraints.
0e. Study `@docs/TROUBLES.md` for repeated planning/execution misses when present.
0f. Search the codebase before assuming anything is missing.

## First-Load Contract

## Pre-context Intake

Before finalizing the plan or handing off to execution:

1. Derive a task slug from the request or ticket for your own reasoning only.
2. Reuse the active ticket, linked docs, and canonical specs as the planning
   context surface.
3. In Codexter itself, do **not** create `.omx/context/*` snapshots; that is an
   older OMX-era pattern and not the active repo contract.
4. If ambiguity remains high even after codebase inspection, use
   `deep-interview --quick` before planning deeper.

Do not hand off to execution while the plan still depends on avoidable unknowns.

## First-Load Contract

### Trigger Conditions

- user asks for a plan, proposal, implementation approach, or approval-ready change summary
- feature/refactor work needs a human yes/no before changing a ticket from `status: review` to `status: building`
- request is large enough that `B -> A` and proof should be made explicit
- execution surfaces redirect a vague implementation request into planning first

### Workflow (Default Mode)

1. **Scope**: choose the next smallest executable slice.
2. **Split check**: if not one commit, stop and ask to split.
3. **Pitch**: show `Req`, `Bet`, `Win`.
4. **Compare**: show 3 viable options with bounded pros/cons; if one is clearly dominant, still name the discarded paths.
5. **Recommend**: state the best option and the tradeoff being accepted.
6. **Delta**: show `Before -> After`, touched areas, and keep/change/delete.
7. **Clarify intent**: when the work is material or ambiguous, add explicit user
   story, JTBD, non-goals, example behavior, quality target, and proof target.
8. **Teach**: for material, cross-module, or architecture-facing work, start
   with one Mermaid delta diagram plus an optional zoom-in or data-flow view;
   keep prose below that. For trivial localized fixes, diagrams stay optional.
9. **Review + ask**: run the plan through the quality gate, fix weak spots before handoff, then show proof points and `Ready: yes/no`.

### Workflow (`--consensus` Mode)

Consensus mode preserves the former `ralplan` behavior inside this one skill.

1. Planner drafts the plan plus a compact decision summary.
2. Architect reviews for steelman antithesis, tradeoff tension, and synthesis.
3. Critic evaluates for option quality, risk clarity, acceptance-test quality,
   and concrete verification.
4. If Critic does not approve, revise and repeat the Architect -> Critic loop.
5. Present the final consensus-backed plan.

Use consensus mode when:

- the change is high risk, ambiguous, or architecturally contentious
- the user explicitly wants stronger challenge before implementation
- the handoff to execution would otherwise rely on untested judgment calls

### Core Decision Branches

- **Low risk / obvious fit** -> keep plan short; no appendix; text-only is okay
  if the change is truly localized.
- **Material / cross-module** -> require a diagram-first approval surface.
- **High ambiguity / risk** -> keep short top section; push details below fold.
- **High risk / architectural tension** -> prefer `--consensus`.
- **Multi-commit work** -> split before planning in detail.
- **Docs-only / rule-text-only** -> no specialized QA delegation.

### Top Gotchas

1. Do not implement; this skill is plan-only.
2. Do not bury `Before -> After` below long explanation.
3. Do not create two separate plan artifacts when one richer primary artifact is
   enough.
4. Do not fall back to essays when one top-level delta diagram plus one
   data-flow view would explain the plan faster.

### Applicability Rule

The richer narrative sections below are:

- **required** for material feature work, workflow/tooling changes, ambiguous
  implementation work, and any ticket where the implementer would otherwise
  need to infer desired behavior
- **diagram-first required** for the same cases when the ticket spans more than
  one component, has a meaningful before/after shape, or depends on a visible
  flow or interface boundary
- **optional or short** for trivial, single-bug, or narrowly localized fixes
  where the file, symbol, or error already anchors the work concretely

### Outcome Contract

Every plan must include:

1. `Pitch`
   - `Req:` what I think you want
   - `Bet:` better option if any
   - `Win:` why this shape
2. `Recommendation`
   - `Best:` chosen option
   - `Why:` why it fits the current constraints
   - `Tradeoff accepted:` the main downside you are knowingly taking
3. `Diagram Summary`
   - `Tier 1:` one top-level Mermaid delta diagram
   - `Legend:` keep / change / add / remove
   - short inline signatures in nodes when the interface or ownership boundary
     matters
   - optional `Tier 2:` zoom-in or component diagram only if Tier 1 is not
     enough
4. `B -> A`
   - before
   - after
   - user/dev outcome
5. `Delta`
   - touched files/modules
   - keep/change/delete
6. `Core Flow`
   - prefer a compact numbered Mermaid data-flow diagram for material work
   - fallback to 6-12 lines of pseudocode only when that is clearer
7. `Proof`
   - 2-4 concrete checks
   - main risk / rollback note
8. `User Story` when the applicability rule says it is required
   - actor
   - need
   - outcome
9. `User Pain / JTBD` when required
10. `Non-Goals` when required
11. `High-Fidelity Example` when required
12. `What Good Looks Like` when required
13. `Proof Target` when required
14. `Plan Review`
   - `Refs:` confirm which sources were actually used: PRD/spec/ticket/memory/troubles/code
   - `Checks:` pass/fix for scope, proof, guardrails, and rollback clarity
   - `Fixes:` what was tightened before handoff, or `none`
15. `Options Appendix`
   - exactly 3 viable options for material choices
   - each option gets concrete pros/cons
   - each non-chosen option gets `Why not chosen`
   - if the path is effectively forced, still name the rejected fallback shapes briefly
16. `Ask`
   - `Ready: yes/no`
   - next step after approval
17. `Delegation`
   - skill/subagent only if needed
   - otherwise `Not needed`
18. `Ticket Move`
   - what `status` / `phase` it should have now
   - any spawned follow-up tickets
   - whether it stays blocked in `status: building` or returns to `status: review`

### Section Roles

- `Summary` = smallest executable slice
- `Scope` = in/out boundaries
- `User Story` = who needs what and why now
- `User Pain / JTBD` = what friction makes the change matter
- `High-Fidelity Example` = one realistic walkthrough of the desired behavior or
  artifact
- `What Good Looks Like` = concise target quality bar
- `Proof Target` = evidence that would convince a reviewer the ticket is done
- `Plan` = how implementation reaches that result

## Efficiency Rules

- Lead with the approval surface, not the appendix.
- For material work, the approval surface starts with diagrams, not paragraphs.
- If the user did not provide a take, default to consultative guidance instead of neutral mirroring.
- Prefer symbols and compact labels over repeated prose.
- Prefer one top-level delta diagram over separate before/after diagrams.
- Put short signatures inside nodes when interface shape is the point.
- Reuse existing modules; justify every new file or abstraction in one line.
- Keep deeper implementation detail below the top section.
- If the plan cannot be understood from `Recommendation + Diagram Summary + Core Flow`, it is not ready.
- If planning reveals overflow scope, split it into new `tickets/` follow-ups instead of stretching one ticket.
- Do not force the richer narrative sections onto trivial localized fixes when
  the work is already concrete from code context.

## Plan Quality Gate

Before returning the plan, run these checks against the drafted output:

1. **Reference coverage**
   - Did the plan actually use the relevant PRD, spec, ticket, memory, troubles, and local code context?
   - If a source was skipped, is that omission safe and explicit?
2. **Scope discipline**
   - Is this really one commit?
   - If not, stop and split instead of hiding extra scope in prose.
3. **Guardrail fit**
   - Does the plan reuse existing patterns?
   - Does it avoid speculative abstractions, silent migrations, and unnecessary new files?
4. **Proof quality**
   - Are the checks concrete and observable?
   - Would a reviewer know exactly how to tell success from failure?
5. **Risk clarity**
   - Is the main risk named?
   - Is rollback or containment clear enough for the size of the change?
6. **Recommendation quality**
   - Did the plan compare real options instead of cosmetic variants?
   - Is the chosen path clearly recommended, not merely listed?
7. **Narrative usefulness**
   - If `User Story` is present, does it name an actor, need, and outcome?
   - If `High-Fidelity Example` is present, is it concrete rather than
     placeholder or boilerplate text?
   - Are the narrative sections distinct from `Summary` and `Scope`, rather
     than duplicated filler?
8. **Diagram usefulness**
   - For material work, is there one top-level delta diagram rather than a
     prose-only explanation?
   - Does the legend make `keep / change / add / remove` obvious?
   - Are short signatures embedded directly in nodes when interfaces matter?
   - Did the plan avoid redundant before/after diagrams?
9. **Approval-surface concision**
   - Can a reviewer still skim the top section quickly?
   - Has the lower detail been kept below the approval surface?

If any check fails, tighten the plan before presenting it. The final output should show the review result, not the draft that failed it.

## References

- [prompts/plan.md](prompts/plan.md)
- [references/template.md](references/template.md)
- [references/examples.md](references/examples.md)
- [references/review.md](references/review.md)

## Final Check

Before handoff, read `references/review.md` and tighten the plan until it passes those checks.
