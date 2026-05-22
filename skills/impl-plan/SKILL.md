---
name: impl-plan
version: 2.5.0
description: "Unified per-ticket planning skill with a detailed file-map-first plan centered on ordered action, callable seams, typed data flow, blast radius, verification, and explicit gap analysis for missing or partial features."
tier: 3
group: coding
source: local
common_chains:
  after: ["impl"]
allowed-tools: Read, Glob, Grep
---

# Impl Plan

Use this for per-ticket implementation planning after a bounded ticket already
exists.

`impl-plan` is a Tier 3 Codexter coding-pipeline skill. It implements the
generic [plan](../plan/SKILL.md) interface for code tickets; it is not the
universal Tier 2 planning interface for every application domain.

`impl-plan` remains the one public planner:

- default mode: detailed, action-oriented ticket planning
- `--consensus`: Planner/Architect/Critic loop for higher-risk or more
  contentious work

Discovery still belongs to `brainstorm`, `deep-interview`, `prd`, and
`spec-to-ticket`. `impl-plan` is not the broad intake surface.

<!-- MEM-0007 decision: planning output should be approval-first and compact: pitch, before->after, delta, core flow, proof, ask. -->
<!-- MEM-0008 decision: root AGENTS should stay repo-only and terse; skill internals belong in skills, not repo contract text. -->
<!-- MEM-0030 decision: material plans may use one top-level Mermaid delta map when flow or ownership is not obvious from files and signatures alone. -->
<!-- MEM-0031 decision: impl-plan should stay compact and file-map-first: change, why, touched files, signature deltas, blast radius, and verification. -->
<!-- MEM-0050 decision: impl-plan must align with the canonical single-surface ticket template and make typed data flow explicit when it materially affects trust. -->
<!-- MEM-0062 decision: compact chat does not mean thin planning; impl-plan should be detailed and action-oriented enough that a builder can execute the ticket without inventing the missing order or tone. -->

When this skill needs diagram taste or pattern depth, reuse
`skills/diagramming/SKILL.md` plus
`docs/specs/diagram-first-conventions.md` instead of inventing a second diagram
style here.

When the architecture itself is still under-specified, or the plan would have
to invent entities, storage ownership, or runtime boundaries, stop and use
`deep-system-design` before finishing the plan. `impl-plan` owns a detailed
call-and-data shape sketch, not a full system-design interview.

## Intent

This skill should produce one detailed plan in the canonical ticket-body shape,
not parallel documents for different readers.

After spec work has already been decomposed into modular tickets, the selected
ticket is the planning boundary by default. Plan the whole ticket, not a safer
"first slice," unless a real blocker, proof boundary, safety issue, or
explicit follow-up ticket makes narrower scope real.

The highest-signal plan answers:

- what changes and why now
- where it lives: touched files, inspected files, signature deltas, and key
  data shapes
- for incomplete feature work: what production-grade capability looks like and
  what the repo is still missing
- blast radius: callers, systems, workflows, or edges that could break
- how to verify it: tests, checks, strongest evidence, and the ticket-level
  `Proof Contract` that names metrics, review rubric gates, and required artifacts

If the plan leaves the builder inventing execution steps or the next concrete
move, it is too thin.

## Modes

- **Default:** detailed, action-oriented planning in the canonical
  ticket-body shape, keeping the top skimmable while making the execution path
  explicit enough to build from directly
- **`--consensus`:** run the former `ralplan` challenge loop with
  Planner/Architect/Critic before presenting the final plan
- **`--interactive`:** consensus mode only; present the draft and final plan
  for user approval
- **`--deliberate`:** consensus mode only; add pre-mortem and expanded test
  planning for higher-risk work

## Core Prompt Wording

