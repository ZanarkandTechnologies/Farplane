---
ticket_id: TASK-0046
title: retire ralph name and runtime surface
phase: complete
status: done
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-09T16:58:32+0100
updated_at: 2026-04-10T03:07:28+0100
next_action: archived; `.harness` is the live runtime root, `$impl` is the public execution surface, and former `ralph-*` docs/schemas now live only under `docs/specs/legacy/`
last_verification: 2026-04-10T03:07:28+0100 | active-surface sweep shows only explicit `docs/specs/legacy/ralph-*` references; `python3 -m unittest bin/test_runtime_state.py bin/test_stop_hook.py`, `python3 -m py_compile bin/stop_hook.py bin/user_turn.py skills/impl/scripts/tmux_helper.py`, `python3 tickets/scripts/check_ticket_metadata.py`, and `python3 bin/check_doc_parity.py` all passed
linked_docs:
  - AGENTS.md
  - PROJECT_RULES.md
  - README.md
  - config.toml.example
  - tickets/README.md
  - docs/specs/harness-techniques.md
  - docs/specs/context-and-handoff-policy.md
  - docs/specs/runtime-surface.md
  - docs/specs/README.md
  - docs/specs/legacy/ralph-runtime-surface.md
  - docs/specs/legacy/ralph-v2-direction.md
  - bin/user_turn.py
  - bin/stop_hook.py
  - skills/impl/scripts/tmux_helper.py
  - skills/impl/SKILL.md
---

# TASK-0046: retire ralph name and runtime surface

## Summary
Remove `ralph` as a live Codexter execution identity, retire `.ralph/` as the primary runtime surface, and converge on a simpler public naming model that matches how the harness is actually supposed to be used now.

## Scope
- In:
  - repo-wide inventory of public `ralph` surfaces across skills, docs, hooks, runtime paths, and status messages
  - choosing the canonical replacement for the execution loop and runtime directory surfaces
  - collapsing the public `$ralph` and `$impl` execution surfaces into one canonical public execution skill
  - migration rules for `.ralph/` -> `.harness/`, `RALPH_*` selectors, and legacy docs/spec names
  - doc/runtime parity cleanup so the public harness story stops advertising `ralph`
- Out:
  - inventing a brand-new orchestration architecture
  - rewriting historical research artifacts where `Ralph` is part of preserved history or quoted source material
  - silently breaking active compatibility paths without an explicit migration plan

## User Story
- `Actor:` Codexter operator entering the harness cold
- `Need:` one clear execution identity instead of overlapping `impl` plus `ralph` terminology and a mysterious `.ralph/` runtime tree
- `Outcome:` the harness is easier to understand, easier to teach, and less likely to accumulate stale runtime behavior around a name that no longer earns its keep

## User Pain / JTBD
- `Current pain:` `ralph` still appears in skills, docs, hooks, runtime paths, and experiments even though the execution model is already shifting toward `impl` and ticket-visible orchestration
- `Why now:` the user explicitly wants the name gone and does not think the current `.ralph/state` surface is useful enough to justify its conceptual cost

## Non-Goals
- `Do not solve:` every future execution-loop simplification, multi-ticket dispatching, or a total rewrite of the stop-hook system in the same pass

## High-Fidelity Example
- `Example flow/artifact:` a new operator reads `AGENTS.md`, `README.md`, or a ticket and sees one execution story, one runtime naming scheme, and no unexplained `ralph` brand residue in the tracked repo surfaces

## What Good Looks Like
- `Quality bar:` the rename is not a naive string replace; it preserves historical evidence where appropriate, keeps a bounded compatibility plan where needed, and leaves the repo with fewer execution concepts than before

## Proof Target
- `Reviewer-visible proof:` a repo-wide scan after implementation shows no live public `ralph` entrypoints or `.ralph/`-first runtime guidance outside intentionally preserved historical/archive contexts, and the replacement execution story reads coherently end to end

## Plan

