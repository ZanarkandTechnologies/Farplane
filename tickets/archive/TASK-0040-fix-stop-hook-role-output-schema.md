---
ticket_id: TASK-0040
title: fix stop-hook role output schema
phase: complete
status: done
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-08T18:20:00Z
updated_at: 2026-04-08T18:28:00Z
next_action: archived after making the stop-hook schema validator-compatible and verifying the live reviewer path no longer falls back to reviewer unavailable
last_verification: `python3 -m py_compile bin/stop_hook.py bin/test_stop_hook.py`, `python3 -m unittest discover -s bin -p 'test_*.py'`, `git diff --check`, direct live reviewer subprocess repro, and isolated live `~/.codex/bin/stop_hook.py` repro passed
linked_docs:
  - docs/specs/review-gates.md
---

# TASK-0040: fix stop-hook role output schema

## Summary
Repair the stop-hook role output schema so `codex exec` accepts it again and reviewer/orchestrator no longer fail with `invalid_json_schema`.

## Scope
- In:
  - `bin/stop_hook_output.schema.json`
  - hook-role TOML prompt contracts
  - focused verification of the live reviewer path
- Out:
  - broader stop-hook routing changes
  - review rubric redesign

## Plan

### Pitch
- `Req:` stop the live hook from falling back to `reviewer unavailable`
- `Bet:` requiring every schema property and allowing nullable gate fields will satisfy the current `codex exec` schema validator while keeping the role contract stable
- `Win:` reviewer and orchestrator subprocesses run normally again

### B -> A
- `Before:` the schema declares optional properties that the current API rejects, so the reviewer subprocess exits early with `invalid_json_schema`
- `After:` the schema requires every property and roles return `null` for unused gate fields
- `Outcome:` the live hook can classify turns instead of taking the unavailable fallback

### Delta
- `Touch:` `bin/stop_hook_output.schema.json`, `agents/reviewer.toml`, `agents/orchestrator.toml`
- `Keep:` current stop-hook decisions and parse logic
- `Change:` schema validity and prompt output contract
- `Delete/Avoid:` further special-case fallback logic

### Core Flow
```pseudo
make all schema properties required
allow gate fields to be null
update role prompts to emit null for unused gate fields
re-run live reviewer subprocess
```

### Proof
- `P1:` direct live `codex exec` reviewer subprocess exits successfully
- `P2:` isolated live `stop_hook.py` invocation no longer reports reviewer unavailable
- `Risk:` prompt contracts drift from parser expectations
- `Rollback:` revert schema and prompt changes together

### Plan Review
- `Refs:` `bin/stop_hook.py`, `bin/stop_hook_output.schema.json`, live reviewer subprocess repro
- `Scope:` schema contract fix only
- `Proof:` direct live repro plus unit hygiene
- `Guardrails:` keep nullable gate fields parser-compatible
- `Fixes:` patch the schema, not the symptom

### Delegation
- `Need:` Not needed
- `Why:` bounded hook contract fix
- `Artifact:` n/a

### Ask
- `Ready: yes`
- `Next:` patch schema and role prompts, then verify live hook behavior

### Ticket Move
- `Now:` `status: building`, `phase: building`
- `On approval:` n/a
- `Follow-ups:` none expected
- `Blocked in building?:` no

## Acceptance Criteria
- [x] AC-1: `stop_hook_output.schema.json` is accepted by the current `codex exec` response-format validator
- [x] AC-2: reviewer and orchestrator role prompts describe null-valued unused gate fields
- [x] AC-3: live reviewer subprocess no longer exits with `invalid_json_schema`
- [x] AC-4: isolated live stop-hook repro no longer reports reviewer unavailable

## Working Notes
- The direct live repro showed `invalid_json_schema: 'required' ... Missing 'overall_score'`.
- `parse_role_output()` already tolerates `None` for the gate fields, so the parser side does not need a semantic change.

## Implementation Notes
- Touched areas: schema file and hook-role TOML instructions
- Reused patterns: existing parser handling for `None`
- Guardrails: keep the standard fields non-null and keep gate fields nullable

## Evidence
- [x] Tests
- [x] Typecheck / syntax verification
- [x] Lint / diff hygiene
- [x] QA / manual verification

- Commands:
  - `python3 -m py_compile bin/stop_hook.py bin/test_stop_hook.py`
  - `python3 -m unittest discover -s bin -p 'test_*.py'`
  - `git diff --check`
- Manual verification:
  - direct live reviewer subprocess repro now exits `0` and writes a valid output payload instead of returning `invalid_json_schema`
  - isolated live `~/.codex/bin/stop_hook.py` repro now returns a normal reviewer decision instead of `reviewer unavailable`

## Review Packet
- `reviewed_at:` 2026-04-08 19:28 +0100
- `rubrics_used:` ["code-quality", "evidence-quality", "integration-readiness"]
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
- `next_action:` keep the stop-hook schema aligned with the current `codex exec` response-format validator and keep unused gate fields nullable at the schema level

## Blockers
- none

## Handoff
- Current state: implemented and archived; the live hook now loads its role configs and the reviewer subprocess returns a normal decision
- Resume from: no follow-up expected unless the response-format validator changes again

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter. Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then move the ticket into `tickets/archive/` or set `status: done` briefly if you intentionally keep a short-lived visible completion state first.
