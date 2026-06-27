---
name: infographic
version: 0.1.0
description: "Turn an explanation, dataset, product flow, or argument into a clear infographic brief, layout spec, and production-ready visual asset plan."
tier: 3
group: content-visual
source: local
skill_template_version: "0.3.6"
template_uses:
  skill-template: "0.3.6"
  skill-method-reference: "0.1.0"
  skill-qa-checklist: "0.1.0"
methods:
  - infographic:handdrawn-saas-wireframe
common_chains:
  after: ["image-generation", "visual-qa"]
eval: eval_task.json
qa_checklist: qa_checklist.md
allowed-tools: Read, Grep, Glob, Bash
---

# Infographic

## Context

Use this skill when the user wants a visual explanation, product-state
storyboard, annotated dashboard, process map, educational graphic, data-backed
social visual, or slide-like image whose value depends on clear composition and
copy hierarchy.

This skill owns the artifact contract before production: the message, evidence
or data claims, copy inventory, layout grammar, style route, generation or
rendering path, and proof. It composes with [visual-design](../visual-design/SKILL.md),
[data-viz](../data-viz/SKILL.md), [diagramming](../diagramming/SKILL.md),
[social-content](../social-content/SKILL.md), [image-generation](../image-generation/SKILL.md),
[frontend-craft](../frontend-craft/SKILL.md), and [visual-qa](../visual-qa/SKILL.md)
when those downstream owners are the right production or proof surface.

Prefer deterministic layout first when the infographic is text-heavy, contains
UI labels, or must preserve exact words. Use bitmap generation only after the
copy, panels, annotations, and visual hierarchy are specified, or when the
output is intentionally painterly and exact text is not the proof target.

## Skill Signature

```text
create_infographic(brief, source_material?, style_ref?, output_context?)
  -> infographic_packet + asset_plan + evidence
state: reads(request, source material, optional ticket/spec/data, style references, existing brand or platform constraints); writes(brief/spec/prompt/rendered assets when requested)
gates: message_claims_named; copy_inventory_complete; layout_legible; style_route_selected; production_path_named; proof_or_blocker_recorded
routes: visual-design | data-viz | diagramming | social-content | image-generation | frontend-craft | visual-qa
fails: decorative poster with unclear point; hallucinated data; text-dense bitmap with unreadable labels; copied reference without adaptation; no local artifact path
```

```text
InfographicPacket = {
  audience,
  central_thesis,
  claims_or_data,
  copy_inventory,
  layout_spec,
  style_profile,
  production_route,
  proof_plan
}
```

## Phase Boundary

Run Tier 0 phases inline for normal one-off infographics. Use `social-content`
when the infographic is a carousel or platform campaign, `data-viz` when chart
correctness is the core task, `frontend-craft` when the output must be a web UI
or deterministic HTML/SVG renderer, and `visual-qa` when the final rendered
asset must be judged against a visual baseline.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the brief and source truth.
   - [ ] Read `qa_checklist.md` before drafting and apply it as preflight
     guardrails.
   - [ ] Identify audience, objective, central thesis, output format, aspect
     ratio, source material, claims or data, and whether exact text fidelity is
     required.
   - [ ] Ask only for missing inputs that would change claims, legality,
     spend, external publishing, or irreversible production choices.
- [ ] 2. Choose the infographic job.
   - [ ] `product_state_storyboard`: several product screens, states, or
     workflow moments shown together.
   - [ ] `annotated_dashboard`: one or more UI states with callouts explaining
     data, policy, or behavior.
   - [ ] `data_story`: charts, metrics, scorecards, tables, or comparisons.
   - [ ] `process_map`: steps, actors, dependencies, or before/after flow.
   - [ ] `social_infographic`: carousel, post image, thumbnail, or platform
     asset; route copy/platform work through [social-content](../social-content/SKILL.md).
   - [ ] `implementation_asset`: deterministic HTML/SVG/canvas or UI-bound
     visual; route production through [frontend-craft](../frontend-craft/SKILL.md).
- [ ] 3. Choose the style route.
   - [ ] For the dense monochrome hand-drawn SaaS product storyboard style,
     load [handdrawn SaaS wireframe](references/handdrawn-saas-wireframe.md)
     and use method address `infographic:handdrawn-saas-wireframe`.
   - [ ] For chart-heavy work, use [data-viz](../data-viz/SKILL.md) before
     final art direction.
   - [ ] For system maps or architecture explanations, use
     [diagramming](../diagramming/SKILL.md) before visual polish.
   - [ ] For a different user-provided style reference, extract transferable
     layout, density, line, type, annotation, and proof constraints before
     writing generation prompts.
- [ ] 4. Build the packet before producing assets.
   - [ ] Write a copy inventory: exact headings, labels, captions, callouts,
     numbers, chart labels, and table text.
   - [ ] Write a layout spec: canvas size, grid, panel count, hierarchy,
     components, annotation zones, and responsive or crop constraints.
   - [ ] Separate facts from illustrative placeholder data.
   - [ ] Choose production route: deterministic render, Mermaid/diagram,
     HTML/SVG/canvas, Codex-native imagegen, [image-generation](../image-generation/SKILL.md),
     or mixed deterministic base plus bitmap texture.
- [ ] 5. Produce or hand off the asset.
   - [ ] For exact-text outputs, render or specify deterministic text layers
     before optional texture/style passes.
   - [ ] For bitmap generation, provide a prompt that names layout, visual
     grammar, negative constraints, and text-fidelity risk.
   - [ ] Save prompts, source refs, rendered files, and notes inside the
     workspace when external generation or rendering happens.
- [ ] 6. Verify and finish.
   - [ ] Apply `qa_checklist.md` again to the packet and any final artifact.
   - [ ] Use [visual-qa](../visual-qa/SKILL.md) when the asset is user-visible,
     client-facing, or meant to prove style match.
   - [ ] Return the infographic packet, final asset paths or production handoff,
     verification result, and any blockers.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Use this compact output shape for one-off work:

```text
Infographic Packet:
Audience:
Central thesis:
Claims/data:
Copy inventory:
Layout spec:
Style profile:
Production route:
Proof plan:
Artifacts:
```

Positive example fixture:
[hand-drawn SaaS wireframe](examples/handdrawn-saas-wireframe/example.md).

## Gotchas

- Do not turn an infographic into a decorative poster before the message is
  true and inspectable.
- Do not invent source metrics. Mark placeholders as illustrative.
- Do not rely on image generation for exact UI text, tables, or small labels
  unless the output will be manually corrected or deterministically rendered.
- Do not copy a reference image's private product, brand, or data unless the
  user supplied it for reuse; extract a transferable visual method instead.

## Reference Map

- [handdrawn-saas-wireframe.md](references/handdrawn-saas-wireframe.md) - load
  when the user wants the monochrome hand-drawn SaaS dashboard/storyboard style
  shown in the included reference image.

## Output

Return an `Infographic Packet`, local artifact paths or a production handoff,
and a proof note. If no final image was generated, name the exact next command,
tool, or owner needed to produce it.
