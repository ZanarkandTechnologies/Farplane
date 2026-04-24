---
name: gap-analysis
version: 0.1.0
description: Use when planning a missing or partial feature needs grounded research on what a production-grade implementation should include, using comparable apps, official docs, standards, or real codebases before scoping the ticket.
allowed-tools: Read, Glob, Grep
---

# Gap Analysis

Use this before implementation planning when the hard question is not "how do we
code it?" but "what does a real, production-grade version of this feature need,
and what are we currently missing?"

If the primary question is broader external parity research such as "what do
other products, standards, or open-source repos consistently include?" use
`parity-research` first, then bring the resulting comparison into this skill.

## Job

1. Define the user-facing capability or operator job the feature must serve.
2. Capture the repo's current state and the exact missing behavior.
3. Study 2-4 grounded comparables: real apps, official docs, standards, or
   production codebases that already implement the capability.
4. Extract the non-negotiable surfaces those comparables consistently include.
5. Separate must-have-now scope from deferable follow-up scope.
6. Hand the resulting gap analysis to `impl-plan` as the ticket's grounding.

## Use When

- the repo only partially implements a feature and the missing scope is unclear
- the ticket is for net-new feature work and "done" depends on production
  expectations rather than just local code
- the team keeps underbuilding a feature because the expected states,
  integrations, or edge cases were never researched explicitly

## Do Not Use When

- the task is a clear localized bug with an already-known expected behavior
- the main question is external parity against another product, repo, or
  ecosystem standard; use `parity-research`
- the work is pure visual/UI workflow design; use `functional-ui`
- the work is runtime/root-cause debugging; use `runtime-debugging`
- the architecture itself is still undefined; use `deep-system-design`

## Workflow

1. State the feature, the primary user or operator, and the top job-to-be-done.
2. Read the ticket, spec, PRD, and nearby code to document the current state.
3. Inspect 2-4 grounded comparables, preferring:
   - real production apps or well-adopted open-source products
   - official documentation or standards
   - real code paths from comparable codebases
4. Extract the capability checklist those comparables converge on:
   - primary workflow
   - required states and failure modes
   - permissions, validation, data, or lifecycle edges
   - observability, admin, migration, or operational surfaces when relevant
5. Produce a `Gap Analysis` with:
   - `Current state`
   - `Production expectation`
   - `Missing gaps`
   - `Comparable implementations`
   - `Recommendation`
6. Recommend one scope boundary for this ticket:
   - what must land now to be credible
   - what should be a follow-up ticket
7. Hand the result to `impl-plan`, which should copy only the compact output it
   actually needs into the ticket body.

## Core Decision Branches

- If the repo already contains the target behavior locally, skip this skill and
  let `impl-plan` stay codebase-grounded.
- If the missing scope first requires a broader comparable-products or
  comparable-codebases pass, run `parity-research` before narrowing this into a
  now-versus-later ticket cut line.
- If the feature shape is mostly product workflow, pair this with
  `functional-ui` after the capability checklist is clear.
- If the missing scope depends on architecture or platform boundaries, stop and
  route to `deep-system-design` before pretending the gap is only feature-level.

## Tooling Guidance

- Prefer repo-local evidence first: nearby code, docs, and active tickets.
- For external research, use the best installed surface that actually exists in
  the repo/runtime:
  - GitHub/repo search for comparable code
  - official docs search or documentation MCPs
  - repo-search/doc MCPs such as DeepWiki, Ref, Context7, or grep-style tools
    when they are installed
- Do not pretend a specific MCP exists. Degrade cleanly to the available tools.
- Favor primary sources and real implementations over blog-post summaries.

## Output

Produce a compact planning artifact with:

- `Capability + user`
- `Current state`
- `Comparable implementations`
- `Production expectation`
- `Recommendation`
- `Follow-ups / out-of-scope`

## Guardrails

- start from the user job and observed repo gap, not from imagined components
- compare real implementations, not just marketing screenshots
- name the current limit explicitly; do not hide it inside prose
- recommend one scope boundary; do not stop at a reference dump
- keep "production-ready" proportional to the product and ticket size, not to a
  FAANG-scale wishlist

## Top Gotchas

1. Do not treat inspiration screenshots as implementation evidence.
2. Do not import every adjacent capability from a large product into one ticket.
3. Do not leave the analysis as a research dump without a recommended now/later
   cut line.

## Outcome Contract

When this skill is used, the resulting plan/ticket should explicitly contain:

1. `Current state`
2. `Production expectation`
3. `Missing gaps`
4. `Comparable implementations`
5. `Recommendation`
