---
title: "Retire skill QA sidecars"
status: pass
owner: skill-maintenance
created_at: 2026-08-24
updated_at: 2026-08-24
context_ref: docs/features/FEAT-0057-skill-local-qa-checklist-artifacts.md
review_focus: skill-contract
overall_tas: TAS-A
verdict: pass
---

# Retire Skill QA Sidecars

## Decision

Delete `skills/*/qa_checklist.md` and remove `qa_checklist` plus `eval` from
skill frontmatter. The feature decision record is
[`FEAT-0057`](../../../docs/features/FEAT-0057-skill-local-qa-checklist-artifacts.md).

## Before

- 64 package-local QA sidecars contained 4,418 lines of duplicated preflight
  and final-check prose.
- 63 frontmatter rows repeated a QA path and 82 repeated an eval path already
  discoverable from the package filesystem.
- Registry, graph, rollout, and budget projections treated those duplicate
  fields as active contract inputs.

## After

- Normal guardrails live in Golden Workflow Node `Rule`/`Assert` blocks.
- `evals/evals.json` is discovered by path and projected as generated `eval`.
- `skill_ui` is the only optional local surface declared in skill frontmatter.
- `check_skill_frontmatter.py` rejects either legacy frontmatter field and any
  new `qa_checklist.md` sidecar.
- Budgeting counts only Todo List nodes and eval rows.

## Proof

- `python3 -m unittest bin/validators/test_check_skill_frontmatter.py bin/validators/test_check_skill_surface_budget.py bin/validators/test_sync_skill_registry.py bin/tests/test_farplane_harness_health.py bin/tests/test_farplane_skill_rollout.py skills/skill-maintenance/scripts/test_generate_skill_graph.py skills/skill-maintenance/scripts/test_generate_template_intelligence.py`
- `python3 bin/farplane.py lint skills`
- `python3 bin/farplane.py skills sync`
- `python3 docs/features/validate_features.py --write`
- `python3 bin/validators/sync_template_registry.py --write`

## Reintroduction Guard

The feature record preserves the decision, while the typed linter enforces the
actual boundary. A future author receives an error that directs the guardrail to
the Todo List, eval, validator, QA, or review owner instead of recreating the
sidecar.

## Independent Review

The initial review returned `TAS-B`: the staged generated report was stale and
a separate command migration had not yet been classified. The command migration
is now its own commit and `farplane skills sync` has regenerated the report.
Read-only skill and harness graph checks plus the complete typed lint passed;
final independent review returned `TAS-A` / `pass` with no remaining finding.
