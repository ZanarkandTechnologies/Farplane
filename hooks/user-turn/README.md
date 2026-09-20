# User turn

- **Event:** `UserPromptSubmit` (30-second timeout).
- **Entrypoint:** `capture_user_turn.py`.
- **Purpose:** Normalize current user intent, capture local conversation windows,
  emit lightweight intent telemetry, and optionally suggest one entry skill.

## Install and control

Registration lives only in [root `hooks.json`](../../hooks.json). From the primary
Farplane checkout, run `farplane hooks install`, then review/trust changed commands
in Codex `/hooks`. Use that control to enable or disable this handler.
`farplane hooks list` displays the configured command; `farplane hooks doctor`
checks its installed target. The installer links this entire folder under
`~/.codex/hooks/`, including this README.

## Configuration and failure behavior

The adapter delegates persistence and classification to
[`bin/runtime/user_turn.py`](../../bin/runtime/user_turn.py). Internal injected
prompts, empty/invalid input, other events, and requests without a resolved project
are ignored. It does not mark tickets complete or invoke suggested skills.

Jev entry-skill suggestion is off unless `FARPLANE_JEV_SKILL_SUGGESTION=1`.
Explicit skill mentions bypass the suggestion. Provider setup, privacy boundaries,
and the two-pass selection contract are documented in the
[runtime guide](../../docs/farplane-framework/hooks-and-runtime.md#optional-jev-entry-skill-suggestion).
Missing setup, provider failure, and low-confidence suggestions emit no advice;
this does not disable normal local turn capture. When enabled, the current prompt
and bounded skill context go to the provider. Keep API keys outside tracked config.

## Checks

Run from the repository root:

```sh
python3 -m unittest discover -s bin/tests -p 'test_capture_user_turn.py'
```
