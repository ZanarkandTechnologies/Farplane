# Todos

- [ ] Confirm `coderabbit --version` works in the repo.
- [ ] Confirm auth status with `coderabbit auth status --agent` or
  `coderabbit auth status`.
- [ ] Choose the stage: `pre-commit`, `pre-push`, `pr`, or direct agent review.
- [ ] Prefer `pre-push` or `pr` for the heavy default path.
- [ ] Use the repo runner for shell or git-hook entrypoints.
- [ ] Use raw `coderabbit review --agent` when Codex should read and fix the
  findings.
- [ ] Summarize Critical, Warning, and Info findings.
- [ ] Decide whether to fix now, rerun, or defer explicitly.
- [ ] Do not treat this as a Stop-hook default.
