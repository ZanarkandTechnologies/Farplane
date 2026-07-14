---
kind: feed-scout-memory
status: active
updated_at: 2026-07-14T08:00:00Z
canonical_icp_ref: farplane/harness.yaml#areas
source_ledger: eval-fixture://feed-scout/ledger
last_report_ref: eval-fixture://feed-scout/2026-07-14
---

# Feed Scout Memory

This clean-room fixture represents current, update-in-place synthesis for the
planner eval. It is not a daily log or snapshot archive. It is evidence, not
planning authority.

## ICPs

### `framework_delivery` — Harness engineers

- Canonical ref: `farplane/harness.yaml#areas.framework_delivery.icp`
- Description: Engineers building reliable coding-agent and long-running agent workflows who need visible state, recovery, evaluation, and proof.
- Jobs to be done: Make agents run longer and recover with less supervision. Decide which harness components earn their complexity.
- Pain points: Agent workflows that look autonomous but silently stall or drift. Framework claims without reproducible comparisons or working artifacts.
- Evidence bar: A runnable product surface or fair with/without comparison that changes an implementation decision against a named baseline.
- Current concerns: Recovery and proof completeness remain the most relevant surfaces for the supplied comparison.
- Current language: recovery, supervision, proof completeness.
- Source refs: `eval-fixture://feed-scout/2026-07-14#long-running-agent-claims`

### `customer_learning` — Agent and harness builders evaluating adoption

- Canonical ref: `farplane/harness.yaml#areas.customer_learning.icp`
- Description: Serious builders deciding whether Farplane solves a costly orchestration, proof, or long-running-work problem better than their current scripts.
- Jobs to be done: Identify which Farplane workflow is worth adopting now. Compare Farplane with an existing manual or framework baseline.
- Pain points: Broad AI research that does not change a product or adoption decision. Missing evidence about migration cost, reliability, or realized value.
- Evidence bar: Source-backed learning tied to a named decision, alternative, and immediate product, sales, demo, or experiment use.
- Current concerns: The supplied evidence supports testing a named manual baseline, not making a broad autonomy claim.
- Current language: manual baseline, recovery cost, implementation decision.
- Source refs: `eval-fixture://feed-scout/2026-07-14#long-running-agent-claims`

### `adoption_and_distribution` — Technical agent builders who share and adopt proven patterns

- Canonical ref: `farplane/harness.yaml#areas.adoption_and_distribution.icp`
- Description: Harness and agent engineers who pay attention to surprising, reproducible knowledge and credible demonstrations rather than generic AI commentary.
- Jobs to be done: Learn a game-changing harness technique they can reproduce. See enough proof to try Farplane on a real project.
- Pain points: Shallow trend summaries and product marketing without technical evidence. Demos that hide the baseline, failure mode, or reusable method.
- Evidence bar: A proof-led artifact with a named baseline, observed delta, reusable method, and honest limit that can survive expert scrutiny.
- Current concerns: Builders are discussing long-running agents but distrust autonomy claims that omit a baseline, recovery evidence, or supervision cost.
- Current language: long-running agents, recovery, supervision turns, proof completeness.
- Source refs: `eval-fixture://feed-scout/2026-07-14#long-running-agent-claims`

### `self_improvement` — Farplane operators and harness maintainers

- Canonical ref: `farplane/harness.yaml#areas.self_improvement.icp`
- Description: Operators responsible for keeping autonomous work useful, reviewable, and productive while human attention is unavailable.
- Jobs to be done: Prevent recurring stalls, shallow planning, and unnecessary intervention. Improve the harness from measured failures and accepted outcomes.
- Pain points: One-off cleanup mislabeled as compounding improvement. Prompt or workflow changes shipped without representative next-run proof.
- Evidence bar: A causal before/after eval or reproduced production-path run proving a durable preventive mechanism, with rollback or rejection criteria.
- Current concerns: No distinct internal failure is supplied in this fixture; do not invent a self-improvement candidate.
- Current language: representative proof, preventive mechanism.
- Source refs: `farplane/harness.yaml#areas.self_improvement.icp`

## Trends

### Long-running agent claims are being challenged on control and recovery

- ICP refs: `adoption_and_distribution`
- Current synthesis: Technical builders are interested in longer-running agents while asking how they recover, how much supervision remains, and what evidence makes autonomy claims credible.
- Why it matters: A useful artifact must compare a concrete harness method against the current manual default instead of repeating the trend label.
- Baseline or default: Manually maintained task files with no durable recovery or proof-completeness contract.
- Last observed: 2026-07-14
- Confidence: medium
- Source refs: `eval-fixture://feed-scout/2026-07-14#long-running-agent-claims`
- Candidate experiment shapes: Compare ticket-backed and manual-task-file runs on recovery, supervision turns, and proof completeness.

## Other Notable Things

### Generic agent-future content does not clear the evidence bar

- Type: constraint
- ICP refs: `adoption_and_distribution`
- Note: A trend-themed video without a baseline or reproducible result is unlikely to change an expert implementation decision.
- Last observed: 2026-07-14
- Source refs: `eval-fixture://feed-scout/2026-07-14#long-running-agent-claims`

## Source Gaps

- The fixture does not establish downstream distribution response; the admitted ticket must treat publication as a later human gate and either measure only same-run evidence or configure a delayed check-in.
