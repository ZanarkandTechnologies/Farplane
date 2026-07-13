---
title: Template Registry
status: active
owner: Farplane
updated_at: 2026-07-13
---

# Template Registry

`docs/templates/registry.jsonl` tracks high-impact templates whose structure can
materially change harness behavior or framework rollout.

Use `docs/templates/global-agents-qa-checklist.md` before changing
`templates/global/AGENTS.md`. It is a companion process doc, not a tracked
template row, unless it later becomes a reusable template with consumers.

## Current Scope

The registry is deliberately focused on high-leverage surfaces:

- `templates/global/AGENTS.md`
- `docs/skills/templates/SKILL_TEMPLATE.md`
- `docs/skills/templates/METHOD_REFERENCE_TEMPLATE.md`
- `skills/skill-creator/references/EVAL_TASK_TEMPLATE.json`
- `docs/skills/templates/QA_CHECKLIST_TEMPLATE.md`
- `tickets/templates/ticket.md`
- `tickets/templates/goal-loop/program.md`
- `skills/harness-creator/templates/project-harness.md`
- `skills/init-advisor/references/MANIFEST_TEMPLATE.json`
- `docs/templates/HUMAN_REPORT_TEMPLATE.md` (prototype consumer only)

Each tracked template declares:

- `template_id`
- `template_version`
- `feature_refs`
- optional `consumer_scope`
- optional `applies_to`

`path` is added by the generator so the UI and validators can resolve the
template row back to source.

Consumers declare template adoption with one field:

```yaml
template_uses:
  skill-template: "0.3.2"
  skill-eval-task: "0.1.0"
```

JSON consumers use the same shape:

```json
{
  "template_uses": {
    "farplane-framework": "1.2.0"
  }
}
```

The rollout report lives in
`skills/skill-maintenance/graph/skill-template-intelligence.json` under
`template_rollout_summary` and `template_rollout`.

`HUMAN_REPORT_TEMPLATE.md` is deliberately at prototype scope. It defines the
shared human reading spine and proof boundary, but no live report-producing
skill has adopted it yet. Expand `consumer_scope` and `applies_to` only after a
representative prototype passes review and a rollout wave is accepted.

## Commands

```bash
python3 bin/validators/sync_template_registry.py --write
python3 bin/validators/sync_template_registry.py --check
python3 bin/validators/check_template_version_metadata.py --all
```

## Boundary

This is not broad document versioning. Add a template only when there is a real
consumer set and the rollout answer matters, such as current/stale/missing
skills or projects.
