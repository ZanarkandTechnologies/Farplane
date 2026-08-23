---
name: research
version: 0.2.0
description: "Turn current external evidence needs into method-addressed research briefs for parity, gaps, competitors, official docs, code patterns, users, or sources."
tier: 2
source: local
methods:
  - id: research:parity
    class: artifact
    output: parity-research-report
  - id: research:gap
    class: artifact
    output: gap-research-report
  - id: research:competitor
    class: artifact
    output: competitor-research-report
  - id: research:official-docs
    class: artifact
    output: official-docs-research-report
  - id: research:code-patterns
    class: artifact
    output: code-patterns-research-report
  - id: research:user-grounding
    class: artifact
    output: user-grounding-report
  - id: research:source-synthesis
    class: artifact
    output: source-synthesis-report
eval: evals/evals.json
allowed-tools: Read, Glob, Grep, web_search, documentation-searcher
---

# Research

## Context

Use this Tier 2 surface when a decision needs current external evidence rather
than ideation. Choose one method, establish the local baseline when repository
scope matters, and stop when a downstream owner has enough evidence. For
implementation work, research external practice first and adapt the smallest
useful version to the local proof surface.

## Skill Signature

```text
research(method, target, local_context?, source_scope?, freshness_bar?)
  -> method_brief + source_refs + recommendation + next_owner
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] Choose exactly one primary method:
  [research:parity](SKILL.md#researchparity),
  [research:gap](SKILL.md#researchgap),
  [research:competitor](SKILL.md#researchcompetitor),
  [research:official-docs](SKILL.md#researchofficial-docs),
  [research:code-patterns](SKILL.md#researchcode-patterns),
  [research:user-grounding](SKILL.md#researchuser-grounding), or
  [research:source-synthesis](SKILL.md#researchsource-synthesis).
- [ ] Read the active ticket, local docs, registry rows, or code needed to state
  the local baseline; apply [reference-grounding](../reference-grounding/SKILL.md)
  for provenance, confidence, and local impact.
- [ ] Search current primary, official, maintained, or credible peer sources;
  use [prototyping](../prototyping/SKILL.md) when a large source set needs a
  representative sample first.
- [ ] If `research:code-patterns` is selected, read and execute
  [code-pattern discovery and deep dive](references/code-patterns.md).
- [ ] Add one supporting method only when the primary brief exposes a real
  evidence gap; stop after the smallest sufficient method set.
- [ ] Separate convergent must-haves from optional extras and outliers, then
  return one evidence-backed recommendation and route to `best-of-worlds` or
  the relevant domain planner such as `impl-plan` when further work is needed.
- [ ] Use the [review protocol](../review/SKILL.md) after meaningful research,
  registry, ticket-handoff, or public-doc changes.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## research:parity

Use when credible peers, standards, or maintained reference code should define
the proportional capability baseline. Frame the user/job and parity lens;
capture the local baseline; inspect `2-5` comparables; search broad then
deep-dive the best `1-2`; extract shared surfaces and outliers; return a
`Parity Brief` with comparables, convergence, repo delta, and recommendation.
Weight official standards highest. Route repo-specific missing scope to
`research:gap`.

## research:gap

Use when planning needs the delta between a local missing or partial feature
and a credible production version. Read the ticket, spec, and nearby code;
inspect `2-4` grounded comparables; cover relevant workflow, states, failures,
permissions, validation, data, lifecycle, observability, migration, and
operations; return a `Gap Brief` with current state, expected state, missing
scope, now/later boundary, and planning handoff. Skip when local behavior
already satisfies the target; use parity first when peer norms are unknown.

## research:competitor

Use for named products, tools, or workflows. Define the user job and comparison
dimensions, record visible behavior, strengths, limits, access or pricing when
relevant, and source confidence. Return a `Competitor Brief` with a comparison
matrix, local implications, recommendation, and next route.

## research:official-docs

Use when correctness depends on an API, library, platform, protocol, or
standard. Prefer current official docs, specs, changelogs, and release notes.
Return a `Docs Brief` with direct links, exact behavior, version/deprecation
caveats, constraints, examples, security or migration implications, and local
recommendation.

## research:code-patterns

Use when the question is how maintained repositories implement a pattern, API,
state flow, file layout, failure path, or test strategy. Read
[code-pattern discovery and deep dive](references/code-patterns.md), search
broadly with literal code queries, inspect the best `1-3` repositories in
context, and return the specified `Pattern Brief`. Do not route through a
separate code-pattern skill.

## research:user-grounding

Use when product, UI, content, docs, onboarding, or workflow decisions need
evidence-backed user lenses. Extract `2-4` groups only when they change the
decision; state each group's job, context, constraints, pain, success signal,
and confidence; write concrete stories and conflicts. Return a `User Grounding
Brief` with decision criteria and route to `functional-ui`, `prd`, or the
relevant content/domain owner. Mark thin evidence as hypotheses rather than
inventing demographics.

## research:source-synthesis

Use when several known sources need normalization rather than a full
adopt/adapt/reject/defer workflow. Inventory URL/path, type, credibility,
recency, and relevance; extract claims, evidence, constraints, and conflicts;
separate direct evidence from interpretation. Return a `Source Synthesis Brief`
with strongest and weak claims, conflicts, recommendation, and next owner. Use
`best-of-worlds` for full transferable-feature synthesis.

## Gotchas

- Anchor one pass to one capability, decision, or source set; do not run every
  method or import every adjacent feature.
- Do not treat marketing pages, screenshots, tutorials, or vague posts as
  strong implementation evidence.
- Do not invent connectors, tools, citations, user facts, or current behavior.
- Do not stop at a source dump: name the proportional boundary and next owner.

## Output

Return the method-specific brief with `Method`, `Target`, `Local baseline`,
`Sources`, `Evidence and confidence`, `Current expectation or delta`,
`Recommendation`, and `Next owner / out-of-scope`. Include method-specific
fields such as comparable implementations, user stories, or code file maps
when required.
