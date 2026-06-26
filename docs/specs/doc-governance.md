# Doc Governance

Use this file to keep Farplane's knowledge base trustworthy without turning the
repo into a markdown-lint maze.

## Goal

Treat docs as the system of record while keeping checks proportional to the kind
of truth each surface carries.

Farplane uses two kinds of documentation checks:

- structural checks for canonical entrypoints and machine-relevant contracts
- narrative audits for richer docs whose wording can change while the truth
  stays the same

## Canonical Surfaces

These surfaces define the live repo story and should stay mutually coherent:

- [AGENTS.md](/Users/kenjipcx/coding-harness/Farplane/AGENTS.md)
- [ARCHITECTURE.md](/Users/kenjipcx/coding-harness/Farplane/ARCHITECTURE.md)
- [README.md](/Users/kenjipcx/coding-harness/Farplane/README.md)
- [docs/specs/README.md](/Users/kenjipcx/coding-harness/Farplane/docs/specs/README.md)
- [docs/specs/harness-techniques.md](/Users/kenjipcx/coding-harness/Farplane/docs/specs/harness-techniques.md)
- [tickets/README.md](/Users/kenjipcx/coding-harness/Farplane/tickets/README.md)

## Documentation Architecture

Use document shape as a retrieval and ownership decision, not as a place to put
all related prose.

Create a new durable Markdown file only when the content has at least one
distinct boundary:

- different audience or reader task
- different owner or review surface
- different lifecycle, status, or update cadence
- different retrieval path, such as an index, registry, skill package, ticket,
  or archive
- different documentation type, such as tutorial, how-to, reference, or
  explanation

Merge content into an existing file when it shares the same audience, owner,
lifecycle, and retrieval path. Prefer one canonical definition with direct
links over repeated explanations in several docs.

Split a file when it mixes concerns that age or get used differently:

- current contract plus historical research
- tutorial/how-to steps plus reference tables
- conceptual doctrine plus implementation procedure
- user-facing documentation plus agent/process instructions
- durable policy plus ticket-local proof, blockers, or closeout notes

Choose density by surface:

- `README.md` and directory indexes: sparse map, current orientation, links
- `ARCHITECTURE.md`: system model, ownership boundaries, major flows
- `docs/specs/*`: dense contracts, schemas, state machines, and testable rules
- `docs/fundamentals/*`: conceptual doctrine and reusable mental models
- `docs/skills/*`: skill-system policy, inventories, and operating guidance
- `skills/<name>/SKILL.md`: compact executable workflow contract
- `skills/<name>/qa_checklist.md`: preflight and final-review guardrails
- `tickets/*`: task-local plan, blockers, progress, and proof

If a doc grows because it is accumulating task evidence, archive notes, or
implementation history, move those details to the ticket, artifact, or `tmp/**`
scratch space and keep the current contract compact.

## Feature Metadata Ownership

Specs own feature metadata. Add or update `feature_records_json` in the
smallest active spec that owns the behavior. Use
`docs/specs/feature-catalog.md` only for transitional, cross-cutting, or
historical `FEAT-*` records without a clearer spec owner.

`docs/features/registry.jsonl` is generated output. Do not hand-edit it. After
feature metadata changes, run:

```bash
python3 docs/features/validate_features.py --write
python3 docs/features/validate_features.py
```

Delete stale docs instead of creating permanent tracked archives by default.
Before deletion, promote any still-current truth into an active owner: spec,
fundamentals, skill, ticket, or generated metadata source.

## Structural Checks

Use mechanical validators when the repo needs wording-independent protection.

Current structural checks:

- `python3 tickets/scripts/check_ticket_metadata.py`
  Purpose: ticket frontmatter/body contract and lifecycle invariants
- `python3 bin/validators/check_doc_parity.py`
  Purpose: narrow entrypoint parity for canonical docs and stale queue claims
- `python3 docs/features/validate_features.py`
  Purpose: generated feature registry freshness, stable ID, ref, and row-shape
  validation

Rule of thumb:

- If the check is about file existence, required canonical links, required
  headings, or machine-readable state, keep it mechanical.
- If the check is about whether the prose is still the best explanation of the
  repo, use a narrative audit instead.

## Narrative Audit

Use `codex exec` when the question is whether the docs still tell the right
story, not whether they include one exact substring.

Suggested prompt shape:

```text
Read AGENTS.md, ARCHITECTURE.md, README.md, docs/specs/README.md,
docs/specs/harness-techniques.md, tickets/README.md, docs/HISTORY.md,
docs/MEMORY.md, and any active tickets that changed the public harness story.

Tasks:
1. Identify stale claims, contradictory statements, missing canonical links,
   and implemented-vs-proposed mismatches.
2. Classify each finding as structural or narrative.
3. Propose the smallest doc patch that restores coherence.
4. Name any follow-up ticket if the fix is broader than a narrow doc change.

Do not rewrite docs for style alone. Prefer patching canonical surfaces rather
than duplicating the same claim into more files.
```

## Gardening Loop

Run this loop when the public harness story changes:

1. Run `python3 tickets/scripts/check_ticket_metadata.py`.
2. Run `python3 bin/validators/check_doc_parity.py`.
3. Re-read the canonical surfaces listed above against the active ticket plus
   `docs/HISTORY.md` and `docs/MEMORY.md`.
4. Run the `codex exec` narrative audit when the change affects explanation,
   architecture shape, implemented/proposed status, or canonical doc links.
5. Patch only the canonical surfaces that drifted.
6. Re-run the structural checks.

## Anti-Goals

- Do not create mechanical validators for every prose nuance.
- Do not let root docs silently drift away from implemented repo surfaces.
- Do not copy the same claim into many files unless those files are all truly
  canonical for that concern.
