# Stop gate

- **Event:** `Stop` (five-second timeout).
- **Entrypoint:** `stop_gate.py`.
- **Purpose:** The one blocking Stop handler. It runs three checks in order and
  returns at most one block per stop. It cannot certify Goal or ticket completion.

| Order | Check | How | Blocks when |
| --- | --- | --- | --- |
| 1 | Length | Deterministic ([`farplane_response.py`](../../bin/core/farplane_response.py)) | Prose is over the word or line limit |
| 2 | Continuation | Jev `nudge` score ([`continuation.py`](../continuation/continuation.py)) | Score ≥ 0.5 and fewer than three continuation nudges this user turn |
| 3 | Response format | Jev `shape`, `gap::<section>` and `visible_feature` scores, the Haiku reader check ([`reader_check.py`](../shared/reader_check.py)), and fixed rules ([`response_format.py`](../shared/response_format.py)) | The reader says the answer misses the user, a gap of the chosen shape scores ≥ 0.6, a file is named by a relative path, a new feature has no video, or a completed change that edited files cites nothing |

Continuation and format share one Jev request. Format nudges at most once per
real user turn and names at most two additions. Format still runs after the
continuation cap is spent.

## Response format

Jev classifies the final answer as one of the shapes in the global contract's
Output Formatting templates (simple answer, proposed change, completed change,
blocked, decision needed, progress), then scores only that shape's missing
sections. A plan is never asked for `Verified:`, and an explanation is never
asked for Before/After.

A long turn (10+ minutes since the user's message, or 15+ tool calls) must
open with one `**Context:** You asked …; I …` sentence, so a user returning
hours later knows what the thread was doing. It is fixed, not scored, and a
Context line of 30 words or fewer is outside the length budget.

Before/After is a fixed rule, not a score: any answer of 40 words or more
that reports edited files, or proposes a change, must carry `Before:` and
`After:` (or `Now:`) labels, as lines or table columns. It outranks the
Goal/Track/Progress ask.

Every shape also gets the reader check. Claude Haiku 5.5 (OpenRouter,
`FARPLANE_READER_MODEL`) reads the user's latest message and the whole answer,
not the 2,400-character cut Jev sees, and returns three facts plus a list of
unexplained internal names. Fixed rules turn them into at most one gap:

- `answers_latest` false → `unanswered`: "answer what you can now, then say
  what you are waiting for". This catches turns that end on a one-line status
  such as "The simulator finished; the runner is fetching them."
- `process_narration` true, or two or more unexplained names (ticket or
  session codes, commit hashes, branches, internal tools; paths, links and
  commands do not count), with `status_first` false → `cold_read`: lead with
  the overall state in plain words.
- Two or more unexplained names with the status first → `plain_names`: say
  what each is in a few words, or drop it. One name alone passes, because
  Haiku over-reports single names.

The reader runs beside the Jev request with a 2.5-second timeout. A timeout,
missing key or bad reply skips it and logs `"reader": "unavailable"`.

Every shape also gets one deterministic check: a relative file link or a
backticked relative path with an extension (`docs/plan.md`) gets
`absolute_paths`. `./run.sh` and `../x` read as commands and pass.

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
`apply_patch` calls this user turn. A format nudge names at most two additions.
After one, the gate asks again only when new tool work has happened since (a
plain rewrite does not count), up to three format nudges a user turn. Proof
keeps its own nudge: when no earlier format nudge asked for proof, the gate
asks once more for the proof or video only.

Short `Verified:`, `Unverified:`, `Limit:`, `Grounding:` and `Context:` lines (at most 30
words) are outside the length budget, so adding proof does not re-trigger the
length check.

## Install and control

Registration lives only in [`hooks/hooks.json`](../hooks.json). Run
`farplane hooks install` (Codex) or `install.sh --runtime claude` (Claude Code),
then review/trust the changed command in Codex `/hooks`.

`FARPLANE_STOP_CHECKS` selects checks (default `length,continuation,format`);
unknown names are ignored. Provider settings and credential scope are shared with
continuation: missing credentials, provider errors and unknown transcript
provenance allow the stop silently. Every thread is checked: one another session started (its prompt is an SDK
turn) and a scheduled task's run count as the user's turn. A stop whose last
block is a tool call (the desktop wrap_up) is judged on the turn's last text.

Every decision, allows included, is appended to
`~/.farplane/state/stop-gate/decisions.jsonl` (metadata only: status, shape,
gaps, scores, reader facts, word count, milliseconds; never answer text). It
rotates at 5 MB. Read it to see what the gate let through:

```sh
jq -c '{at,status,gaps,reader,ms}' ~/.farplane/state/stop-gate/decisions.jsonl | tail
```

## Checks

```sh
python3 -m unittest bin/tests/test_stop_gate.py
farplane run -- python3 hooks/stop-gate/sanity_check.py
```

The live check runs [`eval_cases.json`](eval_cases.json) through the configured
provider and the reader model. It passes only with zero format nudges on clean
answers and at least 80% of known gaps caught.
