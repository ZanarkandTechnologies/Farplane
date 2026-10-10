---
title: Skill department taxonomy
status: active
owner: skills/skill-maintenance
created_at: 2026-08-13
updated_at: 2026-09-28
source_of_truth: [config/skill-departments.toml, config/skill-workflows.toml]
---

# Skill department taxonomy

`department` is the single operating-department membership required on every Tier 3
skill. It is not a technical implementation tag and it does not imply that one
skill invokes another.

| ID | Label | Owns in the constellation |
| --- | --- | --- |
| `back-office` | Back Office | finance, internal records, people, office administration |
| `sales` | Sales | targeting, outreach, and sequencing |
| `deals` | Deals | replies, calls, solution shaping, and closing |
| `marketing` | Marketing | content, brand, creative, distribution, and channels |
| `operations` | Operations | delivery systems, builds, automation, and internal operations |
| `intelligence` | Intelligence | companies, people, markets, research, and learning |
| `customer` | Customer | support, success, and community |

The Capability Map is organized by **specialist desks**. A specialist groups
skill variants that one office employee offers (for example `reporter` holds
`progress-update`, `report-gen`, `recap-task`, and `dogfood-review`).
`config/skill-workflows.toml` `[specialists]` owns each desk's label, department,
deliverable, primary skill (its default verb), and member `skills`. A member
must be a Tier 3 skill in the desk's department and sits at only one desk; the
registry projects it as the row's `specialist`. Skill files stay unchanged, so
oversized skills are never grown by desk membership.
Skills without a specialist are internal: planners dispatch them as needed and
the map omits them. The technical Skill Library remains the full registry.

This is source visibility, not active-session availability. `config/skill-profiles.toml`
controls named-profile enablement; a profile-gated desk remains visible
here so filtering cannot look like deletion.

Map topology combines static ownership with declared artifact flow:
`department -> specialist desk (workstation)`; a member skill with an
`integration` capability is drawn as a system facility beside its desk; an
output-to-input match between member skills creates a directed artifact-flow
edge. That connection means “this desk or facility accepts this artifact
family,” not “automatically calls or publishes.” `consumes` and `produces` are
typed artifact-family IDs, not literal filenames; methods stay outside this
projection and their technical interface schema is owned by [`system.md`](system.md).

```text
department -> explicit department membership for every Tier 3 skill
[specialists] -> desk label, deliverable, primary skill, and member skills
member -> Tier 3 skill in the desk's department, at one desk only
member capability[kind=integration] -> system facility beside the desk
produces ∩ consumes across members -> directed artifact-flow edge
```

The graph does not express Todo calls, live skill-call relationships, concrete
file paths, automatic delivery, or runtime state. The directed edge proves only
that one declared output is compatible with another declared input. Runtime
execution evidence belongs to a ticket's Action Graph when it exists.
