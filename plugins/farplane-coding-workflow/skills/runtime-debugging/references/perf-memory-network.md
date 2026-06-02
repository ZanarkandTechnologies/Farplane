# Perf Memory Network

Use for slow pages, slow APIs, memory leaks, timeouts, and network-sensitive failures.

## Strategy

1. Find the slow path before reading too much code.
2. Break total latency into calls, queries, jobs, or rendering phases.
3. Measure one layer at a time: network, server, database, background jobs, client.
4. For memory issues, watch object growth, listeners, caches, and long-lived references.
5. Fix the narrow bottleneck, then measure again.

## Instrumentation

- duration per phase
- request counts
- query counts
- payload sizes
- retry and timeout counters
- heap/process memory snapshots when available

## Common Causes

- N+1 queries
- missing index
- no pagination
- oversized payloads
- aggressive timeout
- unbounded cache or listener leak

## Output

- measured bottleneck
- likely cause
- fix
- before/after timing or memory evidence
