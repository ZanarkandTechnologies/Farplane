---
name: commit
version: 0.6.0
description: "Use for \"commit this\", \"push it\" or \"watch this PR\": one labelled commit on main, a push straight to main when asked, or a bounded watch on an open PR."
department: delivery
source: local
capability:
  kind: shortcut
template_uses:
  skill-template: "0.6.5"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Glob, Grep, Bash
---

# Commit

## Context

Use this shortcut when the operator asks to commit or publish a change. Threads
share one checkout on `main` with no branches, so a commit takes everything that
has changed, not only this thread's files. The subject names this thread's
change; the body labels what other threads left in progress. Imperfect history
is the accepted price of never waiting on, merging with, or unstaging another
thread. When the operator asks to push, push `main` straight to `origin/main`.
Open a PR only when the operator asks for one; watching an open PR's checks
and review comments is the PR-branch-only [PR watch](references/pr-review-watch.md).

## Skill Signature

```text
commit(change, subject?, push?, pr?) -> commit_receipt | push_receipt | pr_receipt | blocker
reads: current task, git status and diffs (untracked included), recent commit style
does: stages every change, then creates one local commit labelled by owner
writes: Git index, one local commit, optional merge commit and push to main, or a requested PR
returns: commit SHA, subject, this thread's paths, other included paths, gate warnings, pushed range or PR URL
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Sort the change set by owner.**
  `git status + diffs + task context -> this thread's paths + other paths`

  Rule: List every changed, deleted and untracked path. Mark the ones this
  task changed; everything else belongs to other threads, possibly unfinished.
  `.gitignore` keeps `.farplane/`, `.env*` and other private files out.

  Assert:
  - Every changed path appears in exactly one group.
  - No ignored or secret-bearing file is about to be staged.

- [ ] **N2 — Stage everything and commit once.**
  `all changes -> one local commit | commit_failure`

  Rule: `git add -A`, then commit with a compact `type(scope): lower-case
  imperative summary` for this thread's change. Add an `Also includes:` body
  line naming the other threads' paths or work, marked "may be in progress".
  When the gate prints warnings, name them in the body too. Never amend,
  rebase, or rewrite pushed history.

  Example: `fix(hooks): stop gate skips nudges when blocked` with body
  `Also includes (other threads, may be in progress): skills/x-account/ removal.`

  Assert:
  - HEAD advances by exactly one commit and the index matches HEAD.
  - The subject describes this thread's change; the body names everything else.

- [ ] **N3 — Push to main when asked.**
  `commit + push request -> origin/main == HEAD | blocker`

  Rule: Load [push to main](references/push-main.md). Fetch, merge a moved
  `origin/main`, scan the outgoing range for secrets and private data on a
  public repo, then `git push origin main`. Use
  [PR publication](references/single-worktree-pr.md) only when the operator
  asks for a PR.

  Assert:
  - `origin/main` equals local `HEAD` after the push; no force, no rebase.
  - The receipt names every commit the push published.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Another thread may still be editing a file you commit. That's expected: its
  next commit finishes the change. Label it; don't wait for it.
- Quality checks in the git gate warn instead of blocking, because another
  thread's half-done work would otherwise block every commit. The large-file
  guard and the pre-push secret scan still block.
- A push publishes every local commit ahead of `origin/main`, not only this one.

## References

- [commit message style](references/style.md)
- [push to main](references/push-main.md)
- [PR publication](references/single-worktree-pr.md)
- [PR review watch](references/pr-review-watch.md) - PR branches only:
  classify, fix actionable comments, one visible heartbeat per wait.

## Output

```yaml
status: committed | blocker
subject: <commit subject when committed>
commit: <HEAD SHA when committed>
this_thread: [<path>]
also_included: [<path or work, other threads>]
gate_warnings: [<check name>]
push: not_requested | main | remote_branch_created
pr: not_requested | <url>
```
