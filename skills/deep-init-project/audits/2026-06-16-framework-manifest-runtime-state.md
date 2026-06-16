---
skill: deep-init-project
date: 2026-06-16
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/deep-init-project/SKILL.md
after_ref: skills/deep-init-project/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - bootstrap fixture tree from `bash skills/deep-init-project/scripts/bootstrap.sh "$tmpdir"`
  - `python3 bin/validators/check_farplane_project_files.py`
  - direct function run of `bin/validators/test_check_farplane_project_files.py`
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write`
eval_required: no
---

# Skill Audit

## Change

- Before: `deep-init-project` source scaffolded tracked `farplane/*.md` files
  and `farplane/pm.json`, but the installed copy was stale, `.farplane/` was
  only gitignored, and there was no concise Farplane project spec manifest.
- After: the skill scaffolds `farplane/manifest.json`, seeds ignored
  `.farplane/` runtime folders and `state/run-ledger.json`, creates the starter
  PRD handoff ticket, documents the tracked/runtime split, validates the
  manifest, and the installed copy has been refreshed.
- Why: the bootstrap contract should make Farplane's important project files
  visible and repeatable instead of relying on prose or hidden chat memory.
- Tradeoff accepted: the manifest is JSON with a single `spec_version` for
  version tracking and migration checks, while richer semantics stay in
  Markdown.

## First-Principles Reasoning

- Objective: make new or migrated projects visibly Farplane-shaped by default.
- Placement logic: `deep-init-project` owns bootstrap scaffolding, so source
  skill references and `bootstrap.sh` are the owner surfaces; validators enforce
  the high-signal invariant.
- Expected behavior delta: a fresh bootstrap produces tracked `farplane/`
  framework config, ignored `.farplane/` runtime state, `tickets/`, and a
  starter PRD ticket instead of treating PRD authoring as part of init.
- Proof needed: generated fixture tree contains the new files, project-file
  validator passes, validator tests pass, skill registry/checklist validation
  passes, and installed copy includes the updated instructions.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` names `farplane/manifest.json`, `.farplane/`, tickets, optional stack scaffolding, and the starter PRD handoff in numbered todos. |
| `reference_load_precision` | pass | `MANIFEST_TEMPLATE.json` is referenced from `SKILL.md` and copied by `bootstrap.sh`. |
| `missing_context_rate` | pass | The tracked/runtime split is documented in `SKILL.md`, README, and framework docs. |
| `noisy_context_rate` | pass | The manifest is concise; semantic detail remains in Markdown docs. |
| `duplicated_instruction_count` | pass | JSON owns the versioned manifest; Markdown owns explanations. |
| `prompt_size_tokens` | pass | First-load additions are short and directly operational. |
| `task_success_rate` | pass | Bootstrap fixture emitted `farplane/manifest.json`, `.farplane/` runtime files, and `tickets/TASK-0001/ticket.md`. |
| `review_tas_rate` | unknown | No separate reviewer lane was run for this narrow same-scope correction. |
| `maintenance_locality` | pass | Future scaffold changes route to `skills/deep-init-project/references/MANIFEST_TEMPLATE.json` and `bootstrap.sh`. |
| `composition_clarity` | pass | Skill signature already declares Farplane config and ticket outputs; manual steps now name concrete files. |

## Proof Artifacts

- Skill-local evals, when needed: not required.
- Structure evals, when needed: not required.
- Reviewer receipt: skipped; native reviewer spawning is available only when
  the user explicitly asks for subagent delegation in this thread, so review is
  limited to self-check plus validators.
- Validator:
  - `python3 bin/validators/check_farplane_project_files.py` -> pass.
  - direct function run of `bin/validators/test_check_farplane_project_files.py`
    -> pass.
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write` -> pass.
- Eval required: no.
- Evidence gaps: `python3 -m pytest ...` could not run because `pytest` is not
  installed in the active Python; test functions were run directly instead.
  No native reviewer receipt was produced because subagent spawning is gated by
  explicit user delegation in the available tool contract.

## Before Behavior

- Fresh bootstrap did not create a concise framework manifest.
- Fresh bootstrap did not seed `.farplane/` runtime files.
- The installed skill omitted newer `farplane/` setup instructions.

## After Behavior

- Fresh bootstrap creates `farplane/manifest.json`.
- Fresh bootstrap creates `.farplane/README.md`,
  `.farplane/state/run-ledger.json`, `.farplane/reports/`,
  `.farplane/evals/runs/`, and `.farplane/logs/`.
- Fresh bootstrap creates `tickets/TASK-0001/ticket.md` as the PRD handoff.
- The installed skill now includes the updated instructions and script.

## Followups

- Use `spec_version` as the semver release line for Farplane project scaffold
  changes. Archive old manifest snapshots when the spec bumps; keep the current
  manifest focused on the current standard tracked/ignored paths.
