---
skill: lead-scout
example: public-founder-scout
---

# Public Founder Scout Example

Scout goal: Find founder/operators who publicly discuss slow B2B onboarding and
could benefit from an operational workflow demo.

Source boundary: Supplied X search results and public company pages only.

Qualification filter:

- Strong fit: owns or leads onboarding, customer success, implementation, or
  post-sale operations.
- Signal: public post, profile, or company page mentions onboarding delay,
  implementation burden, time-to-value, or manual handoffs.
- Reject: generic sales influencers, agencies selling the same service, or
  candidates with no public operational signal.

Top candidates:

- Candidate: Example Founder, ExampleOps
  Public links: `https://example.com/profile`, `https://example.com/company`
  Fit signals: public post says implementation still depends on manual
  spreadsheets; company sells B2B onboarding-heavy software.
  Disqualifiers: no public hiring or tooling page found.
  Confidence: medium
  Evidence notes: public post and company page only; pain is inferred.
  Next owner: `customer-research`

Rejected near-misses:

- Candidate: Example Consultant
  Why rejected: talks about onboarding as thought leadership but sells onboarding
  consulting; lower buyer-fit for this campaign.
  Evidence notes: public profile and services page.

Wiki writeback:

- Publication intent: `preview` (no Wiki write direction was supplied).

- Entity ID: `example-founder`
- Name: `Example Founder`
- Description: `Founder of ExampleOps with a public onboarding workflow signal.`
- Links: `https://example.com/profile`, `https://example.com/company`
- Status: `scouted`

Next action: run `customer-research` for top 3 only. The resulting report uses
`entity_refs: [example-founder]`; the CRM record does not store report paths.
