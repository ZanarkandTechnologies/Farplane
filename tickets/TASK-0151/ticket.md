---
ticket_id: TASK-0151
title: consolidate video production skills into method addresses
phase: planning
status: review
owner: codex
claimed_by:
priority: medium
depends_on: []
blocked_by: []
ready: false
approval_required: true
requires_qa: false
requires_demo: false
created_at: 2026-05-19T14:45:00+08:00
updated_at: 2026-05-19T14:45:00+08:00
next_action: run impl-plan for a video-production hard migration, using social-content as the reference pattern
last_verification: ticket created after social-content consolidation validated
---

# TASK-0151: consolidate video production skills into method addresses

## Summary
Consolidate sibling Tier 3 video-production workflow skills into one
method-addressed `video-production` package while keeping tool execution layers
such as `video-generation`, `image-generation`, `remotion`, and
`remotion-render` separate.

## Scope
- `In:`
  - inspect `ai-marketing-videos`, `explainer-video-guide`,
    `storyboard-creation`, `talking-head-production`, and `video-ad-specs`
  - decide final method names such as `video-production:marketing`,
    `video-production:explainer`, `video-production:storyboard`,
    `video-production:talking-head`, and `video-production:ad-spec`
  - preserve upstream references under the new owner
  - update Markdown refs, generated registry rows, and domain routing docs
  - validate stale-link cleanup and tier-todo rules
- `Out:`
  - merging `video-generation`, `image-generation`, `remotion`, or
    `remotion-render`
  - creating soft aliases or compatibility wrappers
  - changing Tier 1 / Tier 2 skill rules

## Plan
- `Change:` use the successful `social-content` consolidation as the migration
  template for the video-production cluster.
- `Why:` these video skills are all Tier 3 application workflow routers around
  the same inference.sh/media production infrastructure, so method addresses
  should reduce public skill-list bloat without losing workflow specificity.
- `Before -> After:`
  - Before: several public video workflow skills route to the same media
    execution surfaces.
  - After: one public `video-production` skill owns video workflow methods,
    while execution layers stay direct and separate.
- `Touch:`
  - candidate video skill directories
  - `docs/skills/registry.jsonl`
  - `docs/specs/skill-tier-rollout-plan.md`
  - downstream references in `frontend-craft`, `video-generation`, and content
    docs if present
- `Execution steps:`
  1. Run `impl-plan` before editing to lock the exact candidate table and method
     names.
  2. Hard-migrate one video cluster, preserving upstream references.
  3. Rewrite Markdown refs to `video-production:*`.
  4. Run the skill-maintenance validators and stale-link search.
  5. Install/prune live symlinks if the migration should be available
     immediately.
- `Recommendation:` migrate video-production next; keep documentation and
  external-patterns separate Tier 2 skills for now.

## Acceptance Criteria
- [ ] Candidate table decides each video skill as merge or keep.
- [ ] New `video-production` owner declares method addresses.
- [ ] Removed video sibling directories have no stale Markdown links.
- [ ] Execution-layer media skills remain separate.
- [ ] Validators pass.

## Verification
- `Tests:`
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  - `python3 bin/sync_skill_registry.py --check`
  - `python3 bin/check_skill_todo_tiers.py --allow-peer-tier3`
  - `python3 tickets/scripts/check_ticket_metadata.py`
  - `git diff --check`
- `Manual checks:`
  - stale-link `rg` for removed video skill names
  - registry inspection for `video-production` methods
- `Evidence required:`
  - candidate table
  - validator output
  - stale-link search output
  - review artifact

## Proof Contract
- `Metrics:`
  - `Primary metric:` zero stale Markdown links to removed video sibling skill
    directories
  - `Direction:` zero
  - `Verify:` stale-link `rg` over `AGENTS.md docs skills tickets agents templates`
  - `Guard:` skill-maintenance validators and `git diff --check`
  - `Autoresearch warranted:` no
  - `Autoresearch session:` none
- `Review Rubrics:`
  - `implementation-plan >= 4.0`
  - `integration-readiness >= 4.0`
  - `evidence-quality >= 4.0`
- `Required Evidence:`
  - candidate table
  - validator outputs
  - stale-link search result
  - review result

## Refs
- `docs/specs/skill-tier-rollout-plan.md`
- `docs/skills/registry.jsonl`
- `skills/social-content/SKILL.md`

## Evidence
- `Artifacts:` none yet
- `Commands:` none yet
- `Result summary:` pending

## Blockers
- approval required before build
