---
name: diagramming
description: "Turn plans, tickets, architecture notes, and code explanations into compact diagrams selected by the reader's approval question."
tier: 2
source: local
capability:
  kind: shortcut
---

# Diagramming

Use this when a compact visual system story will replace material prose. Choose
the visual form before choosing Mermaid, ASCII, or a table. This skill owns
system-design diagrams, not visual taste or detailed UI mockups: `functional-ui`
owns interaction models and wireflows; `visual-design` owns look and feel.

## Skill Signature

```text
diagramming(request_or_ticket, approval_question?)
  -> selected_form + compact_diagram_pack + reader_check
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind one reader approval question and select one form.
  - user/action handoff -> numbered sequence or swimlane
  - state, retry, or recovery -> state transition
  - data, ownership, or architecture -> boundary/data-flow map
  - dry run or decision -> numbered trace with a material branch
  - UI behavior -> wireflow/state map; route visual design to its owner
  - system delta -> Before/After map
  - field mapping or comparison -> table; do not force a diagram
- [ ] 2. Draw the smallest form that exposes the needed actors, states,
  boundaries, branch, and proof. Use Mermaid for standalone system packs and
  compact ASCII for a ticket Contract Diagram.
- [ ] 3. Add one distinct second view only when it resolves an unanswered
  question; use short labels, inline signatures only when useful, and a legend
  whenever semantic classes or delta colors appear.
- [ ] 4. When a supplied companion template requires a delta pack, render the
  required Before/After Mermaid views to `diagrams.md` without editing `ticket.md`.
- [ ] 5. Reject prose relabeled as boxes, a form that answers the wrong
  question, decorative detail, or a diagram that needs prose to be understood.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Use When

- a plan, ticket, or explanation is clearer as an explicit flow, state,
  boundary, decision, UI journey, or system delta
- a reader must simulate order, ownership, recovery, or an old-to-new change
- `impl-plan` hands off a non-blocking detailed visual companion

## Do Not Use When

- a trivial change is clearer in a few lines of prose
- a table is a clearer mapping or comparison surface
- the request is pure visual design or illustration
- labels would become paragraphs

## Workflow

1. Read the request, ticket, or spec and state the reader's approval question.
2. Choose the lightest matching pattern from
   [`references/patterns.md`](references/patterns.md).
3. Draw one top-level form with only the actors, states, boundaries, branches,
   and observable proof that answer that question.
4. For a system delta, draw explicit `Before` and `After` maps with a legend;
   do not force that pair on a flow, state, or dry-run question.
5. Add one zoom-in, trace, or per-change-unit map only if the top-level form
   leaves a material question unresolved.
6. If called by `impl-plan`, use
   [`../impl-plan/references/visual-companion-template.md`](../impl-plan/references/visual-companion-template.md),
   keep `ticket.md` canonical, and mark `diagrams.md` non-blocking.
7. Apply [`references/review.md`](references/review.md) before handoff.

## Output Contract

Return a compact diagram pack with:

- `Diagram intent` — the approval question and selected form
- one primary diagram, plus one distinct supplementary view only if needed
- `Legend` for semantic classes, colors, or delta meaning
- `Short notes` — assumptions, proof, or one remaining boundary

For an `impl-plan` companion, return the template's `Before`, `After`, optional
`What Changed`, required metadata, and any compact change-unit maps. If the
pack needs long prose, simplify or choose a different form.

## Guardrails

- A Before/After pair is for a delta, not a universal default.
- A UI wireflow describes behavior; it does not replace `design.md` or visual
  design work.
- Keep each node label short; move detail to short notes or the ticket.
- Do not draw more diagrams than decisions.
- Diagrams clarify the contract; they do not replace proof, risks, or next step.

## References

- [Pattern selection and examples](references/patterns.md)
- [Review checklist](references/review.md)
- [Impl-plan visual companion](../impl-plan/references/visual-companion-template.md)
