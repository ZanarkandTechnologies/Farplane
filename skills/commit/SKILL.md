---
name: commit
version: 0.5.0
description: "Turn a requested worktree change into one isolated commit and, when asked to push, publish it straight to main."
tier: 2
source: local
capability:
  kind: shortcut
template_uses:
  skill-template: "0.6.2"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Glob, Grep, Bash
---

# Commit

## Context

Use this shortcut when the operator asks to commit or publish a change. Resolve
what “this change” means from the current task, isolate that boundary from the
worktree, create one local commit, and verify it. When the operator asks to
push or publish, push `main` straight to `origin/main`. Open a PR only when the
operator asks for one.

## Skill Signature

```text
commit(change, subject?, push?, pr?) -> commit_receipt | push_receipt | pr_receipt | boundary_blocker
reads: current task, worktree, index, requested diff, and recent commit style
does: isolates and stages the requested change, then creates one local commit
writes: Git index, one local commit, optional merge commit and push to main, or a requested PR
returns: commit SHA, subject, committed paths, preservation proof, and pushed range or PR URL
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Resolve the requested commit boundary.**
  `change + task context + worktree -> owned paths/hunks | boundary_blocker`

  Rule: Treat “commit this change” as the change completed in the current task.
  Inspect status and diffs, including untracked files. Use whole files when they
  are fully owned by the request and individual hunks when a file mixes work.

  Assert:
  - Every selected path or hunk supports the requested change.
  - Unrelated changes are excluded without asking the operator to stage them.

- [ ] **N2 — Build an isolated index boundary.**
  `owned paths/hunks + current index -> requested staged diff | conflict`

  Rule: Call `scripts/commit_staged.py` with explicit `--path` inputs for owned
  files and `--cached-patch` for selected hunks. The helper builds a temporary
  index from HEAD, commits it, then aligns only committed paths in the real
  index. If ownership cannot be separated into those inputs, stop first.

  Example: `new skill package + one generated registry row + other registry
  edits -> stage the package and only that row`.

  Assert:
  - The isolated temporary-index diff contains the requested boundary only.
  - No broad pathspec, repository-wide add, or interactive operator step is used.

- [ ] **N3 — Create one honest local commit.**
  `requested staged diff + repo history -> local commit | commit_failure`

  Rule: Choose a compact `type(scope): lower-case imperative summary` and pass it
  to the isolation helper. Never amend, rebase, or rewrite pushed history.

  Assert:
  - The commit subject describes the main behavior change.
  - HEAD advances by exactly one commit.

- [ ] **N4 — Verify the commit and preserved work.**
  `commit + pre-commit snapshots -> commit_receipt | verification_failure`

  Rule: Compare the committed paths and diff with the resolved boundary. Confirm
  unrelated staged and unstaged changes still exist in their original state.

  Assert:
  - The requested change is committed and the requested portion left the index.
  - Unrelated work remains uncommitted; the receipt reports any residual risk.
- [ ] **N5 — Push to main when asked.**
  `verified commit + push request -> origin/main == HEAD | blocker`

  Rule: Load [push to main](references/push-main.md). Fetch, integrate a
  moved `origin/main` with one merge commit, check the outgoing range (scan it
  for secrets and private data on a public repo), then `git push origin main`.
  Use [single-worktree PR publication](references/single-worktree-pr.md) only
  when the operator asks for a PR.

  Assert:
  - `origin/main` equals local `HEAD` after the push; no force, no rebase.
  - Local branch and unrelated staged and unstaged work remain unchanged.
  - The receipt names every commit the push published.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Never use `git add .`, `git add -A`, or a broad directory when it could capture
  unrelated work.
- A generated registry can mix many changes. Stage only the row owned by the
  requested skill instead of committing the whole generated file.
- If ownership cannot be separated safely at hunk level, return the exact
  conflict. Do not commit a mixed boundary to avoid asking a question.
- `git merge` refuses while other threads have staged work; build the merge
  commit with `merge-tree` instead of unstaging their work.
- A push publishes every local commit ahead of `origin/main`, not only this one.

## References

- [commit message style](references/style.md)
- [push to main](references/push-main.md)
- [single-worktree PR publication](references/single-worktree-pr.md)

## Output

```yaml
status: committed | boundary_blocker
subject: <commit subject when committed>
commit: <HEAD SHA when committed>
paths: [<committed path>]
unrelated_work: preserved | <specific verification gap>
push: not_requested | main | remote_branch_created
pr: not_requested | <url>
```
