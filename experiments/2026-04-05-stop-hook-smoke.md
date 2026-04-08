# Experiment: Stop Hook Smoke Test

Date: 2026-04-05

## Goal

Verify that the tracked `Stop` hook can:

1. resolve an active Ralph ticket
2. parse a `RALPH_RESULT`
3. run the Ralph judge path
4. decide whether to continue or stop

## Commands

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

1. The local smoke-eval suite now covers **11 cases**, and the current supported-runtime set passes locally.

- hook replay for missing build evidence
- hook replay for accepted planning output
- current-run selector replay without explicit ticket env
- hook replay for Ralph-mode prose without `RALPH_RESULT`
- judge blocked path
- judge continue-rerun path
- judge build-complete with missing evidence
- judge build-complete with passing evidence
- judge plan-ready advance path
- judge docs-complete path
- tmux follow-up lane spawn replay

2. Hook-style payload for a fixture building ticket with missing evidence returned:

```json
{"decision": "block", "reason": "rerun TASK-9998 in building with explicit missing evidence coverage"}
```

Interpretation:
- the `Stop` hook now recognizes `RALPH_RESULT`
- the hook routes through the Ralph judge
- missing evidence correctly triggers same-ticket continuation
- the missing-evidence regression no longer depends on leaving `TASK-0011` incomplete

3. Hook-style payload for a planning ticket with `plan_ready` returned no stdout and exited `0`.

Interpretation:
- the hook judged the ticket safe to stop
- no same-ticket continuation was requested
- this is the desired path for `ralphplan` success

4. Payload replay using only `cwd` + `.ralph/state/current-run.json` also worked.

Interpretation:
- the prototype no longer depends on `RALPH_TICKET` env as the primary selector
- project-local run state is now sufficient for the hook in payload-driven tests

5. Ralph-mode prose without `RALPH_RESULT` now returns an explicit same-ticket continuation instead of silently stopping as success.

Observed replay:

```json
{
  "decision": "block",
  "reason": "Continue TASK-9997 in building. The last assistant message implied more same-ticket work but ended without an explicit RALPH_RESULT line. Continue the same ticket, update repo/ticket state, and finish with a RALPH_RESULT."
}
```

Interpretation:
- the hook now treats missing `RALPH_RESULT` in execution mode as a contract miss instead of a successful stop
- the operator gets a concrete continuation reason instead of a false completion
- this directly covers the reported "I'm doing it now" failure mode

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

12. The tmux-backed follow-up replay now validates the supported helper surface instead of the retired `bin/ralph_orchestrate.py` / `bin/ralph_tmux.py` pair.

Observed sequence:

- `TASK-0014` was launched in tmux session `ai-brain-local`, pane `%13`
- a `build_complete -> building` stop-hook replay was run in bounded dry-run mode
- the hook log recorded:

```json
{
  "mode": "ralph",
  "ticket_id": "TASK-0014",
  "event": "spawn_followup",
  "followup": {
    "phase": "building",
    "tmux_session": "ai-brain-local",
    "tmux_pane": "%14"
  }
}
```

Interpretation:
- the hook can now hand off to a fresh visible tmux lane using `skills/impl/scripts/tmux_helper.py`
- the new lane is inspectable with the helper's `tail` command or raw `tmux capture-pane`
- the smoke suite now matches the current supported runtime surface

## Next Step

- write refreshed test/lint evidence back into the active ticket so the hook is not blocked by stale unchecked proof
- stress longer, multi-ticket runs
- add a stronger active-ticket selection policy for non-toy concurrent work
