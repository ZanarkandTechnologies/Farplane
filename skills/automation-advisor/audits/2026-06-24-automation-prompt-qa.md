---
title: "Automation Prompt QA Audit"
owner: automation-advisor
status: pass
created_at: 2026-06-24
skill: automation-advisor
mode: qa_checklist_design
---

# Automation Prompt QA Audit

## Behavior Delta

Expected behavior: `automation-advisor` should prevent Codex automation prompts
from becoming bloated mini-skills. Prompt blocks should contain only the
configuration that cannot live in the called skill: cadence identity, project
root, interval windows, cross-interval context refs, enabled workflows,
project-specific sources, policies, and side-effect gates.

Current behavior before change: `automation-advisor` had a general proof step
but no dedicated QA checklist for prompt minimality, config hygiene, state
boundaries, or legacy-orchestrator regressions.

## QA Checklist Design

Verdict: `pass`

- Added `skills/automation-advisor/qa_checklist.md`.
- Added first-load todo pointers to read and apply the checklist for material
  prompt edits or live automation updates.
- Checklist separates skill-owned behavior from project-owned config.
- Checklist includes prompt size, context refs, workflow flags, runtime state,
  workflow-source routing, no-legacy-orchestrator, copyability, and
  review-route checks.

## First Load Review

```text
line_count_before: 180
line_count_after: 186
kept_in_skill:
  - automation-advisor trigger and skill boundary
  - prompt authoring todo path
  - activation recipe
  - QA checklist load/apply hooks
moved_to_reference:
  - detailed prompt QA checks into qa_checklist.md
deleted_as_duplicate_or_rationale: none
extra_sections_kept_with_reason: Live Activation Recipe remains because it is
  the normal activation path and contains side-effect boundaries.
```

## Proof

- `python3 skills/skill-maintenance/scripts/check_skills.py --write`: pass
- `python3 bin/validators/check_farplane_project_files.py`: pass
- `python3 bin/validators/check_doc_refs.py`: pass
- `PYTHONPATH=. uvx pytest bin/validators/test_check_farplane_project_files.py skills/skill-maintenance/scripts/test_generate_farplane_lifecycle_graph.py`: pass, 21 tests
- `git diff --check`: pass
