---
ticket_id: TASK-0044
title: add architecture map and canonical doc index
phase: complete
status: done
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: false
approval_required: false
created_at: 2026-04-09T16:52:49+0100
updated_at: 2026-04-09T17:07:10+0100
next_action: none; ticket completed after landing ARCHITECTURE.md and canonical doc entrypoint cleanup
last_verification: python3 tickets/scripts/check_ticket_metadata.py; python3 bin/check_doc_parity.py; python3 -m unittest bin/test_doc_parity.py; git diff --check
linked_docs:
  - README.md
  - docs/specs/README.md
  - docs/specs/harness-techniques.md
  - docs/specs/review-gates.md
  - skills/review/SKILL.md
  - skills/review/references/review-rubric-index.md
---

# TASK-0044: add architecture map and canonical doc index

## Summary
Add a root `ARCHITECTURE.md` that explains Codexter's current architecture, major surfaces, and relationships between docs, tickets, skills, subagents, and runtime helpers, then tighten the canonical doc index around it.

## Scope
- In:
  - root `ARCHITECTURE.md`
  - explicit mapping of current harness techniques to repo surfaces
  - a clearer canonical-doc entrypoint from `README.md` and `docs/specs/README.md`
  - clear links to review/rubric surfaces instead of burying them inside skill folders
- Out:
  - changing runtime behavior
  - rewriting every spec into a new taxonomy
  - inventing a second planning system alongside tickets

## User Story
- `Actor:` Codexter operator or agent entering the repo cold
- `Need:` one architecture map that explains how the harness is organized and where the canonical truth for each concern lives
- `Outcome:` faster orientation, less drift between README-level story and deeper docs, and better progressive disclosure

## User Pain / JTBD
- `Current pain:` the current story is spread across `README.md`, `docs/specs/harness-techniques.md`, ticket docs, and skill folders, so the repo has the right pieces but not one clean architecture map
- `Why now:` the recent OpenAI harness comparison highlighted that Codexter's philosophy is already close, but the knowledge-base shape is still less legible than it should be

## Non-Goals
- `Do not solve:` full doc taxonomy redesign, all future architecture changes, or a full docs-site generator

## High-Fidelity Example
- `Example flow/artifact:` an agent reads `AGENTS.md`, then `ARCHITECTURE.md`, then follows links to the exact canonical surface for tickets, review scoring, runtime policy, or current techniques without hunting through the repo

## What Good Looks Like
- `Quality bar:` `ARCHITECTURE.md` is concise, current-state-first, and explicit about what is canonical versus supporting; it reduces README sprawl instead of duplicating it

## Proof Target
- `Reviewer-visible proof:` a new operator can answer where planning lives, where review scoring lives, what the major runtime surfaces are, and which docs are canonical after reading `AGENTS.md` plus `ARCHITECTURE.md`

## Plan

### Pitch
- `Req:` create the missing top-level architecture map and make the docs easier to navigate from one stable entrypoint
- `Bet:` one current-state architecture doc plus a tighter canonical-doc index will improve repo legibility more than scattering another round of local doc edits
- `Win:` the harness knowledge base looks and behaves more like an intentional system of record instead of a good set of parts

### Recommendation
- `Best:` add one root `ARCHITECTURE.md` and use it as the top-level system map, while keeping the detailed behavior docs in `docs/specs/*` and the scoring contract in the review skill references
- `Why:` this matches the user's stated need, avoids exploding the doc surface, and gives `init-project` a clear target shape to scaffold later
- `Tradeoff accepted:` the architecture doc will necessarily summarize some existing docs, so the scope must stay map-like rather than becoming another long-form spec

### B -> A
- `Before:` the repo has a short map `AGENTS.md` and several good canonical docs, but no single architecture map and no clean top-level pointer to the review scoring surfaces
- `After:` `ARCHITECTURE.md` explains the major surfaces and canonical ownership, and the nearby entry docs point to it explicitly
- `Outcome:` new agents and operators get a more legible repo map with less initial search overhead

### Delta
- `Touch:` root docs such as `ARCHITECTURE.md`, `README.md`, `docs/specs/README.md`, and maybe `AGENTS.md`
- `Keep:` tickets as the execution/plan surface and `docs/specs/*` as the behavior/spec surface
- `Change:` add one architecture-level map and tighten canonical doc pointers
- `Delete/Avoid:` avoid copying the full review rubric or full technique inventory into the architecture doc

### Core Flow
```pseudo
read current repo-map docs
define the top-level architecture sections
write one current-state architecture map
link each concern to its canonical detailed doc
trim or retarget nearby docs so the top-level story is coherent
```

