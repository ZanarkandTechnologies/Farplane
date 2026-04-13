# Git Hooks

These hooks are optional. `init-project` scaffolds them so each repo has a
clear place for local quality gates, but nothing is enabled automatically.

## Recommended Default

Use `pre-push` for local validators like lint, typecheck, and tests.

Use `pre-commit` only when you explicitly want a smaller fast gate before each
commit.

## Activate

To make this repo use `.githooks/`:

```bash
git config core.hooksPath .githooks
chmod +x .githooks/pre-push
```

If you also want the optional pre-commit hook:

```bash
chmod +x .githooks/pre-commit
```

## Notes

- The sample hooks call repo-local validation scripts first:
  - `scripts/pre_commit_check.sh`
  - `scripts/pre_push_check.sh`
- The `pre-push` hook then tries to run `coderabbit review` directly when the
  CLI is installed on `PATH`.
- Override the review base branch with `CODERABBIT_BASE_BRANCH=<branch>` if the
  repo should not compare against the detected default or `main`.
- Remove or rename the hook files if the project should not use them.
