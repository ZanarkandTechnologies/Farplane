---
name: recap-idea
description: "Turn a product discussion into the visual model that best exposes misunderstandings before requirements, design, or implementation begins."
tier: 2
source: local
capability:
  kind: shortcut
template_uses:
  skill-template: "0.6.2"
allowed-tools: Read, Glob, Grep
---

# Recap Idea

## Context

Use this after a product discussion when the operator wants to see what the
agent thinks is being built. It returns a proposed visual model, not a
transcript, feature list, status recap, PRD, or prototype.

## Skill Signature

```text
recap_idea(discussion, product_context?, focus?) -> proposed_visual_model
reads: conversation, accepted decisions, and supplied product artifacts
does: selects and fills one visual template that exposes likely misunderstandings
writes: none
returns: proposed interpretation, visual, uncertainties, and correction questions
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Frame the product question the operator must verify.**
  `discussion -> confirmed meaning + conflicts + assumptions + alignment_question | task_status_route`

  Rule: Center the user, the change in their experience, and the value they
  receive. Keep contradictions visible. If the request is about task history,
  tests, or next steps, route to the task recap shortcut instead of inventing a product.

  Assert:
  - One sentence says what the operator is being asked to confirm.
  - Confirmed meaning, inference, and unresolved intent are distinguishable.

- [ ] **N2 — Pick the view from the verification question.**
  `alignment_question -> template_id + decisive content`

  Rule: Load [visual templates](references/visual-templates.md) and select one:
  `journey` for end-to-end value, `ui-screen-flow` for what users see and do,
  `lifecycle` for state and recovery, `system-boundary` for ownership and data
  movement, `before-after-example` for a real change, or `comparison-table` for
  exact correspondence.

  Example: `dashboard redesign + “what will the lead see?” -> ui-screen-flow`,
  even when the discussion also mentions backend components.

  Assert:
  - The chosen view answers the operator's question rather than cataloguing the product.
  - UI flows include visible content, actions, and material loading, empty, error, or success states.

- [ ] **N3 — Fill one template and make it correctable.**
  `template_id + decisive content -> proposed_visual_model`

  Rule: Replace every placeholder with discussion-grounded nouns, actions,
  states, and uncertainty. Render Mermaid inline when relationships matter;
  use the comparison table only when exact mapping is clearer. Do not append an
  ASCII duplicate, artifact link, implementation plan, or second decorative view.

  Assert:
  - The visual explains itself before the supporting prose.
  - The model is labeled proposed and ends with one to three questions about the riskiest mismatches.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Architecture is the wrong view when the operator asks what an end user sees.
- Generated prose is not evidence; preserve original sources and verification links when they are part of the product meaning.
- A polished diagram must not silently resolve a contradiction or open choice.

## Reference Map

- [Visual templates](references/visual-templates.md) — load after N1 frames the verification question.

## Output

Return one proposed interpretation, one filled visual template, visible
uncertainty, and one to three correction questions. Write no artifact.
