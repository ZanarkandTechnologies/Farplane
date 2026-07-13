---
title: TASK-0348 prototype verification
kind: qa-evidence
status: complete
created_at: 2026-07-13T21:48:00+08:00
---

# Prototype verification

## Deterministic checks

| Check | Result |
| --- | --- |
| `sync_template_registry.py --write` | pass; generated registry includes `human-report-template@0.1.0` |
| `sync_template_registry.py --check` | pass |
| `check_template_version_metadata.py --all` | pass for tracked templates |
| Direct metadata validation of new untracked template | pass; `template_id` and semver parsed |
| Template registry and version-watch membership | pass |
| `check_doc_refs.py` | pass; 1,888 refs checked |
| `validate_features.py` | pass; 11 systems and 30 features |
| `git diff --check` | pass |
| Exact JSON object keys and expected receipt values | pass |
| Source report SHA-256 | unchanged: `5b1fa2ff3f2df3717d90d9a383daa414ccd2c593e9c8ff32d3999c974749c7f0` |
| Live `skills/dogfood-review/` diff | empty |
| Existing reporting CRM-source hunk | retained |
| Existing registry `farplane-framework@2.0.3` hunk | retained after regeneration |

`check_template_version_metadata.py --all` enumerates Git-tracked files, so the
new worktree template was also passed directly through the validator's metadata
parser. Once tracked, the watchlist makes it part of the ordinary `--all` and
staged version-bump checks.

## Receipt assertions

The JSON check requires exact key sets for `authority`, `mutations`, `guards`,
and `stop`, then asserts:

- `write_policy` is `report_only` and external actions are false;
- Goal Packet, experiment-ticket, and recovery-ticket creation counts are `0`;
- execution/check-in, Pulse/worker, reward mutation, and learning-receipt
  recreation are false;
- all eight source ordering/capacity guards are true;
- the no-execution string exactly matches the source report.

Missing, changed, or extra mapped keys fail the assertion.

## Reading-path measurement

- Source: 1,990 words, 14 headings.
- Prototype: 549 words, 7 headings.
- Delta: 72% fewer words and 50% fewer headings.
- Visual aid: one Mermaid situation map.
