# Agent Testability Plan Review

Run this review before handing off the brief.
If any answer is weak, tighten the output first.

## Must Pass

- Does the brief clearly consume a real `System Design Brief` instead of
  reinventing the architecture?
- Are `Control Accelerators`, `State Probes`, and `Coordination Views` all
  explicit when relevant?
- Are the recommendations concrete enough to drive later tickets without
  jumping into stack-specific implementation detail too early?
- Are `Non-Goals` and `Decision Boundaries` explicit?
- Does the brief preserve the existing no-autonomous publish/deploy/spend
  boundary?
- Is there explicit consumer guidance for `spec-to-ticket` and `impl-plan`?
- Are the proposed proof surfaces observable and hard to game?

## Ask If Relevant

- Are we suggesting too many surfaces for the first useful pass?
- Are any recommendations really domain-specific implementations that should be
  deferred to follow-up tickets?
- Is a distributed/dashboard need being confused with simple log visibility?
- Is a UI/control need being confused with hidden-state instrumentation?
- Would a reviewer understand why each recommended surface exists?

## Fail If

- the brief is just “add logs” with no separation between reachability,
  hidden-state visibility, and coordination visibility
- the output overlaps heavily with `deep-system-design` instead of consuming it
- the output acts like a build ticket instead of a planning/doctrine artifact
- the autonomy boundary is weakened or left implicit
- the consumer guidance is missing, vague, or purely aspirational
