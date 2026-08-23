---
title: Research Code Patterns
owner: research
status: active
kind: workflow-reference
created_at: 2026-08-20
updated_at: 2026-08-20
---

# Code-Pattern Discovery And Deep Dive

Load this reference only after selecting `research:code-patterns`. It preserves
the discovery and repository-analysis behavior formerly owned by the retired
`external-patterns` package.

## Bind The Search

State the implementation question, language/runtime, target repository family,
compatibility constraints, and freshness bar. Translate the question into
literal source expressions before searching:

- imports or package names: `import { useAction } from "convex/react"`
- exported symbols or calls: `useQuery(` or `async function handleAuth`
- filenames, configuration keys, annotations, or error strings
- a regular expression only when the search provider supports it

Do not submit tutorial questions such as `how to use convex auth`. Record every
literal query and filter so an empty search remains reproducible.

## Discover Broadly

1. Search maintained repositories, official examples, or a caller-specified
   repository set. Use available GitHub code-search or repository tools; do not
   claim a particular connector exists when it is unavailable.
2. Form a candidate pool before settling on an example. Prefer relevant
   repositories with visible recent maintenance, releases, or active ownership;
   a mature stable source may pass a caller-defined freshness bar without a
   recent commit when that judgment is explained.
3. Record repository URL, exact file URL and path, language, maintenance or
   freshness signal, and why each finalist or rejected candidate matters.
4. Keep quoted source code minimal. Capture enough surrounding imports, setup,
   and call-site context to explain the pattern without presenting detached
   snippets or obscuring provenance.

## Deep-Dive The Best 1-3

For each finalist, inspect the source tree or architecture overview before
interpreting an isolated file. Then inspect:

- the entrypoint and key file map;
- surrounding types, configuration, data/state flow, and lifecycle;
- adjacent tests and fixtures;
- error handling, retries, fallbacks, validation, and other failure paths;
- documentation or issues that explain constraints and tradeoffs.

Repository documentation or analysis tools may accelerate this pass, but
direct repository URLs and file paths remain the evidence. Stop when `1-3`
deep dives expose a stable comparison or when the search budget yields only
low-signal candidates; report the evidence gap rather than padding the result.

## Compare And Adapt

Separate copied syntax from transferable constraints. Compare finalists on
architecture, API shape, lifecycle, failure behavior, test strategy,
compatibility, and maintenance cost. Then inspect the local baseline and state:

- what can be adopted directly;
- what must be adapted to local owners and conventions;
- what should be rejected or deferred;
- the smallest implementation and proof path that preserves the useful idea.

When multiple viable patterns leave a material judgment call, compare their
tradeoffs inline and state one recommendation plus the accepted downside.

## Pattern Brief

```markdown
# Pattern Brief: <target>

- Method: research:code-patterns
- Date / freshness bar:
- Language / repo scope:
- Literal queries attempted:
- Local baseline:

## Broad candidates
- <repo URL> — <maintenance signal, relevant file, keep/reject reason>

## Deep dives
### <repo / approach>
- Repository and file URLs:
- Key file map / architecture:
- Implementation shape and contextual snippet:
- Tests and failure handling:
- Constraints:

## Comparison
<shared pattern, meaningful differences, compatibility caveats>

## Local adaptation
<adopt/adapt/reject/defer, smallest useful version, proof route>

## Recommendation / next owner
<one recommendation plus evidence gaps and out-of-scope>
```
