# Desloppify Skill Maintenance

## Scope

- `SKILL.md`
- `README.md`
- `AGENTS.md`
- `SKILL.md` Important Checklist

## Boundaries

- Keep one public skill name: `desloppify`.
- Keep the two-mode split explicit: main agent delegates once, worker executes
  directly.
- Keep reviewer and completion-gate roles out of `desloppify`; they should not
  own cleanup execution.
- Do not turn this into a hidden autonomy framework or a second review skill.
- Keep review-only work routed to `review`.

## Conventions

- The default main-agent behavior is one bounded worker, not inline endless
  cleanup by the coordinator.
- The worker prompt must explicitly say `use the desloppify skill in worker
  mode` and `do not spawn another worker`.
- Worker mode must stop and return control when `desloppify` requires nested
  `review --run-batches --runner codex` work.
- Exclude guidance should stay conservative: obvious generated/vendor/runtime
  paths only unless the operator approves more.
- Keep the first-load contract self-sufficient; references are optional, not
  required for basic execution.
- Keep the `SKILL.md` Important Checklist as plain natural-language checklist text
  with Markdown links rather than custom parser syntax. See `MEM-0028`.

## Checks

- `SKILL.md` includes triggers, workflow, mode selector, gotchas, and outcome
  contract.
- The boundary with `review` remains explicit.
- The worker-mode instructions still forbid recursive delegation.
- The worker-mode instructions still forbid nested `--runner codex` review
  execution.
- The install commands still use `desloppify[full]` and `update-skill codex`
  unless the CLI contract changes upstream.

## Testing

- Re-read `SKILL.md` once and confirm an agent can execute it without opening
  other files.
- Confirm the README example matches the first-load contract.
- Confirm the public docs inventory still points to this package when the skill
  is meant to be shipped.
