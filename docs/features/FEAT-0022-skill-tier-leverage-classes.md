---
title: Retired skill tier leverage classes
status: retired
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-10-10
tags:
  - farplane
  - feature
  - sys-0006
refs:
  - runtimes/AGENTS.md
  - docs/skills/system.md
  - skills/research
  - skills/review
  - docs/review/rubrics
  - docs/skills/README.md
  - bin/validators/sync_skill_registry.py
feature_id: FEAT-0022
system_id: SYS-0006
category: skills
public: true
surfaces:
  - runtimes/AGENTS.md
  - docs/skills/system.md
  - skills/research
  - skills/review
  - docs/review/rubrics
  - docs/skills/README.md
  - bin/validators/sync_skill_registry.py
source_refs:
  - "docs/MEMORY.md#MEM-0098"
  - docs/features/README.md
external_refs: []
evidence_refs:
  - docs/HISTORY.md
known_limits: Retired 2026-10-10. Skill tiers no longer classify skills; the Capability Map's specialist desks (config/skill-workflows.toml [specialists]) decide which skills are entrypoints, their department and default verb, and the registry rejects a tier field. The phase protocol and todo-link guidance it carried live in docs/skills/system.md.
metrics: []
last_verified: 2026-06-23
experimental: false
superseded_by: false
---

# Retired skill tier leverage classes

Skill tier leverage classes are retired as of 2026-10-10 (issue #40). Tiers (Tier 0 phase protocol,
Tier 1 primitives, Tier 2 interfaces, Tier 3 domain skills) stopped matching how Farplane decides what a
skill is for. That job belongs to the Capability Map: specialist desks in
`config/skill-workflows.toml` `[specialists]` name each desk's department, deliverable, primary skill
and members, and the registry projects a member's desk as its `specialist`. A skill on no desk is an
internal helper. `FEAT-0022` stays as a stable handle for the skill system's composition rules.

```text
desk(skill) -> specialist | helper
```

## Where its parts went

- The phase protocol (formerly "Tier 0") and the todo-link guidance: [`docs/skills/system.md`](../skills/system.md).
- Desks, departments and map topology: [`docs/skills/department-taxonomy.md`](../skills/department-taxonomy.md).
- Upgrade priority: harness health's priority cohort is each desk's primary skill plus every skill used
  in the last 30 days, and `docs/features/FEAT-0064-skill-signals.md` ranks improvement targets.
- Retired checks: `check_skill_todo_tiers.py` and `check_tier0_phase_protocol.py` are deleted; the registry
  builder rejects a `tier` frontmatter field.