### Proof
- `P1:` `ARCHITECTURE.md` names the major harness surfaces and links to the canonical follow-up docs for each
- `P2:` the review scoring contract is clearly discoverable from the new top-level map without duplicating the rubric content
- `Risk:` the new file becomes a second README and drifts quickly
- `Rollback:` keep the file current-state-only and move detailed behavior back to the existing specs and skill references

### Plan Review
- `Refs:` OpenAI harness engineering article, `README.md`, `docs/specs/README.md`, `docs/specs/harness-techniques.md`, `skills/review/*`
- `Scope:` architecture map plus canonical-doc entrypoint cleanup only
- `Proof:` manual orientation pass plus doc-parity and ticket-metadata validation after edits
- `Guardrails:` do not invent fake architecture layers or duplicate the review rubric families verbatim
- `Fixes:` link to review scoring surfaces instead of rewriting them

### Options Appendix
- `Option 1:` just expand `README.md`
- `Pros:` no new file
- `Cons:` README stays overloaded and still mixes product story, setup, runtime surfaces, and architecture mapping
- `Why not chosen:` it worsens the exact “one big surface” problem we are trying to avoid
- `Option 2:` add `ARCHITECTURE.md` and keep other docs mostly where they are
- `Pros:` clean top-level map; preserves progressive disclosure; easiest to scaffold later
- `Cons:` adds one more canonical file that must stay current
- `Why not chosen:` recommended
- `Option 3:` redesign the whole docs tree now
- `Pros:` most ambitious parity with the OpenAI example
- `Cons:` too much surface churn for the current problem
- `Why not chosen:` over-scoped for the first pass

### Delegation
- `Need:` Not needed
- `Why:` planning slice only
- `Artifact:` n/a

### Ask
- `Ready: yes`
- `Next:` approve the architecture-map slice, then write `ARCHITECTURE.md` and update the nearby canonical-doc pointers

### Ticket Move
- `Now:` `status: done`, `phase: complete`, archived under `tickets/archive/`
- `On approval:` approved on 2026-04-09 and implemented in the same batch
- `Follow-ups:` init-project scaffold parity and doc-audit policy should consume the result instead of guessing the desired doc shape
- `Blocked in building?:` no

## Acceptance Criteria
- [x] AC-1: root `ARCHITECTURE.md` exists and explains the current Codexter architecture in repo-grounded terms
- [x] AC-2: the doc makes the review scoring surfaces explicitly discoverable via links to the review skill and rubric index
- [x] AC-3: `README.md` and `docs/specs/README.md` point to the new architecture map in a way that reduces top-level ambiguity
- [x] AC-4: the new doc stays map-like and current-state-first rather than duplicating the detailed behavior specs

## Working Notes
- The user explicitly wants `ARCHITECTURE.md` and noted that some of the architecture story currently lives in `README.md`.
- The review skill already owns the scoring model and should be linked as the canonical scoring surface, not copied into the architecture doc.
- Result: added a root architecture map, pointed `AGENTS.md`, `README.md`, and `docs/specs/README.md` at it, and kept the review scoring contract in `skills/review/*`.

## Inspiration
- Source: OpenAI, "Harness engineering: leveraging Codex in an agent-first world" https://openai.com/index/harness-engineering
- Relevant takeaway: keep `AGENTS.md` short, treat the repo as the system of record, and give agents a map to deeper sources of truth.

## Implementation Notes
- Touched areas:
  - `ARCHITECTURE.md`
  - `AGENTS.md`
  - `README.md`
  - `docs/specs/README.md`
- Reused patterns:
  - current-state-first docs
  - progressive disclosure
  - ticket-first planning
- Guardrails:
  - no duplicate rubric contract
  - no speculative future architecture

## Evidence
- [x] Tests
- [x] Typecheck
- [x] Lint
- [x] QA / manual verification

- `python3 tickets/scripts/check_ticket_metadata.py`
- `python3 bin/check_doc_parity.py`
- `python3 -m unittest bin/test_doc_parity.py`
- `python3 -m py_compile bin/check_doc_parity.py bin/test_doc_parity.py`
- `git diff --check`
- Manual review of `AGENTS.md`, `ARCHITECTURE.md`, `README.md`, `docs/specs/README.md`, and `skills/review/README.md`

## Review Packet
- `reviewed_at:` 2026-04-09 17:07 +0100
- `rubrics_used:` implementation-plan,spec-contract
- `overall_score:` 4.7
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
- Current state: complete and archived. `ARCHITECTURE.md` is now the top-level system map and the nearby entry docs point to it explicitly.
- Resume from: `ARCHITECTURE.md` when the repo-level system map or canonical entrypoint set changes

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter. Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then move the ticket into `tickets/archive/` or set `status: done` briefly if you intentionally keep a short-lived visible completion state first.
