---
owner: learning-drain
purpose: processed-state idempotence contract
---

# Processed State

`learning-drain` uses processed state to make the weekly drain idempotent while
leaving `docs/TROUBLES.md` and `docs/LESSONS.md` as append-only ledgers.

Canonical path:

```text
.farplane/state/learning-drain/processed.jsonl
```

Legacy read-only compatibility path:

```text
.farplane/state/self-improve/weekly-drain-processed.jsonl
```

## Row Identity

Compute a candidate row identity from:

```text
doc_ref = <relative-file-path>:<line-number>
content_hash = sha256(normalized_row_text)
```

Use both values. Line numbers are helpful for humans, while content hashes
survive small insertions above the row.

## JSONL Shape

```json
{
  "schema_version": 1,
  "doc_ref": "docs/TROUBLES.md:42",
  "content_hash": "sha256:...",
  "source_kind": "trouble|lesson|pair",
  "paired_ref": "docs/LESSONS.md:33",
  "drained_at": "2026-06-13T00:00:00Z",
  "disposition": "optimizer-followup|eval-followup|ticket-created|deferred|duplicate|no-change",
  "followup_ref": "optimize-harness:<short-id>",
  "ticket_ref": "tickets/TASK-0000/ticket.md",
  "thread_ref": "",
  "notes": "compact sanitized reason"
}
```

## Dedupe Rules

- If `content_hash` is already processed, skip unless the operator explicitly
  asks to re-open the row.
- If a trouble row and lesson row are paired, record both source refs in the
  same drain cycle.
- If a row is weak, private-risk, or not actionable, write a processed row only
  when skipping it again would waste future drain work.
- If a row exceeds the run cap, mark it `deferred` with a reason and allow a
  future run to process it.

## Safety

- Store compact sanitized reasons only.
- Do not copy raw transcripts, secrets, local credentials, or private contact
  details into processed state.
- Do not treat processed state as canonical memory. The canonical human ledgers
  remain `docs/TROUBLES.md` and `docs/LESSONS.md`.
