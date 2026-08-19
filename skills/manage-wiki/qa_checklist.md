---
title: Manage Wiki QA Checklist
owner: manage-wiki
status: active
kind: qa-checklist
applies_to:
  - manage-wiki
---

# Manage Wiki QA Checklist

Read this before staging Wiki changes and apply it again before publishing.

```text
manage_wiki_check(source, publication_intent, staged_delta, resolution_receipt,
                  sync_result?)
  -> pass | revise | blocked
```

- [ ] `source_and_scope`: every article, field, claim, alias, coordinate, and
  association is supported by the bound source; uncertainty survives; only
  touched prose and explicit entity scope were scanned; existing links, code,
  citations, generic nouns, and unrelated sources were excluded; private or
  sensitive dossiering is rejected rather than staged.
- [ ] `resolution_safety`: exact lookup precedes fuzzy retrieval; only one
  unique exact ID/name/alias auto-links; every plausible FTS5/prefix/trigram
  candidate was checked against canonical Markdown, kind, location, nearby
  entities, and source evidence.
- [ ] `intent_ambiguity_and_publish_gate`: publication intent is exactly
  `preview` or `apply`; explicit Wiki write verbs select apply, explicit
  preview/no-write language or no Wiki write direction selects preview, and
  conflicting language blocks publication while returning a preview. Multiple plausible identities produce
  `ambiguity`; the complete changeset passes source, notation, ID, and link
  checks before publishing. Source/privacy gaps, ambiguity, or failed validation return
  an explicit outcome and staged diff without merges, duplicates, links,
  canonical writes, or projection mutation; absent or unbounded source input
  is `skip_source_gap`, not `blocked`.
- [ ] `article_and_edge_integrity`: unrelated frontmatter/prose remain intact;
  new IDs, sources, and question refs resolve; no duplicate claim, inferred
  predicate, inverse edge, self-link, unresolved link, or direct projection
  edit was introduced.
- [ ] `projection_and_receipt_proof`: Wiki doctor passed; apply sync succeeded
  in one command containing every changed `--path` and replaced claims by
  originating page, while preview performed no writes;
  generated SQLite/JSON refs and
  diagnostics are named; rebuild remains reproducible; every mention records
  candidates, evidence, decision, outcome, page, and no-op/blocker state;
  replacement diffs do not duplicate old and new sentences; plausible
  candidates are contrasted individually; projection paths are explicit; and
  previews distinguish expected commands from observed execution evidence,
  mark unknown view paths as unknown, and do not claim unobserved projection
  effects.
