# PR Review Watch Maintenance

Keep this skill explicit, bounded, and project-config driven.

## Rules

- Do not turn the watcher into a daemon, queue runner, hidden scheduler, or
  always-on policy.
- Keep live provider behavior optional; unit tests must rely on local fixtures.
- Keep project-specific commands in `docs/pr-review-pipeline.md` or
  `PROJECT_RULES.md`, not in the skill body.
- Use the checkout assigned to the current Codex task and `review` / reviewer
  lanes for material review instead of duplicating those contracts here.

## Checks

```bash
python3 -m unittest skills/pr-review-watch/scripts/test_pr_review_watch.py
python3 skills/skill-maintenance/scripts/check_skills.py --write
```
