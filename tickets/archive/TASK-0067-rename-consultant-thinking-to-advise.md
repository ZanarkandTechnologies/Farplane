---
ticket_id: TASK-0067
title: rename advisory skill to advise
phase: complete
status: done
owner: codex
claimed_by:
priority: medium
depends_on: []
blocked_by: []
ready: false
approval_required: false
created_at: 2026-04-13T19:05:00Z
updated_at: 2026-04-13T19:19:00Z
next_action: none; ticket archived after the public `advise` rename landed, live references were updated, and later review confirmed any remaining old-name hits live only in historical/runtime artifacts
last_verification: `rg -n -i --no-ignore --hidden --glob '!**/.git/**' "consultant-thinking|Consultant Thinking|consultant thinking" .`; `python3 tickets/scripts/check_ticket_metadata.py`; `git diff --check -- agents/reviewer.toml templates/global/AGENTS.md docs/specs/review-gates.md skills/impl/references/stop-hook-routing.md skills/advise/SKILL.md skills/advise/README.md skills/advise/AGENTS.md docs/MEMORY.md docs/HISTORY.md tickets/archive/TASK-0067-rename-consultant-thinking-to-advise.md`; manual inspection of `skills/advise/*`, `agents/reviewer.toml`, `templates/global/AGENTS.md`, active tickets, and the remaining historical/runtime old-name hits
linked_docs:
  - skills/advise/SKILL.md
  - skills/advise/README.md
  - skills/advise/AGENTS.md
  - templates/global/AGENTS.md
  - agents/reviewer.toml
  - docs/specs/review-gates.md
  - skills/impl/references/stop-hook-routing.md
  - docs/MEMORY.md
  - docs/HISTORY.md
---

# TASK-0067: rename advisory skill to advise

## Summary
Rename the public advisory skill to `advise` so the entrypoint name matches its
actual job.

## Scope
- In:
  - rename the skill directory and skill metadata
  - update live repo contracts that invoke the skill by name
  - log the public-surface rename in durable docs
- Out:
  - changing the skill's decision workflow
  - renaming historical append-only references in `docs/HISTORY.md` or `docs/TROUBLES.md`

## Acceptance Criteria
- [x] AC-1: the skill lives at `skills/advise/` and its metadata name is `advise`
- [x] AC-2: live contracts and docs invoke `$advise` instead of the prior advisory-skill name
- [x] AC-3: durable docs capture the rename and historical logs remain untouched

## Working Notes
- This is a public naming cleanup, not a behavior change.
- Historical append-only references may keep the prior name for accuracy.
- Live references updated:
  - `templates/global/AGENTS.md`
  - `agents/reviewer.toml`
  - `docs/specs/review-gates.md`
  - `skills/impl/references/stop-hook-routing.md`
- Durable rename writeback added to `docs/MEMORY.md` and `docs/HISTORY.md`.

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [x] QA / manual verification
- Verification notes:
  - `rg --no-ignore` is required in this repo because `tickets/**/*.md` is ignored; ignore-respecting searches undercount rename residue.
  - `git diff --check` passes on all changed live files.
  - `python3 tickets/scripts/check_ticket_metadata.py` passes after ticket creation.

## Review Packet
- Scores use the anchored `1.0`-to-`5.0` rubric scale.
- `work_type:` `["skills", "docs", "contracts"]`
- `search_scope:` `{changed_files: ["skills/advise/SKILL.md", "skills/advise/README.md", "skills/advise/AGENTS.md", "templates/global/AGENTS.md", "agents/reviewer.toml", "docs/specs/review-gates.md", "skills/impl/references/stop-hook-routing.md", "docs/MEMORY.md", "docs/HISTORY.md", "tickets/archive/TASK-0067-rename-consultant-thinking-to-advise.md"], related_files: ["docs/TROUBLES.md", "tickets/TASK-0060-define-loop-mode-separate-from-impl.md", "tickets/TASK-0065-add-stop-hook-obvious-next-step-gate.md"], invariants_checked: ["MEM-0036", "MEM-0037"], docs_checked: ["templates/global/AGENTS.md", "docs/specs/review-gates.md", "skills/impl/references/stop-hook-routing.md", "docs/MEMORY.md", "docs/HISTORY.md", "docs/TROUBLES.md"]}`
- `reviewed_at:` `2026-04-13 20:19 +0100`
- `rubrics_used:` `["code-quality", "integration-readiness", "evidence-quality"]`
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
- `rubric_sections:`
  - `{name: "code-quality", score: 4.4, threshold: 4.0, pass: true, dimension_scores: {modularity-reusability: 4.0, bloatability: 4.5, readability: 4.5, boundary-clarity: 4.5, error-handling: 4.0, maintainability: 4.5}, findings: ["The rename is localized and consistent across the live ownership surfaces without changing the advisory workflow."], next_action: "None."}`
  - `{name: "integration-readiness", score: 4.2, threshold: 4.0, pass: true, dimension_scores: {integration-safety: 4.0, contract-correctness: 4.0, dependency-readiness: 4.0, coupling-risk: 4.0, merge-readiness: 5.0}, findings: ["The primary live contracts were renamed, but later review showed ignored ticket surfaces still needed follow-up cleanup."], next_action: "Use `rg --no-ignore` for rename verification in this repo and patch live ticket drift."}`
  - `{name: "evidence-quality", score: 4.3, threshold: 4.0, pass: true, dimension_scores: {sufficiency: 4.0, reproducibility: 4.5, traceability: 4.5, consistency: 4.0, inspectability: 4.5}, findings: ["Search output, metadata validation, and diff cleanliness provide enough proof for a rename-only change."], next_action: "None."}`
- `blocking_findings:` `[]`
- `next_action:` `archive the completed ticket`

## Blockers
- none

## Handoff
- Current state: live repo contracts use `advise`, the skill module has moved to `skills/advise/`, and later follow-up review cleaned additional active ticket drift while leaving historical/runtime artifacts intact.
- Resume from: no further work required.
