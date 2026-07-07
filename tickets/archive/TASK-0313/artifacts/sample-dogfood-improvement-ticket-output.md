---
kind: proof-sample
ticket_id: TASK-0313
created_at: 2026-07-07T23:06:00+08:00
status: pass
---

# Sample Dogfood Improvement Ticket Output

This sample proves the intended output shape for both safe modes. It is not a
new ticket and does not repair the seed findings.

## Ticket Creation Disabled

```text
improvement_ticket:
  mode: candidate
  path: null
  candidate_ref: "## Improvement Ticket"
  no_autostart_receipt: "no impl-plan, Goal, Pulse execution, automation sync, or worker spawn invoked"
```

Expected report behavior:

- The report remains under `.farplane/reports/dogfood-review/<timestamp>.md`.
- The `Improvement Ticket` section contains a complete ticket candidate.
- The candidate groups all active feature findings into one follow-up work item.
- No files under `tickets/` are created in this mode.

## Ticket Creation Enabled

```text
improvement_ticket:
  mode: created
  path: tickets/TASK-XXXX/ticket.md
  candidate_ref: null
  no_autostart_receipt: "no impl-plan, Goal, Pulse execution, automation sync, or worker spawn invoked"
```

Expected created ticket frontmatter:

```yaml
phase: planning
status: review
ready: false
approval_required: true
requires_qa: true
requires_demo: false
rewards.kpi:
  - accepted_harness_improvements
```

Expected body payload:

```text
Findings By Feature:
  - feature_ref: FEAT-0066
    track_prompt_summary: review product-scoped Pulse against useful admitted work, duplicate skip volume, reward fit, and interval guidance
    reviewer_tas: TAS-B
    issue: high unchanged skip volume compared with admitted actions
    proposed_repair: cap or compress unchanged skip reports while preserving useful admissions and evidence
    evidence_refs:
      - .farplane/reports/dogfood-review/2026-07-07T092204Z.md
  - feature_ref: FEAT-0067
    track_prompt_summary: verify Daily links tracked-feature dogfood output and resulting improvement work
    reviewer_tas: TAS-B
    issue: latest Daily report did not clearly link the dogfood report or improvement ticket
    proposed_repair: surface report path, active/skipped refs, decisions, and improvement ticket path/candidate
    evidence_refs:
      - .farplane/reports/dogfood-review/2026-07-07T092204Z.md
Skipped Refs:
  - FEAT-0065: retired/superseded; historical evidence only
Done / Proof:
  - dogfood-review report includes one ticket path or candidate
  - interval-update report surfaces that path or candidate
  - no impl-plan, Goal, Pulse execution, automation sync, or worker spawn autostarts
```

## Pass Criteria

- Exactly one ticket path or candidate exists per material dogfood report.
- Feature-specific findings remain grouped inside the one artifact.
- Retired or superseded refs are not active repair targets.
- No-autostart is explicit and inspectable.
