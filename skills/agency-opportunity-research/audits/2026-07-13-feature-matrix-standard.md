---
skill: agency-opportunity-research
date: 2026-07-13
change_type: correction
owner: skill-maintenance
status: passed
review_route: reviewer
before_ref: skills/agency-opportunity-research/SKILL.md
after_ref: skills/agency-opportunity-research/SKILL.md
reasoning_basis: operator_feedback
proof_artifacts:
  - Valefor/tickets/TASK-0035/ticket.md
eval_required: yes
---

# Feature matrix standard audit

## Change

- Before: the semantic-table rule still allowed one vendor-summary row per
  provider, which made capability differences hard to scan.
- After: customer-facing comparisons use capabilities as rows and providers as
  columns, with evidence-safe cell states.
- Example: `Automatic recovery re-optimization` compares Facility Grid,
  CxPlanner, and Valefor in one row.

## Proof

- Valefor Mine-To-Margin and Commissioning landings render feature matrices.
- Commissioning package regression requires the matrix, playground manifest,
  sample thread, and mounted optimizer.
- Browser QA confirmed both matrix headers and the editable Commissioning RFS
  control with no page errors.
- Unsupported competitor absence claims remain phrased as “not shown in the
  reviewed public material.”

## Followup

- Keep deeper source ledgers in `reference/competitive-landscape.md`; keep the
  concise capability matrix directly in the buyer-facing landing.
