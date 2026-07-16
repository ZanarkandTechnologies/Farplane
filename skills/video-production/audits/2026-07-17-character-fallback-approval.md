---
title: Character fallback approval hardening
owner: video-production
status: passed
kind: skill-audit
created_at: 2026-07-17
edited_skills:
  - video-production
  - storyboard
evidence_ref: tickets/TASK-0378/artifacts/whole-short-v1/identity-review-correction.md
---

# Character Fallback Approval Hardening

## Behavior Delta

```text
before:
  A provider-safe motion fallback could be reviewed as a narrow proof, then
  silently become the production character reference while inheriting the
  original storyboard approval.
after:
  Character identity is a hashed storyboard approval asset. Any fallback that
  changes visible identity invalidates affected approvals and returns the
  revised character card and scene grids for explicit operator feedback.
example:
  Human everyperson rejected by privacy detector -> helmeted mannequin may
  prove motion only -> production remains blocked until a same-character safe
  variant and affected grids are reviewed.
```

## Owner Placement

- `video-production/SKILL.md`: first-load approval-invalidation gate.
- `scene-grid-production.md`: packet fields, input/hash check, and reapproval
  contract.
- Retro profile package: canonical recurring character asset and proof-only
  fallback boundary.
- `storyboard`: character card appears in the minimum visual feedback packet.
- QA/evals: runtime guardrails and regression prompts cover the failure.

## Proof

- Canonical character identity sheet is collocated with the style profile and
  hash-bound by its manifest.
- Both changed eval files parse as JSON.
- Video-production and storyboard QA wording matches the new first-load gate.
- `check_skills.py --write` passes, including registry, template, capability,
  config, eval-query, reference, and 24 enrolled skill-surface checks.
- Initial targeted semantic evals correctly failed at `C` / pass rate `0.0`:
  they exposed missing canonical preservation, versioned fallback, unaffected
  scene locking, and approval-to-provider envelope fields. Those findings were
  applied.
- Replacement semantic evals both pass at verdict `A` / pass rate `1.0`:
  - `.farplane/evals/runs/20260716-175348-character-fallback-storyboard-rerun-20260717/`
  - `.farplane/evals/runs/20260716-175516-character-fallback-video-rerun-20260717/`
- The scene-grid contract now defines one stable identity vocabulary, a
  checkable `approved.json`, a local generation envelope, and a preflight
  receipt joining approval hashes to exact provider `reference_images`.
- Independent rereview is required before commit.
