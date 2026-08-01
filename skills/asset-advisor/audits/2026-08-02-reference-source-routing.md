---
title: Reference Source Roles And Landing Media Routing Audit
owner: asset-advisor
status: complete
kind: skill-audit
created_at: 2026-08-02
updated_at: 2026-08-02
mode: behavior_hardening
ticket: TASK-9004
---

# Reference Source Roles And Landing Media Routing Audit

## Behavior Delta

```text
edited_skills: asset-advisor, landing-page, ingest-content
before: inspiration sources had rights notes but no stable usage-role axis,
  prompt compilation had no acceptance-order receipt, landing routing was
  implicit, and discovery wrappers could remain the durable source.
after: source use and rights are classified independently; inspired generation
  accepts transferable moodboard traits before prompt compilation; landing
  pages route missing/reference-led media through Asset Advisor while complete
  licensed inputs record a skip; ingestion prefers canonical originals and
  preserves discovery provenance.
owner_surface: asset-advisor owns source roles and prompt ordering;
  landing-page owns its conditional call boundary; ingest-content owns source
  canonicalization and Resource Bank/Tasty Pack persistence.
non_owners: ad-advisor and content-impl-plan remain unchanged because neither
  owns reference classification or landing-specific media routing.
```

## First Load Review

```text
first_load_review:
  kept_in_skill: role/rights gate, moodboard acceptance order, landing route
    and skip boundary, canonical-source ingestion rule
  moved_to_reference: source-role definitions, established-source examples,
    and the detailed moodboard receipt
  deleted_as_duplicate_or_rationale: none
  remaining_sections_over_budget: none introduced by this change
  proof_surface_fit: focused evals plus QA checks
  qa_preflight_loaded: pass
  query_spoiler_verdict: pass
  project_specific_context_isolation: pass
  verdict: pass
```

## Proof Notes

- Owner-scoped baseline: `tickets/TASK-9004/artifacts/eval-runs/20260801-180255-task-9004-owner-baseline/summary.json` (1/5 pass; the asset, landing, and Pinterest rows were C).
- Final asset candidate: `tickets/TASK-9004/artifacts/eval-runs/20260801-182127-task-9004-owner-candidate-v6/summary.json` (A).
- Final landing candidate: `tickets/TASK-9004/artifacts/eval-runs/20260801-181518-task-9004-owner-candidate-v3/summary.json` (A).
- Final Pinterest candidate: `tickets/TASK-9004/artifacts/eval-runs/20260801-181931-task-9004-owner-candidate-v5/summary.json` (A).
- Comparison receipt: `tickets/TASK-9004/artifacts/eval-comparison.md`.
- `python3 skills/eval/scripts/check_eval_queries.py --root .`: pass.
- `python3 skills/skill-maintenance/scripts/check_skills.py --write`: registry,
  todo-tier, and Tier 0 checks passed; the aggregate command remains nonzero on
  pre-existing `content-impl-plan` QA/eval surface-budget violations outside
  TASK-9004 scope.
