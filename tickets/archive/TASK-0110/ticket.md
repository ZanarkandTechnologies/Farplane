---
ticket_id: TASK-0110
title: add source registry for harness inspiration
phase: complete
status: done
owner: codex
claimed_by:
priority: high
depends_on: []
blocked_by: []
ready: false
approval_required: false
requires_qa: false
requires_demo: false
created_at: 2026-05-05T07:27:16Z
updated_at: 2026-05-05T19:15:00Z
next_action: archived by TASK-0118 closeout; future work should use new active tickets
last_verification: 2026-05-05T19:15:00Z archived by TASK-0118 after ticket train reconciliation; prior ticket evidence and review artifacts preserved under tickets/archive/
---

# TASK-0110: add source registry for harness inspiration

## Summary
Add a lightweight registry for the sources Codexter uses as harness inspiration:
specs, blog posts, videos, docs, repos, and user-provided external materials.
The feature registry already tracks techniques; this ticket adds the missing
source-level dedupe layer so future scout runs can answer "have we already seen
this article/spec/video, and what did we decide from it?"

## Scope
- In:
  - `docs/sources/README.md` describing the source registry contract.
  - `docs/sources/registry.jsonl` with stable `SRC-####` records.
  - Initial source records for the known harness-inspiration inputs, including
    Symphony, Anthropic harness design, Codex docs/blog references, Cursor
    long-running agent references, the self-evolving agents video, and prior
    OMX/Codexter comparison research where applicable.
  - A simple validation command in the README, mirroring the feature registry
    style.
  - `harness-scout` updates so new source runs check the source registry before
    creating a duplicate run folder.
  - Cross-links from `SRC-*` records to `FEAT-*` records, scout runs, research
    memos, and local specs.
- Out:
  - No semantic search, vector memory, crawler, cron feed, or auto-ingestion.
  - No raw transcript promotion into canonical docs.
  - No attempt to make source records replace feature records.
  - No external network fetch during validation.

## Plan
- `Change:` Introduce a source registry parallel to the feature registry.
- `Why:` Codexter can dedupe techniques now, but it cannot dedupe the sources
  that inspired those techniques. This makes repeated blogs/specs/videos easy
  to accidentally re-analyze and makes provenance harder to audit.
- `Before -> After:`
  - Before: `experiments/harness-scout/runs/*` stores source-run artifacts, but
    dedupe is folder/search-based and source identity is not canonical.
  - After: `SRC-*` records identify each source once, link to local artifacts,
    link to `FEAT-*` outputs, and tell future agents whether to adopt, adapt,
    reject, defer, or treat the source as duplicate.
- `Touch:`
  - `docs/sources/README.md`
  - `docs/sources/registry.jsonl`
  - `skills/harness-scout/SKILL.md`
  - `skills/harness-scout/todos.md`
  - `skills/harness-scout/references/architecture.md`
  - `skills/harness-scout/references/workflows.md`
  - `README.md`
  - `ARCHITECTURE.md`
  - `docs/specs/harness-techniques.md`
  - `docs/features/README.md`
  - `docs/HISTORY.md`
- `Inspect:`
  - `docs/features/README.md`
  - `docs/features/registry.jsonl`
  - `experiments/harness-scout/runs/*`
  - `docs/archive/research/web-research/*`
  - `docs/specs/harness-engineering-quickstart.md`
  - `skills/harness-scout/templates/source-run.md`
- `Signature delta:`
  - `docs/sources/registry.jsonl / SourceRecord`
  - `docs/sources/README.md / validation command`
  - `skills/harness-scout / source dedupe step`
- `Type Sketch:`
  - `SourceRecord`: `id`, `title`, `source_type`, `origin`,
    `canonical_url`, `canonical_key`, `visibility`, `captured_at`,
    `local_artifacts`, `feature_refs`, `decision`, `duplicate_of`, `status`,
    `last_verified`.
  - `source_type`: `spec | blog | video | docs | repo | paper | user-provided`.
  - `decision`: `adopt | adapt | reject | defer | duplicate | reference-only`.
  - `status`: `active | archived | superseded | sensitive-redacted`.
