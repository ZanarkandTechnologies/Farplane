---
name: parity-research
version: 0.1.0
description: Use when the main question is what comparable products, official docs, standards, or open-source codebases include for a capability, so external parity can be grounded before scope or prioritization decisions are made.
allowed-tools: Read, Glob, Grep
---

# Parity Research

Use this when the real question is not yet "what are we missing in our repo?"
but "what do credible peers, standards, or reference codebases consistently
include for this capability?"

This is an external-comparables skill. It can feed `gap-analysis`,
`functional-ui`, or `impl-plan`, but it does not replace them.

## First-Load Contract

### Trigger Conditions

- parity-driven asks against another product, ecosystem standard, or category
- "what do others have that we don't?" before ticket scope is clear
- need to inspect open-source repos or official docs to set a credible feature
  target
- current repo behavior is known enough, but the external target is not

Do not use this for runtime/root-cause debugging or obvious local-only feature
planning where the external target is already clear.

### Workflow (6 Steps)

1. **Frame the parity question**: define the capability, target user/operator,
   and the specific parity lens.
2. **Capture the local baseline**: note what our repo already has so the
   comparison does not drift into generic research.
3. **Assemble 2-5 grounded comparables**: prefer real products, official docs
   or standards, and maintained open-source repos with relevant code paths.
4. **Search broad, then go deep**: use literal code-pattern or feature-surface
   searches to find candidates, then deep-dive the best `1-2` repos/docs.
5. **Extract convergence**: separate the surfaces most credible sources share
   from outlier extras or adjacent nice-to-haves.
6. **Return a parity brief**: state the parity target, comparable
   implementations, common surfaces, repo delta, and recommended now/later cut.

### Core Decision Branches

- **Official spec or standard exists** -> weigh that highest and use products or
  repos as secondary implementation evidence.
- **Question is mostly code-pattern parity** -> start from maintained
  open-source repos and literal implementation-pattern searches.
- **Question is mostly workflow/product parity** -> compare real apps and docs
  first, then pair with `functional-ui` if workflow choice is still open.
- **Question is now repo-specific scope and missing pieces** -> hand the output
  to `gap-analysis`.

### Top 3 Gotchas

1. Do not treat screenshots, marketing pages, or vague blog posts as
   implementation evidence.
2. Do not import every adjacent feature from a larger product into the same
   parity target.
3. Do not stop at a research dump; end with one recommended parity boundary.

### Outcome Contract

When this skill is used, the resulting artifact or response must include:

1. `Capability + parity lens`
2. `Local baseline`
3. `Comparable implementations`
4. `Common surfaces`
5. `Repo delta`
6. `Recommendation`
7. `Follow-ups / out-of-scope`

## Use When

- the operator asks what peer products or repos include for a capability
- the ticket is parity-driven and the external comparison set is still fuzzy
- a feature feels under-scoped because nobody checked the actual category norm
- open-source or standards research is needed before deciding what "credible"
  means

## Do Not Use When

- the main task is local current-state versus production-expectation scoping;
  use `gap-analysis`
- the task is runtime debugging or root-cause analysis; use
  `runtime-debugging`
- the task is official-library API lookup with no parity question; use
  `documentation`
- the task is local code exploration only; use `codebase-analysis`

## Tooling Guidance

- Start repo-first: read the local ticket, specs, or code enough to set the
  comparison lens before external search.
- Prefer primary sources and real implementations over commentary.
- For broad external code search, use installed GitHub/repo search surfaces
  such as grep MCP with literal implementation patterns instead of vague
  natural-language queries.
- For deeper repo understanding, use installed deep-dive surfaces such as
  DeepWiki after broad search identifies the most relevant repos.
- For official behavior, standards, or API expectations, prefer official docs
  or spec sources over repo folklore.
- Record why each source made the cut: maintenance, adoption, recency, or
  direct relevance.

## Output

Produce a compact `Parity Brief` with:

- `Capability + parity lens`
- `Local baseline`
- `Comparable implementations`
- `Common surfaces`
- `Repo delta`
- `Recommendation`
- `Follow-ups / out-of-scope`

## Guardrails

- anchor the comparison to one capability, not the whole product category
- prefer convergence across `2-5` sources over one flashy reference app
- distinguish shared must-haves from optional or premium extras
- keep "parity" proportional to the product and ticket scope
- route back into `gap-analysis`, `functional-ui`, or `impl-plan` once the
  parity target is clear
