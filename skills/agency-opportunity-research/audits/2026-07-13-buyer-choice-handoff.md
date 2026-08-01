---
skill: agency-opportunity-research
date: 2026-07-13
change_type: structure_update
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/agency-opportunity-research/SKILL.md@191-lines
after_ref: skills/agency-opportunity-research/SKILL.md@204-lines
proof_artifacts:
  - tickets/TASK-0346/ticket.md
  - Valefor:tickets/TASK-0033/ticket.md
eval_required: yes
---

# Buyer-Choice Handoff Audit

## Behavior Delta

- Before: competitor research could record approaches and a differentiation
  hypothesis but had no stable buyer-choice handoff to accepted demo work.
- After: the reusable opportunity case selects dated, criteria-bounded
  benchmark categories, compares them with custom execution on equal fields,
  and sends the public conclusion directly to the caller's landing surface.
- Duplication rule: one optional deeper landscape ledger is allowed only when
  evidence reuse justifies it; a buyer-choice sidecar that repeats the landing
  is rejected.

## Structure Review

```text
first_load_review:
  line_count_before: 191
  line_count_after: 204
  kept_in_skill: selection gates, equal comparison fields, landing handoff, duplication fail
  moved_to_reference: provider-specific evidence remains caller-owned
  deleted_as_duplicate_or_rationale: none
  extra_sections_kept_with_reason: none
  remaining_sections_over_budget: none
  proof_surface_fit: QA plus behavior eval plus caller exemplar
  task_case_quality: existing industry premise case now covers the handoff
  anti_cheat_case_design: prompt does not reveal the expected structure
  qa_preflight_loaded: pass
  qa_finish_independence: pass; independent re-review TAS-A
  qa_gotcha_deduplication: pass
  project_specific_context_isolation: pass
  low_value_prose_scan: pass; additions change gates, execution, or proof
  verdict: pass
```

## Validation

- JSON parsing: pass.
- Farplane skill-system validation: pass, including registry, templates, todo
  tiers, surface budget, capabilities, eval queries, and 1,888 doc refs.
- Supported installer plus source/live skill, QA, template, and eval equality:
  pass.
- Independent review: initial TAS-B rejected two unsupported vendor-category
  claims in the caller exemplar; the repaired labels passed re-review at TAS-A.
