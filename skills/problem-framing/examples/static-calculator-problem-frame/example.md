# Static Calculator Problem Frame Example

## Use When

Use this as a compact quality reference when a requester names a specific
artifact, but the real operational problem may be broader or narrower.

## Input Brief

```text
A manufacturing client says: "We need a static calculator so sales can quote
custom jobs faster."
```

## Good Output

```text
Raw complaint: Sales needs a static calculator for custom job quotes.
Requested artifact: Static pricing calculator.
Source status: reported.

Symptom: Quote production is slow or inconsistent.

Problem statement: Sales cannot produce reliable quotes quickly because pricing
inputs, margin rules, approvals, and cost assumptions are scattered across
people, files, or tacit knowledge.

Actor / job: Sales rep or estimator needs to produce a quote that is fast enough
for the customer and reliable enough for operations and finance.

Stakes: Bad quotes lose deals, create margin leakage, or commit operations to
work that cannot be fulfilled profitably.

Current workflow: Unknown. Need to identify inputs, approval steps, current
spreadsheets/tools, exception paths, and who owns final quote authority.

Why current workflow exists: likely mix of variable job specs, hidden costing
rules, approval risk, and missing record-of-truth data. Marked unverified.

First-principles basis: A quote requires customer/job inputs, cost model,
margin policy, availability/capacity assumptions, approval authority, and an
output the customer can accept.

Product boundary options:
1. Static calculator: fastest, but risks encoding stale rules without workflow
   control.
2. Quote workflow slice: captures inputs, applies pricing rules, flags approval
   cases, and records quote decisions.
3. ERP-like system: only justified if records of truth, inventory, capacity,
   and order lifecycle must be owned in one system.

Recommended boundary: Quote workflow slice until record-of-truth needs prove a
larger system is necessary.

Assumptions and unknowns: pricing rules, approval authority, source data,
integration needs, security, expected quote volume, error cost.

Next owner: solution-shaping for an agency proposal, or deep-system-design if
the quote workflow slice is approved for system design.
```

## Comparison Gates

- The requested calculator remains visible as evidence, not as the default
  build target.
- The frame names actor, job, stakes, current workflow unknowns, and product
  boundary options.
- The recommendation shows restraint: no full ERP unless the record-of-truth
  need is proven.

## Provenance / Rights

Synthetic example derived from this Farplane design discussion. No client data.
