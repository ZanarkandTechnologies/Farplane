# PR Review Watch

Load only when the operator names an already-open pull request and asks to
watch it ("watch PR 123 until checks pass", "keep fixing the review comments on
this PR"). It applies to PR branches only; the normal shared checkout pushes
straight to `main` and has no PR to watch.

## Contract

1. Resolve the repo and PR number (`gh pr view` on the current branch when no
   number is given).
2. Read `docs/pr-review-pipeline.md` in the target repo, else its `AGENTS.md`.
   One of them must hold a fenced JSON `pr_review_pipeline` block; copy
   [the pipeline template](../templates/pr-review-pipeline.md) when it is
   missing. No block -> `blocked`, no live polling.
3. Classify:
   `python3 skills/commit/scripts/pr_review_watch.py classify --repo <repo> --pr <n> --json`
   (`--fixture <path> --config <path>` for deterministic checks; fixtures live
   in `fixtures/pr-review-watch/`).
4. Act on the `WatchVerdict`:
   - `pass` -> send the terminal summary with the PR URL and stop.
   - `blocked` -> record the blocker, notify when configured, stop.
   - `actionable` -> fix only the listed items, run only the configured
     `fix_commands` / `review_commands`, then classify again.
   - `wait` -> schedule one visible follow-up with
     [the heartbeat prompt](../templates/codex-automation-prompt.md); honour CI
     timing hints, widen the interval while state is unchanged, reset it when
     checks, comments or approvals change; stop at `max_iterations`.
5. Use `review` or the configured reviewer lane for material review findings;
   never make an external review CLI a universal gate.

## Guardrails

- No daemon, hidden loop, queue runner or always-on watcher; one visible
  heartbeat at a time.
- No merge, deploy, force push or invented provider command unless the
  surrounding workflow authorises it. Pushing fixes to the PR branch follows the
  operator's request.
- Notifications are terminal-state only and best effort (`telegram-message`
  when the pipeline asks for it).
- Unit proof uses fixtures:
  `python3 -m unittest skills/commit/scripts/test_pr_review_watch.py`.

## Return

Repo and PR, config source, snapshot or fixture path, `WatchVerdict` JSON,
commands run, heartbeat scheduled or terminal notice sent (with PR URL), and
blocker details when blocked.
