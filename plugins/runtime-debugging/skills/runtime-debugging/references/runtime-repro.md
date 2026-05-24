# Runtime Repro

Use for challenging bugs or regressions with a stable reproduction path.

## Strategy

1. Capture exact repro steps, user/account context, and expected vs actual behavior.
2. Trace the codepath and list 2-4 hypotheses.
3. Instrument only the decision points that separate those hypotheses.
4. Ask the user to reproduce or run the repro yourself.
5. Use the runtime evidence to choose the smallest fix.
6. Re-run the same repro to verify.

## Instrumentation

- Entry/exit logs on the failing flow
- IDs: request, session, user, job, order, transaction
- Branch markers: which path ran and why
- Key state snapshots: only the fields needed to separate hypotheses

## Output

- repro summary
- hypotheses
- instrumentation points
- observed evidence
- root cause
- verification
