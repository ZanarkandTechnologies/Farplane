# Turn clock

- **Event:** `PostToolUse`, matched to `Bash`, `Edit` and `Write`.
- **Entrypoint:** `turn_clock.sh` (five-second timeout; plain `sh` with
  builtins, so a tool call costs one `date`).
- **Purpose:** Every 45 minutes since the user's last message, tell the thread
  to finish the smallest ask, commit it on its own and say so, then carry on.
  On 13 Nov 2026 five asks lost about 15 hours this way: a small change (white
  dots on a scan) was finished early but sat inside a 12-hour turn bundled
  with two larger ones, so Kenji could not use it.

## Behavior

[`capture_user_turn.py`](../user-turn/capture_user_turn.py) writes
`~/.farplane/turns/<session id>` at each user message: the start time and how
many 45-minute slots were already announced. The hook adds one line of context
when a new slot starts. It never blocks a tool or ends a turn, and stays
silent when:

- `FARPLANE_AGENT_RUNTIME` is not `claude`;
- the call comes from a subagent (the payload carries `agent_id`);
- the session has no start file, or the current slot was already announced.

`FARPLANE_TURN_CLOCK_SECONDS` changes the slot length (tests);
`FARPLANE_TURNS` moves the folder.

## Test

```bash
.venv/bin/python -m unittest bin.tests.test_turn_clock_hook
```
