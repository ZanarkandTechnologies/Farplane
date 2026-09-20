# Continuation

- **Event:** `Stop` (five-second timeout).
- **Entrypoint:** `continuation_gate.py`.
- **Purpose:** Ask Jev whether a gentle nudge would advance useful work within
  the user's existing request. It cannot certify Goal or ticket completion.
- **Decision:** A probability of at least 0.5 returns scoped continuation feedback;
  at most three identifiable own nudges are allowed per real user turn.

It reads a bounded transcript, preserves the opening/latest requests, excludes
reasoning and tool output, and applies best-effort credential redaction. Authorized
conversation text still goes to the configured provider. Oversized responses defer
to the response-length hook. Unknown transcript/feedback provenance and provider
failures allow stopping; there is no persistent completion ledger.

## Install and control

Registration lives only in [root `hooks.json`](../../hooks.json). From the primary
Farplane checkout, run `farplane hooks install`, then review/trust changed commands
in Codex `/hooks`. Use that control to enable or disable this handler.
`farplane hooks list` displays the configured command; `farplane hooks doctor`
checks its installed target. The installer links this entire folder under
`~/.codex/hooks/`, including this README.

## Configuration and failure behavior

Provider settings are shared with the optional user-turn skill suggestion:
`FARPLANE_JEV_PROVIDER`, `FARPLANE_JEV_ENDPOINT`, and `FARPLANE_JEV_MODEL`.
Credentials are injected through `farplane run` from the installed Farplane source
directory, never the caller's project. Missing credentials trigger a bounded
bootstrap; setup errors are captured and allow stopping quietly. Do not place API
keys in hook registration. Shared implementation lives in
[`bin/runtime/continuation.py`](../../bin/runtime/continuation.py).

## Checks

Run from the repository root:

```sh
python3 -m unittest discover -s bin/tests -p 'test_continuation*.py'
```

These cover transcript selection, nudge bounds, length-gate interaction, and the
entrypoint's credential scope/failure behavior without requiring a live provider.
