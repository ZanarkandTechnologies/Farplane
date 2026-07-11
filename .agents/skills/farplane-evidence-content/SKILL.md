---
name: farplane-evidence-content
description: "Turn accepted Farplane evidence into trust-building content when distributing proof or learning."
tier: 3
source: local
group: capability
template_uses:
  skill-template: "0.3.2"
---

# Farplane Evidence Content

## Context

Use this project-local capability when accepted Farplane evidence should become
a post, demo, launch note, paper, video, case study, or educational artifact.
Distribution must be grounded in proof, user pain, or a real adoption gap; it
must not market unproven claims.

## Skill Signature

```text
farplane_evidence_content(evidence_refs, audience, channel?, content_goal?, ticket?)
  -> content_brief + draft_or_handoff + proof_refs
state: reads(farplane/harness.yaml, farplane/metrics.yaml, evidence refs, ticket context); writes(content brief, draft, or ticket artifact)
gates: evidence_refs_present; audience_named; claim_strength_matches_proof; publish_requires_approval
routes: root skill `social-content` | root skill `video-production` | root skill `doc-advisor` | root skill `research`
fails: invents metrics; markets unproven claims; publishes without authorization
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Read the evidence and name the concrete pain, claim, or learning.
- [ ] 2. Name the audience, channel, and smallest useful content artifact.
- [ ] 3. Draft with observed evidence separated from interpretation.
- [ ] 4. Map every main claim to its proof reference.
- [ ] 5. Keep publish, outreach, spend, and account mutation approval-gated.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

- Content brief and draft or handoff path.
- Evidence refs supporting every main claim.
- Approval-required final actions.
