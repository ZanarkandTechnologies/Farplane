# Stop gate

- **Event:** `Stop` (five-second timeout).
- **Entrypoint:** `stop_gate.py`.
- **Purpose:** The one blocking Stop handler. It runs three checks in order and
  returns at most one block per stop. It cannot certify Goal or ticket completion.

| Order | Check | How | Blocks when |
| --- | --- | --- | --- |
| 1 | Length | Deterministic ([`farplane_response.py`](../../bin/core/farplane_response.py)) | Prose is over the word or line limit |
| 2 | Continuation | Haiku reader's blocker facts, then Jev `nudge` and `proposal` scores ([`continuation.py`](../continuation/continuation.py)) | The answer stops on a blocker the agent can clear itself (not on a plan or decision question), `nudge` ≥ 0.5, or `proposal` ≥ 0.5: it offers a next step it could take itself that adds value to the user's goal and needs nothing from the user; fewer than three continuation nudges this user turn |
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
In every shape, proposed next steps titled by their work ("add caching")
rather than their gain ("rebuilds 35 s faster") get the `proposal_gain` fix.

A long turn (30+ minutes since the user's message) must carry one
`**Context:** You asked …; I …` sentence, so a user coming back an hour later
knows what the thread was doing. The gate cannot see when the user returns, so
the turn's age stands in; a live exchange gets none (the old 15-tool-call
trigger asked for 392 Context lines in that same week). It is fixed, not scored, and a Context line of 40
words or fewer is outside the length budget.

Short answers are a fixed rule too: a simple answer, proposed change,
decision or blocker with more than 250 prose words gets `short_answer` (about
150 words in "80% ASD-STE100", the named plain-English standard). The target
stays 150; the trigger sits at 250 so only clear misses come back. Labelled
lines, tables and fenced blocks don't count. Completed changes and progress
reports keep the 500-word budget.

Before/After is a fixed rule, not a score: a completed change (files edited)
or proposed change of 40 words or more must carry `Before:` and `After:` (or
`Now:`) labels, as lines or table columns. A status update or an answer in a
turn that also edited files is not a change report. It outranks the
Goal/Track/Progress ask.

A format nudge whose gap is structural (missing Before/After, planned proof,
blocker/recovery, decision choice or progress ledger) carries the template for
the chosen shape (the `skeleton` in
[`response_format.py`](../shared/response_format.py)), with the Context line on
long turns. The template sets the order, not the form. Every other gap
(unanswered, cold read, names, paths, proof, Context) is an in-place edit and
carries no template. Every nudge says to keep tables, diagrams, code blocks
and images as they are.

Every shape also gets the reader check. Claude Haiku 5.5 (`claude -p` on the
Claude Code subscription, never a paid key; `FARPLANE_READER_MODEL`) reads the user's latest message, the last 3,000
characters of their earlier messages (names used there count as known), and the whole answer,
not the 2,400-character cut Jev sees, and returns four facts plus a list of
unexplained internal names. Haiku sees only the user's own words of the latest
message (app notices and session reminders removed) and, for a long brief, its
opening and its end. Haiku over-reports, so fixed rules check its claims first:
a bold opening line (after any heading or Context line) counts as the status;
a name the user used, a number, path, flag, link text or issue number, or a
name the answer explains where it appears (`name (…)`, `name: …`, `name, a …`)
is dropped from the unexplained list. Then fixed rules turn them into at most
one gap:

- `answers_latest` false and Jev's `gap::unanswered` ≥ 0.5 → `unanswered`:
  "answer what you can now, then say what you are waiting for". Haiku alone
  called three in four answered replies unanswered; Jev agreeing keeps the
  real misses (a one-line status, or "No response requested.", in reply to a
  question). A turn started by another session's message or
  an app notice (no words of the user's own) never gets `unanswered`. This catches turns that end on a one-line status
  such as "The simulator finished; the runner is fetching them."
- `process_narration` true, or two or more unexplained names (ticket or
  session codes, commit hashes, branches, internal tools; paths, links and
  commands do not count), with `status_first` false → `cold_read`: lead with
  the overall state in plain words.
- Two or more unexplained names with the status first → `plain_names`: say
  what each is in a few words, or drop it. One name alone passes, because
  Haiku over-reports single names.
- `name_drift` true (one thing called by two or more names, "matcher" then
  "retriever") with no earlier reader gap → `one_name`: keep one name per thing.

The reader runs beside the Jev request with a 4-second timeout (about 1 s in
practice). It runs `claude -p` with no tools, settings, MCP or hooks, and with
`ANTHROPIC_API_KEY` removed, so it bills the subscription. A timeout, missing
`claude` binary or bad reply skips it and logs `"reader": "unavailable"`.
Jev itself goes straight to TypeSafe (`TYPESAFE_API_KEY`), not OpenRouter.
When the subscription limit is spent the reader fails open; it never falls back
to a paid key.

The reader also names the blocker the answer stops on and says whether the
agent could clear it now with its own tools (rerun, start a server, install,
read a log, retry, fix a small bug). If so, and the answer is not a plan or a
decision question, the gate sends the fixed "fix the blocker" continuation
nudge. Anything needing the user (password, login, approval, payment, a
decision) or waiting on another session or job does not count.

Every shape also gets one deterministic check: a relative file link or a
backticked relative path with an extension (`docs/plan.md`) gets
`absolute_paths`. `./run.sh` and `../x` read as commands and pass.

Proof is deterministic once Jev has said whether the turn added a new feature
or multi-step workflow a person would watch (`visible_feature` ≥ 0.6: a screen,
UI flow, interactive page, game, an app's agents or workers acting differently,
or robot or simulation behaviour). Jev judges what the user would see, so launch
code that changes how bunker workers behave counts.

- **New feature** (completed change or a run's last progress update, files
  edited), only while the [evidence switch](../evidence-mode/README.md) is
  asleep: needs an embedded or linked `.mp4`, `.mov` or `.webm`, or an
  `Unverified:` line saying why there is no video. Screenshots and links alone
  get one nudge to record it.
- **Anything else** (completed change, files edited): any citation means the
  agent did not forget: a media embed, a Markdown link, a URL, a fenced block
  (command output), or a `Verified:`/`Unverified:` label. Citing nothing gets
  one nudge to cite its proof or state `Unverified:` and why.

Edits are Claude `Edit`/`Write`/`MultiEdit`/`NotebookEdit` or Codex
`apply_patch` calls this user turn. A format nudge names at most two additions.
One format nudge per user turn, even after more tool work. Proof
keeps its own nudge: when no earlier format nudge asked for proof, the gate
asks once more for the proof or video only.

Everything the format check asks for is outside the length budget: labelled
`Before:`, `After:`, `Example:`, `Context:`, `Verified:`, `Unverified:`,
`Limit:` and `Grounding:` lines (at most 40 words), and tables and fenced
blocks. So a format nudge never re-triggers the length check, and length nudges
stop after two per user turn.

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
