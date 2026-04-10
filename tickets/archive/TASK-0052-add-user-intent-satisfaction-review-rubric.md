---
ticket_id: TASK-0052
title: add user intent satisfaction review rubric
phase: complete
status: done
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: false
approval_required: false
created_at: 2026-04-10T00:00:00Z
updated_at: 2026-04-10T01:29:23Z
next_action: none; archived after the user-intent-satisfaction rubric landed and docs closeout completed
last_verification: `rg -n "user-intent-satisfaction" skills/review/SKILL.md skills/review/README.md skills/review/references docs/specs/review-gates.md`; `python3 tickets/scripts/check_ticket_metadata.py`; `python3 bin/check_doc_parity.py`; `git diff --check`
linked_docs:
  - skills/review/SKILL.md
  - skills/review/README.md
  - skills/review/references/review-rubric-index.md
  - skills/review/references/user-intent-satisfaction.md
  - docs/specs/review-gates.md
  - tickets/templates/ticket.md
  - docs/MEMORY.md
  - docs/HISTORY.md
---

# TASK-0052: add user intent satisfaction review rubric

## Summary
Add a new `user-intent-satisfaction` rubric family to the `review` skill so completion review can score whether the delivered artifact actually satisfies the target user ask, while keeping stronger market-value or willingness-to-pay judgments out of default review unless the ticket includes real evidence for them.

## Scope
- In:
  - one new review family focused on user-intent satisfaction
  - rubric-selection guidance for when to apply it
  - reviewer/search-scope/review-gates updates needed to integrate the new family cleanly
  - explicit limits on when market-viability style judgment is allowed
- Out:
  - full product-strategy or pricing analysis
  - mandatory competitor benchmarking for every ticket
  - replacing `user_intent_impression` as a completion-gate field in the stop hook

## User Story
- `Actor:` reviewer deciding whether a user-facing change is not only correct but worth shipping for the intended user
- `Need:` a rubric that can distinguish "technically works" from "actually satisfies the user ask"
- `Outcome:` review output becomes more useful for user-facing quality without drifting into ungrounded business theater

## User Pain / JTBD
- `Current pain:` the review system is strong on correctness, evidence, and integration, but it still has no first-class family for scoring whether the result actually satisfies the user-facing ask or feels worth the effort from the user’s perspective
- `Why now:` the stop-hook completion gate now has a `user_intent_impression` field, so the review surface should offer a corresponding rubric family instead of leaving that judgment under-specified

## Non-Goals
- `Do not solve:` pricing strategy, business model design, or universal "would they pay for this?" scoring across tickets with no market evidence

## High-Fidelity Example
- `Example flow/artifact:` a ticket improves a product workflow and passes `code-quality`, `integration-readiness`, and `evidence-quality`. Under the new `user-intent-satisfaction` rubric, the reviewer can still score it a `2.0` or `3.0` because the result technically works but does not meaningfully reduce the user’s friction or deliver the leverage promised in the ticket. The review can say exactly why: strong implementation quality, weak user-value delivery.

## What Good Looks Like
- `Quality bar:` the reviewer can explain, with concrete dimensions, why a result is correct but not satisfying enough for the user, without drifting into hand-wavy product vibes

## Proof Target
- `Reviewer-visible proof:` the review index and one new rubric file teach a clear `1.0`-through-`5.0` contract for user-intent satisfaction, and the rubric-selection guidance makes it explicit when that family is appropriate versus when market-value judgment would be overreach

## Plan

### Pitch
- `Req:` give the review system a first-class way to judge whether a result actually satisfies the user-facing ask
- `Bet:` start with one `user-intent-satisfaction` family and explicitly defer broader market-value or willingness-to-pay scoring unless the ticket includes real evidence for it
- `Win:` higher-signal review on user-facing work without encouraging fake pricing or competitor judgments

### Recommendation
- `Best:` add `user-intent-satisfaction` as a new rubric family and keep "user value / market viability / willingness to pay" as an optional future extension only for tickets with explicit user segment, alternative, and price-point context
- `Why:` this captures the real missing review dimension while staying grounded in what the repo usually knows today
- `Tradeoff accepted:` the first family will be narrower than a full product-value rubric, but that is better than teaching reviewers to bluff market truth from thin specs

### B -> A
- `Before:` review can score correctness, evidence, and integration, but user-facing satisfaction is split between generic review prose and the stop-hook’s new completion field
- `After:` review gets a dedicated rubric family for user-intent satisfaction, and stronger business-value judgments remain explicitly conditional on evidence
- `Outcome:` reviewers can give sharper user-facing feedback without overreaching into unsupported market analysis

### Delta
- `Touch:` `skills/review/SKILL.md`, `skills/review/references/review-rubric-index.md`, one new family reference file, maybe `docs/specs/review-gates.md`, and possibly the ticket template if the review packet guidance needs a wording sync
- `Keep:` the existing completion gate and review packet shape
- `Change:` add a user-facing satisfaction family to the review taxonomy
- `Delete/Avoid:` universal "would they pay for it?" scoring with no evidence

### Core Flow
```pseudo
identify user-facing review cases
select user-intent-satisfaction alongside existing quality/evidence families
score dimensions like ask fidelity, outcome completeness, leverage, and worth-it feel
require evidence-backed reasoning for any stronger market or willingness-to-pay claims
keep market-value judgment optional unless the ticket includes explicit user/alternative/price context
```

