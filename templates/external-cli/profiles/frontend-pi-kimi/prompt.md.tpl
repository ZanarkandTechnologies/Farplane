# Delegated Builder Run

Profile: {{profile_name}}
Adapter: {{adapter}}
Model: {{model}}
Run ID: {{run_id}}
Ticket: {{ticket_ref}}

## Delegate Rules

{{append_system}}

## Task

{{prompt}}

## Ticket Context

{{ticket_context}}

## Mounted Skills

Use only the directly relevant mounted skills:

{{skill_list}}

## Attachments

{{attachment_list}}

## Output Contract

Write the final handoff to:

```text
{{handoff_path}}
```

Use the exact headings `## Changed Files`, `## Verification`, and
`## Risks / Followups`, with non-empty bodies. Do not claim final Farplane
completion.
