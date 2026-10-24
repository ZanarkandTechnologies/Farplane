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
middle. It accepts Codex rollouts and Claude Code transcripts: in Claude, only
`origin.kind: "human"` rows are requests and only runtime `isMeta` "Stop hook
feedback" rows count as hook feedback. It excludes reasoning and tool output and
applies best-effort credential redaction. Authorized conversation text still goes to
the configured provider. Oversized responses defer to the response-length hook. Unknown transcript/feedback
provenance and provider failures allow stopping; there is no persistent completion
ledger.

## Thread notes

Each thread keeps its own notes at `~/.farplane/memory/notes/<session-id>.md`
(the prompt hook names the path on the thread's first prompt and the global
contract says how to keep it; Claude Code exposes the id as
`$CLAUDE_CODE_SESSION_ID`, the same id this hook receives). A `parent:
<session-id>` line links a sub-thread to the thread that started it; a
desktop `local_` id works too, mapped by the prompt hook under `notes/.desktop/`. When the
thread has notes, the judge gets them as `thread_notes`, its parent's as
`parent_notes`, plus the original request and the last five messages instead of
twenty. It pushes only for unfinished work inside the notes' Task that its Done
when checks still need; ideas outside it, under V2 candidates, or after the
checks pass let the turn end, and a nudge adds a Scope line. The hook only reads
these files (own up to 4 KB, parent up to 2 KB); it fetches nothing and runs no
model of its own. Missing or unreadable notes behave as today. Code:
[`hooks/shared/thread_notes.py`](../shared/thread_notes.py).

Every continuation request also asks whether the user is still deciding: a
question, an explanation, review or proposal request, or a rethink of the design.
Then neither continuation nudge fires, with or without notes. With no notes and an
action request, behaviour is unchanged.

## Install and control

Registration lives only in [`hooks/hooks.json`](../hooks.json). From the primary
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
[`continuation.py`](continuation.py).

## Checks

Run from the repository root:

```sh
python3 -m unittest discover -s bin/tests -p 'test_continuation*.py'
```

These cover transcript selection (including a sparse 200 MiB rollout), nudge
bounds, length-gate interaction, and the entrypoint's credential scope/failure
behavior without requiring a live provider.

Run the live classifier check through the same configured provider:

```bash
farplane run -- python3 hooks/continuation/sanity_check.py
```

The sanitized cases cover premature stops (including asking to confirm an in-cap,
regenerable delete), legitimate stops (including deleting the only copy of data
and waiting on an approval click only the operator can make), thread-notes cases
(in-scope work left, only out-of-scope ideas left, a sub-thread with its parent's notes) and investigate, explain or
propose requests. A case pushes when continuation or proposal scores at least 0.5
and the user is not still deciding. The command exits nonzero on any wrong
decision.
