---
artifact: irreducible-bin-report
ticket_id: TASK-0218
created_at: 2026-06-24
status: proof
---

# TASK-0218 Irreducible Bin Report

## Count Delta

- `before:` 36 top-level files under `bin/`
- `after:` 17 top-level files under `bin/`
- `removed_or_moved_from_top_level:` 19 files
- `rule:` keep top-level files only when they are live installed command edges,
  live hook/runtime shims, global CLI edges, compatibility aliases that cannot
  be dropped safely yet, or bin-local docs/loader support.

## Remaining Top-Level Files

| File | Decision | Reason |
| --- | --- | --- |
| `bin/AGENTS.md` | keep | Nearest local agent instructions for edits under `bin/`; moving it would weaken owner-local policy. |
| `bin/README.md` | keep | Human command map and proof checklist for the bin surface. |
| `bin/_compat.py` | keep | Shared loader used by installed top-level wrappers; avoids duplicating wrapper boilerplate in every shim. |
| `bin/capture_user_turn.py` | keep | Installed by `install.sh`; referenced by `hooks.json` as a live UserPromptSubmit hook command. |
| `bin/farplane` | keep | Installed global shell command edge; resolves symlinks and executes `farplane.py`. |
| `bin/farplane.py` | keep | Core global CLI implementation used by `bin/farplane`; owns install, hooks, doctor, UI routing, and adoption subcommand. |
| `bin/farplane_boards.py` | keep | Installed/public compatibility command for the board adapter helper; implementation lives in `bin/core/farplane_boards.py`. |
| `bin/farplane_compute.py` | keep | Installed/public compatibility command for compute admission diagnostics; implementation lives in `bin/core/farplane_compute.py`. |
| `bin/farplane_invocation.py` | keep | Installed/public compatibility command used by invocation docs and skills; implementation lives in `bin/core/farplane_invocation.py`. |
| `bin/file_growth_hook.py` | keep | Installed runtime shim for file-growth hook behavior; implementation lives in `bin/runtime/file_growth_hook.py`. |
| `bin/notify.py` | keep | Installed notification command referenced by `config.toml.example`; implementation lives in `bin/runtime/notify.py`. |
| `bin/runtime_telemetry.py` | keep | Installed runtime telemetry command; implementation lives in `bin/runtime/runtime_telemetry.py`. |
| `bin/self_improve_hook_probe.py` | keep | Installed/public probe for hook-backed self-improvement sidecar; implementation lives in `bin/runtime/self_improve_hook_probe.py`. |
| `bin/stop_hook.py` | keep | Installed live Stop hook command referenced by `hooks.json`; implementation lives in `bin/runtime/stop_hook.py`. |
| `bin/ticket-runtime` | keep | Public hyphenated compatibility command for ticket runtime operations; implementation lives in `bin/core/ticket_runtime.py`. |
| `bin/ticket_runtime.py` | keep | Installed/public underscored command used by skills and docs; implementation lives in `bin/core/ticket_runtime.py`. |
| `bin/user_turn.py` | keep | Installed/runtime user-turn helper used by hook implementation and docs; implementation lives in `bin/runtime/user_turn.py`. |

## Removed From Top-Level

| Removed file | Owner path or replacement | Reason |
| --- | --- | --- |
| `bin/check_doc_parity.py` | `bin/validators/check_doc_parity.py` | Validator wrapper was not installed; callers should use the validator owner path. |
| `bin/check_doc_refs.py` | `bin/validators/check_doc_refs.py` | Validator wrapper was not installed; active docs now point to owner path. |
| `bin/check_harness_invariants.py` | `bin/validators/check_harness_invariants.py` | Validator wrapper was not installed; callers should use the validator owner path. |
| `bin/check_skill_capabilities.py` | `bin/validators/check_skill_capabilities.py` | Validator wrapper was not installed; callers should use the validator owner path. |
| `bin/check_skill_todo_tiers.py` | `bin/validators/check_skill_todo_tiers.py` | Validator wrapper was not installed; callers should use the validator owner path. |
| `bin/check_template_version_metadata.py` | `bin/validators/check_template_version_metadata.py` | Validator wrapper was not installed; callers should use the validator owner path. |
| `bin/check_tier0_phase_protocol.py` | `bin/validators/check_tier0_phase_protocol.py` | Validator wrapper was not installed; callers should use the validator owner path. |
| `bin/sync_skill_registry.py` | `bin/validators/sync_skill_registry.py` | Registry sync wrapper was not installed; callers should use the validator owner path. |
| `bin/sync_template_registry.py` | `bin/validators/sync_template_registry.py` | Registry sync wrapper was not installed; callers should use the validator owner path. |
| `bin/delegate_cli_agent.py` | `skills/delegate-cli/scripts/delegate_cli_agent.py` | Skill-owned helper wrapper was not installed; active skill docs now call the owner script directly. |
| `bin/farplane_recent_activity.py` | `skills/board-drain/scripts/farplane_recent_activity.py` | Board-drain-owned helper wrapper was not installed; active skill docs now call the owner script directly. |
| `bin/import_installed_skills.py` | `skills/skill-maintenance/scripts/import_installed_skills.py` | Skill-maintenance-owned helper wrapper was not installed; active docs now call the owner script directly. |
| `bin/install_selected_skills.py` | `skills/skill-maintenance/scripts/install_selected_skills.py` | Skill-maintenance-owned helper wrapper was not installed; `install.sh` now calls the owner script directly. |
| `bin/notion_pinned_read_check.py` | `skills/notion-task-field-fill/scripts/notion_pinned_read_check.py` | Notion skill-owned helper wrapper was not installed; test fixture now points to owner script. |
| `bin/pr_review_watch.py` | `skills/pr-review-watch/scripts/pr_review_watch.py` | PR-review-watch-owned helper wrapper was not installed; active skill docs now call the owner script directly. |
| `bin/sync_frontend_pi_skills.py` | `skills/delegate-frontend/scripts/sync_frontend_pi_skills.py` | Delegate-frontend-owned helper wrapper was not installed; active skill docs now call the owner script directly. |
| `bin/sync_skill_plugins.py` | `skills/skill-maintenance/scripts/sync_skill_plugins.py` | Skill-maintenance-owned helper wrapper was not installed; active docs now call the owner script directly. |
| `bin/farplane_adoption.py` | `bin/farplane.py adoption scan` / `bin/core/farplane_adoption.py` | Non-installed Core helper wrapper replaced by the global Farplane CLI subcommand and core implementation path. |
| `bin/farplane_telemetry_status.py` | `bin/core/farplane_telemetry_status.py` | Non-installed Core diagnostic wrapper removed; implementation stays under `bin/core/` until telemetry surface matures. |

## Compatibility Boundary

Further top-level reductions would require one of these compatibility-breaking
changes:

- changing installed hook commands in `hooks.json`
- changing installed command allowlist semantics in `install.sh`
- removing public `ticket_runtime.py` / `ticket-runtime` aliases
- forcing users and skills off `bin/farplane_invocation.py`,
  `bin/farplane_boards.py`, or `bin/farplane_compute.py`
- moving bin-local docs/policy files away from the directory they govern

Those are architectural or migration decisions, not safe cleanup inside
TASK-0218.
