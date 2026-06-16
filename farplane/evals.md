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
  -> validates farplane/manifest.json, farplane/automations.md,
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
  `farplane/automations.md`, `farplane/bindings.md`, and `farplane/evals.md`,
  plus optional `farplane/pm.json` for UI thread grouping and ignored
  `.farplane/` runtime state.
- `deep-init-project` with `harness_depth != none` calls the harness phase and
  produces concrete unblock tickets for missing bindings or feedback loops.
- Ticket drainer ignores Notion when local tickets are proceedable.
- Weekly PM reuses fresh reports from the run ledger instead of duplicating
  jobs.
