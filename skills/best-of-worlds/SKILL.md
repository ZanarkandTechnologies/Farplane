---
name: best-of-worlds
description: "Use for \"best of worlds\", \"compare these\" or \"what should we take from each\": several named projects, tools or products scored feature by feature and combined into one recommendation."
source: local
template_uses:
  skill-template: "0.6.9"
allowed-tools: Read, Glob, Grep, Bash, web_search
---

# Best of Worlds

## Context

Use this when Kenji names several things (projects, repos, tools, products,
articles) and wants to know what each does best and what to take from each
into one target. It is a shortcut into the `research` skill's `synthesis`
branch: the method, scoring and output live in
[synthesis](../research/references/synthesis.md), not here. A single source
to judge against Farplane goes to `feed-scout` single-source mode; a market
of competitors with no named list goes to `research` market.

## Skill Signature

```text
best_of_worlds(sources: 2+ named things, target: what the result feeds, budget?)
  -> comparison table + combined recommendation + next owner
reads: the named sources (code first, then docs, then write-ups), the local target
does: runs research with branch synthesis on the named sources
writes: the caller's artifact, else .farplane/research/YYYY-MM-DD-best-of-worlds-<slug>.md
returns: the feature table, the combined workflow, the tradeoff accepted, the next owner
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Bind the sources and the target.**
  `request -> named sources + target + success measure | one question`

  Rule: List every source Kenji named and the one target the result feeds (a
  skill, page, product, or workflow). With no target, ask one question naming
  the likely candidates; with fewer than two sources, route to `feed-scout`
  single-source mode instead.

  Assert:
  - Every named source is in the list, or its exclusion is stated.
- [ ] **N2 — Run the research synthesis branch.**
  `sources + target -> feature table + combined recommendation`

  Rule: Invoke the `research` skill with branch `synthesis` and follow
  [synthesis](../research/references/synthesis.md) in full: catalogue,
  extract, cluster, score, decide.

  Assert:
  - Each feature row cites where in which source it came from.
  - No row says "maybe"; timing-only cases are `defer`.
- [ ] **N3 — Return the comparison.**
  `table -> table + combined recommendation + next owner`

  Rule: Return the feature table, the combined workflow, the tradeoff
  accepted, and the next owner (`impl-plan`, `harness`, `prd`, or none).

  Assert:
  - The recommendation names what it gives up.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

| Feature | Sources | Evidence | Scores | Decision | Reason |
| --- | --- | --- | --- | --- | --- |

Then the combined workflow, the tradeoff accepted, and the next owner.
