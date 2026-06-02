# Autoresearch Exec Workflows

## Bounded Execution

1. Read session artifacts.
2. Validate git preconditions.
3. Establish baseline if absent.
4. Run exactly `max_iterations` experiments.
5. Print final baseline/current/best summary.

## Unbounded Execution

1. Read session artifacts.
2. Establish baseline if absent.
3. Continue one atomic experiment at a time.
4. Stop only on user interruption, broken metric contract, plateau, or safety
   issue.

## Guard Failure Rework

1. Revert the failed experiment.
2. Read guard output.
3. Try at most two narrower implementations of the same idea.
4. Keep only when the metric improves and guard passes.
5. Log unrecoverable failures as `checks_failed`.

