---
kind: capability-map
status: draft
created_at: TODO
---

# Capability Map

| Capability | Needed For | Existing Skill / Tool | Status | Evidence | Decision |
| --- | --- | --- | --- | --- | --- |
|  |  |  | ready / needs_config / needs_reference / needs_eval / needs_wrapper / missing / defer |  |  |

## Status Rules

- `ready`: existing skill/tool can run now.
- `needs_config`: credential, account, directory, policy, or boundary missing.
- `needs_reference`: existing skill owns the workflow but needs domain detail.
- `needs_eval`: behavior exists but proof is weak.
- `needs_wrapper`: external/broad capability exists but needs a local contract.
- `missing`: no clear owner exists.
- `defer`: not required for the first evidence loop.

## Missing Primitive Decision

```text
gap -> use_existing | add_reference | create_ticket | create_skill
     | create_tool_connector | add_eval | add_validator | add_subagent
     | defer_until_pilot
```
