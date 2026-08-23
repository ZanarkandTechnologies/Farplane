---
title: "Doc Advisor QA Checklist"
status: active
owner: doc-advisor
created_at: 2026-06-23
updated_at: 2026-06-23
tags:
  - documentation
  - qa
  - docs-as-code
refs:
  - skills/doc-advisor/SKILL.md
  - docs/features/FEAT-0060-registry-backed-documentation-os.md
  - docs/features/FEAT-0060-registry-backed-documentation-os.md
---

# Doc Advisor QA Checklist

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

- Ticket or implementation planning returns `Docs Strategy` with `outcome`,
  `doc_targets`, `no_docs_reason`, and `validation`.
- `no_docs` outcomes include a concrete reason tied to the absence of durable,
  public, canonical, workflow-facing, or user-facing doc changes.
- Docs strategy blocks do not include `close_ticket`, `documentation_skill`, or
  other routine ticket-closeout fields.
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
- Write like one capable human to another. Prefer plain, concrete words and
  name the actor, mechanism, decision, or measurable result.
- Use a specialized term only when it is more accurate than the plain word;
  define it when the intended reader may not know it.
- Split a sentence when the reader must backtrack to parse it.
- If a sentence could appear unchanged in another project's docs, make it
  specific or cut it.
- Examples teach the current model and are complete enough to use.
- Tables, signatures, and checklists make action easier rather than adding
  ceremony.
- Stale sections, repeated setup, low-value boundary notes, and old examples are
  deleted instead of patched around.
- Sentences are concise without removing necessary context, articles, caveats,
  or precision.
- Paragraphs are short enough to scan, and semantic line breaks support clean
  Markdown diffs.

## Review Routing

Use this checklist to inspect documentation while drafting and before
completion. Do not convert checklist results into a numeric documentation score.
For material docs, route readiness judgment through
`docs/review/rubrics/documentation-quality.md` and attach the failed checks,
reasons, evidence, and next action.

Guard against these fake-success patterns:

- Validators pass but the doc is still unhelpful, misplaced, or ungrounded.
- Word count shrinks while required caveats, proof, or ownership details vanish.
- A checklist result or metric label replaces reviewer judgment.
- Polished prose hides uncertainty, stale status, or missing source refs.

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
