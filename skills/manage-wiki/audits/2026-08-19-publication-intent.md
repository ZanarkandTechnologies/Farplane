---
skill: manage-wiki
date: 2026-08-19
mode: harden_skill
status: candidate
ticket: TASK-0441
---

# Wiki Publication Intent Audit

## Behavior Delta

- Before: callers mixed proposals, approvals, and writes, sometimes requiring
  the operator to approve an exact delta after already asking to update Wiki.
- After: one `publication_intent = preview | apply` contract defaults to
  preview; direct Wiki write language selects apply without a second approval.
- Preserved gates: bounded source, professional privacy, identity ambiguity,
  complete changeset validation, and page-scoped sync.
- Ownership: Manage Wiki selects pages, resolves or creates entities, links
  mentions, validates, publishes, and syncs. Intelligest and research callers
  bind intent and supply durable sourced facts.

## Proof Surface

- Natural evals cover article/video preview and apply, ordinary read-only
  research, direct research save-to-Wiki, ambiguity, and privacy blocking.
- Every edited `SKILL.md` remains at or below 200 physical lines.
- Candidate promotion still requires JSON/eval-query/skill validation and the
  TASK-0441 independent completion review.

```yaml
eval_query_review:
  changed_files:
    - skills/manage-wiki/evals/evals.json
    - skills/intelligest/evals/evals.json
    - skills/customer-research/evals/evals.json
    - skills/agency-opportunity-research/evals/evals.json
    - skills/lead-scout/evals/evals.json
    - skills/personalized-offer/evals/evals.json
  reviewed_rows: preview/apply article, video, research, ambiguity, privacy
  reviewer: self
  query_spoiler_verdict: pass
  fixes_applied: direct prompts kept natural; policy and expected routes stay in assertions
  deferrals: behavior execution must use an isolated target root because apply cases write Wiki state
  remaining_risk: independent eval-row and completion review pending
```
