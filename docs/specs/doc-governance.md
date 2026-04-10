# Doc Governance

Use this file to keep Codexter's knowledge base trustworthy without turning the
repo into a markdown-lint maze.

## Goal

Treat docs as the system of record while keeping checks proportional to the kind
of truth each surface carries.

Codexter uses two kinds of documentation checks:

- structural checks for canonical entrypoints and machine-relevant contracts
- narrative audits for richer docs whose wording can change while the truth
  stays the same

## Canonical Surfaces

These surfaces define the live repo story and should stay mutually coherent:

- [AGENTS.md](/Users/kenjipcx/coding-harness/Codexter/AGENTS.md)
- [ARCHITECTURE.md](/Users/kenjipcx/coding-harness/Codexter/ARCHITECTURE.md)
- [README.md](/Users/kenjipcx/coding-harness/Codexter/README.md)
- [docs/specs/README.md](/Users/kenjipcx/coding-harness/Codexter/docs/specs/README.md)
- [docs/specs/harness-techniques.md](/Users/kenjipcx/coding-harness/Codexter/docs/specs/harness-techniques.md)
- [tickets/README.md](/Users/kenjipcx/coding-harness/Codexter/tickets/README.md)

## Structural Checks

Use mechanical validators when the repo needs wording-independent protection.

Current structural checks:

- `python3 tickets/scripts/check_ticket_metadata.py`
  Purpose: ticket frontmatter/body contract and lifecycle invariants
- `python3 bin/check_doc_parity.py`
  Purpose: narrow entrypoint parity for canonical docs and stale queue claims

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
2. Run `python3 bin/check_doc_parity.py`.
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
