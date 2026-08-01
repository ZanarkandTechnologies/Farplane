---
skill: personalized-offer
date: 2026-07-12
change_type: structure
owner: skill-creator
status: pass
review_route: reviewer
before_ref: Valefor/.agents/skills/personalized-offer/SKILL.md
after_ref: skills/personalized-offer/SKILL.md
reasoning_basis: reviewer
proof_artifacts:
  - skills/personalized-offer/evals/evals.json
  - skills/personalized-offer/examples/operations-leader/example.md
  - crm-2.0.3-behavior-smoke
eval_required: yes
---

# Personalized Offer Promotion Audit

## Change

- Promoted the project-proven personalized offer workflow into a reusable
  Farplane skill with generic agency wording and configurable usecase roots.
- Adopted CRM 2.0.3 frontmatter/body semantics while keeping full research,
  offer reports, and outreach drafts in linked skill-owned reports.
- Preserved privacy, proof-integrity, exact CRM-delta approval, and unsent-copy
  gates.

## Proof

- `quick_validate.py`: pass.
- Grounded-person and privacy-pressure behavior smokes: pass.
- Skill registry, eval query lint, doc refs, and structural checks: pass.
- CRM compiler tests: 4/4 pass.
- Installed-copy comparison: source and live installed package match after
  final reinstall.

## Review

- Initial TAS-B found project leakage and stale `.agents/skills` eval paths.
- Repairs changed the group to `marketing`, removed project-name wording, and
  localized eval refs to the Farplane `skills/` source tree.
- `no_self_improve_reason`: use the first operator-reviewed real offer as the
  baseline before starting a recurring quality optimization loop.