### Pitch
- `Req:` remove the `ralph` name from the live harness and stop teaching a runtime surface the user no longer wants
- `Bet:` the highest-value change is to collapse public execution naming onto the already stronger `impl` and ticket-first surfaces, while giving legacy runtime selectors a bounded migration path
- `Win:` the harness becomes easier to reason about and less burdened by prototype-era branding and runtime residue

### Recommendation
- `Best:` retire `ralph` as a public surface, collapse its surviving execution semantics into `$impl`, adopt the neutral `.harness/` runtime naming, and keep only short-lived compatibility shims where they are needed to avoid unsafe breakage
- `Why:` the current public contracts overlap too much to justify two separate execution skills, and `.harness/` plus one public `$impl` surface is simpler to teach and reason about
- `Tradeoff accepted:` the migration will touch many docs/specs/tests at once and may need a transitional alias layer for runtime selectors before compatibility can be fully deleted

### B -> A
- `Before:` the repo teaches `impl`, `impl-plan`, and `ralph`; `.ralph/` still appears as runtime state; multiple docs still describe Ralph-specific flows and invariants
- `After:` one public execution story remains under `$impl`, `.harness/` becomes the neutral runtime surface, and any `ralph` residue is clearly marked as temporary compatibility rather than canonical behavior
- `Outcome:` the harness no longer carries prototype naming debt as a first-class concept

### Delta
- `Touch:` runtime docs, stop-hook/runtime helpers, skill names and references, ticket/docs guidance, and compatibility selectors
- `Keep:` ticket-first execution, review-gated completion, visible worker lanes, and any historical records that should stay historically faithful
- `Change:` public naming, runtime path guidance, and compatibility policy
- `Delete/Avoid:` avoid a blind repo-wide replace that loses historical context or preserves dead aliases indefinitely

### Core Flow
```pseudo
inventory every live public ralph surface
choose the canonical replacement names and runtime path policy
set `.harness/` as the canonical runtime directory and treat `.ralph/` as compatibility-only
collapse public `$ralph` behavior into `$impl`
rename tracked public surfaces and add bounded compatibility shims only where required
update docs/tests/validators to the new canonical story
prove the repo no longer teaches ralph as a live harness concept
```

### Proof
- `P1:` public docs and skills teach one execution surface under `$impl` without `ralph` branding
- `P2:` runtime helpers and selectors have an explicit migration policy instead of ambient `.ralph/` dependence, with `.harness/` documented as the canonical directory
- `Risk:` a broad rename accidentally breaks compatibility or muddies historical records
- `Rollback:` keep narrow runtime/code compatibility fallbacks where needed and mark archived/historical references as preserved context rather than canonical guidance

### Plan Review
- `Refs:` `README.md`, `tickets/README.md`, `docs/specs/ralph-runtime-surface.md`, `docs/specs/harness-techniques.md`, `skills/impl/SKILL.md`
- `Scope:` public rename plus runtime-surface simplification, including collapse of `$ralph` into `$impl`
- `Proof:` repo-wide `rg` scan, doc-parity check, and ticket-metadata validation after the migration
- `Guardrails:` preserve history intentionally, do not leave dual canonical names, and do not ship an unbounded compatibility layer
- `Fixes:` remove the brand debt and runtime ambiguity without inventing a second migration backlog

### Options Appendix
- `Option 1:` keep `ralph` and only document it better
- `Pros:` smallest implementation surface
- `Cons:` preserves the name and runtime residue the user wants gone; overlap with `impl` remains
- `Why not chosen:` it does not solve the actual problem
- `Option 2:` retire `ralph` publicly, collapse it into `impl`, move to neutral runtime naming, and keep temporary compatibility shims
- `Pros:` best balance of clarity and safety; removes overlap while keeping migration explicit
- `Cons:` requires a careful inventory and broad but disciplined repo edits
- `Why not chosen:` recommended
- `Option 3:` hard-cut rename everything immediately with no compatibility layer
- `Pros:` fastest path to a clean end state
- `Cons:` higher breakage risk for scripts, hooks, and documented selectors that still expect legacy names
- `Why not chosen:` too sharp for a harness repo that still has active prototype surfaces

