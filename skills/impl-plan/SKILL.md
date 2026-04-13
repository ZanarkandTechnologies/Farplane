---
name: impl-plan
version: 2.2.0
description: "Unified per-ticket planning skill with a skimmable Human approval surface, a lower Agent execution surface, and signature-first diagrammed plans."
allowed-tools: Read, Glob, Grep
---

# Impl Plan

Use this for per-ticket implementation planning after a bounded ticket or
execution slice already exists.

`impl-plan` remains the one public planner:

- default mode: approval-first ticket planning
- `--consensus`: Planner/Architect/Critic loop for higher-risk or more
  contentious work

Discovery still belongs to `brainstorm`, `deep-interview`, `prd`, and
`spec-to-ticket`. `impl-plan` is not the broad intake surface.

<!-- MEM-0007 decision: planning output should be approval-first and compact: pitch, before->after, delta, core flow, proof, ask. -->
<!-- MEM-0008 decision: root AGENTS should stay repo-only and terse; skill internals belong in skills, not repo contract text. -->
<!-- MEM-0030 decision: material plans default to a diagram-first approval surface with one top-level Mermaid delta map, optional zoom-in/data-flow, and inline signatures when interface shape matters. -->
<!-- MEM-0031 decision: impl-plan approval surfaces should split into a top Human skim lane and a lower Agent execution lane, with a compact signature sketch near the top whenever interface shape drives trust. -->

When this skill needs diagram taste or pattern depth, reuse
`skills/diagramming/SKILL.md` plus
`docs/specs/diagram-first-conventions.md` instead of inventing a second diagram
style here.

When the architecture itself is still under-specified, or the plan would have
to invent entities, storage ownership, or runtime boundaries, stop and use
`deep-system-design` before finishing the plan. `impl-plan` owns a compact
signature sketch, not a full system-design interview.

## Intent

This skill now writes for two readers:

- `Human:` the top skim surface at the start of the ticket. It should answer
  "is this the right move?" without forcing the reviewer through the whole
  ticket.
- `Agent:` the lower execution surface. It should answer "what exactly do I
  touch, in what order, and how do I prove it?"

If the human cannot approve from `Decision + Diagram + Signature Sketch + B ->
A + Proof`, the plan is not ready.

## Modes

- **Default:** approval-first planning with a short top section and a lower
  execution section only as detailed as the ticket needs
- **`--consensus`:** run the former `ralplan` challenge loop with
  Planner/Architect/Critic before presenting the final plan
- **`--interactive`:** consensus mode only; present the draft and final plan
  for user approval
- **`--deliberate`:** consensus mode only; add pre-mortem and expanded test
  planning for higher-risk work

## Core Prompt Wording

0a. Study `@docs/prd.md` for outcomes + constraints.
0b. Study `@docs/specs/*` for spec truth.
0c. Study the active ticket in `@tickets/*` first; if none exists, inspect
`@tickets/*`.
0d. Study `@docs/MEMORY.md` for durable constraints.
0e. Study `@docs/TROUBLES.md` for repeated planning/execution misses when
present.
0f. Search the codebase before assuming anything is missing.

## Pre-context Intake

Before finalizing the plan or handing off to execution:

1. Reuse the active ticket, linked docs, and canonical specs as the planning
   context surface.
2. Read enough nearby code to name real files, seams, and signatures instead of
   inventing them.
3. In Codexter itself, do **not** create `.omx/context/*` snapshots; that is an
   older OMX-era pattern and not the active repo contract.
4. If intent is still vague, use `deep-interview --quick`.
5. If system shape is still vague, use `deep-system-design`.

Do not hand off to execution while the plan still depends on avoidable
unknowns.

## Trigger Conditions

- user asks for a plan, proposal, implementation approach, or approval-ready
  change summary
- feature/refactor work needs a human yes/no before changing a ticket from
  `status: review` to `status: building`
- request is large enough that the code shape, file touch points, or proof
  should be made explicit before implementation
- execution surfaces redirect a vague implementation request into planning first

## Workflow (Default Mode)

1. **Scope:** choose the next smallest executable slice.
2. **Split check:** if not one commit, stop and ask to split.
3. **Compare:** show 3 viable options with bounded pros/cons.
4. **Recommend:** state the best option and the tradeoff being accepted.
5. **Build the `Human` lane first:** decision, diagram, signature sketch,
   before/after, proof, ask.
6. **Build the `Agent` lane second:** delta, execution order, risk/rollback,
   ticket move, and any appendix detail.
