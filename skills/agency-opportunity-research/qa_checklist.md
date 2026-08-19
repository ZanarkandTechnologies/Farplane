---
title: Agency Opportunity Research QA Checklist
owner: agency-opportunity-research
status: active
kind: qa-checklist
applies_to:
  - opportunity-cases
  - target-and-offer research
---

# Agency Opportunity Research QA Checklist

Read this before running the skill and apply it again to the finished
OpportunityCase. For material cases, ask an independent reviewer to try to
reject the artifact.

```text
opportunity_case_check(case) -> pass | violation | deferral
```

## Checks

1. **Bounded intake**
   - Pass: intake type, objective, market/value-chain boundary, geography,
     exclusions, and evidence budget are explicit.
   - Violation: research silently expands into an unbounded industry scan.
2. **Traceable entities and claims**
   - Pass: shortlisted entities use stable IDs; material claims retain source,
     observation date/freshness, provenance label, and confidence.
   - Violation: a company, person, pain, or relationship claim cannot be traced.
3. **Relationship strategy**
   - Pass: each shortlisted target is classified as sell-to, partner/JV,
     channel, data/delivery partner, learn-from, or uncertain with rationale.
   - Violation: different relationship types are hidden behind one lead score.
4. **Honest problem grounding**
   - Pass: each proposed offer traces to actor, job/decision, stakes,
     constraints, source status, problem hypothesis, and correction question.
   - Violation: role stereotypes or inferred private pains are written as fact.
5. **Competitor and capability context**
   - Pass: a dated, criteria-bounded established benchmark and credible emerging
     specialist are compared with the agency/custom path on equal buyer-choice
     fields, including honest limitations, choose-when guidance, gap hypothesis,
     and falsifier. Any customer-facing conclusion goes directly into the demo
     landing as a semantic feature matrix with capabilities as rows and
     providers as columns rather than vendor-summary rows or side-by-side cards;
     cells distinguish documented, demonstrated here, and not shown in reviewed
     public material; a
     deeper landscape file exists only when reuse justifies it.
   - Violation: “best” is unsupported, the agency wins every field, evidence is
     stale or missing, vendor-summary rows or cards obscure feature comparison,
     unsupported absence claims are presented as fact, or a buyer-choice
     sidecar duplicates the landing page.
   - Deferral: the exact research method and evidence gap are named.
6. **Composition without duplication**
   - Pass: child skills own discovery, research, brainstorming, solution
     shaping, experiments, and packaging; the case stores outputs and links.
   - Violation: the pipeline copies a child skill's full method or hides which
     owner produced a judgment.
7. **Proof fit**
   - Pass: existing usecases were checked, proof type and claim are explicit,
     and a polished demo is required only when it helps the target decision.
   - Violation: every opportunity is forced into a new polished demo page.
8. **Graph without premature infrastructure**
   - Pass: records have stable IDs, typed relationships, temporal/source data,
     and confidence revisions without choosing an unapproved database schema.
   - Violation: the research pass silently commits the project to graph storage or
     map implementation.
9. **External-action gates**
   - Pass: outreach, enrichment, private data, public publishing, deploys,
     account mutations, and commitments remain approval gated; Wiki publication
     follows its separate `preview | apply` intent.
   - Violation: an external side effect occurs or is implied without evidence.
10. **Actionable handoff**
    - Pass: research gaps, next action, next owner, handoff inputs, and the
      evidence that would change the recommendation are named.
    - Violation: the result is an interesting report with no decision path.
11. **Wiki writeback**
    - Pass: proposed entity changes separate structured frontmatter from concise
      durable Markdown-body context, link full reports, and route sourced facts
      plus publication intent through `manage-wiki`; ordinary research previews,
      direct Wiki write intent applies without a second exact-delta approval,
      and privacy or ambiguity still blocks.
    - Violation: generated JSON is hand-edited, entity bodies become report
      dumps, or useful unstructured relationship context is discarded.

## Reviewer Output

Return each failed check with `violation | deferral`, exact artifact evidence,
the smallest repair, and an overall `pass | revise | block` verdict.
