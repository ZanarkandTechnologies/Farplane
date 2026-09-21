---
name: implementation-research
description: "Turn a feature question and local codebase into sourced external implementation patterns, a verified local delta, and an implementation handoff."
tier: 2
source: local
template_uses:
  skill-template: "0.6.2"
  skill-eval-task: "0.2.0"
  skill-surface-budget: "0.1.0"
allowed-tools: Read, Glob, Grep, Bash, web_search, documentation-searcher
---

# Implementation Research

## Context

Use this skill when a feature or engineering decision needs evidence from
official documentation, maintained code, issues, demos, and technical videos
before local planning. It owns external pattern discovery, repository deep
dives, and comparison with the actual local seam. It ends with a handoff to
`impl-plan` or a direct small edit; it does not implement the feature.

## Skill Signature

```text
implementation_research(question, local_target, constraints?, source_scope?)
  -> implementation_research_brief + implementation_handoff
reads: local code and proof surface, official docs, repositories, issues, demos
does: discovers and tests external patterns against the local architecture
writes: none unless the caller supplies an artifact owner
returns: source map, local delta, adopt/adapt/reject decisions, proof path
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Map the local seam before searching.**
  `question + local target -> local contract + search hypotheses`

  Rule: Identify the entrypoint, owners, state flow, constraints, adjacent tests,
  and failure behavior that any external pattern must fit.

  Assert:
  - The search question names a concrete symbol, state transition, API, file
    family, or failure path.
  - The brief does not infer a local gap before reading the local owner.

- [ ] **N2 — Discover candidates across complementary source classes.**
  `search hypotheses -> query ledger + candidate pool | docs-only branch`

  Rule: Prefer official docs or a documentation MCP for contracts; use literal
  code queries for repositories; inspect issues and changelogs for failure
  constraints; search X and YouTube for recent demos, authors, and linked code.
  Follow [implementation discovery](references/implementation-discovery.md).

  Assert:
  - Queries and filters are reproducible and discovery covers more than one hit.
  - Every candidate keeps its repo, file, doc, issue, video, or post provenance.

- [ ] **N3 — Promote only maintained, relevant patterns.**
  `candidate pool -> finalists + rejection ledger | no-credible-pattern branch`

  Rule: Score semantic fit, maintenance, completeness, license or dependency
  constraints, test evidence, and compatibility. Select up to three candidates
  that cross the bar; do not fill the set with weak examples.

  Example: `four repositories -> two maintained lifecycle matches -> one stale
  demo and one incompatible framework rejected`.

  Assert:
  - Rejected candidates have a concrete reason.
  - Tutorials and demos without inspectable implementation are supporting
    evidence, not the primary pattern.

- [ ] **N4 — Deep-dive finalists in parallel when useful.**
  `finalists -> implementation dossiers | parallel-lane branch`

  Rule: With multiple finalists and bounded delegation, assign one independent
  lane per finalist. Inspect the repository map, entrypoint, types/configuration,
  state and lifecycle, tests, validation, errors, retries, cancellation,
  migration, and relevant author or issue trail.

  Assert:
  - Each dossier cites exact files or URLs and explains surrounding behavior.
  - Each lane returns transferable constraints, source-specific assumptions,
    unknowns, and evidence against adoption.

- [ ] **N5 — Reconcile external patterns with the local implementation.**
  `dossiers + local contract -> local delta + implementation handoff`

  Rule: Refine or reject the starting hypotheses, then decide what to adopt,
  adapt, trial, reject, or defer. Recommend the smallest local change that
  preserves the useful constraint and name the proof that could falsify it.

  Assert:
  - The local delta covers behavior, ownership, failure paths, and tests rather
    than surface syntax alone.
  - The handoff names one recommended approach, its downside, exact local
    owners, and a proportional proof path.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Natural-language tutorial searches miss the symbols and errors that locate
  real implementations.
- A popular repository is not automatically compatible with the local lifecycle.
- Detached snippets hide setup, cleanup, concurrency, and failure behavior.

## Output

Return an `Implementation Research Brief` with the local contract, hypothesis
tree, query ledger, candidate and rejection ledger, finalist file maps, source
evidence, comparison, verified local delta, adopt/adapt/trial/reject/defer
decisions, recommended implementation shape, and proof-oriented handoff.
