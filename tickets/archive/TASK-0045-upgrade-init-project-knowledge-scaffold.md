---
ticket_id: TASK-0045
title: upgrade init-project knowledge scaffold
phase: complete
status: done
owner: codex
priority: high
depends_on:
  - TASK-0044
blocked_by: []
ready: false
approval_required: false
created_at: 2026-04-09T16:52:49+0100
updated_at: 2026-04-09T17:07:10+0100
next_action: none; ticket completed after landing the architecture-aware init-project scaffold update
last_verification: bash skills/init-project/scripts/bootstrap.sh /tmp/codexter-init-smoke.G9B9l7; python3 tickets/scripts/check_ticket_metadata.py; git diff --check
linked_docs:
  - skills/init-project/SKILL.md
  - skills/init-project/scripts/bootstrap.sh
  - skills/init-project/references/AGENTS_TEMPLATE.md
  - skills/init-project/references/PROJECT_RULES_TEMPLATE.md
  - tickets/archive/TASK-0044-add-architecture-map-and-canonical-doc-index.md
---

# TASK-0045: upgrade init-project knowledge scaffold

## Summary
Update `init-project` so newly scaffolded repos inherit the improved knowledge-base shape instead of only the older minimal docs-and-tickets skeleton.

## Scope
- In:
  - `init-project` bootstrap and templates
  - scaffolding for the agreed top-level architecture/doc-map surfaces
  - migration guidance for existing repos
  - keeping the starter shape lightweight while still more legible than today
- Out:
  - mass migration of all existing downstream repos
  - turning the bootstrap into a heavy docs generator
  - forcing every optional doc surface into every project regardless of need

## User Story
- `Actor:` Codexter user bootstrapping a new repo
- `Need:` the scaffold to create the same knowledge shape we now think is correct
- `Outcome:` new repos start with a coherent map/docs/ticket system instead of needing a later cleanup ticket to catch up

## User Pain / JTBD
- `Current pain:` Codexter's own repo is moving toward a stronger knowledge-base shape, but `init-project` still scaffolds only the earlier, thinner structure
- `Why now:` if the scaffold lags behind the repo's own recommendation, every new project will immediately start from partial parity

## Non-Goals
- `Do not solve:` broad downstream migration automation or a one-size-fits-all enterprise doc taxonomy

## High-Fidelity Example
- `Example flow/artifact:` a fresh project bootstrapped with `init-project` includes a short `AGENTS.md`, an architecture map, canonical docs pointers, tickets, and the minimum durable memory surfaces needed to orient an agent without a follow-up restructuring pass

## What Good Looks Like
- `Quality bar:` the bootstrap stays simple, but the generated repo shape reflects the current best-practice knowledge model rather than a stale snapshot

## Proof Target
- `Reviewer-visible proof:` reading the bootstrap output and migration guide should make it obvious how a new repo gets from `AGENTS.md` to architecture/doc map to specs/tickets without missing foundational surfaces

## Plan

### Pitch
- `Req:` keep the project bootstrap aligned with the harness structure we actually recommend
- `Bet:` a small scaffold upgrade is enough; we do not need to generate a giant doc tree by default
- `Win:` new repos start closer to the desired system-of-record shape, reducing repeated cleanup work

### Recommendation
- `Best:` update `init-project` after `TASK-0044` defines the desired top-level architecture/doc-map shape, then scaffold only the high-value mandatory surfaces
- `Why:` this keeps the scaffold grounded in a real canonical target and avoids baking in a speculative docs taxonomy too early
- `Tradeoff accepted:` the scaffold will still be intentionally lighter than the full OpenAI example, so some optional deeper docs may remain opt-in

### B -> A
- `Before:` `init-project` creates `docs/prd.md`, `docs/specs/`, `HISTORY`, `MEMORY`, `TROUBLES`, `TASTE`, and tickets, but not the richer top-level map we now want
- `After:` bootstrap output includes the agreed knowledge-base entry surfaces and updated guidance for how to use them
- `Outcome:` scaffold parity improves and fewer repos start life already behind the harness standard

### Delta
- `Touch:` `skills/init-project/SKILL.md`, `skills/init-project/scripts/bootstrap.sh`, template references, and migration docs
- `Keep:` docs-first and ticket-first structure
- `Change:` bootstrap the improved knowledge-base entry surfaces and guidance
- `Delete/Avoid:` avoid scaffolding an oversized tree with many empty files that users will not maintain

### Core Flow
```pseudo
use TASK-0044 output as the target scaffold shape
decide which surfaces are mandatory versus optional
update bootstrap and templates
update migration guidance
verify a fresh scaffold matches the intended entrypoint model
```

### Proof
- `P1:` a fresh scaffold includes the agreed top-level map/docs surfaces from the architecture ticket
- `P2:` migration guidance explains how brownfield repos adopt the new shape without a full backlog rewrite
- `Risk:` the scaffold becomes ceremony-heavy and creates files that rot immediately
- `Rollback:` keep only the minimal high-value entry surfaces in the default bootstrap

