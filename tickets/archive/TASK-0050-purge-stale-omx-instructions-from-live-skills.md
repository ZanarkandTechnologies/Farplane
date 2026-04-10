---
ticket_id: TASK-0050
title: purge stale omx instructions from live skills
phase: complete
status: done
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: false
approval_required: false
created_at: 2026-04-10T00:00:00Z
updated_at: 2026-04-10T01:56:29+0100
next_action: archived; continue with `TASK-0046` to retire the `.ralph/` runtime naming in favor of the approved neutral replacement surface
last_verification: 2026-04-10 01:57 +0100 | targeted live-surface OMX grep shows only historical references or explicit do-not-create guardrails, and both `python3 tickets/scripts/check_ticket_metadata.py` plus `python3 bin/check_doc_parity.py` passed
linked_docs:
  - AGENTS.md
  - docs/HISTORY.md
  - docs/MEMORY.md
  - docs/TROUBLES.md
  - tickets/archive/TASK-0015-purge-live-omx-surfaces.md
  - skills/impl-plan/SKILL.md
  - skills/deep-interview/SKILL.md
  - skills/ralph/SKILL.md
---

# TASK-0050: purge stale omx instructions from live skills

## Summary
Remove stale `.omx/*` instructions from live Codexter skill surfaces so the repo stops reintroducing purged OMX-era context, state, and artifact paths during normal planning or execution.

## Scope
- In:
  - live skill instructions that still tell agents to read or write `.omx/*`
  - skill-local docs or references that present `.omx/*` as current Codexter behavior
  - canonical doc updates needed to keep the public harness story consistent
- Out:
  - archived historical tickets
  - research notes analyzing OMX as an external system
  - broad redesign of the skills themselves beyond removing or replacing stale OMX-era behavior

## User Story
- `Actor:` operator using Codexter’s live skills for planning or execution
- `Need:` live skills to point at the current Codexter surfaces instead of stale OMX-era paths
- `Outcome:` the agent stops creating or relying on `.omx/*` artifacts that the repo already considers purged

## User Pain / JTBD
- `Current pain:` the live skills still contain stale `.omx/*` instructions, so the agent can drift into creating or relying on obsolete surfaces during normal work
- `Why now:` this already caused a concrete miss during recent planning, so the stale instructions are not harmless history; they are still shaping behavior

## Non-Goals
- `Do not solve:` preserving full OMX compatibility, rewriting archived historical material, or redesigning every planning/execution skill at once

## High-Fidelity Example
- `Example flow/artifact:` a user asks for an `impl-plan` approval pass on an active ticket. Instead of reusing the ticket plus canonical specs and docs, the skill tells the agent to create `.omx/context/{slug}-*.md`, and the agent writes a new `.omx/context/*` artifact even though the repo already purged live OMX surfaces. After this ticket, the same flow should stay entirely within the current Codexter surfaces and never suggest `.omx/*` unless the content is clearly historical research.

## What Good Looks Like
- `Quality bar:` a live skill can be followed literally without causing the agent to recreate obsolete `.omx/*` runtime or planning artifacts

## Proof Target
- `Reviewer-visible proof:` a repo-wide search over live skills/docs shows no remaining instructions that present `.omx/*` as an active Codexter surface, while archived/research references remain intentionally untouched

## Plan

### Pitch
- `Req:` stop live skills from teaching obsolete `.omx/*` behavior
- `Bet:` one bounded purge pass over the live skill surfaces is enough to remove the current source of drift without reopening historical research or archived tickets
- `Win:` future planning and execution flows stay on the current repo contract instead of resurrecting purged OMX surfaces

### Recommendation
- `Best:` patch the live skills that still mention `.omx/*`, replace those instructions with current Codexter surfaces, and explicitly leave archived/research OMX references alone
- `Why:` this removes the real source of behavior drift while avoiding a noisy and unnecessary sweep across historical material
- `Tradeoff accepted:` some files will still mention `.omx/*` in research or archive contexts, but that is acceptable as long as the live skills and canonical docs no longer treat it as current behavior

