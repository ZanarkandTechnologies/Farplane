---
title: Ingest Content QA Checklist
owner: ingest-content
status: active
kind: qa-checklist
created_at: 2026-07-04
updated_at: 2026-07-22
applies_to:
  - ingest-content
  - resource-bank-ingestion
---

# Ingest Content QA Checklist

Use this before claiming a Resource Bank ingestion is saved, and after changing
the skill contract.

## Checks

- [ ] `capture-shape`: The output stores source/ref, operator note or focus,
  optional top-level transcript, freeform `analysisMarkdown`, selected creative
  elements, and tags/facets when useful.
- [ ] `element-shape`: Every creative element passes
  `is_element(value) = independently selectable && independently conditionable
  from an example && owned by a recognizable production step`, uses one of the
  six canonical kinds (`format`, `storyboard`, `visual`, `character`, `audio`,
  `editing`), and includes non-empty `title`, `description`, `whyItWorks`, one
  `goldenExample { assetId, description? }`, and one non-empty `goldenRecipe`,
  plus optional `anchor`/`pinned`; no `hook`, `copy`, `constraint`,
  `director`, `layout`, or `pacing` kind, element timing, recipe
  object/collection, or production-pattern record is added. Hook folds into
  storyboard opening beat; semantic copy folds into storyboard; subtitle
  rendering/timing folds into editing; constraints are production policy or
  Brand Kit prompt content.
- [ ] `selection-gate`: Every newly stored CreativeElement also passes
  `should_store_element(value, note) = is_element(value) &&
  explicitly_selected_for_reuse(value, note)`. Unselected observations remain
  in capture analysis, a capture may contain zero elements, and whole-source
  context is not represented as unpinned CreativeElement rows.
- [ ] `analysis-shape`: Transcript is optional and top-level. All other
  source-specific interpretation is one freeform Markdown value; headings such
  as Breakdown, Why It Works, and Reuse Notes remain prose sections rather than
  dedicated storage fields.
- [ ] `example-ownership`: Every `goldenExample.assetId` resolves to an asset
  created by the same ingestion job. The chosen asset and optional description
  identify the specific visual, audio, passage, layout, or source quality worth
  conditioning on; one unhelpful whole-source asset is not repeated blindly.
- [ ] `recipe-quality`: Each `goldenRecipe` is a concrete, rights-safe,
  kind-specific prompt that recreates the element's function. It does not
  merely restate `description`, use generic style adjectives, or repeat the
  same recipe across unrelated element kinds.
- [ ] `character-elements`: Distinctive personas, archetypes, guides, hosts,
  mascots, or recurring character systems are extracted as `kind: character`
  when they are a reusable part of the reference; they follow the same
  note-backed pinning rule as every other element kind.
- [ ] `rights-safe-character-remix`: Character/persona elements that resemble a
  real person, actor performance, brand mascot, or protected character include
  production-policy or Brand Kit prompt text that avoids copying likeness,
  exact styling, name, voice, catchphrases, source frames, logos, or branded
  expression.
- [ ] `source-honesty`: The analysis states what is known from the source or
  note and does not invent unseen frames, audio, transcripts, or timing.
- [ ] `selected-music-recognition`: When the note explicitly likes or asks to
  identify the music/song/beat/audio bed, the result includes a recognition
  match or an honest no-match/missing-dependency/source-access limit.
- [ ] `usefulness-extracted`: Source-level analysis is context only; every
  reusable element carries its own what/why/example/recipe capsule.
- [ ] `music-rights-safe`: Recognized music is stored as attribution/research
  and reusable sonic direction, with production policy against copying
  protected music unless licensed.
- [ ] `storage-verified`: The final proof includes a Resource Bank capture
  handle or precise blocker.
- [ ] `derived-preview-real`: If a thumbnail/contact sheet/frame image exists,
  it is uploaded only after the primary asset row exists, as a derived
  `thumbnail`/`image` asset with `parentAssetId`; if no real visual was
  extracted, preview upload is explicitly skipped instead of faked.
- [ ] `pack-minimal`: Tasty Pack output remains source, analysis, and complete
  creative elements. A capsule may reference one derived Resource Bank asset by
  `goldenExample.assetId`; parallel evidence arrays, `storageId`,
  `previewAsset.storageUrl`, recipe collections, and production-pattern objects
  stay out of the active pack contract.
- [ ] `retrieval-verified`: Tasty Pack retrieval can find the
  saved capture and return `source`, `analysis.operatorNote`, `elements`,
  complete capsule fields, element `pinned`, tags/facets on `source`, and meta
  pinned/operator-note counts plus warnings.
- [ ] `promotion-verified`: When a Brand Kit destination was requested, the
  same ingest action returns a promotion receipt for the verified complete
  elements; when none was requested, promotion is explicitly skipped.
- [ ] `repurpose-ticket`: Save-only intent returns `tickets: []`.
  Future-creation intent creates or reuses one thin ticket containing the
  stable source URL/asset ID, the operator's material details, intended output,
  and `content-impl-plan` as its first operation. It does not require a reverse
  ingestion-job/task link.
- [ ] `repurpose-dedupe`: Repeating materially equivalent future-creation
  intent for the same source returns the existing ticket rather than creating
  a duplicate.

## Reviewer Prompt

```text
Review the ingest-content result against
skills/ingest-content/qa_checklist.md. Return pass, violation, or blocked for
each failed check. Focus on whether every element has an honest, same-source
what/why/example/recipe capsule, whether recipes are operational rather than
generic, and whether retrieval/promotion preserve that capsule without adding
parallel evidence or recipe collections.
```