### Delegation
- `Need:` Not needed
- `Why:` user approved the next build slice directly
- `Artifact:` n/a

### Ask
- `Ready: yes`
- `Next:` implement the first migration pass with `.harness/` as the canonical runtime directory, collapse `$ralph` into `$impl`, and keep only bounded `.ralph/` compatibility fallbacks

### Ticket Move
- `Now:` `status: building`, `phase: building`
- `On approval:` approved by the 2026-04-10 user direction to use `.harness/`
- `Follow-ups:` any deeper runtime simplification beyond the rename should become a separate ticket after the public surface is clean
- `Blocked in building?:` no

## Acceptance Criteria
- [x] AC-1: Codexter no longer presents `ralph` as a live public execution skill or canonical runtime surface in tracked repo docs and skills
- [x] AC-2: the replacement execution naming and runtime directory policy are explicit, consistent, and documented across the canonical surfaces
- [x] AC-3: any required runtime/code compatibility aliases for legacy selectors or paths are narrow, documented, and marked temporary
- [x] AC-4: historical/archive references that keep `Ralph` for provenance are intentionally preserved and clearly non-canonical
- [x] AC-5: `$impl` is the only canonical public execution skill, and the separate public `skills/ralph` surface is removed

## Working Notes
- The highest-leverage problem is conceptual overlap, not just the folder name `.ralph/`.
- This should likely consume the existing execution-surface simplification direction in `docs/specs/harness-techniques.md` rather than introducing another public name.
- User chose `.harness/` on 2026-04-10 as the neutral replacement directory because it generalizes better than a Ralph-branded runtime path.
- User also chose on 2026-04-10 to collapse `$ralph` and `$impl` because their public responsibilities are now too similar to justify two public execution skills.
- First migration-pass hotspots from the current inventory: `README.md`, `tickets/README.md`, `bin/README.md`, `ARCHITECTURE.md`, `bin/stop_hook.py`, `bin/user_turn.py`, `skills/impl/scripts/tmux_helper.py`, and `docs/specs/ralph-runtime-surface.md`.
- Follow-on cleanup after the runtime-root slice: keep burning down remaining live `ralph` identity surfaces in README/spec links, compatibility env vars, prototype specs, and operator-facing messages until the only leftover `ralph` references are explicitly historical or compatibility-only.
- Public `skills/ralph` files are now removed. Remaining live residue is in handoff docs, runtime/spec file names, helper strings, env vars, and compatibility-focused code paths.
- Runtime bug found on 2026-04-10: stop-hook switched away from active `TASK-0046` work because `load_current_run()` still fell back to stale `.ralph/state/current-run.json`, which carried older `TASK-0026` / `TASK-0034` intent data.
- Fix shape for this slice: remove ambient `.ralph` fallback from `bin/user_turn.py` and `bin/stop_hook.py`, keep `.harness` as the only live runtime root, and purge the local `.ralph` runtime tree so stale legacy state cannot resolve as the active ticket again.
- Active user-facing cleanup since then: canonical docs now present the remaining `ralph-*` spec files as legacy references, and helper lane names now default to `impl-*` instead of `ralph-*`.
- Remaining residue is now mostly deeper compatibility/protocol naming:
  - `RALPH_RESULT`
  - `RALPH_RUN_STATE`
  - `RALPH_TICKET`
  - old spec/schema filenames that are explicitly marked legacy

## Implementation Notes
- Touched areas:
  - `bin/user_turn.py`
  - `bin/stop_hook.py`
  - `skills/impl/scripts/tmux_helper.py`
  - `bin/test_runtime_state.py`
  - `README.md`
  - `tickets/README.md`
  - `docs/specs/context-and-handoff-policy.md`
  - `docs/specs/ralph-orchestration-blueprint.md`
  - `docs/specs/ralph-flow-examples.md`
  - `bin/README.md`
  - `bin/AGENTS.md`
  - `PROJECT_RULES.md`
  - `config.toml.example`
  - `.gitignore`
  - `AGENTS.md`
  - `docs/MEMORY.md`
  - `docs/HISTORY.md`
