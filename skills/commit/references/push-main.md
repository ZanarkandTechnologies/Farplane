# Push To Main

The default publish route: push the shared checkout's `main` straight to
`origin/main`. Open a PR only when the operator asks for one
([PR publication](single-worktree-pr.md)).

## Preconditions

- The checkout is on `main`; do not create or switch a local branch.
- The change is committed with the commit skill: everything staged, other
  threads' work labelled in the body.

## Integrate

```bash
git fetch origin main
git rev-list --left-right --count origin/main...HEAD   # behind ahead
```

When `origin/main` has commits that local `main` lacks, merge them; never rebase
or force-push.

```bash
git add -A && git commit -m "chore: checkpoint other threads' work before merge"   # only if the tree changed since your commit
git merge --no-edit origin/main
```

On a merge conflict, stop and report the conflicting paths.

## Check the outgoing range

`git log --oneline origin/main..HEAD` lists everything the push publishes; name
each commit in the receipt. For a public repository, scan the outgoing diff
before pushing:

- secrets: API keys and tokens (`sk-`, `ghp_`, `github_pat_`, `xox?-`, `AKIA`),
  private keys, JWTs, credential assignments, `.env`/key files;
- private business data: emails, phone numbers, client names, money figures,
  private Notion or Convex links, personal plan contents.

Stop and report any hit instead of pushing.

## Push

```bash
git push origin main
git fetch origin main
git rev-list --left-right --count origin/main...HEAD   # expect 0 0
```

A rejected push means `origin/main` moved: integrate again and retry. Never pass
`--force`.
