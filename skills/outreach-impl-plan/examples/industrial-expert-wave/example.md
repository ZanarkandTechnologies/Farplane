---
skill: outreach-impl-plan
kind: outreach-campaign
campaign_id: industrial-readiness-expert-wave
name: Industrial Readiness Expert Wave
state: awaiting_approval
created_at: 2026-07-15
entity_refs: []
source_refs:
  - skills/outreach-impl-plan/examples/industrial-expert-wave/synthetic-candidate-packet.md
---

# Outreach Campaign: Industrial Readiness Expert Wave

> Synthetic example. People, companies, and sources are fictional.

## Summary

- Objective: earn three expert corrections and validate whether evidence
  readiness is a recurring decision problem before proposing a pilot.
- Audience: two hands-on commissioning practitioners and one digital-delivery
  community leader.
- Relationship strategies: `learn_from`, then `partner_or_jv` only if the
  recipient validates a collaboration direction.
- Review point: after three approved sends or two replies, whichever comes
  first.

## Waves

| Wave | Shared hypothesis | Candidates | Entry | Exit / promotion | Review point | Stop |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | Practitioners can falsify the readiness model fastest | Alex, Priya | Current public role and access route verified; contribution packet accepted | Two corrections promote the corrected field note; both stopped ends the wave | After every reply and after two send-or-stop receipts | No useful correction after bounded follow-up |
| 2 | Community translation matters only after practitioner correction | Dana | Wave 1 review approves a corrected field note and community question | One community correction or explicit distribution interest | Before any contribution build and after the first response | Wave 1 rejects the premise |

### Metric Linkage IDs

- `campaign_id`: `industrial-readiness-expert-wave`
- canonical `person_id` values: `alex-rowan`, `priya-sen`, `dana-ortiz`
- Wave 1 interaction `offer_id` values: `fv-alex-readiness-v1` and
  `fv-priya-retest-v1`

The interaction IDs attribute first-value bundles; they do not assert a
commercial offer or CRM opportunity.

## Advisor Action List

| Order | Wave | Target | Owner | Input | Output | Acceptance check | Blocker | Approval gate | Evidence writeback |
| ---: | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | Alex | `customer-research` | synthetic candidate packet | person report | current role and one traceable signal | stale role | local research approved | person report and stage `researching` |
| 2 | 1 | Alex | `first-value-outreach` | person report | readiness-map packet with `offer_id: fv-alex-readiness-v1` | standalone value and one correction ask | no supported signal | production approved | contribution report and stage `contribution_planned` |
| 3 | 1 | Alex | `copywriting-advisor` | contribution packet | unsent DM | source-bounded and under 100 words | artifact incomplete | message review only | message artifact and stage `send_review` |
| 4 | 1 | Priya | `customer-research` | synthetic candidate packet | person report | current role and one traceable signal | stale role | local research approved | person report and stage `researching` |
| 5 | 1 | Priya | `first-value-outreach` | person report | retest-window packet with `offer_id: fv-priya-retest-v1` | standalone value and one correction ask | no supported signal | production approved | contribution report and stage `contribution_planned` |
| 6 | 1 | Priya | `copywriting-advisor` | contribution packet | unsent DM | source-bounded and under 100 words | artifact incomplete | message review only | message artifact and stage `send_review` |
| 7 | 1 | Alex and Priya | `review` | exact person, artifact, message, channel, and source refs | per-person `send | revise | stop` verdicts | source, value, limits, and exact-send boundary pass | any QA failure | operator reviews exact bundle; send still unapproved | per-person review receipts |
| 8 | 1 | each approved person | operator-approved sender | exact approved person + artifact + message + channel | `send_receipt | stopped_receipt` | receipt binds campaign, person, `offer_id`, channel, timestamp, and approved bundle | approval missing or route unavailable | separate operator approval for that exact send | receipt, stage `sent | stopped`, and eligible `outreach_sent` event input |
| 9 | 1 | campaign | `customer-acquisition-metrics` | receipts/replies with campaign, person, and `offer_id` linkage | append-only events and observations | only evidenced actions recorded; source gaps stay unknown | no receipt or unsupported event | local recording approval where required | acquisition ledger and observation artifact |
| 10 | review | campaign | `review` | Wave 1 receipts, replies, corrections, and observations | `expand | revise | pause | stop` verdict | falsifiers and Wave 2 changes explicit | review trigger not met and no decisive falsifier | campaign review approval | Wave 1 review receipt and revised campaign state |
| 11 | 2 | Dana | `outreach-impl-plan` | approved Wave 1 review plus Dana fixture evidence | revised future Wave 2 action rows only | rows use corrected practitioner learning and preserve a distinct community hypothesis; no child work starts | Wave 1 rejects premise or corrected field note is missing | separate Wave 2 admission; later child-work and exact-send approvals | updated example campaign artifact with revised Wave 2 rows |

## CRM Proposal — Not Applied

Create sourced `person` and `company` entities for accepted Wave 1 research.
Do not create an opportunity until a recipient validates a recurring problem or
collaboration direction. Campaign stages remain in this artifact.

## Campaign Lock

- Grounded thesis: pass — synthetic candidate packet cited.
- Learning-sized first wave: pass — two practitioners before community scale.
- Advisor program: pass — both Wave 1 people have complete action paths,
  including evidence writeback, send-or-stop receipts, and metric linkage IDs.
- Permissions: pass — campaign approval does not authorize CRM writes or sends.