- `Typed flow example:`
  1. A future agent receives the Symphony spec again.
  2. `harness-scout` checks `docs/sources/registry.jsonl`.
  3. It finds `SRC-0001` by `canonical_key:
     openai-symphony-service-spec-draft-v1`.
  4. It reuses the existing scout run and sees that `FEAT-0014` already
     implemented the invocation contract.
  5. It opens a new ticket only if the source contains a genuinely new
     candidate not already represented by `FEAT-*`.
- `Execution steps:`
  1. Create `docs/sources/README.md` with field contract, update rules,
     retention rules, and validation command.
  2. Create `docs/sources/registry.jsonl` with initial records for known
     inspiration sources.
  3. Add a source-registry check to `harness-scout` workflow docs and todo list.
  4. Update `docs/features/README.md` to clarify feature records link to
     sources but do not own source dedupe.
  5. Update `README.md`, `ARCHITECTURE.md`, and `harness-techniques.md` so the
     source registry is discoverable.
  6. Run source-registry validation, feature-registry validation, doc parity,
     harness invariants, and review.
- `Recommendation:` Keep this simple: JSONL plus a validator and scout
  instructions. Do not build a database until repeated source volume proves the
  need.
- `Options considered:`
  - Add source fields only to `docs/features/registry.jsonl`: too cramped
    because one source can inspire many features and one feature can synthesize
    many sources.
  - Add a separate `docs/sources/registry.jsonl`: recommended because it
    cleanly dedupes source identity and provenance.
  - Add a searchable database/vector store: premature and too much operational
    weight for the current scout workflow.
- `Blast radius:` `harness-scout`, feature registry provenance, research docs,
  README/ARCHITECTURE navigation, and future source-ingestion tickets.
- `Risks:`
  - Duplicating feature registry responsibilities. Containment: `SRC-*` tracks
    sources; `FEAT-*` tracks techniques.
  - Storing too much source content. Containment: records contain identity and
    links only, not raw transcripts.
  - Making validation brittle. Containment: keep the schema narrow and local.

## Gap Analysis
- `Current state:` Codexter has `FEAT-*` records and per-source scout run
  folders, but no canonical source ID or duplicate-source record.
- `Production expectation:` A research-backed harness should separate source
  provenance from feature inventory so agents can dedupe articles/specs/videos,
  preserve decisions, and avoid re-ingesting the same source.
- `Missing gaps:`
  - No `SRC-*` identifier.
  - No canonical source key or duplicate pointer.
  - No structured link from source to feature decisions.
  - No validation command for source records.
  - `harness-scout` dedupe remains folder-search procedural.
- `Comparable implementations:` current feature registry, harness-scout source
  runs, Symphony scout artifacts, prior web-research memos.
- `Recommendation:` Land source registry first; use it as provenance for the
  board/compute respec and later Symphony tickets.

## Diagram
```mermaid
flowchart LR
  classDef source fill:#dbeafe,stroke:#2563eb,color:#111827
  classDef run fill:#fef3c7,stroke:#b45309,color:#111827
  classDef feature fill:#dcfce7,stroke:#15803d,color:#111827
  classDef ticket fill:#fee2e2,stroke:#b91c1c,color:#7f1d1d

  Input["Blog / spec / video"]:::source --> Source["SRC-* record"]:::source
  Source --> Run["harness-scout run"]:::run
  Run --> Feature["FEAT-* technique"]:::feature
  Feature --> Ticket["TASK-* follow-up"]:::ticket
```

## Acceptance Criteria
- [ ] `docs/sources/README.md` defines the source registry fields, update
  rules, retention rules, ID allocation, duplicate behavior, and validation
  command.
- [ ] `docs/sources/registry.jsonl` exists and validates.
- [ ] Initial records cover the known sources used to shape Codexter's harness
  direction, including Symphony and the major harness-engineering references.
- [ ] `harness-scout` explicitly checks `docs/sources/registry.jsonl` before
  creating a new source run.
