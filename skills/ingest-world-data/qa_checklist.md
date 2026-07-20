---
title: Ingest World Data QA Checklist
owner: ingest-world-data
status: active
kind: qa-checklist
applies_to:
  - ingest-world-data
---

# Ingest World Data QA Checklist

Read this checklist before editing CRM state and apply it again after compile.

```text
ingest_world_data_check(capture, markdown_delta, compile_result)
  -> pass | revise | blocked
```

- [ ] `source_fidelity`: every created entity, changed field, coordinate, and
  association is supported by the bound source or explicitly selected facts;
  uncertainty is preserved and unspecified transcripts were not searched.
- [ ] `resolution_safety`: IDs, normalized names, aliases, kinds, and locations
  were searched; plausible duplicates are reported without a silent merge.
- [ ] `markdown_preservation`: unrelated frontmatter and prose remain intact,
  no duplicate claim was added, and generated JSON was not hand-edited.
- [ ] `association_integrity`: each new edge comes from one explicit resolved
  `[label](crm:id)` in a factual sentence; no self-link, inferred predicate,
  inverse relationship, or unresolved link remains. When an explicit question
  is bound, every retained claim block cites one resolved stable `q-*` footnote
  with matching exact question text across touched entities; optional session
  provenance is not treated as identity, and no turn ID is stored.
- [ ] `projection_proof`: paired coordinates are numeric and in range, the CRM
  compiler passes for invocation-owned changes, both projections exist, and
  the receipt names created, updated, skipped, ambiguous, and issue outcomes.
