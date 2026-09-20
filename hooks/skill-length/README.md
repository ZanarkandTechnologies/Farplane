# Skill length

- **Event:** `PostToolUse`, matched to `apply_patch`, `Edit`, or `Write`.
- **Entrypoint:** `skill_file_line_gate.py` (five-second timeout).
- **Purpose:** Return repair feedback for edited repository `skills/**/SKILL.md`
  files exceeding 200 physical lines. The edit remains applied.

## Install and control

Registration lives only in [root `hooks.json`](../../hooks.json). From the primary
Farplane checkout, run `farplane hooks install`, then review/trust changed commands
in Codex `/hooks`. Use that control to enable or disable this handler.
`farplane hooks list` displays the configured command; `farplane hooks doctor`
checks its installed target. The installer links this entire folder under
`~/.codex/hooks/`, including this README.

## Scope and failure behavior

The current parser requires `tool_input.command` containing apply-patch path
markers; the event matcher alone does not make arbitrary Edit/Write payloads
inspectable. Only existing destination paths inside the resolved repository's
`skills/` tree are checked. Unrelated files, missing command fields, malformed
JSON, and other events produce no feedback. There is no network call, file
rewrite, or configurable runtime line limit. Repository pre-commit checks provide
the hard backstop for the same 200-line invariant.

When feedback is returned, the model must repair the source while preserving
its behavior. Conditional details may move behind precise references; this hook
does not own that refactoring.

## Checks

Run from the repository root:

```sh
python3 -m unittest discover -s bin/tests -p 'test_skill_file_line_gate.py'
```
