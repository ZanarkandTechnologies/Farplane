# Fixture PR Review Pipeline

```json
{
  "pr_review_pipeline": {
    "providers": ["github", "reviewer-agent"],
    "poll_interval_minutes": 10,
    "max_iterations": 3,
    "pass_conditions": {
      "require_checks_pass": true,
      "require_no_actionable_comments": true,
      "require_approval": true
    },
    "fix_commands": ["python3 -m pytest"],
    "review_commands": ["reviewer-agent material-review"],
    "notification_policy": {
      "telegram": true,
      "terminal_states": ["pass", "blocked", "timeout"]
    }
  }
}
```
