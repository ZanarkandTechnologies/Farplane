---
ticket_id: TASK-0051
title: add session aliasing and init-session workflow
phase: complete
status: done
owner: codex
priority: high
depends_on:
  - TASK-0046
blocked_by: []
ready: false
approval_required: false
created_at: 2026-04-10T02:19:37+0100
updated_at: 2026-04-10T02:55:10+0100
next_action: none; session aliasing and ticket-visible claim alias landed and the ticket is archived
last_verification: python3 -m unittest bin/test_runtime_state.py; python3 tickets/scripts/check_ticket_metadata.py; python3 bin/check_doc_parity.py; git diff --check
linked_docs:
  - hooks.json
  - bin/capture_user_turn.py
  - bin/user_turn.py
  - bin/README.md
  - docs/specs/context-and-handoff-policy.md
  - docs/MEMORY.md
  - tickets/README.md
  - tickets/templates/ticket.md
  - docs/HISTORY.md
---

# TASK-0051: add session aliasing and init-session workflow

## Summary
Add stable per-session aliases on top of existing `session_id` runtime state, mirror the human-facing claim alias onto the ticket as board-visible state, and leave room for an optional `init-session` rename path without overloading ticket `owner`.

## Scope
- In:
  - session alias fields in `.harness/state/sessions/{session_id}.json`
  - one ticket-visible claim field such as `claimed_by` or `active_session_name`
  - first-use alias initialization from the existing `UserPromptSubmit` hook path
  - a small fixed alias pool such as `agent-01` through `agent-10`
  - status/runtime output that shows alias plus current ticket assignment
  - a lightweight optional `init-session` path for manual rename or explicit reassignment
- Out:
  - changing ticket `owner` semantics
  - storing raw `session_id` in ticket frontmatter unless later evidence proves it is needed
  - depending on an upstream SessionStart hook that the repo has not verified yet
  - a full session/team scheduler

## User Story
- `Actor:` operator working across multiple concurrent Codex sessions
- `Need:` know which live session is which without relying on opaque `session_id` strings or every ticket frontmatter saying `owner: codex`
- `Outcome:` multi-session coordination becomes legible while keeping one-ticket-one-session as the default anti-context-rot practice

## User Pain / JTBD
- `Current pain:` all tickets show `owner: codex`, and live sessions are distinguishable mainly by raw `session_id`, tmux pane, or remembered context, which is weak when several sessions are open
- `Why now:` the runtime already keys state by `session_id`, but it still lacks a human-meaningful alias layer for operators and prompt/runtime surfaces

## Non-Goals
- `Do not solve:` persistent user identities, role-based access control, or a full team-runtime mailbox model

## High-Fidelity Example
- `Example flow/artifact:` the first time a session submits a prompt, the `UserPromptSubmit` hook sees `session_id=sess_abc`, creates `.harness/state/sessions/sess_abc.json` with `session_name=agent-03`, and records `current_ticket_id=TASK-0033` if known. The ticket for `TASK-0033` now shows `claimed_by: agent-03`, while runtime keeps the raw `session_id`. Status surfaces later show `agent-03 -> TASK-0033`. If the operator wants a better name, they run `init-session --name cli-fix`, and the same session becomes `cli-fix -> TASK-0033`.

## What Good Looks Like
- `Quality bar:` every live session has a stable human-readable alias, the board can show who currently claims a ticket, and the runtime makes reassignment explicit instead of silently reusing context

## Proof Target
- `Reviewer-visible proof:` a hook-payload or fixture path shows first-use alias creation, ticket claim writeback shows the same human-facing alias without storing raw session ids, status output surfaces alias with the current ticket, and the docs explain that one ticket per session is the default while reuse is explicit and exceptional

## Plan

### Pitch
- `Req:` make concurrent Codex sessions legible while keeping the ticket board closer to a future local-Linear model
- `Bet:` use a hybrid split where the ticket stores a human-facing claim alias and the runtime stores the raw `session_id` plus session metadata
- `Win:` operators get stable readable session names now, and the board moves toward a stronger ticket-native state model without storing transport-level IDs in frontmatter

