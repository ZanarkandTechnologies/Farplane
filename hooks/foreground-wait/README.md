# Foreground wait

- **Event:** `PreToolUse`, matched to `Bash`.
- **Entrypoint:** `foreground_wait.sh` (five-second timeout; plain `sh`, so a
  Bash call costs a few milliseconds rather than a Python start).
- **Purpose:** Deny a foreground Bash call that sleeps 30 s or more, or polls in
  an `until`/`while`/`for` loop with `sleep`, and tell the model how to rerun
  it. Such calls hold the turn: 912 of them took 23.8 thread-hours across 209
  Claude threads from 15 to 22 Oct 2026. The global rule in
  [`runtimes/AGENTS.md`](../../runtimes/AGENTS.md) ("Never hold a turn in a
  foreground wait") states the policy; this hook enforces it at the call.

## Why deny, not warn

Replays of a real long thread (the product-shot bake-off, 30 foreground polls)
showed the rule and a warning do not move a thread that has already polled many
times: with a warning on every earlier poll, 0 of 4 runs backgrounded the next
wait. Denying the poll itself made 3 of 4 rerun it in the background or under
Monitor; the fourth ended the turn. Claude Code already blocks a bare
foreground `sleep`; this extends that to loops and long sleeps.

## Behavior

The deny reason names the reroutes: `run_in_background: true`, Monitor for a
condition, or `timeout` of 30 000 ms or less for a wait that really is short.
The hook stays silent when:

- `FARPLANE_AGENT_RUNTIME` is not `claude` (Codex has no `run_in_background`);
- the tool is not `Bash`, or the payload has no `sleep`;
- `run_in_background` is true, or `timeout` is 30 000 ms or less.

It reads only the tool input, so a path or description elsewhere in the
payload does not trigger it. It has no network call and writes nothing. To
turn it off, remove its `PreToolUse` entry from [`hooks/hooks.json`](../hooks.json)
and reinstall.

## Install and checks

Registration lives only in [`hooks/hooks.json`](../hooks.json);
`install.sh --runtime claude` renders it into the Claude plugin and
`farplane hooks install` links this folder for Codex, where it stays silent.

```sh
python3 -m unittest bin/tests/test_foreground_wait_hook.py
```

The test replays seven real foreground polls, four non-waits, the background
and short-timeout exemptions, the silent cases, and checks the hook adds under
50 ms over a bare `sh` start.
