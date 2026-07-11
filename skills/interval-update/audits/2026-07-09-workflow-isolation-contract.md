---
title: Interval Workflow Isolation Contract Audit
owner: interval-update
status: complete
created_at: 2026-07-09T11:27:00+08:00
ticket: TASK-0317
kind: skill-audit
---

# Interval Workflow Isolation Contract Audit

## Behavior Delta

- Before: `interval-update` kept a substantial part of its core execution
  contract in `references/interval-update.md`, and workflow references allowed
  inline execution for small cases.
- After: `SKILL.md` owns the parent run skeleton, enabled workflows default to
  read-only subagent lanes, the context bundle separates `summary_context` from
  `raw_evidence_pointers`, and `reward_checkins` is the named gated write
  exception.
- Example: a Daily interval with `plan_progress`, `goal_drift`,
  `reward_checkins`, and `priority_planning` enabled now builds one context
  bundle, spawns read-only workflow lanes, runs the reward due helper only as a
  mechanical exception, writes the report, then applies allowed deltas.

## Source Refs

- `tickets/TASK-0317/ticket.md`
- `.farplane/context/20260709-104943-interval-reuse-council-context.md`
- `skills/interval-update/SKILL.md`
- `skills/interval-update/references/interval-update.md`
- `skills/interval-update/templates/interval-context-bundle.md`
- the former Interval workflow catalog, deleted during TASK-0319 refinement
- `skills/interval-update/eval_task.json`

## Skill-Maintenance Checks

```text
line_count_before:
  SKILL.md: 395
  references/interval-update.md: 444
  templates/interval-context-bundle.md: 92
  eval_task.json: 88
line_count_after:
  SKILL.md: 444
  references/interval-update.md: 456
  templates/interval-context-bundle.md: 135
  eval_task.json: 133
kept_in_skill:
  - non-optional parent run skeleton
  - workflow lane default
  - Daily/Weekly wrapper boundary
  - Pulse boundary
  - reward_checkins gated exception
moved_to_reference:
  - none; existing reference remains extended detail
deleted_as_duplicate_or_rationale:
  - stale inline-default wording in workflow phase boundaries
extra_sections_kept_with_reason:
  - parent run contract belongs in first load because missing it changes behavior
verdict:
  - pass: growth is intentional and tied to first-load behavior
```

## Validation

- `python3 -m json.tool skills/interval-update/eval_task.json` passed.
- The former Interval reward-helper test and compile checks passed at the time
  of this historical audit. TASK-0319 later deleted that runtime path after
  moving derived check-in eligibility to Work Pulse.
- `python3 skills/skill-maintenance/scripts/check_skills.py --write` passed.
- `python3 tickets/scripts/check_ticket_metadata.py` passed.

## Review Notes

- Remaining proof need: final drift review and reviewer completion review for
  TASK-0317.
- Installed skill copies were not synced in this pass. If judging live Codex
  home behavior, reinstall/sync local skills after source review.
