---
title: Functional UI QA Checklist Audit
owner: functional-ui
status: complete
kind: skill-audit
created_at: 2026-07-02
updated_at: 2026-07-02
mode: qa_checklist_design
---

# Functional UI QA Checklist Audit

## Behavior Delta

```text
edited_skill: skills/functional-ui
expected_behavior: functional-ui reads and applies reusable runtime guardrails
  for primary workspace priority, compact chrome, readable information, text
  overflow, balanced spacing and padding rhythm, ethical interaction patterns,
  accessibility, states, and workflow efficiency.
current_behavior: SKILL.md described workflow planning, diagnosis,
  comparable patterns, and handoff, but had no skill-local qa_checklist.md and
  no first-load pointer to preflight/final functional UI QA.
mode: qa_checklist_design
owner_surface: skills/functional-ui/qa_checklist.md plus compact SKILL.md
  frontmatter and todo pointers.
proof_required: check_skills.py --write, structure checklist review, and
  focused diff inspection.
```

## First Load Review

```text
first_load_review:
  line_count_before: 115
  line_count_after: 122
  kept_in_skill: frontmatter qa_checklist pointer and two todo gates
  moved_to_reference: detailed runtime guardrails kept in qa_checklist.md
  deleted_as_duplicate_or_rationale: none
  extra_sections_kept_with_reason: existing sections unchanged
  remaining_sections_over_budget: none
  proof_surface_fit: pass
  task_case_quality: pass
  anti_cheat_case_design: not_applicable
  qa_preflight_loaded: pass
  qa_finish_independence: pass for material work via reviewer prompt
  qa_gotcha_deduplication: pass
  project_specific_context_isolation: pass
  low_value_prose_scan: not_applicable
  verdict: pass
```

## Audit Notes

- The checklist has prevention value before execution and final-review value
  after execution.
- A follow-up spacing guardrail was added for even-looking padding and gaps
  without allowing chrome to bloat at the expense of the primary workspace.
- The new checks are not metrics or scalar scores; they remain binary runtime
  guardrails with evidence and fix/deferral notes.
- No eval task changed, so eval-to-QA sync is not required.
- `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  regenerated registries and passed skill/todo/template/eval checks, then
  failed on an unrelated root `AGENTS.md` doc reference:
  `missing local ref 'skills/tools' -> skills/tools`.
