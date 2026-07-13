---
title: TASK-0348 pre-existing overlap record
kind: preservation-evidence
status: complete
created_at: 2026-07-13T21:32:00+08:00
---

# Pre-existing overlap

These semantic changes existed before TASK-0348 implementation and must remain
after its scoped edits.

## Reporting CRM source state

```diff
- CRM state lives separately in `.farplane/crm/entities.json`.
+ CRM source state lives separately in `.farplane/crm/entities/**/*.md`;
+ `farplane crm compile` generates `.farplane/crm/entities.json`.
```

Retained-hunk assertions:

- `docs/farplane-framework/reporting.md` still names
  `.farplane/crm/entities/**/*.md` as source state.
- It still says `farplane crm compile` generates
  `.farplane/crm/entities.json`.

## Manifest template version

```diff
- "template_version":"2.0.2"
+ "template_version":"2.0.3"
```

Retained-hunk assertion: the `farplane-framework` row in
`docs/templates/registry.jsonl` remains at `2.0.3` after registry regeneration.
