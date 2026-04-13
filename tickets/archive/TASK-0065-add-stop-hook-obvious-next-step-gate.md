---
ticket_id: TASK-0065
title: add stop hook obvious next step gate
phase: complete
status: done
owner: codex
claimed_by:
priority: high
depends_on: []
blocked_by: []
ready: false
approval_required: false
created_at: 2026-04-13T17:20:00Z
updated_at: 2026-04-13T18:31:15Z
next_action: none; closeout complete and ticket archived after confirming the targeted Stop-hook tests and review packet were sufficient for this slice
last_verification: closeout pass decided no broader replay was required beyond the existing targeted coverage; verification remains `python3 -m unittest bin.test_stop_hook`, `python3 tickets/scripts/check_ticket_metadata.py`, and `git diff --check -- bin/stop_hook.py bin/stop_hook_output.schema.json bin/test_stop_hook.py agents/reviewer.toml docs/specs/review-gates.md skills/impl/references/stop-hook-routing.md bin/AGENTS.md docs/MEMORY.md docs/TROUBLES.md docs/HISTORY.md tickets/TASK-0065-add-stop-hook-obvious-next-step-gate.md`
linked_docs:
  - bin/stop_hook.py
  - agents/reviewer.toml
  - docs/specs/review-gates.md
  - skills/impl/references/stop-hook-routing.md
---

# TASK-0065: add stop hook obvious next step gate

## Summary
Strengthen the Stop hook completion gate so the reviewer must explicitly judge
whether an obvious in-scope next step still exists before the hook can route to
the orchestrator.

## Scope
- In:
  - reviewer completion-gate fields for obvious-next-step judgment
  - stop-hook parsing and validation for the new fields
  - reviewer prompt guidance to ground completion review through the `review`
    skill contract and return one consultant-style best next step
  - explicit dollar-syntax ordering for `$review` then `$advise`
  - docs and tests for the stronger completion-routing rule
- Out:
  - adding a fourth Stop-hook role
  - broad input-hook foresight systems
  - changing tmux/runtime ownership behavior

## Acceptance Criteria
- [x] AC-1: reviewer completion-gate output includes explicit obvious-next-step fields
- [x] AC-2: stop hook refuses completion routing when reviewer says an obvious next step still exists
- [x] AC-3: targeted Stop-hook tests cover the new gate behavior
- [x] AC-4: review-gate docs explain that reviewer, not the main model, is the authority for orchestrator routing

## Working Notes
- The user does not trust the main model to reliably decide it is done enough to
  route; reviewer judgment must be the deciding gate.
- Keep the hybrid shape: deterministic impl judge, one stronger reviewer, and
  orchestrator only after explicit reviewer approval.
- The user also wants continuation advice to come from the reviewer with fresh
  eyes, grounded through the `review` skill, instead of appending a vague
  proactive instruction at the end of the stop-hook output.
- The skill ordering is now explicit: `$review` first for grounded judgment,
  `$advise` second for the single best immediate next step.

## Evidence
- [x] Tests
- [ ] Typecheck
- [ ] Lint
- [x] QA / manual verification

## Review Packet
- Scores use the anchored `1.0`-to-`5.0` rubric scale.
- `work_type:` `["runtime", "hooks", "tests"]`
- `search_scope:` `{changed_files: ["bin/stop_hook.py", "bin/stop_hook_output.schema.json", "bin/test_stop_hook.py", "agents/reviewer.toml", "docs/specs/review-gates.md", "skills/impl/references/stop-hook-routing.md", "bin/AGENTS.md", "docs/MEMORY.md", "docs/TROUBLES.md", "docs/HISTORY.md", "tickets/TASK-0065-add-stop-hook-obvious-next-step-gate.md"], related_files: ["docs/specs/runtime-surface.md", "skills/impl/SKILL.md", "skills/review/SKILL.md", "skills/advise/SKILL.md", "agents/orchestrator.toml"], invariants_checked: ["MEM-0032", "MEM-0034", "MEM-0035"], docs_checked: ["docs/specs/review-gates.md", "skills/impl/references/stop-hook-routing.md", "skills/review/SKILL.md", "skills/advise/SKILL.md", "bin/AGENTS.md", "docs/MEMORY.md", "docs/TROUBLES.md", "docs/HISTORY.md"]}`
- `reviewed_at:` `2026-04-13 18:27 +0100`
- `rubrics_used:` `["code-quality", "integration-readiness", "evidence-quality"]`
- `overall_score:` `4.4`
- `overall_score:` `4.5`
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
- `next_action:` `none; targeted coverage and current review packet were sufficient, so the ticket can stay archived unless a later replay-specific ticket reopens this area`

## Handoff
- Current state: documenting closeout finished; no broader replay was run in this pass because the ticket already had targeted Stop-hook tests, docs writeback, and a passing review packet.
- Resume from: reopen only if a separate replay-focused ticket is created for broader premature-completion fixtures.
