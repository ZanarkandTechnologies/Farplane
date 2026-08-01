---
skill: agency-opportunity-research
date: 2026-07-12
change_type: structure
owner: skill-creator
status: pass
review_route: reviewer
before_ref: Valefor/.agents/skills/agency-opportunity-research/SKILL.md
after_ref: skills/agency-opportunity-research/SKILL.md
reasoning_basis: reviewer
proof_artifacts:
  - skills/agency-opportunity-research/evals/evals.json
  - skills/agency-opportunity-research/examples/data-center-construction/example.md
  - crm-2.0.3-behavior-smoke
eval_required: yes
---

# Agency Opportunity Research Promotion Audit

## Change

- Promoted the project-proven opportunity pipeline into a reusable Farplane
  skill with generic agency wording and configurable usecase roots.
- Adopted CRM 2.0.3 entity Markdown: structured frontmatter, durable body
  context, report/source links, exact-delta approval, and compiler ownership.
- Removed Valefor/Yevon/DemoHub runtime dependencies from the reusable contract.

## Proof

- `quick_validate.py`: pass.
- Skill registry, todo tiers, eval query lint, doc refs, capabilities, and
  surface-budget checks: pass.
- CRM compiler tests: 4/4 pass.
- Behavior smoke: body context used without becoming unsourced fact;
  frontmatter/body delta separated; generated JSON never hand-edited.
- Installed-copy comparison: source and live installed package match after
  final reinstall.

## Review

- Initial TAS-B found project leakage, stale eval paths, and wrong report root.
- Repairs changed the group to `research`, set the report root to
  `.farplane/agency-opportunity-research/reports/`, made routes generic, and
  localized eval refs to `skills/`.
- `no_self_improve_reason`: run the first real multi-company OpportunityCase
  before creating a measured optimization loop.
