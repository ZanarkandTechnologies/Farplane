# Metric Advisor

`metric-advisor` is the small Farplane primitive for deciding what signal is
honest enough to optimize.

Use it when an eval result, Goal Packet, ticket proof block, strategy frontier,
or improvement idea needs a measurement contract before execution. It returns a
metric card with provider, primary metric, direction, guard metrics,
anti-metrics, minimum meaningful delta, measurement method, and route hint.

It does not run the loop. Callers keep their jobs:

- `optimize-harness` coordinates recovery and accept/hold/rollback.
- `goal-advisor` compiles Goal Packet metric providers.
- `self-improve` compares variants after a baseline exists.
- `metric-advisor` owns measurable project objectives, directions, guards, and providers.
- `impl-plan` owns ticket Done / Proof wording.
- `review` judges evidence when metric traceability is qualitative.
