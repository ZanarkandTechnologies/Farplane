---
name: token-burn
description: "Turn leftover weekly Claude plan usage near reset into parallel revive, triage, and backlog work with local-only commits and one dated report."
tier: 3
department: operations
source: local
template_uses:
  skill-template: "0.6.3"
allowed-tools: Read, Write, Glob, Grep, Bash, Agent, mcp__ccd_session_mgmt__get_usage
---

# Token Burn

## Context

Use this skill when a subscription's weekly usage would reset with a large
share unused, usually from the "Burn before reset" scheduled task, or manually
with `force`. It gates on the plan limits the host reports, then spends the
remainder on bounded jobs that leave reviewable local commits and one report.
Backlog lines are not Farplane tickets: this skill never creates, claims, or
comments on issues, and `pulse-update` keeps ticket execution. It does not own
scheduling, pushing, deploys, or account pooling.

## Skill Signature

```text
token_burn(workspace_root, owners[], backlog_path?, force?) -> burn_report | skip_line | blocked
reads: get_usage plan windows, backlog_path, git state of listed repos, gh repo data for owners[]
does: gates on expiring weekly usage, runs disjoint jobs, and records results as they land
writes: local commits in clean listed repos, backlog ticks, <workspace_root>/reports/<date>[-n].md
returns: skip or blocked line with readings, or report path plus commits made
```

Defaults: `backlog_path` is `<workspace_root>/backlog.md`; `force` is false.
Backlog lines use `- [ ] path:<absolute repo path> — <problem>`.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Gate on the window that would expire unused.**
  `get_usage plan -> burn | skip(readings) | blocked(status)`

  Rule: The binding window is whichever has less left of `Weekly · all models`
  and the weekly window for the model this session runs on, when listed. Burn
  when the binding window resets in <= 30h (from `resetsAt`) with >= 20% left.
  Skip when the 5-hour window is already >= 90% used. `force` bypasses only the
  reset and leftover tests. Status `not_applicable` or `unavailable` returns
  `blocked`, never a burn.

  Example: `Fable weekly 0% used, all models 99% used, running on Fable ->
  binding = all models (1% left) -> skip`; `all models 59% used, resets in 8h
  -> burn`.

  Assert:
  - A skip or blocked result changes nothing and lists each weekly window.
  - The before-readings and binding window are frozen for the report.

- [ ] **N2 — Plan disjoint jobs and open the report.**
  `burn + backlog -> job list + report skeleton | revive+triage only`

  Rule: Always plan Revive and Triage (report-only). Plan one Backlog lane per
  repo path with open lines, at most 4, in file order. A lane is eligible only
  if the path exists, is a git checkout, and `git status --porcelain` is empty;
  otherwise record it as `needs owner: <reason>` and never clone or clean it.
  A repo with an active Pulse worker claim (see `tickets/README.md`) is also
  `needs owner`.
  Write the report skeleton now (readings, binding window, planned jobs);
  if today's report exists, use `<date>-2.md`, `-3`, and so on.

  Assert:
  - Each repo has at most one lane; dirty, missing, or non-git paths get none.
  - An empty backlog plans no lane and invents no work.

- [ ] **N3 — Dispatch one item per subagent, in parallel across lanes.**
  `job list -> per-item subagent summaries`

  Rule: Run Revive and Triage as one subagent each. For each lane, dispatch
  its items one subagent at a time; lanes run in parallel. Give every subagent
  its job text plus these rules verbatim: work in the given checkout on its
  current branch, never a new worktree or branch; verify with the repo's tests
  or the smallest real check before committing, and commit nothing unverified;
  stage only files this item changed; commit locally only; never push, deploy,
  publish, message, spend, edit `backlog.md`, or touch credentials or settings;
  return what changed, proof, commit hash, what is left, and what needs the
  owner.

  Jobs:
  - **Revive** — for each of `owners[]`, scan `gh repo list <owner> --limit 200`
    plus unfinished local work; rank the top 5 worth another pass now with last
    activity, what is done, what is missing, and why now. Report only.
  - **Triage** — for repos active in the last 60 days, list open PRs, issues,
    and unmerged branches with a merge, finish, or kill call each. Report only.
  - **Backlog item** — treat the line as a problem, not a spec; build the
    simplest fix, verify it, and commit it.

  Assert:
  - Report-only jobs leave every repo unchanged.
  - Every commit cites its verification.

- [ ] **N4 — Re-check usage before each dispatch.**
  `fresh get_usage -> dispatch next item | stop starting work`

  Rule: Before every dispatch, re-read usage. Stop starting work when the
  binding window falls below 15% left while its reset is more than 12h away,
  or below 5% otherwise, or when the 5-hour window is >= 90% used. Running
  items finish their current commit. Before each lane dispatch, re-run
  `git status --porcelain` and `git symbolic-ref -q HEAD`; a dirty tree or
  detached HEAD stops that lane as `needs owner`. An abandoned item restores
  only the files it changed.

  Assert:
  - The report names the reading or repo state that stopped work, if any.
  - No commit lands on a tree that was dirty before its item started.

- [ ] **N5 — Record results as they land, then reply.**
  `summaries + readings -> report + backlog ticks + reply`

  Rule: Append each subagent's summary to the report as it returns, so a dead
  run still shows its commits. The parent alone ticks finished backlog lines,
  appending the short hash. Finish with after-readings, every commit as
  `repo path @ hash`, unverified or abandoned items with reasons, and what
  needs the owner. Reply with a short digest pointing at the report.

  Assert:
  - Commits listed in the report exist in `git log` of the named repo.
  - Only the parent wrote `backlog.md`.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Treating the 5-hour window as leftover usage burns on every run and drains
  the next day; only weekly windows near reset count.
- Burning because the Fable window is empty while all-models is nearly spent
  stalls the first dispatch; gate on the binding window.
- Committing in a dirty checkout sweeps the owner's unfinished work into a
  burn commit; skip the repo instead.
- Pushing "because the tests passed" removes the morning review this skill
  exists to preserve; commits stay local.

## Output

A skip or blocked line with weekly readings, or the report path plus a digest:
usage before/after, jobs run, skipped repos, and commits as `repo @ hash`.
