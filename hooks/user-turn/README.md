# User turn

- **Event:** `UserPromptSubmit` (30-second timeout).
- **Entrypoint:** `capture_user_turn.py`.
- **Purpose:** Normalize current user intent, capture local conversation windows,
  emit lightweight intent telemetry, and optionally suggest one entry skill.

## Install and control

Registration lives only in [`hooks/hooks.json`](../hooks.json). From the primary
Farplane checkout, run `farplane hooks install`, then review/trust changed commands
in Codex `/hooks`. Use that control to enable or disable this handler.
`farplane hooks list` displays the configured command; `farplane hooks doctor`
checks its installed target. The installer links this entire folder under
`~/.codex/hooks/`, including this README.

## Configuration and failure behavior

The adapter delegates persistence and classification to
[`bin/core/user_turn.py`](../../bin/core/user_turn.py), which the `farplane` CLI also uses;
`runtime_telemetry.py` here sends the intent event. Each skill the prompt names
goes to the skill stream as `skill_requested` (`hooks/shared/skill_events.py`,
see [skill invocation](../skill-invocation/README.md)); skill heat keeps it
apart from real invocations. Internal injected
prompts, empty/invalid input, other events, and requests without a resolved project
are ignored. It does not mark tickets complete or invoke suggested skills.

Jev entry-skill suggestion is off unless `FARPLANE_JEV_SKILL_SUGGESTION=1`.
Explicit skill mentions bypass the suggestion. The code lives in
[`hooks/shared/skill_suggestion.py`](../shared/skill_suggestion.py). Pass 1 runs
one Choice over the generated skill registry plus three skill-need Noul gates;
pass 2 reranks the top three using descriptions and bounded `SKILL.md` excerpts,
and its fit Nouls may reject all three. A winner is injected as one advisory
`<skill_relevance>` block. The public Jev demo endpoint is not used: its 2k
context cannot hold the registry. Provider setup and privacy boundaries are in
the [runtime guide](../../docs/guides/hooks-and-runtime.md#optional-jev-entry-skill-suggestion).
Missing setup, provider failure, and low-confidence suggestions emit no advice;
this does not disable normal local turn capture. When enabled, the current prompt
and bounded skill context go to the provider. Keep API keys outside tracked config.

## Checks

Run from the repository root:

```sh
python3 -m unittest discover -s bin/tests -p 'test_capture_user_turn.py'
```
