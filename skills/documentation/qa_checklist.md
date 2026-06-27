---
title: "Documentation QA Checklist"
status: active
owner: documentation
created_at: 2026-06-23
updated_at: 2026-06-23
tags:
  - documentation
  - qa
  - docs-as-code
refs:
  - skills/documentation/SKILL.md
  - docs/features/FEAT-0060-registry-backed-documentation-os.md
  - docs/features/FEAT-0060-registry-backed-documentation-os.md
---

# Documentation QA Checklist

Use this checklist after the draft or edit pass, before claiming a durable doc
is ready. Keep the check proportional: tiny typo fixes may only need the
affected local checks, while canonical docs, public guidance, specs, runbooks,
and cross-surface policy need the full gate.

## Reader Contract

- Audience is named or obvious from the owning file.
- Doc type is clear: tutorial, how-to, reference, explanation, spec, doctrine,
  runbook, checklist, decision note, README, or registry companion.
- The intended next action is clear.
- The source of truth is linked or named.
- The main definition, decision, or workflow appears near the top.
- The doc is written for a human reader, not as hidden instructions to a future
  agent.

## Placement And Ownership

- The owning surface is the smallest durable place that should carry this truth.
- The nearest index, README, registry, or owner doc has been checked when the
  edit changes discoverability.
- Canonical claims are linked to their owner instead of copied into multiple
  docs.
- A new file was created only when the content has a distinct owner, audience,
  lifecycle, update cadence, or retrieval path.
- Content was merged into an existing file when it shares the same owner,
  audience, lifecycle, and retrieval path.
- Content was split when one file mixed tutorial/how-to/reference/explanation,
  current contract with historical research, user-facing docs with agent
  process, or reusable policy with task-local proof.
- Ticket-local plans, blockers, and proof stayed in tickets or artifacts unless
  distilled into a durable docs owner.
- Routine final ticket writeback stays with `close-ticket`; this checklist only
  covers substantive durable documentation changes.

## Density And Shape

- README and index pages are sparse maps with links and current orientation,
  not full policy dumps.
- Specs and contracts are dense, precise, and testable enough to govern future
  work.
- Runbooks and how-to guides are executable, ordered, and light on background.
- References are complete and scannable, with explanation moved to conceptual
  docs when it grows.
- Doctrine and fundamentals explain mental models without taking over
  implementation-specific procedures.
- Archives preserve historical context without being presented as current
  operating truth.

## Metadata And Versioning

- New durable Markdown has YAML front matter unless the owner surface forbids it
  or the file is raw prompt-loaded content.
- Existing front matter preserves local schema fields such as `status`,
  `owner`, `created_at`, `updated_at`, `refs`, `template_version`,
  `feature_refs`, `source_refs`, `supersedes`, or `last_verified`.
- `updated_at`, `status`, `refs`, and owner-specific version fields are updated
  when the material meaning changed.
- No new version field is invented unless a local owner schema already uses it.
- Front matter stays compact and contains no secrets, private handles, raw
  transcripts, bulky evidence, or long prose.

## Grounding

- Claims that depend on local repo state cite or align with canonical files.
- Claims that depend on current facts, API behavior, peer norms, standards, or
  external best practice were grounded through `reference-grounding` or a
  broader research method.
- External best practices are labeled as evidence or synthesis, not silently
  promoted to Farplane policy.
- Unsupported claims are removed, softened, or marked as local policy.
- Historical context remains only when it helps the reader understand the
  current contract.

## Terms And Definitions

- Each concept has one canonical term.
- Duplicate or competing definitions are removed unless the doc explicitly
  compares alternatives.
- Headings, examples, formulas, tables, links, and captions use the same
  vocabulary.
- Acronyms or symbols are introduced before use.
- Old names are deleted or clearly marked as retired.

## Structure And Writing

- Sections follow the reader's task order.
- Examples teach the current model and are complete enough to use.
- Tables, signatures, and checklists make action easier rather than adding
  ceremony.
- Stale sections, repeated setup, low-value boundary notes, and old examples are
  deleted instead of patched around.
- Sentences are concise without removing necessary context, articles, caveats,
  or precision.
- Paragraphs are short enough to scan, and semantic line breaks support clean
  Markdown diffs.

## Documentation Quality Scores

Use this scoring pass for material docs, public guidance, specs, runbooks, and
before/after migrations. Scores are reviewer judgment, not fake mechanical
precision. Rate each dimension `0`, `1`, or `2`:

| Dimension | 0 | 1 | 2 |
| --- | --- | --- | --- |
| Followability | Reader cannot tell what to do next. | Reader can infer next action with effort. | Reader can follow the doc without extra context. |
| Usefulness | Doc is mostly labels, history, or metadata. | Doc answers some real reader questions. | Doc helps the reader make or verify a decision. |
| Trustworthiness | Claims lack owner, evidence, or freshness. | Most claims are grounded, with gaps visible. | Claims point to owners, evidence, limits, and checks. |
| Concision | Bloated, repetitive, or noisy. | Some redundancy, but still scannable. | Every section earns its space for the doc type. |
| Findability | Owner, audience, or source of truth is unclear. | Discoverable with some link-following. | Owner, audience, source of truth, and related docs are obvious. |
| Maintainability | Future edits are risky or ambiguous. | Update path exists but has weak boundaries. | Metadata, owner, checks, and update/rollback path are clear. |

Recommended summary:

```text
doc_quality_score =
  followability + usefulness + trustworthiness + concision + findability + maintainability
```

Interpretation:

- `10-12`: ship-ready for the doc type.
- `8-9`: usable, with named follow-up or review notes.
- `6-7`: revise before broad rollout.
- `0-5`: do not promote; fold, rewrite, or delete.

Guard metrics:

- Relevant validators still pass.
- Link/reference count does not rise from copied boilerplate.
- Word or line count growth is justified by higher followability/usefulness, not
  template padding.
- No required metadata, owner, evidence, or limits are removed.

Anti-metrics:

- Optimizing for longer docs.
- Adding every template section even when it does not help the reader.
- Hiding uncertainty behind confident prose.
- Improving score by deleting necessary caveats, proof, or ownership details.

## Checks To Run

Adapt the patterns to the actual edit:

```bash
rg -n "old_term|duplicate_term|removed_section" path/to/doc.md
rg -n "the agent should|must define|do not introduce|for future agents" path/to/doc.md
rg -n "^## |^### " path/to/doc.md
```

When links, canonical surfaces, or metadata changed:

```bash
python3 bin/validators/check_doc_refs.py
python3 bin/validators/check_doc_parity.py
```

When skill metadata, Markdown links, or todo lists changed:

```bash
python3 skills/skill-maintenance/scripts/check_skills.py --write
```

## Completion Gate

- Terms are consistent across prose, headings, code blocks, tables, examples,
  links, and captions.
- Every definition has one owner.
- Every example teaches the current model.
- Stale sections were deleted instead of preserved.
- Touched links, refs, registries, or metadata were refreshed.
- Relevant validators or searches passed, or failures are recorded with
  explicit deferrals.
- Material canonical docs, public guidance, cross-surface policy, or completion
  claims have a review route or an explicit reason review was skipped.
