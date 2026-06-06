---
name: diagramming
description: Use when a plan, spec, ticket, architecture note, or code explanation needs compact Mermaid system-design diagrams such as top-level delta maps, zoom-ins, numbered data-flow traces, or inline-signature component diagrams.
tier: 2
source: local
---

# Diagramming

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] Read the active request, ticket, or spec and identify the exact approval question.
- [ ] Draw one top-level delta map before considering any second diagram.
- [ ] Add a numbered data-flow trace only if the flow is the actual question.
- [ ] Embed short signatures in nodes when interface shape matters.
- [ ] Add a legend; do not rely on color alone.
- [ ] Cut any node label that turns into a paragraph.
- [ ] Stop at one or two diagrams unless the user explicitly asks for more depth.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Use this when the missing thing is not more prose, but a compact visual system
story.

The default target is not "more diagrams." The target is one useful top-level
diagram, then one optional zoom-in or data-flow view if the top-level picture is
not enough.

## Job

1. Infer the smallest diagram set that makes the change legible.
2. Start with one top-level system delta map.
3. Add one zoom-in or numbered data-flow diagram only when needed.
4. Embed short signatures in nodes when the interface shape matters.
5. Keep the result compact, legend-backed, and readable in Markdown.
6. Hand the diagram pack back to the active ticket, spec, or explanation.

## Use When

- a plan or spec is turning into an essay
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
  2. draw one top-level delta map
  3. decide whether a zoom-in or data-flow trace is needed
  4. add short legend + inline signatures
  5. keep prose below the diagram short
  6. hand back a compact diagram pack
- Core decision branches:
  - architecture/delta question -> top-level map first
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
- `Tier 1 map`
- `Tier 2` only if needed
- `Legend`
- `Short notes`

If the diagram pack still needs long prose to make sense, it is not ready.

## Workflow

1. Read the active ticket/spec/request and identify the exact approval question.
2. Choose the lightest useful pattern from
   [`references/patterns.md`](references/patterns.md).
3. In Farplane, align the output with
   [`docs/specs/diagram-first-conventions.md`](../../docs/specs/diagram-first-conventions.md)
   when that file exists.
4. Draw the top-level map:
   - system boundary
   - changed components
   - kept components
   - removed components when relevant
   - proof or handoff point if that matters
5. Add inline signatures only where they improve understanding:
   - short function or interface names
   - key file/state fields
   - service responsibilities
6. Decide whether to add one second diagram:
   - zoom-in for one subsystem
   - numbered data-flow trace for read/write/control order
7. Add a short legend and 2-5 short notes.
8. Stop before the output becomes a full spec rewrite.

## Decision Branches

- **Branch A: system delta is the question**
  - produce a top-level keep/change/add/remove map
  - avoid a second diagram unless one boundary remains unclear
- **Branch B: flow is the question**
  - produce the top-level map
  - add a numbered data-flow trace
- **Branch C: interfaces are the question**
  - embed short signatures in nodes
  - keep the labels compact and move extra detail into short notes
- **Branch D: the change is too small**
  - say a diagram is unnecessary and fall back to brief prose

## Guardrails

- prefer one delta diagram over separate before/after diagrams
- color is helpful, but never rely on color alone; include a legend
- keep node labels short
- if the diagram starts looking like a wall of text, split or simplify it
- do not draw more than two diagrams unless the user explicitly asks for depth
- diagrams support the argument; they do not replace proof, risks, or next step

## Documentation Index

- Pattern library: [`references/patterns.md`](references/patterns.md)
- Review checklist: [`references/review.md`](references/review.md)
- Farplane canonical convention:
  [`docs/specs/diagram-first-conventions.md`](../../docs/specs/diagram-first-conventions.md)
