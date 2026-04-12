---
ticket_id: TASK-0061
title: fix control-surface trigger parsing for impl and impl-plan
phase: documenting
status: building
owner: codex
claimed_by:
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-13T00:00:00Z
updated_at: 2026-04-12T23:17:33Z
next_action: archive after any desired broader stop-hook/runtime regression sweep
last_verification: targeted runtime verification passed via `python3 -m unittest bin/test_runtime_state.py`, `python3 -m py_compile bin/user_turn.py bin/capture_user_turn.py`, `python3 tickets/scripts/check_ticket_metadata.py`, and a manual parser repro confirming malformed hyphen-suffixed `$skill` lookalikes now stay non-owning
linked_docs:
  - docs/specs/runtime-surface.md
  - tickets/TASK-0060-define-loop-mode-separate-from-impl.md
---

# TASK-0061: fix control-surface trigger parsing for impl and impl-plan

## Summary
Fix the runtime capture substrate so public control-skill detection requires exact `$skill` tokens, `$impl-plan` no longer trips `$impl`, and planning prompts do not activate the `$impl` build loop.

## Scope
- In:
  - exact control-surface parsing for `UserPromptSubmit` capture
  - explicit `$impl` detection without prefix bleed from `$impl-plan`
  - intent classification that respects explicit public skill tokens before broad keyword heuristics
  - regression tests for `$impl`, `$impl-plan`, and non-token prompts
- Out:
  - adding the new `$loop` surface
  - redesigning the Stop-hook policy pipeline
  - natural-language skill inference without `$` prefixes

## Acceptance Criteria
- [x] AC-1: `$impl` still activates control-session ownership and `impl_loop_active`
- [x] AC-2: `$impl-plan` is classified as planning and does not set `impl_loop_active`
- [x] AC-3: non-token prompts like `impl TASK-0060` remain non-owning by default
- [x] AC-4: regression tests cover the exact trigger cases and pass

## Working Notes
- User explicitly wants `$`-prefixed skill invocation to remain the control trigger; do not broaden this fix into natural-language skill detection.
- This is the substrate fix needed before comparing `$impl` against a future lighter `loop` profile.
- The bug came from two separate detection paths: exact control-surface extraction already distinguished `$impl-plan`, but `explicit_impl_requested` still used a prefix regex that matched `$impl-plan` as `$impl`.
- The fix makes parsed `control_surface` the single source of truth for explicit `$impl` activation and lets intent classification honor explicit public skill tokens before broader keyword heuristics.
- Follow-up fix: the token parser now requires a real terminator after `$skill`, so malformed lookalikes such as `$impl-plan-extra` and `$deep-interview-notes` no longer count as valid public control-skill invocations.

## Evidence
- [x] Tests
- [x] Typecheck
- [ ] Lint
- [x] QA / manual verification

## Review Packet
- Scores use the anchored `1.0`-to-`5.0` rubric scale.
- `work_type:` `["runtime", "hooks", "tests"]`
- `search_scope:` `{changed_files: ["bin/user_turn.py", "bin/test_runtime_state.py", "tickets/TASK-0061-fix-control-surface-trigger-parsing.md"], related_files: ["docs/specs/runtime-surface.md", "hooks.json", "bin/stop_hook.py"], invariants_checked: ["MEM-0029", "MEM-0025"], docs_checked: ["docs/specs/runtime-surface.md", "docs/HISTORY.md", "skills/review/references/code-quality.md", "skills/review/references/integration-readiness.md", "skills/review/references/evidence-quality.md", "skills/review/references/desloppify.md"]}`
- `reviewed_at:` `2026-04-13 00:17 +0100`
- `rubrics_used:` `["code-quality", "integration-readiness", "evidence-quality"]`
- `overall_score:` `4.4`
- `overall_threshold:` `4.0`
- `overall_verdict:` `pass`
- `rerun_required:` `false`
- `evidence_quality:` `pass`
- `integration_readiness:` `pass`
- `traceability:` `pass`
- `freshness:` `pass`
- `hard_gate_failures:` `[]`
- `finding_log:` `[]`
- `blocking_findings:` `[]`
- `next_action:` `archive or fold into the broader loop-mode follow-up after any desired wider runtime sweep`

## Implementation Notes
- Touched areas:
  - `bin/user_turn.py`
  - `bin/test_runtime_state.py`
  - `docs/HISTORY.md`
- Reused patterns:
  - exact `$skill` control-surface ownership
  - session-first runtime capture
- Guardrails:
  - no natural-language skill inference
  - no Stop-hook policy expansion
  - keep `$impl` activation explicit and exact

## Handoff
- Current state: exact `$skill` parsing is fixed, `$impl-plan` no longer arms the `$impl` loop, and the focused runtime-state regressions pass
- Resume from: run a wider hook/runtime sweep only if you want extra confidence before archive; otherwise close out alongside the loop-mode follow-up work
