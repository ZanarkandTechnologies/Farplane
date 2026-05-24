# Todos

- [ ] Read the selected ticket, linked docs/specs, proof contract, and relevant
  local files before building the delegate prompt.
- [ ] Use [plan](../plan/SKILL.md) when profile choice, checkout mode, live run
  permission, or expected output is not already clear.
- [ ] Identify the minimal context bundle: key files, constraints, output paths,
  acceptance criteria, proof artifacts, and off-limits surfaces.
- [ ] Choose the external profile and mounted skills deliberately; include only
  directly relevant skill context.
- [ ] Run doctor/setup/dry-run before any live CLI run.
- [ ] Use `rules/prompt-engineering.md` for the delegate prompt structure when
  role, constraints, output format, or examples matter.
- [ ] Capture runtime logs, prompt artifact, handoff note, first-write or output
  proof, and optional diff into the ticket evidence surface.
- [ ] Hand the result back to [qa](../qa/SKILL.md), [demo](../demo/SKILL.md), or
  [impl](../impl/SKILL.md) instead of letting the delegate approve itself.
