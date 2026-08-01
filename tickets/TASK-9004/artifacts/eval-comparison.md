---
ticket_id: TASK-9004
artifact: eval-comparison
created_at: 2026-08-02
status: complete
---

# Eval Comparison

## Setup

- Owner-scoped baseline ran the new focused rows against a clean detached HEAD
  worktree so each pre-change skill body was injected by the eval runner.
- Candidate rows ran against the edited owner skill.
- The early custom baseline/candidate runs under `174007` and `174334` did not
  inject owning skills; they remain diagnostic evidence only and are not used
  for the completion claim.
- Functional browser operation was split into live browser QA plus a focused
  synthesis eval because the clean-room CLI eval fixture did not expose
  `agent-browser`.

## Results

| Behavior | Baseline | Final Candidate | Evidence |
| --- | --- | --- | --- |
| Asset source roles + moodboard gate | C | A | `eval-runs/20260801-180255-task-9004-owner-baseline/summary.json`; `eval-runs/20260801-182127-task-9004-owner-candidate-v6/summary.json` |
| Landing Asset Advisor route + complete-input skip | C | A | baseline above; `eval-runs/20260801-181518-task-9004-owner-candidate-v3/summary.json` |
| Functional material comparable synthesis | C | A | baseline above; `eval-runs/20260801-182439-task-9004-owner-candidate-v8/summary.json` |
| Functional tiny settled-fix skip | A | A | baseline above; `eval-runs/20260801-180304-task-9004-owner-candidate/summary.json` |
| Pinterest canonical resolution + unresolved fallback | C | A | baseline above; `eval-runs/20260801-181931-task-9004-owner-candidate-v5/summary.json` |

## External Operation Proof

`browser-operation-qa.md` independently operated current public Mobbin and
Page Flows surfaces with `agent-browser`. It recorded Mobbin's public access
limit, Page Flows' public flow categories and timestamped HeyGen onboarding
states, and rejected Pinterest/social galleries as functional proof.

## Experiment Result

The observation is `expected`: all four newly targeted positive behaviors
improved from C to A, while the already-correct tiny-fix negative route remained
A. The initial generic candidate's lack of movement was traced to missing
owner-skill injection rather than an implausibly positive result or method
failure.

## Eval Query Review

```text
eval_query_review:
  changed_files:
    - skills/asset-advisor/evals/evals.json
    - skills/landing-page/evals/evals.json
    - skills/functional-ui/evals/evals.json
    - skills/ingest-content/evals/evals.json
  reviewed_rows:
    - asset_advisor_reference_roles_moodboard_01
    - landing_page_conditional_asset_advisor_01
    - functional_ui_browser_comparables_01
    - functional_ui_skip_comparables_01
    - ingest_content_pinterest_canonical_source_01
  reviewer: self + independent reviewer
  query_spoiler_verdict: pass
  fixes_applied: supplied concrete source/evidence URLs where preservation or current browser evidence was part of the task
  deferrals: none
  remaining_risk: source sites and public access can change
```
