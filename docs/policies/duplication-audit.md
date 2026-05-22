# Documentation Duplication Audit

Date: 2026-05-22

## Scope

Audited Markdown docs under:

- `docs/`
- `README.md`
- `ARCHITECTURE.md`
- `AGENTS.md`
- `templates/global/AGENTS.md`

The audit used a normalized 8-word shingle comparison and then manually
inspected the high-similarity pair before editing.

## Result

One true duplicate was found:

| Duplicate | Canonical owner | Action |
| --- | --- | --- |
| `docs/specs/legacy/ralph-runtime-surface.md` duplicated most of `docs/specs/runtime-surface.md` and carried stale Ralph wording | [`docs/specs/runtime-surface.md`](/Users/kenjipcx/coding-harness/Codexter/docs/specs/runtime-surface.md) | Deleted with the rest of the retired legacy Ralph spec bundle |

No other Markdown pair crossed the high-similarity threshold in this pass.

## Policy

Prefer this pattern for future doc cleanup:

1. Keep the canonical owner detailed.
2. Delete retired duplicates when no live surface needs the old link.
3. Keep indexes link-heavy and summary-light.
4. Do not merge research notes into specs unless the research has become live
   doctrine.
5. Keep historical context in research/history, not active spec compatibility
   files, unless a live external link still needs a pointer.

## Follow-Up

The next useful improvement is a small reusable duplicate-doc checker that
reports high-similarity doc pairs and allows known intentional pointers. It should
feed the case-based memory graph later, but does not need to block current docs.
