---
title: Notion Token Standard
owner: notion-task-field-fill
status: complete
kind: skill-audit
created_at: 2026-07-06
superseded_by: 2026-07-06-ntn-migration.md
---

# Notion Token Standard

## Delta

Farplane now treats `NOTION_TOKEN` as the canonical Notion credential for
`notion-task-field-fill`. `NOTION_API_KEY` is no longer accepted by the skill
helper as a fallback.

## Reason

The Notion task field-fill path expects `NOTION_TOKEN`; after TASK-0303 the
skill bridges that value to `NOTION_API_TOKEN` only for the official `ntn` CLI
subprocess. Keeping `NOTION_API_KEY` as Farplane's internal canonical name
created hidden mapping and stale-runtime confusion.

## Proof

- `farplane run -- farplane install`
- `python3 skills/notion-task-field-fill/scripts/test_notion_config.py`
- `python3 -m unittest bin/tests/test_runtime_config.py bin/tests/test_farplane_config_doctor.py`
- `python3 skills/skill-maintenance/scripts/check_skills.py --write`

## Residual

Doppler still contains the old `NOTION_API_KEY` value as an unused duplicate.
Farplane no longer checks or reads it for Notion task field fill.
