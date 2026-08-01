---
skill: customer-research
change: person-signal-card
ticket_id: TASK-0421
created_at: 2026-07-31
verdict: candidate_ready_for_agent_qa
---

# Person Signal Card Audit

## Before / After / Example

> **Before:** Deep Person ICP rendered 13 body sections and the synthetic
> example was 168 lines. Identity, achievement, hiring, language, objections,
> outreach fit, and conversation strategy competed for attention.
>
> **After:** The template has one opening paragraph, one bounded Person Signal
> Card, and one compact evidence/unknowns block. The example is 87 lines.
>
> **Example:** Lena Ortiz is oriented in one sourced paragraph, followed by
> three goals/pressures, two problems, three relationship surfaces, one first
> move, three correction questions, and four evidence rows.

## Preserved Gates

- Public, supplied, or explicitly authorized professional evidence only.
- Rendered browser inspection remains read-only and access-labeled.
- Hiring surfaces/status/recency remain required when a company is bound.
- Snippet-only and single-interaction evidence cannot receive high confidence.
- Problems remain testable hypotheses with alternatives and falsifiers.
- Empty CRM uses `entity_refs: []`; no write or compile without exact approval.

## Skill Structure QA

```text
first_load_review:
  authored_file_structure: pass; SKILL owns selection/gates, template owns body shape
  kept_in_skill: opening order, bounded groups, evidence/safety gates, first-move hierarchy
  moved_to_reference: bulky evidence remains linked rather than copied
  deleted_as_duplicate_or_rationale: category-complete output requirements
  extra_sections_kept_with_reason: none
  proof_surface_fit: focused behavior eval plus agent QA and final review
  task_case_quality: dense synthetic person, auth-wall, authorized browser, hiring, privacy, CRM
  anti_cheat_case_design: natural operator prompts; query lint passes
  qa_preflight_loaded: skill-maintenance and eval QA loaded
  qa_finish_independence: delegated agent QA and reviewer required
  qa_gotcha_deduplication: selection rules live in todo/gates; template holds layout
  project_specific_context_isolation: synthetic fixtures only
  low_value_prose_scan: added lines change ordering, bounds, safety, or output ownership
  golden_calibration_independence: not applicable
  lean_owner_reuse: existing customer-research deep mode and artifact type retained
  verdict: pass_candidate
```

## Behavior Evidence

- Comparable candidate: A / pass on
  `customer_research_dense_sources_priority_01`.
- Query-spoiler lint: pass.
- JSON and diff checks: pass.
- `check_skills.py --write`: registry generation passed; overall command remains
  nonzero only for the unrelated pre-existing `content-impl-plan` QA/eval
  surface-budget violations.

See
`tickets/TASK-0421/artifacts/evals/customer-research-baseline-vs-candidate/comparison.md`.
