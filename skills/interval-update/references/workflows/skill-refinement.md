---
title: "Skill Refinement Workflow"
status: active
owner: interval-update
kind: workflow-reference
template_uses:
  skill-template: "0.3.2"
---

# Skill Refinement Workflow

## Context

Use this workflow when an interval needs to compact already-hardened skill
surfaces. Refinement is intentionally separate from hardening: fresh repeated
failures need immediate evals, gotchas, checklist guardrails, or tickets before
any prose-shortening pass.

This workflow selects and routes refinement. It does not edit skills directly
unless the parent interval explicitly enters a `skill-maintenance` subtask.

## Workflow Signature

```text
skill_refinement(context_bundle, review_window, planning_window,
                 workflow_findings?, cap?)
  -> refine_skill_handoffs
   + compaction_candidates
   + coverage_risks
   + deferred_refinement
   + source_gaps

state: reads(context_bundle, skills/**/audits?, edited_skill/eval_task.json?,
             edited_skill/qa_checklist.md?, usage_results?, interval_reports?);
       writes(parent_interval_update_report_section)
gates: hardening_exists_or_deferred; behavior_guardrails_preserved;
       owner_surface_named; coverage_risk_named; cap_respected
routes: skill-maintenance:refine_skill | eval | review | direct no-change
fails: delays urgent hardening; deletes guardrails without proof; treats shorter
       skill text as sufficient evidence; creates unbounded compaction work
```

## Source Contract

Default sources from the context bundle:

- skill-local audits and recent interval reports that identify bloat,
  duplicated gotchas, old eval cases, or first-load prose drift.
- `eval_task.json` and `qa_checklist.md` for candidate skills when present.
- usage results, review notes, or validation output that show which behavior
  guardrails are still needed.

## Todo List

- [ ] 1. Bind refinement candidates.
  - [ ] Confirm `review_window`, `planning_window`, and `cap`.
  - [ ] Read skill-local audits, evals, QA checklists, and usage results only for
        candidate skills.
  - [ ] Mark missing optional sources as source gaps.
- [ ] 2. Separate hardening from refinement.
  - [ ] Defer any fresh repeated failure to `skill_hardening`.
  - [ ] Continue only when immediate guardrails already exist or the candidate
        is explicitly behavior-preserving.
- [ ] 3. Route compaction.
  - [ ] Route duplicate evals, overlapping gotchas, long examples, stale
        rationale, or oversized first-load text to
        [skill-maintenance](../../../skill-maintenance/SKILL.md) with
        `mode: refine_skill`.
  - [ ] Route coverage-risk questions to [eval](../../eval/SKILL.md) or
        [review](../../review/SKILL.md).
  - [ ] Mark weak, unclear, or low-value candidates as deferred.
- [ ] 4. Bound the work.
  - [ ] Default cap is 3 refinement handoffs per weekly run.
  - [ ] Prefer one representative skill or one clearly related skill cluster.
- [ ] 5. Record the result.
  - [ ] Write refine-skill handoffs, coverage risks, deferred candidates, and
        source gaps into the interval report.

## Output

```text
refine_skill_handoffs:
  - edited_skill:
    evidence_refs:
    compaction_goal:
    proof_required:
compaction_candidates:
coverage_risks:
deferred_refinement:
source_gaps:
```
