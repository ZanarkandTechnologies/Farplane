---
skill: skill-maintenance
date: 2026-08-23
change_type: maintenance
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: types/farplane_skill_contracts + bin/core/skill_frontmatter.py
after_ref: bin/core/skill_contract.py + farplane validate frontmatter
reasoning_basis: first_principles
proof_artifacts:
  - bin/core/skill_contract.py
  - bin/validators/check_doc_frontmatter.py
  - bin/tests/test_farplane_frontmatter_validation.py
eval_required: no
---

# Skill Contract And Frontmatter Validation

## Change

- Before: the strict skill type and its YAML parser were separate modules; no
  single CLI command exposed the owners of all static skill/document metadata.
- After: `bin/core/skill_contract.py` owns strict skill types, parsing, and
  normalization. `farplane validate frontmatter [skills|docs|all]` routes to
  the relevant owner validators.
- Why: one static-contract import path eliminates the `types/` shim, while
  retaining dedicated validators for document families with distinct schemas.
- Tradeoff accepted: generic docs receive syntax/duplicate-key linting; only
  registered document families receive semantic field validation.

## First-Principles Reasoning

- Objective: one owner for static skill metadata and one discoverable lint
  entrypoint without conflating runtime capability-profile policy.
- Placement logic: Core owns shared parsing/contracts; validators own
  deterministic family checks; CLI only routes existing validators.
- Expected behavior delta: `farplane validate frontmatter all` reports skill,
  document syntax, feature/system, template, and source-record results.
- Proof needed: contract consumers import only the Core module; each routed
  validator passes; Git gates select the focused contract suite.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | No global prompt or new skill added. |
| `reference_load_precision` | pass | Docs syntax lint is generic; semantic validation remains family-owned. |
| `missing_context_rate` | pass | CLI reports every selected validator and its output. |
| `noisy_context_rate` | pass | Three scopes: `skills`, `docs`, `all`. |
| `duplicated_instruction_count` | pass | Old `types/` package and parser module removed. |
| `prompt_size_tokens` | pass | No prompt changes. |
| `task_success_rate` | unknown | No behavior eval applies to deterministic validation routing. |
| `review_tas_rate` | unknown | Pending reviewer receipt. |
| `maintenance_locality` | pass | Contract lives in `bin/core`; checks remain in validators. |
| `composition_clarity` | pass | CLI delegates rather than reimplementing validation. |

## Proof Artifacts

- Validator: `python3 bin/farplane.py validate frontmatter all --json` passed
  six checks: skill contract; document syntax; feature/system records;
  template registry; template metadata; source registry.
- Structure: 62 focused unit tests passed; `check_skills.py --write` and
  `sync_skill_plugins.py --check` passed.
- Reviewer receipt: `TAS-A`, pass. No stale contract imports or scope leaks;
  runtime capability profiles remain a separate Core policy module.
- Eval required: no; deterministic validators and unit tests cover the change.
- Evidence gaps: none known.

## Followups

- Runtime capability profiles remain in `bin/core/farplane_capability_profiles.py`.
- Add a semantic document validator only when a new documented family has a
  stable schema; do not force generic prose into one type.
