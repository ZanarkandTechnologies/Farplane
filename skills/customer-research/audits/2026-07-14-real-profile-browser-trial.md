---
skill: "customer-research"
change: "real-profile-browser-trial"
target: "Mohamed Mo Tarek El-Fatatry"
created_at: "2026-07-14"
verdict: "pass_with_validator_blocker"
---

# Real Profile Browser Trial Audit

## Claim Under Test

The deep ICP route can turn a supplied public LinkedIn profile into a useful,
source-traceable, ethical person-level report even when the profile is
auth-walled.

The claim would fail if the report invented LinkedIn activity, overstated
inferred pains, hid source access mode, lacked an actionable first ask, or
quietly created unapproved CRM state.

## Trial Artifact

- Report:
  `/Users/kenjipcx/Zanarkand Technologies/projects/Valefor/.farplane/customer-research/reports/2026-07-14-mohamed-mo-tarek-el-fatatry.md`
- Browser evidence:
  `/Users/kenjipcx/Zanarkand Technologies/projects/Valefor/.farplane/customer-research/evidence/2026-07-14-mohamed-mo-tarek-el-fatatry/linkedin-auth-wall.png`
- Supplied target: `https://my.linkedin.com/in/dixrupt`

## Observed Trial Behavior

- Local project context and public sources bound the profile to Mohamed "Mo"
  Tarek El-Fatatry, founder of ERTH in Cyberjaya.
- Direct fetch returned LinkedIn status 999.
- Interactive `agent-browser` inspection rendered LinkedIn's Join/auth wall for
  the personal profile. The public company page rendered with a sign-in overlay.
- The report continued through full-public interviews, founder writing,
  company/partner material, regulator evidence, and current market context.
- Personal LinkedIn posts, comments, reactions, and full history remained
  `auth_walled` and were not inferred.
- No CRM entity or external record was created. The report used
  `entity_refs: []` and proposed the delta without applying it.

## Skill Repairs

- Added rendered browser inspection before declaring a supplied profile
  inaccessible.
- Added source access labels: `full_public`, `indexed_snippet`,
  `operator_supplied`, `auth_walled`, and `not_inspected`.
- Added the empty-CRM/no-write branch.
- Added a `Priority Call Brief` so the first ask and smallest credible help are
  visible before detailed evidence.
- Added auth-wall/empty-CRM and dense-source prioritization eval cases.
- Updated the template, synthetic example, and real trial artifact to match.

## Agent QA

- Tester lane: pass for the happy path and auth-wall path; pass with evidence
  instrumentation gaps for the skeptical-operator path before repair.
- Evidence-review lane: initial `revise` for source-status ambiguity, missing
  CRM-empty contract, eval gaps, and buried prioritization.
- Rerun reviewer after repair: `TAS-A`, `pass`, no behavior gate failures.
- Browser screenshot was inspected and confirmed to show LinkedIn's Join wall.

## Proof

- `python3 -m json.tool evals/evals.json` passed.
- `SKILL.md` is 211 lines, under the approximate 250-line first-load budget.
- Template and real report expose matching deep ICP sections, including the new
  priority brief and conditional CRM delta.
- Public-link spot checks returned expected reachable or access-controlled
  states; LinkedIn personal access remained blocked as recorded.

## Validator Blocker

`python3 /Users/kenjipcx/.codex/skills/skill-maintenance/scripts/check_skills.py --write`
still fails with:

```text
RuntimeError: could not find Farplane repo root
```

The installed skill package lacks the validator's expected source-repo root.
Run the registry validator from the repo-owned skill source when that source is
available.

## Skill Structure QA

```text
first_load_review:
  line_count_before: 190
  line_count_after: 211
  kept_in_skill: browser fallback, source access labels, CRM-empty gate, priority brief requirement
  moved_to_reference: detailed report shape remains in template
  deleted_as_duplicate_or_rationale: none
  extra_sections_kept_with_reason: none
  remaining_sections_over_budget: none
  proof_surface_fit: real browser artifact + agent QA + behavior evals + structural checks
  task_case_quality: auth-wall/empty-CRM and dense-source cases trace to real trial failures
  anti_cheat_case_design: prompts describe user conditions without naming template implementation
  qa_preflight_loaded: skill-maintenance and agent-qa-test checklists loaded
  qa_finish_independence: separate tester and reviewer lanes; reviewer rerun after repair
  qa_gotcha_deduplication: runtime behavior is in todos/gates; gotchas remain concise
  project_specific_context_isolation: real target exists only in project report and audit, not reusable skill behavior
  low_value_prose_scan: added lines change routing, evidence confidence, or write safety
  verdict: pass_with_validator_blocker
```
