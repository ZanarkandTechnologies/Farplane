# Experiment: Stop Hook Smoke Test

Date: 2026-04-05

## Goal

Verify that the tracked `Stop` hook can:

1. resolve an active Ralph ticket
2. parse a `RALPH_RESULT`
3. run the Ralph judge path
4. decide whether to continue or stop

## Commands

Planning dry-run through orchestrator:

```bash
python3 bin/ralph_orchestrate.py \
  --ticket tickets/building/TASK-0010-ralph-thin-prototype.md \
  --phase planning \
  --dry-run \
  --json
```

Manual hook-style payload for a fixture building ticket with missing evidence:

```bash
python3 - <<'PY'
from pathlib import Path

Path("/tmp/TASK-9998-hook-missing.md").write_text(
    """---
ticket_id: TASK-9998
title: hook missing evidence fixture
phase: building
status: active
owner: codex
priority: medium
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-05T00:00:00Z
updated_at: 2026-04-05T00:00:00Z
next_action: test fixture
last_verification: none
linked_docs: []
---

# TASK-9998: hook missing evidence fixture

## Acceptance Criteria
- [ ] AC-1

## Evidence
- [ ] Tests

## Blockers
- none
""",
    encoding="utf-8",
)
PY

CODEXTER_RALPH_HOOK=1 \
RALPH_TICKET=/tmp/TASK-9998-hook-missing.md \
python3 bin/stop_hook.py <<'EOF'
{
  "hook_event_name": "Stop",
  "last_assistant_message": "RALPH_RESULT: status=build_complete next=building reason=dry_run"
}
EOF
```

## Expected Interpretation

- If evidence gaps remain on the active ticket, the hook should ask to continue same-ticket work.
- If evidence is sufficient, the hook should stop safely and announce that the ticket can advance or complete.

## Findings

1. The local smoke-eval suite now covers **10 cases**, and all 10 currently pass:

- orchestrator planning dry-run
- hook replay for missing build evidence
- hook replay for accepted planning output
- current-run selector replay without explicit ticket env
- judge blocked path
- judge continue-rerun path
- judge build-complete with missing evidence
- judge build-complete with passing evidence
- judge plan-ready advance path
- judge docs-complete path

2. Planning dry-run through the orchestrator returned:

```json
{
  "worker_result": "RALPH_RESULT: status=plan_ready next=building reason=dry_run",
  "judge_verdict": {
    "decision": "advance_ticket",
    "next_phase": "building"
  }
}
```

Interpretation:
- the simpler `ralphplan` path now advances directly to `building`
- this matches the intended two-workflow model

3. Hook-style payload for a fixture building ticket with missing evidence returned:

```json
{"decision": "block", "reason": "rerun TASK-9998 in building with explicit missing evidence coverage"}
```

Interpretation:
- the `Stop` hook now recognizes `RALPH_RESULT`
- the hook routes through the Ralph judge
- missing evidence correctly triggers same-ticket continuation
- the missing-evidence regression no longer depends on leaving `TASK-0011` incomplete

4. Hook-style payload for a planning ticket with `plan_ready` returned no stdout and exited `0`.

Interpretation:
- the hook judged the ticket safe to stop
- no same-ticket continuation was requested
- this is the desired path for `ralphplan` success

5. Payload replay using only `cwd` + `.ralph/state/current-run.json` also worked.

Interpretation:
- the prototype no longer depends on `RALPH_TICKET` env as the primary selector
- project-local run state is now sufficient for the hook in payload-driven tests

6. Real `codex exec` session with `codex_hooks` enabled printed:

```text
hook: Stop
hook: Stop Completed
```

Interpretation:
- the live Codex hook system is now wired and firing
- the previous “stop hook does not work” problem was partly install/config, not only script logic

7. Project-local hook logs now exist at:

```text
Codexter/.ralph/logs/stop-hook.jsonl
```

and contain replay-driven verdicts such as:

```json
{"mode":"ralph","ticket_id":"TASK-0011","decision":"repeat_ralph","next_phase":"building"}
{"mode":"ralph","ticket_id":"TASK-0011","decision":"advance_ticket","next_phase":"building"}
```

8. Real `codex exec` sessions with `codex_hooks` enabled now visibly print:

```text
hook: Stop
hook: Stop Completed
```

Interpretation:
- the live hook path is running end to end
- the installation / feature flag problem is solved

9. After making the hook auto-activate on `RALPH_RESULT` / current-run state and adding raw invocation logging, a real live probe produced:

```text
hook: Stop
hook: Stop Blocked
```

and the project-local hook log recorded:

```json
{
  "mode": "debug",
  "event": "invocation",
  "payload_keys": [
    "cwd",
    "hook_event_name",
    "last_assistant_message",
    "model",
    "permission_mode",
    "session_id",
    "stop_hook_active",
    "transcript_path",
    "turn_id"
  ]
}
```

plus the Ralph verdict:

```json
{
  "mode": "ralph",
  "ticket_id": "TASK-0011",
  "decision": "repeat_ralph",
  "next_phase": "building",
  "reason": "payload_contract_probe_2"
}
```

Interpretation:
- the real live hook now resolves the active ticket from project-local state
- the live hook sees the real Codex payload contract
- the live hook can issue a real blocking/continuation decision, not just a no-op

10. The remaining uncertainty is no longer whether the hook works end to end. It is narrower:

- how stable this behavior is across longer, non-toy runs
- how best to encode active-ticket selection once multiple real client tickets are active at the same time

11. The automated missing-evidence regression now uses a disposable fixture ticket (`TASK-9998`) instead of the live `TASK-0011`.

Interpretation:
- closeout evidence on the active ticket no longer changes the expected missing-evidence replay result
- the smoke eval suite now tests both explicit-selector precedence and current-run selection without coupling to the live board state

## Next Step

- write refreshed test/lint evidence back into the active ticket so the hook is not blocked by stale unchecked proof
- stress longer, multi-ticket runs
- add a stronger active-ticket selection policy for non-toy concurrent work
