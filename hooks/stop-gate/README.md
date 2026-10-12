# Stop gate

- **Event:** `Stop` (five-second timeout).
- **Entrypoint:** `stop_gate.py`.
- **Purpose:** The one blocking Stop handler. It runs three checks in order and
  returns at most one block per stop. It cannot certify Goal or ticket completion.

| Order | Check | How | Blocks when |
| --- | --- | --- | --- |
| 1 | Length | Deterministic ([`farplane_response.py`](../../bin/core/farplane_response.py)) | Prose is over the word or line limit |
| 2 | Continuation | Jev `nudge` score ([`continuation.py`](../continuation/continuation.py)) | Score ≥ 0.5 and fewer than three continuation nudges this user turn |
| 3 | Response format | Jev `shape` choice, `gap::<section>` and `visible_feature` scores ([`response_format.py`](../shared/response_format.py)) | A gap of the chosen shape or `cold_read` scores ≥ 0.6, a new feature has no video, or a completed change that edited files cites nothing |

Continuation and format share one Jev request. Format nudges at most once per
real user turn and names at most two additions. Format still runs after the
continuation cap is spent.

## Response format

Jev classifies the final answer as one of the shapes in the global contract's
Output Formatting templates (simple answer, proposed change, completed change,
blocked, decision needed, progress), then scores only that shape's missing
sections. A plan is never asked for `Verified:`, and an explanation is never
asked for Before/After.

Every shape is also scored for `cold_read`: would someone who saw only the
user's latest message be lost, because the answer narrates the latest fix
instead of where the request stands, or uses terms coined during the work? A
template-perfect delta report ("reach strip fixed, 6 of 7 agree") fails it;
the nudge asks for the overall state in plain words, what works, what does not,
and the one thing the user must do.

Proof is deterministic once Jev has said whether the turn added a new feature
or multi-step workflow a person would watch (`visible_feature` ≥ 0.6: a screen,
UI flow, interactive page, game, an app's agents or workers acting differently,
or robot or simulation behaviour). Jev judges what the user would see, so launch
code that changes how bunker workers behave counts.

- **New feature** (completed change or a run's last progress update, files
  edited): needs an embedded or linked `.mp4`, `.mov` or `.webm`, or an
  `Unverified:` line saying why there is no video. Screenshots and links alone
  get one nudge to record it.
- **Anything else** (completed change, files edited): any citation means the
  agent did not forget: a media embed, a Markdown link, a URL, a fenced block
  (command output), or a `Verified:`/`Unverified:` label. Citing nothing gets
  one nudge to cite its proof or state `Unverified:` and why.

Edits are Claude `Edit`/`Write`/`MultiEdit`/`NotebookEdit` or Codex
`apply_patch` calls this user turn. Cold-read and shape gaps share one format
nudge per real user turn, naming at most two additions. Proof has its own: when
an earlier format nudge this turn did not ask for proof, the gate asks once more
for the proof or video only, so a Goal/Track/Progress nudge cannot use up the
video check.

Short `Verified:`, `Unverified:`, `Limit:` and `Grounding:` lines (at most 30
words) are outside the length budget, so adding proof does not re-trigger the
length check.

## Install and control

Registration lives only in [`hooks/hooks.json`](../hooks.json). Run
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
