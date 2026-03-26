# Runtime Debugging Skill Maintenance Rules

## Scope

Applies to files in this directory:

- `SKILL.md`
- `README.md`
- `references/*.md`

## Boundaries

- Keep `SKILL.md` focused on routing and the first-load workflow, not detailed playbooks.
- Route UI-first debugging to `visual-qa` instead of duplicating browser workflows here.
- Route broad testing strategy to `testing` and shell-heavy execution patterns to `bash-efficiency`.
- Keep bug-class strategies in `references/*.md`, one file per mode.

## Conventions

- Keep the first-load workflow compact and executable.
- Prefer concrete trigger language over generic advice.
- Keep the output contract stable so agents produce consistent debugging sessions.
- Reference durable runtime-debugging rules with `MEM-0001` when changing boundaries.
- Reference `MEM-0003` when changing the router-vs-reference split.

## Required Checks After Edits

- Frontmatter in `SKILL.md` remains valid and includes `name`, `version`, `description`, and `allowed-tools`.
- Trigger conditions, workflow, decision branches, gotchas, and outcome contract are all present.
- The boundary with `visual-qa` remains explicit.
- Every reference file is directly linked from `SKILL.md`.

## Testing Expectations

- Re-read `SKILL.md` to ensure an agent can execute it without opening other files.
- Validate all linked references exist and remain one level deep from `SKILL.md`.
- Confirm the workflow still distinguishes obvious stack-trace fixes from runtime-evidence investigations.
