---
title: Notion Task Field Fill ntn Migration
owner: notion-task-field-fill
status: complete
kind: skill-audit
created_at: 2026-07-06
ticket: TASK-0303
---

# Notion Task Field Fill ntn Migration

## Delta

`notion-task-field-fill` now treats the official `ntn` CLI as its normal Notion
execution surface. Farplane keeps `NOTION_TOKEN` as the canonical credential and
bridges it to `NOTION_API_TOKEN` only for the `ntn` subprocess.

## Reason

The Notion MCP connector could keep stale auth state inside a live thread even
after `farplane run` and Doppler had a valid token. Launching `ntn` per run
uses the current local credential source and keeps Notion access scriptable,
bounded, and inspectable from the shell.

## Proof

- `./bin/farplane run -- sh -lc 'NOTION_API_TOKEN="$NOTION_TOKEN" ntn doctor'`
- `./bin/farplane run -- sh -lc 'NOTION_API_TOKEN="$NOTION_TOKEN" ntn api v1/users/me'`
- `./bin/farplane run -- python3 skills/notion-task-field-fill/scripts/ntn_task_field_fill.py --mode dry-run --this-week --artifact-dir tickets/TASK-0303/artifacts/read-only-run`
- `./bin/farplane run -- python3 skills/notion-task-field-fill/scripts/ntn_task_field_fill.py --mode live-high-confidence --this-week --live-field Attention\ Required --max-live-writes 1 --artifact-dir tickets/TASK-0303/artifacts/live-high-confidence-run`

## Residual

`ntn` is still beta. The skill keeps raw API helpers out of the normal path and
requires compact `filter_properties` queries, high-confidence-only writes, and
readback receipts before claiming live field-fill success.