0a. Study `@docs/prd.md` for outcomes + constraints.
0b. Study `@docs/specs/*` for spec truth, including any `Agent Testability Brief` when present.
0b2. For complex runtime/service specs, use
`@docs/specs/spec-authoring-contract.md` to distinguish PRD, system-spec, and
ticket responsibilities; do not push system-spec state machines or conformance
matrices into the ticket plan unless the ticket needs the specific proof row.
0c. Study the active ticket in `@tickets/*` first; if none exists, inspect
`@tickets/*`.
0d. Study `@docs/MEMORY.md` for durable constraints.
0e. Study `@docs/TROUBLES.md` for repeated planning/execution misses when
present.
0f. Search the codebase before assuming anything is missing.
0g. When repo-local context cannot define expected feature scope, ground the
target with the best available installed research surfaces: comparable
codebases, official docs, standards, or repo-search/doc MCPs when available.

## Pre-context Intake

Before finalizing the plan or handing off to execution:

1. Reuse the active ticket, linked docs, and canonical specs as the planning
   context surface.
2. When an `Agent Testability Brief` exists, preserve its control accelerators,
   state probes, coordination views, and proof surfaces in the plan instead of
   inventing testability doctrine again.
3. Preserve or create a ticket-level `Proof Contract` for material tickets:
   honest mechanical metrics when available, `Metrics: none mechanical` when
   not, review rubric families and thresholds, hard gates, required evidence,
   and optional autoresearch session path.
4. Preserve any `Autonomy Readiness` fields from the ticket, PRD, bootstrap
   brief, system design, taste brief, or agent-testability brief; for `$ralph`
   or long-running execution, name missing inputs, permissions, compute, tools,
   QA risks, and human gates before handoff.
5. Read enough nearby code to name real files, seams, signatures, and typed
   data shapes instead of inventing them.
6. In Codexter itself, do **not** create hidden sidecar context snapshots; the
   active repo contract is tickets, linked docs, and mode state.