7. **Review + ask:** run the plan through the quality gate, fix weak spots
   before handoff, then show `Ready: yes/no`.

## Workflow (`--consensus` Mode)

Consensus mode preserves the former `ralplan` behavior inside this one skill.

1. Planner drafts the `Human` lane and the smallest useful `Agent` lane.
2. Architect reviews for steelman antithesis, tradeoff tension, and synthesis.
3. Critic evaluates for option quality, signature clarity, risk clarity, and
   concrete verification.
4. If Critic does not approve, revise and repeat the Architect -> Critic loop.
5. Present the final consensus-backed plan.

Use consensus mode when:

- the change is high risk, ambiguous, or architecturally contentious
- the user explicitly wants stronger challenge before implementation
- the handoff to execution would otherwise rely on untested judgment calls

## Core Decision Branches

- **Low risk / obvious fit:** keep the whole plan short; text-only is okay if
  the change is truly localized.
- **Material / cross-module:** require a diagram-first `Human` lane.
- **Interface-heavy / signature-heavy:** require a `Signature Sketch` near the
  top.
- **High ambiguity / risk:** keep the `Human` lane short and push detail below
  fold.
- **High risk / architectural tension:** prefer `--consensus`.
- **Multi-commit work:** split before planning in detail.
- **Docs-only / rule-text-only:** no specialized QA delegation.

## Human Lane

The start of the ticket should carry a skimmable `Human` section. It is the
approval surface, not an appendix.

### Required `Human` fields

1. `Decision`
   - `Req:` what I think you want
   - `Best:` chosen option
   - `Why:` why it fits the current constraints
   - `Tradeoff accepted:` the main downside you are knowingly taking
   - `Not chosen:` short note for the rejected viable paths
2. `Diagram`
   - `Tier 1:` one top-level Mermaid delta diagram for material or cross-module
     work
   - `Legend:` keep / change / add / remove
   - show the new or changed components directly
   - if interface shape matters, embed short signatures in the relevant nodes
   - optional `Tier 2:` numbered data-flow or zoom-in only if Tier 1 is not
     enough
3. `Signature Sketch`
   - 3-7 important seams when the plan changes interfaces, ownership
     boundaries, data shape, handlers, jobs, or state flow
   - format should stay compact, for example
     `module / symbol(input): output`
   - name real files, handlers, jobs, helpers, state atoms, or schema seams
   - this exists to prove codebase understanding and build trust
   - do **not** paste full type dumps
4. `B -> A`
   - before
   - after
   - user/dev outcome
5. `Proof`
   - 2-4 concrete checks
   - main risk
   - rollback or containment note
6. `Ask`
   - `Ready: yes/no`
   - next step after approval

### `Human` lane guidance

- Lead with the diagram before long prose for material work.
- Keep the top section skimmable in under a minute.
- Use the signature sketch to show the important code contracts, not every
  helper.
- If the reviewer still needs the lower section to understand the plan, tighten
  the `Human` lane.

## Agent Lane

The lower `Agent` section is the execution-facing contract. It exists to remove
implementation ambiguity without turning the top of the ticket into an essay.

### Required `Agent` fields

1. `Delta`
   - touched files/modules
   - keep/change/delete
2. `Execution Plan`
   - 3-7 concrete steps or one compact numbered data-flow diagram
   - enough detail that the build shape is obvious
3. `Risk / Rollback`
   - what could go wrong first
   - how to contain or undo it
4. `Plan Review`
   - `Refs:` confirm which sources were actually used:
     PRD/spec/ticket/memory/troubles/code
   - `Checks:` pass/fix for scope, proof, guardrails, diagram usefulness,
     signature usefulness, and rollback clarity
   - `Fixes:` what was tightened before handoff, or `none`
5. `Delegation`
   - skill/subagent only if needed
   - otherwise `Not needed`
6. `Ticket Move`
   - what `status` / `phase` it should have now
   - any spawned follow-up tickets
   - whether it stays blocked in `status: building` or returns to
     `status: review`

### Optional `Agent` fields

Only add these when they materially reduce ambiguity:

- `User Story`
- `User Pain / JTBD`
- `Non-Goals`
- `High-Fidelity Example`
- `What Good Looks Like`
- `Proof Target`
- `Options Appendix`

Narrative sections are required for material feature work, workflow/tooling
changes, ambiguous implementation work, and any ticket where the implementer
would otherwise need to infer desired behavior. They are optional or short for
trivial localized fixes.

