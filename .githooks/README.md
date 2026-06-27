# Farplane Git Hooks

This directory is active when the repository has:

```bash
git config core.hooksPath .githooks
```

The hook shims call `bin/validators/run_git_gate.py`, and
`rules/git-review-gates.toml` owns which checks run at each boundary.

- `pre-commit`: fast staged-file checks.
- `pre-push`: branch-level deterministic checks. Use Farplane reviewer agents
  for material review instead of external CLI review hooks.