### B -> A
- `Before:` live skills still contain stale OMX-era read/write instructions, so the agent can follow them and recreate purged surfaces
- `After:` live skills point only at current Codexter tickets/docs/runtime surfaces, and any remaining `.omx/*` mentions are clearly historical or external-analysis context
- `Outcome:` less execution drift and less confusion about what the current harness actually uses

### Delta
- `Touch:` `skills/deep-interview/SKILL.md`, `skills/ralph/SKILL.md`, maybe related references, and any canonical doc that still describes `.omx/*` as current
- `Keep:` archived tickets and external research notes about OMX
- `Change:` replace stale live-instruction paths with current Codexter surfaces
- `Delete/Avoid:` half-purges that leave live skills ambiguous about whether `.omx/*` is current or historical

### Core Flow
```pseudo
search live skills/docs for .omx references
classify each hit as live instruction vs historical/research
patch live instruction hits to current Codexter surfaces
leave archived/research references untouched
validate that live surfaces no longer instruct agents to create or rely on .omx artifacts
```

### Proof
- `P1:` live skill surfaces no longer instruct agents to create or read `.omx/*`
- `P2:` repo docs still distinguish current Codexter behavior from historical/external OMX analysis
- `Risk:` an over-broad sweep could delete useful historical context
- `Rollback:` keep the purge scoped to live skills and canonical docs only; do not touch archived/research references unless they are incorrectly presented as current

### Plan Review
- `Refs:` root `AGENTS.md`, `docs/MEMORY.md`, `docs/TROUBLES.md`, `tickets/archive/TASK-0015-purge-live-omx-surfaces.md`, `skills/impl-plan/SKILL.md`, `skills/deep-interview/SKILL.md`, `skills/ralph/SKILL.md`
- `Scope:` pass; one bounded live-surface cleanup
- `Proof:` pass; grep-based verification is concrete and observable
- `Guardrails:` pass; preserves historical/research context while removing live drift
- `Fixes:` none

### Options Appendix
- `Option 1:` patch only the one skill that just caused the miss
- `Pros:` smallest diff; fastest fix
- `Cons:` leaves other live skills able to reintroduce the same problem
- `Why not chosen:` too narrow for a now-proven repo-wide drift source
- `Option 2:` purge stale `.omx/*` instructions from all live skills and canonical docs only
- `Pros:` fixes the real source of drift; bounded enough for one commit; preserves history
- `Cons:` requires careful classification of live vs historical references
- `Why not chosen:` recommended
- `Option 3:` delete every `.omx` reference everywhere
- `Pros:` maximal cleanliness
- `Cons:` destroys useful research/archive context and overreaches far beyond the live-contract problem
- `Why not chosen:` too destructive and conceptually sloppy

### Delegation
- `Need:` Not needed
- `Why:` this is a bounded repo-local cleanup
- `Artifact:` n/a

### Ask
- `Ready: yes`
- `Next:` approve the live-surface OMX purge, then patch the affected skills and rerun a targeted grep plus ticket/doc validators

### Ticket Move
- `Now:` `status: review`, `phase: planning`
- `On approval:` set `status: building` and remove stale `.omx/*` instructions from the live skills/docs in scope
- `Follow-ups:` none yet
- `Blocked in building?:` no

## Acceptance Criteria
- [x] AC-1: live skills no longer instruct the agent to create or depend on `.omx/*` context, state, interview, plan, or spec artifacts for current Codexter work
- [x] AC-2: the replacement instructions point at current Codexter surfaces instead of simply deleting context expectations outright
- [x] AC-3: archived tickets and research docs that mention OMX remain untouched unless they incorrectly present it as the live current contract
- [x] AC-4: verification includes a targeted repo search proving that remaining `.omx/*` hits are historical or research-only, not live instruction surfaces

