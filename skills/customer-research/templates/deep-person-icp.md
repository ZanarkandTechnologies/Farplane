---
skill: "customer-research"
entity_refs:
  - "{{ person_entity_id }}"
name: "{{ person_name }}"
links:
  - "{{ primary_link }}"
industry: "{{ industry_or_field }}"
relevance: "{{ one_sentence_reason_this_person_matters }}"
created_at: "{{ YYYY-MM-DD }}"
---

Use `entity_refs: []` when no entity exists and CRM writes are not approved;
include a proposed-but-not-applied CRM delta in the body. Add other resolved
CRM IDs only when the report actually covers those entities. Keep deep ICP mode
in the body, not frontmatter.

# {{ Person Name }} Deep Person ICP

Write one sourced paragraph of no more than 150 words: identify the person,
their current role, one to three largest relevant achievements, and why they
matter for this call now. Prefer orientation over praise or career chronology.

## Person Signal Card

Keep every group to three entries or fewer by default. Each hypothesis must
remain easy to correct.

### Goals And Pressures

| Goal or pressure | Status | Evidence ref | Why it changes the next move | Confidence / falsifier |
| --- | --- | --- | --- | --- |
|  | `observed | supplied | inferred | unknown` |  |  |  |

### Likely Active Problems

| Testable problem hypothesis | Evidence ref | Why now | Confirm / disprove | Confidence |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

### Relationship Surfaces

Use professionally relevant common ground, trusted paths, value the operator can
offer first, or a thoughtful gesture only when directly supported. Do not infer
private preferences, favors, or access.

| Surface | Evidence ref | Potential value | Confidence / risk / boundary |
| --- | --- | --- | --- |
|  |  |  |  |

### Recommended First Move

- First correction ask:
- Smallest credible help:
- Language to mirror carefully:
- Avoid:

### Correction Questions

1.
2.
3.

## Evidence And Unknowns

Access labels: `full_public`, `indexed_snippet`, `operator_supplied`,
`operator_authorized_session`, `auth_walled`, `not_inspected`.

| Evidence ref | Claim supported | Access | Date | Confidence | Limits / alternative explanation |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

- Hiring coverage: name official careers/ATS, LinkedIn company jobs, company or
  recruiter posts, and relevant indexed listings inspected. Record each useful
  signal as `active`, `closed_or_stale`, `status_unknown`, `none_surfaced`, or
  `not_applicable`; fold its implication into the affected hypothesis above.
- Missing or inaccessible:
- Highest-value unknown:
- Boundary honored:

## CRM Delta Proposed, Not Applied

Include this section only when `entity_refs: []` because relationship-state
writes were not approved.
