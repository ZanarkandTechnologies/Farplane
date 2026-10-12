# Infographic

Owner: [ai-image](../SKILL.md) `infographic` mode. Load when the request is a
visual explanation, product-state storyboard, annotated dashboard, process map,
data story, or slide-like image whose value depends on composition and copy
hierarchy. Folded from the former infographic skill.

## Packet

```text
InfographicPacket = {
  audience, central_thesis, claims_or_data, copy_inventory,
  layout_spec, style_profile, production_route, proof_plan
}
gates: message_claims_named; copy_inventory_complete; layout_legible;
       style_route_selected; production_path_named; proof_or_blocker_recorded
fails: decorative poster with unclear point; hallucinated data; text-dense
       bitmap with unreadable labels; copied reference without adaptation;
       no local artifact path
```

## Steps

1. **Bind the brief and source truth.** Audience, objective, central thesis,
   output format, aspect ratio, source material, claims or data, and whether
   exact text fidelity is required. Ask only for inputs that change claims,
   legality, spend, publishing, or irreversible choices.
2. **Choose the job.**
   - `product_state_storyboard`: several product screens or workflow moments.
   - `annotated_dashboard`: UI states with callouts on data, policy, behavior.
   - `data_story`: charts, metrics, scorecards, tables, comparisons; read the
     [data-visualization reference](../../../docs/fundamentals/data-visualization.md)
     before art direction.
   - `process_map`: steps, actors, dependencies, before/after flow; draft the
     Mermaid structure inline before visual polish.
   - `social_infographic`: carousel or post image; copy and platform work go to
     [social-content](../../social-content/SKILL.md).
   - `implementation_asset`: deterministic HTML/SVG/canvas or UI-bound visual;
     production goes to [impl-plan](../../impl-plan/SKILL.md).
3. **Choose the style route.** For the dense monochrome hand-drawn SaaS
   storyboard, load [handdrawn-saas-wireframe](handdrawn-saas-wireframe.md).
   For another user-supplied reference, extract transferable layout, density,
   line, type, annotation, and proof constraints before writing prompts.
4. **Build the packet before producing assets.**
   - Copy inventory: exact headings, labels, captions, callouts, numbers, chart
     labels, table text.
   - Layout spec: canvas size, grid, panel count, hierarchy, components,
     annotation zones, crop constraints.
   - Separate facts from illustrative placeholder data; mark placeholders.
   - Production route: deterministic render (HTML/SVG/canvas, Mermaid), image
     model, or mixed deterministic text layer over a generated texture.
5. **Produce.** Exact-text outputs render text deterministically first; the
   image model only supplies texture, illustration, or style. A bitmap prompt
   names layout, visual grammar, negative constraints, and text-fidelity risk.
6. **Verify.** Open the rendered file and check every label against the copy
   inventory. Use [qa](../../qa/SKILL.md) when the asset is client-facing or must
   prove a style match.

## Template

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

Positive fixture: [hand-drawn SaaS wireframe](../examples/handdrawn-saas-wireframe/example.md)
(reference image, accepted dense output PNG, and its deterministic SVG source).

## Gotchas

- An infographic is not a decorative poster; the message must be true and
  inspectable first.
- Do not invent source metrics. Mark placeholders as illustrative.
- Image models cannot be trusted with exact UI text, tables, or small labels;
  render them deterministically or composite the real screen.
- Do not copy a reference image's private product, brand, or data unless the
  operator supplied it for reuse; extract the visual method instead.
