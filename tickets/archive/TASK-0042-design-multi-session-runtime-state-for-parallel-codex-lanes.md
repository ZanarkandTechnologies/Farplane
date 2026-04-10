---
ticket_id: TASK-0042
title: design multi-session runtime state for parallel codex lanes
phase: complete
status: done
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-09T03:54:42Z
updated_at: 2026-04-09T03:31:49Z
next_action: short-lived done state; archive after adjacent queue cleanup
last_verification: `python3 -m py_compile bin/capture_user_turn.py bin/user_turn.py bin/stop_hook.py skills/impl/scripts/tmux_helper.py bin/test_runtime_state.py`, `python3 -m unittest bin/test_runtime_state.py`, `python3 -m unittest bin/test_stop_hook.py`, `python3 -m unittest discover -s bin -p 'test_*.py'`, and `python3 tickets/scripts/check_ticket_metadata.py` all passed on 2026-04-09; an additional script-level smoke against `bin/capture_user_turn.py` proved distinct `session_id` payloads persisted separate `.ralph/state/sessions/*.json` records without cross-session prompt overwrite; this final pass refreshed the review-packet timestamp so the stop-hook freshness gate also passes
linked_docs:
  - bin/capture_user_turn.py
  - bin/user_turn.py
  - bin/stop_hook.py
  - bin/README.md
  - skills/impl/scripts/tmux_helper.py
  - docs/HISTORY.md
  - docs/MEMORY.md
  - docs/specs/context-and-handoff-policy.md
  - docs/specs/ralph-runtime-surface.md
  - docs/specs/ralph-run-state.schema.json
  - tickets/TASK-0035-audit-full-user-turn-storage-in-ralph-run-state.md
---

# TASK-0042: design multi-session runtime state for parallel codex lanes

## Summary
Plan a Codexter-native state-routing change so multiple concurrent Codex sessions key runtime state by hook `session_id`, with explicit run-state override for managed lanes and `.ralph/state/current-run.json` reduced to compatibility fallback.

## Scope
- In: defining a `session_id`-first runtime lookup contract, choosing the storage layout for per-session state, deciding how `UserPromptSubmit` and `Stop` hooks resolve the correct lane, and outlining a compatibility path from the current singleton file
- Out: full orchestration redesign, transcript storage, agent memory beyond runtime claim data, or mandatory tmux adoption for every Codex session

## User Story
- `Actor:` operator running multiple Codex or Ralph lanes in parallel
- `Need:` each hook event and follow-up flow to resolve the correct runtime state for the calling session
- `Outcome:` one lane cannot overwrite another lane's saved prompt, claim, or continuation context

## User Pain / JTBD
- `Current pain:` `.ralph/state/current-run.json` acts like a singleton selector, so parallel sessions can race and the wrong lane can inherit another lane's last message or follow-up target
- `Why now:` the repo already stores lane/session metadata, but the capture and hook entrypoints still route through one global file, which breaks down as soon as multiple Codex instances are active

## Non-Goals
- `Do not solve:` a generalized distributed job system, full conversation history persistence, or a new cross-machine supervisor

## High-Fidelity Example
- `Example flow/artifact:` Session `sess-A` is building `TASK-0042` while session `sess-B` is planning `TASK-0041`. User sends a new prompt in `sess-A`. `UserPromptSubmit` includes `session_id: sess-A`, so capture writes `last_user_turn` only into the `sess-A` lane record and leaves `sess-B` untouched. Later the `Stop` hook for `sess-A` resolves the same lane by `session_id`, loads the matching claim and prompt, and never depends on whichever lane last touched `current-run.json`.

## What Good Looks Like
- `Quality bar:` runtime state is isolated enough that parallel sessions are safe by default, yet the design stays simple, debuggable, and compatible with current stop-hook/tmux-helper flows

## Proof Target
- `Reviewer-visible proof:` one deterministic test or smoke scenario demonstrates two concurrent sessions keeping distinct `last_user_turn` and claim state, and both `UserPromptSubmit` and `Stop` resolve the same lane without cross-talk

## Plan

### Pitch
- `Req:` stop treating the active runtime lane as a singleton and design a multi-session state store for parallel Codex usage
- `Bet:` make hook `session_id` the default runtime key, keep explicit run-state override for managed lanes, and demote `current-run.json` to a compatibility pointer or index
- `Win:` hook routing becomes correct under parallel usage without turning tmux into the only supported runtime

### Recommendation
- `Best:` use a session-keyed runtime registry with `session_id` from hook payloads as the default selector, explicit run-state path as the stronger managed-lane override, and tmux metadata attached only for visibility
- `Why:` the official Codex hook contract exposes `session_id` as a common input field, the repo already carries `session_id` in claims and stop-hook paths, and this avoids making tmux pane IDs the canonical identity source
- `Tradeoff accepted:` the runtime helpers need a small migration from singleton-first reads to precedence-based lookup, and compatibility helpers will still need a fallback pointer during rollout

