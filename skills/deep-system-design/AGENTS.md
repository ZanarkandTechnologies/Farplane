# `skills/deep-system-design/AGENTS.md`

Rules for the `deep-system-design` skill surface.

## Purpose

`skills/deep-system-design/` owns the ambiguity-reduction contract that
sharpens a system architecture before `agent-testability-plan`, `impl-plan`,
`spec-to-ticket`, or implementation-oriented work.

## Keep

- one-question-at-a-time architecture clarification
- explicit ambiguity scoring and readiness gates
- reusable `System Design Brief` outputs on visible Farplane surfaces
- strong emphasis on entities, signatures, ownership, execution boundaries, and reliability policy
- explicit separation from UI workflow and visual taste planning
- a clear handoff boundary into `agent-testability-plan` when the next missing
  question is agent operability/testability rather than system shape

## Do Not

- collapse into generic architecture prose without signatures or entities
- create hidden sidecar design artifacts outside normal specs/ticket surfaces
- drift into product workflow planning owned by `functional-ui`
- implement code directly from inside the interview mode
- absorb the post-design agent testability planning owned by
  `agent-testability-plan`
