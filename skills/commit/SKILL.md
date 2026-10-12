---
name: commit
version: 0.7.1
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
share one checkout on `main` with no branches, so a commit names this thread's
files and leaves every other thread's changes unstaged for their owner. A file
this thread and another both edited is committed whole, with the other
thread's edit labelled in the body; never wait on or unstage another thread.
Never sweep the checkout with `git add -A`, `git add .` or `git commit -a`.
When the operator asks to push, push `main` straight to `origin/main`.
Open a PR only when the operator asks for one; watching an open PR's checks
and review comments is the PR-branch-only [PR watch](references/pr-review-watch.md).

## Skill Signature

```text
commit(change, subject?, push?, pr?) -> commit_receipt | push_receipt | pr_receipt | blocker
reads: current task, git status and diffs (untracked included), recent commit style
does: stages this thread's named paths, then creates one local commit
writes: Git index, one local commit, optional merge commit and push to main, or a requested PR
returns: commit SHA, subject, this thread's paths, labelled shared files, other threads' changes left unstaged, gate warnings, pushed range or PR URL
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Sort the change set by owner.**
  `git status + diffs + task context -> this thread's paths + other paths`

  Rule: List every changed, deleted and untracked path. Mark the ones this
  task changed; everything else belongs to other threads, possibly unfinished,
  and stays out of the commit. Flag outliers before committing: when this
  thread's own set is larger than the task explains (dozens of files, or
  folders the task never touched), stop and name it to the operator instead of
  committing. `.gitignore` keeps `.farplane/`, `.env*` and other private files out.

  Assert:
  - Every changed path appears in exactly one group.
  - Every path in this thread's group is explained by the task.
  - No ignored or secret-bearing file is about to be staged.

- [ ] **N2 — Stage the named paths and commit once.**
  `this thread's paths -> one local commit | commit_failure`

  Rule: `git add -- <path>...` for this thread's paths (deletions included),
  then check `git diff --cached --name-only` lists exactly that set before
  committing with a compact `type(scope): lower-case imperative summary`.
  When the index already holds another thread's staged paths, leave them
  staged and commit with a pathspec, `git commit -- <this thread's paths>`, so
  only this thread's paths land.
  When a staged file also carries another thread's edit, add a body line
  `Also includes (other threads, may be in progress): <file>: <what>`. When the
  gate prints warnings, name them in the body too. Never amend, rebase, or
  rewrite pushed history.

  Example: this thread changed `hooks/stop-gate/stop_gate.py` and its test;
  another thread is deleting `skills/x-account/`. Stage the two stop-gate
  files only: `fix(hooks): stop gate skips nudges when blocked`. The
  `skills/x-account/` deletions stay unstaged and are named in the receipt.

  Assert:
  - The staged set equals this thread's paths; other threads' files are still unstaged.
  - HEAD advances by exactly one commit; the subject describes this thread's change.

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
- `git add -A` once pushed about 600 of another thread's in-progress files
  under one unrelated subject (12 Oct 2026). The staged-set check in N2 exists
  to catch exactly that.
- Quality checks in the git gate warn instead of blocking, because another
  thread's half-done work in the shared tree would otherwise block every commit. The large-file
  guard and the pre-push secret scan still block.
- A push publishes every local commit ahead of `origin/main`, not only this one.

## References

- [commit message style](references/style.md)
- [push to main](references/push-main.md)
- [PR publication](references/single-worktree-pr.md)
- [PR review watch](references/pr-review-watch.md) - PR branches only:
  classify, fix actionable comments, one visible heartbeat per wait.

## Output

Always end with this receipt; `this_thread` lists every path in the commit,
and `left_unstaged` names what other threads' work stayed out.

```yaml
status: committed | blocker
subject: <commit subject when committed>
commit: <HEAD SHA when committed>
this_thread: [<path>]
shared_files: [<path: other thread's edit included>]
left_unstaged: <count> paths from other threads (<top folders>)
gate_warnings: [<check name>]
push: not_requested | main (merged origin/main: yes | no) | remote_branch_created
scan: not_pushed | clean | <hits that stopped the push>
pr: not_requested | <url> | not_opened: <exact gh command to open it>
```
