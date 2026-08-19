---
title: Intelligest QA Checklist
owner: skills/intelligest
status: active
kind: qa-checklist
updated_at: 2026-08-19
---

# Intelligest QA Checklist

Apply before extraction and again before the terminal receipt.

- [ ] The source has one canonical identity and the visible Content
      Intelligence job was created or reused before long analysis.
- [ ] A repeated request reuses active/ready work unless re-analysis was
      explicit; no duplicate dossier or hidden background job was created.
- [ ] Transcript/page status and limitations are explicit, and `media-ingest`
      ran only when text could not support the requested evidence; when the
      media source was missing, the receipt explicitly records
      `media-ingest: blocked_missing_source`.
- [ ] The dossier is grounded in inspected evidence; timestamps, entities,
      claims, dates, and references were not inferred to fill a schema.
- [ ] Related coverage uses an inspected 2–14 day candidate set and retains
      only distinct-source same-development or same-discussion takes.
- [ ] Broad tag, industry, creator category, or evergreen-topic overlap was
      rejected rather than presented as comparison.
- [ ] News is null unless a current public development is supported by an exact
      direct HTTPS original/official/reference document URL; internal IDs and
      generated synthesis are never cited sources.
- [ ] Wiki writeback went through `manage-wiki` and records changed, no-op,
      ambiguity, skipped, or blocked without speculative entity creation.
- [ ] Resource Bank writeback went through `ingest-content` only after explicit
      like/save/reuse intent and includes only selected reusable elements.
- [ ] The final receipt exposes job status, branch outcomes, evidence refs,
      limitations, and actionable retry/review blockers.
