# Workflows

## Main Agent

1. Confirm the operator actually wants `desloppify` cleanup rather than a plain
   review.
2. Inspect obvious generated or runtime-only paths.
3. Spawn one worker and tell it to use the `desloppify` skill in worker mode.
4. Own follow-up decisions, questionable excludes, and any blocker the worker
   returns.

## Worker

1. Verify Python 3.11+ is available.
2. Run `pip install --upgrade "desloppify[full]"`.
3. Run `desloppify update-skill codex`.
4. Exclude only obvious generated, vendored, or runtime paths.
5. Run `desloppify scan --path <target>`, then `desloppify next`.
6. Fix the current queue item, run the exact resolve command, and repeat.
7. Stop and report back if nested `review --run-batches --runner codex` is
   required.
