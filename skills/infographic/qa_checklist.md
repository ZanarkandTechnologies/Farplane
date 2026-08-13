---
template_uses:
  skill-qa-checklist: "0.1.0"
---

# Infographic QA Checklist

Read this checklist before creating an infographic packet, then apply it again
to the finished packet or asset. Record each item as `pass`, `violation`,
`not_applicable`, or `deferred` in the final proof note, audit, or ticket.

## Checklist

- [ ] `message_clear`: The artifact has one central thesis and each panel,
  chart, or section supports it.
- [ ] `source_truth`: Facts, metrics, and claims are either sourced from the
  user's material or explicitly marked as illustrative placeholders.
- [ ] `copy_inventory`: Exact visible text is listed before production,
  including titles, labels, numbers, captions, and callouts.
- [ ] `layout_legible`: The layout has a named canvas, grid, scan order,
  hierarchy, and crop/aspect-ratio constraints.
- [ ] `density_match`: The artifact has enough information for the selected
  style. For `infographic:handdrawn-saas-wireframe`, each large panel should
  contain multiple UI regions, repeated shell details, and 2-4 annotations;
  sparse panels are a style mismatch.
- [ ] `style_route`: A style profile or method reference is selected, with
  adopt/adapt/reject boundaries from any reference image.
- [ ] `text_fidelity`: Text-heavy outputs use a deterministic or correction
  route; bitmap-only generation is accepted only when exact labels are not the
  proof target.
- [ ] `annotation_quality`: Callouts explain behavior, state, evidence, or
  decision points rather than generic praise.
- [ ] `production_path`: The packet names the next owner/tool: deterministic
  render, imagegen, ai-image-advisor, impl-plan, social-content, or
  visual-qa.
- [ ] `artifact_locality`: Generated images, prompts, source refs, and notes
  are saved inside the workspace when production happens.
- [ ] `final_proof`: The final answer includes the asset path or a blocker, plus
  the checklist verdict and any visual QA or review artifact when required.
