---
name: diagramming
description: "Turn plans, specs, tickets, architecture notes, or code explanations into compact Mermaid diagrams and flow traces."
tier: 2
source: local
---

# Diagramming

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] Read the active request, ticket, or spec and identify the exact approval question.
- [ ] Draw the target flow and before/after delta before considering any
  supplementary diagram.
- [ ] Add a numbered data-flow trace only if the flow is the actual question.
- [ ] When called by `impl-plan`, render the visual companion template from the
  ticket and write `diagrams.md` without editing `ticket.md`.
- [ ] Embed short signatures in nodes when interface shape matters.
- [ ] Add a legend; do not rely on color alone.
- [ ] Cut any node label that turns into a paragraph.
- [ ] Stop at one or two diagrams unless the user explicitly asks for more
  depth or an `impl-plan` visual companion needs compact per-change-unit maps.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Use this when the missing thing is not more prose, but a compact visual system
story.

The default target is not "more diagrams." The target is one useful flow map
plus one explicit before/after delta, then one optional zoom-in or data-flow
view if those two pictures are not enough.

## Job

1. Infer the smallest diagram set that makes the change legible.
2. Start with the target flow and before/after delta.
3. Add one zoom-in, numbered data-flow diagram, or `impl-plan` change-unit map
   set only when needed.
4. Embed short signatures in nodes when the interface shape matters.
5. Keep the result compact, legend-backed, and readable in Markdown.
6. Hand the diagram pack back to the active ticket, spec, or explanation.

## Use When

- a plan or spec is turning into an essay
- `impl-plan` hands off a non-blocking `diagrams.md` visual companion
- the reader needs to see the before/after system shape quickly
- the critical thing is component ownership or data flow
- a ticket spans multiple modules or interfaces
- a code explanation would be clearer as a component map plus short signatures

## Do Not Use When

- the change is a trivial one-symbol fix that 3 lines of prose can explain
- the request is pure visual design or illustration rather than system design
- the diagram would duplicate an already-clear existing map without adding delta
- the node labels would need paragraphs to make sense

## First-Load Checklist

Ensure an agent can execute the core path after only reading this file.

- Trigger conditions:
  - multi-component or flow-heavy change
  - need for before/after compression
  - need for inline signatures or ownership clarity
- Workflow:
  1. identify the approval question
  2. draw the target flow and before/after delta
  3. decide whether a zoom-in or data-flow trace is needed
  4. add short legend + inline signatures
  5. keep prose below the diagram short
  6. hand back a compact diagram pack
- Core decision branches:
  - architecture/delta question -> target flow plus before/after delta first
  - flow question -> add numbered data-flow second
  - one subsystem still unclear -> add one zoom-in
- Top gotchas:
  - do not create decorative Mermaid
  - do not split into before/after diagrams by default
  - do not move important interfaces back into detached prose lists
- Outcome contract:
  - the reader can understand the change from the first diagram
  - every diagram has a legend or clearly labeled delta semantics
  - no diagram contains paragraph-sized node labels

## Output Contract

Produce one compact diagram pack with:

- `Diagram intent`
- `Target Flow`
- `Before / After Delta`
- `Tier 2` only if needed
- `Change Unit Maps` when rendering an `impl-plan` visual companion
- `Legend`
- `Short notes`

If the diagram pack still needs long prose to make sense, it is not ready.

## Workflow

1. Read the active ticket/spec/request and identify the exact approval question.
2. Choose the lightest useful pattern from
   [`references/patterns.md`](references/patterns.md).
3. If called by `impl-plan`, load
   [`../impl-plan/references/visual-companion-template.md`](../impl-plan/references/visual-companion-template.md)
   and write `tickets/TASK-XXXX/diagrams.md` as a companion with
   `blocks_approval: false` and `canonical_contract: ticket.md`.
4. In Farplane, use this skill as the owner of diagram-first convention.
5. Draw the target flow:
   - system boundary
   - trigger or input
   - changed workflow owner
   - new or updated artifact/state
   - proof or feedback point when it matters
6. Draw the before/after delta:
   - old path, owner, or behavior
   - new path, owner, or behavior
   - replacement, move, or upgrade edge
7. Add inline signatures only where they improve understanding:
   - short function or interface names
   - key file/state fields
   - service responsibilities
8. Decide whether to add one supplementary diagram:
   - zoom-in for one subsystem
   - numbered data-flow trace for read/write/control order
   - compact per-change-unit maps when the `impl-plan` companion template asks
     for a visual map of each material change unit
9. Add a short legend and 2-5 short notes.
10. Stop before the output becomes a full spec rewrite.

## Decision Branches

- **Branch A: system delta is the question**
  - produce target flow plus before/after delta
  - avoid supplementary diagrams unless one boundary remains unclear
- **Branch B: flow is the question**
  - produce the top-level map
  - add a numbered data-flow trace
- **Branch C: interfaces are the question**
  - embed short signatures in nodes
  - keep the labels compact and move extra detail into short notes
- **Branch D: the change is too small**
  - say a diagram is unnecessary and fall back to brief prose
- **Branch E: impl-plan visual companion**
  - use `ticket.md` as the only source of scope
  - write or return `diagrams.md` from the impl-plan companion template
  - include target flow, before/after delta, optional compact change-unit maps,
    optional proof map, and a feedback guide
  - do not edit `ticket.md`; scope corrections must go back to `impl-plan`

## Guardrails

- prefer target flow plus a before/after delta over random supplementary maps
- color is helpful, but never rely on color alone; include a legend
- keep node labels short
- if the diagram starts looking like a wall of text, split or simplify it
- do not draw more than two diagrams unless the user explicitly asks for depth
  or the `impl-plan` visual companion template requires compact per-change maps
- diagrams support the argument; they do not replace proof, risks, or next step
- `impl-plan` companions are reader aids, not canonical approval contracts

## Documentation Index

- Pattern library: [`references/patterns.md`](references/patterns.md)
- Review checklist: [`references/review.md`](references/review.md)
- Impl-plan companion template:
  [`../impl-plan/references/visual-companion-template.md`](../impl-plan/references/visual-companion-template.md)

## Farplane Convention

Use diagram-first approval surfaces for material, cross-module, workflow,
tooling, or architecture-facing changes when visual structure is easier to
approve than prose. Prefer one target-flow diagram plus one before/after delta
and short notes. Add one zoom-in or numbered data-flow diagram only when those
diagrams cannot carry the decision.

When called after `impl-plan`, produce a separate `diagrams.md` companion from
the impl-plan template. Keep `ticket.md` canonical, mark the companion
non-blocking, and mirror the ticket structure visually so the operator can read
the maps first and give feedback.
