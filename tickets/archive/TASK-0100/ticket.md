---
ticket_id: TASK-0100
title: remove duplicated ticket link and proof fields
phase: complete
status: done
owner: codex
claimed_by:
priority: medium
depends_on: []
blocked_by: []
ready: true
approval_required: false
requires_qa: false
requires_demo: false
created_at: 2026-04-28T22:21:28Z
updated_at: 2026-04-28T22:26:00Z
next_action: none; contract cleanup implemented and ready for local commit, push not requested
last_verification: 2026-04-29 06:26 +0800 ticket metadata OK; `python3 -m unittest bin.test_ticket_metadata bin.test_stop_hook` OK; structural doc parity OK; harness invariants OK; review artifact `tickets/archive/TASK-0100/artifacts/review-2026-04-29-0626+0800.json` passed at 4.6 overall
---

# TASK-0100: remove duplicated ticket link and proof fields

## Summary
Simplify the ticket contract so frontmatter keeps operational state while the
body owns durable links and detailed proof. Remove `linked_docs` from the
frontmatter contract, stop repeating the artifact root under `Verification`,
and redefine `last_verification` as a one-line current verdict instead of a
second evidence block.

## Scope
- In:
  - ticket template and ticket docs cleanup
  - validator and runtime parser alignment
  - impl-plan reference cleanup where it repeats the old ticket fields
  - a visible module rule for tickets explaining frontmatter vs body ownership
- Out:
  - removing `ready` from the runtime-facing ticket state
  - migrating every archived legacy ticket to the new shape
  - broader ticket-state-machine redesign

## Plan
- `Change:` remove `linked_docs` from the canonical frontmatter contract, make
  `Refs` the canonical durable-link section, drop `Artifacts path` from the
  default `Verification` shape, and keep `last_verification` as a one-line
  status while `Evidence` owns the detailed commands and artifacts.
- `Why:` the current ticket contract stores the same concepts twice, which
  invites drift between YAML state and body content and makes tickets harder to
  trust.
- `Before -> After:` before, durable links could live in both frontmatter and
  `Refs`, proof location was repeated under both `Verification` and `Evidence`,
  and `last_verification` could drift into a mini evidence log; after,
  frontmatter is operational-only, `Refs` is the single docs list, and
  `Evidence` is the single detailed proof section.
- `Touch:` `tickets/templates/ticket.md`, `tickets/README.md`,
  `tickets/AGENTS.md`, `tickets/scripts/check_ticket_metadata.py`,
  `docs/specs/context-and-handoff-policy.md`,
  `skills/impl-plan/references/template.md`,
  `skills/impl-plan/references/examples.md`, `bin/stop_hook.py`,
  `bin/test_stop_hook.py`, `bin/test_ticket_metadata.py`, `docs/MEMORY.md`,
  `docs/HISTORY.md`
- `Inspect:` `tickets/templates/ticket.md`, `tickets/README.md`,
  `docs/specs/context-and-handoff-policy.md`, `bin/stop_hook.py`,
  `skills/impl-plan/references/template.md`, active and archived ticket samples
- `Signature delta:`
  - `tickets/scripts/check_ticket_metadata.py / validate_ticket(path): list[str]`
  - `bin/stop_hook.py / load_ticket(path): dict[str, object]`
  - `tickets/AGENTS.md / ticket_contract(): guidance`
- `Execution steps:`
  - remove the duplicated canonical fields from the ticket template and ticket docs
  - align the validator and stop-hook parser with the reduced frontmatter shape
  - add the ticket-module rule for frontmatter-versus-body ownership
  - write durable memory/history for the new ticket contract invariant
  - run targeted validators/tests, write a review artifact, and archive this ticket
- `Recommendation:` keep `ready` for now because runtime consumers still use it,
  but remove the true duplication fields now instead of waiting for a larger
  state-model rewrite.
- `Blast radius:` ticket authoring, closeout writeback, reset/resume guidance,
  and any runtime code that parses active ticket frontmatter.
- `Risks:` leaving legacy tickets untouched could preserve some old examples,
  or removing `linked_docs` from the contract could miss a hidden consumer if
  runtime parsing assumptions are broader than they look.

## Acceptance Criteria
- [x] AC-1: the canonical ticket template and ticket docs no longer define
      `linked_docs` in frontmatter
- [x] AC-2: `Refs` is documented as the canonical durable-link section and
      `Evidence` as the canonical detailed-proof section
- [x] AC-3: the validator and stop-hook parser no longer depend on
      `linked_docs`
- [x] AC-4: the duplicate `Artifacts path` field is removed from the canonical
      ticket and impl-plan reference templates

## Verification
- `Tests:` `python3 tickets/scripts/check_ticket_metadata.py`; `python3 -m unittest bin.test_ticket_metadata bin.test_stop_hook`
- `Manual checks:` read the updated ticket contract surfaces and confirm the
  frontmatter/body ownership split is explicit and non-overlapping
- `Evidence required:` passing validator/test output plus a fresh review
  artifact for the final contract slice

## Refs
- `tickets/templates/ticket.md`
- `tickets/README.md`
- `docs/specs/context-and-handoff-policy.md`
- `skills/impl-plan/references/template.md`
- `bin/stop_hook.py`

## Evidence
- `Artifacts:` `tickets/archive/TASK-0100/artifacts/review-2026-04-29-0626+0800.json`
- `Commands:` `python3 tickets/scripts/check_ticket_metadata.py`; `python3 -m unittest bin.test_ticket_metadata bin.test_stop_hook`; `python3 bin/check_doc_parity.py`; `python3 bin/check_harness_invariants.py`; `git diff --check -- tickets/templates/ticket.md tickets/README.md tickets/AGENTS.md tickets/scripts/check_ticket_metadata.py docs/specs/context-and-handoff-policy.md skills/impl-plan/references/template.md skills/impl-plan/references/examples.md bin/stop_hook.py bin/test_stop_hook.py bin/test_ticket_metadata.py docs/MEMORY.md docs/HISTORY.md tickets/archive/TASK-0100/ticket.md`
- `Result summary:` the ticket contract now has one source of truth per concern: frontmatter for operational state, `Refs` for durable links, and `Evidence` for detailed proof. The validator and stop-hook parser no longer require `linked_docs`, the duplicate `Artifacts path` line is removed from the canonical template surfaces, and the reduced contract is documented in tracked ticket guidance instead of only in one template file.

## Blockers
- none
