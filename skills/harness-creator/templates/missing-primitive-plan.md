---
kind: missing-primitive-plan
status: draft
created_at: TODO
---

# Missing Primitive Plan

| Gap | Why It Matters | Current Coverage | Recommended Action | Owner | Trigger Criteria | Proof |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  | use_existing / add_reference / create_ticket / create_skill / create_tool_connector / add_eval / add_validator / add_subagent / defer_until_pilot |  |  |  |

## Creation Gate

Create a new skill only when:

- the trigger is stable;
- the workflow repeats beyond one goal;
- existing skills, templates, tickets, or references are insufficient;
- the output and proof surface are explicit;
- registry validation and review can check it.

Otherwise, prefer a ticket, reference, connector note, eval, validator,
subagent boundary, or defer-until-pilot.

## Feedback Primitive Implementation Plan

Use this section when the missing primitive is the metric or feedback source
needed to make the harness honest.

```text
feedback_primitive_implementation_plan {
  capability:
  owner_surface: existing_skill | project_local_skill | root_skill | ticket | connector | defer
  trigger:
  input_ids_or_export_shape:
  official_or_source_grounding:
  private_env_keys:
  non_secret_bindings:
  kpi_rows:
  storage_path:
  scripts:
    check_config:
    fetch_or_import:
    normalize:
    validate_payload:
  eval_rows:
  guardrail_branches:
  blocked_mode_proof:
  live_proof_command:
  interval_update_binding:
  ui_snapshot_check:
}
```

Minimum viable feedback primitive:

- a skill or ticket owner;
- non-secret binding rows and private setup keys;
- one fetch/import path that writes normalized observations;
- one blocked-mode proof that does not leak secrets or invent metrics;
- one live-proof command to run after access exists;
- eval rows for agent branch choice when the workflow is skill-like;
- KPI registry rows only for metrics the UI should render.
