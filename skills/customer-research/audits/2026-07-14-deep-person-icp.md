---
skill: "customer-research"
change: "deep-person-icp"
created_at: "2026-07-14"
---

# Deep Person ICP Skill Audit

## Summary

Added deep ICP mode to the existing customer-research skill rather than creating
a duplicate skill. The mode turns public or operator-supplied professional
signals into sourced buyer/problem hypotheses, conversation strategy, and
correction-seeking questions.

## Changed Files

- `SKILL.md`
- `templates/deep-person-icp.md`
- `examples/deep-person-icp/example.md`
- `evals/evals.json`

## Checklist Verdicts

- skill-creator ownership: pass. Existing `customer-research` owns known-person
  research and conversation prep.
- first-load sufficiency: pass. Deep ICP trigger, source boundaries, todo
  branch, template route, gates, and gotchas are in `SKILL.md`.
- conservative scaffolding: pass. Added one template, one example, and one eval
  case; no scripts or duplicate skill package.
- domain specificity: pass. The branch names professional signal categories,
  buyer/problem hypotheses, objections, language mirroring, and correction
  questions.
- private dossiering guardrail: pass. The skill requires public or supplied
  professional evidence only and rejects bypassing LinkedIn limits or private
  content.

## Skill Structure QA

```text
first_load_review:
  line_count_before: 156
  line_count_after: 190
  kept_in_skill: trigger/context, signature gate, todo branch, template route, gotchas
  moved_to_reference: none
  deleted_as_duplicate_or_rationale: none
  extra_sections_kept_with_reason: none
  remaining_sections_over_budget: none expected
  proof_surface_fit: eval case plus skill validator
  task_case_quality: one safety-sensitive deep ICP eval added
  anti_cheat_case_design: prompt asks for deep research without naming template sections directly
  qa_preflight_loaded: skill-creator and skill-maintenance QA loaded
  qa_finish_independence: inline review; no subagent used because scope is a narrow existing-skill branch
  qa_gotcha_deduplication: concise gotchas only; detailed body shape lives in template
  project_specific_context_isolation: synthetic example only, no private project target embedded
  low_value_prose_scan: pass; added prose changes execution or safety behavior
  verdict: pass_with_validator_blocker
```

## Proof

- `python3 -m json.tool /Users/kenjipcx/.codex/skills/customer-research/evals/evals.json >/dev/null`
  passed.
- `wc -l /Users/kenjipcx/.codex/skills/customer-research/SKILL.md` reports
  `190`, under the approximate 250-line first-load budget.
- `rg` inspection confirmed exactly one visible todo marker pair and required
  headings: `Context`, `Todo List`, `Templates`, `Gotchas`, `Reference Map`,
  and `Output`.
- `rg` inspection confirmed the deep ICP template and example expose matching
  sections for source snapshot, professional narrative, signal map, priorities,
  likely problems, buying triggers, objections, language, outreach fit,
  conversation strategy, questions, and source notes.

Blocked command:

```bash
python3 /Users/kenjipcx/.codex/skills/skill-maintenance/scripts/check_skills.py --write
```

Result:

```text
RuntimeError: could not find Farplane repo root
```

Reason: this installed skill copy does not include the validator repo root
expected by `check_skills.py` (`bin/validators/sync_skill_registry.py` plus a
repo-owned `skills` directory). The behavior proof is therefore direct
structural inspection plus the new eval case, not a full registry validation
run.