### Proof
- `P1:` the review skill and rubric index can direct a reviewer to the new family for appropriate tickets
- `P2:` the family reference teaches a concrete `1/2/3/4/5` score guide and skeptic questions
- `P3:` the docs make it explicit that market-viability style scoring requires stronger ticket evidence than most normal tickets provide
- `Risk:` the rubric becomes too fluffy or overlaps too much with existing generic review prose
- `Rollback:` keep the family narrow and user-ask-focused; defer or remove any speculative market-value dimensions

### Plan Review
- `Refs:` `skills/review/SKILL.md`, `skills/review/references/review-rubric-index.md`, `docs/specs/review-gates.md`, `tickets/templates/ticket.md`, `docs/MEMORY.md`
- `Checks:` scope=pass; proof=pass; guardrails=pass; rollback=pass
- `Fixes:` narrowed the proposal from a broad "worth it / pay for it" rubric idea to a safer first family with explicit guardrails on market claims

### Options Appendix
- `Option 1:` keep user-facing judgment only in freeform review prose
- `Pros:` no taxonomy expansion; zero schema churn
- `Cons:` keeps the judgment under-specified; hard to calibrate; duplicates the current problem
- `Why not chosen:` too weak
- `Option 2:` add `user-intent-satisfaction` now and defer market-value scoring unless evidence exists
- `Pros:` grounded; useful immediately; aligns with the new completion-gate field; low risk of fake precision
- `Cons:` narrower than a full product-value rubric
- `Why not chosen:` recommended
- `Option 3:` add a broad combined value / market / willingness-to-pay rubric immediately
- `Pros:` ambitious; potentially strong for product strategy work
- `Cons:` too easy to bluff; most tickets lack the evidence needed to support it
- `Why not chosen:` overreaches for the first slice

### Delegation
- `Need:` Not needed
- `Why:` planning slice only
- `Artifact:` n/a

### Ask
- `Ready: yes`
- `Next:` approve the rubric-expansion slice, then implement the new review family plus its selection guidance

### Ticket Move
- `Now:` `status: done`, `phase: complete`, ready for `tickets/archive/`
- `On approval:` already implemented
- `Follow-ups:` optional future ticket for `user-value` or `market-viability` rubrics only if specs/tickets start carrying explicit user, alternative, and pricing evidence
- `Blocked in building?:` no

## Acceptance Criteria
- [ ] AC-1: the `review` skill and rubric index include a new `user-intent-satisfaction` family
- [ ] AC-2: the new family defines concrete `1.0`-through-`5.0` guidance, skeptic questions, and evidence cues
- [ ] AC-3: rubric-selection guidance explains when to use `user-intent-satisfaction` and when stronger market-value judgment would require additional ticket evidence
- [ ] AC-4: the resulting review guidance helps reviewers judge user-facing satisfaction without defaulting to unsupported pricing or competitor claims

## Working Notes
- User idea on 2026-04-10: maybe review should judge end-user satisfaction, worth-it score, and whether the solution feels worth paying for relative to real alternatives.
- Best immediate interpretation: split the grounded first family (`user-intent-satisfaction`) from the more speculative future family (`user-value` / `market-viability`).
- This should complement the stop-hook `user_intent_impression` completion gate rather than duplicating it blindly.

## Inspiration
- Source: direct user ideation on 2026-04-10 about adding rubric support for user satisfaction, value, and "worth it" judgment in the `review` skill.

## Implementation Notes
- Touched areas: `skills/review/SKILL.md`, `skills/review/README.md`, `skills/review/references/review-rubric-index.md`, `skills/review/references/user-intent-satisfaction.md`, `docs/specs/review-gates.md`
- Reused patterns: existing review family template, anchored 1.0-to-5.0 score guide, skeptic-question format
- Guardrails: keep market/pricing judgments explicitly conditional on evidence rather than default review behavior

## Evidence
- [x] Tests
- [x] Typecheck
- [ ] Lint
- [x] QA / manual verification

- `rg -n "user-intent-satisfaction" skills/review/SKILL.md skills/review/README.md skills/review/references docs/specs/review-gates.md`
- `python3 tickets/scripts/check_ticket_metadata.py`
- `python3 bin/check_doc_parity.py`
- `git diff --check`
- Manual verification: confirmed the new rubric is present in the review skill, index, README, and reference file, and that stronger market-value claims are explicitly gated behind ticket evidence rather than treated as default review expectations
- `Lint:` not run; this slice is docs/markdown only and no additional lint target was needed for acceptance

## Review Packet
- `work_type:` `["planning"]`
- `search_scope:` `{changed_files: ["tickets/TASK-0052-add-user-intent-satisfaction-review-rubric.md"], related_files: ["skills/review/SKILL.md", "skills/review/references/review-rubric-index.md", "docs/specs/review-gates.md", "tickets/templates/ticket.md"], invariants_checked: ["MEM-0023"], docs_checked: ["docs/specs/review-gates.md"]}`
- `reviewed_at:` `2026-04-10 02:29 +0100`
- `rubrics_used:` `["implementation-plan","spec-contract","debloatability"]`
- `overall_score:` `4.6`
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
- `next_action:` `archive the completed ticket`

## Blockers
- none

## Handoff
- Current state: implementation and docs writeback are complete. The review system now has a dedicated `user-intent-satisfaction` family, and stronger market-value judgments are explicitly documented as evidence-dependent rather than default behavior.
- Resume from: no resume required unless a follow-up ticket is opened for richer `user-value` or `market-viability` families.

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter. Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then move the ticket into `tickets/archive/` or set `status: done` briefly if you intentionally keep a short-lived visible completion state first.
