---
ticket_id: TASK-9004
title: Ground creative references and functional UI research
status: done
priority: high
created_at: 2026-08-02T01:38:58+08:00
updated_at: 2026-08-02T02:30:00+08:00
---

# Ground creative references and functional UI research

## Summary

Turn the approved reference-source model into repeatable skill behavior: classify inspiration sources separately from rights, accept moodboard traits before generation, route landing-page media work through Asset Advisor when needed, browser-operate established UI references for material workflow design, and preserve curated landing-page taste through Resource Bank ingestion.

## Scope

- In: `asset-advisor`, `landing-page`, `functional-ui`, and a narrow `ingest-content` source-resolution rule.
- In: focused positive/negative eval rows, QA guards, generated skill metadata, and skill-local audit receipts.
- Out: changing `ad-advisor` or `content-impl-plan`; automating logins or bypassing public-source access limits; treating Pinterest or reference libraries as production licenses.

## Delta

- Before: discovery sources were mostly undifferentiated and rights notes could be conflated with how a source was used.
- After: every reference has an independent usage role and rights status; prompt compilation follows accepted transferable traits.
- Before: Landing Page could discover media without an explicit Asset Advisor boundary.
- After: missing/reference-led media routes to Asset Advisor; complete licensed inputs skip the route with provenance recorded.
- Before: Functional UI asked for comparable apps but did not require operating current products or preserve browser evidence.
- After: material unsettled workflows use browser-operated comparables and an adopt/adapt/reject receipt; Pinterest remains aesthetic evidence, not workflow proof.
- Before: an aggregator pin could become the durable source without attempting to resolve the original page.
- After: ingestion prefers the canonical original, preserves the discovery URL, and keeps unresolved pins inspiration-only with unknown rights.

## Program

1. Capture baseline behavior against natural reference-routing tasks.
2. Update first-load contracts, deeper reference files, QA checklists, and focused evals.
3. Run skill registry/link/config/eval validation and compare candidate behavior.
4. Obtain independent reviewer judgment and repair material findings.

## Map

- `skills/asset-advisor/`
- `skills/landing-page/`
- `skills/functional-ui/`
- `skills/ingest-content/`
- `docs/skills/registry.jsonl` (generated)
- `tickets/TASK-9004/artifacts/`

## Done / Proof

- [x] Asset Advisor records independent `usage_role` and `rights_status` and gates prompts on accepted moodboard traits.
- [x] Landing Page conditionally routes missing/reference-led media through Asset Advisor and has a documented skip path.
- [x] Functional UI browser-operates 2-4 established comparables for material unsettled workflows, records evidence and access limits, and excludes Pinterest from functional proof.
- [x] Ingest Content prefers canonical original landing pages while retaining discovery provenance and conservative rights treatment.
- [x] Positive and negative evals pass query-spoiler review and candidate evaluation.
- [x] `check_skills.py --write` regenerated valid registries and focused validators pass; aggregate surface-budget validation remains nonzero only on pre-existing `content-impl-plan` debt outside this ticket.
- [x] Independent reviewer returns TAS-A readiness; prior findings are repaired.

## State

- Current: implementation, install, QA, evals, and independent TAS-A review complete.
- Next: no implementation work remains. Local ticket packet is retained because GitHub issue creation, commit, push, and remote closeout were not requested.

## Links

- Learned video packet: `.farplane/learn-from-video/DZF8gItI1N/learned-video-packet.md`
- Reviewer receipt: `.farplane/learn-from-video/DZF8gItI1N/reviewer-receipt-v2.md`
- Browser operation QA: `tickets/TASK-9004/artifacts/browser-operation-qa.md`
- Browser operation best evidence: `tickets/TASK-9004/artifacts/pageflows-heygen-direct.png`
- Eval comparison: `tickets/TASK-9004/artifacts/eval-comparison.md`
- Independent reviewer: `tickets/TASK-9004/artifacts/reviewer-receipt.md`

## Notes

EvalExperimentExpectation:
  hypothesis: Explicit source roles, route gates, and browser receipts will prevent reference copying, unnecessary Asset Advisor calls, and vibe-only UI research.
  expected_observation: Candidate responses satisfy the new focused reference points while retaining existing skill behavior.
  observation_horizon: One baseline and one candidate pass across changed skill-local rows.
  confidence: medium
  falsifier: Candidate misses a required route/skip boundary or treats aesthetic aggregators as rights-cleared production/workflow evidence.
  surprise_trigger: Candidate passes every new row without mentioning any new contract behavior, or materially regresses an existing row.
  surprise_route: agent-qa-test:experiment
