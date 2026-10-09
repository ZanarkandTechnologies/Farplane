# Push To Main

The default publish route: push the shared checkout's `main` straight to
`origin/main`. Open a PR only when the operator asks for one
([single-worktree PR publication](single-worktree-pr.md)).

## Preconditions

- The checkout is on `main`; do not create or switch a local branch.
- The requested change is already an isolated, verified local commit.
- One writer owns Git state for the push window.

## Integrate

```bash
git fetch origin main
git rev-list --left-right --count origin/main...HEAD   # behind ahead
```

When `origin/main` has commits that local `main` lacks, add one merge commit;
never rebase or force-push.

- Index matches `HEAD`: `git merge --no-edit origin/main`.
- Index holds other threads' staged work (`git merge` refuses): first confirm
  `git diff --name-only HEAD...origin/main` shares no path with
  `git status --porcelain`, then:

```bash
T=$(git merge-tree --write-tree HEAD origin/main)       # fails on conflict: stop
M=$(git commit-tree "$T" -p HEAD -p origin/main -m "Merge remote-tracking branch 'origin/main'")
git update-ref refs/heads/main "$M" <previous HEAD>
git checkout HEAD -- <each incoming path>
```

Confirm `git status --porcelain` is unchanged by the merge.

## Check the outgoing range

`git log --oneline origin/main..HEAD` lists everything the push publishes. Other
threads' earlier local commits ship too; name them in the receipt. For a public
repository, scan the outgoing diff before pushing:

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