- Reused patterns:
  - ticket-first execution
  - session-first runtime routing
  - bounded compatibility fallbacks for legacy runtime paths
- Guardrails:
  - no blind global replace
  - no infinite dual-name era
  - `.ralph/` remains fallback-only, not canonical

## Evidence
- [x] Tests
- [ ] Typecheck
- [ ] Lint
- [x] QA / manual verification

Validation details:
- `python3 -m unittest bin/test_runtime_state.py bin/test_stop_hook.py bin/test_tmux_helper.py`
- `python3 -m py_compile bin/stop_hook.py bin/user_turn.py skills/impl/scripts/tmux_helper.py`
- `python3 -m unittest bin/test_runtime_state.py`
- `python3 bin/check_doc_parity.py`
- `python3 tickets/scripts/check_ticket_metadata.py`
- `rg -n 'captured turn targets TASK-0034|ticket_id": "TASK-0026"' .harness/logs/stop-hook.jsonl .ralph/logs/stop-hook.jsonl`
  - confirmed the failure came from stale `.ralph` runtime state, not from `.harness`
- `rg -n '\bralph\b|Ralph|RALPH_|ralph-' README.md ARCHITECTURE.md docs/specs/README.md docs/specs/runtime-surface.md docs/specs/harness-techniques.md docs/specs/spec-first-execution-loop.md docs/specs/context-and-handoff-policy.md skills bin config.toml.example tickets/README.md --glob '!docs/specs/legacy/**' --glob '!tickets/archive/**' --glob '!docs/research/**' --glob '!experiments/**'`
  - active-surface hits are only explicit legacy `docs/specs/legacy/ralph-*` references
- `find .harness .ralph -maxdepth 3 -type f 2>/dev/null | sort`
  - only `.harness/logs/stop-hook.jsonl` remains; no `.ralph` runtime files remain

## Review Packet
- `work_type:` `["runtime","docs","migration"]`
- `search_scope:` `{changed_files: ["AGENTS.md", ".gitignore", "PROJECT_RULES.md", "README.md", "bin/AGENTS.md", "bin/README.md", "bin/stop_hook.py", "bin/test_runtime_state.py", "bin/user_turn.py", "config.toml.example", "docs/HISTORY.md", "docs/MEMORY.md", "docs/specs/context-and-handoff-policy.md", "docs/specs/ralph-flow-examples.md", "docs/specs/ralph-orchestration-blueprint.md", "skills/impl/scripts/tmux_helper.py", "skills/impl/SKILL.md", "docs/specs/harness-techniques.md", "docs/specs/ralph-runtime-surface.md"], related_files: ["tickets/README.md", "skills/deep-interview/SKILL.md", "skills/init-project/README.md"], invariants_checked: ["MEM-0022"], docs_checked: ["README.md", "tickets/README.md", "docs/specs/context-and-handoff-policy.md", "bin/README.md"]}`
- `reviewed_at:` `2026-04-10 02:04 +0100`
- `rubrics_used:` `["integration-readiness","evidence-quality","debloatability"]`
- `overall_score:` `3.8`
- `overall_threshold:` 4.0
- `overall_verdict:` pass
- `rerun_required:` false
- `evidence_quality:` pass
- `integration_readiness:` pass
- `traceability:` pass
- `freshness:` pass
- `hard_gate_failures:` []
- `finding_log:` `[]`
- `blocking_findings:` []
- `next_action:` `archive the completed rename ticket`

## Blockers
- none

## Handoff
- Current state: archived. `.harness/` is the live runtime root, `$impl` is the public execution surface, and former `ralph-*` docs/schemas now live only under `docs/specs/legacy/`.
- Resume from: no resume required unless a future ticket chooses to rename or delete the explicit legacy artifacts under `docs/specs/legacy/`.

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter. Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then move the ticket into `tickets/archive/` or set `status: done` briefly if you intentionally keep a short-lived visible completion state first.
