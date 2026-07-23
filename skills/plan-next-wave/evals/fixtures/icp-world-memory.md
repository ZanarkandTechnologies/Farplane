---
kind: feed-scout-world-memory
status: active
updated_at: 2026-07-14T08:00:00Z
canonical_icp_ref: farplane/harness.yaml#areas
source_ledger: eval-fixture://feed-scout/ledger
last_report_ref: eval-fixture://feed-scout/2026-07-14
---

# Feed Scout World Memory

Current update-in-place synthesis for planner evals, not a daily log, snapshot
archive, or planning authority. Keep under 100 non-empty lines; full ICP truth
lives in `farplane/harness.yaml#areas`.

## ICPs

- `framework_delivery` — Harness engineers | ref=`farplane/harness.yaml#areas.framework_delivery.icp` | concerns=recovery and proof completeness | language=recovery, supervision, proof completeness | refs=`eval-fixture://feed-scout/2026-07-14#long-running-agent-claims`
- `customer_learning` — Agent and harness builders evaluating adoption | ref=`farplane/harness.yaml#areas.customer_learning.icp` | concerns=test a named manual baseline, not broad autonomy | language=manual baseline, recovery cost, implementation decision | refs=`eval-fixture://feed-scout/2026-07-14#long-running-agent-claims`
- `adoption_and_distribution` — Technical agent builders who share and adopt proven patterns | ref=`farplane/harness.yaml#areas.adoption_and_distribution.icp` | concerns=builders distrust autonomy claims without baseline, recovery evidence, or supervision cost | language=long-running agents, recovery, supervision turns | refs=`eval-fixture://feed-scout/2026-07-14#long-running-agent-claims`
- `self_improvement` — Farplane operators and harness maintainers | ref=`farplane/harness.yaml#areas.self_improvement.icp` | concerns=no distinct internal failure supplied; do not invent self-improvement work | language=representative proof, preventive mechanism | refs=`farplane/harness.yaml#areas.self_improvement.icp`

## Trends

- observed | icp=adoption_and_distribution | claim=Technical builders are interested in longer-running agents but ask about recovery, supervision, and credible autonomy proof | use=make matched recovery comparison and runnable proof central to the candidate | seen=2026-07-14 | conf=medium | refs=`eval-fixture://feed-scout/2026-07-14#long-running-agent-claims`

## Other Notable Things

- observed | type=constraint | icp=adoption_and_distribution | note=Trend-themed content without a baseline or reproducible result will not change expert implementation decisions | use=reject generic content and require matched comparison proof | seen=2026-07-14 | refs=`eval-fixture://feed-scout/2026-07-14#long-running-agent-claims`

## Source Gaps

- The fixture does not establish downstream distribution response; admitted work must treat publication as a later human gate.
