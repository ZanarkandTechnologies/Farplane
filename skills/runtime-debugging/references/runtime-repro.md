# Runtime Repro

Use for challenging bugs or regressions with a stable reproduction path.

## Strategy

1. Capture exact repro steps, user/account context, and expected vs actual behavior.
2. For a configuration, package, discovery, visibility, or routing symptom, run
   the Local-Control-First Path before tracing the broader codepath.
3. If that path does not explain the symptom, trace the codepath and list 2-4
   hypotheses.
4. Instrument only the decision points that separate those hypotheses.
5. Ask the user to reproduce or run the repro yourself.
6. Use the runtime evidence to choose the smallest fix.
7. Re-run the same repro to verify.

## Local-Control-First Path

Use this before broad codebase, binary, release, or upstream-source research
when one runtime item is missing, disabled, routed incorrectly, or otherwise
behaves differently from nearby items.

1. Run the faithful repro and name the exact missing or incorrect item.
2. Inspect its effective runtime configuration and compare it with one working
   neighbor.
3. Verify source and installed-package identity, then inspect the item's nearest
   metadata or policy control.
4. Patch the first mismatch that fully explains the symptom and rerun the same
   repro.
5. Escalate to platform internals only if the whole local control path agrees
   and the repro still fails. State the failed local checks before escalating.

Do not infer a platform limit from a count, ordering, or other coincidence
without first exhausting this local path.

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
