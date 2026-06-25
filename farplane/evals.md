---
kind: project-evals
status: draft
project: Farplane
created_at: 2026-06-15
updated_at: 2026-06-25
framework_template_version: "0.1.0"
owner: harness
---

# Farplane Evals

## Project Framework Checks

```text
check_farplane_project_files()
  -> validates farplane/manifest.json, farplane/bindings.md,
     farplane/products.md, optional farplane/pm.json, retired names, and
     obvious secret leakage

check_harness_invariants()
  -> validates high-value harness rules and project-file conventions
```

## Standard Verification

Run after framework, skill, or docs changes:

```bash
python3 bin/validators/check_farplane_project_files.py
python3 bin/validators/check_harness_invariants.py
python3 bin/validators/check_doc_refs.py
python3 skills/skill-maintenance/scripts/check_skills.py --write
```

## Future Eval Candidates

- A new project bootstrap produces `farplane/README.md`,
  `farplane/manifest.json`, `farplane/harness.md`, `farplane/goals.md`,
  `farplane/products.md`, `farplane/bindings.md`, and `farplane/evals.md`,
  plus optional `farplane/pm.json` for UI thread grouping and ignored
  `.farplane/` runtime state.
- `init-advisor` with `init_mode=full` calls the harness phase and
  produces concrete unblock tickets for missing bindings or feedback loops.
- Pulse chooses at most one bounded action per beat and embeds simple local
  ticket selection instead of calling a separate ticket drainer.
- Daily and Weekly Interval automations write date-stamped reports, plan the
  next bounded window, and do not mutate tracked scheduler config or runtime
  scheduler state.
