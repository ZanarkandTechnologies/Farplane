# Autoresearch Execution Loop

## Phase 0: Preflight

Run:

```bash
git rev-parse --git-dir
git status --short
pwd
```

Rules:

- Do not proceed if unrelated dirty changes overlap the editable scope.
- Run from the directory containing `autoresearch.md`; nested skill-memory runs
  are valid session roots.
- Create or switch to an `autoresearch/<slug>` branch when starting from an
  ordinary feature branch and the user has not already prepared a branch.
- Preserve `autoresearch.*` artifacts across experiment reverts.

## Phase 1: Resume

Read:

```bash
python3 skills/autoresearch-exec/scripts/summarize_jsonl.py autoresearch.jsonl
tail -20 autoresearch.jsonl
git log --oneline -20
```

If the last run has ASI fields such as `next_action_hint`, use them before
inventing a new idea.

For nested skill-memory runs, also read the target skill's
`self-improve/program.md` and avoid hypotheses listed under rejected ideas.

## Phase 2: Baseline

If no `baseline` run exists in the current JSONL segment:

1. run `./autoresearch.sh`
2. parse the primary metric
3. run `./autoresearch.checks.sh` if present
4. append a `baseline` JSONL entry with the current commit

Do not modify editable files before the baseline exists.

## Phase 3: Hypothesis

Write a one-sentence hypothesis before editing. Good hypotheses are narrow:

- "remove redundant serializer branch to reduce type errors"
- "cache expensive parser setup to reduce benchmark time"
- "split eval assertions so self-improve can diagnose prompt misses"

Avoid changes that need "and" to explain unrelated intents.

## Phase 4: Modify and Commit

Modify one logical thing. Then:

```bash
git diff --name-only
git add <specific files>
git diff --cached --name-only
git commit -m "experiment(<scope>): <description>"
```

No diff means log `no_op` and continue.

## Phase 5: Verify

Run:

```bash
./autoresearch.sh > .autoresearch-run.log 2>&1
python3 skills/autoresearch-exec/scripts/parse_metric.py --metric-name <name> --file .autoresearch-run.log
```

If parsing fails, log `metric_error`, revert the experiment commit, and inspect
the last 50 lines of output.

If checks exist, run:

```bash
./autoresearch.checks.sh > .autoresearch-checks.log 2>&1
```

Check time does not count toward the primary metric.

## Phase 6: Decide

Compare against the best kept metric in the current direction:

- improved + checks pass -> keep
- same/worse -> revert and log `discard`
- crash -> fix trivial syntax/import issues, otherwise revert and log `crash`
- checks fail -> revert and log `checks_failed`

Rollback preference:

```bash
git revert HEAD --no-edit
```

Use destructive reset only when revert cannot complete and user work is not at
risk.

## Phase 7: Log

Each JSONL run entry should include:

- `type`
- `run`
- `commit`
- `metric`
- `metrics`
- `status`
- `description`
- `asi`
- `timestamp`

ASI should capture the lesson, not repeat the description.

## Phase 8: Repeat or Stop

Bounded mode stops after `max_iterations`.

Unbounded mode stops only on:

- user interruption
- broken metric contract
- plateau threshold when configured
- safety issue requiring human judgment

At stop, print baseline, current best, keeps/discards/crashes, and the strongest
next idea.
