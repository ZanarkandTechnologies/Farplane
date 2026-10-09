# Stop gate

- **Event:** `Stop` (five-second timeout).
- **Entrypoint:** `stop_gate.py`.
- **Purpose:** The one blocking Stop handler. It runs three checks in order and
  returns at most one block per stop. It cannot certify Goal or ticket completion.

| Order | Check | How | Blocks when |
| --- | --- | --- | --- |
| 1 | Length | Deterministic ([`farplane_response.py`](../../bin/core/farplane_response.py)) | Prose is over the word or line limit |
| 2 | Continuation | Jev `nudge` score ([`continuation.py`](../../bin/runtime/continuation.py)) | Score ≥ 0.5 and fewer than three continuation nudges this user turn |
| 3 | Response format | Jev `shape` choice plus `gap::<section>` scores ([`response_format.py`](../../bin/runtime/response_format.py)) | A gap of the chosen shape scores ≥ 0.6, or a completed change that edited files cites nothing |

Continuation and format share one Jev request. Format nudges at most once per
real user turn and names at most two additions.

## Response format

Jev classifies the final answer as one of the shapes in the global contract's
Output Formatting templates (simple answer, proposed change, completed change,
blocked, decision needed, progress), then scores only that shape's missing
sections. A plan is never asked for `Verified:`, and an explanation is never
asked for Before/After.

Proof is deterministic. Any citation means the agent did not forget: a media
embed, a Markdown link, a URL, a fenced block (command output), or a
`Verified:`/`Unverified:` label. A completed change that edited files this turn
(Claude `Edit`/`Write`/`MultiEdit`/`NotebookEdit`, Codex `apply_patch`) and cites
nothing gets one nudge to cite its proof or state `Unverified:` and why.

Short `Verified:`, `Unverified:`, `Limit:` and `Grounding:` lines (at most 30
words) are outside the length budget, so adding proof does not re-trigger the
length check.

## Install and control

Registration lives only in [root `hooks.json`](../../hooks.json). Run
`farplane hooks install` (Codex) or `install.sh --runtime claude` (Claude Code),
then review/trust the changed command in Codex `/hooks`.

`FARPLANE_STOP_CHECKS` selects checks (default `length,continuation,format`);
unknown names are ignored. Provider settings and credential scope are shared with
continuation: missing credentials, provider errors and unknown transcript
provenance allow the stop silently.

## Checks

```sh
python3 -m unittest bin/tests/test_stop_gate.py
farplane run -- python3 hooks/stop-gate/sanity_check.py
```

The live check runs [`eval_cases.json`](eval_cases.json) through the configured
provider. It passes only with zero format nudges on clean answers and at least 80%
of known gaps caught.
