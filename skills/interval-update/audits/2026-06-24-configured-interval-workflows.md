---
title: "Configured Interval Workflows Audit"
owner: interval-update
status: pass
created_at: 2026-06-24
skill: interval-update
mode: structure_update
---

# Configured Interval Workflows Audit

## Behavior Delta

Expected behavior: `interval-update` is a generic report-then-plan primitive
that takes configured timeframes, context refs, cross-interval refs, optional
report workflow flags, planning policy, and write policy. It must not encode
daily or weekly cadence behavior in the skill package.

Current behavior before change: `interval-update` contained daily and weekly
default presets, skill-local daily/weekly templates, and special-case parent
context rules.

## QA Checklist Result

Verdict: `pass`

- `composition_clarity`: pass. Signature now exposes `context_refs`,
  `report_workflows`, `planning_policy`, and `write_policy`.
- `maintenance_locality`: pass. Daily/weekly wiring moved to
  `farplane/automations.md` and automation templates.
- `project_specific_context_isolation`: pass. The skill package no longer
  mentions `daily_interval` or `weekly_interval`.
- `duplicated_instruction_count`: pass. Presets were removed from the skill;
  interval-to-interval dependencies are configured at the caller.
- `reference_load_precision`: pass. The remaining reference file owns generic
  config schemas, while each enabled workflow loads one skill-shaped workflow
  reference with its own signature, checklist, gates, and output contract.

## First Load Review

```text
line_count_before: 180
line_count_after: 229
kept_in_skill:
  - trigger/context boundary
  - generic signature and state reads/writes
  - default Farplane refs
  - configured cross-interval refs
  - optional report workflow gating
  - report-before-mutation gates
moved_to_reference:
  - context_refs schema
  - report_workflows schema
  - workflow index in SKILL.md
  - one skill-shaped detailed file per report workflow
  - workflow-specific source refs, gates, todos, gotchas, output contracts, and
    subagent routing
deleted_as_duplicate_or_rationale:
  - skill-local daily interval preset
  - skill-local weekly interval preset
  - daily/weekly template files under interval-update
extra_sections_kept_with_reason: none
```

## Proof

- `python3 skills/skill-maintenance/scripts/check_skills.py --write`: pass
- `python3 bin/validators/check_farplane_project_files.py`: pass
- `python3 bin/validators/check_doc_refs.py`: pass
- `PYTHONPATH=. uvx pytest bin/validators/test_check_farplane_project_files.py skills/skill-maintenance/scripts/test_generate_farplane_lifecycle_graph.py`: pass, 21 tests
- `git diff --check`: pass

## Remaining Risk

Live and template automations now pass daily/weekly behavior as config, but the
next real interval run should be inspected to verify agents actually respect
the new `context_refs.interval_output_refs` selectors instead of inferring old
cadence presets.