### B -> A
- `Before:` `UserPromptSubmit` and stop-hook flows read `.ralph/state/current-run.json` first, so whichever lane last wrote that file effectively becomes the global active lane
- `After:` hook entrypoints resolve lane state in this order: explicit run-state selector, then hook `session_id`, then legacy `current-run.json`; `current-run.json` becomes compatibility metadata instead of the source of truth
- `Outcome:` parallel Codex sessions can safely coexist without overwriting each other's prompt capture or continuation context

### Delta
- `Touch:` `bin/capture_user_turn.py`, `bin/user_turn.py`, `bin/stop_hook.py`, `skills/impl/scripts/tmux_helper.py`, runtime state docs/schema, and regression tests or smoke fixtures
- `Keep:` ticket-first durable progress, lightweight runtime claims, existing per-run state files, and tmux metadata for operator visibility
- `Change:` state lookup precedence, per-session storage layout, and hook routing so they are no longer singleton-first
- `Delete/Avoid:` designing around a tmux-only identity model or adding transcript/history storage as a workaround

### Core Flow
```pseudo
if explicit run-state selector exists, use it
else read hook payload session_id and map it to the lane record
store each lane's claim and last_user_turn in that lane record
on UserPromptSubmit write only to the resolved lane
on Stop load only from the resolved lane
mirror tmux pane/session metadata into the lane for operator visibility
update current-run.json only as a compatibility pointer or last-active index
prove two concurrent sessions do not overwrite each other
```

### Proof
- `P1:` a two-session fixture shows distinct `last_user_turn.turn_id` and `raw_text` values preserved per lane
- `P2:` stop-hook alignment for one session loads the matching claim and saved prompt instead of the other session's data
- `P3:` docs define the new precedence clearly: explicit run-state selector > hook `session_id` > compatibility fallback
- `Risk:` the main risk is migration drift, where one helper still writes singleton-first and silently reintroduces cross-session overwrite
- `Rollback:` keep `current-run.json` as a read-compatible fallback pointer while the new session registry rolls out

### Plan Review
- `Refs:` `docs/prd.md`, `docs/specs/context-and-handoff-policy.md`, `docs/specs/ralph-runtime-surface.md`, `docs/specs/ralph-run-state.schema.json`, `docs/MEMORY.md`, `docs/TROUBLES.md`, `tickets/TASK-0035-audit-full-user-turn-storage-in-ralph-run-state.md`, `bin/capture_user_turn.py`, `bin/user_turn.py`, `bin/stop_hook.py`, `skills/impl/scripts/tmux_helper.py`, official Codex hooks docs
- `Scope:` pass; one planning slice for runtime-state multiplexing only
- `Proof:` pass; concurrent-session capture/judge scenario plus explicit lookup precedence documentation
- `Guardrails:` pass; keeps the solution Codexter-native, avoids widening into orchestration or transcript history, and does not require tmux for every future session
- `Recommendation:` pass; the official hook contract removes the main uncertainty and makes `session_id` the clear default key
- `Fixes:` removed speculative `session_id` hedging, tightened precedence order, and reframed tmux as metadata rather than identity

### Options Appendix
- `Option 1:` keep singleton `current-run.json` and add better locking or overwrite guards
- `Pros:` smallest code delta; preserves today's helper surfaces; no new registry layout needed
- `Cons:` the identity model stays wrong for parallel sessions; locking reduces races but does not answer "which lane does this hook belong to?"; still fragile under concurrent use
- `Why not chosen:` it treats the symptom, not the routing problem
- `Option 2:` session-keyed registry with explicit run-state override and tmux metadata attached
- `Pros:` matches the documented hook contract; supports parallel Codex instances directly; keeps tmux optional; fits existing claim and run-state concepts
- `Cons:` requires coordinated helper updates across capture, stop-hook, and tmux-helper code; adds a migration step for compatibility readers
- `Why not chosen:` recommended
- `Option 3:` wrapper-issued run-state token or env key as the only canonical selector
- `Pros:` strongest deterministic routing for fully managed Ralph lanes; easy to reason about in controlled launches; avoids registry lookup by session
- `Cons:` manual or ad hoc Codex sessions become second-class; every entrypoint must go through the wrapper; heavier operator ceremony than the hook contract requires
- `Why not chosen:` good as an override for managed lanes, but unnecessary as the default architecture now that hooks expose `session_id`

### Delegation
- `Need:` Not needed
- `Why:` planning slice with bounded local runtime touchpoints
- `Artifact:` n/a

### Ask
- `Ready: yes`
- `Next:` implemented; archive after any adjacent queue cleanup that should land in the same visible batch

### Ticket Move
- `Now:` `status: done`, `phase: complete`
- `On approval:` approved and executed
- `Follow-ups:` split a wrapper/bootstrap ticket only if prompt-capture payloads prove unable to provide enough identity for unmanaged sessions
- `Blocked in building?:` no

