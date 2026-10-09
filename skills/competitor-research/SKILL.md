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

- [ ] **N3 — Qualify and classify candidates before comparison.**
  `candidate pool -> qualification ledger + finalists + rejection ledger | evidence-gap branch`

  Rule: Open and operate each candidate's official site before promotion; a
  search result or snippet discovers a candidate but never proves a
  qualification field. Record dated direct observations for target geography
  and actual market availability; current product availability and production
  status; relevant offering breadth/depth; operating recency; website freshness;
  social activity and engagement; estimated traffic or a defensible demand
  proxy; customer/review evidence; organizational credibility; and same-customer-
  job fit. Classify every candidate as `direct competitor`, `adjacent
  competitor`, `supplier`, `inactive/noise`, or `unverified`, with confidence.
  Choose exactly one primary class; record secondary relationships separately.

  Promotion threshold: a competitive-threat claim requires all four mandatory
  gates—same customer job, target geography served, currently obtainable and
  meaningfully in production, and more than an incidental relevant SKU—plus a
  current official observation and at least two independent demand, customer,
  operating, or organizational evidence lineages. Missing or conflicting
  mandatory evidence means `unverified` or rejection, never assumed passage.
  Investigate up to the highest-value `top-k`; `k` is a ceiling, never a quota.

  Example: `a local distributor with one backordered robot-arm SKU -> supplier
  or adjacent, not direct threat; geography or production unresolved ->
  unverified and recorded in the rejection ledger`.

  Assert:
  - Every finalist has direct-site observations for all qualification fields,
    passes every mandatory gate, and states threshold evidence and confidence.
  - The ledger keeps rejected and unverified candidates with failed or unknown
    fields, source URLs, inspection dates, and reasons; no blank is scored as a pass.
    Use one row per candidate and qualification field with `pass`, `fail`, or
    `unknown`; cite the source and observation date in that row.
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
- A matching SKU, local domain, reseller page, or search-indexed location claim
  does not establish geography, production, offering depth, or competitive threat.
- Repeated copies of one complaint are one source lineage, not independent demand.
- Feature-count matrices hide the customer job; compare outcomes and failure
  modes before counting visible controls.

## Output

Return a `Competitor Intelligence Brief` with the decision contract, query
ledger, candidate qualification ledger (classification, field evidence, unknowns,
and confidence), rejection ledger, finalist dossiers, source-linked comparison,
review themes with confidence, table stakes, differentiation, opportunity,
counterevidence, recommendation, and next owner. Label any competitive-threat
claim with the passed threshold evidence; otherwise report the candidate as
adjacent, supplier, inactive/noise, or unverified.

The qualification ledger is required even when every candidate is rejected. It
must enumerate every N3 field rather than summarize them in prose. The rejection
ledger must name the failed or unknown mandatory gates, one primary class, and
confidence for each candidate that was not promoted.
