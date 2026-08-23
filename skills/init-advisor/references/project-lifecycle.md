# Project Lifecycle

Use this as the canonical project-work lifecycle when bootstrapping a repo and
when aligning downstream skills. This is a reference, not a standalone skill:
`init-advisor` owns the bootstrap surface, while domain skills implement
the lifecycle phases for their project type.

## Algebra

```text
ProjectLifecycle :=
  Bootstrap
+ DeepInterview
+ PRD
+ TicketBreakdown
+ TicketLoop*

TicketLoop :=
  PlanTicket
+ ExecuteTicket
+ VerifyTicket
+ ReviewTicket
+ CloseTicket
```

## Phase Owners

```text
Bootstrap := init-advisor
ClarifyBootstrap := direct clarification
PRD := prd
TicketBreakdown := spec-to-ticket
PlanTicket<CodingTicket> := impl-plan
ExecuteTicket<CodingTicket> := goal-advisor
VerifyTicket := qa | visual-qa | review | domain proof skill
CloseTicket<CodingTicket> := close-ticket
```

Domain project profiles may bind the same lifecycle to different ticket
planners, executors, and proof skills. For example, a video project may plan a
content ticket through `content-impl-plan` and execute/render through
`ai-video-advisor`, `remotion`, or `remotion-render`.

## Pattern Map

- `Template Method`: the lifecycle order is fixed; domain skills fill in the
  phase-specific work.
- `Strategy`: planners, executors, and proof skills vary by domain and ticket
  type.
- `Abstract Factory`: project profiles create component sets, advice axes,
  prototype gates, ticket shapes, and proof surfaces.
- `Command`: tickets are executable work packages with scope, plan, evidence,
  blockers, and closeout.
- `Observer`: QA, visual QA, review, and evidence checks inspect artifacts
  without owning the work.
- `Memento`: `docs/`, `tickets/`, archived tickets, history, memory, and
  artifacts preserve project state across agent loops.

## Placement Rules

- Keep the compact lifecycle invariant in generated project `AGENTS.md` because
  agents load it every loop.
- Keep technical stack, commands, runtime, and QA paths in `PROJECT_RULES.md`.
- Keep project-specific profile, lifecycle route, prototype gates, and handoff
  choices in `docs/bootstrap-brief.md`.
- Keep the detailed lifecycle theory here until multiple higher-tier skills
  actively need a public `project-pipeline` skill.
- Keep generic planning and execution in native lifecycle phases while domain
  skills own the real artifacts and algorithms.