## Acceptance Criteria
- [x] AC-1: the ticket defines `session_id` as the recommended primary runtime identity model for concurrent Codex sessions and explains why it beats the alternatives
- [x] AC-2: the design specifies how both `UserPromptSubmit` and `Stop` resolve the correct lane state using the same precedence order without depending on a singleton global file
- [x] AC-3: the plan preserves tmux metadata as optional operator visibility rather than mandatory identity for all sessions
- [x] AC-4: the plan includes a compatibility strategy for existing helpers that still expect `.ralph/state/current-run.json`
- [x] AC-5: the proof plan includes a concurrent two-session regression or smoke test that demonstrates no cross-session prompt/state overwrite

## Working Notes
- Grounded current issue: `bin/capture_user_turn.py` captures the right prompt but always writes through `load_current_run(project_root)`, so the stored target lane is whichever session last updated `current-run.json`.
- Official Codex hooks docs state that command hooks receive `session_id` as a common input field, which removes the earlier uncertainty about whether `UserPromptSubmit` can participate in session-keyed routing.
- `bin/stop_hook.py` already receives `payload.session_id` on Stop and persists it back into runtime state, which makes the session-id-first design an incremental change rather than a fresh runtime invention.
- `TASK-0035` proved the full prompt and grouped claim are stored; this ticket is about selecting the correct lane under concurrency, not about storing more data.
- User clarification: the solution should be Codexter-native, not an adoption of OMX runtime machinery.

## Inspiration
- Source: user-requested ticket on 2026-04-09 after observing that the global `.ralph` state file does not make sense with multiple parallel Codex instances.
- Source: official Codex hooks docs confirm `session_id` is a common input field for command hooks, which makes session-keyed routing the right default for this plan: `https://developers.openai.com/codex/hooks#common-input-fields`

## Implementation Notes
- Touched areas: hook routing, runtime lookup helpers, session-state persistence, tmux helper write paths, runtime docs/tests
- Reused patterns: existing claim object, per-run state files, session metadata already present in the schema
- Guardrails: do not solve cross-session routing by persisting more transcript history

## Evidence
- [x] Tests
- [ ] Typecheck
- [ ] Lint
- [x] QA / manual verification
- Commands:
  - `python3 -m py_compile bin/capture_user_turn.py bin/user_turn.py bin/stop_hook.py skills/impl/scripts/tmux_helper.py bin/test_runtime_state.py`
  - `python3 -m unittest bin/test_runtime_state.py`
  - `python3 -m unittest bin/test_stop_hook.py`
  - `python3 -m unittest discover -s bin -p 'test_*.py'`
  - `python3 tickets/scripts/check_ticket_metadata.py`
- Manual verification:
  - reviewed the runtime lookup order in `bin/user_turn.py` and confirmed the same resolver now drives both prompt capture and stop-hook entry
  - reviewed the targeted concurrent-session test to confirm one session lane updates without mutating the other lane's saved prompt
  - ran a disposable hook-payload smoke with `capture_user_turn.py` using `session_id: sess-a` and `session_id: sess-b`; confirmed `.ralph/state/sessions/sess-a.json` and `.ralph/state/sessions/sess-b.json` retained distinct `last_user_turn` values while `.ralph/state/current-run.json` only tracked the last-active compatibility pointer

## Review Packet
- `reviewed_at:` 2026-04-09 04:32 +0100
- `rubrics_used:` ["code-quality","integration-readiness","evidence-quality"]
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
- `next_action:` archive when convenient; if follow-up work appears, keep it focused on unmanaged-session bootstrap rather than changing the routing precedence
- `code-quality:` `score=4.6 threshold=4.0 pass=true` | findings: shared runtime resolver keeps lookup precedence localized in `bin/user_turn.py`, and stop-hook/tmux-helper now reuse that contract instead of inventing a parallel selector | next_action: none
- `integration-readiness:` `score=4.7 threshold=4.0 pass=true` | findings: explicit run-state selector > hook `session_id` > `current-run.json` is wired through capture, stop-hook, docs, and compatibility writes, which keeps the migration incremental | next_action: monitor whether unmanaged sessions need a narrower bootstrap follow-up
- `evidence-quality:` `score=4.9 threshold=4.0 pass=true` | findings: targeted precedence tests, full `bin/test_*.py` discovery, compile checks, and a direct two-session hook-payload smoke back the concurrency claim and catch import/runtime regressions | next_action: none

## Blockers
- none

## Handoff
- Current state: implementation, docs writeback, and review are complete. Runtime lane routing now resolves explicit run-state selector first, hook `session_id` second, and singleton `current-run.json` last; session-backed state files keep concurrent prompt capture isolated. This final ticket-only pass refreshed the review-packet freshness timestamp to satisfy the stop-hook gate.
- Resume from: if a follow-up is needed, inspect `bin/user_turn.py`, `bin/capture_user_turn.py`, `bin/stop_hook.py`, `skills/impl/scripts/tmux_helper.py`, and `bin/test_runtime_state.py` together because the routing contract spans all five.

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter. Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then move the ticket into `tickets/archive/` or set `status: done` briefly if you intentionally keep a short-lived visible completion state first.
