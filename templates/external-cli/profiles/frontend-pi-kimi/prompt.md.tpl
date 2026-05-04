# Delegated Frontend Run

Profile: {{profile_name}}
Adapter: {{adapter}}
Model: {{model}}
Run ID: {{run_id}}
Ticket: {{ticket_ref}}

## Delegate System Rules

{{append_system}}

## Task

{{prompt}}

## Ticket Context

{{ticket_context}}

## Skill Bundle

Use these frontend skill paths when relevant:

{{skill_list}}

## Output Contract

Write the final handoff here:

```text
{{handoff_path}}
```

Follow the handoff template. Include changed files, behavior built,
verification commands/results, risks, and follow-ups.

## Boundaries

- Codexter remains final reviewer and integrator.
- Preserve unrelated changes.
- Do not push, deploy, publish, or perform destructive actions.
- Do not claim final completion. Produce a builder handoff.
