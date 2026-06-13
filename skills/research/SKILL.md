---
name: research
version: 0.1.0
description: "Turn current external evidence needs into method-addressed research briefs for parity, gaps, competitors, official docs, code patterns, users, or sources."
tier: 2
source: local
methods: ["research:parity", "research:gap", "research:competitor", "research:official-docs", "research:code-patterns", "research:user-grounding", "research:source-synthesis"]
allowed-tools: Read, Glob, Grep, web_search, documentation-searcher
---

# Research

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] Choose exactly one primary method first:
  [research:parity](SKILL.md#researchparity),
  [research:gap](SKILL.md#researchgap),
  [research:competitor](SKILL.md#researchcompetitor),
  [research:official-docs](SKILL.md#researchofficial-docs),
  [research:code-patterns](SKILL.md#researchcode-patterns), or
  [research:user-grounding](SKILL.md#researchuser-grounding), or
  [research:source-synthesis](SKILL.md#researchsource-synthesis).
- [ ] Use [reference-grounding](../reference-grounding/SKILL.md) as the Tier 1
  evidence discipline: local baseline, primary sources, source confidence, and
  local impact.
- [ ] Use [prototyping](../prototyping/SKILL.md) when the source set, skill set,
  dataset, or comparison set is large enough that a representative sample
  should shape the full pass first.
- [ ] Read the active ticket, local docs, specs, registry rows, or nearby code
  needed to state the local baseline.
- [ ] Add a supporting method only when the primary method exposes a real gap:
  - official/API uncertainty -> [research:official-docs](SKILL.md#researchofficial-docs)
    or the documentation helper
  - real repo implementation pattern needed ->
    [research:code-patterns](SKILL.md#researchcode-patterns) or the external
    patterns helper
  - peer/product norm missing -> [research:parity](SKILL.md#researchparity)
  - current-state production gap needed -> [research:gap](SKILL.md#researchgap)
  - user groups, jobs, stories, context, friction, or success signals needed ->
    [research:user-grounding](SKILL.md#researchuser-grounding)
  - several sources need normalization ->
    [research:source-synthesis](SKILL.md#researchsource-synthesis)
- [ ] Stop after the smallest method set that can produce the needed brief; do
  not run every research method by default.
- [ ] Route the brief to the next owner:
  [advise](../advise/SKILL.md) for judgment calls,
  `best-of-worlds` for adopt/adapt/reject/defer synthesis, or the relevant
  domain planning skill such as `impl-plan` for coding.
- [ ] Run the [review protocol](../review/SKILL.md) after meaningful research-skill,
  registry, ticket-handoff, or public-doc changes.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Use this as the Tier 2 research workflow when the task needs grounded
references without ideation. Pick one method explicitly and keep the output
compact enough for `brainstorm`, `plan`, or a domain pipeline to consume.
This is a method-addressed surface, not a sequential checklist: choose one
primary method, add a supporting method only when the primary brief exposes a
real gap, and stop when the downstream skill has enough evidence.

For implementation planning, use this skill when the approach should be shaped
by the latest external practice: current official docs, maintained code
examples, credible peer products, standards, or production-grade feature
expectations. The default pattern is external-first, local-fit second: learn the
current high-quality approaches, then adapt the smallest useful version to the
repo's existing code and proof surface.

This skill absorbs the former public `parity-research` and `gap-analysis`
packages. Use method addresses instead of nested research routers.

Methods:

- `research:parity`
- `research:gap`
- `research:competitor`
- `research:official-docs`
- `research:code-patterns`
- `research:user-grounding`
- `research:source-synthesis`

## First-Load Contract

1. Name the method and target capability, workflow, API, or source set.
2. Use [reference-grounding](../reference-grounding/SKILL.md) as the Tier 1
   evidence discipline: local baseline first when repo scope matters, primary
   sources over commentary, and explicit source confidence.
3. For implementation features, search current external sources before locking
   the approach unless the user explicitly asks for local-only work or the
   change is a tiny same-scope fix.
4. Use [prototyping](../prototyping/SKILL.md) when a large source set should be
   sampled before expanding the research pass.
5. Separate common must-haves from optional extras and outliers.
6. End with one recommendation and the next skill or artifact that should use
   the brief.

## research:parity

Use `research:parity` when the main question is "what do credible peers,
standards, or reference codebases consistently include for this capability?"
before local scope or priority is locked.

### Workflow

1. Frame the capability, target user/operator, and parity lens.
2. Capture the local baseline so the comparison stays anchored.
3. Assemble `2-5` grounded comparables across products, official docs,
   standards, or maintained repos.
4. Search broad, then deep-dive the best `1-2` sources.
5. Extract convergence: shared surfaces, outlier extras, and proportional
   must-haves.
6. Return a `Parity Brief` with parity target, comparable implementations,
   common surfaces, repo delta, recommendation, and follow-ups.

### Branches

- Official spec or standard exists: weigh it highest.
- Code-pattern parity is the question: start from maintained repos and literal
  implementation-pattern searches.
- Workflow or product parity is the question: compare real apps and docs first.
- The output is now repo-specific missing scope: route to `research:gap`.

## research:gap

Use `research:gap` before implementation planning when the hard question is
"what does a credible production version of this missing or partial feature
need, and what is Farplane currently missing?"

### Workflow

1. State the feature, primary user/operator, and job-to-be-done.
2. Read the ticket, spec, PRD, and nearby code to document current state.
3. Inspect `2-4` grounded comparables after the local limit is clear.
4. Extract the capability checklist those comparables converge on: workflow,
   states, failure modes, permissions, validation, data, lifecycle,
   observability, admin, migration, or operations surfaces as relevant.
5. Produce a `Gap Brief` with current state, production expectation, missing
   gaps, comparable implementations, recommendation, and follow-ups.
6. Recommend one now-versus-later boundary.
7. Hand the compact result to the domain planning skill, such as
   `impl-plan` for coding.

### Branches

- The repo already contains the target behavior: skip this method.
- Peer norms are unknown: run `research:parity` first.
- Workflow or IA dominates: pair with `functional-ui`.
- Architecture is undefined: route to `deep-system-design`.

## research:competitor

Use `research:competitor` when named products, tools, or workflows need to be
compared against Farplane or against each other.

### Workflow

1. Name the comparison set and why each competitor belongs.
2. Define the user job and comparison dimensions.
3. Capture visible surfaces, strengths, limits, pricing/access constraints when
   relevant, and source confidence.
4. Compare against the local baseline or desired workflow.
5. Return a `Competitor Brief` with matrix, adoption implications, and next
   route: `advise`, `best-of-worlds`, `functional-ui`, or a domain plan.

## research:official-docs

Use `research:official-docs` when correctness depends on current official
library, platform, API, protocol, or standards behavior.

### Workflow

1. Name the API, standard, library, or platform behavior question.
2. Prefer official docs, specs, changelogs, or release notes.
3. Extract relevant constraints, examples, version notes, deprecations, limits,
   and security/migration requirements.
4. Return a `Docs Brief` with source links, exact behavior, version caveats,
   local impact, and recommended route.

## research:code-patterns

Use `research:code-patterns` when the question is how maintained repositories
actually implement a pattern, API, state flow, file layout, or test strategy.

### Workflow

1. Convert the question into literal code patterns, filenames, package names,
   or exported symbols.
2. Search current maintained repos, official examples, or the requested repo set
   before inventing an implementation pattern locally.
3. Deep-dive the most relevant `1-3` examples and inspect surrounding tests,
   docs, and failure handling.
4. Separate copied syntax from transferable design constraints.
5. Return a `Pattern Brief` with examples, common implementation shape,
   compatibility caveats, and local recommendation.

## research:user-grounding

Use `research:user-grounding` when a product, UI, content, docs, onboarding,
or workflow decision needs a grounded view of the people or roles affected
before comparing options.

This method is not fake persona writing. It derives or hypothesizes user
lenses from the available context, labels confidence, and turns those lenses
into decision criteria for `plan`, `advise`, `functional-ui`, `prd`, content
planning, or another domain skill.

### Workflow

1. Name the artifact or workflow being shaped and the decision it needs to
   inform.
2. Extract known users, stakeholders, operators, or audiences from the request,
   PRD, ticket, screenshots, analytics, support notes, existing product, or
   comparable examples.
3. Identify `2-4` user groups only when they change the product decision.
4. For each group, state job-to-be-done, context, constraints, pain points,
   success signals, and confidence level.
5. Write concrete job stories or user stories that can judge the options.
6. Name conflicts between groups and the decision criteria they imply.
7. Return a `User Grounding Brief` with user groups, stories, decision
   criteria, confidence notes, and the recommended next route.

### Branches

- If the main work is UI or workflow shape: hand off to `functional-ui`.
- If the main work is requirements: hand off to `prd`.
- If the main work is a content asset or campaign: hand off to the relevant
  content or media skill.
- If evidence is too thin, mark the user lens as a hypothesis instead of
  inventing demographic detail.

## research:source-synthesis

Use `research:source-synthesis` when several sources need to be summarized into
one decision-ready brief, but the job is evidence synthesis rather than full
adopt/adapt/reject workflow design.

For full synthesis that scores transferable features from known sources and
turns them into a local workflow or implementation handoff, use
`best-of-worlds`. This method can feed that skill by normalizing source facts.

### Workflow

1. Inventory each source with URL/path, source type, credibility, recency, and
   why it matters.
2. Extract claims, evidence, constraints, and contradictions.
3. Cluster overlapping ideas and separate direct evidence from interpretation.
4. Return a `Source Synthesis Brief` with inventory, strongest claims, weak
   claims, conflicts, recommendation, and next route.

## Output Contracts

Use the method-specific title and keep these fields where they apply:

- `Method`
- `Capability / target`
- `Local baseline`
- `Sources / comparable implementations`
- `User groups / job stories`
- `Decision criteria`
- `Common surfaces / current expectation`
- `Current state`
- `Missing gaps / repo delta`
- `Recommendation`
- `Follow-ups / out-of-scope`

## Guardrails

- Anchor each research pass to one capability or source set.
- Do not treat screenshots, marketing pages, or vague blog posts as strong
  implementation evidence.
- Do not import every adjacent feature from a larger product into one ticket.
- Do not stop at a research dump; recommend a boundary or next route.
- Keep production expectations proportional to Farplane and the ticket size.
- Do not pretend a specific MCP, connector, or external tool exists.
