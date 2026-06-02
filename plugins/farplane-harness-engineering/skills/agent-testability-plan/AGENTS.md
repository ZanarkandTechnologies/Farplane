# `skills/agent-testability-plan/AGENTS.md`

Rules for the `agent-testability-plan` skill surface.

## Purpose

`skills/agent-testability-plan/` owns the post-system-design planning contract
that derives agent testability surfaces before ticketization or per-ticket
build planning. See `MEM-0043`.

## Keep

- one explicit post-design planning step
- visible `Agent Testability Brief` outputs on normal spec/ticket surfaces
- the three-bucket framing: control accelerators, state probes, coordination views
- explicit consumer guidance for `spec-to-ticket` and `impl-plan`
- explicit non-goals and autonomy boundaries

## Do Not

- collapse back into generic “observability” prose
- absorb system-design ownership from `deep-system-design`
- absorb per-ticket build planning from `impl-plan`
- implement concrete helper scripts, dashboards, or runtime adapters inside this skill
- create hidden sidecar artifacts outside normal specs/ticket surfaces
