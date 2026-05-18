---
name: loop
description: Use when one bounded same-session task should auto-resume until explicit local completion checks pass or the operator explicitly stops it. Prefer it for short deterministic work, not ticketed multi-lane implementation.
tier: 2
---

# Loop

`$loop` is the lightweight same-session persistence surface.

Use it when:

- one bounded task should keep going in the same session
- completion can be expressed with local deterministic predicates
- ticket orchestration, review lanes, and evidence packets would be overkill

Do not use it when:

- the work needs a ticket plan or approval surface; use `impl-plan`
- the work should run through build, QA, review, and evidence lanes; use `$impl`
- completion depends on fuzzy judgment, non-local state, or broad orchestration

## Contract

- `$loop` is session-owned, not ticket-owned.
- The loop arms only when the prompt includes `$loop` and a completion contract.
- v1 completion checks are local and deterministic only:
  - `completion_marker_seen`
  - `path_exists`
  - `file_contains`
- Explicit stop intent such as `stop loop`, `cancel loop`, `exit loop`, or
  `$loop stop` clears the loop safely.
- Escape/cancel is not the canonical loop-stop contract.

## Invocation Shape

Keep the contract explicit in the prompt. Inline JSON must stay on one line.

```text
$loop fix the auth script and keep trying until the local checks pass
done_when=[{"kind":"path_exists","path":".harness/tmp/auth-fixed.flag"},{"kind":"file_contains","path":"logs/auth.log","text":"AUTH OK"}]
completion_marker=AUTH FIXED
retry_message=Continue fixing auth until the flag exists and the log contains AUTH OK.
```

Minimal marker-only loop:

```text
$loop finish the current bounded cleanup
completion_marker=CLEANUP DONE
retry_message=Continue the cleanup and print CLEANUP DONE only when it is really finished.
```

## Predicate Reference

- `{"kind":"completion_marker_seen","text":"..."}`:
  pass when the assistant message contains the exact text
- `{"kind":"path_exists","path":"relative/or/absolute/path"}`:
  pass when the path exists from the repo root or as an absolute path
- `{"kind":"file_contains","path":"relative/or/absolute/path","text":"..."}`:
  pass when the file exists and contains the text

`completion_marker=...` is shorthand for adding a
`completion_marker_seen` predicate.

## Guardrails

- Keep the task bounded and reversible.
- Prefer concrete local checks over vague “done enough” language.
- Use one retry message that tells the same session exactly what to continue.
- If the work grows into ticketed implementation, stop the loop and hand off to
  `impl-plan` or `$impl`.
- Do not assume tmux helpers, ticket claims, or worker lanes are part of
  `$loop` v1.
