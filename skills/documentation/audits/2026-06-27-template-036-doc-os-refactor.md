---
skill: documentation
date: 2026-06-27
change_type: structure
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/documentation/SKILL.md
after_ref: skills/documentation/SKILL.md
reasoning_basis: proof_advisor
proof_artifacts:
  - docs/systems/documentation-os.md
  - skills/documentation/eval_task.json
  - skills/documentation/references/doc-architecture.md
  - skills/documentation/references/metadata-and-registries.md
  - skills/documentation/references/feature-system-specs.md
  - skills/documentation/references/finish-gate.md
eval_required: yes
---

# Documentation Template 0.3.6 And Documentation OS Refactor

## Change

- Before: `documentation` used `skill-template: "0.3.0"`, declared one method
  without a method reference, and carried feature/system/metadata/doc architecture
  detail in first load.
- After: `documentation` uses `skill-template: "0.3.6"`, exposes four branch
  method references, and points durable documentation architecture to
  `docs/systems/documentation-os.md`.
- Why: normal documentation invocation should load the executable workflow first
  and branch into deeper docs architecture only when the task needs it.
- Tradeoff accepted: branch references add files, but keep first-load behavior
  smaller and more precise.

## First-Principles Reasoning

- Objective: keep the documentation skill executable while preserving docs-as-code
  governance.
- Placement logic: system-level lore belongs in Documentation OS; skill
  references own conditional methods; `SKILL.md` owns trigger, routing, gates,
  and output.
- Expected behavior delta: agents select the correct documentation branch instead
  of reading all metadata, feature/system, and finish-gate rules every time.
- Proof needed: registry sync, doc refs, skill validation, and skill-local eval
  rows for the key behavior boundaries.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` keeps trigger, signature, branch choice, gates, and output. |
| `reference_load_precision` | pass | Each method reference has a named load condition in Todo and Reference Map. |
| `missing_context_rate` | pass | Documentation OS and selected refs preserve moved detail. |
| `noisy_context_rate` | pass | Feature/system, metadata, and finish-gate detail moved out of first load. |
| `duplicated_instruction_count` | pass | System lore and executable methods now have distinct owner surfaces. |
| `prompt_size_tokens` | pass | First-load skill is materially smaller and branch-oriented. |
| `maintenance_locality` | pass | Future doc architecture edits have Documentation OS and method refs. |
| `composition_clarity` | pass | Signature, branch refs, proof route, and output are explicit. |

## Proof Artifacts

- Skill-local evals: `skills/documentation/eval_task.json`.
- Structure evals: static eval rows added for future harness use.
- Reviewer receipt: not requested for this local refactor.
- Validators: passed `python3 docs/features/validate_features.py --write`,
  `python3 skills/skill-maintenance/scripts/check_skills.py --write`,
  `python3 bin/validators/check_doc_refs.py`, and
  `python3 bin/validators/check_doc_parity.py`, and
  `python3 skills/eval/scripts/check_eval_queries.py --root .`.
- Eval required: yes, query lint passed for new rows.
- Evidence gaps: no live eval harness run in this pass unless available.

## Before Behavior

- The skill could over-load documentation architecture detail even for small doc
  edits and did not expose real method references for its method declaration.

## After Behavior

- The skill routes doc architecture, metadata/registry, feature/system specs, and
  finish-gate behavior through explicit branch references.

## Followups

- Run the documentation eval rows in a proper skill eval harness when available.
