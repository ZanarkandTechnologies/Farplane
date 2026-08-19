---
title: Mixed Wiki resolution example
kind: skill-example
skill: manage-wiki
created_at: 2026-08-19
---

# Mixed Wiki Resolution Example

## Bound Source

> Penang Castings, also called PC Manufacturing, supplies aluminum housings to
> Acme Motors. The contact was Alex Chen, but the call does not identify which
> Alex Chen. Batu Kawan Finishing is a named new facility; its opening date is
> tentative.

The project already contains Acme Motors and two people named Alex Chen.

## Staged Resolution

| Mention | Search evidence | Outcome |
| --- | --- | --- |
| Penang Castings | Unique exact name; new alias in source | `update_existing` |
| Acme Motors | Unique exact name | `link` |
| Alex Chen | Two plausible person articles; no employer/location | `ambiguity` |
| Batu Kawan Finishing | No plausible exact or fuzzy candidate | `create_new` |

The skill reads every plausible candidate article. It does not choose either
Alex Chen, create a third duplicate, or publish a partial changeset while that
required mention remains unresolved.

With `publication_intent: preview`, it returns this fully resolved and validated
changeset without writing. With `publication_intent: apply`, the same ambiguity
still blocks the complete publication; direct Wiki write intent removes only a
second approval prompt, never the identity gate.

## Validated Article Form

After the operator supplies enough evidence to resolve or explicitly omit the
ambiguous mention, the supported sentence can read:

```markdown
Supplies aluminum housings to [Acme Motors](entity:acme-motors). [^q-20260720-01]
```

The same changeset merges `PC Manufacturing` into aliases, creates the sourced
Batu Kawan article, preserves the tentative date in prose, and runs one
`farplane wiki sync` command with repeated `--path` arguments for every touched
page. Sync replaces only their emitted claims; inbound claims survive.

## Comparison Gates

- The source and scan are bounded to touched articles.
- Exact identity precedes FTS5/trigram candidate retrieval.
- Fuzzy similarity never auto-merges an identity.
- Canonical Markdown is the only authored state.
- Preview writes nothing; apply publishes and page-scoped syncs only after every gate passes.
- The receipt names every candidate, outcome, changed page, and projection.

## Provenance / Rights

Synthetic fixture adapted from the earlier bounded capture scenario; no
customer or private call data is included.
