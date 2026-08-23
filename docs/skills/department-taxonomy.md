---
title: Skill department taxonomy
status: active
owner: skills/skill-maintenance
created_at: 2026-08-13
updated_at: 2026-08-13
source_of_truth: [rules/skill-departments.toml, rules/skill-workflows.toml]
---

# Skill department taxonomy

`group` is the single operating-department membership required on every Tier 3
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

The Capability Map uses `rules/skill-workflows.toml` as an explicit admission
list. An admitted Tier 3 skill must declare a typed `capability` contract in
its own frontmatter. An `artifact` capability becomes a permanent workstation;
an `integration` capability becomes a permanent system facility. Empty
departments remain visible at the organization level until a real capability is
intentionally admitted. The technical Skill Library remains the full registry,
including helpers, methods, and unclassified packages.

This is source visibility, not active-session availability. `rules/skill-profiles.toml`
controls named-profile enablement; a profile-gated workstation remains visible
here so filtering cannot look like deletion.

Map topology combines static ownership with declared artifact flow:
`department -> workstation`; an output-to-input match creates a directed
`workstation -> facility` handoff. That connection means “this facility accepts
this artifact family,” not “automatically calls or publishes.” A facility with
no same-department declared input remains directly rooted at its department.
`consumes` and `produces` are typed artifact-family IDs, not literal filenames;
methods stay outside this projection and their technical interface schema is
owned by [`system.md`](system.md).

```text
group -> explicit department membership for every Tier 3 skill
capability_admission + capability_labels -> explicit static-map selection/names
capability[kind=artifact] -> workstation
capability[kind=integration] -> system facility
artifact.produces ∩ capability.consumes -> directed artifact-flow edge
```

The graph does not express Todo calls, live skill-call relationships, concrete
file paths, automatic delivery, or runtime state. The directed edge proves only
that one declared output is compatible with another declared input. Runtime
execution evidence belongs to a ticket's Action Graph when it exists.
