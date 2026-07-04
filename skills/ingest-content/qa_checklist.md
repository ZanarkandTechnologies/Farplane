---
title: Ingest Content QA Checklist
owner: ingest-content
status: active
kind: qa-checklist
created_at: 2026-07-04
updated_at: 2026-07-04
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
  `title`, `description`, and optional `anchor`.
- [ ] `source-honesty`: The analysis states what is known from the source or
  note and does not invent unseen frames, audio, transcripts, or timing.
- [ ] `usefulness-extracted`: The saved record contains reusable creative
  elements, remix constraints, or generation/recreation notes, not only a
  summary.
- [ ] `storage-verified`: The final proof includes a Resource Bank capture
  handle or precise blocker.
- [ ] `retrieval-verified`: Tasty Pack/Inspiration Pack retrieval can find the
  saved capture and return `source`, `analysis`, `elements`, and tags/facets on
  `source`.

## Reviewer Prompt

```text
Review the ingest-content result against
skills/ingest-content/qa_checklist.md. Return pass, violation, or blocked for
each failed check. Focus on whether the capture is compact, honest about source
limits, and useful for future content plans without requiring default evidence
objects.
```
