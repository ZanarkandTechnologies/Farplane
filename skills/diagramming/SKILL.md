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
hands off a non-blocking visual companion, or when the reader asks how one
value changes another (a one-control explainer page). Skip it when a few lines
of prose or a table say it better. It owns system-design diagrams and explainer
pages only: `prd` workflow mode
owns interaction models and wireflows, `visual-design` owns look and feel.

## Skill Signature

```text
diagramming(request_or_ticket, approval_question?) -> diagram_pack
reads: the request, ticket or spec; the target renderer
does: picks one form for one reader question and draws the smallest version
writes: inline diagram, or diagrams.md for an impl-plan companion (never ticket.md);
  in Claude, a published Artifact for every Mermaid diagram or explainer page
returns: diagram intent, primary diagram (or its Artifact link), optional second view, legend, short notes
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
  Before/After map; "how do wrong picks change as the threshold drops?" ->
  one-control explainer page (N6).

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
- [ ] **N5 — Render Mermaid where the reader can see it.**
  `Mermaid pack + Artifact tool? -> artifact link | inline Mermaid`

  Rule: Claude chat and Markdown files show Mermaid as raw source. When the
  Artifact tool exists, run `python3 scripts/mermaid_artifact.py <file.md|.mmd|->`
  (from this skill's folder; it keeps headings, prose and tables and writes
  `.farplane/diagramming/<name>.html`), publish that path with the Artifact
  tool, and link it in the reply. Keep the Mermaid source in its Markdown
  owner; republish the same path after edits. Without the tool, write it inline.

  Assert:
  - In Claude, no reply or handoff leaves a Mermaid diagram visible only as source.
- [ ] **N6 — Build a one-control page when one value drives another.**
  `question + value range + data? -> explainer page | diagram fallback`

  Rule: Follow [the explainer page reference](references/interactive.md): a
  fast helper (Sonnet in Claude) writes only the JSON spec, and
  `scripts/explainer_page.py` wraps it in the fixed shell. One slider, one
  canvas, about 2 minutes; on failure or overrun, answer with a diagram.
  Video explainers run only when the user asks (`vox-video`, `hyperframes`).

  Assert:
  - The page has exactly one control, publishes, and its link says what to try.
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
- [mermaid_artifact.py](scripts/mermaid_artifact.py) - Markdown or `.mmd` to
  an Artifact page that renders Mermaid in Claude.
- [interactive](references/interactive.md) and
  [explainer_page.py](scripts/explainer_page.py) - one-control explainer page:
  helper brief, budget and the fixed page shell.
- [impl-plan visual companion](../impl-plan/references/visual-companion-template.md).

## Output

`Diagram intent` (question and form), one primary diagram, an optional second
view, a `Legend` when classes or colours appear, and `Short notes` (assumptions,
proof, one remaining boundary). An `impl-plan` companion returns the template's
`Before`, `After`, optional `What Changed` and metadata.
