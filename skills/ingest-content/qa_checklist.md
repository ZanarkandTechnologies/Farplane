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

- [ ] `note-selection-cardinality`: Broad analysis does not create broad
  Creative Elements. A narrow note promotes only its evidenced selected
  components; an explicit complete-system note may promote several or all six
  evidenced kinds. There is no fixed one-element or six-element default.

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
- [ ] `discovery-canonicalization`: Pinterest pins and curated-gallery items
  attempt canonical-original resolution. A resolved capture preserves both the
  original and discovery provenance; an unresolved item remains
  inspiration-only with `rights_status: unknown`. No license is inferred and no
  source-specific schema field is added. The final packet exposes
  a resolution attempt with method/candidate URLs/evidence/access limit or
  no-match reason, `source_resolution`, storage handle/blocker, Tasty Pack
  retrieval verdict, and `tickets: []` for save-only intent. Failure to resolve
  the original does not block a URL/note capture; it only blocks unsupported
  element capsules or a write when storage itself is unavailable.
  `attempt_method: not_attempted` fails unless the packet records the exact
  browser/web command or tool failure that prevented the attempt.
  When storage is unavailable, a complete `pending_capture_payload` preserves
  the unresolved inspiration-only capture for deterministic rerun; a prose
  suggestion to save it later is insufficient.
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
- [ ] `video-skill-benefit-scan`: Every video ingestion ends with a lightweight
  skill-benefit scan after retrieval verification. Non-video sources mark it
  `not_applicable` unless they explicitly teach a reusable workflow. The scan
  carries `retrievalStatus: verified | blocked` and cannot report `complete`
  when retrieval is blocked.
- [ ] `skill-finding-grounding`: Skill findings are based on operational
  techniques visible in transcript, frames, analysis, or precise source
  anchors; each finding names `skill`, `status`, `evidenceAnchor`, `benefit`,
  `confidence`, and `recommendedRoute`. Purely aesthetic inspiration returns
  `skill_findings: []` with scan-level route `none`; it does not invent a
  downstream skill-improvement route.
- [ ] `skill-owner-comparison`: The scan shortlists owners through
  `docs/skills/registry.jsonl`, inspects only likely owner skills, and uses
  exactly `covered`, `augment`, `missing`, `reject`, or `defer` rather than
  declaring every novel-looking technique a new skill.
- [ ] `skill-primary-owner`: When one technique overlaps multiple skills, the
  result chooses one primary owner for the proposed change, explains the
  boundary, and does not return unresolved duplicate `augment` findings.
- [ ] `skill-grounding-honesty`: The result claims registry or owner-skill
  inspection only for files actually read and labels unavailable comparisons
  instead of fabricating local grounding.
- [ ] `skill-action-boundary`: The scan does not edit skills, create
  skill-improvement tickets, or add Resource Bank schema fields. Credible
  workflow-teaching videos route to `harness-scout`; accepted owner-local
  changes may later route to `skill-maintenance`, and reviewed ownerless gaps
  may later route to `skill-creator`.
- [ ] `style-profile-compilation`: An explicit style-profile request reuses a
  verified capture, preserves provenance and observation/inference boundaries,
  blocks collisions without replace authority, copies no protected source
  media, and writes collocated `profile.md`, `prompts.md`, and `example.md`.

## Reviewer Prompt

```text
Review the ingest-content result against
skills/ingest-content/qa_checklist.md. Return pass, violation, or blocked for
each failed check. Focus on whether every element has an honest, same-source
what/why/example/recipe capsule, whether recipes are operational rather than
generic, whether retrieval/promotion preserve that capsule without adding
parallel evidence or recipe collections, and whether video ingestion ends with
an evidence-backed, non-mutating skill-benefit scan.
```
