---
template_uses:
  skill-qa-checklist: "0.1.1"
---

# Editing Advisor QA Checklist

- [ ] `source-integrity`: Resource Bank `editing` elements remain the reusable
  corpus; Brand Kit entries are approved snapshots and skill findings are not
  production recipes. Every candidate preserves source/provenance, description,
  why, golden example, golden recipe, anchor, and tags when available. Brand
  policy prose stays in a separate policy table unless it is itself a complete
  CreativeElement, and retrieval counts as attempted only after an observable
  adapter call. Advisor-authored or brief-inferred operations stay in original
  edit direction/recipe records with `advisor_authored_from_brief` provenance;
  they never masquerade as user-supplied or reusable creative patterns. Every
  reusable-pattern request returns exactly one of `selected_fit`,
  `searched_no_fit`, or `adapter_blocked`; an empty pattern table is never
  presented as a completed search.
- [ ] `selection-and-compatibility`: Every candidate is visibly `use`, `adapt`,
  `reject`, or `block`; selected patterns pass story, brand, timing, asset,
  renderer, accessibility, and mutual-compatibility checks. Incomplete selected
  packets and decorative effect piles block readiness.
- [ ] `timed-recipe`: One timing master governs a fully ordered frame- or
  time-addressed recipe. Every step names scene/state, method, operation,
  usable parameters, dependencies, pattern ref, owner, and acceptance check.
  When exact timing or files are missing, the output still includes the
  strongest provisional recipe using one declared relative basis and marks the
  exact remapping/file blockers; it does not collapse into an input checklist.
  Canonical recipe coordinates never mix seconds, frames, normalized ranges,
  and verbal cues; any conversion is labeled derived metadata. When voiceover
  or a measured voice cue sheet is in scope, it is the canonical timing master;
  normalized scene timing remains provisional until remapped to it.
- [ ] `owner-boundaries`: Every unprepared media dependency returns to Asset
  Advisor, which explicitly owns selection of image, video, avatar, or audio
  realization children. Deterministic rendering stays with Remotion. The
  advisor does not mutate the corpus, select generation children, generate
  provider media, or claim rendered pixels.
  Every recipe row repeats a named renderer owner; deterministic assembly
  defaults provisionally to Remotion when the caller omits the renderer.
- [ ] `observable-handoff`: The renderer packet includes files or exact
  blockers, layer/composition order, captions, transitions, motion, output
  spec, and frame/range or render checks; material direction receives an
  independent review receipt before readiness is claimed. Missing files still
  carry expected output paths and null accepted-file refs.
