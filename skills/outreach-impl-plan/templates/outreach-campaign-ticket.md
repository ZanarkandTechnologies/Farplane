---
skill: outreach-impl-plan
kind: outreach-campaign
campaign_id: "{{ campaign_id }}"
name: "{{ campaign_name }}"
state: "draft"
created_at: "{{ YYYY-MM-DD }}"
entity_refs: []
source_refs: []
---

# Outreach Campaign: {{ Campaign Name }}

## Summary

- Objective:
- Audience:
- Relationship strategies:
- Campaign promise / contribution thesis:
- Learning question:
- Why now:
- Review point:

## Scope

- In:
- Out:
- Geography / segment:
- Channels:
- Creator budget:
- Recipient effort cap:
- External spend:

## Delta

- Before:
- After:
- Why now:
- Assumptions:
- Falsifiers:

## Program

### Campaign Thesis And Success Evidence

- Value hypothesis:
- Evidence already available:
- Evidence that would validate the campaign:
- Evidence that would revise it:
- Campaign stop condition:

### Waves

| Wave | Shared hypothesis | Candidates | Entry | Exit / promotion | Review point | Stop |
| ---: | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |

### Advisor Action List

| Order | Wave | Target / cohort | Owner | Input | Output | Acceptance check | Blocker | Approval gate | Evidence writeback |
| ---: | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |  |  |

### Contribution And Offer Map

| Candidate | Relationship | Professional signal | First contribution | Interaction / offer ID | Optional proof / demo reason | Validated-offer route | Stop condition |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |  |  |

## CRM Materialization Proposal — Not Applied

| Entity ID | Kind | Proposed action | Sourced fields | Body context | Evidence | Approval status |
| --- | --- | --- | --- | --- | --- | --- |
|  | `person | company | opportunity` | `create | update | none` |  |  |  | `proposed` |

Campaign queue stages remain in this campaign artifact. Do not create an
opportunity merely because a candidate is included. Applying an approved delta
requires editing canonical entity Markdown and running `farplane entities compile`;
never edit generated CRM JSON directly.

## State And Measurement

- Candidate stages: `queued | researching | contribution_planned |
  contribution_ready | send_review | sent | replied | validated | stopped`
- Campaign observations:
- Per-wave observations:
- Metric linkage IDs: stable `campaign_id`, canonical `person_id`, and opaque
  interaction `offer_id` for every planned send/reply event. A first-value
  interaction ID is attribution only, not a commercial-offer claim.
- Send action contract: after per-person review and before metrics, require the
  exact approved person + artifact + message + channel as input and a
  `send_receipt | stopped_receipt` as output.
- Evidence owner:
- Review cadence:
- Decision after review:

## Campaign Lock

| Gate | Verdict | Evidence / blocker |
| --- | --- | --- |
| Grounded thesis |  |  |
| Learning-sized first wave |  |  |
| Executable advisor actions |  |  |
| Personalized contribution routes |  |  |
| CRM proposal restrained |  |  |
| Metrics beyond activity |  |  |
| Stop and review rules |  |  |
| Permissions separated |  |  |

## Done / Proof

- Plan ready when:
- Campaign admitted when:
- Wave 1 ready when:
- Review required:
- Evidence paths:
- Residual risk:

## Approval Inventory

| Action | Current status | Exact approval needed |
| --- | --- | --- |
| Campaign plan | `draft | approved` |  |
| CRM materialization | `proposed | approved | applied` |  |
| Research | `planned | approved | complete` |  |
| Contribution production | `planned | approved | complete` |  |
| Exact sends | `not_approved | approved | sent` |  |
| Publishing / tagging | `not_approved | approved | published` |  |
| Spend / enrichment | `not_approved | approved | spent` |  |
| Proposal / promise | `not_approved | approved | made` |  |

## State

`draft | awaiting_approval | approved | active | learning | paused | completed | blocked`

## Links

- Opportunity research:
- Candidate packet:
- Customer research:
- Contributions:
- Offers / proof:
- CRM:
- Metrics:
- Review:

## Notes

- Rejected campaign shapes:
- Evidence gaps:
- Next action:
