---
skill: "customer-research"
change: "company-hiring-signals"
created_at: "2026-07-14"
verdict: "pass"
---

# Company Hiring Signals Audit

## Behavior Delta

Deep ICP research now inspects the target company's hiring footprint before
solution shaping and preserves role status, recency, source access, capability
themes, alternative explanations, and falsifiers.

## Owner Boundary

- `customer-research` owns evidence collection and hiring interpretation.
- `research:source-synthesis` remains the method when several hiring sources
  need normalization.
- `solution-shaping` consumes the resulting problem hypotheses; it does not own
  the hiring scan.

## Representative Proof

The ERTH trial produced three deliberately distinct signals:

- no current job cards surfaced on the authenticated LinkedIn company Jobs tab;
- an indexed Ecommerce Manager listing was closed and approximately one year old;
- a founder-posted strategic finance role dated 2025-05-20 had unknown current
  status and therefore could not be presented as an active vacancy.

The project report records those signals separately and uses them to support a
correction-seeking finance/reporting hypothesis rather than a vacancy-derived
pitch.

## Guardrails

- Hiring proves recruiting intent at a point in time, not dysfunction.
- A no-jobs result records inspected coverage but does not prove no openings.
- Browser inspection remains read-only and excludes applications, recruiter
  contact, social actions, credentials, bulk extraction, and monitoring.

## Validation

- `python3 -m json.tool skills/customer-research/evals/evals.json` passed.
- `python3 skills/skill-maintenance/scripts/check_skills.py --write` passed all
  skill-system, registry, template, capability, eval-query, and doc-reference
  checks across 120 skill rows.
- `install_selected_skills.py --skills customer-research` completed and a
  recursive diff between the source and `~/.codex/skills/customer-research`
  reported exact parity.
- Representative ERTH proof preserved `status_unknown`, `closed_or_stale`, and
  `none_surfaced` separately and did not convert hiring into an asserted pain.
- Independent reviewer verdict: `TAS-A`, `pass`, no hard-gate failures, no rerun
  required. One low stale-audit finding was repaired by this receipt.

## Skill Structure QA

```text
first_load_review:
  line_count_before: 219
  line_count_after: 238
  kept_in_skill: conditional hiring trigger, source coverage, status semantics, finish gate, false-inference gotcha
  moved_to_reference: detailed output fields remain in templates/deep-person-icp.md
  deleted_as_duplicate_or_rationale: none
  extra_sections_kept_with_reason: none
  remaining_sections_over_budget: none
  eval_guardrail_sync: company-hiring regression case added; no target qa_checklist exists
  source_owner: Farplane skills/customer-research
  installed_parity: pass
  reviewer: TAS-A pass
  verdict: pass
```
