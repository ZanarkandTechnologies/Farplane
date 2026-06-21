---
title: Opportunity Scan Lane
owner: weekly-strategy-analysis
kind: lane-reference
---

# Opportunity Scan Lane

```text
opportunity_scan_lane(
  context_bundle,
  lane_output,
  goal_terms,
  people_org_terms,
  codex_work_terms,
  tracked_profiles_or_sources?,
  max_queries = 8,
  max_results = 12
) -> opportunity_candidates
```

Question: what public opportunities are worth considering given the private
week evidence?

## Routing

1. Use [feed-scout](../../feed-scout/SKILL.md) when tracked profiles, entities,
   or harness resources exist for relevant goals, people, or orgs.
2. Use bounded web search only when feed-scout has no configured source or the
   current meeting/Codex evidence introduces a new term.
3. Use [summarize](../../summarize/SKILL.md) for long articles, transcripts, or
   pages before judging fit.

## Search Strategy

Search order:

1. Named people/orgs from meetings: fresh updates, events, hiring, grants,
   partnerships, launches, talks, papers.
2. Active goal domains plus geography or market constraints.
3. Codex-work-derived terms: repos, framework releases, benchmark shifts,
   competitor launches, buyer pain, implementation patterns.
4. Current focus domains: industrial AI, healthcare AI, Malaysia/SEA
   manufacturing, medical devices, factory automation, edge vision, smart
   glasses/perception, robotics/VLA, knowledge graphs/business data, coding
   agents, finance/ops AI.

Deduplicate by canonical URL and cluster by opportunity thesis before judging
fit.

## Result Fields

Each candidate needs:

- `source_url`
- `source_date_or_observed_date`
- `why_now`
- `fit_to_goal`
- `fit_to_people_or_codex_evidence`
- `next_action`
- `displace_existing_priority?`
- `confidence`

Rules:

- Do not let public opportunity scanning dominate stronger obligations from
  tasks, meetings, or actual Codex work.
- Do not create tasks, CRM records, proposals, or public posts unless the
  automation wrapper explicitly enables writes.
- Reject items without links or evidence.
