# PR Review Watch Maintenance

Keep this skill explicit, bounded, and project-config driven.

## Rules

- Do not turn the watcher into a daemon, queue runner, hidden scheduler, or
  always-on policy.
- Keep live provider behavior optional; unit tests must rely on local fixtures.
- Keep project-specific commands in `docs/pr-review-pipeline.md` or
  `PROJECT_RULES.md`, not in the skill body.
- Use `pr-runtime` for checkout isolation and `coderabbit-review` for explicit
  heavy CodeRabbit passes instead of duplicating those contracts here.

## Checks

```bash
python3 bin/test_pr_review_watch.py
python3 skills/skill-maintenance/scripts/check_skills.py --write
```