### Plan Review
- `Refs:` `skills/init-project/*`, `tickets/README.md`, `TASK-0044`, current bootstrap output
- `Scope:` scaffold parity only
- `Proof:` fresh bootstrap smoke check plus ticket/doc validator pass on changed repo surfaces
- `Guardrails:` no speculative doc sprawl and no downstream migration engine
- `Fixes:` make the bootstrap reflect current best practice without overfitting to this repo's every detail

### Options Appendix
- `Option 1:` leave `init-project` as-is and document the gap manually
- `Pros:` no bootstrap changes
- `Cons:` every new repo starts with known doc-shape debt
- `Why not chosen:` it institutionalizes the mismatch we just identified
- `Option 2:` update the scaffold to include the new mandatory knowledge surfaces only
- `Pros:` best balance of parity and simplicity
- `Cons:` still requires judgment about which surfaces are mandatory
- `Why not chosen:` recommended
- `Option 3:` scaffold the full OpenAI-style tree
- `Pros:` maximal parity with the article example
- `Cons:` too much empty structure for most projects
- `Why not chosen:` over-scoped and likely to rot

### Delegation
- `Need:` Not needed
- `Why:` planning slice only
- `Artifact:` n/a

### Ask
- `Ready: yes`
- `Next:` after `TASK-0044` lands, update `init-project` bootstrap and templates to match the new knowledge-base entry shape

### Ticket Move
- `Now:` `status: done`, `phase: complete`, archived under `tickets/archive/`
- `On approval:` approved on 2026-04-09 and implemented after `TASK-0044` landed in the same batch
- `Follow-ups:` optional deeper doc scaffolds can be ticketed later if the lighter default proves insufficient
- `Blocked in building?:` yes; needs the architecture/doc-map target from `TASK-0044`

## Acceptance Criteria
- [x] AC-1: `init-project` scaffolds the agreed top-level knowledge-base entry surfaces defined by `TASK-0044`
- [x] AC-2: bootstrap/migration docs explain the new shape clearly for both greenfield and brownfield repos
- [x] AC-3: the default scaffold stays intentionally lightweight and avoids low-value empty doc sprawl
- [x] AC-4: one fresh-bootstrap smoke check proves the generated shape matches the intended map/docs/ticket flow

## Working Notes
- This ticket is intentionally downstream of the architecture-map ticket so the bootstrap follows a real target instead of guessing.
- The bootstrap currently stops at the lighter docs/tickets skeleton; this is a parity upgrade, not a full redesign of all starter files.
- Result: `init-project` now scaffolds `ARCHITECTURE.md` and `docs/specs/README.md`, updates the docs-state guidance, and stops referring to the retired `ralphplan` name.

## Inspiration
- Source: OpenAI, "Harness engineering: leveraging Codex in an agent-first world" https://openai.com/index/harness-engineering
- Relevant takeaway: the repository knowledge base shape should be deliberate and scaffolded, not rediscovered piecemeal in each new repo.

## Implementation Notes
- Touched areas:
  - `skills/init-project/SKILL.md`
  - `skills/init-project/README.md`
  - `skills/init-project/scripts/bootstrap.sh`
  - `skills/init-project/references/*`
- Reused patterns:
  - docs-first bootstrap
  - ticket-first execution
  - progressive disclosure
- Guardrails:
  - keep default scaffold compact
  - avoid empty taxonomy spam

## Evidence
- [x] Tests
- [x] Typecheck
- [x] Lint
- [x] QA / manual verification

- `bash skills/init-project/scripts/bootstrap.sh /tmp/codexter-init-smoke.G9B9l7`
- Manual review of `/tmp/codexter-init-smoke.G9B9l7/ARCHITECTURE.md`
- Manual review of `/tmp/codexter-init-smoke.G9B9l7/docs/specs/README.md`
- `python3 tickets/scripts/check_ticket_metadata.py`
- `git diff --check`

## Review Packet
- `reviewed_at:` 2026-04-09 17:07 +0100
- `rubrics_used:` implementation-plan,spec-contract
- `overall_score:` 4.5
- `overall_threshold:` 4.0
- `overall_verdict:` pass
- `rerun_required:` false
- `evidence_quality:` pass
- `integration_readiness:` pass
- `traceability:` pass
- `freshness:` pass
- `hard_gate_failures:` []
- `blocking_findings:` []
- `next_action:` none; archive the completed ticket after writeback

## Blockers
- none

## Handoff
- Current state: complete and archived. `init-project` now scaffolds the architecture map and specs index as part of the default docs-first starter shape.
- Resume from: `skills/init-project/scripts/bootstrap.sh`, `skills/init-project/SKILL.md`, and the reference templates when the default scaffold shape changes again

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter. Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then move the ticket into `tickets/archive/` or set `status: done` briefly if you intentionally keep a short-lived visible completion state first.