### Recommendation
- `Best:` use a hybrid model: auto-assign a stable alias from a small pool on first `UserPromptSubmit`, persist it in session runtime state, mirror only the human-facing alias onto the ticket as `claimed_by` or an equivalent field, and keep raw `session_id` runtime-only
- `Why:` this fits the existing runtime architecture, keeps the ticket board closer to a local Linear-style execution surface, and avoids making `owner` or raw transport IDs do the wrong job
- `Tradeoff accepted:` the first version adds one new ticket-state field and one runtime alias field, but avoids a larger ticket metadata redesign until this claim model proves useful

### B -> A
- `Before:` runtime state resolves by `session_id`, but there is no human-readable alias, no fixed naming pool, and ticket `owner: codex` tells the operator nothing about which live session is active
- `After:` each session gets a persisted alias such as `agent-03`, each active ticket can show a human-facing claim like `claimed_by: agent-03`, and optional manual rename can improve that alias without changing the underlying `session_id`
- `Outcome:` multi-session coordination is easier, and the ticket board becomes more useful as a future local-kanban surface

### Delta
- `Touch:` `bin/capture_user_turn.py`, `bin/user_turn.py`, `tickets/README.md`, `tickets/templates/ticket.md`, runtime/session-state docs, maybe `bin/README.md`, and a small `init-session` entrypoint if the rename path is included in the same slice
- `Keep:` `session_id` as the true runtime key and `owner: codex` as ticket-level broad ownership
- `Change:` add a human-facing alias layer in runtime and a ticket-visible claim alias field for the board
- `Delete/Avoid:` avoid making aliases the canonical transport identity or tying aliases directly to ticket ids

### Core Flow
```pseudo
receive UserPromptSubmit payload
resolve project root and session_id
load or create .harness/state/sessions/{session_id}.json
if no session_name exists:
  assign first free alias from fixed pool
infer current_ticket_id when safely available
persist session_name + current_ticket_id + last_seen_at
write ticket-visible claim alias when the ticket assignment is explicit
show session_name in status/runtime read surfaces
optionally allow init-session to rename the alias later
```

### Proof
- `P1:` first-use hook replay creates a session-state file with `session_name` and preserves the alias on later prompts for the same `session_id`
- `P2:` one runtime/status read shows `session_name` together with `session_id` and `current_ticket_id`
- `P3:` one ticket can show the human-facing claim alias without storing raw `session_id`
- `P4:` docs clearly state that one ticket per session is the default and that session reuse must be explicit
- `Risk:` alias assignment or ticket-claim writeback collides with the ongoing runtime-surface cleanup in `TASK-0046`
- `Rollback:` land runtime alias persistence first and defer ticket claim-field writeback if the overlap proves too broad

### Plan Review
- `Refs:` `hooks.json`, `bin/capture_user_turn.py`, `bin/user_turn.py`, `docs/specs/context-and-handoff-policy.md`, `docs/MEMORY.md`, `tickets/README.md`, `tickets/templates/ticket.md`, `TASK-0046`, current runtime/session-state handling
- `Checks:` scope pass; proof pass; guardrails pass; rollback pass
- `Fixes:` kept the slice off ticket `owner`, moved the board-visible part to a dedicated claim field instead, avoided assuming SessionStart support, and made the alias pool fixed-size to keep v1 small

### Options Appendix
- `Option 1:` keep ticket `owner` as the session identity and write different owner values into tickets
- `Pros:` reuses an existing visible field
- `Cons:` conflates ticket ownership with live runtime identity; breaks down when one session touches multiple tickets or several sessions coordinate on one ticket
- `Why not chosen:` wrong layer for the problem
- `Option 2:` keep aliases runtime-only and never surface them on the ticket
- `Pros:` simpler implementation; no ticket metadata change
- `Cons:` weak fit for a future local-Linear board because the board still cannot show who currently claims a ticket
- `Why not chosen:` under-shoots the user's stated board goal
- `Option 3:` auto-assign aliases from a small pool on first hook use, store raw transport identity in runtime only, and mirror the human-facing alias onto the ticket as a claim field
- `Pros:` zero-friction default, stable runtime identity, and better board visibility without leaking raw session ids into ticket frontmatter
- `Cons:` slightly more moving parts than a pure runtime-only path
- `Why not chosen:` recommended

### Delegation
- `Need:` Not needed
- `Why:` planning slice only
- `Artifact:` n/a

