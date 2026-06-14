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
