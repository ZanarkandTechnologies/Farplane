# Root Cause Analysis

Use after the immediate bug is fixed but the underlying reason still matters.

## Strategy

1. Explain why the system entered the bad state.
2. Trace the sequence of events, not just the failing line.
3. Identify the broken assumption, migration gap, data drift, or missing invariant.
4. Search for similar patterns nearby.
5. Recommend prevention: guard, constraint, migration, invalidation, or observability.

## Output

- root cause sequence
- broken assumption
- similar risk sites
- prevention steps
