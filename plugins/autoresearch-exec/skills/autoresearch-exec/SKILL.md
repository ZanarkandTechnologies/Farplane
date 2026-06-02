---
name: autoresearch-exec
description: Use when an autoresearch session exists or the user asks to run, continue, resume, or execute metric-driven autoresearch experiments with keep/discard decisions based on autoresearch.md, autoresearch.sh, checks, and autoresearch.jsonl.
tier: 3
group: self-improvement
source: local
---

# Autoresearch Exec

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Important Checklist

- [ ] Read `autoresearch.md`, `autoresearch.jsonl`, optional ideas/checks, git
  status, and the editable scope before changing anything.
- [ ] Use [plan](../plan/SKILL.md) if the session contract, metric, guard, or
  editable scope is inconsistent.
- [ ] Resume from the logged baseline, best metric, last run, and next run
  number.
- [ ] Run or establish the baseline before the first experiment if needed.
- [ ] Pick one hypothesis, modify one logical thing, and stage only intended
  files.
- [ ] Verify the metric and guard, then keep, revert, or stop according to the
  session policy.
- [ ] Update JSONL/session memory with wins, dead ends, and blockers.
- [ ] Use [self-improve](../self-improve/SKILL.md) when the target is a skill
  and durable skill eval memory is involved.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Run the metric-driven experiment loop prepared by `autoresearch-plan`.

## Trigger Conditions

Use when the user asks to:

- run or continue autoresearch
- resume an existing `autoresearch.md` session
- execute a bounded number of metric experiments
- keep improving until a metric plateau or iteration limit
- summarize or finalize an existing autoresearch run

Do not use for ticketed build work requiring QA/review lanes; use `$impl`.
Do not use for short one-off retries; use a normal prompt, explicit command, or
native `/goal` when continuation needs evidence.

## Required Context

Before editing anything, read:

1. `autoresearch.md`
2. `autoresearch.jsonl`
3. `autoresearch.ideas.md` when present
4. recent git history for experiment commits/reverts
5. the editable scope named in `autoresearch.md`

Run from the directory that contains `autoresearch.md`. For skill
self-improvement sessions, that directory may be
`skills/<target-skill>/self-improve/runs/<run-slug>/`; read the target skill's
`self-improve/program.md` through `self-improve` before choosing hypotheses.

Load `references/execution-loop.md` for the detailed loop and
`../autoresearch-plan/references/session-contract.md` for artifact fields when
needed.

Reference split:

- `references/architecture.md` for ownership and boundaries
- `references/workflows.md` for execution phases
- `references/gotchas.md` for rollback and logging failure modes
- `references/recovery-and-finalize.md` for interrupted runs and finalization

## Workflow

1. **Preflight:** confirm this is a git repo, identify dirty files, and refuse
   to risk unrelated user changes in the editable scope.
2. **Resume state:** summarize baseline, best metric, last runs, open ideas, and
   the next run number from `autoresearch.jsonl`.
3. **Ticket bridge:** when the session is linked from a ticket `Proof Contract`,
   keep run summaries and final metric evidence linkable from that ticket's
   `Evidence` section.
4. **Baseline if needed:** run `./autoresearch.sh`, parse the primary metric,
   run checks if configured, and log `baseline`.
5. **Pick one hypothesis:** use `autoresearch.md`, JSONL ASI, ideas, and git log
   to avoid repeats.
6. **Modify one logical thing:** only touch editable scope unless updating
   session memory.
7. **Commit before verify:** stage only intended files and commit
   `experiment(<scope>): <description>`.
8. **Verify and guard:** run `./autoresearch.sh`, parse `METRIC` output, then
   run `./autoresearch.checks.sh` when present.
9. **Decide:** keep if the metric improves in the configured direction and the
   guard passes; otherwise `git revert HEAD --no-edit` and log the reason.
10. **Repeat:** continue until max iterations, plateau, hard failure, or user
   interruption.

## User Modes

- **Bounded operator run:** run the requested iteration count, then summarize
  baseline, best, keeps, discards, and next idea.
- **Resume after compaction:** trust the session files over transcript memory
  and reconstruct state from JSONL, `autoresearch.md`, and git history.
- **Unattended optimization:** obey max iterations, plateau, noise, and safety
  limits from the session instead of inventing open-ended continuation.
- **Skill self-improvement:** keep raw run facts in the nested run directory
  and update the target skill's `self-improve/program.md` only with durable
  lessons through the `self-improve` workflow.
- **Dirty worktree owner:** never risk unrelated user changes; stop for a clean
  branch/stash decision when dirty files overlap editable scope.

## Scripts

- `scripts/parse_metric.py` parses `METRIC name=value` output.
- `scripts/summarize_jsonl.py` prints a compact baseline/current/best summary.

Examples:

```bash
./autoresearch.sh | python3 skills/autoresearch-exec/scripts/parse_metric.py --metric-name type_errors
python3 skills/autoresearch-exec/scripts/summarize_jsonl.py autoresearch.jsonl
```

## Core Decision Branches

- **No session files:** stop execution and use `autoresearch-plan`.
- **Ticket Proof Contract exists:** treat it as the scoreboard for expected
  metric, direction, guard, and evidence link. If the session contradicts the
  ticket, stop and reconcile the contract before continuing.
- **Dirty tree:** continue only when dirty files are unrelated to editable scope;
  otherwise preserve user work and ask for a clean branch/stash decision.
- **Metric parse fails twice:** stop; the Verify contract is broken.
- **Guard fails after improvement:** revert and try at most two reworks of the
  same idea without editing guard/test files.
- **Five consecutive discards:** reread scope and ideas, then try a structurally
  different hypothesis.
- **No best improvement for plateau window:** stop bounded runs normally; for
  unbounded runs, summarize and ask for strategy change unless the session says
  `Plateau-Patience: off`.

## Top Gotchas

1. Do not use `git add -A`; stage only intended files.
2. Do not keep a change when guard checks fail.
3. Do not destroy failed-experiment memory with `git reset --hard` unless
   `git revert` conflicts and the user work is protected.
4. Do not summarize after every run; log the run and keep moving.
5. Do not let session files become stale. Update `autoresearch.md` after major
   wins, dead ends, or strategy shifts.
6. Do not treat nested skill-memory sessions as permission to edit the target
   skill before baseline evals exist.

## Outcome Contract

An execution pass should leave:

- appended `autoresearch.jsonl` entries for every baseline/run/crash/guard fail
- git commits for kept experiments and revert commits for discarded experiments
- updated `autoresearch.md` when learnings materially affect future runs
- optional new bullets in `autoresearch.ideas.md`
- a final summary only when bounded execution stops or the user interrupts
