---
title: Ticket Spec Reviewer Handoff
owner: plan-next-wave
status: active
kind: reviewer-handoff
created_at: 2026-07-06
updated_at: 2026-07-10
---

# Ticket Spec Reviewer Handoff

Use the native reviewer only when a material candidate needs independent
judgment before it can be treated as executable. Normal bounded specs should
pass the deterministic planner checklist without adding review latency.

```text
review_next_wave(candidate_specs, program, objective_contract, history, context)
  -> pass | revise | reject + findings
```

## Required Context

- `context_ref:` current Pulse report, ticket, or planning artifact.
- `candidate_specs:` proposed executable specs.
- `program_and_objective:` stable policy, value direction, metrics/guards, and
  authority boundaries.
- `ticket_history:` active commitments plus recent outcomes and attempts.
- `current_context:` dated Interval/Feed reports or external observations when
  they affected priority.

## Reviewer Focus

- objective contribution is real rather than ceremonial;
- candidate is BAU by primary outcome and not harness self-improvement;
- bottleneck, lever, compounding value, ranking, and deprioritization are
  explicit without fake precision;
- output and proof are worth a worker cycle;
- worker can start without more ideation;
- dedupe examined outcome/artifact/surface, not title only;
- capability ownership is referenced rather than duplicated;
- authority, dependencies, and source gaps are honest;
- planner returned specs only and left all side effects to Pulse.

## Expected Receipt

```yaml
verdict: pass | revise | reject
overall_tas: TAS-A | TAS-B | TAS-C | block | invalid
failed_gates: []
required_changes: []
accepted_specs: []
rejected_specs: []
evidence_refs: []
```

Only `pass` specs may be materialized as executable tickets.
