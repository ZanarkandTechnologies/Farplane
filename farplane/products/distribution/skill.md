---
name: farplane-evidence-content
description: "Turn accepted Farplane evidence into trust-building content when distributing proof, learnings, or product progress."
tier: 3
source: local
group: product
template_uses:
  skill-template: "0.3.2"
---

# Farplane Evidence Content

## Context

Use this project-local skill when Farplane should turn accepted evidence into
distribution: posts, demos, launch notes, papers, videos, case studies, or
educational content.

Distribution must be grounded in proof, user pain, or a real adoption gap. It
should not market unproven claims.

## Skill Signature

```text
farplane_evidence_content(evidence_refs, audience, channel?, content_goal?, ticket?)
  -> content_brief + draft_or_handoff + proof_refs
state: reads(farplane/harness.md, farplane/products/distribution/product.md, generated product indexes, evidence refs, ticket context); writes(content brief, draft, or ticket artifact)
gates: evidence_refs_present; audience_named; claim_strength_matches_proof; packet_claim_safety_review_for_multi_artifact_or_metric_scaffold; publish_requires_approval
routes: root skill `social-content` | root skill `video-production` | root skill `documentation` | root skill `research`
fails: invents metrics; markets unproven claims; advances multi-artifact or metric-capture packet to human review or final distribution action without packet-level claim-safety review receipt; publishes without authorization
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the evidence and audience.
  - [ ] Read the evidence refs and identify the concrete pain, claim, or
    learning.
  - [ ] Name the target audience and channel when known.
- [ ] 2. Choose the content artifact.
  - [ ] Pick the smallest artifact that can communicate the evidence clearly.
  - [ ] Use social, video, documentation, or research skills only when that
    artifact needs their workflow.
- [ ] 3. Draft the content.
  - [ ] Separate observed evidence from interpretation.
  - [ ] Keep claims no stronger than the proof.
- [ ] 4. Prepare review.
  - [ ] For multi-artifact packets or packets with metric-capture
    scaffolding, write a packet-level claim-safety review receipt before human
    review or any final distribution action.
  - [ ] In that receipt, check source refs, caveats, metric honesty,
    final-action gates, and prioritized human-review readiness across the
    packet.
  - [ ] Mark publish, external outreach, spend, or account mutation as
    approval-required unless already authorized by ticket policy.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

- Content brief and draft or handoff path.
- Evidence refs supporting every main claim.
- Packet-level claim-safety review receipt when the packet has multiple local
  artifacts or metric-capture scaffolding.
- Approval-required publish steps.