- [ ] Source records link to local scout runs, research memos, and `FEAT-*`
  records without copying raw source text.
- [ ] Public docs explain the split: `SRC-*` is source provenance, `FEAT-*` is
  durable technique inventory.

## Verification
- `Tests:`
  - Source registry validation command from `docs/sources/README.md`.
  - Feature registry validation command from `docs/features/README.md`.
- `Manual checks:`
  - Confirm a duplicate Symphony source lookup would point to the existing
    scout run and `FEAT-0014`.
  - Confirm no raw transcripts or bulky source extracts are promoted into
    `docs/sources/registry.jsonl`.
- `Evidence required:`
  - Validation output.
  - Review artifact linked from this ticket.

## Agent Contract
- `Open:` no app/UI. Work directly in repo docs.
- `Test hook:` source registry validation command.
- `Stabilize:` use deterministic JSONL sorting by `SRC-####`.
- `Inspect:` `docs/sources/registry.jsonl`, `docs/features/registry.jsonl`,
  scout run folders, and research memo links.
- `Key screens/states:` none.
- `QA cookbook:` none needed.
- `Taste refs:` none.
- `Expected artifacts:` validation output and review JSON.
- `Delegate with:` this ticket plus `skills/harness-scout/SKILL.md`; expected
  artifact is the registry plus review.

## Autonomy Readiness
- `Human inputs/assets:` None beyond this approved ticket.
- `Credentials / external access:` None. Use existing local source records and
  URLs already present in docs; do not browse unless a source identity is
  unclear.
- `Compute/runtime needs:` local filesystem and Python/JSON validation.
- `Tooling gaps:` no source registry validator exists yet; include inline
  command in README or a small script if the implementation proves repetition.
- `QA risks:` claim inflation: make sure source records do not imply adoption
  when the linked scout decision was reject/defer/duplicate.
- `Human gates:` approval before implementation; no publish/push.
- `Agent decision boundaries:` may choose exact initial `SRC-*` allocation; may
  not store raw transcripts or add crawler behavior.

## Evidence Checklist
- [ ] Source registry validation output.
- [ ] Feature registry validation output.
- [ ] Review JSON linked.

## Refs
- `skills/harness-scout/SKILL.md`
- `docs/features/README.md`
- `docs/features/registry.jsonl`
- `experiments/harness-scout/runs/2026-05-05-symphony-compatible-codexter/`
- `experiments/harness-scout/runs/2026-05-04-self-evolving-agents/`

## Evidence
- `Artifacts:`
  - [future-ticket-batch-review.json](/Users/kenjipcx/coding-harness/Codexter/tickets/archive/TASK-0111/artifacts/review/2026-05-05-ticket-batch-review.json)
  - [impl-review.json](/Users/kenjipcx/coding-harness/Codexter/tickets/archive/TASK-0110/artifacts/review/2026-05-05-impl-review.json)
- `Commands:`
  - `python3 docs/sources/validate_sources.py`
    - `source registry contract OK (7 records)`
  - `python3 -m py_compile docs/sources/validate_sources.py`
  - feature registry validation snippet from `docs/features/README.md`
    - `feature registry contract OK (14 records)`
  - `python3 tickets/scripts/check_ticket_metadata.py`
    - `ticket metadata OK (22 ticket files checked)`
  - `git diff --check -- docs/sources/AGENTS.md docs/sources/README.md docs/sources/registry.jsonl docs/sources/validate_sources.py docs/features/README.md skills/harness-scout/SKILL.md skills/harness-scout/todos.md skills/harness-scout/references/architecture.md skills/harness-scout/references/workflows.md blockers.md`
    - pass
- `Result summary:`
  - Added `docs/sources/` as the `SRC-*` source provenance layer with a
    validator and seven initial records covering Symphony, the self-evolving
    agents video, Anthropic, Cursor, OpenAI Codex docs, and OMX research.
  - Updated `harness-scout` so source dedupe happens before source-run creation
    and before `FEAT-*` feature dedupe.
  - Clarified the split between source provenance and feature inventory in
    `docs/features/README.md`.

## Blockers
- none