## Working Notes
- Immediate concrete miss: `impl-plan` still had stale `.omx/context` instructions and caused a new `.omx/context/*` artifact to be created during planning.
- Verified on 2026-04-10 that `skills/deep-interview/SKILL.md` and `skills/ralph/SKILL.md` still contain many `.omx/*` references.
- Archived prior purge work exists in `TASK-0015`, but the remaining live skill instructions show that the purge was incomplete or later drifted back in.

## Inspiration
- Source: direct user correction on 2026-04-10 after a fresh planning miss recreated `.omx/context/*` despite the repo’s purge of live OMX surfaces.

## Implementation Notes
- Touched areas:
  - `skills/deep-interview/SKILL.md`
  - `skills/ralph/SKILL.md`
  - `skills/deep-interview/AGENTS.md`
  - `skills/deep-interview/README.md`
  - `skills/ralph/AGENTS.md`
  - `skills/ralph/README.md`
  - `AGENTS.md`
  - `docs/MEMORY.md`
  - `docs/HISTORY.md`
- Reused patterns:
  - ticket/docs/runtime-grounding from `tickets/README.md` and `docs/specs/context-and-handoff-policy.md`
  - `.ralph/state/*` as the live runtime surface instead of `.omx/*`
- Guardrails:
  - preserved historical/archive OMX references
  - kept the remaining live `.omx/*` mentions strictly as negative guardrails

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [x] QA / manual verification

Validation details:
- `rg -n '\\.omx|\\bomx\\b|USE_OMX' skills/deep-interview/SKILL.md skills/ralph/SKILL.md skills/impl-plan/SKILL.md AGENTS.md docs README.md ARCHITECTURE.md tickets`
  - remaining live hits are the existing `impl-plan` do-not-create guardrail, the new do-not-create guardrails in `deep-interview` / `ralph`, and historical/archive/research references
- `python3 tickets/scripts/check_ticket_metadata.py`
  - passed
- `python3 bin/check_doc_parity.py`
  - passed

## Review Packet
- `work_type:` `["docs","skills","cleanup"]`
- `search_scope:` `{changed_files: ["skills/deep-interview/SKILL.md","skills/ralph/SKILL.md","skills/deep-interview/AGENTS.md","skills/deep-interview/README.md","skills/ralph/AGENTS.md","skills/ralph/README.md","AGENTS.md","docs/MEMORY.md","docs/HISTORY.md"], related_files: ["skills/impl-plan/SKILL.md","tickets/README.md","docs/specs/context-and-handoff-policy.md","docs/specs/ralph-runtime-surface.md"], invariants_checked: ["MEM-0021","ticket/docs/runtime surfaces stay canonical","historical OMX references remain preserved"], docs_checked: ["AGENTS.md","docs/MEMORY.md","docs/HISTORY.md"]}`
- `reviewed_at:` `2026-04-10 01:56 +0100`
- `rubrics_used:` `["cleanup","spec-contract","integration-readiness"]`
- `overall_score:` `4.7`
- `overall_threshold:` `4.0`
- `overall_verdict:` `pass`
- `rerun_required:` `false`
- `evidence_quality:` `pass`
- `integration_readiness:` `pass`
- `traceability:` `pass`
- `freshness:` `pass`
- `hard_gate_failures:` `[]`
- `finding_log:` `[]`
- `blocking_findings:` `[]`
- `next_action:` `archive complete; continue with the runtime-surface rename tracked in TASK-0046`

## Blockers
- none

## Handoff
- Current state: live `deep-interview` and `ralph` skill surfaces now point at current Codexter ticket/docs/runtime artifacts, and the remaining live `.omx/*` mentions are explicit guardrails rather than active instructions.
- Resume from: `TASK-0046` if you want to keep collapsing the runtime naming model from `.ralph/` toward the approved neutral replacement surface.

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter. Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then move the ticket into `tickets/archive/` or set `status: done` briefly if you intentionally keep a short-lived visible completion state first.
