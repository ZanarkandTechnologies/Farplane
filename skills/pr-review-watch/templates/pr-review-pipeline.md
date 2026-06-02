# PR Review Pipeline

Copy this file to `docs/pr-review-pipeline.md` in a project that wants explicit
Farplane PR review watching.

The watcher requires this fenced JSON block. Keep commands project-local and
safe to run repeatedly.

`poll_interval_minutes` is the fixed-cadence compatibility field. New projects
should treat it as the maximum normal heartbeat interval and use adaptive
backoff from `docs/specs/adaptive-backoff.md` when a watcher has repeated
unchanged wait states.

```json
{
  "pr_review_pipeline": {
    "providers": ["github"],
    "poll_interval_minutes": 10,
    "max_iterations": 12,
    "pass_conditions": {
      "require_checks_pass": true,
      "require_no_actionable_comments": true,
      "require_approval": false
    },
    "fix_commands": [
      "npm test"
    ],
    "review_commands": [],
    "notification_policy": {
      "telegram": true,
      "terminal_states": ["pass", "blocked", "timeout"]
    }
  }
}
```

## Boundaries

- The watcher may fix actionable review comments and run the configured local
  commands.
- The watcher may schedule one visible Codex heartbeat when the PR is still
  waiting on checks or reviewers.
- The watcher should use adaptive backoff for repeated unchanged wait states
  and honor provider timing hints before local defaults.
- The watcher may send Telegram notifications for terminal states when the
  installed environment supports the `telegram-message` skill.
- The watcher must not push, merge, deploy, change billing/spend, or invent new
  review provider commands without an explicit workflow authorization.
