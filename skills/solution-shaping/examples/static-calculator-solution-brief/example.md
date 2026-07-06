# Static Calculator MVP Brief Example

## Use When

Use this as a compact quality reference when an agency workflow needs to turn a
reported operational complaint into a reviewable MVP proposal.

## Input Brief

```text
A manufacturing prospect says quoting custom jobs is too slow and asks whether
we can make them a static calculator.
```

## Good Output

```text
Target / client: Custom manufacturing sales and estimating team.
Source status: Reported complaint plus inferred operating context.

Reported problem or outreach signal: Quotes take too long; prospect asked for a
static calculator.

Problem frame: The real problem is likely quote reliability and quote cycle
time, not calculator availability. Sales needs a way to collect job inputs,
apply pricing/cost rules, identify approval cases, and produce a quote that
operations and finance can trust.

Actor / job / stakes: Sales rep or estimator must create a customer-facing
quote quickly. Bad quotes lose deals, leak margin, or create fulfillment risk.

Current workflow hypothesis: Quoting likely depends on scattered spreadsheets,
tribal rules, approval messages, and manual checks. This is unverified.

First-principles insight: A correct quote needs inputs, cost assumptions, margin
policy, approval authority, and an auditable output. A calculator alone only
solves arithmetic if those inputs and rules are already trusted.

MVP options:
1. Static calculator: fast to build, likely too narrow.
2. Quote workflow slice: captures inputs, applies known rules, flags approval
   cases, and records decisions.
3. ERP-like quoting module: likely too broad until record-of-truth and
   integration constraints are proven.

Recommended MVP: Quote workflow slice.

V1 scope: intake form, rule-backed price estimate, approval flag, generated
quote summary, and quote decision log with representative demo data.

Deferred V2: inventory/capacity integration, accounting integration, automated
order lifecycle, role-specific dashboards.

Non-goals: replace ERP, own full order management, automate all exception cases.

Proof model: The prospect reviews a realistic quote flow and confirms whether
it would reduce quote delay, improve quote consistency, and expose approval
cases early.

Demo / review artifact: clickable quote workflow or narrated walkthrough with
3 representative quote scenarios: simple, approval-required, and missing-data.

Risks and assumptions: pricing rule availability, approval authority, data
quality, integration needs, security requirements, quote volume.

Next owner: `prd` for product scope, `deep-system-design` if the workflow is
accepted and data ownership must be designed, or `impl-plan` for a narrow demo
slice after acceptance.
```

## Comparison Gates

- The MVP follows from the problem frame, not from the requested artifact.
- The brief names V1, deferred V2, non-goals, and a prospect-review proof model.
- Unknowns stay labeled and do not become fake client truth.

## Provenance / Rights

Synthetic example derived from this Farplane design discussion. No client data.
