---
kind: project-evals
status: draft
project: Farplane
created_at: 2026-06-15
updated_at: 2026-06-15
framework_template_version: "0.1.0"
owner: harness
---

# Farplane Evals

## Project Framework Checks

```text
check_farplane_project_files()
  -> validates farplane/manifest.json, farplane/steer.config.toml,
     farplane/bindings.md, optional farplane/pm.json, retired names, and
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
  `farplane/steer.config.toml`, `farplane/bindings.md`, and `farplane/evals.md`,
  plus optional `farplane/pm.json` for UI thread grouping and ignored
  `.farplane/` runtime state.
- `deep-init-project` with `harness_depth != none` calls the harness phase and
  produces concrete unblock tickets for missing bindings or feedback loops.
- Pulse chooses at most one bounded action per beat and embeds simple local
  ticket selection instead of calling a separate ticket drainer.
- Steer compares current time to cached `next_due_at` values, runs due planning
  jobs, writes date-stamped reports, and updates scheduler state without
  mutating tracked config.
