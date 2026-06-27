---
title: "Docs Consolidation Workflow"
status: active
owner: interval-update
kind: workflow-reference
template_uses:
  skill-template: "0.3.2"
---

# Docs Consolidation Workflow

## Context

Use this workflow when an interval needs to identify stale, duplicated, or
misplaced durable documentation and route it to the right owner. It is a
planning and routing workflow for interval reports, not a broad autonomous docs
rewrite.

Use `update-memory` for whole-project context refresh across README, memory,
history, lessons, troubles, and docs deltas. Use `consolidate` for
keep/merge/move/delete decisions over docs and memory surfaces. Use
`documentation` for substantive reader-quality rewrites or durable docs-as-code
changes. Route stale feature rows back to the owning `docs/systems/*.md`
metadata source;
`docs/systems/registry.jsonl` and `docs/features/registry.jsonl` are generated
output, not interval write targets.

## Workflow Signature

```text
docs_consolidation(context_bundle, review_window, planning_window,
                   workflow_findings?, cap?)
  -> consolidate_docs_handoffs
   + stale_doc_candidates
   + duplicate_doc_candidates
   + update_memory_handoffs
   + documentation_handoffs
   + source_gaps

state: reads(context_bundle, README.md?, docs/**/*.md?, docs/MEMORY.md?,
             docs/HISTORY.md?, docs/LESSONS.md?, docs/TROUBLES.md?,
             doc reference reports?);
       writes(parent_interval_update_report_section)
gates: docs_owner_identified; source_refs_cited; no_append_only_rewrite;
       no_unbounded_doc_cleanup; handoff_before_mutation;
       generated_registry_not_hand_edited
routes: consolidate | update-memory | documentation | knowledge-tidier |
        ticket delta | direct no-change
fails: rewrites docs from interval context alone; deletes append-only ledgers;
       treats every stale note as a docs task; creates an artifact graveyard;
       hand-edits generated registries
```

## Source Contract

Default sources from the context bundle:

- README and project docs referenced by recent work or interval findings.
- `docs/MEMORY.md`, `docs/HISTORY.md`, `docs/LESSONS.md`, and
  `docs/TROUBLES.md` when present.
- recent interval reports, ticket closeouts, review artifacts, and generated doc
  reference reports when present.
- generated system and feature registry freshness reports when capability
  metadata changed.

## Todo List

- [ ] 1. Bind the docs window.
  - [ ] Confirm `review_window`, `planning_window`, and `cap`.
  - [ ] Read only docs implicated by recent work, stale references, generated
        graph/report evidence, or explicit context refs.
  - [ ] Mark missing optional docs or reports as source gaps.
- [ ] 2. Classify candidates.
  - [ ] Route broad project memory/context refresh to
        [update-memory](../../../update-memory/SKILL.md).
  - [ ] Route docs or memory keep/merge/move/delete decisions to
        [consolidate](../../../consolidate/SKILL.md) with `structure =
        docs_tree | memory`.
  - [ ] Route substantive durable doc writing, reader-quality cleanup, or docs
        architecture changes to [documentation](../../../documentation/SKILL.md).
  - [ ] Route bloat or knowledge-specific scoring/rerouting to
        [knowledge-tidier](../../../knowledge-tidier/SKILL.md), which will call
        `consolidate` for the shared decision pass.
  - [ ] Route stale or duplicated `FEAT-*` records to the owning
        `docs/systems/*.md` source and regenerate the registry.
  - [ ] Create a ticket delta when the consolidation is too large for the next
        interval window.
- [ ] 3. Preserve append-only and proof surfaces.
  - [ ] Do not rewrite `docs/HISTORY.md`, `docs/LESSONS.md`, or
        `docs/TROUBLES.md` to mark items complete.
  - [ ] Do not hand-edit generated registries such as
        `docs/systems/registry.jsonl` or `docs/features/registry.jsonl`.
  - [ ] Keep detailed proof, review, and ticket evidence in their owning
        artifacts rather than copying them into summary docs.
- [ ] 4. Bound the work.
  - [ ] Default cap is 5 consolidation handoffs per weekly run.
  - [ ] Prefer the smallest useful handoff with source refs and owner surface.
  - [ ] Prefer promote-or-delete over tracked archives for stale docs unless a
        current owner explicitly requires archival context.
- [ ] 5. Record the result.
  - [ ] Write handoffs, stale candidates, duplicate candidates, source gaps, and
        deferred docs work into the interval report.

## Output

```text
consolidate_docs_handoffs:
  - owner_route:
    target_refs:
    evidence_refs:
    recommended_delta:
stale_doc_candidates:
duplicate_doc_candidates:
update_memory_handoffs:
documentation_handoffs:
source_gaps:
```