7. If intent is still vague, use `deep-interview --quick`.
8. If system shape is still vague, use `deep-system-design`.
9. If the repo does not yet implement the target capability clearly enough to
   scope the work, run [research:gap](../research/SKILL.md#researchgap) before
   finalizing the ticket plan. When the open question is what peer products,
   standards, or repos include, run
   [research:parity](../research/SKILL.md#researchparity) first.

Do not hand off to execution while the plan still depends on avoidable
unknowns.

## Trigger Conditions

- user asks for a plan, proposal, implementation approach, or approval-ready
  change summary
- feature/refactor work needs a human yes/no before changing a ticket from
  `status: review` to `status: building`
- request is large enough that the code shape, file touch points, or proof
  should be made explicit before implementation
- execution surfaces redirect a vague implementation request into planning first

## Workflow (Default Mode)

1. **Scope:** treat the selected ticket as the execution ambition by default.
   Keep the approved coherent ticket intact unless it clearly hides multiple
   independent build loops or a real split boundary emerged.
2. **Split check:** split only when proof, reuse, blocking risk, external
   dependency, or runtime ownership genuinely improves; do not force a split
   just because the work will span multiple commits, feels safer, or could be
   shipped incrementally.
3. **Compare:** show 3 viable options with bounded pros/cons when the user did
   not already provide a take on a material choice.
4. **Recommend:** state the best option and the tradeoff being accepted.
5. **Gap check when needed:** for missing or partial feature work, define the
   current state, production expectation, missing gaps, grounding references,
   and recommended now/later boundary.
6. **Proof contract:** for material tickets, write or refine the ticket's
   `Proof Contract` with metrics, rubric gates, and required evidence. Use
   `Metrics: none mechanical` when a number would be dishonest; use
   `autoresearch-plan` only when repeated metric experiments are warranted.
7. **Build one detailed plan:** use the canonical ticket sections and make the
   `Plan` section explicit enough that the builder does not have to invent the
   sequence.
8. **Review + handoff:** run the plan through the quality gate, fix weak spots
   before handoff, then end with a decisive readiness call and next move.

## Workflow (`--consensus` Mode)

Consensus mode preserves the former `ralplan` behavior inside this one skill.

1. Planner drafts one detailed file-grounded plan.
2. Architect reviews for steelman antithesis, tradeoff tension, and synthesis.
3. Critic evaluates for option quality, signature clarity, type-flow clarity,
   risk clarity, and concrete verification.
4. If Critic does not approve, revise and repeat the Architect -> Critic loop.
5. Present the final consensus-backed plan.

Use consensus mode when:

- the change is high risk, ambiguous, or architecturally contentious
- the user explicitly wants stronger challenge before implementation
- the handoff to execution would otherwise rely on untested judgment calls

## Core Decision Branches

- **Low risk / obvious fit:** keep the whole plan lean, but still state the
  concrete action sequence plainly; text-only is okay if the change is truly
  localized.
- **Material / cross-module:** require a clear file map and add a diagram only
  when the flow, ownership, or typed data path is not obvious from the file
  map alone.
- **Interface-heavy / data-shape-heavy:** require explicit signature deltas,
  type sketches, and one typed flow example through the main path.
- **High ambiguity / risk:** add only the extra sections that reduce ambiguity.
- **High risk / architectural tension:** prefer `--consensus`.
- **Linked `Agent Testability Brief`:** carry it into proof/testability
  sections instead of re-deriving shortcuts, probes, or coordination surfaces
  ad hoc.
- **Multi-commit work:** acceptable when the ticket is still one coherent
  build-and-proof loop; split only when a real boundary appears.
- **Already modularized tickets:** assume ticketization already did the
  decomposition work; default to planning full-ticket completion instead of a
  smaller internal phase.
- **Docs-only / rule-text-only:** no specialized QA delegation.

## Plan Shape

Use the canonical ticket-body shape:

- `Summary`
- `Scope`
- `Plan`
- optional `Gap Analysis`
- optional `Diagram`
- `Acceptance Criteria`
- `Verification`
- `Proof Contract`
- optional `Autonomy Readiness`
- optional `Refs`
- `Evidence`
- `Blockers`

`Plan` is the action core of the ticket and should include:

1. `Change`
2. `Why`
3. `Before -> After`
4. `Touch`
5. `Inspect`
6. `Signature delta`
   - compact callable seams in the form `file / symbol(input): output`
7. `Type Sketch`
   - compact struct/type shapes for the data crossing boundaries
   - only the fields that matter
   - never a full dump
8. `Typed flow example`
   - one golden-path dry run showing a representative object or payload
     evolving through the main stages
9. `Execution steps`
   - ordered implementation steps using concrete verbs
10. `Recommendation`
11. `Options considered`
    - only when the user did not already provide a take on a material choice
12. `Blast radius`
13. `Risks`

## Applicability Rule

- **File map + signature delta required:** material feature work,
  workflow/tooling changes, ambiguous implementation work, cross-module
  changes, or any ticket where trust depends on seeing real code seams.
- **Type Sketch + Typed flow example required:** material, stateful,
  interface-heavy, or cross-boundary work where trust depends on seeing data
  shapes stay coherent across steps.
- **Diagram optional but expected for material work:** when system shape, flow,
  ownership, or typed data path is not obvious from the file map alone.
- **Gap Analysis required:** missing or partially implemented feature work,
  parity work, or tickets whose scope depends on external expectations rather
  than an already-clear local implementation.
- **Autonomy Readiness required:** tickets intended for `$ralph`, unattended
  long-running work, external-service work, hard-to-QA UI/motion/simulation, or
  deploy/spend/destructive boundaries.
- **Proof Contract required:** material, review-sensitive, agentically hard, or
  ticketed build work. Include mechanical metrics when useful, `Metrics: none
  mechanical` when not, required review rubric families, thresholds, hard
  gates, required evidence, and optional autoresearch session path.
- **Text-only allowed:** trivial, single-bug, or narrowly localized fixes where
  the file, symbol, or error already anchors the work concretely.

## Top Gotchas

1. Do not implement; this skill is plan-only.
2. Do not duplicate the same idea across summary, plan, criteria, and evidence.
3. Do not hide the key interfaces in prose when a short signature delta would
   prove understanding faster.
4. Do not show callable seams without the matching data seams when the change
   depends on typed payloads, structs, or objects crossing boundaries.
5. Do not leave the builder inferring the execution sequence when the ticket is
   material enough to need an explicit order of operations.
6. Do not preallocate empty review output inside the input ticket.
7. Do not make `Acceptance Criteria` and `Verification` say the same thing;
   criteria define done, verification defines measurement.
8. Do not confuse metrics with rubrics: metrics are mechanical signals,
   rubrics are review judgment frames. Put both in the `Proof Contract` when
   they matter.
9. Do not skip the option comparison for material choices.
10. Do not guess at "production-ready" scope from intuition alone when
   comparable products, codebases, or official docs can ground it.
11. Do not rewrite a coherent ticket into "part 1" or "first slice" just
    because that feels safer than planning the full ticket.
12. Do not use timid language like "maybe", "might", or "could" where the plan
    should be making a recommendation or naming an execution step.
13. Do not hand off a `$ralph`-eligible ticket with vague autonomy-readiness
    fields; name the blockers or keep the ticket gated.

## Efficiency Rules

- Lead with the plan, not the appendix.
- If the user did not provide a take, default to consultative guidance instead
  of neutral mirroring.
- Prefer clear action language over hedging.
- Reuse the `diagramming` skill's compact delta-map patterns instead of
  inventing a new diagram style in each plan.
- Reuse existing modules; justify every new file or abstraction in one line.
- If planning reveals overflow scope, split it into new `tickets/` follow-ups
  instead of stretching one ticket.
- Do not force the richer sections onto trivial localized fixes when the work
  is already concrete from code context.

## Plan Quality Gate

Before returning the plan, run these checks against the drafted output:

1. **Reference coverage**
   - Did the plan actually use the relevant PRD, spec, ticket, memory,
     troubles, and local code context?
   - If a source was skipped, is that omission safe and explicit?
2. **Scope discipline**
   - Is this still one coherent build-and-proof loop?
   - If not, is the split boundary real and explicit rather than just
     commit-count driven?
   - If the ticket was already modularized from the spec, does the plan still
     target the whole ticket instead of inventing a narrower first pass?
3. **Recommendation quality**
   - Did the plan compare real options instead of cosmetic variants?
   - Is the chosen path clearly recommended, not merely listed?
4. **Diagram usefulness**
   - For material work, would a compact diagram make the flow or ownership
     easier to skim?
   - If no diagram is present, is the file map alone clearly enough?
5. **Signature usefulness**
   - Does the signature delta name the real seams that matter?
   - Is it explicit enough to guide implementation?
   - Would it convince a reviewer that the planner understands the codebase?
6. **Type-flow usefulness**
   - Do the named types prove how data crosses the important seams?
   - Is one golden-path object or payload trace enough to make the flow
     believable?
   - Did we avoid turning the plan into a schema dump?
7. **Proof quality**
   - Are the checks concrete and observable?
   - Would a reviewer know exactly how to tell success from failure?
   - Does the `Proof Contract` clearly separate mechanical metrics, review
     rubric gates, and required evidence?
   - If no metric exists, does it honestly say `Metrics: none mechanical`
     instead of inventing a proxy?
8. **Risk clarity**
   - Is the main risk named?
   - Is rollback or containment clear enough for the size of the change?
9. **Gap grounding**
   - If the work depends on external expectations, does the plan show what is
     currently missing and what comparable implementations prove should exist?
   - Are the references concrete instead of hand-wavy product intuition?
10. **Narrative usefulness**
   - If optional sections are present, do they actually reduce ambiguity?
   - Are they concrete rather than decorative or duplicated filler?
   - Does the plan speak in decisive action language instead of hedged
     possibilities?
11. **Architecture boundary**
   - If the plan still depends on invented entities, storage ownership, or
     runtime boundaries, did we stop and route to `deep-system-design`?

If any check fails, tighten the plan before presenting it. The final output
should show the review result, not the draft that failed it.

## References

- [prompts/plan.md](prompts/plan.md)
- [references/template.md](references/template.md)
- [references/examples.md](references/examples.md)
- [references/review.md](references/review.md)

## Final Check

Before handoff, read `references/review.md` and tighten the plan until it passes
