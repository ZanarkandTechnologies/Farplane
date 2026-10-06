# Cleanup catalog — 2026-09-24

Read-only sweep of Farplane (bin/, skills/*/scripts, repo surfaces), cross-checked
against Farplane-UI callers. "Dead" means grep found no live caller outside the
module's own test.

**Status (2026-09-24):** section 1 done in `9f63f9c0` except the lifecycle-graph
wrapper (moved to the graph consolidation), the CLI alias/shim cleanup, and the 12
retired FEAT specs (wait for the pending registry changes). `import_installed_skills.py`
stays: it still serves skills born in live runtime homes. Ticket `node_modules`
(~1.2G) deleted; renders, `output/`, and the phone-chaser venv kept.

## Root cause worth fixing first

The Multica migration is half-finished. `tickets/README.md` forbids
`farplane ticket finalize` and GitHub closeout, but live instructions still use
them, and several live scripts still read `tickets/TASK-*/ticket.md`. Most of the
"retired concept" code below survives only because of that drift.

Still pointing at the old flow:
- `skills/close-ticket/SKILL.md` steps 8–10, line 77; `skills/goal-advisor/SKILL.md:159`
- Docs: `README.md:269,289`, `farplane/README.md:102`, `docs/prd.md:287`,
  `docs/farplane-framework/hooks-and-runtime.md:168-177`, `ticket-execution-loop.md:262`,
  `FEAT-0007:138,219`, `FEAT-0068:151`
- Scripts reading filesystem tickets: `pulse-update/{list_pulse_board,next_ticket_id,materialize_skill_call}.py`,
  `plan-next-wave/validate_wave_response.py:210`, `delegate-cli/delegate_cli_agent.py:153`,
  `phone-chaser/compile_review_call.py --ticket`

## 1. Remove now (no live caller)

| Path | Lines | Evidence |
|---|---|---|
| `bin/core/farplane_telemetry_status.py` + test | 327 + 173 | test-only |
| `bin/core/farplane_reward_migration.py` + test | 181 + 113 | finished one-off migration, test-only |
| `skills/skill-maintenance/scripts/sync_skill_plugins.py` + test | 524 | never installed; symlink installs replace it. Also drop FEAT-0030, `bin/README.md:186-188`, git-review-gates entries |
| `skills/skill-creator/scripts/package_skill.py` | 109 | plugin packaging, docs-only refs |
| `skills/notion-task-field-fill/scripts/notion_pinned_read_check.py` + test + `tests/notion-task-field-fill/pinned_tasks_read_check.json` | 274 | no skill/automation caller |
| `skills/content-impl-plan/scripts/verify_scene_direction.py` + test | 186 | retired video-production leftover |
| `skills/eval/scripts/migrate_skill_evals.py` + test | 163 | finished one-off migration |
| `skills/qa/scripts/validate_eval_run.py` + test | 99 | test-only |
| `skills/apify/scripts/helper.py` | 14 | unfilled skill-creator stub |
| `skills/skill-maintenance/scripts/generate_farplane_lifecycle_graph.py` | 11 | wrapper shim |
| `hooks/shared_checkout_guard.py` + README/docs lines | 12 | unregistered no-op shim |
| `blockers.md` | — | empty batch-era log; blockers live in Multica |
| 12 retired FEAT specs (0014, 0015, 0025, 0029, 0031, 0042, 0043, 0054, 0057, 0065, 0066, 0069) | ~57K | registry marks retired; docs/AGENTS.md says delete |
| CLI: `farplane bank` alias, `OLD_CONVEX_SITE_URL`, `HOOK_MIGRATION_LINKS`/`RETIRED_HOOK_FILES` in `farplane_cli_base.py` | — | unused alias and migration shims |

About 3,000 lines of code plus tests.

## 2. Remove after the Multica close-out rewrite

| Path | Lines | Blocked by |
|---|---|---|
| `bin/core/farplane_ticket_close.py` + `farplane_ticket_issue.py` + tests | 853 + ~523 | close-ticket / goal-advisor still call `ticket finalize` |
| `farplane ticket finalize`, `farplane mining ticket` subcommands, `mine_ticket` path | — | same |
| `bin/core/farplane_ticket_history.py`, `validators/check_ticket_closure_gate.py` | 489 + 213 | pulse-update, dogfood-review, and the git gate still read `tickets/` |

Keep the rest of `farplane_mining.py`: Farplane-UI calls `farplane mining` (`ui/server/mining-local-api.ts`).

## 3. Consolidate

| Group | Today | Target |
|---|---|---|
| skill-maintenance graph stack | 9 files, ~3,180 lines, one external caller (`farplane_skill_sync.py`) | `graph.py` runner + shared IR, one function per projection |
| pulse-update scripts | 6 executables, ~2,080 lines | `pulse.py guard\|wave\|circuit\|board\|reserve\|materialize`, board/next-id/materialize on Multica |
| x-account + instagram-account | 15 files, mirrored config/env/metrics; they import each other's `runtime_env` | one runner per skill + shared `social_runtime` module |
| feed-scout | 5 scripts, 1 named in SKILL.md | `feed_scout.py` subcommands |
| check_skills family | `sync_skill_checklists`, `minimize_skill_surface`, `generate_template_intelligence`, `skill-creator/quick_validate` | subcommands of `check_skills.py` |
| Frontmatter parsers | ~8 copies (reports, ticket_history, ticket_close, project_snapshot, primitive_metrics, check_ticket_closure_gate, user_turn, metric_shared, skill_contract) | `lint/source.parse_markdown_frontmatter` |
| `read_json`/`read_jsonl` | 10+ copies | one shared io helper |
| `bin/core/farplane_metric_cli.py` | second CLI entry via `metric_refresh __main__` | `farplane metrics` subcommand group |
| `bin/_compat.py` | 13-line runpy shim for `notify.py` and the user-turn hook | direct imports |
| `bin/farplane.py` | ~25 re-exports only for tests | tests import owner modules |
| Doc names | `pulse-and-interval-loop.md`, `FEAT-0067-daily-interval-review-reports.md`; Interval described as live in `reporting.md`, `systems/horizon-loop.md` | rename; rewrite as Company OS reviews |

## 4. Local disk (untracked, rebuildable)

| Path | Size | Note |
|---|---|---|
| `node_modules` / Chrome / webpack caches under `tickets/TASK-*` | ~1.3G | no path references; `pnpm install` rebuilds |
| `tickets/TASK-0416`, `0419`, `0422` | ~1.7G total | renders + node_modules; 0422 is the retired GitHub-closeout ticket. Attach wanted MP4s/receipts to Multica first |
| `farplane/phone-chaser/.venv` | 205M | gitignored; `uv sync` rebuilds |
| `output/`, `tmp/`, `.tmp-validation.*`, `.pytest_cache` | ~32M | no references |
| `tickets/archive/TASK-0378` | 153M | tracked bulk inside the archive |

## Keep (checked, live)

`automations/` vs `farplane/automations/` are not duplicates: reusable recipes vs configured records (HISTORY.md:356), both mid-migration and uncommitted. `hooks/*` (except the guard), `rules/*`, `qa/`, `templates/`, `farplane/*.yaml|json`, runtime modules, validators, `hatch-pet` scripts, and account `check_config` scripts all have live callers. Unverified: `requirements.txt` has no references but may back the root `.venv`; `extension youtube`/`delegate` CLI callers were only checked in Farplane-UI's server files.

## Suggested order

1. Section 1 deletions (one commit, run the test suite).
2. Local disk cleanup (no git impact).
3. Multica close-out ticket (the draft from 2026-09-23), then section 2.
4. Consolidations, largest first: graph stack, pulse-update, social runtime, parsers.
