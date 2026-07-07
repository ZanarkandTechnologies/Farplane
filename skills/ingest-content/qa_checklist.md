---
title: Ingest Content QA Checklist
owner: ingest-content
status: active
kind: qa-checklist
created_at: 2026-07-04
updated_at: 2026-07-05
applies_to:
  - ingest-content
  - resource-bank-ingestion
---

# Ingest Content QA Checklist

Use this before claiming a Resource Bank ingestion is saved, and after changing
the skill contract.

## Checks

- [ ] `capture-shape`: The output stores source/ref, operator note or focus,
  compact analysis, creative elements, and tags/facets when useful.
- [ ] `element-shape`: Creative elements use the compact shape: `kind`,
  `title`, `description`, optional `anchor`, and optional `pinned`; pinned
  elements represent note-backed operator taste, and numeric weights are not
  stored durably.
- [ ] `character-elements`: Distinctive personas, archetypes, guides, hosts,
  mascots, or recurring character systems are extracted as `kind: character`
  when they are a reusable part of the reference; they follow the same
  note-backed pinning rule as every other element kind.
- [ ] `rights-safe-character-remix`: Character/persona elements that resemble a
  real person, actor performance, brand mascot, or protected character include
  a `constraint` element that avoids copying likeness, exact styling, name,
  voice, catchphrases, source frames, logos, or branded expression.
- [ ] `source-honesty`: The analysis states what is known from the source or
  note and does not invent unseen frames, audio, transcripts, or timing.
- [ ] `usefulness-extracted`: The saved record contains reusable creative
  elements, remix constraints, or generation/recreation notes, not only a
  summary.
- [ ] `storage-verified`: The final proof includes a Resource Bank capture
  handle or precise blocker.
- [ ] `derived-preview-real`: If a thumbnail/contact sheet/frame image exists,
  it is uploaded only after the primary asset row exists, as a derived
  `thumbnail`/`image` asset with `parentAssetId`; if no real visual was
  extracted, preview upload is explicitly skipped instead of faked.
- [ ] `pack-minimal`: Tasty Pack/Inspiration Pack output remains source,
  analysis, and creative elements; evidence assets, `storageId`,
  `previewAsset.storageUrl`, and duplicated production-pattern objects stay out
  of the active pack contract.
- [ ] `retrieval-verified`: Tasty Pack/Inspiration Pack retrieval can find the
  saved capture and return `source`, `analysis.operatorNote`, `elements`,
  element `pinned`, tags/facets on `source`, and meta pinned/operator-note
  counts plus warnings.

## Reviewer Prompt

```text
Review the ingest-content result against
skills/ingest-content/qa_checklist.md. Return pass, violation, or blocked for
each failed check. Focus on whether the capture is compact, honest about source
limits, useful for future content plans, and whether storage-backed previews are
real derived UI assets rather than default evidence objects or pack payload.
```
