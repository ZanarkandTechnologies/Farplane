# Flaky Race

Use for flaky tests, intermittent failures, race conditions, and timing-sensitive bugs.

## Strategy

1. Run the failing path repeatedly until a pattern emerges.
2. Log timestamps, attempt numbers, request IDs, and transaction boundaries.
3. Look for overlap, out-of-order completion, async cleanup, or missing idempotency.
4. Tighten the proof condition: for example "passes 20 times in a row".
5. Fix the ordering, synchronization, waiting, or idempotency gap.

## Instrumentation

- monotonic timestamps
- attempt counter
- request or click sequence number
- transaction open/close markers
- queue enqueue/dequeue markers

## Common Causes

- async work assumed synchronous
- duplicate submits without idempotency
- background job not awaited in tests
- shared mutable state across runs
- missing lock, debounce, or dedupe

## Output

- observed failure pattern
- race window or flaky trigger
- fix
- repeat-run verification
