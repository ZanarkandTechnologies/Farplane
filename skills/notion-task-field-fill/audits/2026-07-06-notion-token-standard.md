---
title: Notion Token Standard
owner: notion-task-field-fill
status: complete
kind: skill-audit
created_at: 2026-07-06
---

# Notion Token Standard

## Delta

Farplane now treats `NOTION_TOKEN` as the canonical Notion credential for
`notion-task-field-fill` and the Notion MCP adapter. `NOTION_API_KEY` is no
longer accepted by the skill helper as a fallback.

## Reason

The live Notion MCP adapter expects `NOTION_TOKEN`. Keeping `NOTION_API_KEY` as
Farplane's internal canonical name created a hidden mapping step and made
Doppler, install, MCP, and skill helper behavior harder to debug.

## Proof

- `farplane run -- farplane install`
- `python3 skills/notion-task-field-fill/scripts/test_notion_config.py`
- `python3 -m unittest bin/tests/test_runtime_config.py bin/tests/test_farplane_config_doctor.py`
- `python3 skills/skill-maintenance/scripts/check_skills.py --write`

## Residual

Doppler still contains the old `NOTION_API_KEY` value as an unused duplicate.
Farplane no longer checks or reads it for Notion task field fill.
