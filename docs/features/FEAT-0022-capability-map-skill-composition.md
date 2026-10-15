---
title: Capability Map skill composition
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-10-13
tags:
  - farplane
  - feature
  - sys-0006
refs:
  - runtimes/AGENTS.md
  - skills/harness/references/skill-system/system.md
  - skills/research
  - skills/review
  - skills/review/references/rubrics
  - skills/harness/references/skill-system/README.md
  - bin/validators/sync_skill_registry.py
feature_id: FEAT-0022
system_id: SYS-0006
category: skills
public: true
surfaces:
  - runtimes/AGENTS.md
  - skills/harness/references/skill-system/system.md
  - skills/research
  - skills/review
  - skills/review/references/rubrics
  - skills/harness/references/skill-system/README.md
  - bin/validators/sync_skill_registry.py
source_refs:
  - "docs/MEMORY.md#MEM-0098"
  - docs/features/README.md
external_refs: []
evidence_refs:
  - docs/HISTORY.md
known_limits: Desk membership is authored in config/skill-workflows.toml [specialists]; a skill on no desk is an internal helper and the map omits it.
metrics: []
last_verified: 2026-06-23
experimental: false
superseded_by: false
---

# Capability Map skill composition

The Capability Map decides what each skill is for. Specialist desks in
`config/skill-workflows.toml` `[specialists]` name each desk's department,
deliverable, primary skill and members, and the registry projects a member's
desk as its `specialist`. A skill on no desk is an internal helper.

```text
desk(skill) -> specialist | helper
```

## Where the parts live

- The phase protocol and the todo-link guidance: [`skills/harness/references/skill-system/system.md`](../../skills/harness/references/skill-system/system.md).
- Desks, departments and map topology: [`skills/harness/references/skill-system/department-taxonomy.md`](../../skills/harness/references/skill-system/department-taxonomy.md).
- Upgrade priority: harness health's priority cohort is each desk's primary skill plus every skill used
  in the last 30 days, and `docs/features/FEAT-0064-skill-signals.md` ranks improvement targets.
