---
title: Skill Composition Contract
status: active
owner: skill-maintenance
created_at: 2026-08-07
refs:
  - docs/skills/system.md
  - docs/skills/templates/SKILL_TEMPLATE.md
  - skills/skill-maintenance/SKILL.md
---

# Skill Composition Contract

Use this contract when a skill feels like a router, its todos overlap with
neighbors, or its artifacts cannot be handed off without explanation.

```text
skill(request, accepted_inputs, state?)
  -> primary_output + evidence? + next_owner | blocked_report
```

`primary_output` is one named artifact, delivery, or verdict. Evidence proves
that output; it is not another vague `packet`, `report`, or `handoff`.

## Roles

| Role | Owns | Does not own |
| --- | --- | --- |
| Planner | a plan and ordered action graph | specialist artifacts it schedules |
| Advisor | one decision artifact and its acceptance criteria | downstream execution |
| Executor | a materialized delivery and receipt | upstream strategy or final readiness verdict |
| Verifier | an evidence-backed verdict | rebuilding or replanning the candidate |
| Ingest | normalized source/context | downstream decisions or delivery |

Roles describe the invocation, not a new frontmatter field or registry. A
skill can have a different role in a genuinely separate method, but one normal
invocation has one primary output and owner.

## Artifact Lifecycle

```text
context -> decision -> plan -> delivery -> evidence
```

Use specific names at each boundary. For a durable plan, the canonical ticket
is the plan container: put the action graph in its `Change Plan`, completion
conditions in `Done` and `QA Strategy`, and child links in `Links`. Do not add
a parallel plan file, JSON program, or second ticket schema unless a named
consumer needs a derived projection. A caller records child-output links rather
than copying their bodies.

## Todo Boundary

The normal leaf shape is:

1. route or block;
2. bind inputs and choose one domain branch;
3. produce the owned output;
4. apply the domain-specific gate;
5. return the output, evidence, and next owner.

Tier 0 planning/execution/review/writeback and the standard applicable-QA
routine are inherited. Do not repeat them in a leaf todo. Keep provider maps,
rare recipes, and long examples in references that load only after the branch
is selected.

## Planner Contract

```text
planner(intent, constraints, accepted_context?)
  -> canonical_ticket {
       Change Plan: { target, action_graph, dependencies, gates },
       Done / QA Strategy: proof
     } | blocked_report

Action {
  owner
  accepted_inputs
  primary_output
  acceptance_or_blocker
  next_handoff
}
```

The planner is not a thin ICP brief. It decides the complete route needed for a
real artifact to be born, including optional specialist calls and final proof.
Its primary output is the canonical ticket, not a separately named `PLAN`
artifact. It may set requirements for a child, but the child remains the sole
author of its own decision, delivery, or verdict.

## Content Production Prototype

`content-impl-plan` writes a content action graph inside the canonical ticket's
`Change Plan`: target artifact, creative intent, ordered actions, dependencies,
gates, and proof path. It is a section of the ticket, not another artifact
type.

```text
ticket.md
  -> Change Plan / Content action graph
    -> storyboard: SCRIPT_STORYBOARD
    -> asset-advisor: ASSET_MANIFEST + selected realization routes
    -> image/video/audio/avatar executors: accepted media + receipt
    -> editing-advisor: EDIT_DIRECTION
    -> remotion/remotion-render: rendered delivery + render receipt
  -> Done + QA Strategy: evidence verdict
```

Asset Advisor chooses reuse/source/generation and the required realization
child. Content Impl Plan schedules that returned action; it does not select the
same provider a second time. Storyboard owns final scenes, Editing Advisor owns
the timed recipe, and QA/review judge rather than rebuild.

## Migration And Proof

Migrate one family at a time. For each changed skill, record its old and new
primary output, removed duplicate work, retained domain gate, and next owner.
Test one full representative route and at least one blocker route before using
the grammar as a mechanical validator. Use review for ownership sufficiency;
add a validator only after a repeated structural failure is deterministic.