## Applicability Rule

- **Diagram + signature sketch required:** material feature work,
  workflow/tooling changes, ambiguous implementation work, cross-module
  changes, or any ticket where trust depends on seeing new components, changed
  data flow, or important code seams.
- **Diagram required, signature sketch optional:** when system shape matters but
  the interface seam is already obvious from one symbol or file.
- **Text-only allowed:** trivial, single-bug, or narrowly localized fixes where
  the file, symbol, or error already anchors the work concretely.

## Top Gotchas

1. Do not implement; this skill is plan-only.
2. Do not turn the `Human` lane into the whole ticket.
3. Do not hide the key interfaces in prose when a short signature sketch would
   prove understanding faster.
4. Do not paste large raw type dumps into the ticket.
5. Do not create two separate plan artifacts when one `Human` + `Agent` split
   is enough.
6. Do not skip the option comparison for material choices.

## Outcome Contract

Every plan must include:

1. `Human`
   - `Decision`
   - `Diagram`
   - `Signature Sketch` when the applicability rule says it is required
   - `B -> A`
   - `Proof`
   - `Ask`
2. `Agent`
   - `Delta`
   - `Execution Plan`
   - `Risk / Rollback`
   - `Plan Review`
   - `Delegation`
   - `Ticket Move`
3. `Options Appendix`
   - exactly 3 viable options for material choices
   - each option gets concrete pros/cons
   - each non-chosen option gets `Why not chosen`
   - if the path is effectively forced, still name the rejected fallback shapes
     briefly

## Efficiency Rules

- Lead with the approval surface, not the appendix.
- Keep the `Human` lane short enough to skim quickly.
- For material work, the approval surface starts with diagrams, not paragraphs.
- If the user did not provide a take, default to consultative guidance instead
  of neutral mirroring.
- Prefer symbols and compact labels over repeated prose.
- Reuse the `diagramming` skill's compact delta-map, color/legend, and
  inline-signature patterns instead of inventing a new diagram style in each
  plan.
- Reuse existing modules; justify every new file or abstraction in one line.
- Keep deeper implementation detail in the `Agent` lane, not above it.
- If the plan cannot be understood from `Decision + Diagram + Signature Sketch
  + B -> A + Proof`, it is not ready.
- If planning reveals overflow scope, split it into new `tickets/` follow-ups
  instead of stretching one ticket.
- Do not force the richer narrative sections onto trivial localized fixes when
  the work is already concrete from code context.

## Plan Quality Gate

Before returning the plan, run these checks against the drafted output:

1. **Reference coverage**
   - Did the plan actually use the relevant PRD, spec, ticket, memory,
     troubles, and local code context?
   - If a source was skipped, is that omission safe and explicit?
2. **Scope discipline**
   - Is this really one commit?
   - If not, stop and split instead of hiding extra scope in prose.
3. **Recommendation quality**
   - Did the plan compare real options instead of cosmetic variants?
   - Is the chosen path clearly recommended, not merely listed?
4. **Diagram usefulness**
   - For material work, is there one top-level delta diagram rather than a
     prose-only explanation?
   - Does the legend make `keep / change / add / remove` obvious?
   - Are short signatures embedded directly in nodes when interfaces matter?
5. **Signature usefulness**
   - Does the `Signature Sketch` name the real seams that matter?
   - Is it compact enough to skim?
   - Would it convince a reviewer that the planner understands the codebase?
6. **Agent usefulness**
   - Does the lower section remove implementation ambiguity without bloating the
     ticket?
   - Are touched files and execution order explicit?
7. **Proof quality**
   - Are the checks concrete and observable?
   - Would a reviewer know exactly how to tell success from failure?
8. **Risk clarity**
   - Is the main risk named?
   - Is rollback or containment clear enough for the size of the change?
9. **Narrative usefulness**
   - If narrative sections are present, do they actually reduce ambiguity?
   - Are they concrete rather than decorative or duplicated filler?
10. **Architecture boundary**
   - If the plan still depends on invented entities, storage ownership, or
     runtime boundaries, did we stop and route to `deep-system-design`?

If any check fails, tighten the plan before presenting it. The final output
should show the review result, not the draft that failed it.

## References

- [prompts/plan.md](prompts/plan.md)
- [references/template.md](references/template.md)
- [references/examples.md](references/examples.md)
- [references/review.md](references/review.md)

## Final Check

Before handoff, read `references/review.md` and tighten the plan until it passes
those checks.