### Ask
- `Ready: yes`
- `Next:` approve the hybrid aliasing path, then implement first-use session alias creation, add the ticket-visible claim alias, and surface the alias in status/runtime outputs before deciding whether `init-session` ships in the same patch or a follow-up

### Ticket Move
- `Now:` `status: done`, `phase: complete`, archived under `tickets/archive/`
- `On approval:` approved and implemented on 2026-04-10 after the user cleared the overlap concern
- `Follow-ups:` manual rename UX or richer hook-facing session messaging can split into a follow-up if the first patch gets too wide
- `Blocked in building?:` no

## Acceptance Criteria
- [x] AC-1: first-use session alias creation works through the existing hook/runtime path without changing ticket `owner`
- [x] AC-2: each session state file can carry a stable `session_name` plus current ticket assignment
- [x] AC-3: at least one ticket-visible field can show the human-facing claim alias without storing raw `session_id`
- [x] AC-4: at least one status/runtime surface shows alias plus ticket assignment in a human-usable way
- [x] AC-5: docs state that one ticket per session is the default and that session reuse is explicit rather than silent

## Working Notes
- User preference is clear: small fixed name pool, one ticket per session as the default anti-context-rot rule, and hook-based auto-init is preferable to mandatory manual setup.
- Later clarification tightened the design: the ticket board should carry more live assignment state because the long-term goal is a local board closer to Linear, but raw transport identity should still remain runtime-only.
- The unresolved question is not whether aliasing is useful, but whether visible assistant-facing hook text is supported on `UserPromptSubmit`; this plan intentionally does not depend on that.
- Result: first-use prompt capture now initializes `session_name`, session runtime state persists the alias, and ticket frontmatter may mirror the human-facing alias as `claimed_by`.

## Inspiration
- Source: local repo runtime/session-state design and the current multi-session coordination pain surfaced in the user discussion on 2026-04-10.
- Relevant takeaway: `session_id` is already the runtime key; the missing layer is human-readable session identity, not another ticket-ownership field.

## Implementation Notes
- Touched areas:
  - `bin/user_turn.py`
  - `bin/test_runtime_state.py`
  - `tickets/README.md`
  - `tickets/templates/ticket.md`
  - `docs/specs/context-and-handoff-policy.md`
  - `bin/README.md`
  - `docs/HISTORY.md`
  - `docs/MEMORY.md`
- Reused patterns:
  - session-keyed runtime state
  - additive runtime metadata
  - ticket-first durable progress
- Guardrails:
  - no owner-field overloading
  - no unverified SessionStart dependency
  - keep alias pool small and explicit

## Evidence
- [x] Tests
- [x] Typecheck
- [x] Lint
- [x] QA / manual verification

- `python3 -m unittest bin/test_runtime_state.py`
- `python3 tickets/scripts/check_ticket_metadata.py`
- `python3 bin/check_doc_parity.py`
- `git diff --check`
- Manual review of `bin/user_turn.py`, `tickets/README.md`, `tickets/templates/ticket.md`, and `docs/specs/context-and-handoff-policy.md`

## Review Packet
- Scores use the anchored `1.0`-to-`5.0` rubric scale.
- `work_type:` `["planning"]`
- `search_scope:` `{changed_files: ["bin/user_turn.py", "bin/test_runtime_state.py", "tickets/README.md", "tickets/templates/ticket.md", "docs/specs/context-and-handoff-policy.md", "bin/README.md"], related_files: ["hooks.json", "bin/capture_user_turn.py", "docs/MEMORY.md"], invariants_checked: ["MEM-0016", "MEM-0017", "MEM-0020"], docs_checked: ["docs/specs/context-and-handoff-policy.md", "docs/MEMORY.md", "tickets/README.md"]}`
- `reviewed_at:` `2026-04-10 02:55 +0100`
- `rubrics_used:` `["code-quality", "integration-readiness", "evidence-quality"]`
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
- `next_action:` `none; ticket archived after writeback`

## Blockers
- none

## Handoff
- Current state: complete and archived. First-use prompt capture now initializes `session_name`, session runtime state persists `current_ticket_id`, and ticket frontmatter can mirror the human-facing alias as `claimed_by`.
- Resume from: `bin/user_turn.py` if a follow-up adds manual rename UX or richer status messaging

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter. Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then move the ticket into `tickets/archive/` or set `status: done` briefly if you intentionally keep a short-lived visible completion state first.
