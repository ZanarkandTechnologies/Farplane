---
skill: board-drain
date: 2026-06-15
change_type: create
owner: codex
status: draft
review_route: self_check
reasoning_basis: first_principles
eval_required: no
---

# Board Drain Skill Creation Audit

## Change

Created `skills/board-drain/SKILL.md` as a Tier 3 selector workflow for hourly
idle board draining. The skill keeps execution ownership with `goal-advisor`,
uses `weekly-strategy-analysis` as the no-ticket fallback, and treats Notion as
a read source through `notion-context` when available.

## Before Behavior

- Board-drain heartbeat policy existed inside Goal Advisor references.
- There was no public skill whose first-load contract combined activity
  detection, local/Notion board normalization, compounding selection, and
  Goal Advisor handoff.

## After Behavior

- Operators can call `board-drain` as the visible hourly idle-worker selector.
- The skill defines input binding, activity check, local/Notion candidate
  loading, autonomous safety filters, compounding ranking, and fallback routing.
- A helper command provides deterministic activity evidence through the
  Farplane Console activity endpoint, with local event logs available only as
  an explicit diagnostic fallback.

## Rubric

- `first_load_sufficiency:` pass. The default path is executable from
  `SKILL.md` without hidden chat context.
- `reference_load_precision:` pass. References are route-specific and not
  required for every branch.
- `missing_context_rate:` pass. Required inputs and fallback behavior are named.
- `noisy_context_rate:` pass. Long examples and broad rationale are avoided.
- `duplicated_instruction_count:` pass. The skill composes Goal Advisor and
  weekly strategy instead of copying their internals.
- `prompt_size_tokens:` pass. First-load scope is compact enough for normal use.
- `task_success_rate:` unknown. No behavioral eval has run for this new skill.
- `review_tas_rate:` unknown. No reviewer receipt exists yet.
- `maintenance_locality:` pass. Skill-local behavior is owned by the new package.
- `composition_clarity:` pass. Inputs, outputs, gates, routes, and failures are explicit.

## Proof Artifacts

- `python3 -m unittest skills/board-drain/scripts/test_farplane_recent_activity.py`
- `python3 skills/board-drain/scripts/farplane_recent_activity.py --project-root . --window-minutes 60 --json`
- `python3 skills/skill-maintenance/scripts/check_skills.py --write`
- `python3 bin/validators/sync_skill_registry.py --check`

## Followups

- Add a behavioral eval after the first real board-drain heartbeat run produces
  a transcript or artifact to judge.
