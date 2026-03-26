# From Error

Use when the user starts from an error message or stack trace.

## Strategy

1. Start at the failing frame, then trace upstream callers.
2. Check whether the error site is the cause or only where bad data surfaced.
3. Search for recent assumptions around nullability, missing relations, stale state, or changed contracts.
4. Prefer a direct fix if the path is obvious; do not force runtime instrumentation.
5. If the upstream cause is still unclear, switch to `runtime-repro.md`.

## Common Checks

- missing include or preload
- null/undefined assumption
- stale schema or data shape
- bad mock or test fixture
- caller passing incomplete state

## Output

- failing frame
- likely upstream cause
- smallest direct fix
- proof by rerun or targeted test
