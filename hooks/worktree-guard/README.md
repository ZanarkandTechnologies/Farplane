# Worktree guard

- **Event:** `PreToolUse` on `Bash` and the app's `start_session`.
- **Entrypoint:** `worktree_guard.sh` (plain sh; a call without "worktree" spawns nothing).
- **Purpose:** Kenji's rule is "only create a worktree when I specify". In the week of
  22-29 Oct 2026 threads ran `git worktree add` 196 times and started 55 sessions with
  `use_worktree: true`; the Oures checkout held 48 worktrees. A written rule did not stop
  it, because three copies of the Oures rulebook disagreed and older ones say "branch in a
  worktree". This guard denies the call and says what to do instead.
- **Override:** `FARPLANE_WORKTREE_OK=1 git worktree add ...` when Kenji asked in his own
  words (or, in Oures, for a Chairhorse task); the reply quotes him.

## Checks

```sh
python3 -m unittest bin/tests/test_worktree_guard.py
```
