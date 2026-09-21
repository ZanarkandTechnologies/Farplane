---
name: competitor-research
description: "Turn a market or product question into sourced competitor evidence, review themes, differentiated gaps, and a recommended opportunity."
tier: 2
source: local
template_uses:
  skill-template: "0.6.2"
  skill-eval-task: "0.2.0"
  skill-surface-budget: "0.1.0"
allowed-tools: Read, Glob, Grep, Bash, web_search
---

# Competitor Research

## Context

Use this skill when a product or business decision depends on how named or
discoverable competitors perform for a specific customer job. It owns broad
discovery, thresholded finalist selection, review and community evidence, and
the resulting market opportunity. It does not own customer interviews or the
implementation plan.

## Skill Signature

```text
competitor_research(question, market?, tracked_platforms?, budget?)
  -> competitor_intelligence_brief
reads: local product baseline, public product evidence, reviews, discussions, demos
does: discovers, qualifies, investigates, and compares relevant competitors
writes: none unless the caller supplies an artifact owner
returns: sourced comparison, review themes, opportunity, recommendation
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Bind the customer job and competitive claim.**
  `business question + local baseline -> comparison contract | missing-baseline branch`

  Rule: Compare products only on behavior that changes the named user's choice
  or outcome. Record hypotheses as questions that evidence can confirm, revise,
  or reject.

  Assert:
  - The brief names the user, job, decision, dimensions, geography or segment,
    freshness bar, and local baseline.
  - Unknowns remain hypotheses rather than implied facts.

- [ ] **N2 — Build a broad, reproducible candidate pool.**
  `comparison contract -> query ledger + candidate pool | thin-market branch`

  Rule: Search product sites and the tracked review, Reddit, X, YouTube, forum,
  marketplace, and analyst surfaces with explicit product, alternative,
  complaint, switching, pricing, and workflow queries. Follow useful links and
  author trails instead of treating each platform as a single search result.

  Assert:
  - Every search surface has recorded queries, filters, dates, and result counts.
  - Discovery does not stop after the first plausible competitor or thread.

- [ ] **N3 — Promote only candidates that cross the evidence threshold.**
  `candidate pool -> finalists + rejection ledger | evidence-gap branch`

  Rule: Score relevance to the job, product activity, evidence diversity, and
  review volume. Investigate up to the highest-value `top-k`; `k` is a ceiling,
  never a quota for weak candidates.

  Example: `five candidates -> two pass job-fit and evidence thresholds -> two
  dossiers and three recorded rejections`.

  Assert:
  - Every finalist passes the stated threshold and every material rejection has
    a reason.
  - Syndicated, copied, affiliate, and vendor-authored evidence is deduplicated.

- [ ] **N4 — Investigate finalists in independent evidence lanes.**
  `finalists -> product dossiers + review-theme ledger | parallel-lane branch`

  Rule: When two or more finalists pass and bounded delegation is available,
  assign one lane per finalist in parallel. Each lane inspects official product
  behavior, pricing/access, review sites, Reddit threads and comments, X posts
  and linked demos, YouTube videos/transcripts/comments, and contrary evidence.
  Follow [platform review research](references/platform-review-research.md).

  Example: `Reddit complaint -> pricing hypothesis -> official pricing and
  switching-thread search -> complaint confirmed only for one segment`.

  Assert:
  - Each dossier includes direct sources, dates, observed behavior, recurring
    themes, illustrative evidence, counterevidence, and unresolved unknowns.
  - Anecdotes are not reported as prevalence without adequate independent data.

- [ ] **N5 — Convert convergence and divergence into a decision.**
  `dossiers + local baseline -> competitor intelligence brief`

  Rule: Separate table stakes, meaningful differentiation, recurring pain,
  underserved jobs, and noisy outliers. Trace every opportunity to customer
  evidence and the local product's ability to act.

  Assert:
  - The comparison distinguishes source fact, synthesis, and recommendation.
  - The brief recommends one opportunity, states its downside, and names the
    next owning workflow.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- A search-results page is discovery evidence, not proof of product behavior.
- Repeated copies of one complaint are one source lineage, not independent demand.
- Feature-count matrices hide the customer job; compare outcomes and failure
  modes before counting visible controls.

## Output

Return a `Competitor Intelligence Brief` with the decision contract, query
ledger, candidate and rejection ledger, finalist dossiers, source-linked
comparison, review themes with confidence, table stakes, differentiation,
opportunity, counterevidence, recommendation, and next owner.
