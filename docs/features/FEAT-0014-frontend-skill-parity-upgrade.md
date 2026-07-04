---
title: Frontend skill parity upgrade
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-07-05
tags:
  - farplane
  - feature
  - sys-0010
refs:
  - skills/frontend-craft
  - skills/frontend-design
  - skills/visual-design
  - skills/delegate-frontend
  - skills/visual-qa
  - skills/landing-page
  - "docs/MEMORY.md#MEM-0085"
  - docs/HISTORY.md
feature_id: FEAT-0014
system_id: SYS-0010
category: frontend-skills
public: true
surfaces:
  - skills/frontend-craft
  - skills/frontend-design
  - skills/visual-design
  - skills/delegate-frontend
  - skills/visual-qa
  - skills/landing-page
source_refs:
  - "docs/MEMORY.md#MEM-0085"
external_refs:
  - https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/main/.claude/skills
  - https://github.com/Leonxlnx/taste-skill/blob/main/skills/taste-skill/SKILL.md
  - https://ui.shadcn.com/docs/mcp
  - https://ui.shadcn.com/docs/cli
  - https://ui.shadcn.com/docs/components-json
  - https://ui.shadcn.com/r/registries.json
evidence_refs:
  - skills/frontend-craft/SKILL.md
  - skills/frontend-design/SKILL.md
  - skills/visual-design/SKILL.md
  - skills/visual-qa/SKILL.md
  - docs/HISTORY.md
known_limits: Docs/skill-contract upgrade only; no automated eval suite or searchable frontend rule corpus yet.
metrics:
  - frontend_skill_prebuild_completeness_rate
  - generic_ui_regression_rate
last_verified: 2026-05-11
---
# Frontend skill parity upgrade

Frontend skill parity upgrade exists to keep Farplane frontend skills aligned with
modern UI craft, QA, and delegation patterns. It belongs to [Domain Skill
Families](../systems/domain-skill-families.md) and keeps `FEAT-0014` as a stable
capability handle because the behavior has an owner, proof path, and maintenance
boundary.

```text
frontend_skill_upgrade(skill, parity_evidence) -> guidance_delta + proof_gate
```

## At A Glance

- Feature ID: `FEAT-0014`
- System: [Domain Skill Families](../systems/domain-skill-families.md)
- Status: `implemented`
- Category: `frontend-skills`
- Primary user: frontend builder, reviewer, and skill maintainer
- Job: keep Farplane frontend skills aligned with modern UI craft, QA, and delegation patterns.

## Problem

Frontend work is easy to make technically correct but visually weak, hard to verify, or
misrouted to the wrong helper skill.

This feature keeps the frontend skill family as a coherent product surface: design
direction, implementation guidance, browser proof, visual QA, and review standards move
together.

## What It Does

- Maintains the core frontend skill family and its handoff boundaries.
- Captures parity learnings from strong frontend examples and folds them into local skill guidance.
- Requires browser or visual proof when the change is user-visible.
- Keeps design, implementation, QA, and review guidance connected instead of duplicated across skills.
- Preserves Farplane's preference for usable first screens over marketing placeholders unless the task is explicitly a landing page.

## User Stories

- As a frontend builder, I can find the right skill for design, implementation, QA, or review.
- As a reviewer, I can judge the result against visible evidence and frontend craft standards.
- As a maintainer, I can update one feature spec when the frontend skill family changes shape.

## Operating Contract

Frontend parity upgrades must improve the reusable skill family, not just one page.

- External examples are adapted through local skills and QA gates.
- User-visible changes need screenshot, browser, or visual QA evidence proportional to risk.
- Skill boundaries stay explicit: design, build, functional QA, visual QA, review, and delegation each keep their owner.
- The registry points to the skills that currently implement the family.

## Surfaces

Owner surfaces:

- `skills/frontend-craft`
- `skills/frontend-design`
- `skills/visual-design`
- `skills/delegate-frontend`
- `skills/visual-qa`
- `skills/landing-page`

Source context:

- `docs/MEMORY.md#MEM-0085`

External context:

- `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/main/.claude/skills`
- `https://github.com/Leonxlnx/taste-skill/blob/main/skills/taste-skill/SKILL.md`
- `https://ui.shadcn.com/docs/mcp`
- `https://ui.shadcn.com/docs/cli`
- `https://ui.shadcn.com/docs/components-json`
- `https://ui.shadcn.com/r/registries.json`

Evidence:

- `skills/frontend-craft/SKILL.md`
- `skills/frontend-design/SKILL.md`
- `skills/visual-design/SKILL.md`
- `skills/visual-qa/SKILL.md`
- `docs/HISTORY.md`

## Proof And Quality

Required checks:

- `python3 docs/features/validate_features.py`
- `python3 bin/validators/check_doc_refs.py`

Acceptance signals:

- The feature remains listed under exactly one owning system.
- The owner surfaces still exist and agree with this contract.
- Evidence refs support the current status.

## Rollout And Maintenance

- Update this feature page first when the capability contract changes.
- Then update owner surfaces and regenerate feature/system registries when metadata changes.
- Preserve the feature ID while active templates, skills, tickets, or docs still reference it.
- Maintenance owner: Domain Skill Families.

## Limits And Non-Goals

- This feature is not a design system for one app.
- This feature does not bypass local frontend QA.
- This feature does not import external UI frameworks as policy by default.
- Known limit: Docs/skill-contract upgrade only; no automated eval suite or searchable frontend rule corpus yet.
- Delete or merge this feature only when its current truth has moved into a clearer owner and all active refs are removed.

## Metrics

- `frontend_skill_prebuild_completeness_rate`
- `generic_ui_regression_rate`

## Alternatives Considered

- Keep this only as a registry row.
  Decision: reject.
  Reason: Farplane features must be readable specs, not opaque metadata entries.
- Fold this entirely into the owning system page.
  Decision: defer.
  Reason: keep the `FEAT-*` page while templates, skills, tickets, or proof surfaces need a stable capability handle.

## Change History

- 2026-06-26: Feature spec created.
- 2026-06-27: Migrated into the reader-first feature-spec shape.
