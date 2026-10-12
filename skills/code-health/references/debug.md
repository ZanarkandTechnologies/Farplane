# Debug Mode

Load after `SKILL.md` selects `debug`. Pick the one branch that matches the
evidence you have, not the fix you suspect. Every branch ends the same way:
root cause tied to observed behaviour, smallest fix at the owner, proof on the
same repro.

## Local-control-first path

Use before broad codebase, binary, release or upstream-source research when one
runtime item is missing, disabled, routed wrong, or behaves differently from
its neighbours.

1. Run the faithful repro and name the exact missing or wrong item.
2. Inspect its effective runtime configuration and compare it with one working
   neighbour.
3. Verify source and installed-package identity, then the item's nearest
   metadata or policy control.
4. Patch the first mismatch that fully explains the symptom; rerun the repro.
5. Escalate to platform internals only when the whole local path agrees and the
   repro still fails. State the local checks that did not explain it.

Do not infer a platform limit from a count, ordering or other coincidence
before this path is exhausted.

## From an error or stack trace

- Start at the failing frame, then trace upstream: the error site is often only
  where bad data surfaced.
- Check missing preload or relation, null assumption, stale schema or data
  shape, bad mock or fixture, caller passing incomplete state.
- Fix directly when the path is obvious; switch to the repro branch when the
  upstream cause stays unclear.

## Reproducible runtime bug

- Capture exact repro steps, account or environment context, expected versus
  actual.
- List 2-4 hypotheses that predict different evidence; instrument only the
  decision points that separate them (entry/exit, IDs, branch markers, the few
  state fields that matter).
- Run the repro, choose the fix from the evidence, rerun the same repro.

## From logs or traces

- Rebuild the timeline first; correlate by request, account, job or
  transaction IDs and timestamps.
- Find the last confirmed good event and the first bad or missing one; trace
  the handoff between them in code.
- Add logging only when the existing logs still leave the handoff ambiguous.

## Flaky, intermittent or race

- Run the failing path repeatedly until a pattern appears; log monotonic
  timestamps, attempt counters, sequence numbers, transaction and queue
  markers.
- Look for async work assumed synchronous, duplicate submits without
  idempotency, un-awaited background jobs, shared mutable state across runs,
  missing lock or dedupe.
- Proof bar: the fixed path passes 20 consecutive runs. A sleep is not a fix.

## Performance, memory or network

- Find the slow path before reading code; split latency by network, server,
  database, jobs and client and measure one layer at a time.
- Usual causes: N+1 queries, missing index, no pagination, oversized payloads,
  aggressive timeouts, unbounded caches or listener leaks.
- Report before/after timing or memory numbers for the same scenario.

## Support ticket or account-specific

- Translate the symptom into boundaries: auth, permissions, sync, caching,
  exports, billing, feature flags.
- Check token claims against database truth, role or plan casing, org
  membership propagation, flag targeting, export filters and date ranges.
- Return a short-term workaround and the code fix separately.

## Unfamiliar code

Map responsibilities, callers, side effects and state transitions before
proposing a fix (use the `explore` agent for the file map). Name the parts most
likely to explain the symptom, then return to a branch above.

## After the fix: prevention

Only when prevention or a postmortem matters: explain why the system entered
the bad state, name the broken assumption, search for the same pattern nearby,
and propose a guard, constraint, migration, invalidation or observability fix
with a durable owner. When the same bug class is likely to recur, record it in
the project's `docs/MEMORY.md` (durable constraint) or the owning skill or
validator before closing.
