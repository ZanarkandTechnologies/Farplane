# From Logs

Use when the user provides logs, timestamps, traces, or event sequences.

## Strategy

1. Reconstruct the timeline first.
2. Correlate events by IDs, timestamps, and execution phase.
3. Find the last confirmed good event and the first bad or missing one.
4. Trace the handoff between those two points in code.
5. Add targeted logging only if the current logs still leave ambiguity.

## What To Correlate

- request IDs
- user/account/org IDs
- job IDs
- transaction or webhook IDs
- start/end timing
- timeout boundaries

## Output

- event timeline
- missing or inconsistent transition
- suspected handoff failure
- fix and verification source
