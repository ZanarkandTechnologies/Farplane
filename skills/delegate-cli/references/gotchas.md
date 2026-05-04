# Delegate CLI Gotchas

- A successful external CLI exit code is not Codexter completion.
- Do not document future adapters as shipped profiles.
- Do not store API keys in profile templates or generated prompt files.
- Do not run live paid models when `--dry-run` proves enough for the ticket.
- Prefer worktree mode when another live writer may touch the same checkout;
  dry-run records the intended path, while live runs create the worktree.
