# PR Review Watch Heartbeat

Resume `pr-review-watch` for:

- Repo: `<repo_path>`
- PR: `<pr_number>`
- Iteration: `<iteration>` of `<max_iterations>`
- Config source: `<config_source>`
- Previous verdict artifact: `<verdict_artifact>`
- PR URL: `<pr_url>`

Use the project `pr_review_pipeline` config. Re-run:

```bash
python3 bin/pr_review_watch.py classify --repo <repo_path> --pr <pr_number> --json
```

Then:

1. If `state` is `pass`, send the configured terminal notification with the PR
   URL and stop.
2. If `state` is `blocked`, write the blocker summary, notify when configured,
   include the PR URL, and stop.
3. If `state` is `actionable`, fix only listed actionable items, run configured
   local commands, and classify again.
4. If `state` is `wait`, schedule one more visible heartbeat unless
   `<iteration>` reached `<max_iterations>`.

Do not merge, push, deploy, or create a hidden polling loop.
