---
title: Representative supply-call capture
kind: skill-example
skill: ingest-world-data
created_at: 2026-07-13
---

# Representative Supply-Call Capture

## Use When

One selected call passage contains a mixture of existing entities, new durable
entities, explicit associations, and a possible duplicate.

## Input Brief

> Penang Castings, sometimes called PC Manufacturing, manufactures in Penang
> and supplies aluminum housings to Acme Motors. The contact was Alex Chen, but
> the call does not identify which Alex Chen. A new Batu Kawan finishing
> facility is expected to open, though the date was described as tentative.

Current CRM contains Acme Motors and two different people named Alex Chen.

Bound question: `q-20260720-01` — “Which Malaysian suppliers can support Acme
Motors?” Optional origin session: `019f7e88-6864-7f23-8dbb-5e058009e911`.

## Good Output

- Update or create `penang-castings` only after registry lookup; merge
  `PC Manufacturing` into aliases and set `location: Penang, Malaysia` only if
  that country-level normalization is supported by the source or known context.
- Add: `Supplies aluminum housings to [Acme Motors](crm:acme-motors). [^q-20260720-01]`
- Add the matching question definition under `## Question index`, including the
  supplied session ID but no turn ID.
- Create the Batu Kawan facility only if the passage establishes it as a
  durable named entity; preserve the opening-date uncertainty in prose.
- Report both Alex Chen records as ambiguous. Do not merge them, create a third
  record, or link one to the claim.
- Compile `entities.json` and `world.json`; report that Penang Castings is
  unlocated on the map unless verified coordinates were supplied.

## Comparison Gates

- The capture is bounded to the supplied passage.
- Existing prose survives unchanged outside the appended or merged facts.
- Exactly one explicit association is generated from the Acme sentence.
- The association and both involved entities can be filtered through
  `q-20260720-01` in the compiled projection.
- No relationship predicate, inverse edge, automatic geocoding, or guessed
  Alex Chen identity appears.

## Provenance / Rights

Synthetic fixture derived from the TASK-0344 accepted scenario; no customer or
private call data is included.
