# Autoresearch Plan Workflows

## Setup Workflow

1. Inspect repo scripts, docs, and target files for likely metrics.
2. Infer Goal, Scope, Metric, Direction, Verify, Guard, and Iterations.
3. Ask for only missing preferences that cannot be discovered.
4. Validate scope resolves to files.
5. Safety-screen Verify.
6. Dry-run Verify and confirm one numeric metric.
7. Scaffold session files.
8. Hand off to `autoresearch-exec`.

## Metric Repair Workflow

1. Run the candidate command.
2. Capture raw output.
3. Identify the exact numeric value that represents success.
4. Wrap the command in `autoresearch.sh` so it emits `METRIC name=value`.
5. Reject the metric if it remains subjective, multi-valued, or slow enough to
   make iteration impractical.

