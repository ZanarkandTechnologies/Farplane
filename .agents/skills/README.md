---
kind: local-capability-skills-index
project: Farplane
created_at: 2026-06-26
updated_at: 2026-07-11
framework_template_version: "0.1.0"
owner: harness
---

# Local Capability Skills

Project-local capability skills live here.

Use `.agents/skills/<capability>/SKILL.md` for workflows that are specific
to this project or company. Keep them on the normal evolving Farplane skill
template from day one.

Tickets, interval reports, and automation prompts should call local skills by
path when those skills own the capability workflow. Promote a local capability
skill to reusable root `skills/` only through an explicit human-reviewed change
after repeated use shows cross-project value.

These are reusable workflows called by tickets and Work Pulse. They are not
planning lanes, controllers, or independent heartbeats.

## Farplane Capability Skills

| Capability | Local skill |
| --- | --- |
| Experiment reports | `farplane-experiment-report` |
| Trust ablations | `farplane-ablation-proof` |
| Harness improvements | `farplane-productization` |
| Evidence content | `farplane-evidence-content` |
| Market learning | `farplane-market-learning` |
