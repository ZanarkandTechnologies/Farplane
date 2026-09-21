# Continuation

- **Event:** `Stop` (five-second timeout).
- **Entrypoint:** `continuation_gate.py`.
- **Purpose:** Ask Jev whether a gentle nudge would advance useful work within
  the user's existing request. It cannot certify Goal or ticket completion.
- **Decision:** A probability of at least 0.5 returns scoped continuation feedback;
  at most three identifiable own nudges are allowed per real user turn.

The classifier looks for concrete completion gaps: naming the next correction
instead of doing it, admitting that a requested fix remains incomplete, or
stopping at diagnosis after a fix/finish request. A completed bounded request
does not continue merely because separate validation or an older issue remains.
The feedback uses a level-four Markdown heading plus labeled instruction bullets.
It asks Codex to take one concrete action, using tools when the task requires
them, while retaining the existing scope, approval, safety, and budget boundaries.
A hidden version marker keeps in-flight sessions parseable when this text changes.

It reads complete JSONL rows from a bounded 1 MiB opening window and 8 MiB recent
window, preserving the opening/latest requests without loading a long rollout's
middle. It excludes reasoning and tool output and applies best-effort credential
redaction. Authorized conversation text still goes to the configured provider.
Oversized responses defer to the response-length hook. Unknown transcript/feedback
provenance and provider failures allow stopping; there is no persistent completion
ledger.

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

These cover transcript selection (including a sparse 200 MiB rollout), nudge
bounds, length-gate interaction, and the entrypoint's credential scope/failure
behavior without requiring a live provider.

Run the five-case live classifier check through the same configured provider:

```bash
farplane run -- python3 hooks/continuation/sanity_check.py
```

The sanitized cases cover two premature stops and three legitimate stops. The
command exits nonzero if any score crosses the 0.5 boundary in the wrong direction.
