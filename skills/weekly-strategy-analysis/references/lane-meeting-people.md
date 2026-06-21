---
title: Meeting People Lane
owner: weekly-strategy-analysis
kind: lane-reference
---

# Meeting People Lane

```text
meeting_people_lane(context_bundle, lane_output)
  -> commitments + relationship_leverage + crm_pkm_candidates
```

Question: what relationship, commitment, and personal-CRM updates did the week
create?

Track:

- meetings by person/org.
- repeated contacts and high-leverage relationships.
- commitments made, commitments received, follow-ups, blockers, and open loops.
- opportunity clusters by person/org.
- plan changes caused by calls, especially unfinished tasks that became correct
  because the conversation changed the strategy.
- people/org records to create, backfill, or update in the personal CRM/PKM.

Rules:

- Propose CRM/PKM mutations only. Do not write unless the automation wrapper
  explicitly enables mutation.
- Do not include private contact details in durable reports.
- Cite meeting rows or raw source pointers for every commitment.

Output:

- `relationship_moves`: person/org, why it matters, next action, date.
- `commitments`: owner, commitment, source, due date or inferred date.
- `crm_pkm_candidates`: create/backfill/update, evidence, safe fields only.
- source gaps and rejected claims.
