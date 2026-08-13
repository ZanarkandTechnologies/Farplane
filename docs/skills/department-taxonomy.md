---
title: Skill department taxonomy
status: active
owner: skills/skill-maintenance
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

The Capability Map uses `rules/skill-workflows.toml` to select a small set of
real Tier 3 workflow roots from the membership pool. The projection renders
those roots as workflow nodes and includes only their declared `artifact`
methods as format specialists. The technical Skill Library remains the full
registry, including helpers and integrations.

Map topology is static containment, not execution: `department -> selected
workflow root -> artifact method`. Declared `integration` and `internal`
methods remain outside this projection. The full three-class `methods` schema
is owned by [`system.md`](system.md).

```text
group -> explicit department membership for every Tier 3 skill
workflow_roots + workflow_labels -> explicit static-map selection/names for real skill packages
methods[class=artifact] -> explicit format-specialist containment in the map
```

Neither configuration nor frontmatter expresses process order, artifact
consumption, Todo calls, or live skill-call relationships. That evidence
belongs to a ticket's runtime Action Graph when it exists.
