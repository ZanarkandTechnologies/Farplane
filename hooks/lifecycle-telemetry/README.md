# Lifecycle telemetry

- **Events:** `UserPromptSubmit`, `Stop`, `SubagentStart`, `SubagentStop`.
- **Entrypoint:** `farplane_console_ping.py` (five-second hook timeout).
- **Purpose:** Send sanitized lifecycle metadata for Farplane UI observation.
  A Stop attempt is not successful task completion.

## Install and control

Registration lives only in [root `hooks.json`](../../hooks.json). From the primary
Farplane checkout, run `farplane hooks install`, then review/trust changed commands
in Codex `/hooks`. Use that control to enable or disable this handler.
`farplane hooks list` displays the configured command; `farplane hooks doctor`
checks its installed target. The installer links this entire folder under
`~/.codex/hooks/`, including this README.

## Configuration and failure behavior

Each registration supplies `--expect-event <CodexEvent>`. The sender compares it
with stdin `hook_event_name`; a mismatch is diagnosed and not sent. The shared
sender handles all four events, so code is not duplicated per registration.

Endpoint selection uses `FARPLANE_TELEMETRY_HOOKS_URL`, then
`FARPLANE_CONVEX_SITE_URL` plus `/telemetry/hooks`. Config is resolved by Core runtime
configuration. Payloads contain sanitized metadata, not full transcripts or final
answers. Missing endpoints skip delivery; network failures allow the turn to end.
HTTP delivery has a two-second timeout and never returns a blocking decision.

Latest per-event receipts live under `~/.farplane/state/hook-delivery/`, respecting
`FARPLANE_STATE_DIR`, and appear in `farplane hooks list`. Status is `unconfigured`,
`attempted`, `accepted`, or `failed`; accepted means HTTP 2xx, not verified UI state.
Receipts exclude credentials and payloads. Transport is shared in
[`bin/runtime/hook_delivery.py`](../../bin/runtime/hook_delivery.py).

Each new Stop payload receives a distinct event key. Farplane UI shows Stop as
idle / “Codex stop attempted”; newer observed tool activity restores running.
SubagentStop stops the child, not the parent.

## Checks

Run both from the repository root:

```sh
python3 -m unittest discover -s bin/tests -p 'test_farplane_console_ping.py'
python3 -m unittest discover -s bin/tests -p 'test_hook_delivery.py'
```

These checks use local fixtures/mocked delivery rather than publishing fake events.
