---
title: Opportunity Reviewer Handoff
owner: ticket-opportunity-generator
status: active
kind: reviewer-handoff
created_at: 2026-07-06
---

# Opportunity Reviewer Handoff

Use the existing native `reviewer` lane for material generated-ticket specs
when Pulse or a product loop is about to admit AI-planned work. The reviewer is
adversarial by default: it should try to reject valid-but-mid work before a
worker spends a cycle. Do not create a new reviewer subagent unless this
handoff fails in practice.

```text
review_ticket_opportunities(candidate_specs, context_refs, hard_gates)
  -> pass | revise | reject + findings + required_changes
```

## Required Context

- `context_ref:` current ticket, product `product.md`/progress, Pulse report, or
  product-loop cycle entry that produced the candidate.
- `candidate_specs:` generated ticket specs or draft tickets.
- `product_context:` `farplane/products.json` plus the owning
  `farplane/products/<product>/skill.md`.
- `recent_attempts:` prior tickets, product-loop progress entries, artifacts,
  rejection reasons, or explicit source gap.
- `external_attention:` Feed Scout/source refs for distribution or
  market-learning tickets when available.

## Reviewer Focus

Ask the reviewer to find reasons the ticket is not yet worth doing:

- weak or fake reward trace
- weak ICP resonance
- no current trend/source relevance
- below current/default/state-of-art bar
- low artifact ambition
- product skill mismatch
- duplicate prior attempt
- worker still has to discover the idea
- unsafe or unclassified human gate
- missing product-loop learning writeback
- no decision Kenji or the ICP would actually care to make
- "safe and executable" substituting for "worth a worker cycle"

## Expected Receipt

```yaml
verdict: pass | revise | reject
tas: TAS-A | TAS-B | TAS-C | block | invalid
failed_gates:
  - reward_trace
  - icp_resonance
required_changes:
  - ""
accepted_specs:
  - ticket_id_or_title: ""
rejected_specs:
  - ticket_id_or_title: ""
evidence_refs:
  - ""
```

Pulse or the product loop may admit only `pass` specs. `revise` specs must be
strengthened and reviewed again or explicitly parked. `reject` specs should
write the rejection reason into the product-loop progress entry.
