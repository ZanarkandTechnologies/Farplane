---
name: diagramming
description: "Use for \"draw this\", \"diagram the architecture\", \"show me the flow\" or \"make a before/after map\": one compact diagram pack chosen by the reader's approval question."
source: local
department: delivery
capability:
  kind: shortcut
template_uses:
  skill-template: "0.6.5"
---

# Diagramming

## Context

Use this when a plan, ticket, or explanation is clearer as an explicit flow,
state, boundary, decision, UI journey, or system delta, or when `impl-plan`
hands off a non-blocking visual companion. Skip it when a few lines of prose or
a table say it better. It owns system-design diagrams only: `prd` workflow mode
owns interaction models and wireflows, `visual-design` owns look and feel.

## Skill Signature

```text
diagramming(request_or_ticket, approval_question?) -> diagram_pack
reads: the request, ticket or spec; the target renderer
does: picks one form for one reader question and draws the smallest version
writes: inline diagram, or diagrams.md for an impl-plan companion (never ticket.md)
returns: diagram intent, primary diagram, optional second view, legend, short notes
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Bind one approval question and pick the form.**
  `request -> reader question + form | prose_or_table`

  Rule: Map the question to a form with the global contract's visual routing
  table (reader question -> form). Exact mappings stay tables. For Mermaid,
  load the [capability catalog](references/patterns.md) and verify the target
  renderer supports the type before using it.

  Example: "what happens when the webhook retries?" -> state transition, not a
  Before/After map.

  Assert:
  - One question, one form; a Before/After pair only for a system delta.
- [ ] **N2 — Draw the smallest form that answers it.**
  `form + facts -> primary diagram`

  Rule: Show only the actors, states, boundaries, branch and proof the question
  needs; short labels, no prose in boxes. Mermaid for standalone packs, compact
  ASCII for a ticket Contract Diagram. Add a legend whenever classes or delta
  colours appear.

  Assert:
  - The diagram reads without colour and without surrounding prose.
- [ ] **N3 — Add a second view only for an unanswered question.**
  `primary diagram + open question -> zoom-in | trace | per-unit map | none`

  Rule: Never draw more diagrams than decisions. For a ticket's visual
  companion, use the companion template in the Reference Map, write
  `diagrams.md`, keep `ticket.md` canonical, mark it non-blocking.

  Assert:
  - Each extra view resolves a named question.
- [ ] **N4 — Review before handoff.**
  `diagram pack -> pass | revise`

  Rule: Apply [the review checklist](references/review.md). Reject prose
  relabelled as boxes, a form that answers the wrong question, decorative
  detail, or invented precision in a chart.

  Assert:
  - The pack passes the checklist or is simplified until it does.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Defaulting to Before/After for a flow or state question; the reader cannot
  simulate order or recovery from two static maps.
- Using an experimental Mermaid type (mindmap, timeline) the client cannot
  render; fall back to a flowchart, state diagram, table or ASCII.
- A UI wireflow standing in for `design.md` or visual design work.

## Reference Map

- [patterns](references/patterns.md) - form selector with essential content,
  the Mermaid capability catalog, and worked examples per form.
- [review](references/review.md) - pre-handoff checklist.
- [impl-plan visual companion](../impl-plan/references/visual-companion-template.md).

## Output

`Diagram intent` (question and form), one primary diagram, an optional second
view, a `Legend` when classes or colours appear, and `Short notes` (assumptions,
proof, one remaining boundary). An `impl-plan` companion returns the template's
`Before`, `After`, optional `What Changed` and metadata.
