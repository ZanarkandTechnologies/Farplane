# Code Review: Ralph Prototype Implementation Files

## Summary
- Files reviewed: 5
- Critical issues: 1
- Important issues: 4
- Suggestions: 0

## Critical Issues (must fix)
### Issue 1: `docs_complete` can complete tickets with missing required proof
- **File**: `bin/ralph_judge.py:227`
- **Confidence**: 95
- **Problem**: The `docs_complete` branch returns `complete_ticket` unconditionally and does not check unchecked acceptance/evidence items. A docs-phase result can therefore mark a ticket complete while required QA evidence is still missing.
- **Fix**: Apply the same `missing = acceptance_gaps + evidence_gaps` gate used in `build_complete`/`done`, and only return `complete_ticket` when `missing` is empty.

## Important Issues (should fix)
### Issue 1: Stop hook judges Ralph phase from ticket frontmatter instead of current run state
- **File**: `bin/stop_hook.py:259`
- **Confidence**: 92
- **Problem**: `run_ralph_judge` passes `ticket["phase"]` (or defaults to `building`) to `ralph_judge.py`. With state-first `current-run.json`, the active run phase may differ from ticket frontmatter. This can misclassify decisions (for example `repeat_ralphplan` downgraded to `repeat_ralph`).
- **Fix**: Source phase from `current-run.json` when available and pass that through the stop-hook Ralph path; use ticket frontmatter only as fallback.

### Issue 2: Plain `none` in Blockers is treated as a real blocker
- **File**: `bin/stop_hook.py:157`
- **Confidence**: 90
- **Problem**: `blocked_items` excludes only `"- none"`, but not `"none"`. Tickets using plain `none` will be interpreted as blocked and force stop.
- **Fix**: Normalize and exclude both `none` and `- none` (matching `ralph_judge.py` behavior).

### Issue 3: Orchestrator leaves run-state as `running` when worker/judge fails
- **File**: `bin/ralph_orchestrate.py:226`
- **Confidence**: 88
- **Problem**: Initial state is written as `running` before invoking worker/judge. Any exception from `run_worker`/`run_judge` exits without updating status, leaving stale `current-run.json` that can mislead state-first ticket/phase resolution.
- **Fix**: Wrap worker/judge in `try/except/finally`, persist a terminal failure status (`failed`/`judge_failed`) plus `updated_at`, and keep `current-run.json` consistent.

### Issue 4: Smoke eval never fails the process and does not assert semantics
- **File**: `experiments/run_ralph_smoke_evals.py:251`
- **Confidence**: 86
- **Problem**: Script always returns `0` and `ok` is mostly based on subprocess exit code. Regressions in expected judge decisions can pass silently, reducing eval usefulness.
- **Fix**: Add explicit assertions on expected verdict fields per case and return non-zero if any case fails.

## Strengths
- `ralph_worker.sh` is explicit and bounded to one phase with clear CLI validation.
- `ralph_orchestrate.py` cleanly separates worker and judge responsibilities.
- Judge output schema is consistent and machine-readable.

## Recommended Actions
1. Fix the `docs_complete` completion gate in `ralph_judge.py` first.
2. Align stop-hook phase source with `current-run.json` and normalize blocker parsing.
3. Make orchestrator failure states explicit in run-state artifacts.
4. Harden smoke evals to fail loudly on behavior drift.
