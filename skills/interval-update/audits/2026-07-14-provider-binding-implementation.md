---
title: "Interval Update Provider Binding Implementation"
status: review
owner: interval-update
created_at: 2026-07-14
kind: implementation-audit
---

# Interval Update Provider Binding Implementation

## Claim

`interval-update` now resolves its work-evidence provider from
`farplane/bindings.yaml#integrations.kanban`, preserves configured filesystem
ticket behavior, routes Notion through a named private handle plus `ntn`, and
does not fall back to filesystem tickets when Notion access is unavailable and
filesystem policy is `exclude`.

## Before / After / Example

> **Before:** Interval always read `tickets/**` for work evidence and dedupe.
>
> **After:** Interval resolves a sanitized provider plan first; provider access
> failure is a source gap and explicit filesystem exclusion is a hard gate.
>
> **Example:** `provider: notion` plus `filesystem_ticket_policy: exclude` and
> unavailable `ntn` writes `ntn_unavailable` with `fallback: none`, even when a
> local `tickets/` directory exists.

## Changed Surfaces

- `skills/interval-update/SKILL.md`
- `skills/interval-update/qa_checklist.md`
- `skills/interval-update/references/interval-update.md`
- `skills/interval-update/templates/interval-context-bundle.md`
- `skills/interval-update/templates/interval-report.md`
- `skills/interval-update/evals/evals.json`
- `skills/interval-update/scripts/resolve_evidence_binding.py`
- `skills/interval-update/scripts/test_resolve_evidence_binding.py`
- `skills/init-advisor/references/BINDINGS_TEMPLATE.yaml`
- `farplane/bindings.yaml`
- `docs/farplane-framework/pulse-and-interval-loop.md`
- `bin/validators/check_farplane_project_files.py`
- `bin/validators/test_check_farplane_project_files.py`

## Evidence

- `uv run --with pytest python -m pytest -q skills/interval-update/scripts/test_resolve_evidence_binding.py skills/interval-update/scripts/test_metric_refresh.py bin/validators/test_check_farplane_project_files.py::test_bindings_accept_filesystem_and_notion_kanban_contracts bin/validators/test_check_farplane_project_files.py::test_notion_kanban_binding_cannot_enable_filesystem_fallback`
  - Result: `16 passed, 9 subtests passed`.
- `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  - Result: skill todo, registry, eval-query, doc-ref, capability, tier, and
    surface-budget checks passed.
- `python3 bin/validators/check_farplane_project_files.py --root .`
  - Result: `Farplane project file conventions OK` after regenerating the
    ignored project snapshot for the binding hash.
- `python3 -m py_compile skills/interval-update/scripts/resolve_evidence_binding.py`
  and `python3 -m json.tool skills/interval-update/evals/evals.json`
  - Result: pass.
- `git diff --check`
  - Result: pass.
- `python3 skills/skill-maintenance/scripts/install_selected_skills.py --skill interval-update --json`
  - Result: installed the repo-owned `interval-update` source into the live
    Codex skill path through the canonical installer.

## Review Focus

1. Does the implementation satisfy filesystem and Notion-bound projects
   without introducing a project wrapper or provider client duplication?
2. Is the no-filesystem-fallback guarantee complete across evidence, dedupe,
   and recovery admission?
3. Can any raw private Notion ID, URL, token, or payload enter tracked output?
4. Are report-first, no-execution, and side-effect gates preserved?
5. Are the tests and eval cases sufficient for the claimed behavior?

## Known Worktree Context

The checkout already contained broad unrelated in-progress changes, including
the interval metric-refresh path and project-file schema migration. This patch
preserves and builds on those changes; review should not attribute or revert
unrelated diffs.

## Independent Review

Initial reviewer verdict: `TAS-C — block readiness`.

- Fixed blocker: `filesystem_tickets` plus `filesystem_ticket_policy: exclude`
  now returns `filesystem_tickets_excluded`, exposes no ticket coordinates,
  and has a dedicated regression test.
- Fixed overclaim: Notion handle/CLI resolution now returns
  `access_ready: null` with `access_check: required_compact_ntn_query`; only a
  successful bounded query may establish provider evidence access.
- Remaining finish gate: run focused agent evals and request reviewer rerun.

First native eval run was infrastructure-invalid because local Codex CLI
`0.142.5` rejected the configured `gpt-5.6-sol` model. The explicit
`gpt-5.4-mini` rerun executed both cases and returned one TAS-C and one TAS-B,
identifying first-load omissions: bindings-first/no-execution wording for the
filesystem answer and available report/metric evidence wording for the Notion
gap answer. Those guarantees were promoted into `SKILL.md`; the same cases are
being rerun as the finish gate.

Final focused behavior evidence:

- Notion unavailable/no-fallback:
  `.farplane/evals/runs/20260713-184355-provider-binding-20260714-final/summary.json`
  - Verdict: TAS-A pass.
- Filesystem binding/report-first/no-execution:
  `.farplane/evals/runs/20260713-184613-provider-binding-20260714-filesystem-gpt54/summary.json`
  - Verdict: TAS-A pass.
- The failed `gpt-5.6-sol` run is retained as infrastructure evidence only; it
  never executed an agent turn and is not counted as a behavior verdict.

Eval query QA: `check_eval_queries.py --root .` passed. The filesystem prompt
was revised to ask the natural run-level question (evidence, writes, and work
started) instead of narrowly asking only how evidence is resolved.

Final independent reviewer verdict: `TAS-A — pass-ready` across skill contract,
code quality, eval quality, evidence quality, and integration readiness. No
remaining blockers. Successful live Notion retrieval remains intentionally
runtime-dependent on the bounded compact `ntn` query and is not claimed by
configuration discovery alone.
