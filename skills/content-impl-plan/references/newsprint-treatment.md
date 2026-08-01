---
title: Newsprint Treatment
status: active
owner: content-impl-plan
kind: reference
created_at: 2026-08-02
updated_at: 2026-08-02
---

# Newsprint Treatment

Load this reference when the operator, Brand Kit, or supplied reference calls
for newspaper, newsprint, scanned-paper, or editorial-print treatment.

```text
plan_newsprint_treatment(reference_evidence, brand_kit?, accepted_assets, final_size)
  -> evidence_classification
   + paper_surface_packet
   + subject_print_packet
   + compositing_packet
   + final_resolution_receipt
```

## Evidence boundary

Classify the observed texture before describing a recipe:

- `source_baked_scan`: grain, fibers, uneven ink, or photographic noise is
  already present in the supplied newspaper scan or photograph.
- `demonstrated_added_effect`: transcript, controls, layer stack, or before/after
  evidence explicitly shows a texture/filter operation.
- `operator_requested_style`: the operator wants the visible result, but the
  source does not prove how it was made.

Appearance alone cannot support an exact named-filter, blend-mode, opacity, or
effect-stack claim. Preserve that uncertainty in the production plan.

## Clean-room production recipe

Treat page surface and printed subject as separate jobs.

### Paper surface

1. Route discovery to `asset-advisor` and select a rights-cleared raster paper
   or scan plate with real fibers and low-frequency tonal variation. CSS noise
   or procedural grain alone is not a paper asset.
2. Normalize the page toward a quiet neutral or Brand-Kit-approved stock color.
   Avoid sepia, stains, tears, and full-frame distress unless the story requires
   actual archival damage.
3. Composite the raster plate in page/object coordinates so it moves and scales
   with the newspaper. Start with restrained multiply or soft-light blending;
   calibrate opacity and texture contrast against rendered evidence rather than
   treating a numeric range as brand truth.
4. If the grain disappears at delivery size, increase the plate's useful local
   contrast or blend strength and rerender. Do not compensate with unrelated
   high-frequency noise across every pixel.

### Printed subject

1. Prepare photographs or cutouts separately with deliberate grayscale and
   contrast.
2. Apply controlled halftone or dithering at a scale that remains legible after
   final resizing; keep alpha edges crisp.
3. Use restrained registration offset or one accent family only when it supports
   hierarchy. Do not outline every object.

### Layer order

```text
paper stock color
-> raster paper/scan plate
-> rules, type, and prepared printed subjects
-> page-bound annotations
-> restrained optical finish, if required
```

The paper plate belongs below typography and annotations. A final finish may
soften digital perfection, but it cannot replace the actual paper surface or
subject-print treatment.

## Brand Kit placement

A recurring approved newsprint identity belongs in a Brand Kit `visual` element
only when the operator approves a stable example and recipe. Store:

- a displayable `goldenExample` for the accepted paper/print result;
- a `goldenRecipe` naming the accepted raster plate, stock color, subject
  contrast/halftone behavior, accent boundary, and final-resolution checks;
- provenance and rights for every reusable texture asset.

Do not create a third-party-named Brand Kit merely because one reference is
attributed to that publisher. Keep a source observation as inspiration until
the operator approves a rights-safe local identity.

## Proof

Creative lock requires:

- texture-off versus texture-on comparison at final delivery size;
- one full-frame crop showing a quiet, coherent surface;
- one close crop showing fibers/tonal variation and controlled printed detail;
- page-motion frames proving the surface stays registered to the page;
- independent style review confirming texture is visible without reducing text
  or annotation readability.

The mechanical scene manifest records these replayable fields:

```text
treatment_receipt:
  texture_classification: source_baked_scan | demonstrated_added_effect | operator_requested_style
  raster_paper_asset_ref: <accepted raster path or stable asset locator>
  raster_paper_rights_ref: <license, provenance, or operator-owned source receipt>
  page_or_object_coordinates: true
  full_frame_texture_proof_ref: <final-resolution frame>
  close_crop_texture_proof_ref: <final-resolution crop>
  final_resolution_halftone_scale: <measured or inspectable subject-print scale>
  crisp_alpha: true
  subject_mask_final_resolution_proof_ref: <final-resolution subject crop>
  background_crop_final_resolution_proof_ref: <final-resolution paper crop>
  remotion_compositing_receipt_ref: <deterministic page-bound render receipt>
  independent_style_review_ref: <review receipt>
  rejection_gate: global noise or a tiny halftone swatch cannot pass
```

Asset Advisor owns texture discovery and rights. The image owner owns prepared
subject treatment. Remotion owns deterministic compositing and delivery-size
frames. The parent content plan records all receipts but does not self-certify
downstream pixels.
