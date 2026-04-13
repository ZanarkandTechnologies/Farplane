# Hook Recipes

These hooks are examples only. They are not auto-installed by this repo.

## Pre-push

Use when you want CodeRabbit as a manual quality gate before publishing a
branch:

```bash
cp skills/coderabbit-review/scripts/pre-push.sample .git/hooks/pre-push
chmod +x .git/hooks/pre-push
```

The sample hook calls the repo-local runner in `pre-push` mode. Set
`CODEXTER_SKIP_CODERABBIT=1` to bypass one push intentionally.

## Pre-commit

Use only when you explicitly want a heavy local review before commit:

```bash
cp skills/coderabbit-review/scripts/pre-commit.sample .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

This is intentionally secondary to `pre-push`. If it becomes annoying, remove
it and keep the `pre-push` gate only.

## What Not To Do

- Do not wire these scripts into `hooks.json`.
- Do not treat CodeRabbit as the only review signal.
- Do not auto-install these hooks in the repo without an explicit user request.
