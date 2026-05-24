---
ticket_id: TASK-0182
title: add curated skill bundle plugins
phase: documenting
status: done
owner: codex
claimed_by:
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
requires_qa: false
requires_demo: false
created_at: 2026-05-25T03:20:00+08:00
updated_at: 2026-05-25T03:28:00+08:00
next_action: completed and archived
last_verification: 2026-05-25 03:28 +0800 - review passed with code-quality 4.2, integration-readiness 4.2, evidence-quality 4.3
---

# TASK-0182: add curated skill bundle plugins

## Summary
Add curated grouped plugins to the Codexter repo marketplace while preserving
one-plugin-per-skill packages and the direct selected-skill installer. This
lets normal users install practical bundles such as coding workflow, frontend,
research, media, and harness engineering, while power users can still install a
single skill.

## Scope
- In:
  - extend `bin/sync_skill_plugins.py` with curated bundle generation
  - generate bundle plugin packages under `plugins/codexter-*`
  - list bundles first in `.agents/plugins/marketplace.json`
  - update docs and tests
- Out:
  - no new TUI
  - no removal of per-skill plugins
  - no removal of selected-skill CLI fallback

## Acceptance Criteria
- [x] Marketplace contains curated bundle plugins and individual skill plugins.
- [x] Bundle plugin manifests validate.
- [x] Bundle plugins contain copied source skill folders.
- [x] README documents the group-first install flow and the single-skill fallback.
- [x] Sync tests cover bundle generation.

## Proof Contract
- `Metrics:`
  - `Primary metric:` plugin sync, tests, and validation pass
  - `Direction:` pass/fail
  - `Verify:` `python3 bin/sync_skill_plugins.py --check`
  - `Guard:` `python3 -m unittest bin/test_sync_skill_plugins.py bin/test_install_selected_skills.py`
  - `Min acceptable result:` pass
  - `Autoresearch warranted:` no
  - `Autoresearch session:` none
- `Review Rubrics:`
  - `code-quality >= 4.0`
  - `integration-readiness >= 4.0`
  - `evidence-quality >= 4.0`
- `Required Evidence:`
  - tests
  - sync check
  - plugin validation
  - final review result

## Evidence
- `Artifacts:`
  - `tickets/archive/TASK-0182/artifacts/review/2026-05-25-curated-skill-bundles-review.json`
- `Commands:`
  - `python3 bin/sync_skill_plugins.py` - generated 81 plugins, including 6 bundles and 75 individual skills
  - `python3 bin/sync_skill_plugins.py --check` - passed, skill plugins in sync
  - `python3 -m unittest bin/test_sync_skill_plugins.py bin/test_install_selected_skills.py` - passed, 14 tests
  - plugin-creator `validate_plugin.py` over `plugins/*` - passed, 81 plugins
  - `python3 docs/features/validate_features.py` - passed, 33 records
  - `python3 tickets/scripts/check_ticket_metadata.py` - passed, 22 ticket files checked
  - `python3 bin/check_doc_parity.py` - passed, 6 files checked / 29 rules
- `Result summary:` marketplace now lists six curated bundle plugins first, followed by individual skill plugins; selected-skill CLI remains available.

## Blockers
- none
