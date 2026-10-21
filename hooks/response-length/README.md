# Response length

- **Event:** `Stop` (five-second timeout).
- **Entrypoint:** `final_response_gate.py`.
- **Purpose:** Request a rewrite when the proposed final answer exceeds its prose
  word or nonblank-line ceiling. It never truncates text or edits artifacts.

Blocking feedback uses a level-four Markdown heading plus labeled bullets for
the limit, content to keep/remove, exclusions, and required return shape.

## Install and control

Registration lives only in [`hooks/hooks.json`](../hooks.json). From the primary
Farplane checkout, run `farplane hooks install`, then review/trust changed commands
in Codex `/hooks`. Use that control to enable or disable this handler.
`farplane hooks list` displays the configured command; `farplane hooks doctor`
checks its installed target. The installer links this entire folder under
`~/.codex/hooks/`, including this README.

## Configuration and failure behavior

Defaults are 500 prose words and 50 nonblank prose lines. Override with
`FARPLANE_FINAL_RESPONSE_MAX_PROSE_WORDS` and
`FARPLANE_FINAL_RESPONSE_MAX_PROSE_LINES` using Farplane runtime configuration.
Invalid/nonpositive settings use defaults. Missing, malformed, irrelevant, or
empty hook input produces no feedback. Each nudge asks for about 90% of the
word cap so one rewrite clears it. The Stop gate stops length nudges after two
in one user turn; the answer then stands as it is. No network requests.

Tables, closed fenced blocks (Mermaid, wireframe, ASCII diagrams, code), exact
media embed lines, marker-only blockquote spacers, labelled lines (`Before:`,
`After:`, `Example:`, `Context:`, `Verified:`, `Unverified:`, `Limit:`,
`Grounding:`) of at most 40 words, and a final link-only References/Citations
section are outside the prose budget. A 1,200-word ceiling on the whole answer
stops prose hiding in tables or blocks. These are counted by the shared
[`response accountant`](../../bin/core/farplane_response.py). Inspect a draft with
`farplane response check --stdin --json`.

## Checks

```sh
python3 -m unittest discover -s bin/tests -p 'test_final_response_gate.py'
```

Run from the repository root. Tests cover limits, exclusions, and rewrite feedback.
