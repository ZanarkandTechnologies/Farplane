---
template_uses:
  skill-method-reference: "0.1.0"
---

# Doc Architecture

Use this reference when placement, split/merge/delete, density, lifecycle, or
owner-surface choice is unclear.

```text
doc_architecture(doc_delta, repo_state?) -> owner_surface + doc_type + disposition + evidence
state: reads(target doc?, nearest index/README, docs/systems/documentation-os.md, relevant owner docs); writes(decision note or target doc)
gates: owner_surface_named; duplicate_truth_checked; reader_path_clear
fails: creates a new doc for content with an existing owner; archives stale lore by default
```

## Use When

- A doc request could belong in more than one surface.
- Content may need to be merged, split, deleted, or kept ticket-local.
- The doc is growing into mixed tutorial, reference, explanation, policy, and proof.

## Inputs

```text
input_packet:
  required:
    doc_delta:
  optional:
    target_file:
    nearest_owner:
    evidence_refs:
  source_refs:
    - docs/systems/documentation-os.md
    - docs/features/README.md
    - docs/systems/README.md
```

## Workflow

1. **Name the reader path.** Identify who reads this, what they are trying to
   decide or do, and where they would naturally look.
2. **Check owner fit.** Prefer an existing owner when audience, lifecycle,
   update cadence, and retrieval path match.
3. **Choose disposition.**
   - `keep_here`: content fits the current owner.
   - `move`: content is useful but belongs to another owner.
   - `split`: one file mixes different doc jobs or lifecycles.
   - `merge`: content duplicates an existing owner.
   - `ticket_artifact`: content is task-local proof or planning.
   - `delete`: content is stale lore, duplicate truth, or no longer useful.
4. **Choose density.** Use sparse maps for indexes, executable steps for
   runbooks, dense contracts for specs, complete but scannable entries for
   references, and conceptual prose for fundamentals.

## Output Shape

```text
doc_architecture_decision:
  reader:
  owner_surface:
  doc_type:
  disposition:
  source_of_truth:
  metadata_implications:
  proof_route:
```

## Quality Gates

- New files have a distinct owner, audience, lifecycle, or retrieval path.
- Canonical claims link to an owner instead of duplicating long doctrine.
- Stale content is folded into an active owner or deleted, not archived by habit.

## Bad Output

- "Create a doc because this is important" without owner, reader, or lifecycle.
- Keeping proof or planning artifacts in durable docs before distillation.
