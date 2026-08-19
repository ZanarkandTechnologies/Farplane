---
skill: customer-research
date: 2026-08-19
change_type: structure
owner: skill-maintenance
status: draft
review_route: reviewer
before_ref: skills/customer-research/SKILL.md@280-lines
after_ref: skills/customer-research/SKILL.md@159-lines
reasoning_basis: first_principles
proof_artifacts:
  - tickets/TASK-0438/ticket.md
eval_required: yes
---

# Customer Research Wiki Handoff And Compaction Audit

## Change

- Before: the first-load skill contained the full deep-ICP browser/hiring
  protocol and directly compiled approved entity Markdown.
- After: the conditional deep-ICP protocol has one owner-local reference, while
  first load hands sourced approved page deltas to `manage-wiki`.
- Why: meet the 200-line hard envelope without dropping research or safety
  behavior, and make Wiki mutation single-owner.
- Tradeoff accepted: deep ICP invocations load one explicit conditional
  reference; ordinary customer-research calls no longer pay that context cost.

## First-Principles Reasoning

- Objective: preserve decision-quality person research while removing direct
  canonical-article and projection mutation.
- Placement logic: always-needed routing/gates remain in `SKILL.md`; session,
  source, and hiring mechanics live in `references/deep-icp-sources.md`.
- Expected behavior delta: approved Wiki updates route to `manage-wiki`; report,
  ethics, Signal Card, evidence, and conversation behavior remain intact.
- Proof needed: line-count, link/tier/surface/eval validators, behavior eval,
  caller sweep, and independent TASK-0438 review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Trigger, signature, six-step report path, Wiki handoff, and output remain visible. |
| `reference_load_precision` | pass | Deep-ICP-only source/hiring branch has an explicit load condition. |
| `missing_context_rate` | pass | Source classes, safety boundary, report shape, Signal Card, and finish gates remain routed. |
| `noisy_context_rate` | pass | Conditional browser/hiring mechanics moved out of ordinary first load. |
| `duplicated_instruction_count` | pass | The source protocol has one owner-local location. |
| `prompt_size_tokens` | pass | First load changed from 280 to 159 physical lines. |
| `task_success_rate` | unknown | Behavior eval execution is pending. |
| `review_tas_rate` | unknown | TASK-0438 completion review is pending. |
| `maintenance_locality` | pass | Research stays here; canonical Wiki mutation routes to `manage-wiki`. |
| `composition_clarity` | pass | Report output, proposed delta, handoff, gates, and failure state are explicit. |

## Proof Artifacts

- Skill-local evals: Wiki/no-write assertions updated; query lint passes.
- Structure evals: todo tiers, surface budgets, Tier 0, and checklist sync pass.
- Reviewer receipt: pending TASK-0438 completion review.
- Validator: JSON and shell syntax pass; global skill/doc registries await the
  coordinating lane's integrated regeneration.
- Eval required: yes; behavior execution remains pending.
- Evidence gaps: integrated registry generation, behavior comparison, reviewer.

## Before Behavior

- Customer Research directly invoked the retired entity compiler after writes.

## After Behavior

- It returns a report plus proposed delta, invoking `manage-wiki` only for an
  exact sourced delta with operator write approval.

## Followups

- `no_self_improve_reason`: this is an owner-boundary migration, not measured
  variant search; use real Wiki handoff failures to justify optimization.
